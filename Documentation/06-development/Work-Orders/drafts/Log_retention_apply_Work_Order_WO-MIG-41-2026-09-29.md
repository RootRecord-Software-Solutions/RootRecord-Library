# WORK ORDER — Log retention apply

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-MIG-41-2026-09-29 |
| **Date** | 2026-09-30 (HST) |
| **Status** | COMPLETE — LogRetention built 2026-09-30; `log_retention` stays off (`--dry-run`). Live `--apply` is not signed off |
| **Owner** | RootRecord |
| **Related** | Agent 41, Wave G. Cleanup and hold-backs. Old home `log-cleanup` in `Solar-Pacific-RootRecord-Server` (`online-safe-20260920`). Live policy model: Pacific `Weather/scripts/weather-retention.py` (`weather_retention` stays dry-run and disabled). |

**Scope:** Add log retention under Pacific `System/LogRetention`. The script reports what it would move. `--apply` moves aged log files into `Archive/Previous-Datasets/Logs-<YYYYMM>/` and never deletes. The scheduled job stays off and stays on `--dry-run`. Out of scope: restoring the old unlink script, turning on `weather_retention --apply`, editing `weather-retention.py`, other agents’ functions, and any runtime edit, move, delete, or GitHub change before this draft is accepted and a build is ordered.

This file is the before-documentation. It is not on the active index.

---

## 1. Intent

The old job `log-cleanup/scripts/job.py` ran at 04:20. It unlinked dated or rotated log files older than 7 days and, for a fixed list of live log names, copied the file and truncated the original in place once it passed 2 MiB. It walked only the top level of old Ava log roots. It never removed directories. That unlink is why the function is still missing.

The live system already has the replacement policy on weather data. `weather-retention.py` defaults to `--dry-run`, and `--apply` moves files past their window into `2 - RootRecord-Database/Archive/Previous-Datasets/Weather-<YYYYMM>/`. Nothing is deleted. Job `weather_retention` is `enabled: False` and its command is `--dry-run`. That weather script, that job, and the weather windows stay as they are.

This function applies that same policy to logs under `2 - RootRecord-Database/Logs/`. Aged log files become move candidates. Live writers stay. Nothing is unlinked. The old `job.py` body is not restored.

---

## 2. Current reality

### 2.1 What exists

Folder name: `LogRetention`. Same name in all three places. Domain is System, the same placement as `NightSleep`. No lowercase twin and no symlink. No `Logs/` directory on the server. No `master-key.env` keys.

| Item | Location / status |
| --- | --- |
| Server code | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/System/LogRetention/scripts/log_retention.py` — installed. Package name `LogRetention` |
| Database data | `2 - RootRecord-Database/System/LogRetention/log-retention.json` — written by the 01:00 HST dry-run. Counts and paths only. Runtime output. Not committed |
| Database logs | `2 - RootRecord-Database/Logs/System/LogRetention/log-retention_dry-run_2026-09-30_0100.md` — dry-run report. Runtime output. Not committed |
| Apply destination | `2 - RootRecord-Database/Archive/Previous-Datasets/Logs-<YYYYMM>/`, path mirrored under `Logs/`. Used only by `--apply`. Not a fourth home for the function |
| master-key.env | No key names. The script does not read secrets |
| Live weather retention | `Weather/scripts/weather-retention.py`. Job `weather_retention` at 00:30, `enabled: False`, command `--dry-run`. Do not edit. Do not switch it to `--apply` |
| Live AI log rotate | `System/scripts/plumbing/ai-log-rotate.sh` rotates `inference_current.jsonl`. This function does not touch `.jsonl` |
| Log folders | `2 - RootRecord-Database/Logs/` already has domain folders from waves A–F. No dependency Folder is missing |
| Old source | `/home/rootrecord/old ollama/old skills/log-cleanup/scripts/job.py`. Remote `git@github.com:rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server.git`, branch `online-safe-20260920` |
| Old pre-move file | `origin/ns/apps/core/crons/on_time/log_cleanup.py` in that same checkout. `references/migrate.md` says do not restore that body |
| Shared file at build time | `Automations/scripts/jobs.py` was clean at build time. Gated block `log_retention` is in `ON_AT` |

### 2.2 Completed so far

- [x] Old source read. Live weather dry-run policy identified. Folder and three paths named.
- [x] Draft work order written (this file).
- [x] Alexander accepted this draft and said to build (2026-09-30).
- [x] `System/LogRetention` package and `scripts/log_retention.py` added.
- [x] Gated `log_retention` block in `jobs.py` (`enabled: False`, command `--dry-run`).
- [x] Dry-run test on live `Logs/` (zero moves, zero deletes) and synthetic `--apply` on a temp directory.
- [x] Phase 4 archive, old-repo deletion, and GitHub commit/push.
- [x] Result note on this work order, and the stale Library rows corrected.

### 2.3 Known friction

- The old script deleted files. The new script must not call `unlink`, `rmdir`, or `rmtree`. A move is not a delete: the bytes have to exist at the archive path.
- `--apply` on the live `Logs/` tree moves files. That stays behind a separate sign-off. The scheduled command stays `--dry-run`.
- `jobs.py` is a shared file and is already dirty. Pause at build time if another agent still owns that edit.
- `origin/ns/apps/core/crons/on_time/` holds 27 tracked files. Phase 4 removes only `log_cleanup.py`. The other 26 stay.
- `state/store/log-cleanup.json` is local generated state. It is not on GitHub. Archive it. Do not import it.
- Copies under `/home/rootrecord/old ollama/github-history/` are snapshots, not the live old repo. Leave them.

---

## 3. Tasks

Build only after Alexander accepts this draft and says to build. Until then, do not edit runtime files, restart services, send messages, actuate hardware, or spend cloud money.

1. Add `1 - Servers/1 - RootRecord-Pacific-Solar-Server/System/LogRetention/scripts/log_retention.py` and the package `LogRetention`. No `config/` unless a later need appears. No server `Logs/` directory.
2. Default root is only `2 - RootRecord-Database/Logs/`. Do not scan Ava home paths. Do not walk `Weather/Hawai'i`. Files only. Log-like names only (`.log`, `.out`, `.log.gz`, `.log.N`, `.log.old`). Skip `.jsonl`, `__pycache__`, leveldb, `.config`, and paths containing “local storage”.
3. Dated or rotated logs older than 7 days are move candidates. Age is the `YYYY-MM-DD` in the filename when present, otherwise mtime. Live writers (`*_current.log` and an undated active log) stay. A live `.log` over 10 MB is a copytruncate candidate (10 MB x 5, matching weather retention). The oldest rotation is a move candidate, not a delete.
4. `--dry-run` is the default. It writes a report under `2 - RootRecord-Database/Logs/System/LogRetention/` and changes nothing. The report states that the would-delete count is 0. Last state (counts and paths only) goes to `2 - RootRecord-Database/System/LogRetention/log-retention.json`. Do not commit that JSON or the report.
5. `--apply` moves those candidates to `2 - RootRecord-Database/Archive/Previous-Datasets/Logs-<YYYYMM>/`, mirroring the path under `Logs/`. It does not unlink. It is not the scheduled command. Do not run it against live Ecosystem logs without a separate sign-off.
6. Propose one gated block in `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Automations/scripts/jobs.py`: id `log_retention`, `enabled: False`, `at_times: ["04:20"]`, command `python3` on `log_retention.py --dry-run`. Do not enable it. Do not edit any other job. If `jobs.py` is still dirty from another agent, pause and name that block as unwritten.
7. Small test, no service restart. Dry-run the real `Logs/` tree: the report is written, zero files move, zero files delete. Then `--apply` only against a temp directory outside the Ecosystem: an 8-day-old dated log exists at the temp archive dest and is gone from the source only because it was moved; a young live log is not unlinked. Do not point `--apply` at live `Logs/`.
8. This function does not depend on another migration Folder. Log folders already exist. Do not pause for a missing Folder. Do not build any other agent’s function.
9. After the migration works, and before Library updates: copy this function’s old files into `/home/rootrecord/RootRecord-Ecosystem/Old repos deleted and merged/Solar-Pacific-RootRecord-Server/`, keeping the path each file had inside the old repo. Generated data that lived beside that source goes into this archive too, and still does not go into Pacific, Database, the website, or git. After the archive copy is on disk, delete those same files from the old repo on this machine and on GitHub. Commit that deletion and push it. Do not force-push. Do not delete the GitHub repository. If the archive copy fails, do not delete. If another agent is committing that old repo at the same time, pause before the push.
10. Then update this same work order with what landed, the archive path, the GitHub deletion, and the new status. Correct only the Library pages this function made stale. Do not rewrite unrelated work orders.

Phase 4 file list, from checkout `/home/rootrecord/old ollama/old skills` (remote `git@github.com:rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server.git`, branch `online-safe-20260920`):

- Tracked, archive then delete: `log-cleanup/DAILY.md`, `log-cleanup/INDEX.md`, `log-cleanup/SKILL.md`, `log-cleanup/references/migrate.md`, `log-cleanup/scripts/job.py`, and `origin/ns/apps/core/crons/on_time/log_cleanup.py`.
- Generated, archive then delete on this machine only: `log-cleanup/scripts/__pycache__/` and `state/store/log-cleanup.json`. `log-cleanup.json` is not on GitHub.
- Leave in place: the other 26 files in `origin/ns/apps/core/crons/on_time/`, and the snapshots under `/home/rootrecord/old ollama/github-history/` that contain `log-cleanup`.

---

## 4. Non-goals

- Do not restore `log-cleanup/scripts/job.py` or `origin/ns/apps/core/crons/on_time/log_cleanup.py` into the live tree. Do not unlink, `rmdir`, or `rmtree`.
- Do not edit `Weather/scripts/weather-retention.py`. Do not enable `weather_retention` or switch it from `--dry-run` to `--apply`. Do not change weather retention windows.
- Do not replace EcoFlow BLE, the poller, Hawaiʻi weather, the globe collector, camera grabs, Kokoro, or `geology_collect.py`.
- Do not change `System/scripts/plumbing/ai-log-rotate.sh`. `.jsonl` is out of scope.
- Do not add a night-sleep gate, a file browser, a drop runner, or a full-disk index.
- Do not send messages, play audio, switch hardware, delete live Ecosystem files, or spend cloud money.
- Do not import logs, samples, last-state files, generated reports, collected images, radar frames, zip archives of collected data, database dumps, caches, virtualenvs, `node_modules`, or `__pycache__` into Pacific, Database, the website, or git.
- Do not restore files under `~/.ollama/skills/energy`, automations, or `coms/ssh/local-data-globe`.
- Do not edit other agents’ files. The only shared live file this function may touch, and only as a gated-off block when that file is free, is `Automations/scripts/jobs.py`.
- Do not rewrite unrelated work orders, including `Ecosystem_Migration_Work_Order_WO-ECO-2026-09-27.md`.
- Do not delete the GitHub repository. Do not force-push.

---

## 5. Key file / path reference

| Path | Role |
|------|------|
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/System/LogRetention/scripts/log_retention.py` | New script. Dry-run by default. Move on `--apply`. Never delete. Add at build time |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/System/LogRetention/` | Package `LogRetention`. Add `__init__.py` only if the script needs the package import |
| `2 - RootRecord-Database/System/LogRetention/log-retention.json` | Last state: counts and paths only. Runtime output. Not committed |
| `2 - RootRecord-Database/Logs/System/LogRetention/` | Reports only |
| `2 - RootRecord-Database/Logs/` | The only default scan root |
| `2 - RootRecord-Database/Archive/Previous-Datasets/Logs-<YYYYMM>/` | `--apply` destination. Mirror of the path under `Logs/` |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Weather/scripts/weather-retention.py` | Policy model (dry-run default, move, never delete). Do not edit |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/System/scripts/plumbing/ai-log-rotate.sh` | Live `.jsonl` rotation. Do not edit |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Automations/scripts/jobs.py` | At build time, one gated block `log_retention` (`enabled: False`, 04:20, `--dry-run`), and only if this file is not already being edited. No other edit |
| `/home/rootrecord/old ollama/old skills/log-cleanup/` | Old source to archive in phase 4, then delete from that repo |
| `/home/rootrecord/old ollama/old skills/origin/ns/apps/core/crons/on_time/log_cleanup.py` | Pre-move body. Archive, then delete this file only |
| `/home/rootrecord/old ollama/old skills/state/store/log-cleanup.json` | Old local state. Archive. Do not import. Not on GitHub |
| `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/log-cleanup/` | Phase 4 archive path (after the copy succeeds) |
| `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/origin/ns/apps/core/crons/on_time/log_cleanup.py` | Phase 4 archive path for the pre-move file |
| `5 - RootRecord-Library/Documentation/00-architecture/Old-Repo-Migration-Matrix.md` | After phase 4, correct row 20 and the destructive note that still lists log-cleanup as blocked |
| `5 - RootRecord-Library/Documentation/00-architecture/G1-Scheduler-To-G3-Jobs-Map-2026-09-29.md` | After phase 4, correct the `log-cleanup` row only |

---

## 6. Open items

**Additional requirements:**

- Accept this draft before any build.
- Separate sign-off before `log_retention` is enabled, and a separate sign-off before `--apply` runs on live `2 - RootRecord-Database/Logs/`. The scheduled command stays `--dry-run`.
- Phase 4 GitHub deletion waits until the archive copy is on disk, and only for this function’s old files on `Solar-Pacific-RootRecord-Server` branch `online-safe-20260920`.
- If `jobs.py` is still being edited by another agent at build time, pause. Do not write the gated block until that edit is free.

---

## 7. Notes & constraints

- No force-push.
- Secrets stay out of git. This function has no `master-key.env` keys. Never print secret values. Never add a second env file.
- Prefer small reversible steps.
- Sign-off gates: no sends, speaker playback, OBS, hardware switching, deletion of live Ecosystem files, or cloud spend. Phase 4 deletion is limited to the old function’s files after the archive copy succeeds. `--apply` on live `Logs/` stays off until Alexander reviews a dry-run report.
- Small test that proves the new behavior: dry-run `log_retention.py` against `2 - RootRecord-Database/Logs/`, confirm the report says zero files would be deleted and that no file moved, then run `--apply` only on a temp tree and confirm the aged log exists at the archive dest and the young live log was not unlinked. No service restart.
- New code wins. Enhance nothing that already deletes logs, because no live delete script exists. Do not copy `job.py` over `weather-retention.py`.
- Result note (2026-09-30 01:15 HST):
  - Landed: `System/LogRetention/scripts/log_retention.py` and `System/LogRetention/__init__.py`. Dry-run report `2 - RootRecord-Database/Logs/System/LogRetention/log-retention_dry-run_2026-09-30_0100.md`. State `2 - RootRecord-Database/System/LogRetention/log-retention.json` (`would_delete` 0, scanned 43, would move 0). `jobs.py` id `log_retention`, `enabled: False`, 04:20, command `--dry-run`. Poller was not restarted.
  - Test: temp `--apply` moved `old-2026-09-22.log` and `rotated.log.1` into `Logs-202609/`; both files still had their bytes at the dest. `young-2026-09-29.log` and `live_current.log` stayed. Live `--apply` without `RR_LOG_RETENTION_APPLY` exited 2 and wrote nothing. A second live `--dry-run --no-save` left all 103 log-file paths and sizes unchanged. Would delete: 0.
  - Archived: `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/log-cleanup/` (source plus `__pycache__`), `origin/ns/apps/core/crons/on_time/log_cleanup.py`, and `state/store/log-cleanup.json`. Copies were byte-checked before deletion.
  - Removed on this machine: `/home/rootrecord/old ollama/old skills/log-cleanup/`, `state/store/log-cleanup.json`, and `origin/ns/apps/core/crons/on_time/log_cleanup.py`. Local commit `45842637` on branch `online-safe-20260920`.
  - Removed on GitHub: `Solar-Pacific-RootRecord-Server` branch `online-safe-20260920` contains `45842637` (branch tip when checked: `8e6be6f2`). `log-cleanup` and `log_cleanup.py` return 404 on that branch. `Solar-Pacific-RootRecord-Server-Old` `main` commit `91503c38` (`fa261cba..91503c38`); both paths return 404 on `main`. Neither repository was deleted. No force-push.
  - Left in place: the other files in `origin/ns/apps/core/crons/on_time/`, and the snapshots under `/home/rootrecord/old ollama/github-history/` that contain `log-cleanup`. `weather-retention.py` and `weather_retention` were not changed.

---

*Work order prepared 2026-09-30 HST. Update status when closed.*

---

## Archive / location note

**Active / accepted WOs** — filename when saved:

```text
Log_retention_apply_Work_Order_WO-MIG-41-2026-09-29.md
```

Location when accepted (do not move this file there now):

```text
Documentation/06-development/Work-Orders/
```

**Drafts (not on active index)** — this file stays here until Alexander promotes it:

```text
Documentation/06-development/Work-Orders/drafts/
```

See `drafts/README.md` and WO-WOGEN-001. Do not auto-promote.

**Closed WOs:** set Status → COMPLETE/CLOSED → `git mv` into:

```text
Documentation/06-development/Work-Orders/Complete/
```

Human session logs archive under `Documentation/01-operations/archive/YYYY-Www/` (WO-ARCH) — separate from closed work orders.
