# WORK ORDER — Meta AI chat client

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-MIG-45-2026-09-29 |
| **Date** | 2026-09-30 (HST) |
| **Status** | BUILT — on demand; `--send` still needs sign-off |
| **Owner** | RootRecord |
| **Related** | Agent 45, Wave G. Cleanup and hold-backs. Old home `operations/meta/meta.py` in `rootrecordsoftwaresolutions/old`. Matrix row 86. |

**Scope:** Add an on-demand Meta AI chat CLI as Pacific `Communications/MetaAI`. In scope after this draft is accepted: a script that refuses to pip-install and refuses to call meta.ai until a send is signed off. Out of scope: auto-install of `meta-ai-api`, `jobs.py`, secrets, a public page, other agents’ functions, and any send, archive, or GitHub deletion before acceptance and a working build.

This file is the before-documentation. It is not on the active index.

---

## 1. Intent

The old function `operations/meta/meta.py` was an interactive chat with Meta AI (meta.ai). If `meta_ai_api` was missing it ran `pip install meta-ai-api`, then looped on `MetaAI().prompt(message=..., stream=True)` until exit, quit, or Ctrl+C. It stored nothing and read no secrets.

That client is not in the live system. Alexander still uses it, so the build adds it under Communications and enhances the old script: no automatic pip install, and no prompt to meta.ai unless a send is explicitly signed off. EcoFlow BLE, the poller, Hawaiʻi weather, the globe collector, camera grabs, Kokoro, and `geology_collect.py` stay as they are.

---

## 2. Current reality

### 2.1 What exists

Folder name: `MetaAI`. Same name in all three places. No lowercase twin and no symlink. No `Logs/` directory on the server. No `config/`.

| Item | Location / status |
| --- | --- |
| Server code | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/MetaAI/scripts/meta.py` — installed |
| Database data | `2 - RootRecord-Database/Communications/MetaAI` — README tracked; `last.json` only after a signed-off send, not in git |
| Database logs | `2 - RootRecord-Database/Logs/Communications/MetaAI` — `.gitkeep` tracked; run log not in git |
| master-key.env | No key names. The old client used none. None added. |
| Live callers | None. Nothing in Pacific imports this client. |
| Old source | Archived, then removed. GitHub `old` commit `1315506` on `cursor/radio-idle-obs-gates`. |
| Dependency | `Communications` exists. No pause. |

### 2.2 Completed so far

- [x] Draft work order written (this file).
- [x] Alexander accepted this draft and said to build.
- [x] `MetaAI` package and `scripts/meta.py` added.
- [x] `--check` test passed (no `prompt`, no pip install). Exit 2 because `meta-ai-api` is not installed.
- [x] Phase 4 archive, old-repo deletion, and GitHub commit/push.
- [x] Result note on this work order, and matrix row 86 corrected.

### 2.3 Known friction

- A live prompt is a send to meta.ai. It stays gated until Alexander signs off.
- `meta-ai-api` is an unofficial client. The new script does not install it. If the import fails, `--check` says so and exits.
- The scratch clone is not a durable checkout. Phase 4 uses a local clone of `old` whose committed tree contains `operations/meta/meta.py`, then pushes the deletion. No force-push.
- `2 - RootRecord-Database/.gitignore` is shared. If another agent is editing it, pause before adding the MetaAI ignore lines.

---

## 3. Tasks

Build only after Alexander accepts this draft and says to build. Until then, do not edit runtime files, restart services, send messages, actuate hardware, or spend cloud money.

1. Add the `MetaAI` package under Pacific `Communications/`, with `__init__.py`, `scripts/meta.py`, and a short README. Python package name `MetaAI`.
2. Do not auto-pip. If `meta_ai_api` cannot be imported, exit with a message that names `meta-ai-api`. Do not install it.
3. No arguments, and `--check`, never call `MetaAI().prompt`. `--check` reports whether the package imports. It writes nothing under Database and opens no network send.
4. `--send` (interactive, or one message) is gated. Do not run it until Alexander signs off. A signed-off send may write the last exchange under `2 - RootRecord-Database/Communications/MetaAI`. Logs, if any, go under `2 - RootRecord-Database/Logs/Communications/MetaAI`. Do not put logs on the server. Do not import transcripts or logs into git.
5. Do not edit `jobs.py`. No new periodic job. If `2 - RootRecord-Database/.gitignore` is already being edited, pause. Otherwise add ignore lines for the MetaAI data and log directories.
6. Small test, before any `--send`: from `Communications/MetaAI/scripts`, `python3 meta.py --check` does not call `prompt` and does not pip-install.
7. After the migration works, phase 4: copy `operations/meta/meta.py` to `Old repos deleted and merged/old/operations/meta/meta.py`, keeping that path inside the old repo. Generated data that belonged beside that source goes with it and still does not go into the live Folders. If the archive copy fails, do not delete. After the archive copy is on disk, delete that same file from the local `old` repo and from GitHub `rootrecordsoftwaresolutions/old` on the branch that contains it. Commit that deletion and push it. Do not force-push. Do not delete the GitHub repository.
8. Then add the result note to this work order and correct only the Library page this function made stale.

---

## 4. Non-goals

- Do not overwrite EcoFlow BLE, the poller, Hawaiʻi weather, the globe collector, camera grabs, Kokoro, or `geology_collect.py`.
- Do not edit `jobs.py`.
- Do not pip-install `meta-ai-api` or any other package. Do not add a second env file. Do not commit secrets. No new `master-key.env` key names.
- Do not call `MetaAI().prompt` without `--send` and Alexander’s sign-off.
- Do not add a public website page. Do not edit the Vercel app shell.
- Do not edit other agents’ files. No shared old-repo file belongs to this function.
- Do not import logs, transcripts, or other generated data into Pacific, Database git, the website, or git.
- Do not restore files under `~/.ollama/skills/energy`, automations, or `coms/ssh/local-data-globe`.
- Do not delete the GitHub repository. Do not force-push.

---

## 5. Key file / path reference

| Path | Role |
|------|------|
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/MetaAI/scripts/meta.py` | New CLI (add at build) |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/MetaAI/__init__.py` | Package `MetaAI` (add at build) |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/MetaAI/README.md` | Short README (add at build) |
| `2 - RootRecord-Database/Communications/MetaAI/` | Last transcript JSON after a signed-off send (runtime; not git) |
| `2 - RootRecord-Database/Logs/Communications/MetaAI/` | Logs only (runtime; not git) |
| `2 - RootRecord-Database/.gitignore` | Ignore the two runtime dirs. Pause if another agent is editing this file. |
| `operations/meta/meta.py` in `rootrecordsoftwaresolutions/old` | Old source. Archive, then delete, only in phase 4. |

---

## 6. Open items

**Additional requirements:**

- Alexander accepts this draft and says to build before any runtime edit.
- Alexander signs off before any `--send` to meta.ai.
- Phase 4 runs only after the migration works, and only for `operations/meta/meta.py`.

---

## 7. Notes & constraints

- No force-push.
- Secrets stay out of git. No new `master-key.env` key names.
- Prefer small reversible steps.
- Sends to meta.ai, speaker playback, OBS, hardware switching, deletion of live Ecosystem files, and cloud spend require Alexander’s sign-off. Do not do those things in the draft phase. Phase 4 is already ordered for the old function’s file only: archive first, then remove it from the old repo locally and on GitHub.
- Small test that proves the new behavior: from `Communications/MetaAI/scripts`, `python3 meta.py --check` does not call `prompt` and does not pip-install.
- Shared old-repo files to leave: none. `operations/meta/meta.py` is the only file in that directory, and nothing else in the old repo imports it.
- If the archive copy fails, do not delete.
- After phase 4, add a short result note here (what landed, what was archived, what was removed on GitHub) and correct only matrix row 86 in `Documentation/00-architecture/Old-Repo-Migration-Matrix.md`.
- Do not rewrite unrelated work orders. Do not promote this draft onto the active index.

---

*Work order prepared 2026-09-30 HST. Update status when closed.*

---

## Archive / location note

**Active / accepted WOs** — filename when saved:

```text
Meta_AI_chat_client_Work_Order_WO-MIG-45-2026-09-29.md
```

Location when accepted (not yet):

```text
Documentation/06-development/Work-Orders/
```

**Drafts (not on active index)** — this file:

```text
Documentation/06-development/Work-Orders/drafts/Meta_AI_chat_client_Work_Order_WO-MIG-45-2026-09-29.md
```

See `drafts/README.md` and WO-WOGEN-001. Do not auto-promote.

**Closed WOs:** set Status → COMPLETE/CLOSED → `git mv` into:

```text
Documentation/06-development/Work-Orders/Complete/
```

Human session logs archive under `Documentation/01-operations/archive/YYYY-Www/` (WO-ARCH) — separate from closed work orders.

---

## Result note

Built 2026-09-30 (HST).

- Landed: `Communications/MetaAI` (`__init__.py`, `scripts/meta.py`, `README.md`). Database README at `2 - RootRecord-Database/Communications/MetaAI/README.md`. Log marker at `2 - RootRecord-Database/Logs/Communications/MetaAI/.gitkeep`. Ignore lines in `2 - RootRecord-Database/.gitignore`. `jobs.py` was already modified by another agent and was not edited.
- Test: `python3 meta.py --check` printed JSON with `"send": false` and `"package": "meta-ai-api"`, exit 2, because the package is not installed. No pip install. A follow-up with a stand-in `meta_ai_api` confirmed no-args, `--check`, and a bare message do not call `prompt`. `--send` was not run.
- Archived: `Old repos deleted and merged/old/operations/meta/meta.py` (87 lines, checksum matched the old file).
- Removed on GitHub: `rootrecordsoftwaresolutions/old` commit `1315506` on `cursor/radio-idle-obs-gates`. Message: "Remove the Meta AI chat client now archived in the Ecosystem." No force-push. Repository not deleted. No shared file left.
