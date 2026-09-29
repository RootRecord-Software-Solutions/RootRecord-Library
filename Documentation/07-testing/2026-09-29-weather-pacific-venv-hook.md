# Test record — Weather hook from Pacific with Weather/.venv

| Field | Value |
| --- | --- |
| **Date / time (HST)** | 2026-09-29 01:45–01:59 HST |
| **Change under test** | G2 weather code copied to Pacific `Weather/` (G2 KEPT), git-ignored `Weather/.venv`, `weather_poller` job → Pacific script |
| **State** | **PASS** |
| **Evidence** | `2 - RootRecord-Database/Logs/Migration/g3-weather-archive-evidence-20260929T115429Z.md` (item D) |
| **Commits** | Pacific `b72db19` (01:48, code copy + requirements) · `e977252` (01:49, ensure script + job) |
| **Backup** | `/home/rootrecord/Database/GITHUB/g3-archive.bak-20260929-014552/` |

## How
`Weather/.venv` was built from `Weather/requirements.txt` (the G2 venv freeze). Then one poller restart at 01:49:36.

## Pass criteria
1. One `Weather/scripts/run_poller.py`, running under the Pacific venv.
2. Fresh files under the canonical weather root.
3. 0 tracebacks.

## Result
- MainPID 880218, NRestarts 0. The boot job started weather PID 880724 (single).
- By 01:53: 110 files / 207 MB under canonical `WEATHER/Hawai'i/` (now `Weather/Hawai'i/`), 0 tracebacks, 8 upstream NWS warnings (HTTP 500 / HTML placeholder).
- Reports **PASS** (generated 01:59:13 HST, per WO-SRV pre-reboot checkpoint).
- After the reboot: weather pid 5355 (single, Pacific `.venv`), 39 files since boot, 0 tracebacks.

## Resource impact
Disk: the first pass grew fast (~200 MB in 4 min). Steady dated-archive growth is about 0.23 GB/day (follow-ups evidence 02:44). Retention policy is **PROPOSED** (Pacific `Weather/README.md` §Retention, awaiting sign-off). CPU and memory were not recorded.

## Open items
- Weather retention PROPOSED.
- Whether `Weather/` gets its own repo (data is local only today).
- Weather starts only at poller boot (ON_BOOT): no mid-session auto-recovery.
