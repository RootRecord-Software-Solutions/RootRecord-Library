# Smart Devices in Energy (WiZ bulbs + Tuya BSD01 plugs)

| Field | Value |
| --- | --- |
| **Date (HST)** | 2026-09-29 13:25–13:40 HST |
| **Author** | Grok (executor, smart-devices pass) for Alexander |
| **State** | Foundation **LANDED** · collector **PASS** (manual) · poller job **gated OFF** · WiZ real-bulb test **BLOCKED** (none found) · plug control **BLOCKED** (no `local_key`) |
| **Pacific code** | `Energy/Smart-Devices/` (`scripts/wiz.py`, `scripts/tuya.py`, `scripts/smart_devices_collect.py`, `config/`, `README.md`) |
| **Database** | `2 - RootRecord-Database/Energy/Smart-Devices/{wiz,plugs,collector}-last.json` |
| **Test record** | [07-testing/2026-09-29-smart-devices-foundation.md](../07-testing/2026-09-29-smart-devices-foundation.md) |
| **Idea** | [08-ideas/2026-09-29-smart-plug-load-shedding.md](../08-ideas/2026-09-29-smart-plug-load-shedding.md) |
| **Backup** | `/home/rootrecord/Database/GITHUB/smart-devices.bak-20260929-132525/` |

## Purpose

Local (LAN-only, no cloud at runtime) status and — later — control of Wi-Fi smart devices that belong to the Energy picture:
lights and plugged loads that could be dimmed or shed when the EcoFlow packs (Delta 2 B2/B3, River 2 Pro) run low.
This pass builds the drivers, a read-only collector and the data contract. **Nothing switches automatically.**

## Devices

| Device | Protocol | Local API | Status on 2026-09-29 13:30 HST |
| --- | --- | --- | --- |
| **WiZ smart bulbs** ("waze bulbs") | Wi-Fi 2.4 GHz | UDP **38899** JSON: `getPilot`, `setPilot`, `getSystemConfig`, `registration` | **BLOCKED** — 0 replies (broadcast + unicast sweep of 192.168.1.1–254) |
| **Unbranded Smart Plug BSD01** (Tuya / Smart Life, ESP8266) ×N, one in pairing mode | Wi-Fi 2.4 GHz | Tuya local TCP **6668** (AES, needs per-device `local_key`), UDP 6666/6667/7000 presence broadcasts | **BLOCKED** — not on LAN yet; no `SmartLife-XXXX` AP visible; no `local_key` |

### LAN inventory seen from the desk (read-only)

Desk: `wlo1` 192.168.1.66/24 on SSID **Bmwfarm** (5.8 GHz, ch 161); gateway 192.168.1.1. `nmap`/`arp-scan` are **not installed**, so the inventory is `ip neigh` after the WiZ unicast sweep (which ARP-resolves each host as a side effect).

| IP | MAC | Vendor (OUI) | What it is | WiZ 38899 | Tuya TCP 6668 |
| --- | --- | --- | --- | --- | --- |
| 192.168.1.1 | 74:24:9f:b3:77:70 | TIBRO Corp. | router / gateway | — | — |
| 192.168.1.33 | 54:2b:57:5c:46:48 | Night Owl SP | Night Owl camera DVR/NVR | — | — |
| 192.168.1.35 | 24:58:7c:20:92:60 | Espressif | **EcoFlow Delta 2 (B2)** Wi-Fi (BLE MAC `…:92:61` in `devices.conf`) | no reply | refused |
| 192.168.1.192 | 66:ea:76:5b:86:be | (locally administered / randomised) | phone or laptop with private MAC | — | — |
| 192.168.1.210 | 24:ec:4a:82:43:34 | Espressif | unidentified ESP32 device (likely the other EcoFlow unit); **not** WiZ, **not** Tuya | no reply | refused |

Wi-Fi APs visible (`nmcli dev wifi list`, read-only): only `Bmwfarm` (2.4 GHz ch 11 + 5 GHz ch 36/161) and hidden mesh BSSIDs. **No `SmartLife-XXXX` AP.**
That means the plug in pairing mode is in **EZ mode (fast blink)**, which does not broadcast an AP, or it is out of range / unpowered.
The desk was **not** connected to any AP and no Wi-Fi/NetworkManager setting was changed.

### Firewall note (important for discovery)

`ufw` is active with `DEFAULT_INPUT_POLICY="DROP"` and no user rules. Consequences:

- WiZ **broadcast** discovery replies are dropped (no conntrack match for a reply to 255.255.255.255). `wiz.py discover --sweep 192.168.1` adds a unicast `getPilot` to each host; those replies are conntrack-matched and pass.
- Tuya UDP 6666/6667/7000 presence broadcasts are inbound-unsolicited and are **dropped before any socket sees them**. The 20 s passive listen (0 packets) therefore cannot prove absence. Local Tuya control itself is an **outbound** TCP 6668 connection and works through ufw.
- If Alexander wants passive Tuya discovery: `sudo ufw allow in on wlo1 proto udp from 192.168.1.0/24 to any port 6666:6667` (not done — no sudo, no network changes in this pass).

## Architecture

```text
                    Pacific Energy/Smart-Devices/                      Database Energy/Smart-Devices/
  WiZ bulbs  <-UDP 38899->  scripts/wiz.py (stdlib)  ---+
                                                        +--> smart_devices_collect.py --> wiz-last.json
  BSD01 plugs <-TCP 6668->  scripts/tuya.py (tinytuya, .venv) +   (read-only, nice 10)  --> plugs-last.json
                                 ^ config/tuya-devices.local.json (gitignored: id, ip, local_key, version)  --> collector-last.json
                                                        |
   Automations/scripts/jobs.py EVERY_SECONDS "smart_devices_collect" (300 s) — enabled only if RR_SMART_DEVICES=1 at poller start
                                                        |
   future: Root Monitor  Energy -> Devices page  reads *-last.json (no imports of drivers, no network from the panel)
```

### `wiz.py` (stdlib only)

`discover [--timeout 3] [--sweep 192.168.1]` · `status <ip>` · `on <ip>` · `off <ip>` · `dim <ip> <10-100>` · `temp <ip> <2200-6500>` · `restore <ip> '<saved getPilot json>'`.
Discovery broadcasts `getPilot` and `registration` (`register:false`, read-only) to 255.255.255.255 and 192.168.1.255, then `getSystemConfig` per responder for `moduleName` / `fwVersion` / `mac`.
`restore_params()` rebuilds the exact state from a saved `getPilot` (off → `state:false`; scene → `sceneId`+`speed`+`dimming`; white → `temp`+`dimming`; colour → `r,g,b,c,w`+`dimming`) and `same_state()` verifies it.

### `tuya.py` (scaffold, venv `tinytuya` 1.20.0)

`listen [--seconds 20]` (no key; prints id / ip / version only) · `config-check` (which fields are missing — never values) · `status <name>` · `on <name>` · `off <name>`.
Reads `config/tuya-devices.local.json` (gitignored; template `config/tuya-devices.example.json`). Returns `BLOCKED` until id / ip / `local_key` / version exist. Uses `OutletDevice`, 3 s socket timeout, 1 retry, switch DP 1 (configurable `switch_dp`).

### Gitignore (Pacific `.gitignore`, added **before** any secrets file existed)

```text
Energy/Smart-Devices/config/*.local.json
Energy/Smart-Devices/config/*.secret.json
Energy/Smart-Devices/config/tuya-cloud.env
Energy/Smart-Devices/**/tinytuya.json      # tinytuya wizard: Tuya cloud API key/secret
Energy/Smart-Devices/**/devices.json       # tinytuya wizard: local_keys
Energy/Smart-Devices/**/tuya-raw.json
Energy/Smart-Devices/**/snapshot.json
Energy/Smart-Devices/.venv/
```

Verified with `git check-ignore`. No secrets file exists yet.

## Plugs: two paths to local control

### Path A — keep Tuya firmware, get the `local_key` from the Tuya IoT cloud (recommended first; reversible)

1. Pair the BSD01 in the **Smart Life** app on the **2.4 GHz** side of `Bmwfarm` (ch 11). Fast blink = EZ mode (app default); if EZ fails, hold the button ~5 s more until slow blink = AP mode (phone joins `SmartLife-XXXX`). The desk never joins that AP.
2. Create a free account at **iot.tuya.com** → Cloud → Create Cloud Project (Industry *Smart Home*, Development Method *Smart Home*, Data Center **Western America** for a US/Hawaiʻi Smart Life account). Authorise the *IoT Core* and *Authorization* API services.
3. Project → Devices → **Link App Account** → scan the QR code from Smart Life (Me → ⚙/scan). The plug appears in the device list.
4. On the desk (no secrets printed to chat/logs; all outputs gitignored):
   ```bash
   cd "/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server/Energy/Smart-Devices"
   nice -n 10 .venv/bin/python -m tinytuya wizard      # asks for Access ID / Access Secret / region; writes devices.json (gitignored)
   cp config/tuya-devices.example.json config/tuya-devices.local.json && chmod 600 config/tuya-devices.local.json
   # fill id / ip / local_key / version from devices.json (ip from the router DHCP list or `ip neigh`)
   .venv/bin/python scripts/tuya.py config-check      # expect state READY
   .venv/bin/python scripts/tuya.py status bsd01-1     # read-only first
   ```
   Caveats: re-pairing a plug in the app **changes its `local_key`** (re-run the wizard). Keep the Tuya cloud project alive (trial renewals) only for key retrieval; runtime control is LAN-only.

### Path B — flash Tasmota or ESPHome (no cloud, no keys; not reversible to stock easily)

- Gives a plain local HTTP API (Tasmota: `http://<ip>/cm?cmnd=Power%20On|Off|Status`) and/or MQTT; ESPHome gives its native API/web server.
- Only if the plug really is **ESP8266** (open it / check the module; many newer "BSD01"-style plugs ship **Beken BK7231 (WB2S/CB2S)** — then the tool is **OpenBeken**, not Tasmota).
- Methods: OTA `tuya-convert` (works only on old Tuya firmware; mostly patched) or serial flash with a 3.3 V USB-TTL adapter (TX/RX/GND/3V3, GPIO0 to GND at boot). Mains device — unplug before opening.
- If chosen, add a `tasmota.py` driver beside `wiz.py` (stdlib HTTP) and a `kind:"tasmota"` block in `plugs-last.json`; the collector contract does not change.

**Plug control stays BLOCKED** until Alexander picks A (pair + Tuya cloud credentials) or B (flash).

## WiZ: what is needed to unblock

1. Confirm the bulbs are powered (wall switch on) and on `Bmwfarm` — WiZ app → Settings → Lights → bulb → shows IP and MAC.
2. WiZ app → Settings → Security / Privacy → **Allow local communication = ON** (without it bulbs ignore UDP 38899).
3. Re-run: `nice -n 10 python3 scripts/wiz.py discover --timeout 3 --sweep 192.168.1`, add each bulb to `config/wiz-devices.json` as `"name": {"ip": "...", "mac": "...", "module": "..."}` (DHCP reservation on the router recommended).
4. Then the one reversible test from the test record (save → dim for 2 s → restore → verify) on ONE bulb.

## Relation to the BLE battery owner

- `Energy/scripts/ble/ble-owner.py` (PID 3195 at 13:32 HST) is the single owner of the Bluetooth adapter; EcoFlow reads take short BLE sessions under `flock /tmp/ecoflow-ble.lock`.
- WiZ and BSD01 are **Wi-Fi** devices. Smart-Devices code never imports `bleak`/eflib, never scans BLE, never takes the BLE lock. No BLE scan was run in this pass.
- The two meet only in data: the future load-shedding idea reads `Energy/soc/*-last.json` (BLE-fed) and would act on plugs (Wi-Fi). See the idea doc.

## Future Root Monitor Energy → Devices page (design only; `Apps/Control-Panel/` not touched)

Root Monitor already reads Database JSON through `Apps/Control-Panel/Lib/rr_sources.py` (`read_json(paths.energy / "soc/<dev>-last.json")`). A Devices page would:

1. Add a source function (owned by the Control-Panel agent) such as `smart_devices(paths)` returning `read_json(paths.energy / "Smart-Devices/wiz-last.json")`, `.../plugs-last.json`, `.../collector-last.json` — file reads only; the panel never imports `wiz.py`/`tinytuya` and never opens sockets (keeps RSS under the 80 MB target).
2. Mark data **STALE** when `at` is older than 2 × 300 s (collector interval), and show "gated OFF (`RR_SMART_DEVICES`)" from `collector-last.json.gate_on`.
3. Render two tables: Bulbs (name, ip, on, dimming %, temp K / scene, rssi, state) and Plugs (name, ip, version, on, state; for BLOCKED show `note` / `missing` field names — never key values).
4. Controls (on/off/dim) only later, behind the existing `risky_actions_enabled` + per-action `signed_off` pattern in `settings.json`, executed as a subprocess (`wiz.py on <ip>` / `.venv/bin/python tuya.py off <name>`), one action per click, with the result re-read from the next `*-last.json`.

## Enabling the collector (when wanted)

Add `RR_SMART_DEVICES=1` to the poller's environment and let the next ordinary stack reload pick it up (jobs.py gates are read once at poller start). This pass did **not** restart or modify the running poller (PID 105444).

*Smart-Devices foundation, 2026-09-29 HST.*
