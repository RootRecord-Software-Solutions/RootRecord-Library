# WORK ORDER — Python drop runner

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-MIG-46-2026-09-29 |
| **Date** | 2026-09-30 (HST) |
| **Status** | OPEN — landed. Phase 4 archive and GitHub deletion done. Not promoted. |
| **Owner** | RootRecord |
| **Related** | Agent 46, Wave G. Cleanup and hold-backs. Old home `python-drop-runner` in `Solar-Pacific-RootRecord-Server` (`online-safe-20260920`). Live scheduler: Pacific `Automations/scripts/jobs.py`. |

**Scope:** Add an allowlist runner under Pacific `System/PythonDrop`. A catalog file is the only list of scripts that may run, and it ships empty. The scheduled job stays off. Out of scope: copying the old runner that executes any dropped `.py`, GUI terminals, restart-on-exit, origin `:8787`, the 288 clock-slot folders, other agents’ functions, and any runtime edit, service restart, or GitHub change before this draft is accepted and a build is ordered.

This file is the before-documentation. It is not on the active index.

---

## 1. Intent

The old runner (`python-drop-runner/scripts/python_drop_runner.py`) watched a drop folder. It discovered every top-level `*.py`, opened a GUI terminal, and restarted the process on exit. Timed folders (`on-time/HH:MM` for every five-minute Hawaiian slot, plus `Every 5 Mins`, `Every 15 minutes`, `Every 30 minutes`, and `Every Hour`) ran whatever `.py` was in them, once per slot, and wrote logs under `drop/logs/`. Origin on `:8787` reported status. That arbitrary execution is why the function is still missing.

The live system already schedules work in `Automations/scripts/jobs.py`. EcoFlow BLE, the poller, Hawaiʻi weather, the globe collector, camera grabs, Kokoro, and `geology_collect.py` stay as they are. Nothing in Pacific scans a folder and runs dropped Python.

This function is a new allowlist, not a copy of the old runner. Only names in `config/catalog.json` may run, and only if the path stays inside `System/PythonDrop/`. An empty catalog starts zero processes.

---

## 2. Current reality

### 2.1 What exists

Folder name: `PythonDrop`. Same name in all three places. Domain is System, the same placement as `NightSleep`. No lowercase twin and no symlink. No `Logs/` directory on the server. No `master-key.env` keys.

| Item | Location / status |
| --- | --- |
| Server code | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/System/PythonDrop/scripts` — not installed. Package name `PythonDrop` |
| Database data | `2 - RootRecord-Database/System/PythonDrop` — not installed. Last-fire state only, created when the runner is later used. Runtime output. Not committed |
| Database logs | `2 - RootRecord-Database/Logs/System/PythonDrop` — not installed. Tick logs only |
| master-key.env | No key names. The script does not read secrets |
| Live scheduler | `Automations/scripts/jobs.py`. Already the place periodic work runs. This function does not replace it |
| Old source | `/home/rootrecord/old ollama/old skills/python-drop-runner/scripts/python_drop_runner.py`. Remote `git@github.com:rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server.git`, branch `online-safe-20260920` |
| Shared file, leave it | `origin/ns/apps/core/services/python_drop_runner.py` in that same checkout. It is an origin shim that `exec`s the skill script. It belongs to origin, not this function |
| Shared file at build time | `Automations/scripts/jobs.py` is already modified in the Ecosystem working tree. If it is still dirty from another agent when the build is ordered, pause and do not edit it |

### 2.2 Completed so far

- [x] Old source read. Allowlist design chosen. Folder and three paths named.
- [x] Draft work order written (this file).
- [x] Alexander said to build.
- [x] `System/PythonDrop` package, `scripts/python_drop.py`, and empty `config/catalog.json` added.
- [x] Gated `system_python_drop` block in `jobs.py` (`RR_PYTHON_DROP` unset). The file was clean at build time.
- [x] Status and tick test with the empty catalog, and a refused path outside the catalog. PASS 2026-09-30.
- [x] Phase 4 archive, old-repo deletion, and GitHub commit/push.
- [x] Result note on this work order, and the stale Library rows corrected.

### 2.3 Known friction

- The old script runs any `.py` it finds. The new script must not scan a drop folder, open a terminal, or restart a process.
- Turning the job on, or adding a catalog entry, executes code. Both stay behind sign-off. The catalog ships empty and `RR_PYTHON_DROP` stays unset.
- `jobs.py` is a shared file and is already dirty. Pause at build time if another agent still owns that edit.
- The origin shim stays. After `python-drop-runner/` is removed from the old repo, that shim will fail if origin still loads it. Rebuilding origin is not this function.
- `drop/` beside the old source is generated (clock folders, READMEs, state JSON). `drop/.gitignore` ignores everything except itself. Archive that tree. Do not import it. The JSON and READMEs are not on GitHub. The 576 directories under `drop/on-time/` are not on GitHub.
- Copies under `/home/rootrecord/old ollama/github-history/` are snapshots, not the live old repo. Leave them.

---

## 3. Tasks

Build only after Alexander accepts this draft and says to build. Until then, do not edit runtime files, restart services, send messages, actuate hardware, or spend cloud money.

1. Add `1 - Servers/1 - RootRecord-Pacific-Solar-Server/System/PythonDrop/__init__.py`, `scripts/python_drop.py`, and `config/catalog.json`. Package name `PythonDrop`. No server `Logs/` directory.
2. `catalog.json` ships with an empty entry list. Each later entry names a `.py` path that must stay inside `System/PythonDrop/` and a schedule: one HST `HH:MM`, or `5m`, `15m`, `30m`, or `1h`. Refuse `..`, non-`.py` files, paths outside that tree, and any name not in the catalog.
3. CLI is `status` and `tick` only. `status` prints the due list and starts nothing. `tick` fires due catalog entries once per HST day and appends logs under `2 - RootRecord-Database/Logs/System/PythonDrop/`. Last-fire state goes to `2 - RootRecord-Database/System/PythonDrop/`. Do not commit that state or those logs. An empty catalog means `tick` exits 0 and spawns nothing.
4. Do not create clock-slot directories. Do not open a GUI terminal. Do not restart on exit. Do not listen on a port.
5. Propose one gated block in `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Automations/scripts/jobs.py`, same shape as `system_uptime_log`: id `system_python_drop`, `enabled` only when `RR_PYTHON_DROP=1` at poller start, interval 300 seconds, command `python3` on `python_drop.py tick`. The gate stays unset. Do not edit any other job. If `jobs.py` is still dirty from another agent, pause and name that block as unwritten.
6. Small test, no service restart. `python3` on `python_drop.py status` prints an empty due list and starts no process. `tick` with the empty catalog exits 0. A path outside the catalog is refused and not executed.
7. This function does not depend on another migration Folder. Do not pause for a missing Folder. Do not build any other agent’s function. Nothing later in the agent list depends on this one.
8. After the migration works, and before Library updates: copy `python-drop-runner/` (source plus the generated `drop/` tree beside it) into `/home/rootrecord/RootRecord-Ecosystem/Old repos deleted and merged/Solar-Pacific-RootRecord-Server/python-drop-runner/`, keeping the path it had inside the old repo. That generated tree still does not go into Pacific, Database, the website, or git. Leave `origin/ns/apps/core/services/python_drop_runner.py` and name it here as shared. After the archive copy is on disk, delete those same `python-drop-runner/` files from the old repo on this machine and on GitHub. Commit that deletion and push it. Do not force-push. Do not delete the GitHub repository. If the archive copy fails, do not delete. If another agent is committing that old repo at the same time, pause before the push.
9. Then update this same work order with what landed, the archive path, the GitHub deletion, and the new status. Correct only the Library pages this function made stale. Do not rewrite unrelated work orders.

Phase 4 file list, from checkout `/home/rootrecord/old ollama/old skills` (remote `git@github.com:rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server.git`, branch `online-safe-20260920`):

- Tracked, archive then delete: `python-drop-runner/DAILY.md`, `python-drop-runner/INDEX.md`, `python-drop-runner/SKILL.md`, `python-drop-runner/drop/.gitignore`, `python-drop-runner/references/migrate.md`, `python-drop-runner/scripts/python_drop_runner.py`.
- Generated, archive then delete on this machine only: `python-drop-runner/drop/Every 5 Mins/README.txt`, `python-drop-runner/drop/Every 15 minutes/README.txt`, `python-drop-runner/drop/Every 30 minutes/README.txt`, `python-drop-runner/drop/Every Hour/README.txt`, `python-drop-runner/drop/on-time/README.txt`, `python-drop-runner/drop/python-script-autostart.json`, `python-drop-runner/drop/timed-fire-state.json`, and the `python-drop-runner/drop/on-time/` clock directories. These are not on GitHub.
- Leave in place: `origin/ns/apps/core/services/python_drop_runner.py` (origin’s shim), and the snapshots under `/home/rootrecord/old ollama/github-history/` that contain `python-drop-runner`.

---

## 4. Non-goals

- Do not copy `python_drop_runner.py` into the live tree. Do not scan a drop folder. Do not create 288 clock directories. Do not open GUI terminals. Do not restart on exit. Do not bind origin `:8787`.
- Do not enable `RR_PYTHON_DROP`. Do not add a catalog entry in this build. An entry that names a real script is a later sign-off.
- Do not replace EcoFlow BLE, the poller, Hawaiʻi weather, the globe collector, camera grabs, Kokoro, or `geology_collect.py`.
- Do not add a file browser or a full-disk index. Those are other agents.
- Do not send messages, play audio, switch hardware, delete live Ecosystem files, or spend cloud money.
- Do not import logs, samples, last-state files, generated reports, collected images, radar frames, zip archives of collected data, database dumps, caches, virtualenvs, `node_modules`, or `__pycache__` into Pacific, Database, the website, or git.
- Do not restore files under `~/.ollama/skills/energy`, automations, or `coms/ssh/local-data-globe`.
- Do not edit other agents’ files. The only shared live file this function may touch, and only as a gated-off block when that file is free, is `Automations/scripts/jobs.py`.
- Do not delete `origin/ns/apps/core/services/python_drop_runner.py`. It is shared with origin.
- Do not rewrite unrelated work orders, including `Ecosystem_Migration_Work_Order_WO-ECO-2026-09-27.md`.
- Do not delete the GitHub repository. Do not force-push.

---

## 5. Key file / path reference

| Path | Role |
|------|------|
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/System/PythonDrop/scripts` | Server code. Not installed |
| `2 - RootRecord-Database/System/PythonDrop/` | Database data. Last-fire state only. Not installed. Not committed |
| `2 - RootRecord-Database/Logs/System/PythonDrop/` | Database logs. Tick logs only. Not installed |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/System/PythonDrop/__init__.py` | Package `PythonDrop`. Add at build time |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/System/PythonDrop/scripts/python_drop.py` | New script. Empty catalog runs nothing. Add at build time |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/System/PythonDrop/config/catalog.json` | Allowlist. Ships empty. Add at build time |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Automations/scripts/jobs.py` | At build time, one gated block `system_python_drop` (`RR_PYTHON_DROP` unset, 300 s, `tick`), and only if this file is not already being edited. No other edit |
| `/home/rootrecord/old ollama/old skills/python-drop-runner/` | Old source and generated `drop/` tree. Archive in phase 4, then delete from that repo |
| `/home/rootrecord/old ollama/old skills/origin/ns/apps/core/services/python_drop_runner.py` | Origin shim. Shared. Leave it |
| `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/python-drop-runner/` | Phase 4 archive path (after the copy succeeds) |
| `5 - RootRecord-Library/Documentation/00-architecture/Old-Repo-Migration-Matrix.md` | After phase 4, correct row 16 only |
| `5 - RootRecord-Library/Documentation/00-architecture/Solar-Pacific-Old-Full-TopLevel-Catalog-2026-09-28.md` | After phase 4, correct the `python-drop-runner` row only |

---

## 6. Open items

**Additional requirements:**

- Accept this draft before any build.
- Separate sign-off before `RR_PYTHON_DROP` is set, and a separate sign-off before any catalog entry is added. The scheduled command stays off.
- Phase 4 GitHub deletion waits until the archive copy is on disk, and only for this function’s old files on `Solar-Pacific-RootRecord-Server` branch `online-safe-20260920`.
- If `jobs.py` is still being edited by another agent at build time, pause. Do not write the gated block until that edit is free.

---

## 7. Notes & constraints

- No force-push.
- Secrets stay out of git. This function has no `master-key.env` keys. Never print secret values. Never add a second env file.
- Prefer small reversible steps.
- Sign-off gates: no sends, speaker playback, OBS, hardware switching, deletion of live Ecosystem files, or cloud spend. Do not enable `RR_PYTHON_DROP` or add a catalog entry without Alexander’s sign-off. Phase 4 deletion is limited to the old function’s files after the archive copy succeeds. The origin shim stays.
- Small test that proves the new behavior: `python_drop.py status` prints an empty due list and starts no process; `tick` with the empty catalog exits 0; a path outside the catalog is refused and not executed. No service restart.
- New code wins. Do not copy the old runner over this design.
- Result note (2026-09-30): Landed Pacific `System/PythonDrop` (`__init__.py`, `scripts/python_drop.py`, empty `config/catalog.json`) and a gated `jobs.py` block `system_python_drop` (`RR_PYTHON_DROP` unset, 300 s, `tick`). Smoke: `status` and `tick` printed `{"due": [], "catalog": 0, "spawned": 0}` and wrote no Database files. An absolute path and a `..` path were refused and not executed. Archive: `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/python-drop-runner/` (13 files, 586 directories, matching the old tree). Removed on this machine: that whole `python-drop-runner/` directory, including the gitignored `drop/` state and clock folders. Removed on GitHub: commit `98a7b651` on `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server` branch `online-safe-20260920` (the 6 tracked files). Left in place: `origin/ns/apps/core/services/python_drop_runner.py` (origin shim) and the `github-history` snapshots. Gate stays off. No catalog entry was added.

---

*Work order prepared 2026-09-30 HST. Update status when closed.*

---

## Archive / location note

**Active / accepted WOs** — filename when saved:

```text
Python_drop_runner_Work_Order_WO-MIG-46-2026-09-29.md
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
