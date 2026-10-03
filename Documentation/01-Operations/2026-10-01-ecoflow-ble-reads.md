# EcoFlow BLE reads

Written 1 October 2026, 23:11 HST; standing rule updated 3 October 2026 ~04:42 HST. A work order or Energy README sentence that disagrees with this page is stale.

## Standing rule (2026-10-03)

Two separate failures blocked live River BLE. Both must be clear for `source: ble`.

### 1) Pack LCD sleep kills BLE

When the River LCD times out and the screen goes dark, the pack drops Bluetooth even while it is still discharging. That looks like a radio or auth bug; it is the screen timeout.

- Set the pack LCD to **never off** (Alexander did this on the unit ~04:31 HST 2026-10-03).
- After the first live BLE sample, `Energy/scripts/ble/ble-hold.py` also writes `lcdOffSec=0` via `set_screen_timeout(0)` and re-asserts about every 5 minutes. Do **not** send that write while the session is empty — a config write against a sleeping screen tears the link (`NotConnectedError`).

### 2) `NeedBindInstallFirst` (auth reply `04`) blocks heartbeats

Measured ~04:41 HST 2026-10-03 with packet logging:

1. ECDH public-key exchange and session key succeed.
2. User-id auth (`cmd_id=0x86`, MD5 of `ECOFLOW_ACCOUNT_ID` + River SN) returns payload `04` → `AuthErrors.NeedBindInstallFirst`.
3. Soft-keep (below) latches `authenticated` and keeps GATT open.
4. **Zero** PD / EMS / inverter heartbeat packets arrive.
5. After about 8 seconds the pack disconnects GATT on its own.

So `NeedBindInstallFirst` is **not** harmless “encrypted-session labeling.” Older notes that said that (HANDOFF / Energy README ~2026-10-02) are superseded. Soft-keeping GATT and latching `AUTHENTICATED` on `04` was a lie — measured zero PD packets, pack drops ~8s later. Cloud quota is also not a substitute for `src=ble`.

**Unblock:** bind River over Bluetooth in the EcoFlow app on the same account as `ECOFLOW_ACCOUNT_ID` in `master-key.env` (19-digit user id). If sticky, unbind and re-bind. Then **force-close** the phone app — EcoFlow allows only one BLE client. Master hold: user unit `rr-ecoflow-ble-hold.service`.

Vendor (2026-10-03 ~05:05 HST): `eflib/connection.py` treats `NeedBindInstallFirst` as auth failure again (no fake `AUTHENTICATED`). IoT/auth cmd_set `0x35` packets (including late `0x89`) must not count as “first data packet” auth success. `ble_client.await_session` no longer proceeds on NeedBind. ML1 energy push timer stays disabled until a real `src=ble` sample lands.

### Live pieces (2026-10-03 morning)

| Piece | Role |
| --- | --- |
| `rr-ecoflow-ble-hold.service` | Holds River GATT; samples into layers + watts/soc when fields land |
| `read_runner.py` | BLE only — miss → keep last BLE or `WAITING` / `cloud not used` (no cloud, no `ble+cloud`) |
| `leapfrog-read.sh` | Skips discharged packs (SOC ≤5% and age >30 min); Delta currently treated discharged/powered off |
| `rr-ecoflow-read.timer` | Stopped while hold owns the radio (do not dual-start against the lock) |
| Soft gate | Untouched (`RR_LOCAL_DATA_POLL` left as found) |

Success signal: hold log `sample soc=… src=ble`, and Database `Energy/watts/river2pro_current.json` / `soc/river2pro_current.json` show `source: ble` with a fresh `at`.

### ML1 push every minute (2026-10-03 ~04:44 HST)

Pacific pushes the current Energy soc/watts snapshot straight to ML1 over SSH — not through the poller, not through EcoFlow cloud.

| Piece | Role |
| --- | --- |
| Script | `Energy/scripts/push/ml1-energy-stats.py` |
| Timer | user unit `rr-ml1-energy-stats.timer` (`OnUnitActiveSec=1min`) |
| ML1 JSON | `/home/ubuntu/youtube-stills/energy_current.json` |
| ML1 line | `/home/ubuntu/youtube-stills/energy_current.txt` |
| ML1 home copy | `/home/ubuntu/energy_current.json` (not `radio/state/stage` — mixer deletes `*.json` there) |
| Thumb | `live_picture.py energy` — BLE gauges only, atomic `thumb.png` + `clock.txt` |

Disable thumb refresh with `RR_ENERGY_ML1_THUMB=0`. Soft gate untouched.

**2026-10-03 ~04:50 HST:** First pushes showed River **93% / 41 W** from a stale `source: cloud` file — incorrect. Push and `live_picture` energy mode are now **BLE-only**: cloud → `WAITING`, BLE older than 180 s → blank/stale, discharged quiet pack → `off`. Soft gate untouched. No commit.

## Changelog

2026-10-03 ~04:44 HST: Armed `rr-ml1-energy-stats.timer` — every-minute SSH push of energy_current + energy-mode YouTube thumb to ML1. Soft gate untouched. No commit.

2026-10-03 ~04:42 HST: Packet-logged NeedBind path; documented LCD + bind standing rule above. Soft gate untouched. No commit.

2026-10-03 ~04:38 HST: Soft-keep NeedBind in vendor `eflib/connection.py`. Soft gate untouched. No commit.

2026-10-03 ~04:29 HST: Identified LCD timeout as BLE drop while discharging; hold sets never-off after first live sample. Soft gate untouched. No commit.

2026-10-03 ~04:26 HST: Alexander ordered EcoFlow cloud fallback off. `Energy/lib/read_runner.py` is BLE only. A miss keeps a fresh last BLE file or prints `WAITING` with `cloud not used`. No `source: cloud`, no `ble+cloud` inverter fill, no `prefer_api` cloud path. `rr-ecoflow-ble-hold.service` holds River GATT. Delta at ≤5% quiet >30 min stays discharged/powered off. Soft gate untouched. No commit.

2026-10-02 ~16:58 HST, measured from the watt and soc files, not from the monitor caption. Delta 2 last write is `2026-10-02T15:54:07-10:00`, `source: ble`, SOC 17.12%, AC in 0 W, AC out 0 W, solar 0 W, USB-C 0 W, `charge_source` none. River 2 Pro last write is `2026-10-02T12:25:29-10:00`, `source: cloud`, SOC 59%, solar 139 W, AC out 92 W, USB-C 35 W. That River row is not a field sample. Alexander said around 16:12 that Delta was on the generator; this file does not show generator input. `rr-ecoflow-read.timer` was stopped at 16:29:53 HST and started again about 16:45. One earlier reset had left the adapter powered off (`BleakBluetoothNotAvailableReason.POWERED_OFF`); `bluetoothctl power on` brought it back. `leapfrog-read.sh` no longer runs `bluetoothctl power off`. When both watt files are at least 3 minutes old it runs `bluetoothctl power on` at most once per `STALE_SEC`, then reads. `Energy/scripts/watchdog/ac-force.sh` does not open a session on a fresh sighting when the last BLE sample is older than 180 seconds; it logs `sample_stale` and leaves the radio to the reader. When it does command AC on, it takes `/tmp/ecoflow-ble.lock` and skips if the reader holds it. `Energy/lib/ble_client.py` `_scan` returns on the first advertisement of the MAC instead of waiting out the whole window. Reads after that change still did not write a new file. Delta came back `error_not_found` (Bleak not found after a sighting), not seen, or auth timeout. River came back `NeedBindInstallFirst` and no `soc` inside the 2.5 second grace, so the sample was not kept. Alexander toggled host Bluetooth off for a moment around 16:48; the read after that failed the same way. The timer was left running. No commit.

2026-10-02 ~16:07–16:10 HST: `Energy/lib/read_runner.py` waits 2.5 s after an auth-flag miss and keeps the sample when `soc` is set. `Energy/scripts/read/leapfrog-read.sh` reads Delta before River when River’s last watt `source` is not `ble` or `ble+cloud`; otherwise it still prefers the older watt file and falls back once. Soft gate and live timers were not touched. No commit.

2026-10-02 ~15:16 HST: `Energy/scripts/ble/ble-owner.py` still does not poll GATT. When either `delta2-last.json` or `river2pro-last.json` under Database `Energy/watts/` is older than 30 minutes and `/tmp/ecoflow-owner-wake` is past the same cooldown, the owner runs `Energy/scripts/read/leapfrog-read.sh` once and stamps the wake file. Soft gate and live timers were not touched. No commit.

## Who reads

| Piece | Path | Role |
| --- | --- | --- |
| Timer | user unit `rr-ecoflow-read.timer` | Leapfrog oneshot cadence. **Stopped** while `rr-ecoflow-ble-hold.service` owns `/tmp/ecoflow-ble.lock` (2026-10-03 morning). |
| Hold | user unit `rr-ecoflow-ble-hold.service` | Persistent River GATT + sample loop (`ble-hold.py`). Soft-keeps NeedBind; writes LCD never-off after first live sample. |
| Read | user unit `rr-ecoflow-read.service` | Oneshot. Runs `Energy/scripts/read/leapfrog-read.sh`. Timeout 90 seconds. |
| Pick | `leapfrog-read.sh` | Skips discharged packs. When River’s last watt `source` is not `ble` or `ble+cloud`, reads Delta first then tries River. Otherwise prefers the older watt file and falls back once. Then rewrites the agent desk via `desk-live.py`. Lock: `/tmp/ecoflow-ble.lock`. |
| Reader | `Energy/lib/read_runner.py` | One pack per run. BLE only as of 2026-10-03 ~04:26. Writes Database watts/soc current files. On an auth-flag miss it waits and keeps the sample when `soc` is present. |
| Owner | `ava-ecoflow-ble.service` | Heartbeat process `Energy/scripts/ble/ble-owner.py`. It does not poll GATT. As of ~15:16 HST it may run `leapfrog-read.sh` once when a watt sample is older than 30 minutes and `/tmp/ecoflow-owner-wake` is past cooldown. |
| Poller job | `ecoflow_read_cycle` | **Deleted 2026-10-02.** Repeating read is `rr-ecoflow-read.timer` / ENERGY `delta2_read` + `river2pro_read`. `leapfrog-read.sh` stays for the timer. |

The timer is a user unit with `rootrecord` linger enabled (`linger=yes`). It is persistent and runs 24/7; `OnBootSec=45` starts it after boot. Editing `jobs.py` does not start it, and the poller loads `jobs.py` once at process start.

`prefer_api` stays `0` for Delta 2 and River 2 Pro in `Energy/config/devices.conf`.

## Bluetooth is the reading

A successful read is `source: ble`. If the AC outlet is on and the inverter watt field is empty, those watts may be filled from quota and the source becomes `ble+cloud`. If the outlet is off, empty AC watts are 0. Do not paste a cloud watt number onto an outlet Bluetooth measured as off.

A Bluetooth miss while that pack's watt file is still a `ble` or `ble+cloud` read younger than 3 minutes (`BLE_HOLD_SEC`) does **not** call the EcoFlow API and does **not** rewrite the last files. The process prints `WAITING` and exits 2. One `No discovery started` after a good Bluetooth streak is that case. On 1 October 2026 at 23:09 HST a miss of that kind published Delta 2 as `source: cloud` at 23.86% while Bluetooth had just read about 2%. The next Bluetooth read put 1.73% back. That publish is what this hold stops.

As of 2026-10-03 ~04:26 HST, quota does **not** run after the hold. A BLE miss past `BLE_HOLD_SEC` prints `WAITING` / `cloud not used` and leaves the last files alone. `source: cloud` and `ble+cloud` are off in `read_runner.py`.

## Both packs stale

If both `delta2-last.json` and `river2pro-last.json` under Database `Energy/watts/` are missing or at least 3 minutes old (`STALE_SEC`), `leapfrog-read.sh` runs `bluetoothctl power on` and then reads. It does not power the adapter off. A power-off on 2 October 2026 left `hci0` down and the next passes found no adapter. A stamp at `/tmp/ecoflow-ble-adapter-reset` blocks another power-on check for 3 minutes. One fresh pack does not touch the radio.

This account cannot restart `bluetooth.service` without a password. A power cycle clears the BlueZ device cache. A firmware wedge on the Realtek RTL8922AU (`hci0`) still needs a reboot or a `bluetoothd` restart. The kernel line `ACL packet for unknown connection handle` means the controller is already dropping the link.

As of 2026-10-02 ~16:10 HST, when River’s last watt `source` is not `ble` or `ble+cloud`, leapfrog reads Delta first then tries River. When River already has a live BLE sample it still prefers the older watt file first; if that preferred read exits non-zero it falls back to the other pack once, then always rewrites the agent desk with `Communications/telegram/scripts/desk-live.py` from the last files. After one pack disappears from the scan, that file stays older, so most retries still hit the same pack until the other file is also stale. Do not power the adapter off to recover a miss. Do not "fix" a failed scan by publishing quota for that pack.

## A pack at 5 percent or less that goes quiet

A last reading of 5 percent or less that is older than 30 minutes is not a live battery and not a radio miss to keep announcing. The voice reports, the desk file, the state slice, and the public power page say that pack discharged and powered off. They do not repeat its watts or call it reporting. A pack above 5 percent that goes quiet is still "out of range." A fresh Bluetooth read clears the powered-off line.

The minute `ENERGY` log uses `B2=off` or `B1=off` for that case. The poller process reads that code when it starts.

## River 2 Pro AC auto-recover

The desk watchdog is `Energy/scripts/watchdog/river2pro-ac-recover.sh`. Its units, `Communications/network/systemd/rr-river2pro-ac-recover.service` and `.timer`, are installed under `~/.config/systemd/user/`; the timer is enabled persistently 24/7 with `OnBootSec=45` and `Persistent=true`, not as an overnight window. `rootrecord` linger is enabled (`linger=yes`). It logs to `Database/Logs/Energy/river2pro-ac-recover.log`.

Current live logic (landed ~12:06 HST 2026-10-02): no SOC floor. When AC is off, `river2pro-ac-recover.sh` keeps calling `river2pro-ac-on.sh` every timer tick. Fresh `ac_input_power`≥50W still triggers when the switch is unknown. A stale `ac_ports=false` does not block forever unless fresh AC output (≥10 W) shows the outlet already delivering. Cloud is no longer the recover source for BLE packs. `COOLDOWN_SEC=0` retries every `OnUnitActiveSec=45` tick while AC remains off; AC already on is a no-op. Alexander verified the power-off/recovery path at about 04:30 HST. To disable it: `systemctl --user disable --now rr-river2pro-ac-recover.timer`.

The standing rule is keep trying whenever AC is off, with no SOC floor; retries are every 45-second timer tick with no cooldown. Master owns the EcoFlow/BLE path and the ML lane stays clear.

Measured 2026-10-02, not a new policy. Pre-dawn, River SOC fell to about 0–1.1%. The old recover gate (on only if SOC ≥5% or AC-in ≥50 W) blocked re-enable, and cloudflared and the desk died with power. Last-known before the drop (overnight, not a live read at 11:45): River about 1.1% SOC, Delta 2 about 2.7%. Desk Cursor was offline from about 05:44–05:51 HST through about 11:45 HST; River SOC and AC were unmeasurable from Master in that window. At reconnect (~11:45–11:49 HST) River was about 16% SOC (cloud), AC out about 46 W, USB-C about 20 W (AC appears on); Delta 2 was about 11% with about 71 W solar in. A `river2pro-ac-on` attempt over BLE returned NeedBindInstallFirst / auth failed and did not change the outlet. Recover no-op reason was then `ac_unknown_or_stale` because the `ac_ports` sample was stale from about 05:45. The soft gate was not touched and the poller was not flipped. Alexander ordered ~11:59 HST that the floor be dropped and `ac_ports` plus the BLE bind be refreshed. Landed ~12:06 HST on the desk: `Energy/scripts/watchdog/river2pro-ac-recover.sh`, `Energy/lib/ecoflow_api.py` (cloud `ac_ports`), `Energy/lib/ble_client.py` and `Energy/lib/read_runner.py` (auth failures name the exception class). Live log at ~12:06: `ac_already_on_fresh_output` then `ac_already_on` from `cloud-fallback-river2pro.json` with `ac_out=46`. The 04:30 keep-retry stays. Master landed the BLE/read-side and force-AC portions for `prefer_api=0`. **Paused ~12:32 HST (superseded 2026-10-03):** earlier notes called `NeedBindInstallFirst` “labeling only”; that is wrong — see Standing rule above. Soft gate and live timers were left as they were. Backups are `*.bak-20261002-dual-ac-force`; no commit/push or invented SHA.

## What not to do

- Do not turn `ecoflow_read_cycle` back on in the poller. Voice and GitHub jobs in that queue were freezing the read. The timer is outside that queue.
- Do not treat `src=cloud` and `STATUS=OK` as a repaired Bluetooth read.
- Do not treat `NeedBindInstallFirst` as a successful session. Soft-keep keeps GATT; it does not invent heartbeats.
- Do not leave the EcoFlow phone app on BLE while the hold is supposed to own River (one client).
- Do not write LCD never-off over BLE before the first live sample (sleeping screen + write = link tear).
- Do not restart the poller to pick up a `jobs.py` edit unless Alexander asks. Say that the running process still has the old list.
- Do not document this rule only in a chat. Matching pages: Pacific `Energy/README.md`, this ops note, and the test record `Documentation/07-Testing/2026-10-01-ecoflow-ble-hold-and-adapter-reset.md`.
