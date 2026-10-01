# WORK ORDER — Slack poller

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-MIG-22-2026-09-29 |
| **Date** | 2026-09-30 (HST) |
| **Status** | LANDED — job gated off, not LIVE. Not promoted to the active index. |
| **Owner** | RootRecord |
| **Related** | Agent 22. Wave D. One send pipe, then the messages. Depends on 21 Discord poller. No later function depends on this one. Matrix row 59 (Slack half). |

**Scope:** Slack polling is one Communications subfolder. The poller is landed and gated off. No token was written, no message was sent, and `RR_SLACK` stays unset. Discord poller, Telegram relay, and every other agent's function stay with their own agents.

---

## 1. Intent

The old function is the mainland stub `1 - Servers/2 - RootRecord-US-Mainland-Server/communications/slack/poll.py`. If `SLACK_BOT_TOKEN` is unset it does nothing. If the token is set it still does nothing (`pass`). It never calls the Slack API and never posts. The mainland job `communications_slack` in `automations/scripts/jobs.py` is enabled, interval 1 second, and points at that stub. `communications/.env.example` has `SLACK=notsetupyet`. The root `.env.example` lists the name `SLACK_BOT_TOKEN` with no value.

Pacific keeps a live quiet Telegram council relay (`RR_RELAY_REPLIES` stays `0`, one `getUpdates` owner). The notify-policy draft stays unsealed. EcoFlow BLE, the Hawaiʻi weather poller, the globe collector, camera grabs, Kokoro, and `geology_collect.py` stay as they are. Slack is not a second live relay.

This function, once accepted, is the same no-post lane under `Communications/Slack`. No token means write `not_configured` and exit 0, with no HTTP. A present token still does not call Slack and does not post. Posting stays behind Alexander's sign-off.

---

## 2. Current reality

### 2.1 What exists

Folder name, used in all three paths: **Slack**. It is a subfolder of Communications. No second top-level domain. No lowercase twin. No symlink. No `Logs/` directory on the server.

| Item | Location / status |
| --- | --- |
| Folder | `Slack` under Communications. Created 2026-09-30. Lowercase `Communications/slack/` removed (README and `.gitkeep`). |
| Code | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/Slack/scripts` |
| Database | `2 - RootRecord-Database/Communications/Slack/` |
| Logs | `2 - RootRecord-Database/Logs/Communications/Slack/` |
| Secrets | `/home/rootrecord/master/master-key.env` only. Allowlist key name: `SLACK_BOT_TOKEN`. That key is not in the file today. No second env file. `SLACK` in the old example is a placeholder status, not a secret, and is not copied in. |
| Existing shell | Lowercase `Communications/slack/` removed. Text now lives in `Communications/Slack/README.md`. |
| Old source | Removed locally after archive. Was `1 - Servers/2 - RootRecord-US-Mainland-Server/communications/slack/poll.py`. |
| Old job line, shared file | `communications_slack` in `1 - Servers/2 - RootRecord-US-Mainland-Server/automations/scripts/jobs.py`. Leave it. That file also runs Telegram and Discord. |
| Shared examples, leave them | `communications/README.md`, `communications/.env.example`, and the mainland root `.env.example`. |
| Dependency | Discord poller (agent 21). `Communications/Discord/` was absent when this draft was first written, then present (`scripts/poll.py` and `lib/envload.py`) before the Slack build. |
| Live Telegram | `council_relay` stays the one `getUpdates` owner. Sandbox replies on. Live council stays quiet. |
| Matrix | Row 59 is one Discord/Slack line. Left unchanged so the Discord half is not rewritten. |

### 2.2 Completed so far

- [x] Old stub read. Pacific shell confirmed as a README.
- [x] Folder and the three paths named above.
- [x] `master-key.env` checked for key names only. No Slack key is present.
- [x] Discord poller folder `Communications/Discord/` was in place before the Slack build.
- [x] `Communications/Slack/` script, env allowlist, README move, and gated-off `jobs.py` block.
- [x] No-token test (exit 0, `not_configured`, `http_calls` 0) at 2026-09-30 00:35 HST.
- [x] Phase 4 archive and GitHub file deletion.
- [x] Result note, Pacific `Communications/README.md` slack row, and the absorbed Slack README.

### 2.3 Known friction

- Discord poller was missing at the first check and present before any Slack runtime file was added. It was not built here.
- Lowercase `Communications/slack/` was removed in the same change as `Communications/Slack/`.
- Pacific `jobs.py` has the gated block. `RR_SLACK` stays unset. The poller was not restarted.
- Mainland `automations/scripts/jobs.py` still has an enabled `communications_slack` line. That file is shared. It is named here and not edited.

---

## 3. Tasks

Do these only after Alexander accepts this draft and says to build. Until then, stop.

1. Pause if `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/Discord/` is missing. Name the function: Discord poller (agent 21). Do not build it.
2. Create `Communications/Slack/` with package name `Slack`. Move `Communications/slack/README.md` into `Communications/Slack/README.md` in the same change. Do not leave a lowercase twin. No `Logs/` directory on the server. Logs go only under `2 - RootRecord-Database/Logs/Communications/Slack/`.
3. Add `Communications/Slack/lib/envload.py` following `Energy/lib/envload.py`: an allowlist of `SLACK_BOT_TOKEN` only, read from `/home/rootrecord/master/master-key.env`, never print values, never add a second env file. Add `Communications/Slack/scripts/poll.py`. No token: exit 0, write `2 - RootRecord-Database/Communications/Slack/slack-last.json` with status `not_configured`, and a line under the Logs path. Do not call Slack. A present token still does not call Slack and does not post. Do not write a token into git or into `master-key.env`.
4. Do not edit `jobs.py` unless this accepted build inserts only the gated-off block below. Do not set `RR_SLACK`. Do not restart the poller. Do not touch any other job.

```python
{
    # Slack poller (WO-MIG-22). OFF unless RR_SLACK=1 at poller start. No token and no post.
    "id": "communications_slack",
    "enabled": os.environ.get("RR_SLACK", "0") == "1",
    "description": "Slack poller -> Database Communications/Slack/slack-last.json. No HTTP and no post until a token and sign-off exist.",
    "interval_sec": 60,
    "builtin": "",
    "command": f'nice -n 10 python3 "{PACIFIC}/Communications/Slack/scripts/poll.py"',
    "timeout_sec": 20,
    "needs_internet": False,
    "cwd": f"{PACIFIC}/Communications/Slack",
    "env": {},
}
```

5. Smoke test: run `poll.py` once with no `SLACK_BOT_TOKEN`. Expect exit 0, `not_configured` in `slack-last.json`, a log under `2 - RootRecord-Database/Logs/Communications/Slack/`, and no network.
6. If `jobs.py` or `master-key.env` is already being edited, pause.
7. After the script works: copy `communications/slack/poll.py` into `/home/rootrecord/RootRecord-Ecosystem/Old repos deleted and merged/US-Mainland-Server/communications/slack/poll.py`, keeping that path. Old repo: `rootrecordsoftwaresolutions/US-Mainland-Server`. If the archive copy fails, do not delete. If it succeeds, delete that file from the mainland checkout on this machine and on GitHub. Commit that deletion and push it. Do not force-push. Do not delete the GitHub repository. Leave mainland `automations/scripts/jobs.py`, `communications/README.md`, `communications/.env.example`, and the root `.env.example`.
8. Update this work order with the result note (what landed, the archive path, what was removed on GitHub) and set the new status. Correct Pacific `Communications/README.md` so slack is no longer described as only a shell, and correct the absorbed `Communications/Slack/README.md`. Do not rewrite unrelated work orders. Do not edit the Discord half of matrix row 59.

---

## 4. Non-goals

- Do not overwrite the Telegram `council_relay`, EcoFlow BLE, the Hawaiʻi weather poller, `geology_collect.py`, the globe collector, camera grabs, or Kokoro.
- Do not build Discord poller, and do not edit agent 21's files.
- Do not edit mainland `automations/scripts/jobs.py`, `communications/README.md`, `communications/.env.example`, or the root `.env.example`. The enabled `communications_slack` line stays and is named here.
- Do not import logs, samples, last-state files, generated reports, collected images, radar frames, zip archives, database dumps, caches, virtualenvs, `node_modules`, or `__pycache__` from the old repo into Pacific, Database, the website, or git. The new poller's own last file and log are written only by the smoke test under the Database paths above.
- Do not send, including `chat.postMessage`. Do not play audio, touch OBS, switch hardware, delete live Ecosystem files beyond this function's own lowercase README move, or spend cloud money.
- Do not enable `communications_slack` on Pacific. Do not set `RR_SLACK`.
- Do not add a public page or a second Vercel app.
- Do not edit other agents' files. If `jobs.py` or `master-key.env` is already being edited, pause.
- Do not put a Slack key value in this file or in git.
- Do not unseal the Communications notify-policy draft or add a notify job.
- Do not restore files under `~/.ollama/skills/energy`, automations, or `coms/ssh/local-data-globe`.

---

## 5. Key file / path reference

| Path | Role |
|------|------|
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/Slack/scripts` | Code. Landed. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/Slack/scripts/poll.py` | The poller. No token means no Slack HTTP. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/Slack/lib/envload.py` | Allowlist `SLACK_BOT_TOKEN` from `master-key.env`. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/Slack/README.md` | Absorbs the lowercase shell README on build. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/slack/` | Removed. No lowercase twin. |
| `2 - RootRecord-Database/Communications/Slack/` | `slack-last.json` from the no-token smoke test. |
| `2 - RootRecord-Database/Logs/Communications/Slack/` | Logs only. |
| `/home/rootrecord/master/master-key.env` | Unchanged. Key name `SLACK_BOT_TOKEN` is absent. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Energy/lib/envload.py` | Pattern for the allowlist loader. Not edited. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Automations/scripts/jobs.py` | Gated-off `communications_slack` block only. `RR_SLACK` unset. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/README.md` | Slack row updated. Email stays a shell. |
| `1 - Servers/2 - RootRecord-US-Mainland-Server/communications/slack/poll.py` | Old stub. Archived in phase 4, then removed locally and on GitHub. |
| `1 - Servers/2 - RootRecord-US-Mainland-Server/automations/scripts/jobs.py` | Shared. `communications_slack` line left in place. |
| `1 - Servers/2 - RootRecord-US-Mainland-Server/communications/README.md` | Shared. Left in place. |
| `1 - Servers/2 - RootRecord-US-Mainland-Server/communications/.env.example` | Shared. Left in place. `SLACK=notsetupyet` is not copied. |
| `1 - Servers/2 - RootRecord-US-Mainland-Server/.env.example` | Shared. Left in place. Name `SLACK_BOT_TOKEN` only. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/Discord/` | Dependency folder. Present before the Slack build. |
| `Old repos deleted and merged/US-Mainland-Server/communications/slack/poll.py` | Archive of the stub. On disk. |
| `5 - RootRecord-Library/Documentation/00-architecture/Old-Repo-Migration-Matrix.md` | Row 59 Slack half, after phase 4 only, and only that half. |

---

## 6. Open items

**Additional requirements:**

- `SLACK_BOT_TOKEN` in `master-key.env` is required before any Slack HTTP call. This work did not add that key. Even with a token, posting needs a separate sign-off.
- Enabling the Pacific job or setting `RR_SLACK` needs a separate sign-off.
- Mainland `communications_slack` stays enabled in the shared jobs file until a later sign-off edits that shared file. The stub it points at is already archived and removed.

---

## 7. Notes & constraints

- No force-push.
- Secrets stay out of git. The allowlist name is `SLACK_BOT_TOKEN`. Do not print the value.
- Prefer small reversible steps.
- Sign-off before any send (`chat.postMessage` included), speaker playback, OBS, hardware switch, deletion of live Ecosystem files, or cloud spend. The lowercase README move is this function's own shell, done in the same change as `Communications/Slack/`. Phase 4 deletion is limited to `communications/slack/poll.py`, and only after it is in `Old repos deleted and merged`. Do not delete the GitHub repository `rootrecordsoftwaresolutions/US-Mainland-Server`.
- Small test, run 2026-09-30 00:35 HST: `python3 Communications/Slack/scripts/poll.py` with no `SLACK_BOT_TOKEN`. Exit 0. `slack-last.json` status `not_configured`, token `absent`, `http_calls` 0, `posted` false. Log line in `2 - RootRecord-Database/Logs/Communications/Slack/poll.log`. The script has no HTTP client.
- `RR_SLACK` was unset, so the `communications_slack` job stays off. The poller was not restarted.

## Result (2026-09-30 HST)

Landed `Communications/Slack/` (`scripts/poll.py`, `lib/envload.py` allowlist `SLACK_BOT_TOKEN` only, package `Slack`). No token writes `not_configured` and does not call Slack. A present token still does not call Slack and does not post. Pacific `jobs.py` has one gated block, id `communications_slack`, enabled only when `RR_SLACK=1`. That flag is unset.

Archived to `Old repos deleted and merged/US-Mainland-Server/communications/slack/poll.py` (141 bytes, matched the stub before delete).

Removed `communications/slack/poll.py` from the mainland checkout. Ecosystem `HEAD` `3d04da9` (desk sync, already on `origin/main`) records that local deletion. Shared mainland files left in place: `automations/scripts/jobs.py` (enabled `communications_slack` line), `communications/README.md`, `communications/.env.example`, and the root `.env.example`.

Removed the same file on GitHub repo `rootrecordsoftwaresolutions/US-Mainland-Server`, branch `main`, commit `7d63359934a92a3872b390735a691ea984fd4871`. The contents API then returns 404. The repository was not deleted. No force-push.

Matrix row 59 is one shared Discord/Slack line. It was left unchanged so the Discord half is not rewritten.

This file stays in `drafts/`. It is not on the active index.

---

*Work order prepared 2026-09-30 HST. Update status when closed.*

---

## Archive / location note

This file is a draft. It is not on the active index. Do not auto-promote.

```text
Documentation/06-development/Work-Orders/drafts/Slack_poller_Work_Order_WO-MIG-22-2026-09-29.md
```

See `drafts/README.md` and WO-WOGEN-001. Do not auto-promote.

**Closed WOs:** set Status → COMPLETE/CLOSED → `git mv` into:

```text
Documentation/06-development/Work-Orders/Complete/
```

Human session logs archive under `Documentation/01-operations/archive/YYYY-Www/` (WO-ARCH) — separate from closed work orders.
