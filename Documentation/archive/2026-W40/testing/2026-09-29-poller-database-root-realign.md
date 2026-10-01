# Test record — Poller realigned to the new Database root

| Field | Value |
| --- | --- |
| **Date / time (HST)** | 2026-09-29 01:10–01:25 HST |
| **Change under test** | Poller energy/system-status/log paths → `/home/rootrecord/RootRecord-Ecosystem/2 - RootRecord-Database` (WO-SRV) |
| **State** | **PASS** |
| **Evidence** | `2 - RootRecord-Database/Logs/Migration/g3-poller-realign-evidence-20260929T111731Z.md` |
| **Commits** | Pacific `d9f074b` (01:11, poller paths) · `75d86f2` (01:14, `Github/scripts/common.sh` DATABASE_ROOT) · `f27604d` (01:20, `ensure-relay.sh` LOG quoting) · Database `eabe62e` (01:25, live logs untracked) |
| **Backup** | `/home/rootrecord/Database/GITHUB/g3-poller.bak-20260929-011046/` |

## What was tested
`rootserver_poller.py` `ENERGY_ROOT` and `SYSTEM_STATUS_JSON` defaults, plus the `POLLER_LOG` default in `run-poller.sh`/`open-poller-window.sh` and the user unit, all moved to the new root (env overrides kept).

## How
`py_compile`, `bash -n`, `daemon-reload`, then one `systemctl --user restart rr-rootserver-poller.service` at 01:11:28.

## Pass criteria
1. The status line `src=` points to the new root, and B2 matches the fresh `delta2-last.json`.
2. The `:8799/system-status.json` it serves is the new-root file.
3. One poller, NRestarts 0.

## Result
- 01:12:04 `ENERGY status=live B2=85% … src=…/2 - RootRecord-Database/ENERGY`. `delta2-last.json` soc=85.0 @01:12:05 → match.
- Served `system-status.json` = new-root file (generated_at 01:12:06 HST) → match.
- MainPID 804007, NRestarts 0, one poller and one cloudflared. The old-root log was last written at 01:11:41.
- Follow-ups: common.sh **LANDED** (`75d86f2`). The relay failed at the 01:19 reload (unquoted path) and was fixed in `f27604d`. Live logs untracked **PASS** (`eabe62e`).
- Note: the path was `ENERGY/` at the time. Since 03:09 HST it is Title-case `Energy/` (see the [Title-case rename record](./2026-09-29-database-titlecase-rename.md)).

## Resource impact
One restart. The old PID ignored SIGTERM and was SIGKILLed at the 30 s TimeoutStopSec (cause later fixed, see WO-SRV follow-ups 02:50). Load and memory were not recorded.

## Cleanup confirmation
No test process was started. The single poller and cloudflared were confirmed.
