# Test record — EcoFlow stale data: Pacific Energy/.venv

| Field | Value |
| --- | --- |
| **Date / time (HST)** | 2026-09-29 ~03:20 HST (read-only recheck 03:39 HST) |
| **Change under test** | Created git-ignored `Pacific/Energy/.venv` from the pinned G2 energy venv freeze (no restart) |
| **State** | **PASS** (data freshness). Battery levels **flagged** (both low; B1 needs a physical check) |
| **Evidence** | WO-SRV entry "03:20 HST — EcoFlow stale data, root cause"; `2 - RootRecord-Database/Energy/soc/*-last.json` (`source: ble`) |
| **Commits** | None (the venv is git-ignored). Fresh BLE samples appear in Database auto-sync commits, e.g. `dc382a2` (03:31, `Energy/samples/read-river2pro-20260929-033119.json`) |
| **Backup** | not applicable (new git-ignored directory) |

## Root cause
Pacific `Energy/` had no `.venv`, so `lib/py` fell back to system python3 without `ecdsa`. eflib was unavailable, every read fell back to the EcoFlow cloud API, and those values were frozen (B2 78%, B1 0% while 168 W out). This was not caused by the rename.

## Pass criteria
`Energy/soc/*-last.json` update with `source: ble` and plausible values.

## Result
- BLE reads resumed at 03:20:31: B2 52.2% → 51.69%, B1 5.25%, `src=ble`.
- Recheck 03:39 HST: `delta2-last.json` soc 47.56 (03:39:05, ble); `river2pro-last.json` soc 5.23 (03:38:10, ble). Data is fresh; B2 is still falling.

## Flags (open)
- **Both batteries are low.** B1 (River 2 Pro) at ~5% needs a physical check.
- Energy arm/disarm and AC hardware tests remain VERIFY PENDING (need approval).

## Resource impact
Not recorded (venv creation only).

## Cleanup confirmation
No test process. BLE owner (`ava-ecoflow-ble`) was not restarted.
