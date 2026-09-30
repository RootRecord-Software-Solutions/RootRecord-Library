# WORK ORDER — Earthquake Discord post

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-MIG-23-2026-09-29 |
| **Date** | 2026-09-30 (HST) |
| **Status** | OPEN — dry-run landed, live send not signed off |
| **Owner** | RootRecord |
| **Related** | Agent 23. Wave D. One send pipe, then the messages. Depends on 21 Discord poller. No later function in this list depends on this one. Matrix row 1 (Discord half only). WO-COM-002. |

**Scope:** Earthquake Discord post is one Geology subfolder. The dry-run script and the three paths are on disk. The job stays off. No token was written, no message was sent, and nothing was archived. Live send still needs a separate sign-off. The collector, the voice report, the Discord poller, Slack, the Kilauea queue, and the economy brief stay with their own owners.

---

## 1. Intent

The old hourly script at `/home/rootrecord/old ollama/old skills/earthquakes/earthquake-hourly/scripts/earthquake_hourly.py` (about lines 354–375) posted a deduped earthquake report to Discord channel `ava_home`. The message text was “Carly earthquake report generated.” The attachments were the markdown report and the WAV. That file also fetches USGS, builds the spoken script, notifies Telegram, and plays the speaker. Those other behaviors are already ported or stay blocked. This function is only the Discord post.

The live system already collects USGS. Pacific `Geology/scripts/geology_collect.py` writes Database `Geology/Earthquakes/{hawaii,global}-last.json`. Pacific `Media/Voice/scripts/voice_reports.py` `b_earthquake_report` already turns those files into report text. Both stay. This function does not re-fetch USGS, does not replace either script, does not attach a WAV, and does not play the speaker.

Once accepted, it formats a short message from the collector files and hands that text to the Discord send pipe. The default run is a dry-run: print the message, do not call Discord.

---

## 2. Current reality

### 2.1 What exists

Folder name, used in all three paths: **Earthquake-Discord**. It is a subfolder of Geology. No second top-level domain. No lowercase twin. No symlink. No `Logs/` directory on the server. Python is invoked by script path, same as `Energy/Smart-Devices/scripts/`.

| Item | Location / status |
| --- | --- |
| Folder | `Earthquake-Discord` under Geology. Staged 2026-09-30. |
| Code | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Geology/Earthquake-Discord/scripts` |
| Database | `2 - RootRecord-Database/Geology/Earthquake-Discord/` (posted digest only; USGS samples stay in `Geology/Earthquakes/`) |
| Logs | `2 - RootRecord-Database/Logs/Geology/Earthquake-Discord/` |
| Secrets | `/home/rootrecord/master/master-key.env` only. Allowlist key name this function may read: `DISCORD_EARTHQUAKE_CHANNEL_ID`. That key is not in the file today. No second env file. Values are never printed. |
| Bot token | `DISCORD_BOT_TOKEN` belongs to the Discord poller and WO-COM-002. This function does not load it and does not open a second Discord client. |
| Collector, keep | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Geology/scripts/geology_collect.py` → `2 - RootRecord-Database/Geology/Earthquakes/{hawaii,global}-last.json`. Live. Do not replace. |
| Voice, keep | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Media/Voice/scripts/voice_reports.py` `b_earthquake_report`. No delivery. Do not replace. |
| Send pipe | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/Discord/scripts` is in place (agent 21). This function calls it only with `--send`. Default dry-run does not. |
| Old source read | `/home/rootrecord/old ollama/old skills/earthquakes/earthquake-hourly/scripts/earthquake_hourly.py`. Shared with the collector and the voice report. Leave it. |
| Old GitHub tree | `Solar-Pacific-RootRecord-Server-Old/earthquakes/earthquake-hourly/` is not on disk. No exclusive file to archive. |

### 2.2 Completed so far

- [x] Old Discord block read. Collector and voice report confirmed as the live data path.
- [x] Folder `Earthquake-Discord` and the three paths named above.
- [x] `master-key.env` checked for key names only. No `DISCORD_*` key is present.
- [x] Alexander said to keep working and stage missing folders.
- [x] Discord poller folder `Communications/Discord/scripts` was already in place. Not built here.
- [x] `Geology/Earthquake-Discord/scripts/earthquake_discord_post.py` dry-run against the files already on disk. Exit 0. Printed Hawaii 9 and Global 34. No `posted-last.json`.
- [x] Gated `jobs.py` block `earthquake_discord_post`, left off unless `RR_EARTHQUAKE_DISCORD=1`.
- [x] Phase 4: nothing exclusive to archive. Shared `earthquake_hourly.py` stays. No GitHub deletion.
- [x] Result note below. Library lines for this post corrected. Live send still unsigned.

### 2.3 Known friction

- The pipe’s `post_message` (agent 21) returns without HTTP unless `RR_DISCORD_POST=1`. That gate stays unset. This function’s own gate `RR_EARTHQUAKE_DISCORD` also stays unset.
- `earthquake_hourly.py` is shared with the already-migrated collector and voice report. Phase 4 leaves it. Do not delete `communications/discord` (agent 21).
- WO-COM-002 requires a new bot token before any live Discord login. This draft does not add a key.

---

## 3. Tasks

Done 2026-09-30. Recorded here so the order of work stays visible. Live send was not part of this pass.

1. `Communications/Discord/scripts` was already in place. The Discord poller was not built here.
2. `jobs.py` received only the gated block below. `RR_EARTHQUAKE_DISCORD` stays unset, so `enabled` is false at poller start.
3. Done. `earthquake_discord_post.py` reads the two last files, formats new events plus 24-hour counts, and skips when `posted-last.json` has the same collector digest. Default is dry-run.
4. Done. Only the gated block below was inserted. The job stays off.

```python
{
    # Earthquake Discord post (WO-MIG-23). OFF unless RR_EARTHQUAKE_DISCORD=1
    # is in the poller's environment at poller start. Dry-run by default. No send.
    "id": "earthquake_discord_post",
    "enabled": os.environ.get("RR_EARTHQUAKE_DISCORD", "0") == "1",
    "description": "Format Database Geology/Earthquakes last files and hand text to the Discord send pipe. Dry-run unless a separate send sign-off is set.",
    "interval_sec": 3600,
    "builtin": "",
    "command": f'nice -n 10 python3 "{PACIFIC}/Geology/Earthquake-Discord/scripts/earthquake_discord_post.py"',
    "timeout_sec": 30,
    "needs_internet": False,
    "cwd": f"{PACIFIC}/Geology/Earthquake-Discord",
    "env": {},
}
```

5. Done. Dry-run against the files on disk printed Hawaii 9 and Global 34, wrote no `posted-last.json`, and made no Discord request. A second check with a matching digest in a temporary database printed `unchanged`. `--send` with no channel id printed `channel-absent` and wrote nothing. A live send still waits for a separate sign-off.
6. Done. `earthquake_hourly.py` is shared and stays. `Solar-Pacific-RootRecord-Server-Old/earthquakes/earthquake-hourly/` is absent. Nothing was copied, deleted, or pushed.
7. Done. Result note is in section 7. Library lines for this post now say the dry-run landed and the live send is still unsigned.

---

## 4. Non-goals

- Do not edit `geology_collect.py`, `kilauea_cams.py`, `earthquakes_backfill.py`, or `voice_reports.py`.
- Do not replace EcoFlow BLE, the Hawaiʻi weather poller, the globe collector, camera grabs, or Kokoro.
- Do not build the Discord poller, Slack poller, Kilauea public draft queue, council-quake Telegram, or the economy brief.
- Do not re-fetch USGS, attach a WAV, or play the speaker.
- Do not import logs, samples, last-state files, generated reports, collected images, radar frames, zip archives, database dumps, caches, virtualenvs, `node_modules`, or `__pycache__` into Pacific, Database, the website, or git. `posted-last.json` is runtime output and stays out of git.
- Do not send, play audio, touch OBS, switch hardware, delete live Ecosystem files, or spend cloud money.
- Do not enable `earthquake_discord_post`. Do not set `RR_EARTHQUAKE_DISCORD` or `RR_DISCORD_POST`.
- Do not add a public page or a second Vercel app.
- Do not edit other agents' files. If `jobs.py`, the Vercel app shell, or `master-key.env` is already being edited, pause.
- Do not put a Discord key value in this file or in git.
- Do not restore files under `~/.ollama/skills/energy`, automations, or `coms/ssh/local-data-globe`.

---

## 5. Key file / path reference

| Path | Role |
|------|------|
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Geology/Earthquake-Discord/scripts` | Code. Staged 2026-09-30. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Geology/Earthquake-Discord/scripts/earthquake_discord_post.py` | Formats collector output. Dry-run prints the message and does not call Discord. |
| `2 - RootRecord-Database/Geology/Earthquake-Discord/` | Posted digest only. Folder staged. Dry-run did not write `posted-last.json`. |
| `2 - RootRecord-Database/Geology/Earthquake-Discord/posted-last.json` | Runtime digest. Not committed. Not written by the dry-run. |
| `2 - RootRecord-Database/Logs/Geology/Earthquake-Discord/` | Logs only. |
| `2 - RootRecord-Database/Geology/Earthquakes/hawaii-last.json` | Collector output. Read. Do not overwrite. |
| `2 - RootRecord-Database/Geology/Earthquakes/global-last.json` | Collector output. Read. Do not overwrite. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Geology/scripts/geology_collect.py` | Live collector. Do not replace. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Media/Voice/scripts/voice_reports.py` | Spoken report. Do not replace. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/Discord/scripts` | Send pipe (agent 21). In place. Used only by `--send`. |
| `/home/rootrecord/master/master-key.env` | Unchanged. Key name `DISCORD_EARTHQUAKE_CHANNEL_ID` is absent. Token stays with the pipe. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Energy/lib/envload.py` | Allowlist pattern followed by `Earthquake-Discord/lib/envload.py`. Not edited. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Automations/scripts/jobs.py` | Gated `earthquake_discord_post` block inserted. Left off. |
| `/home/rootrecord/old ollama/old skills/earthquakes/earthquake-hourly/scripts/earthquake_hourly.py` | Shared old source. Leave it. |
| `5 - RootRecord-Library/Documentation/00-architecture/Old-Repo-Migration-Matrix.md` | Earthquake-hourly Discord clause updated. Speaker play still not ported. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Geology/README.md` | Earthquake Discord dry-run noted. Other posts still not ported. |
| `2 - RootRecord-Database/Geology/README.md` | Dry-run reader noted. Voice jobs still do not deliver. |
| `5 - RootRecord-Library/Documentation/00-architecture/Voice-Reports-G3.md` | Discord text post noted. Telegram post stays blocked. |
| `5 - RootRecord-Library/Documentation/06-development/Work-Orders/WO-COM-002-Discord-Bot-Credential-Rotation.md` | New token before any live login. Owned by the pipe. |

---

## 6. Open items

**Additional requirements:**

- A live Discord send needs a separate sign-off, a channel id in `DISCORD_EARTHQUAKE_CHANNEL_ID`, and the pipe’s `RR_DISCORD_POST=1`. Both gates stay unset.
- Enabling `earthquake_discord_post` or setting `RR_EARTHQUAKE_DISCORD` needs a separate sign-off.
- If `jobs.py`, the Vercel app shell, or `master-key.env` is already being edited at build time, pause.
- Phase 4 leaves the shared `earthquake_hourly.py`. There is no exclusive old file to delete.

---

## 7. Notes & constraints

- No force-push.
- Secrets stay out of git. The allowlist name for this function is `DISCORD_EARTHQUAKE_CHANNEL_ID`. Do not print the value. Do not load `DISCORD_BOT_TOKEN` here. Follow `Energy/lib/envload.py`: an allowlist of key names, never a second env file.
- Prefer small reversible steps.
- Sign-off before any send, speaker playback, OBS, hardware switch, deletion of live Ecosystem files, or cloud spend. Phase 4 deletion is limited to this function’s exclusive old files, and only after they are in `Old repos deleted and merged`. Do not delete the GitHub repository. The shared hourly script stays.
- Small test, 2026-09-30: dry-run against the current `hawaii-last.json` and `global-last.json`. Exit 0. Printed Hawaii 9 and Global 34. No `posted-last.json`. No Discord request.
- Result note (2026-09-30): Landed `Geology/Earthquake-Discord/scripts/earthquake_discord_post.py` and the three folders (code, Database `Geology/Earthquake-Discord/`, Logs `Logs/Geology/Earthquake-Discord/`). Dry-run printed the collector message and did not write `posted-last.json` or call Discord. Job `earthquake_discord_post` is in `jobs.py` and stays off. Archived: none. Removed on GitHub: none. `earthquake_hourly.py` is shared and stays.

---

*Work order prepared 2026-09-30 HST. Update status when closed.*

---

## Archive / location note

This file is a draft. It is not on the active index. Do not auto-promote.

```text
Documentation/06-development/Work-Orders/drafts/Earthquake_Discord_post_Work_Order_WO-MIG-23-2026-09-29.md
```

See `drafts/README.md` and WO-WOGEN-001. Do not auto-promote.

**Closed WOs:** set Status → COMPLETE/CLOSED → `git mv` into:

```text
Documentation/06-development/Work-Orders/Complete/
```

Human session logs archive under `Documentation/01-operations/archive/YYYY-Www/` (WO-ARCH) — separate from closed work orders.
