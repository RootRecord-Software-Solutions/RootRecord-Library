# Test record — Database Title-case folder rename (one stack restart)

| Field | Value |
| --- | --- |
| **Date / time (HST)** | 2026-09-29 03:08–03:24 HST (stack stop 03:09:36, start 03:09:39) |
| **Change under test** | `ENERGY→Energy`, `SYSTEM→System`, `WEATHER→Weather`, `GITHUB→Github`, `ROOTRECORD→RootRecord`, `WORKLOG→Worklog`, `intake→Intake` in `2 - RootRecord-Database/` (Alexander 03:03 HST). No symlinks/shims, no data deleted |
| **State** | **PASS** |
| **Evidence** | `2 - RootRecord-Database/Logs/Migration/g3-titlecase-rename-evidence-20260929T130752Z.md` |
| **Commits** | Database `92bd69c` (03:10, 455 renames) · Pacific `1368822` (03:10, 26 code/config files) · docs: Pacific `0b7be45` (03:24, READMEs) · Library `7d2e79b` (03:25) · Database `66cbae7` (03:25, README) |
| **Backup** | `/home/rootrecord/Database/GITHUB/g3-titlecase.bak-20260929-030817/`; docs `/home/rootrecord/Database/GITHUB/g3-titlecase-docs.bak-20260929-032352/` |

## How
The edits were staged and syntax-checked first. Then: `stop-poller-stack.sh` → `rmdir` the empty placeholders + 7 × `mv` → install the 27 staged files (incl. `.gitignore`) → `systemctl --user start rr-rootserver-poller` → relaunch the read-only dashboard. The BLE owner was not restarted.

## Pass criteria
1. `git ls-files` shows 0 paths under the old names, and bulk data stays ignored under the new names.
2. Fresh data is written under the new names.
3. No old-name folder is recreated.
4. Single instance of every service.

## Result
- `92bd69c`: 455 renames (`R`), 0 old-name paths. `check-ignore` holds `/Weather/`, `/RootRecord/`, `/Github/logs/`, `/Energy/state/`, `/Energy/ports/`.
- Fresh data: `Energy/soc` 03:21–03:22 (BLE), `System/samples/sys-20260929-032425.json`, 147 Weather files in 3 min, `Worklog/worklog_current.md` 03:18:48.
- No old names recreated at 03:15 or 03:24.
- Services single: relay 105964 (replies OFF), cam 106033, weather 106159, cloudflared 105450, globe 94778, BLE 3195, dashboard 111257.
- **Side effect:** the restart exposed the resident-warmup OOM loop (NRestarts 11). That is recorded separately as FAIL → fixed ([OOM record](./2026-09-29-oom-flm-warmup-resident.md)). The first stop at 03:08:56 was interrupted, and the old poller was SIGKILLed at TimeoutStopSec.

## Resource impact
Memory pressure came from the OOM side effect, not from the rename. Otherwise not recorded.

## Cleanup confirmation
No test processes. Historical evidence files keep the old names by design.
