# WORK ORDER — Full-disk path index

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-MIG-42-2026-09-29 |
| **Date** | 2026-09-30 (HST) |
| **Status** | COMPLETE — PathIndex built 2026-09-30; `path_index` stays off |
| **Owner** | RootRecord |
| **Related** | Agent 42, Wave G. Cleanup and hold-backs. Old home `fs-index` and topic desk `live-directories` in `Solar-Pacific-RootRecord-Server` (`online-safe-20260920`). Migration matrix row 26. |

**Scope:** Add a scoped path index under Pacific `System/PathIndex`. The script lists path and kind for four Ecosystem source trees only. It does not read file bytes. The scheduled job stays off. Out of scope: the old full-machine walk, `print_directory.py`, a file browser, other agents’ functions, and any runtime edit, scan of live trees, service restart, or GitHub change before this draft is accepted and a build is ordered.

This file is the before-documentation. It is not on the active index.

---

## 1. Intent

The old job `fs-index` ran every 15 minutes, including through night sleep. `fs-index/scripts/incremental_fs_index.py` walked `/home/rootrecord`, `/mnt`, `/media`, `/opt`, `/usr`, `/etc`, `/var`, `/srv`, and `/root`. Unchanged directory mtimes reused prior lines. Output was `paths.txt` (path, kind, optional symlink target), `CURRENT.md`, and `state/dir-mtimes.json`, all beside the skill. The last `CURRENT.md` records 1,017,780 paths. `live-directories` is the topic desk only. Its runner is a symlink back to that same script. `print_directory.py` is a separate tool in the same folder: it previews the first 20 lines of text files, including `.env`, hashes files, and installs a Nautilus launcher.

The live system has no path index. Host sampling (`sys-sample.sh`), uptime (`uptime_log.py`), and host desks stay as they are. A full scan would index private paths, which is why this function was not ported.

This function is a scoped index. It records path and kind only, under an allowlist of source trees. Symlink targets are omitted, because a target can name a secret path. File contents are never read.

---

## 2. Current reality

### 2.1 What exists

Folder name: `PathIndex`. Same name in all three places. Domain is System. No lowercase twin and no symlink. No `Logs/` directory on the server. No `master-key.env` keys.

| Item | Location / status |
| --- | --- |
| Server code | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/System/PathIndex/scripts` — not installed. Package name `PathIndex` |
| Database data | `2 - RootRecord-Database/System/PathIndex` — not installed. `paths.txt` and `dir-mtimes.json` only. Runtime output. Not committed |
| Database logs | `2 - RootRecord-Database/Logs/System/PathIndex` — not installed. Counts-only `current.md` |
| master-key.env | No key names. The script does not read secrets and does not open `/home/rootrecord/master/master-key.env` |
| Allowlisted roots | Pacific server `1 - Servers/1 - RootRecord-Pacific-Solar-Server`, `3 - RootRecord-Website`, `5 - RootRecord-Library`, `6 - Android Development` |
| Refused roots | `/`, home, `/etc`, `/root`, `/usr`, `/var`, `/mnt`, `/media`, `/opt`, `/srv`, `0 - Master-Prompt`, `2 - RootRecord-Database`, `4 - RootRecord-Node`, `7 - Client Projects`, `Old repos deleted and merged`, and `/home/rootrecord/master` |
| Stub names | `node_modules`, `.venv`, `venv`, `__pycache__`, `.git` objects. Record the directory. Do not open children |
| Live host tools | `System/scripts/sys-sample.sh`, `uptime_log.py`, `host_desks.py`, `host_hw.py`. Do not edit |
| Old source | `/home/rootrecord/old ollama/old skills/fs-index/` and `live-directories/`. Remote `git@github.com:rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server.git`, branch `online-safe-20260920` |
| Old index file | `paths.txt` is not on disk and is not tracked. `fs-index/state/` is gitignored and empty. `CURRENT.md` is tracked and is the last stats snapshot |
| Shared file at build time | `Automations/scripts/jobs.py` was free at build time. Gated block `path_index` is in the job list, `enabled: False` |
| Shared old file | `origin/ns/apps/core/scheduler.py` is the target of `fs-index/desk/scheduler.py`. Leave the target. Phase 4 removes the symlink entry only |

### 2.2 Completed so far

- [x] Old source read. Full-machine walk identified. Folder and three paths named. Scope limited to four source trees.
- [x] Draft work order written (this file).
- [x] Alexander accepted this draft and said to build (2026-09-30).
- [x] `System/PathIndex` package and `scripts/path_index.py` added.
- [x] Gated `path_index` block in `jobs.py` (`enabled: False`, 900 s).
- [x] Fixture test (no file contents, `/etc` refused) and one allowlisted walk.
- [x] Phase 4 archive, old-repo deletion, and GitHub commit/push.
- [x] Result note on this work order, and the stale Library rows corrected.

### 2.3 Known friction

- The old walk indexed home, `/etc`, and `/root`. The new script refuses any root outside the allowlist and writes no partial index when a root is refused.
- Symlink targets are omitted. Listing a target would publish a private path when a link inside a source tree points outside it.
- `jobs.py` is a shared file. Pause at build time if another agent still owns that edit.
- `fs-index/desk/scheduler.py` and `live-directories/desk/live/incremental_fs_index.py` are symlinks. Archive the symlink entries. Do not delete `origin/ns/apps/core/scheduler.py`.
- `CURRENT.md` is generated stats that were committed in the old repo. Archive it. Do not import it into Pacific, Database, the website, or git.
- Copies under `/home/rootrecord/old ollama/github-history/` are snapshots, not the live old repo. Leave them.

---

## 3. Tasks

Build only after Alexander accepts this draft and says to build. Until then, do not edit runtime files, restart services, send messages, actuate hardware, or spend cloud money.

1. Add `1 - Servers/1 - RootRecord-Pacific-Solar-Server/System/PathIndex/scripts/path_index.py` and the package `PathIndex`. No `config/`. No server `Logs/` directory. No `master-key.env` allowlist, because there are no keys.
2. Default roots are only the four allowlisted trees in section 2.1. A requested root outside that list exits with a non-zero status and does not write `paths.txt`. Do not walk `/`, home, Database, Master-Prompt, Node, Client Projects, or the old-repo archive.
3. Columns are `path` and `kind` (`dir`, `file`, `dir-stub`, `symlink`, `missing`, `error`). No third column. Do not read file bytes, hash files, or store symlink targets. Stub names in section 2.1 are `dir-stub`. Incremental reuse: if a directory mtime matches `dir-mtimes.json` and prior lines exist for that prefix, keep those lines.
4. Write `2 - RootRecord-Database/System/PathIndex/paths.txt` and `dir-mtimes.json`. Write counts-only `2 - RootRecord-Database/Logs/System/PathIndex/current.md` (roots walked, path count, rewalks, reused dirs, stubs, errors). Do not commit those files. Do not list every path inside `current.md`.
5. Propose one gated block in `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Automations/scripts/jobs.py`: id `path_index`, `enabled: False`, `interval_sec: 900`, command `python3` on `path_index.py` with no extra roots. Do not enable it. Do not edit any other job. Do not add `path_index` to the `NightSleep` allow list. If `jobs.py` is still dirty from another agent, pause and name that block as unwritten.
6. Small test, no service restart. Against a temp directory that contains a `.env` file and a `node_modules` child: the `.env` path appears as `file`, its contents do not appear, and `node_modules` is `dir-stub`. A run pointed at `/etc` writes no `/etc` lines and does not replace a good `paths.txt`. Then one walk of the four allowlisted roots into the Database paths above.
7. This function does not depend on another migration Folder. Do not pause for a missing Folder. Do not build any other agent’s function.
8. After the migration works, and before Library updates: copy this function’s old files into `/home/rootrecord/RootRecord-Ecosystem/Old repos deleted and merged/Solar-Pacific-RootRecord-Server/`, keeping the path each file had inside the old repo. Generated data that lived beside that source goes into this archive too, and still does not go into Pacific, Database, the website, or git. After the archive copy is on disk, delete those same files from the old repo on this machine and on GitHub. Commit that deletion and push it. Do not force-push. Do not delete the GitHub repository. If the archive copy fails, do not delete. If another agent is committing that old repo at the same time, pause before the push.
9. Then update this same work order with what landed, the archive path, the GitHub deletion, and the new status. Correct only the Library pages this function made stale. Do not rewrite unrelated work orders.

Phase 4 file list, from checkout `/home/rootrecord/old ollama/old skills` (remote `git@github.com:rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server.git`, branch `online-safe-20260920`):

- Tracked, archive then delete: `fs-index/CURRENT.md`, `fs-index/DAILY.md`, `fs-index/INDEX.md`, `fs-index/SKILL.md`, `fs-index/references/migrate.md`, `fs-index/scripts/incremental_fs_index.py`, `fs-index/scripts/print_directory.py`, `fs-index/desk/scheduler.py` (symlink entry only), `live-directories/DAILY.md`, `live-directories/INDEX.md`, `live-directories/SKILL.md`, `live-directories/desk/README.md`, `live-directories/desk/live/incremental_fs_index.py` (symlink entry only), `live-directories/references/migrate.md`.
- Generated, archive then delete on this machine only: `fs-index/scripts/__pycache__/`. `fs-index/state/` is gitignored and currently empty. `paths.txt` is absent.
- Leave in place: `origin/ns/apps/core/scheduler.py`, and the snapshots under `/home/rootrecord/old ollama/github-history/` that contain `fs-index` or `live-directories`.

---

## 4. Non-goals

- Do not restore the walk of home, `/etc`, `/root`, `/usr`, `/var`, `/mnt`, `/media`, `/opt`, or `/srv`.
- Do not restore `print_directory.py` (content preview, hashing, Nautilus install). Do not open file contents. Do not record symlink targets.
- Do not index `2 - RootRecord-Database`, `0 - Master-Prompt`, `7 - Client Projects`, or `/home/rootrecord/master`.
- Do not add a file browser, a drop runner, or a listening service.
- Do not edit `System/NightSleep`, `sys-sample.sh`, `uptime_log.py`, `host_desks.py`, or `host_hw.py`.
- Do not replace EcoFlow BLE, the poller, Hawaiʻi weather, the globe collector, camera grabs, Kokoro, or `geology_collect.py`.
- Do not send messages, play audio, switch hardware, delete live Ecosystem files, or spend cloud money.
- Do not import logs, samples, last-state files, generated reports, `paths.txt`, mtimes, collected images, radar frames, zip archives of collected data, database dumps, caches, virtualenvs, `node_modules`, or `__pycache__` into Pacific, Database as committed source, the website, or git.
- Do not restore files under `~/.ollama/skills/energy`, automations, or `coms/ssh/local-data-globe`.
- Do not edit other agents’ files. The only shared live file this function may touch, and only as a gated-off block when that file is free, is `Automations/scripts/jobs.py`.
- Do not delete `origin/ns/apps/core/scheduler.py`.
- Do not rewrite unrelated work orders, including `Ecosystem_Migration_Work_Order_WO-ECO-2026-09-27.md`.
- Do not delete the GitHub repository. Do not force-push.

---

## 5. Key file / path reference

| Path | Role |
|------|------|
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/System/PathIndex/scripts` | Server code. Not installed |
| `2 - RootRecord-Database/System/PathIndex` | Database data: `paths.txt`, `dir-mtimes.json`. Runtime. Not committed |
| `2 - RootRecord-Database/Logs/System/PathIndex` | Database logs: counts-only `current.md` |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/System/PathIndex/scripts/path_index.py` | New script. Allowlist only. Path and kind. No file bytes. Add at build time |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/System/PathIndex/` | Package `PathIndex`. Add `__init__.py` only if the script needs the package import |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Automations/scripts/jobs.py` | At build time, one gated block `path_index` (`enabled: False`, 900 s), and only if this file is not already being edited. No other edit |
| `/home/rootrecord/old ollama/old skills/fs-index/` | Old source to archive in phase 4, then delete from that repo |
| `/home/rootrecord/old ollama/old skills/live-directories/` | Topic desk. Archive, then delete with `fs-index` |
| `/home/rootrecord/old ollama/old skills/origin/ns/apps/core/scheduler.py` | Shared scheduler. Leave it |
| `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/fs-index/` | Phase 4 archive path (after the copy succeeds) |
| `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/live-directories/` | Phase 4 archive path for the topic desk |
| `5 - RootRecord-Library/Documentation/00-architecture/Old-Repo-Migration-Matrix.md` | After phase 4, correct row 26 only |
| `5 - RootRecord-Library/Documentation/00-architecture/G1-Scheduler-To-G3-Jobs-Map-2026-09-29.md` | After phase 4, correct the `fs-index` row only |
| `5 - RootRecord-Library/Documentation/00-architecture/Solar-Pacific-Old-Full-TopLevel-Catalog-2026-09-28.md` | After phase 4, correct the `fs-index` and `live-directories` rows only |

---

## 6. Open items

**Additional requirements:**

- Accept this draft before any build. Accepting it accepts the four-root allowlist.
- Separate sign-off before `path_index` is enabled. The scheduled job stays `enabled: False`.
- Phase 4 GitHub deletion waits until the archive copy is on disk, and only for this function’s old files on `Solar-Pacific-RootRecord-Server` branch `online-safe-20260920`.
- If `jobs.py` is still being edited by another agent at build time, pause. Do not write the gated block until that edit is free.

---

## 7. Notes & constraints

- No force-push.
- Secrets stay out of git. This function has no `master-key.env` keys. Never print secret values. Never add a second env file. Never open `master-key.env`.
- Prefer small reversible steps.
- Sign-off gates: no sends, speaker playback, OBS, hardware switching, deletion of live Ecosystem files, or cloud spend. Phase 4 deletion is limited to the old function’s files after the archive copy succeeds. Enabling the 15-minute job stays off until Alexander says so.
- Small test that proves the new behavior: temp tree with a `.env` and `node_modules` shows the path, hides the contents, and stubs `node_modules`; a run pointed at `/etc` writes no `/etc` lines; then one allowlisted walk writes `paths.txt` under Database `System/PathIndex`. No service restart.
- New code wins. There is no live indexer to enhance. Do not copy `incremental_fs_index.py` over a Pacific file.
- Result note (2026-09-30 01:20 HST):
  - Landed: `System/PathIndex/scripts/path_index.py`. Allowlist is Pacific server, Website, Library, and Android. Output `2 - RootRecord-Database/System/PathIndex/paths.txt` (3145 paths) and `dir-mtimes.json`. Counts log `2 - RootRecord-Database/Logs/System/PathIndex/current.md` (rewalks 845, stubs 66, errors 0). `jobs.py` id `path_index`, `enabled: False`, `interval_sec: 900`. Poller was not restarted.
  - Test: a temp tree listed `.env` as `file` and `node_modules` as `dir-stub`. The text `SECRET=hunter2` was absent. `--root /etc` exited 2 and left the sentinel `paths.txt` unchanged. The allowlisted walk wrote no `/etc` lines and no `master-key.env` path.
  - Archived: `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/fs-index/` and `live-directories/`, including `__pycache__` and the two symlink entries. `origin/ns/apps/core/scheduler.py` was not copied.
  - Removed on this machine: `/home/rootrecord/old ollama/old skills/fs-index/` and `live-directories/`. Local commit `46cda95a` on branch `online-safe-20260920`.
  - Removed on GitHub: `Solar-Pacific-RootRecord-Server` branch `online-safe-20260920` commit `46cda95a` (`7763b4e8..46cda95a`). `Solar-Pacific-RootRecord-Server-Old` `main` commit `4c7ff83` (`91503c3..4c7ff83`). Both `fs-index` and `live-directories` return 404 on those branches. Neither repository was deleted. No force-push.
  - Left in place: `origin/ns/apps/core/scheduler.py`, and the snapshots under `/home/rootrecord/old ollama/github-history/` that contain `fs-index` or `live-directories`.

---

*Work order prepared 2026-09-30 HST. Update status when closed.*

---

## Archive / location note

**Active / accepted WOs** — filename when saved:

```text
Full_disk_path_index_Work_Order_WO-MIG-42-2026-09-29.md
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
