# WORK ORDER — Broadcast directory browser

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-MIG-47-2026-09-29 |
| **Date** | 2026-09-30 (HST) |
| **Status** | BUILT — stays in drafts, not promoted to the active index |
| **Owner** | RootRecord |
| **Related** | Agent 47, Wave G. No other function has to exist before this build. No later function in the agent list depends on this one. Old home: `operations/broadcast.py` in GitHub `rootrecordsoftwaresolutions/old` (branch `cursor/radio-idle-obs-gates`). Matrix row 83. |

**Scope:** One local listing tool for an explicit root the caller passes in. In scope is the Folder, a library and CLI that list one directory level and do not read file bytes, empty Database and Logs READMEs, a temp-root smoke test, then archive and removal of the two old files that belong only to this function. Out of scope is the old public file server, any HTTP listener, a public website page, EcoFlow / system / uptime / static-page code that shares `broadcast.py`, and any other agent's function. This file stays in drafts. Do not promote it onto the active index.

---

## 1. Intent

Old `operations/broadcast.py` is one process. It serves EcoFlow sqlite APIs, host and uptime pages, static site files, and a `/directory` browser. This work order is only the browser.

The browser binds `0.0.0.0:8080`. Its root is `/home/ava-core`. It lists that tree, including a recursive mode, and serves file bytes from `/api/directory/file`, `/directory/view`, and `/ava-ivy/file/`. A name denylist hides some secret-looking paths. Other paths are listed and their contents are served. `web/sites/avaivy.cloud/directory/directory.js` calls that API with root `/home/ava-core`. The on/off switch is the presence of `operations/cronologicals/always-on/directory.enabled`.

The live Ecosystem does not serve this tree. EcoFlow BLE, the poller, Hawaiʻi weather, the globe collector, camera grabs, Kokoro, and `geology_collect.py` stay as they are. This function does not replace them.

What it adds is a listing library, package name `DirectoryBrowser`, plus a CLI. The caller passes `--root`. There is no default of `/home`, `/home/ava-core`, or the Ecosystem root. It lists one directory level (name, type, size, mtime). It does not read file bytes, does not bind a socket, and does not copy the old denylist. The old listener is not ported.

---

## 2. Current reality

### 2.1 What exists

Folder name: **DirectoryBrowser**. It belongs in Security, so it is a subfolder of that domain, mirrored under Database and Logs. Same name in all three places. No lowercase twin and no symlink.

| Item | Location / status |
| --- | --- |
| Server code | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Security/DirectoryBrowser/scripts` — landed. Package name `DirectoryBrowser`. No `Logs/` directory on the server. `config/` is not needed. |
| Database data | `2 - RootRecord-Database/Security/DirectoryBrowser/` — README only in git. |
| Database logs | `2 - RootRecord-Database/Logs/Security/DirectoryBrowser/` — README only in git. |
| Secrets | None. No key names in `/home/rootrecord/master/master-key.env`. No second env file. |
| Old source | GitHub `rootrecordsoftwaresolutions/old`, branch `cursor/radio-idle-obs-gates`. Directory behavior lives inside `operations/broadcast.py` and the always-on copy. The files that belong only to this function are `operations/cronologicals/always-on/directory.enabled` and `web/sites/avaivy.cloud/directory/directory.js`. |
| Live functions to keep | EcoFlow BLE, the poller, Hawaiʻi weather, the globe collector, camera grabs, Kokoro, `geology_collect.py` |

### 2.2 Completed so far

- [x] Old source read (`operations/broadcast.py` directory section, `directory.js` header, `directory.enabled`) and Security / Energy layout checked
- [x] `DirectoryBrowser` package and CLI
- [x] Empty Database and Logs READMEs
- [x] Temp-root smoke test
- [x] The two directory-only old files archived, then removed from the old repo and GitHub
- [x] Library row 83 and the broadcast blocker sentence corrected

### 2.3 Known friction

- The old root is `/home/ava-core` and the process listens on every interface. The live tool has no default root and opens no port.
- `operations/broadcast.py` and `operations/cronologicals/always-on/broadcast.py` also implement EcoFlow, system, uptime, and static pages. Those files stay. They are named in §4.
- A string-prefix path check and a name denylist are why the old browser was held. The replacement uses an explicit root and refuses a symlink that resolves outside it.

---

## 3. Tasks

1. This draft stays OPEN until Alexander accepts it and says to build. Until then, do not edit runtime files, restart services, send messages, actuate hardware, or spend cloud money.
2. Add package `DirectoryBrowser` under `Security/DirectoryBrowser/scripts/`: `__init__.py` and `list_dir.py`. Add CLI `scripts/directory_browser.py`. Add `Security/DirectoryBrowser/README.md`. `--root` is required. One level only. Refuse `..`. Refuse a symlink whose resolved path is outside that root. Do not follow directory symlinks. Do not read file bytes. Do not bind a socket.
3. Do not add a `serve` command. Do not edit `jobs.py`. Do not add a public page under `3 - RootRecord-Website`.
4. Add a short README only under `2 - RootRecord-Database/Security/DirectoryBrowser/` and under `2 - RootRecord-Database/Logs/Security/DirectoryBrowser/`. No samples, last-state files, or generated listings in git.
5. No other function has to exist before this build. There is no dependency Folder to wait on.
6. Smoke test against a temp root under `/tmp`, not the live Database and not `/home`: one ordinary file and one symlink that points outside the temp root. The CLI lists the file and omits or refuses the symlink. Confirm importing the package does not bind a socket.
7. After that test passes: copy only `operations/cronologicals/always-on/directory.enabled` and `web/sites/avaivy.cloud/directory/directory.js` to `Old repos deleted and merged/old/`, keeping the path each had inside `old`. Generated data that lived beside that source goes into the archive too, and still does not go into the live Folders. If the archive copy fails, do not delete. Then delete those same two files from the old repo on this machine and on GitHub branch `cursor/radio-idle-obs-gates`. Commit and push. Do not force-push. Do not delete the GitHub repository. Leave the shared files named in §4.
8. Update this work order with what landed, the archive path, and the GitHub deletion. Correct only row 83 of `Documentation/00-architecture/Old-Repo-Migration-Matrix.md` and the broadcast sentence in that file's blockers list.

---

## 4. Non-goals

- Do not port the browser as it was. Do not bind `0.0.0.0:8080` or any other listener. Do not root a listing at `/home`, `/home/ava-core`, or the live Ecosystem.
- Do not overwrite EcoFlow BLE, the poller, Hawaiʻi weather, the globe collector, camera grabs, Kokoro, or `geology_collect.py`.
- Do not edit `jobs.py`, the Vercel app, or `master-key.env`.
- Do not add a public page under `3 - RootRecord-Website`.
- Do not copy the EcoFlow, system, uptime, or static-page code out of `broadcast.py`.
- Do not import logs, samples, last-state files, generated reports, or listings into Pacific, Database, the website, or git.
- Do not build any other agent's function. Do not restore files under `~/.ollama/skills/energy`, automations, or `coms/ssh/local-data-globe`.
- Shared files, left in the old repo and named here:
  - `operations/broadcast.py` — EcoFlow API, system, uptime, static pages, and the directory handlers in one file.
  - `operations/cronologicals/always-on/broadcast.py` — the same server, plus quake routes.
  - `web/sites/avaivy.cloud/js/earthquake-directory.js` — quake pages, another function.
  - The desk snapshot of `broadcast.py` under `operations/system-tools/desk/` stays with agent 44.
- Sends, speaker playback, OBS, hardware switching, deletion of live Ecosystem files, and cloud spend stay off.

---

## 5. Key file / path reference

| Path | Role |
|------|------|
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Security/DirectoryBrowser/scripts` | Server code. Package name `DirectoryBrowser`. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Security/DirectoryBrowser/scripts/DirectoryBrowser/list_dir.py` | One-level listing. To add. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Security/DirectoryBrowser/scripts/DirectoryBrowser/__init__.py` | Package exports. To add. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Security/DirectoryBrowser/scripts/directory_browser.py` | CLI. `--root` required. No listener. To add. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Security/DirectoryBrowser/README.md` | Domain readme. To add. |
| `2 - RootRecord-Database/Security/DirectoryBrowser/` | Data folder. README only in git. |
| `2 - RootRecord-Database/Logs/Security/DirectoryBrowser/` | Logs. README only until a real run. |
| `/home/rootrecord/master/master-key.env` | Not used. Not edited. |
| `operations/cronologicals/always-on/directory.enabled` in `rootrecordsoftwaresolutions/old` | Old on/off flag. Archive, then delete. |
| `web/sites/avaivy.cloud/directory/directory.js` in `rootrecordsoftwaresolutions/old` | Old browser page script. Archive, then delete. |
| `operations/broadcast.py` and `operations/cronologicals/always-on/broadcast.py` | Shared. Leave them. |
| `Old repos deleted and merged/old/operations/cronologicals/always-on/directory.enabled` | Archive path after phase 4. |
| `Old repos deleted and merged/old/web/sites/avaivy.cloud/directory/directory.js` | Archive path after phase 4. |
| `Documentation/00-architecture/Old-Repo-Migration-Matrix.md` | Row 83 and the broadcast blocker sentence, after phase 4. |

---

## 6. Open items

**Additional requirements:**

- Alexander accepts this draft and says to build before any of §3 tasks 2–8.
- An HTTP listener, a public page, or a root of `/home` or the live Ecosystem needs a separate sign-off. This work order does not add `serve`.
- Phase 4 deletes the two directory-only files only after the archive copy is on disk. The shared `broadcast.py` files stay.

---

## 7. Notes & constraints

- No force-push. Do not delete the GitHub repository `old`.
- Secrets stay out of git. This function has no key names.
- Prefer small reversible steps. New periodic jobs stay off. Do not edit `jobs.py`.
- Sign-off gates: HTTP listener, public page, a listing root of `/home` or the live Ecosystem, sends, speaker playback, OBS, hardware switching, deletion of live Ecosystem files, and cloud spend. Phase 4 archive-then-delete of `directory.enabled` and `directory.js` is already ordered, and only after the archive copy succeeds.
- Proof, and the only test to run: CLI list of a temp root under `/tmp` that contains one file and one symlink pointing outside that root. Expect the file in the listing and the symlink omitted or refused, and no listening socket. Do not write that listing into `2 - RootRecord-Database/Security/DirectoryBrowser/`.

## Result

Landed 2026-09-30. Package `DirectoryBrowser` at `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Security/DirectoryBrowser/scripts/DirectoryBrowser/` with CLI `scripts/directory_browser.py`. `--root` is required. No `serve` command. `jobs.py` and `master-key.env` were not edited. Import does not bind a socket.

Smoke test, temp root `/tmp/rr-mig47-list`: `note.txt` listed as a file, `inside` listed as a link that stays in the root, `escape` refused with reason `outside root`. `--rel ../` exited 1 with `path traversal`. A missing root exited 1. Omitting `--root` exited 2. Listening sockets were unchanged. No listing was written under `2 - RootRecord-Database/Security/DirectoryBrowser/`.

Archive (checksums matched the old files before deletion):

- `Old repos deleted and merged/old/operations/cronologicals/always-on/directory.enabled`
- `Old repos deleted and merged/old/web/sites/avaivy.cloud/directory/directory.js`

Removed on GitHub `rootrecordsoftwaresolutions/old` branch `cursor/radio-idle-obs-gates` commit `528ca18`. The repository was not deleted. Left in that repo: `operations/broadcast.py`, `operations/cronologicals/always-on/broadcast.py`, and `web/sites/avaivy.cloud/js/earthquake-directory.js`.

---

*Work order prepared 2026-09-30 HST. Update status when closed.*

---

## Archive / location note

This draft stays here:

```text
Documentation/06-development/Work-Orders/drafts/Broadcast_directory_browser_Work_Order_WO-MIG-47-2026-09-29.md
```

Do not promote it onto the active index. Active / accepted work orders live in `Documentation/06-development/Work-Orders/`. Closed work orders move to `Documentation/06-development/Work-Orders/Complete/`.
