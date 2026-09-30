# WORK ORDER — Code review pack

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-MIG-34-2026-09-29 |
| **Date** | 2026-09-30 (HST) |
| **Status** | OPEN — pack landed. jobs.py block paused. Not promoted. |
| **Owner** | RootRecord |
| **Related** | Agent 34. Wave E. Cloud and keys, after the local path. No later function depends on this one. Matrix row 67. Scheduler map row `code-review`. |

**Scope:** One function, the code review pack. This draft names Folder `CodeReview` and the three paths, and it records the build that waits for acceptance. EcoFlow BLE, the poller, Hawaiʻi weather, the globe collector, camera grabs, Kokoro, `geology_collect.py`, and template reports stay as they are. No public page. No model load and no cloud spend in this draft.

---

## 1. Intent

The old pack at `/home/rootrecord/old ollama/old skills/code-review/scripts/code_review.py` writes markdown only. It gathers facts, optionally chats with local `qwen2.5-coder` (`keep_alive=0`), and writes `store/CURRENT.md`, a dated file, and `DROP-INTO-CURSOR.md`. It never patches the tree. G1 fired that pack at 11:20 and 17:20 HST. `scripts/job.py` still imports `apps.core.services.code_review`. There is no `~/.ollama/skills/code-review`.

The live poller has no review job. The pack is absent because it needs a model load and it was not designed in the new jobs file.

The live system already runs EcoFlow BLE, the poller, Hawaiʻi weather, the globe collector, camera grabs, Kokoro, `geology_collect.py`, and template reports. Those stay.

This function, once accepted, is a new review job. It writes an evidence pack and leaves the coder section off. It does not schedule the old 11:20 and 17:20 pack, and it does not pull `qwen2.5-coder`.

---

## 2. Current reality

### 2.1 What exists

Folder name, used in all three paths: **CodeReview**. It is its own capitalized Folder. It is not a subfolder of Reports, System, or Github. No lowercase twin. No symlink. No `Logs/` directory on the server.

| Item | Location / status |
| --- | --- |
| Folder | `CodeReview`. Landed 2026-09-30 01:06 HST. |
| Code | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/CodeReview/scripts` |
| Database | `2 - RootRecord-Database/CodeReview/` (packs: `CURRENT.md` and dated files) |
| Logs | `2 - RootRecord-Database/Logs/CodeReview/` |
| Secrets | `/home/rootrecord/master/master-key.env` only. Key names for this function: none. No `envload.py`. No second env file. |
| Old source read | `/home/rootrecord/old ollama/old skills/code-review/` (`scripts/code_review.py`, `scripts/job.py`, `SKILL.md`, `INDEX.md`, `DAILY.md`, `references/migrate.md`) |
| Old GitHub tree | Tracked by `git@github.com:rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server.git` from the `old ollama/old skills` checkout. Tracked files: `code-review/DAILY.md`, `INDEX.md`, `SKILL.md`, `references/migrate.md`, `scripts/code_review.py`, `scripts/job.py`. `store/` is gitignored. |
| Skill path, leave it | `~/.ollama/skills` has no `code-review` directory. |
| History snapshots, leave them | `/home/rootrecord/old ollama/github-history/09202026 1830/code-review` and `09202026 Early AM/code-review` |
| Shared import, leave it | `apps.core` is imported by the old `job.py` and is not in the `code-review/` tree. |
| Live jobs | No `code_review` or `code_review_pack` entry in `Automations/scripts/jobs.py`. |
| Matrix | Row 67 status missing. This draft does not edit that row. |
| Scheduler map | `code-review` is BLOCKED (LLM model load). This draft does not edit that row. |

### 2.2 Completed so far

- [x] Old pack read. It writes markdown and never patches source.
- [x] Folder and the three paths named above.
- [x] `master-key.env` checked for key names only. No key belongs to this function.
- [x] `CodeReview/scripts/code_review.py` and `CodeReview/README.md`.
- [ ] Gated `code_review_pack` block in `jobs.py`. Paused: that file was already being edited.
- [x] `/CodeReview/` and `/Logs/CodeReview/` in `2 - RootRecord-Database/.gitignore`.
- [x] Smoke test under `/tmp/rr-mig-34` (2026-09-30 01:06 HST).
- [x] Phase 4 archive and GitHub file deletion.
- [x] Result note, and the two Library rows named in task 8.

### 2.3 Known friction

- Build waits until Alexander accepts this draft. No other function has to exist before that build.
- `jobs.py` and `2 - RootRecord-Database/.gitignore` stay untouched by this draft. If either is already being edited at build time, pause.
- `store/` markdown is generated and gitignored in the old repo. Phase 4 archives it locally. It is not a GitHub deletion.
- The checkout that holds the tracked files is `/home/rootrecord/old ollama/old skills`, remote `Solar-Pacific-RootRecord-Server`. The matrix names `Solar-Pacific-RootRecord-Server-Old/code-review`. That `-Old` archive tree on this machine has no `code-review/` directory. Phase 4 uses the checkout that actually tracks the files.

---

## 3. Tasks

Do these only after Alexander accepts this draft and says to build. Until then, stop.

1. Create `1 - Servers/1 - RootRecord-Pacific-Solar-Server/CodeReview/` with package name `CodeReview`. Add `CodeReview/scripts/code_review.py` and a short `CodeReview/README.md`. The script writes markdown only. It does not patch source. No `Logs/` directory on the server. Logs go only under `2 - RootRecord-Database/Logs/CodeReview/`.
2. Evidence comes from the Ecosystem root: `git status --short -uno` (capped) and error, exception, or traceback lines from an allowlist of existing Database logs. Skip lines that contain `password`, `api_key`, `token=`, `secret`, `sk-`, or `bot`. Leave out the old Windows pieces: `apps.core`, voice-clip checks, `net-gate.json`, `governance.json`, `C:\Users\rootr\context\common-bugs`, and the Ava tree header.
3. The pack includes a coder section that says it is off. No call to `run-infer.sh`, Ollama, or a cloud API unless Alexander later sets `RR_CODE_REVIEW_CODER=1`. That flag stays unset. Do not pull `qwen2.5-coder`.
4. Do not edit `jobs.py` unless this accepted build inserts only the gated block below. `RR_CODE_REVIEW` stays unset. `at_times` stays empty so the old 11:20 and 17:20 clock is not restored. The command has no coder flag.

```python
{
    # Code review pack (WO-MIG-34). Evidence markdown only. OFF unless RR_CODE_REVIEW=1
    # at poller start. Empty at_times: not the old 11:20 / 17:20 pack. No coder flag.
    "id": "code_review_pack",
    "enabled": os.environ.get("RR_CODE_REVIEW", "0") == "1",
    "description": "Code review pack (WO-MIG-34). Evidence markdown only. No model load. Gate RR_CODE_REVIEW stays unset.",
    "at_times": [],
    "builtin": "",
    "command": f'nice -n 10 python3 "{PACIFIC}/CodeReview/scripts/code_review.py"',
    "timeout_sec": 60,
    "needs_internet": False,
    "cwd": f"{PACIFIC}/CodeReview",
    "env": {},
}
```

5. Add a `/CodeReview/` ignore under `2 - RootRecord-Database/.gitignore` so generated packs stay out of git. If `jobs.py` or that gitignore is already being edited, pause.
6. Smoke test: run the script with output rooted at `/tmp/rr-mig-34`. Expect exit 0, a `CURRENT.md` plus one dated file, a coder section that says off, and no inference process. That test does not write the live Database path.
7. After the smoke test passes: copy the old `code-review/` tree, including `store/` markdown, into `/home/rootrecord/RootRecord-Ecosystem/Old repos deleted and merged/Solar-Pacific-RootRecord-Server/code-review/`, keeping the path it had inside the old repo. Generated data that lived beside that source goes into this archive too, and still does not go into the live Folders. After the archive copy is on disk, delete the tracked files from the `old ollama/old skills` checkout and from GitHub `Solar-Pacific-RootRecord-Server`. Commit that deletion and push it. Do not force-push. Do not delete the GitHub repository. If the archive copy fails, do not delete. Leave the `github-history` snapshots. Leave `apps.core`. Leave `~/.ollama/skills`. `store/` is gitignored, so it is archived locally and is not a GitHub deletion.
8. Update this work order with the result note (what landed, what was archived, what was removed on GitHub) and set the new status. Correct only row 67 of `5 - RootRecord-Library/Documentation/00-architecture/Old-Repo-Migration-Matrix.md` and the `code-review` row of `5 - RootRecord-Library/Documentation/00-architecture/G1-Scheduler-To-G3-Jobs-Map-2026-09-29.md`. Do not rewrite unrelated work orders.

---

## 4. Non-goals

- Do not overwrite EcoFlow BLE, the poller, Hawaiʻi weather, the globe collector, camera grabs, Kokoro, `geology_collect.py`, or template reports.
- Do not schedule the old pack at 11:20 and 17:20. Do not port `scripts/job.py` or its `apps.core` import.
- Do not pull `qwen2.5-coder`. Do not call `run-infer.sh`, Ollama, or a cloud API while `RR_CODE_REVIEW_CODER` is unset.
- Do not restore or delete `~/.ollama/skills`, the `github-history` snapshots, or `apps.core`.
- Do not import logs, samples, last-state files, generated reports, collected images, radar frames, zip archives of collected data, database dumps, caches, virtualenvs, `node_modules`, or `__pycache__` into Pacific, Database, the website, or git. The old `store/` packs go to the phase 4 archive only.
- Do not send, play audio, touch OBS, switch hardware, delete live Ecosystem files, or spend cloud money. Phase 4 deletion is limited to this function's old files, and only after they are in `Old repos deleted and merged`.
- Do not enable `code_review_pack`. Do not set `RR_CODE_REVIEW` or `RR_CODE_REVIEW_CODER`.
- Do not add a public page or a second Vercel app. Android apps in `6 - Android Development` stay there.
- Do not build any other agent's function. If `jobs.py`, the Vercel app shell, or `master-key.env` is already being edited, pause.
- Do not put a secret value in this file or in git.

---

## 5. Key file / path reference

| Path | Role |
|------|------|
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/CodeReview/scripts` | Code. Landed. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/CodeReview/scripts/code_review.py` | Evidence pack writer. Markdown only. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/CodeReview/README.md` | Short folder note. |
| `2 - RootRecord-Database/CodeReview/` | Packs (`CURRENT.md`, dated files). Gitignored on build. |
| `2 - RootRecord-Database/Logs/CodeReview/` | Logs only. |
| `2 - RootRecord-Database/.gitignore` | `/CodeReview/` and `/Logs/CodeReview/` added. |
| `/home/rootrecord/master/master-key.env` | Unchanged. No key name for this function. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Automations/scripts/jobs.py` | Left unchanged. The file was already being edited, so the gated block was not inserted. |
| `/home/rootrecord/old ollama/old skills/code-review/` | Old source read for this draft. Phase 4 archive source. |
| `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/code-review/` | Phase 4 archive. 24 files copied. |
| `5 - RootRecord-Library/Documentation/00-architecture/Old-Repo-Migration-Matrix.md` | Row 67, after phase 4 only. |
| `5 - RootRecord-Library/Documentation/00-architecture/G1-Scheduler-To-G3-Jobs-Map-2026-09-29.md` | `code-review` row, after phase 4 only. |

---

## 6. Open items

**Additional requirements:**

- Alexander accepts this draft before any build.
- `RR_CODE_REVIEW_CODER=1` is required before any model load. It stays unset. That sign-off is also the gate for `run-infer.sh`, Ollama, and any cloud call.
- Enabling `code_review_pack` or setting `RR_CODE_REVIEW` needs a separate sign-off. A clock other than an empty `at_times` needs a separate sign-off. 11:20 and 17:20 stay unused.
- Phase 4 pauses if the archive copy fails.
- If `jobs.py` or `2 - RootRecord-Database/.gitignore` is already being edited at build time, pause.

---

## 7. Notes & constraints

- No force-push.
- Secrets stay out of git. This function has no `master-key.env` key names.
- Prefer small reversible steps.
- Sign-off before any send, speaker playback, OBS, hardware switch, deletion of live Ecosystem files, model load, or cloud spend. Phase 4 deletion is limited to this function's old files, and only after they are in `Old repos deleted and merged`. Do not delete the GitHub repository.
- Small test, 2026-09-30 01:06 HST: `python3` `CodeReview/scripts/code_review.py --root /tmp/rr-mig-34` exited 0. Wrote `CURRENT.md` and `2026-09-30-0106.md`. Coder line `_Coder off._`. Log line `coder=off`. Live `2 - RootRecord-Database/CodeReview/` was not created.
- Result note (2026-09-30 01:15 HST): Landed `CodeReview/` (`scripts/code_review.py`, `README.md`, package `CodeReview`). Packs and the run log are gitignored. `jobs.py` was already modified, so the gated `code_review_pack` block was not inserted. `RR_CODE_REVIEW` and `RR_CODE_REVIEW_CODER` stay unset. Archived 24 files at `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/code-review/`. Removed the six tracked files from `old ollama/old skills` and from GitHub `Solar-Pacific-RootRecord-Server` branch `online-safe-20260920` commit `8e6be6f2`. `store/` was gitignored, so it is in the archive and was not a GitHub file. Left `github-history` snapshots, `apps.core`, and `~/.ollama/skills`.

---

*Work order prepared 2026-09-30 HST. Update status when closed.*

---

## Archive / location note

This file is a draft. It is not on the active index. Do not auto-promote.

```text
Documentation/06-development/Work-Orders/drafts/Code_review_pack_Work_Order_WO-MIG-34-2026-09-29.md
```

See `drafts/README.md` and WO-WOGEN-001. Do not auto-promote.

**Closed WOs:** set Status → COMPLETE/CLOSED → `git mv` into:

```text
Documentation/06-development/Work-Orders/Complete/
```

Human session logs archive under `Documentation/01-operations/archive/YYYY-Www/` (WO-ARCH) — separate from closed work orders.
