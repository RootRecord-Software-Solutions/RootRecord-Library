# WORK ORDER — Discord poller

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-MIG-21-2026-09-29 |
| **Date** | 2026-09-30 (HST) |
| **Status** | OPEN — code landed. Phase 4 blocked. Not promoted. |
| **Owner** | RootRecord |
| **Related** | Agent 21. Wave D. One send pipe, then the messages. Later functions depend on this folder: 22 Slack poller; 23 Earthquake Discord post; 24 Kilauea public draft queue; 29 Economy brief. Matrix row 59 (Discord half). WO-COM-002. |

**Scope:** Discord polling is one Communications subfolder. The script, empty channel list, and disabled job block are landed. Phase 4 (archive and GitHub deletion) is not done. No token was written, no Discord request was made, and no message was sent. Slack, earthquake posts, the Kilauea queue, and the economy brief stay with their own agents.

---

## 1. Intent

The old helper at `/home/rootrecord/old ollama/old skills/communications/discord/scripts/discord.py` is Discord REST: `get_messages`, `get_me`, and post, pin, forward, and DM. The AWS stub `1 - Servers/2 - RootRecord-US-Mainland-Server/communications/discord/poll.py` checks `DISCORD_BOT_TOKEN` and does nothing. Pacific `Communications/discord/` was a README. The poller now lives at `Communications/Discord/`. `master-key.env` still has no Discord key, and posting has no sign-off (WO-COM-002).

The live system already runs Telegram `council_relay` (one `getUpdates` owner), EcoFlow BLE, the Hawaiʻi weather poller, `geology_collect.py`, the globe collector, camera grabs, and Kokoro. Those stay.

This function polls only. It does not post. `post_message` returns without HTTP unless `RR_DISCORD_POST=1`, and that gate stays unset. Later agents call this folder. They are not built here.

---

## 2. Current reality

### 2.1 What exists

Folder name, used in all three paths: **Discord**. It is a subfolder of Communications. No second top-level domain. No lowercase twin. No symlink. No `Logs/` directory on the server.

| Item | Location / status |
| --- | --- |
| Folder | `Discord` under Communications. Landed 2026-09-30 00:34 HST. Lowercase `discord/` removed. |
| Code | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/Discord/scripts` |
| Database | `2 - RootRecord-Database/Communications/Discord/` |
| Logs | `2 - RootRecord-Database/Logs/Communications/Discord/` |
| Secrets | `/home/rootrecord/master/master-key.env` only. Allowlist key name: `DISCORD_BOT_TOKEN`. That key is not in the file today. No second env file. |
| Existing shell | Lowercase `Communications/discord/` removed 2026-09-30. README is `Communications/Discord/README.md`. Not LIVE. |
| Old source read | `/home/rootrecord/old ollama/old skills/communications/discord/scripts/discord.py` |
| AWS stub, leave it | `1 - Servers/2 - RootRecord-US-Mainland-Server/communications/discord/poll.py` |
| Skill copies, leave them | `~/.ollama/skills/coms/discord` and `old ollama/old skills/communications/discord`. Do not restore them. Do not delete them in phase 4. |
| Old GitHub tree | `Solar-Pacific-RootRecord-Server-Old/communications/discord` is not a separate checkout on this machine. The archive folder is inside the Ecosystem repo and has no `communications/` directory. |
| Live Telegram | `council_relay` stays the one `getUpdates` owner. |
| Matrix | Row 59 Discord half is partial (2026-09-30). Slack half left missing. |

### 2.2 Completed so far

- [x] Old helper and the AWS stub read. Pacific shell confirmed as a README.
- [x] Folder and the three paths named above.
- [x] `master-key.env` checked for key names only. No Discord key is present.
- [x] `Communications/Discord/` script, env allowlist, README move, and disabled `jobs.py` block.
- [x] No-token test 2026-09-30 00:34 HST: exit 0, `token` absent, `channels` 0, `http_calls` 0. `post_message` returned None.
- [ ] Phase 4 archive and GitHub file deletion (blocked: no local checkout of `Solar-Pacific-RootRecord-Server-Old/communications/discord`).
- [x] Result note below. Matrix row 59 Discord half set to partial. Slack half left missing.

### 2.3 Known friction

- Tasks 1–4 and the result note are done. The job stays `enabled: False`.
- Lowercase `Communications/discord/` is gone. One folder: `Communications/Discord/`.
- Phase 4 is paused. Checked again 2026-09-30 00:46 HST: no local checkout of `Solar-Pacific-RootRecord-Server-Old/communications/discord`. The only `communications/discord` tree on disk is `old ollama/old skills/communications/discord`, which stays. Do not clone the old repo. Do not delete that skill copy.
- `DISCORD_BOT_TOKEN` is still absent from `master-key.env` (key names only, rechecked 2026-09-30 00:46 HST). WO-COM-002 still requires a new token before any live login. Do not fall through `AVA_DISCORD_BOT_TOKEN`, `SEXI_DISCORD_BOT_TOKEN`, or `DISCORD_ROOTMC_BOT_TOKEN`. `config/channels.json` is `[]`.

---

## 3. Tasks

Tasks 1–5 and 7 are done. Task 6 is paused. The record below is what was built.

1. Create `Communications/Discord/` with package name `Discord`. Move `Communications/discord/README.md` into `Communications/Discord/README.md` in the same change. Do not leave a lowercase twin. No `Logs/` directory on the server. Logs go only under `2 - RootRecord-Database/Logs/Communications/Discord/`. **Done.**
2. Add `Communications/Discord/lib/envload.py` following `Energy/lib/envload.py`: an allowlist of `DISCORD_BOT_TOKEN` only, read from `/home/rootrecord/master/master-key.env`, never print values, never add a second env file. Add `Communications/Discord/scripts/poll.py`. No token, or an empty channel list: exit 0, write a status file under the Database path, do not call Discord. `post_message` returns without HTTP unless `RR_DISCORD_POST=1`. That gate stays unset. Do not set `RR_DISCORD_POLLER`.
3. Do not port `discord_chat.py` (persona replies) or `discord_september.py` (archive, nuke, rebuild).
4. Do not edit `jobs.py` unless this accepted build inserts only the disabled block below. Do not enable the job.

```python
{
    "id": "discord_poller",
    "enabled": False,
    "description": "Discord poller (WO-MIG-21). OFF. No token and no post. Gate RR_DISCORD_POLLER stays unset.",
    "interval_sec": 60,
    "builtin": "",
    "command": f'nice -n 10 python3 "{PACIFIC}/Communications/Discord/scripts/poll.py"',
    "timeout_sec": 30,
    "needs_internet": True,
    "cwd": f"{PACIFIC}/Communications/Discord",
    "env": {},
}
```

5. If `jobs.py` or `master-key.env` is already being edited, pause. Do not build Slack poller, earthquake Discord post, Kilauea public draft queue, or economy brief.
6. After the script works: copy this function's old-repo files into `/home/rootrecord/RootRecord-Ecosystem/Old repos deleted and merged/Solar-Pacific-RootRecord-Server-Old/`, keeping the path they had inside the old repo (`communications/discord/...`). **Paused 2026-09-30 00:46 HST.** No local checkout of `Solar-Pacific-RootRecord-Server-Old/communications/discord`. Do not clone it. Nothing archived. Nothing removed on GitHub. Leave the AWS stub. Leave `~/.ollama/skills/coms/discord` and `old ollama/old skills/communications/discord`.
7. Update this work order with the result note (what landed, what was archived, what was removed on GitHub) and set the new status. Correct only the Discord half of row 59 in `5 - RootRecord-Library/Documentation/00-architecture/Old-Repo-Migration-Matrix.md`. Leave the Slack half for agent 22. Do not rewrite unrelated work orders.

---

## 4. Non-goals

- Do not overwrite the Telegram `council_relay`, EcoFlow BLE, the Hawaiʻi weather poller, `geology_collect.py`, the globe collector, camera grabs, or Kokoro.
- Do not replace the AWS stub `communications/discord/poll.py`.
- Do not restore or delete `~/.ollama/skills/coms/discord` or `old ollama/old skills/communications/discord`.
- Do not port `discord_chat.py` or `discord_september.py`.
- Do not import logs, samples, last-state files, generated reports, collected images, caches, virtualenvs, `node_modules`, or `__pycache__` into Pacific, Database, the website, or git.
- Do not send, play audio, touch OBS, switch hardware, delete live Ecosystem files beyond this function's own lowercase README move, or spend cloud money.
- Do not enable `discord_poller`. Do not set `RR_DISCORD_POLLER` or `RR_DISCORD_POST`.
- Do not add a public page or a second Vercel app.
- Do not build Slack poller, earthquake Discord post, Kilauea public draft queue, or economy brief.
- Do not edit other agents' files. If `jobs.py` or `master-key.env` is already being edited, pause.
- Do not put a Discord key value in this file or in git.

---

## 5. Key file / path reference

| Path | Role |
|------|------|
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/Discord/scripts` | Code. Landed. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/Discord/scripts/poll.py` | The poller. No token means no Discord HTTP. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/Discord/lib/envload.py` | Allowlist `DISCORD_BOT_TOKEN` from `master-key.env`. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/Discord/README.md` | Absorbed the lowercase shell README. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/discord/` | Lowercase shell removed 2026-09-30. No twin. |
| `2 - RootRecord-Database/Communications/Discord/` | Runtime status. Gitignored. `status-last.json` written by the no-token test. |
| `2 - RootRecord-Database/Logs/Communications/Discord/` | Logs only. |
| `/home/rootrecord/master/master-key.env` | Unchanged. Key name `DISCORD_BOT_TOKEN` is absent. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Automations/scripts/jobs.py` | Disabled `discord_poller` block only. `enabled: False`. |
| `1 - Servers/2 - RootRecord-US-Mainland-Server/communications/discord/poll.py` | AWS stub. Leave it. |
| `/home/rootrecord/old ollama/old skills/communications/discord/scripts/discord.py` | Old REST helper read for this draft. Not the phase 4 GitHub tree. |
| `Old repos deleted and merged/Solar-Pacific-RootRecord-Server-Old/communications/discord/` | Phase 4 archive path. Not copied in this draft. |
| `5 - RootRecord-Library/Documentation/00-architecture/Old-Repo-Migration-Matrix.md` | Row 59 Discord half set to partial. Slack half left missing. |
| `5 - RootRecord-Library/Documentation/06-development/Work-Orders/WO-COM-002-Discord-Bot-Credential-Rotation.md` | New token before any live login. |

---

## 6. Open items

**Additional requirements:**

- A new `DISCORD_BOT_TOKEN` in `master-key.env`, issued per WO-COM-002, is required before any live Discord login. This build did not add that key. Empty `channels.json` still does not call Discord after the key exists.
- `RR_DISCORD_POST=1` is required before any post. It stays unset.
- Enabling `discord_poller` or setting `RR_DISCORD_POLLER` needs a separate sign-off.
- Phase 4 pauses if there is no local checkout of `Solar-Pacific-RootRecord-Server-Old/communications/discord`, or if the archive copy fails.
- If `jobs.py` or `master-key.env` is already being edited at build time, pause.

---

## 7. Notes & constraints

- No force-push.
- Secrets stay out of git. The allowlist name is `DISCORD_BOT_TOKEN`. Do not print the value. Do not load `AVA_DISCORD_BOT_TOKEN`, `SEXI_DISCORD_BOT_TOKEN`, or `DISCORD_ROOTMC_BOT_TOKEN`.
- Prefer small reversible steps.
- Sign-off before any send, speaker playback, OBS, hardware switch, deletion of live Ecosystem files, or cloud spend. The lowercase README move is this function's own shell, done in the same change as `Communications/Discord/`. Phase 4 deletion is limited to this function's old files, and only after they are in `Old repos deleted and merged`. Do not delete the GitHub repository.
- Small test, 2026-09-30 00:34 HST: `poll.py` with no `DISCORD_BOT_TOKEN` exited 0, wrote `status-last.json` with `token` absent, `channels` 0, `http_calls` 0, `posted` false. `post_message` with the gate unset returned None. No Discord request.
- Result note (2026-09-30 00:34 HST): Landed `Communications/Discord/` (`scripts/poll.py`, `lib/envload.py` allowlist `DISCORD_BOT_TOKEN`, `lib/api.py` `post_message` refuses HTTP unless `RR_DISCORD_POST=1`, `config/channels.json` = `[]`, README, package `Discord`). Lowercase `Communications/discord/` removed. Disabled job `discord_poller` is in `jobs.py` (`enabled: False`). Nothing archived. Nothing removed on GitHub. Phase 4 stays blocked until a local checkout of `Solar-Pacific-RootRecord-Server-Old/communications/discord` exists. Token still absent; add `DISCORD_BOT_TOKEN` to `master-key.env` later. Empty `channels.json` still does not call Discord after that key exists.

---

*Work order prepared 2026-09-30 HST. Update status when closed.*

---

## Archive / location note

This file is a draft. It is not on the active index. Do not auto-promote.

```text
Documentation/06-development/Work-Orders/drafts/Discord_poller_Work_Order_WO-MIG-21-2026-09-29.md
```

See `drafts/README.md` and WO-WOGEN-001. Do not auto-promote.

**Closed WOs:** set Status → COMPLETE/CLOSED → `git mv` into:

```text
Documentation/06-development/Work-Orders/Complete/
```

Human session logs archive under `Documentation/01-operations/archive/YYYY-Www/` (WO-ARCH) — separate from closed work orders.
