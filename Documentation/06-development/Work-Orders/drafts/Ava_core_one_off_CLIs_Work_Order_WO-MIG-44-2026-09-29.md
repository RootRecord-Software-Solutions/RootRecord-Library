# WORK ORDER — Ava-core one-off CLIs

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-MIG-44-2026-09-29 |
| **Date** | 2026-09-30 (HST) |
| **Status** | OPEN — landed. Phase 4 archive and GitHub deletion done. Not promoted. |
| **Owner** | RootRecord |
| **Related** | Agent 44, Wave G. No other function has to exist before this build. No later function in the agent list depends on this one. Old home: directory printer, uploader, mapper, create_migration, plus the same matrix row's sync, visual CLI, database-root-migrate, and route builder. GitHub `rootrecordsoftwaresolutions/old`, branch `cursor/radio-idle-obs-gates`. Matrix row 87. |

**Scope:** Archive these one-off Ava-core CLIs and leave them out of the live Ecosystem. In scope, after this draft is accepted and Alexander says to build, is a path-preserving copy into `Old repos deleted and merged/old/`, then deletion of those same files on GitHub `old`. Out of scope is a new Folder, any Pacific / Database / Logs / website path, `jobs.py`, running the CLIs, and every file another agent still owns. This file stays in drafts. Do not promote it onto the active index.

---

## 1. Intent

These tools target `/home/ava-core`. The Ecosystem numbered folders replaced that layout, so they are not installed.

- `core_uploader.py` selectively pushes `/home/ava-core` to `Ava-Core-Dev/ava-core`, reading token files under `/home/ava-core/Credentials`. Live replacement: Pacific `Github/scripts` (`push-once.sh`, `poll-and-push.sh`).
- `file_mapper.py` walks `/home/ava-core` and writes `file_mapping.json`. The full-disk index stays with a later agent.
- `create_migration.py` builds a `/tmp/ava_stage` route manifest, per-location SQLite files, and a USGS poller. Weather, Geology, Reports/News, and the country location pollers already cover that work.
- `tools/build-global-routes.py` writes old route HTML from location JSON. Website routes stay with the website.
- `operations/system-tools/database-root-migrate.py` moves SQLite files into `/home/ava-core/database`.
- `operations/system-tools/directory-printer/` scans a tree into a text report and a tree file.
- `operations/system-tools/directory-sync/ava-directory-sync.sh` and `operations/system-tools/sync-ava-directory.sh` rsync `/home/ava-core` onto `Ava-Directory`. The second script uses `rsync --delete`.
- `operations/system-tools/desk/` is the visual CLI plus an audio player aimed at `/home/ava-core/operations/cronologicals/`. Kokoro and `Media/Voice` stay.

EcoFlow BLE, the poller, Hawaiʻi weather, the globe collector, camera grabs, Kokoro, and `geology_collect.py` stay as they are. This function does not replace them.

---

## 2. Current reality

### 2.1 What exists

No new Folder. The function is not installed. Same answer in all three places: none.

| Item | Location / status |
| --- | --- |
| Server code | None. Do not create a path under `1 - Servers/1 - RootRecord-Pacific-Solar-Server/`. |
| Database data | None. Do not create a path under `2 - RootRecord-Database/`. |
| Database logs | None. Do not create a path under `2 - RootRecord-Database/Logs/`. |
| Secrets | None. No key names in `/home/rootrecord/master/master-key.env`. The old uploader read `/home/ava-core/Credentials`. Those files are not copied. No second env file. |
| Old source | GitHub `rootrecordsoftwaresolutions/old`, branch `cursor/radio-idle-obs-gates`. Not present on this machine. `Old repos deleted and merged/old/` does not contain them yet. |
| Live functions to keep | Pacific `Github/scripts`; Weather; Geology; Reports/News; country location pollers; Kokoro; `Media/Voice`; EcoFlow BLE; the poller; Hawaiʻi weather; the globe collector; camera grabs; `geology_collect.py` |

### 2.2 Completed so far

- [x] Old source read on GitHub (uploader, mapper, create_migration, route builder, database-root-migrate, directory printer, both sync scripts, visual CLI readme)
- [x] Confirmed no local checkout contains these files
- [x] Archive copy under `Old repos deleted and merged/old/` (28 files, checksums match)
- [x] Those files removed on GitHub `old` commit `97a2557` (no force-push)
- [x] This work order updated with the archive path and the GitHub commit
- [x] Matrix row 87 corrected from missing to archived

### 2.3 Known friction

- Matrix row 87 writes `old/operations/system-tools/*`. That wildcard also covers Git auto-push and the Grok usage report. Those files stay in the `old` repo. See §4.
- There is no local working tree of `old` that contains these files, so phase 4 deletes them on GitHub only. Nothing else on disk is removed.
- `desk/ava_directory_feature/` contains a nested snapshot of `broadcast.py`. That snapshot is archived with the desk tree. The live `operations/broadcast.py` stays for the file-browser agent.
- `desk-backup-20260823-193454.tar.gz` and `ava_directory_feature.zip` are generated bundles. They go into the archive and do not go into Pacific, Database, the website, or git as live data.

---

## 3. Tasks

1. This draft stays OPEN until Alexander accepts it and says to build. Until then, do not edit runtime files, restart services, send messages, actuate hardware, or spend cloud money. Do not archive or delete yet.
2. No dependency Folder is required. Do not pause for another function. Do not create Pacific, Database, or Logs paths. Do not edit `jobs.py`. Do not import logs, samples, zips, dumps, or caches into the live Folders.
3. Copy only this function's files into `Old repos deleted and merged/old/`, keeping each path they had inside `old`. If the copy fails, stop and do not delete.
   - `core_uploader.py`
   - `file_mapper.py`
   - `create_migration.py`
   - `tools/build-global-routes.py`
   - `operations/system-tools/database-root-migrate.py`
   - `operations/system-tools/sync-ava-directory.sh`
   - `operations/system-tools/directory-printer/` (whole directory)
   - `operations/system-tools/directory-sync/` (whole directory)
   - `operations/system-tools/desk/` (whole directory, including `ava_directory_feature.zip`)
   - `operations/system-tools/desk-backup-20260823-193454.tar.gz`
4. Leave these in the `old` repo. They belong to other functions:
   - `operations/system-tools/github-auto-push.py` and `GITHUB-AUTO-PUSH.txt` (Git auto-push, already in Pacific `Github/scripts`)
   - `operations/system-tools/ai_usage.py`, `ai_usage_report.py`, and `new 1.txt` (Grok usage report)
   - `operations/system-tools/AGENTS.md` (shared system-tools note)
   - `operations/system-tools/screenshot.sh.disabled`
   - `operations/broadcast.py` and any live cronologicals
   - Any other file under `tools/` besides `build-global-routes.py`
5. Commit that deletion on GitHub `old`, branch `cursor/radio-idle-obs-gates`, and push. No force-push. Do not delete the GitHub repository. Do not delete the new archive, and do not delete unrelated files already under `Old repos deleted and merged/old/`.
6. Update this work order with what landed, the archive path, and the GitHub commit. Correct only row 87 of `Documentation/00-architecture/Old-Repo-Migration-Matrix.md`. Do not rewrite other work orders.

---

## 4. Non-goals

- Do not install a Folder, a package, a CLI wrapper, or a public page.
- Do not overwrite EcoFlow BLE, the poller, Hawaiʻi weather, the globe collector, camera grabs, Kokoro, or `geology_collect.py`.
- Do not edit `jobs.py`, the Vercel app, or `master-key.env`.
- Do not run `core_uploader.py`, `file_mapper.py`, `create_migration.py`, `build-global-routes.py`, `database-root-migrate.py`, either sync script, the directory printer, or the visual CLI. Do not rsync, move databases, push `Ava-Core-Dev/ava-core`, write route pages, play audio, or scan the live Ecosystem.
- Do not build the file browser, the drop runner, or the full-disk index.
- Do not delete the shared files named in §3 task 4.
- Do not import generated reports, zips, tar archives, logs, samples, or caches into Pacific, Database, the website, or git.
- Do not build any other agent's function. Do not restore files under `~/.ollama/skills/energy`, automations, or `coms/ssh/local-data-globe`.
- Sends, speaker playback, OBS, hardware switching, deletion of live Ecosystem files, and cloud spend stay off.

---

## 5. Key file / path reference

| Path | Role |
|------|------|
| Server code | None. Not created. |
| Database data | None. Not created. |
| Database logs | None. Not created. |
| `/home/rootrecord/master/master-key.env` | Not used. Not edited. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Github/scripts/` | Live replacement for the uploader. Not edited. |
| `core_uploader.py`, `file_mapper.py`, `create_migration.py` in `rootrecordsoftwaresolutions/old` | Old root CLIs. Archive, then delete on GitHub. |
| `tools/build-global-routes.py` | Old route builder. Archive, then delete on GitHub. Leave every other file in `tools/`. |
| `operations/system-tools/database-root-migrate.py` | Old database mover. Archive, then delete on GitHub. |
| `operations/system-tools/sync-ava-directory.sh` | Old rsync. Archive, then delete on GitHub. |
| `operations/system-tools/directory-printer/` | Directory printer. Archive the directory, then delete it on GitHub. |
| `operations/system-tools/directory-sync/` | Directory sync. Archive the directory, then delete it on GitHub. |
| `operations/system-tools/desk/` | Visual CLI snapshot, including the nested broadcast copy and `ava_directory_feature.zip`. Archive the directory, then delete it on GitHub. |
| `operations/system-tools/desk-backup-20260823-193454.tar.gz` | Generated desk backup. Archive, then delete on GitHub. Not a live Folder. |
| `operations/system-tools/github-auto-push.py`, `GITHUB-AUTO-PUSH.txt`, `ai_usage.py`, `ai_usage_report.py`, `new 1.txt`, `AGENTS.md`, `screenshot.sh.disabled` | Shared or other functions. Leave them. |
| `operations/broadcast.py` | File-browser agent. Leave it. |
| `Old repos deleted and merged/old/` | Archive root after phase 4. Same relative paths as in `old`. |
| `Documentation/00-architecture/Old-Repo-Migration-Matrix.md` | Row 87 only, after phase 4. |

---

## 6. Open items

**Additional requirements:**

- Alexander accepts this draft and says to build before any of §3 tasks 2–6.
- Phase 4 deletes GitHub files only after the archive copy is on disk.
- Speaker playback, rsync, database moves, and a push to `Ava-Core-Dev/ava-core` need a separate sign-off. This work order does not do them.

---

## 7. Notes & constraints

- No force-push. Do not delete the GitHub repository `old`.
- Secrets stay out of git. This function has no key names. Do not copy `/home/ava-core/Credentials`.
- Prefer small reversible steps. New periodic jobs stay off. Do not edit `jobs.py`.
- Sign-off gates: running any of these CLIs, rsync, moving databases, pushing `Ava-Core-Dev/ava-core`, writing route pages, speaker playback, sends, OBS, hardware switching, deletion of live Ecosystem files, and cloud spend. Phase 4 archive-then-delete of this function's old files is already ordered, and only after the archive copy succeeds.
- Proof, 2026-09-30 00:52 HST: 28 archived files match the GitHub blobs by sha256. No copy of these scripts was added under Pacific or Database. `jobs.py` was not edited. The CLIs were not run.
- Result note (2026-09-30 00:52 HST): No Folder landed. Archived 28 files under `Old repos deleted and merged/old/` at the old paths (`core_uploader.py`, `file_mapper.py`, `create_migration.py`, `tools/build-global-routes.py`, `operations/system-tools/database-root-migrate.py`, `operations/system-tools/sync-ava-directory.sh`, `directory-printer/`, `directory-sync/`, `desk/` including `ava_directory_feature.zip`, and `desk-backup-20260823-193454.tar.gz`). `tools/` held only `build-global-routes.py`, so that directory is gone from git. Removed those 28 files on GitHub `rootrecordsoftwaresolutions/old` commit `97a2557` (default branch `cursor/radio-idle-obs-gates`). Left `github-auto-push.py`, `GITHUB-AUTO-PUSH.txt`, `ai_usage.py`, `ai_usage_report.py`, `new 1.txt`, `AGENTS.md`, `screenshot.sh.disabled`, and `operations/broadcast.py`. The repository was not deleted. There was no local checkout to delete from. WO-MIG-37 still lists some of these paths as leftovers to leave; that work order was not rewritten.

---

*Work order prepared 2026-09-30 HST. Update status when closed.*

---

## Archive / location note

This draft stays here:

```text
Documentation/06-development/Work-Orders/drafts/Ava_core_one_off_CLIs_Work_Order_WO-MIG-44-2026-09-29.md
```

Do not promote it onto the active index. Active / accepted work orders live in `Documentation/06-development/Work-Orders/`. Closed work orders move to `Documentation/06-development/Work-Orders/Complete/`.
