# WORK ORDER — Earthquake Discord post

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-MIG-23-2026-09-29 |
| **Date** | 2026-09-30 (HST) |
| **Status** | OPEN — draft, not accepted for execution |
| **Owner** | RootRecord |
| **Related** | Agent 23. Wave D. One send pipe, then the messages. Depends on 21 Discord poller. No later function in this list depends on this one. Matrix row 1 (Discord half only). WO-COM-002. |

**Scope:** Earthquake Discord post is one Geology subfolder. This draft names the folder and the three paths and records the build. No runtime files are edited, no job is enabled, no token is written, no message is sent, and nothing is archived until Alexander accepts this draft and says to build. The collector, the voice report, the Discord poller, Slack, the Kilauea queue, and the economy brief stay with their own owners.

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
| Folder | `Earthquake-Discord` under Geology. Not created. This draft only names it. |
| Code | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Geology/Earthquake-Discord/scripts` |
| Database | `2 - RootRecord-Database/Geology/Earthquake-Discord/` (posted digest only; USGS samples stay in `Geology/Earthquakes/`) |
| Logs | `2 - RootRecord-Database/Logs/Geology/Earthquake-Discord/` |
| Secrets | `/home/rootrecord/master/master-key.env` only. Allowlist key name this function may read: `DISCORD_EARTHQUAKE_CHANNEL_ID`. That key is not in the file today. No second env file. Values are never printed. |
| Bot token | `DISCORD_BOT_TOKEN` belongs to the Discord poller and WO-COM-002. This function does not load it and does not open a second Discord client. |
| Collector, keep | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Geology/scripts/geology_collect.py` → `2 - RootRecord-Database/Geology/Earthquakes/{hawaii,global}-last.json`. Live. Do not replace. |
| Voice, keep | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Media/Voice/scripts/voice_reports.py` `b_earthquake_report`. No delivery. Do not replace. |
| Send pipe | Agent 21 names `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/Discord/scripts`. Not created. The lowercase shell `Communications/discord/README.md` is a README only. |
| Old source read | `/home/rootrecord/old ollama/old skills/earthquakes/earthquake-hourly/scripts/earthquake_hourly.py`. Shared with the collector and the voice report. Leave it. |
| Old GitHub tree | `Solar-Pacific-RootRecord-Server-Old/earthquakes/earthquake-hourly/` is not on disk. No exclusive file to archive. |

### 2.2 Completed so far

- [x] Old Discord block read. Collector and voice report confirmed as the live data path.
- [x] Folder `Earthquake-Discord` and the three paths named above.
- [x] `master-key.env` checked for key names only. No `DISCORD_*` key is present.
- [ ] Alexander accepts this draft and says to build.
- [ ] Pause check: Discord poller folder `Communications/Discord` must exist before this build continues.
- [ ] `Geology/Earthquake-Discord/scripts/earthquake_discord_post.py` and a dry-run against the files already on disk.
- [ ] Proposed gated `jobs.py` block, left off.
- [ ] Phase 4: nothing exclusive to archive. Shared `earthquake_hourly.py` stays.
- [ ] Result note and the Library lines that still say this post was not ported.

### 2.3 Known friction

- Build waits until Alexander accepts this draft. The first build step pauses if `Communications/Discord` still has no send-pipe scripts. Name the missing function: Discord poller (agent 21). Do not build it.
- `jobs.py` is not edited by this draft. A gated block is proposed below. If `jobs.py`, the Vercel app shell, or `master-key.env` is already being edited at build time, pause.
- The pipe’s `post_message` (agent 21) returns without HTTP unless `RR_DISCORD_POST=1`. That gate stays unset. This function’s own gate `RR_EARTHQUAKE_DISCORD` also stays unset.
- `earthquake_hourly.py` is shared with the already-migrated collector and voice report. Phase 4 leaves it. Do not delete `communications/discord` (agent 21).
- WO-COM-002 requires a new bot token before any live Discord login. This draft does not add a key.

---

## 3. Tasks

Do these only after Alexander accepts this draft and says to build. Until then, stop.

1. Pause if `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/Discord/scripts` is not in place. Name the missing function: Discord poller (agent 21). Do not build it.
2. Pause if `jobs.py`, the Vercel app shell, or `master-key.env` is already being edited.
3. Add `Geology/Earthquake-Discord/scripts/earthquake_discord_post.py`. Read `2 - RootRecord-Database/Geology/Earthquakes/hawaii-last.json` and `global-last.json`. Format a short message: new events since the local digest, plus 24-hour counts. Compare a digest to `2 - RootRecord-Database/Geology/Earthquake-Discord/posted-last.json`. If unchanged, skip. If the pipe exists, hand it the text. Default is dry-run: print the message, do not call Discord, do not write `posted-last.json`.
4. Do not edit `jobs.py` unless this accepted build inserts only the gated block below. Do not enable the job. `RR_EARTHQUAKE_DISCORD` stays unset, so `enabled` is false at poller start.

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

5. One dry-run test against the files already on disk. Expect a printed message, no `posted-last.json` write, and no Discord request. A live send waits for a separate sign-off.
6. After the migration works, and before the Library update: `earthquake_hourly.py` is shared with the collector and the voice report. Leave it. `Solar-Pacific-RootRecord-Server-Old/earthquakes/earthquake-hourly/` is already absent, so there is no exclusive old-repo file to copy or delete. Do not delete `communications/discord`. Do not delete the GitHub repository. Do not force-push. If a later checkout shows an exclusive file for this post, copy it into `Old repos deleted and merged/<old-repo-name>/` keeping its old path, and delete it from the old repo locally and on GitHub only after that copy is on disk. If the archive copy fails, do not delete.
7. Update this work order with the result note (what landed, what was archived, what was removed on GitHub) and set the new status. Correct only the Library lines this function made stale: Pacific `Geology/README.md` “Not ported” Discord clause, Database `Geology/README.md` “no delivery”, the earthquake-hourly row in `Old-Repo-Migration-Matrix.md`, and the Voice-Reports line that this Discord post stays blocked. Do not rewrite unrelated work orders.

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
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Geology/Earthquake-Discord/scripts` | Code. Not created in this draft. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Geology/Earthquake-Discord/scripts/earthquake_discord_post.py` | Formats collector output. Dry-run prints the message and does not call Discord. |
| `2 - RootRecord-Database/Geology/Earthquake-Discord/` | Posted digest only. Not written in this draft. |
| `2 - RootRecord-Database/Geology/Earthquake-Discord/posted-last.json` | Runtime digest. Not committed. Not written by the dry-run. |
| `2 - RootRecord-Database/Logs/Geology/Earthquake-Discord/` | Logs only. |
| `2 - RootRecord-Database/Geology/Earthquakes/hawaii-last.json` | Collector output. Read. Do not overwrite. |
| `2 - RootRecord-Database/Geology/Earthquakes/global-last.json` | Collector output. Read. Do not overwrite. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Geology/scripts/geology_collect.py` | Live collector. Do not replace. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Media/Voice/scripts/voice_reports.py` | Spoken report. Do not replace. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/Discord/scripts` | Send pipe (agent 21). Must exist before this build continues. |
| `/home/rootrecord/master/master-key.env` | Unchanged. Key name `DISCORD_EARTHQUAKE_CHANNEL_ID` is absent. Token stays with the pipe. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Energy/lib/envload.py` | Allowlist pattern to follow. Do not edit. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Automations/scripts/jobs.py` | Proposed gated `earthquake_discord_post` block only. Not edited in this draft. |
| `/home/rootrecord/old ollama/old skills/earthquakes/earthquake-hourly/scripts/earthquake_hourly.py` | Shared old source. Leave it. |
| `5 - RootRecord-Library/Documentation/00-architecture/Old-Repo-Migration-Matrix.md` | Earthquake-hourly Discord clause, after phase 4 only. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Geology/README.md` | “Not ported” Discord clause, after the post works. |
| `2 - RootRecord-Database/Geology/README.md` | “no delivery” clause, after the post works. |
| `5 - RootRecord-Library/Documentation/00-architecture/Voice-Reports-G3.md` | Line that this Discord post stays blocked, after the post works. |
| `5 - RootRecord-Library/Documentation/06-development/Work-Orders/WO-COM-002-Discord-Bot-Credential-Rotation.md` | New token before any live login. Owned by the pipe. |

---

## 6. Open items

**Additional requirements:**

- Alexander accepts this draft before any build.
- Discord poller (agent 21) must have `Communications/Discord/scripts` in place before this build continues. If it does not, pause and name that function. Do not build it.
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
- Small test, at build time: run `earthquake_discord_post.py` as a dry-run against the current `hawaii-last.json` and `global-last.json`. Expect one printed message, no `posted-last.json`, and no Discord request. Not run for this draft.
- Result note: add it after phase 4 (what landed, what was archived, what was removed on GitHub). Not written yet. Archive path: none. `earthquake_hourly.py` is shared and stays. GitHub deletion: none for this function.

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
