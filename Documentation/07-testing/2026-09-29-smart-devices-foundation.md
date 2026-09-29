# Test record — Smart Devices foundation (WiZ discovery + driver, Tuya passive scan, collector)

| Field | Value |
| --- | --- |
| **Date / time (HST)** | 2026-09-29 13:26–13:33 HST |
| **Tester** | Grok (executor, smart-devices pass) |
| **Change under test** | New Pacific `Energy/Smart-Devices/` (wiz.py, tuya.py, smart_devices_collect.py), gated job `smart_devices_collect` in jobs.py. Architecture: [Smart-Devices-Energy](../00-architecture/Smart-Devices-Energy.md) |
| **State** | Driver + collector **PASS** · real WiZ toggle test **BLOCKED** (no bulbs found) · Tuya plug **BLOCKED** (not on LAN, no `local_key`) · poller job **LANDED, gated OFF** |
| **Evidence** | Database `Energy/Smart-Devices/{wiz,plugs,collector}-last.json` (13:30:37 HST run) |
| **Commits** | Pacific `cd48536` (13:29, .gitignore + wiz.py + tuya.py + example config) · `11e7f2d` (13:33, collector, jobs.py gated job, READMEs) · Database `2818128` (13:33, `Energy/Smart-Devices/*-last.json` + README) · Library `225c36f` (13:37, these docs) |
| **Backup** | `/home/rootrecord/Database/GITHUB/smart-devices.bak-20260929-132525/` |

## What was tested

1. WiZ LAN discovery: broadcast `getPilot` + `registration` (3 s), then unicast `getPilot` sweep of 192.168.1.1–254.
2. `wiz.py` command/restore logic end-to-end against a **mock bulb on 127.0.0.1:38899** (in-process thread), because no real bulb answered.
3. Tuya passive listen on UDP 6666 / 6667 / 7000 for 20 s (no key); TCP 6668 connect probe of the two Espressif hosts.
4. `nmcli dev wifi list` (read-only) for a `SmartLife-XXXX` pairing AP.
5. `smart_devices_collect.py --discover` once, manually.
6. jobs.py gate: job enabled only with `RR_SMART_DEVICES=1`.

## How (exact commands / procedure)

```bash
cd "/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server/Energy/Smart-Devices"
nice -n 10 timeout 20 python3 scripts/wiz.py discover --timeout 3                 # 13:26
nice -n 10 timeout 30 python3 scripts/wiz.py discover --timeout 3 --sweep 192.168.1  # 13:27
ip neigh show dev wlo1
nice -n 10 python3 scripts/wiz.py status 192.168.1.35 ; ... 192.168.1.210        # + TCP connect 6668/80/6053
nmcli -f IN-USE,SSID,BSSID,CHAN,FREQ,SIGNAL,SECURITY dev wifi list
nice -n 10 timeout 40 .venv/bin/python scripts/tuya.py listen --seconds 20         # 13:29
nice -n 10 timeout 60 python3 scripts/smart_devices_collect.py --discover          # 13:30
nice -n 10 python3 - # mock bulb: status -> dim 20 -> off -> temp 4000 -> restore(saved) -> same_state
.venv/bin/python scripts/tuya.py config-check ; .venv/bin/python scripts/tuya.py status bsd01-1
python3 -c 'import jobs ...'  # with and without RR_SMART_DEVICES=1 (sys.dont_write_bytecode)
```

## Pass criteria (written before running)

1. Discovery completes within its timeout and records IP / MAC / module / state for every WiZ responder (0 responders ⇒ BLOCKED, not FAIL).
2. Real bulb: exactly one save → change (≤ 2 s) → restore on ONE bulb, and `same_state(saved, after)` is true. Other bulbs read only.
3. Tuya: no key needed, nothing printed except id / ip / version; desk Wi-Fi untouched.
4. Collector writes 3 valid `*-last.json` files atomically, contains no key material, exits 0.
5. Job is `enabled=False` by default and `True` only with the gate; running poller not restarted.
6. MemAvailable stays > 2 GB; no process left behind.

## Result

| # | Result | State |
| --- | --- | --- |
| 1 | Broadcast: 0 replies (ufw DROP policy drops replies to broadcasts). Sweep: 0 replies on 38899 from any of the 5 live hosts (router .1, Night Owl .33, Delta 2 Wi-Fi .35, phone .192, Espressif .210) | **BLOCKED** — no WiZ bulb on 192.168.1.0/24 answering |
| 2 | Real toggle test **not run** (no bulb). Mock bulb: saved `{state:true, temp:2700, dimming:55}` → dim 20 → off → temp 4000 → restore → read back identical, `same_state` = SAME. Scene / RGB / off restore params correct; JSON-RPC error path raises | mock **PASS** · real **BLOCKED** |
| 3 | Ports 6666/6667/7000 bound, 20 s, **0 packets**, 0 devices (inconclusive: ufw drops inbound broadcasts). .35 and .210 refuse TCP 6668 (not Tuya). No `SmartLife-XXXX` AP visible (plug likely in EZ fast-blink mode). Desk stayed on `Bmwfarm`; no Wi-Fi/NM change | **BLOCKED** |
| 4 | 3 files written 13:30:37 HST; wiz `BLOCKED` count 0 (9.2 s incl. sweep), plugs `BLOCKED` count 0; exit 0; no key fields | **PASS** |
| 5 | default `enabled = False`; with `RR_SMART_DEVICES=1` `enabled = True`; poller 105444 start time unchanged (03:13:28) | **PASS** |
| 6 | see below | **PASS** |

## Resource impact

| When | Load (1/5/15) | MemAvailable | Swap used | Peak RSS |
| --- | --- | --- | --- | --- |
| before | not recorded | 6,754 MB (13:26) | 491 MB | — |
| during | not recorded | 6,791–6,820 MB | 491 MB | not recorded (stdlib scripts, one short process each) |
| after | 2.09 / 1.83 / 1.77 (13:32) | 6,710 MB | 491 MB | — |

## Cleanup confirmation

- [x] no test process left (`pgrep -af "wiz.py|tuya.py|smart_devices"` = only the checking shell itself)
- [x] UDP 6666/6667/7000/38899 sockets closed on exit (in-process `finally`)
- [x] no model loaded; no BLE use; no sudo; no restart; no git writes

## Open items / caveats

- WiZ: confirm bulbs powered, on `Bmwfarm`, and WiZ app *Allow local communication* ON; then run the one real save/dim/restore test (VERIFY PENDING).
- Tuya: plug control BLOCKED until Path A (Smart Life pair + Tuya IoT cloud creds → tinytuya wizard) or Path B (flash Tasmota/ESPHome/OpenBeken). See architecture doc.
- Passive Tuya discovery needs a ufw allow rule for UDP 6666:6667 (Alexander, sudo) — optional.
- `tinytuya` 1.20.0 installed in gitignored `Energy/Smart-Devices/.venv/`.
