# Test record — Post-reboot: all services

| Field | Value |
| --- | --- |
| **Date / time (HST)** | Boot 2026-09-29 02:28:09 HST; checks ~02:33 HST |
| **Change under test** | Full desk reboot after the G3 cutover (pre-reboot checkpoint list in WO-SRV) |
| **State** | **PASS** (row 12 NPU PARTIAL at the time; closed by the [NPU/FLM record](./2026-09-29-npu-flm-install-validate.md)) |
| **Evidence** | `2 - RootRecord-Database/Logs/Migration/g3-post-reboot-evidence-20260929T123313Z.md` (pre-reboot snapshot `g3-pre-reboot-checkpoint-20260929T120755Z.md`) |
| **Commits** | Library `65d654f` (02:33, WO-SRV post-reboot entry) |
| **Backup** | `/home/rootrecord/Database/GITHUB/g3-post-reboot.bak-20260929-023313/` |

## How
Read-only checks only: no changes, no restarts.

## Pass criteria
Every unit/process from the checkpoint list is up as a single instance on Pacific paths, with fresh data and no G2 duplicates.

## Result
| Check | Result |
| --- | --- |
| Poller | PASS: pid 3226, NRestarts 0. Status 02:31:16 `B2=78% B1=0%` = `delta2-last.json` / `river2pro-last.json` |
| Relay | PASS: pid 4634 (boot job), retry fix `b3754fb` live, 0 × 401. Replies BLOCKED (models) |
| BLE owner | PASS: pid 3195 |
| Globe | PASS: pid 5436 |
| cam_server | PASS: pid 5223 |
| Weather | PASS (upstream WARN): pid 5355, 39 files since boot, 0 tracebacks |
| Ollama | PASS: pid 2476, 12 models |
| cloudflared | PASS: pid 3509 |
| Auto-sync | PASS: Database 5 commits since boot; Pacific/Library/skills clean |
| Dashboard | PASS: 1 × `poller-dashboard.py` (pid 5002) |
| NPU | PARTIAL: `amdxdna` + `/dev/accel/accel0` + firmware OK; `xrt-smi`/`flm` missing then |
| G2 duplicates | PASS: 0 |

Note: the B2 78% / B1 0% readings were later found to be stale cloud values (see the [EcoFlow record](./2026-09-29-ecoflow-stale-data-energy-venv.md)).

## Resource impact
Not recorded.

## Cleanup confirmation
Read-only. No test processes.
