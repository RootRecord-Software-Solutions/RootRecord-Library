# Test record — Status viewer: poller-dashboard single-window launcher

| Field | Value |
| --- | --- |
| **Date / time (HST)** | 2026-09-29 02:10–02:23 HST |
| **Change under test** | Read-only `poller-dashboard.py`, single-instance `open-poller-window.sh`, and docs-only Pacific pulls no longer reload the stack |
| **State** | **PASS** |
| **Evidence** | `2 - RootRecord-Database/Logs/Migration/g3-poller-viewer-evidence-20260929T121959Z.md`; WO-GH refresh (02:23 HST) |
| **Commits** | Pacific `884c832` (02:13, dashboard) · `89a8d6d` (02:15, launcher + reload verify) · `4a4107a` (02:16, launcher) · `31fd21e` (02:23, `push-repo-once.sh` docs-only skip) |
| **Backup** | `/home/rootrecord/Database/GITHUB/g3-viewer.bak-20260929-021233/` |

## What was tested
The status window was flashing because every Pacific pull, even docs-only, triggered a stack reload that killed `poller-watch.py`. On top of that, ptyxis `-e` had no hold shell and a G2 autostart entry was still in use.

## How
Relaunched the viewer once, launched a second `open-poller-window.sh`, and watched the journal and the poller PID. `pull_is_docs_only` was tested against past diff ranges.

## Pass criteria
1. Exactly one viewer, and it survives the observation window.
2. A second launch is refused.
3. The poller is not restarted by the viewer.
4. A docs-only diff does not arm a reload; a code/mixed diff still does.

## Result
- 02:15:42 relaunch → pid 938130 (own `ptyxis-spawn` scope). It had run 226 s at 02:19:29: 1 viewer, no new spawns, poller MainPID 933807 unchanged, NRestarts 0.
- Second launch → "viewer already open — leaving it".
- `31fd21e`: eb8f465 docs range = skip; 884c832 / 89a8d6d / mixed = reload.
- After the reboot (02:32:50): exactly 1 `poller-dashboard.py` (pid 5002), started by autostart → Pacific launcher.
- Screenshot: not possible (GNOME Wayland refused capture).

## Resource impact
Not recorded (read-only viewer).

## Cleanup confirmation
The single viewer was left running by design. No test process remained.
