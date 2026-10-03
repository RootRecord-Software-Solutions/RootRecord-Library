# Test record — EcoFlow BLE hold and adapter reset

**Correction 2026-10-02 16:58 HST:** The power-off half of this test is no longer the rule. `leapfrog-read.sh` only runs `bluetoothctl power on` when both watt files are stale. It does not power `hci0` off. The 3-minute BLE hold still stands. See `Documentation/01-Operations/2026-10-01-ecoflow-ble-reads.md`.

**Standing rule 2026-10-03 ~04:42 HST:** River live BLE also needs pack LCD never-off and EcoFlow-app Bluetooth bind. `NeedBindInstallFirst` (auth `04`) yields zero heartbeats even with soft-keep GATT. Full rule in that same ops note; this test record does not re-validate bind.

| Field | Value |
| --- | --- |
| **Date / time (HST)** | 2026-10-01 23:08–23:12 HST |
| **Tester** | Cursor agent, with Alexander |
| **Change under test** | `leapfrog-read.sh` power-cycles `hci0` when both watt files are stale. `read_runner.py` keeps a Bluetooth last-file for 3 minutes instead of publishing quota. |
| **State** | PASS (logic). Live power-cycle path VERIFY PENDING (both packs were fresh, so the script did not fire). |
| **Evidence** | User journal `rr-ecoflow-read.service` 2026-10-01 17:33–23:10 HST. Operations note `Documentation/01-Operations/2026-10-01-ecoflow-ble-reads.md`. |
| **Commits** | none yet |
| **Backup** | not applicable (no file replaced by a copy) |

## What was tested

The age check in `leapfrog-read.sh` and `_hold_last_ble` in `Energy/lib/read_runner.py`. A live Bluetooth failure was not provoked.

## How (exact commands / procedure)

```bash
bash -n "1 - Servers/1 - RootRecord-Pacific-Solar-Server/Energy/scripts/read/leapfrog-read.sh"
python3 -m compileall -q "1 - Servers/1 - RootRecord-Pacific-Solar-Server/Energy/lib/read_runner.py"
```

A fixture shell checked four cases: both files missing (stale), both new (not stale), both 5 minutes old (stale), one new (not stale). Then `_hold_last_ble("delta2")` and `_hold_last_ble("river2pro")` against the live watt files, and `_hold_last_ble("no-such-pack")`.

Earlier the same evening, `bluetoothctl power off` then `power on` succeeded as user `rootrecord` without sudo. `sudo -n systemctl restart bluetooth.service` asked for a password. That check was not the script under test.

## Pass criteria (written before running)

1. `bash -n` and `compileall` succeed.
2. Both files old, or both missing, counts as stale. One fresh file does not.
3. Live Delta 2 and River 2 Pro watt files, both Bluetooth and under 3 minutes, make `_hold_last_ble` true. A missing alias is false.

## Result

- Parse and compile: PASS.
- Fixture: missing stale, fresh not stale, 5 minutes stale, one fresh not stale.
- Live hold: Delta 2 true (about 24 s, `source: ble`), River 2 Pro true (about 1 s, `source: ble`), missing alias false.
- Journal evidence for the bug the hold stops: 23:09:32 `SUMMARY=delta2 … soc=23.86% … src=cloud` after `BleakDBusError … No_discovery_started`. The Bluetooth read before it was about 2%, and the next one at 23:10:16 was `soc=1.73% src=ble`.
- Journal evidence for the wedge the reset is for: 17:33:53–23:03:31, 870 `device not seen` lines, all `mac=DC:06:75:56:AC:1D` (River 2 Pro), zero new samples. The timer was active the whole time.

## Resource impact

| When | Load (1/5/15) | MemAvailable | Swap used | Peak RSS |
| --- | --- | --- | --- | --- |
| before | not recorded | not recorded | not recorded | not recorded |
| during | not recorded | not recorded | not recorded | not recorded |
| after | not recorded | not recorded | not recorded | not recorded |

## Cleanup confirmation

- [x] no test process left (the checks were `bash -n`, a fixture shell, and one Python import)
- [x] ports closed, lock IDLE (the checks did not take `/tmp/ecoflow-ble.lock`)
- [x] no resident model

## Open items / caveats

- The leapfrog power-cycle has not run on a real both-stale stretch yet. VERIFY PENDING until both watt files age past 3 minutes and the journal shows `both packs stale — power-cycling hci0`.
- Restarting `bluetooth.service` still needs a password. The script only power-cycles the adapter.
- Pages updated so they match this rule: this record, `Documentation/01-Operations/2026-10-01-ecoflow-ble-reads.md`, `Documentation/01-Operations/HANDOFF.md`, `Documentation/11-Runtime-Jobs-and-Control/Desk-Automations-and-Service-Windows.md`, `Documentation/15-Domains-and-External-Systems/Smart-Devices-Energy.md`, `Guides & Tutorials/Root-Monitor-Operators-Handbook/Root-Monitor-Operators-Handbook.md`, Pacific `Energy/README.md`, and a dated correction on draft WO-MIG-36.
