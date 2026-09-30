# WORK ORDER — Context session builder

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-MIG-43-2026-09-29 |
| **Date** | 2026-09-30 (HST) |
| **Status** | BUILT — temp-root smoke PASS 2026-09-30 00:48 HST. Listener not started. Not on the active index. |
| **Owner** | RootRecord |
| **Related** | Agent 43, Wave G. No other function has to exist before this build. No later function in the agent list depends on this one. Old home: `operations/context_session_builder` in GitHub `rootrecordsoftwaresolutions/old` (default branch `cursor/radio-idle-obs-gates`). Matrix row 85. |

**Scope:** One library for per-user context sessions. In scope is the Folder, the sqlite store, a CLI that does not open a port, empty Database and Logs READMEs, a temp-root smoke test, then archive and removal of this function's old files. Out of scope is a FastAPI listener, a poller job, a public website page, placeholder account and automation layers, and any other agent's function. This file stays in drafts. Do not promote it onto the active index.

---

## 1. Intent

Old `operations/context_session_builder` stores Ava Ivy context sessions. `store.py` is a `SessionStore`: one sqlite file per user id, a sessions table and an events table, user ids limited to `[A-Za-z0-9._-]{1,128}`, default root `/home/ava-core/data/context/users`. `api.py` is an optional FastAPI factory, `create_app`. It does not call uvicorn. `placeholders/accounts` and `placeholders/automations` are README stubs that say they are not implemented. A code search of `old` finds no other file importing this package.

The live Ecosystem has no context-session store. EcoFlow BLE, the poller, Hawaiʻi weather, the globe collector, camera grabs, Kokoro, and `geology_collect.py` stay as they are. This function does not replace them.

What it adds is the store as a library, package name `ContextSession`, with the store root moved to the Database path in §2.1. The FastAPI factory may be copied so the old adapter is not lost. Nothing starts it. The two placeholder READMEs come across as source and stay unimplemented.

---

## 2. Current reality

### 2.1 What exists

Folder name: **ContextSession**. It does not belong inside Energy, Geology, Weather, Reports, Security, Communications, System, or Media, so it is one new top-level folder. Same name in all three places. No lowercase twin and no symlink.

| Item | Location / status |
| --- | --- |
| Server code | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/ContextSession/scripts` — landed. Package name `ContextSession`. No `Logs/` directory on the server. `config/` is not needed. |
| Database data | `2 - RootRecord-Database/ContextSession/` — README only. Per-user sqlite files live here after a real run. The smoke test does not write here. |
| Database logs | `2 - RootRecord-Database/Logs/ContextSession/` — README only. The CLI does not write a log file. |
| Secrets | None. No key names in `/home/rootrecord/master/master-key.env`. No second env file. |
| Old source | Removed from GitHub `rootrecordsoftwaresolutions/old` commit `3c67f7a`. Archive: `Old repos deleted and merged/old/operations/context_session_builder/`. |
| Live functions to keep | EcoFlow BLE, the poller, Hawaiʻi weather, the globe collector, camera grabs, Kokoro, `geology_collect.py` |

### 2.2 Completed so far

- [x] Old source read (`store.py`, `api.py`, `__init__.py`, both placeholder READMEs) and Geology / Energy layout checked
- [x] `ContextSession` package and CLI
- [x] Empty Database and Logs READMEs
- [x] Temp-root smoke test (2026-09-30 00:48 HST)
- [x] Old files archived, then removed from the old repo and GitHub
- [x] Library row 85 and the context-session blocker sentence corrected

### 2.3 Known friction

- The old default root is `/home/ava-core/data/context/users`. The live store root is the Database path above, overridable by argument.
- `create_app` imports FastAPI. Importing the store and the CLI must not import FastAPI and must not bind a socket.
- Opening a listener is why this function was left out. The factory stays unwired until Alexander signs off on a serve path.

---

## 3. Tasks

1. This draft stays OPEN until Alexander accepts it and says to build. Until then, do not edit runtime files, restart services, send messages, actuate hardware, or spend cloud money.
2. Add package `ContextSession` under `ContextSession/scripts/`: `__init__.py`, `store.py`, `api.py` (factory only), and the two placeholder READMEs. Add `ContextSession/README.md`. Default store root is `2 - RootRecord-Database/ContextSession/`.
3. Add a CLI that creates a session, appends an event, lists sessions, and prints current state. It must not import FastAPI. Do not add a `serve` command. Do not edit `jobs.py`. Do not open a port.
4. Add a short README only under the Database folder and under `Logs/ContextSession/`. No sqlite, samples, or last-state files in git.
5. No other function has to exist before this build. There is no dependency Folder to wait on.
6. Smoke test against a temp root under `/tmp`, not the live Database: create, append, list, current. Assert the store refuses an unsafe user id. Confirm importing the package does not bind a socket.
7. After that test passes: copy the old tree to `Old repos deleted and merged/old/operations/context_session_builder/`, keeping the path it had inside `old`. Generated data that lived beside that source goes into the archive too, and still does not go into the live Folders. If the archive copy fails, do not delete. Then delete those same files from the old repo on this machine and on GitHub branch `cursor/radio-idle-obs-gates`. Commit and push. Do not force-push. Do not delete the GitHub repository. No shared file was found; if one turns up, leave it and name it here.
8. Update this work order with what landed, the archive path, and the GitHub deletion. Correct only row 85 of `Documentation/00-architecture/Old-Repo-Migration-Matrix.md` and the context-session sentence in that file's blockers list.

---

## 4. Non-goals

- Do not overwrite EcoFlow BLE, the poller, Hawaiʻi weather, the globe collector, camera grabs, Kokoro, or `geology_collect.py`.
- Do not edit `jobs.py`, the Vercel app, or `master-key.env`.
- Do not start uvicorn or bind a port. Do not add a public page under `3 - RootRecord-Website`.
- Do not implement the accounts or automations placeholders.
- Do not import generated session databases, logs, samples, or caches into Pacific, Database, the website, or git.
- Do not build any other agent's function. Do not restore files under `~/.ollama/skills/energy`, automations, or `coms/ssh/local-data-globe`.
- Sends, speaker playback, OBS, hardware switching, deletion of live Ecosystem files, and cloud spend stay off.

---

## 5. Key file / path reference

| Path | Role |
|------|------|
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/ContextSession/scripts` | Server code. Package name `ContextSession`. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/ContextSession/scripts/ContextSession/store.py` | Session store. Landed. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/ContextSession/scripts/ContextSession/api.py` | FastAPI factory only. Not served. Landed. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/ContextSession/scripts/ContextSession/__init__.py` | Package exports. Landed. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/ContextSession/scripts/context_session.py` | CLI. No listener. Landed. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/ContextSession/README.md` | Domain readme. Landed. |
| `2 - RootRecord-Database/ContextSession/` | Per-user sqlite after a real run. README only in git. |
| `2 - RootRecord-Database/Logs/ContextSession/` | Logs. README only until a real run. |
| `/home/rootrecord/master/master-key.env` | Not used. Not edited. |
| `operations/context_session_builder/` in `rootrecordsoftwaresolutions/old` | Old source. Archive, then delete. |
| `Old repos deleted and merged/old/operations/context_session_builder/` | Archive path after phase 4. |
| `Documentation/00-architecture/Old-Repo-Migration-Matrix.md` | Row 85 and the context-session blocker sentence, after phase 4. |

---

## 6. Open items

**Additional requirements:**

- Alexander accepts this draft and says to build before any of §3 tasks 2–8.
- A FastAPI listener needs a separate sign-off. This work order does not add `serve`.
- Phase 4 deletes old-repo files only after the archive copy is on disk.

---

## 7. Notes & constraints

- No force-push. Do not delete the GitHub repository `old`.
- Secrets stay out of git. This function has no key names.
- Prefer small reversible steps. New periodic jobs stay off. Do not edit `jobs.py`.
- Sign-off gates: FastAPI listener / uvicorn, sends, speaker playback, OBS, hardware switching, deletion of live Ecosystem files, and cloud spend. Phase 4 archive-then-delete of this function's old files is already ordered, and only after the archive copy succeeds.
- Proof, and the only test to run: CLI create, append, list, and current against a temp root under `/tmp`. Expect one session, one user event after the system `session_created` event, a refused unsafe user id, and no listening socket. Do not write that sqlite into `2 - RootRecord-Database/ContextSession/`.

The result note is below.

---

## Result

Landed 2026-09-30. Package `ContextSession` at `1 - Servers/1 - RootRecord-Pacific-Solar-Server/ContextSession/scripts/ContextSession/` with CLI `scripts/context_session.py`. No `serve` command. `jobs.py` and `master-key.env` were not edited. Import does not load FastAPI.

Smoke test, temp root `/tmp/rr-mig43-context`: create, append, list, and current returned one session. Events were `session_created` then the user `note`. `list 'bad id'` exited 1 with `invalid user_id`. Listening sockets were unchanged. No sqlite was written under `2 - RootRecord-Database/ContextSession/`.

Archive (checksums matched the old tree before deletion):

- `Old repos deleted and merged/old/operations/context_session_builder/` (5 files)

Removed on GitHub `rootrecordsoftwaresolutions/old` branch `cursor/radio-idle-obs-gates` commit `3c67f7a`. The repository was not deleted. No shared file was left behind.

---

*Work order prepared 2026-09-30 HST. Update status when closed.*

---

## Archive / location note

This draft stays here:

```text
Documentation/06-development/Work-Orders/drafts/Context_session_builder_Work_Order_WO-MIG-43-2026-09-29.md
```

Do not promote it onto the active index. Active / accepted work orders live in `Documentation/06-development/Work-Orders/`. Closed work orders move to `Documentation/06-development/Work-Orders/Complete/`.
