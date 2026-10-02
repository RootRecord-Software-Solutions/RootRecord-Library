# EcoFlow BLE reads

Written 1 October 2026, 23:11 HST, from the Pacific files named below. This is the current rule. A work order or Energy README sentence that disagrees with this page is stale.

## Who reads

| Piece | Path | Role |
| --- | --- | --- |
| Timer | user unit `rr-ecoflow-read.timer` | Starts a read 20 seconds after the previous start. `OnBootSec=20`. Enabled. |
| Read | user unit `rr-ecoflow-read.service` | Oneshot. Runs `Energy/scripts/read/leapfrog-read.sh`. Timeout 90 seconds. |
| Pick | `leapfrog-read.sh` | Prefers the pack with the older watt file. If that read fails, tries the other pack. Then rewrites the agent desk via `desk-live.py`. Lock: `/tmp/ecoflow-ble.lock`. |
| Reader | `Energy/lib/read_runner.py` | One pack per run. Writes Database `Energy/watts/<alias>-last.json` and `Energy/soc/<alias>-last.json`. |
| Owner | `ava-ecoflow-ble.service` | Heartbeat process `Energy/scripts/ble/ble-owner.py`. It does not poll the packs. |
| Poller job | `ecoflow_read_cycle` in `jobs.py` | **Off.** `enabled` is false. The timer owns the repeating read. `ecoflow_read_boot` still runs once when a poller process starts. |

The timer is a user unit and linger is off. It runs when the `rootrecord` session is up. A reboot that reaches the desktop starts it. Editing `jobs.py` does not start it, and the poller loads `jobs.py` once at process start.

`prefer_api` stays `0` for Delta 2 and River 2 Pro in `Energy/config/devices.conf`.

## Bluetooth is the reading

A successful read is `source: ble`. If the AC outlet is on and the inverter watt field is empty, those watts may be filled from quota and the source becomes `ble+cloud`. If the outlet is off, empty AC watts are 0. Do not paste a cloud watt number onto an outlet Bluetooth measured as off.

A Bluetooth miss while that pack's watt file is still a `ble` or `ble+cloud` read younger than 3 minutes (`BLE_HOLD_SEC`) does **not** call the EcoFlow API and does **not** rewrite the last files. The process prints `WAITING` and exits 2. One `No discovery started` after a good Bluetooth streak is that case. On 1 October 2026 at 23:09 HST a miss of that kind published Delta 2 as `source: cloud` at 23.86% while Bluetooth had just read about 2%. The next Bluetooth read put 1.73% back. That publish is what this hold stops.

Quota runs only after that 3-minute Bluetooth file is gone. It is labeled `source: cloud`. It is not a success that replaces a live Bluetooth sample.

## Both packs stale

If both `delta2-last.json` and `river2pro-last.json` under Database `Energy/watts/` are missing or at least 3 minutes old (`STALE_SEC`), `leapfrog-read.sh` power-cycles the adapter with `bluetoothctl power off` and `bluetoothctl power on`, waits 2 seconds, then reads. A stamp at `/tmp/ecoflow-ble-adapter-reset` blocks another cycle for 3 minutes. One fresh pack does not reset the radio.

This account cannot restart `bluetooth.service` without a password. A power cycle clears the BlueZ device cache. A firmware wedge on the Realtek RTL8922AU (`hci0`) still needs a reboot or a `bluetoothd` restart. The kernel line `ACL packet for unknown connection handle` means the controller is already dropping the link.

Leapfrog still prefers the older watt file first. As of 2026-10-02 ~01:11 HST, if that preferred read exits non-zero it falls back to the other pack once, then always rewrites the agent desk with `Communications/telegram/scripts/desk-live.py` from the last files. After one pack disappears from the scan, that file stays older, so most retries still hit the same pack until the other file is also stale. The adapter reset remains the recovery for a wedged radio. Do not "fix" it by publishing quota for the pack that failed the scan.

## A pack at 5 percent or less that goes quiet

A last reading of 5 percent or less that is older than 30 minutes is not a live battery and not a radio miss to keep announcing. The voice reports, the desk file, the state slice, and the public power page say that pack discharged and powered off. They do not repeat its watts or call it reporting. A pack above 5 percent that goes quiet is still "out of range." A fresh Bluetooth read clears the powered-off line.

The minute `ENERGY` log uses `B2=off` or `B1=off` for that case. The poller process reads that code when it starts.

## River 2 Pro AC auto-recover

The desk watchdog is `Energy/scripts/watchdog/river2pro-ac-recover.sh`. Its units, `Communications/network/systemd/rr-river2pro-ac-recover.service` and `.timer`, are installed under `~/.config/systemd/user/`; the timer is enabled at about 90 seconds and is a persistent 24/7 rule, not an overnight window. It logs to `Database/Logs/Energy/river2pro-ac-recover.log`.

Current live logic is fresh River SOC≥5% (≤5 minutes) and `ac_ports=false` → `river2pro-ac-on.sh`, with a 120-second cooldown; already-on is a no-op. That no-op was verified with AC already on at about 28.6% SOC. To disable it: `systemctl --user disable --now rr-river2pro-ac-recover.timer`.

Alexander's standing preference is SOC≥5% **or** input≥50W, whichever arrives first, like the BLE poller IDEA. The 50W OR is WIP until Master wires it; Master owns the EcoFlow/BLE path and the ML lane stays clear.

## What not to do

- Do not turn `ecoflow_read_cycle` back on in the poller. Voice and GitHub jobs in that queue were freezing the read. The timer is outside that queue.
- Do not treat `src=cloud` and `STATUS=OK` as a repaired Bluetooth read.
- Do not restart the poller to pick up a `jobs.py` edit unless Alexander asks. Say that the running process still has the old list.
- Do not document this rule only in a chat. The pages that have to match this note are listed in the test record `Documentation/07-Testing/2026-10-01-ecoflow-ble-hold-and-adapter-reset.md`.
