# WORK ORDER — Kilauea public draft queue

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-MIG-24-2026-09-29 |
| **Date** | 2026-09-30 (HST) |
| **Status** | OPEN — built. Phase 4 pushed. Not promoted. |
| **Owner** | RootRecord |
| **Related** | Agent 24. Wave D. One send pipe, then the messages. No later function depends on this one. Build pauses if Council persona prompts (agent 03) or the Discord poller (agent 21) is missing. Matrix row 3 (public draft queue half). |

**Scope:** One Geology subfolder that queues a Kīlauea public draft from volcano JSON already on disk. Landed: the script, the gated job block, the temp-tree test, the archive, and the GitHub deletion of this function's old files. Still out of scope: Discord, Slack, or Telegram sends, and Grok.

---

## 1. Intent

The old runner at `/home/rootrecord/old ollama/old skills/kilauea/rr-kilauea/scripts/kilauea.py` (git repo `Solar-Pacific-RootRecord-Server`, path `kilauea/rr-kilauea/scripts/kilauea.py`) scraped HANS HTML. When the HVO notice id and alert level changed, it called Grok and `reports.queue_public_draft("kilauea", body[:1900])`. Council published that file later. The operator does not approve the draft. The first seen notice only seeds the publish hash. An unchanged fingerprint does not queue again. No notice id does not overwrite the last hash.

The live system already collects HVO status with the HANS API. `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Geology/scripts/geology_collect.py` writes `2 - RootRecord-Database/Geology/Volcanoes/kilauea-last.json` (`status_notice_id`, `alert_level`, `color_code`, `headline`, `erupting`, `latest_notice`). Keep that collector, `Geology/scripts/kilauea_cams.py`, `Media/Voice/scripts/voice_reports.py` `kilauea_report`, and the website page built from that JSON. Draft from that JSON. Do not bring back the HTML scrape.

---

## 2. Current reality

### 2.1 What exists

Folder name, used in all three paths: **PublicDraftQueue**. It is a subfolder of Geology. No second top-level domain. No lowercase twin. No symlink. No `Logs/` directory on the server. Installed 2026-09-30.

| Item | Location / status |
| --- | --- |
| Folder | `PublicDraftQueue` under Geology. Landed 2026-09-30. |
| Code | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Geology/PublicDraftQueue/scripts` |
| Database | `2 - RootRecord-Database/Geology/PublicDraftQueue/` |
| Logs | `2 - RootRecord-Database/Logs/Geology/PublicDraftQueue/` |
| Secrets | None. The queue reads JSON already on disk. No key names. `DISCORD_BOT_TOKEN` stays with the Discord poller. No second env file. |
| Live volcano JSON | `2 - RootRecord-Database/Geology/Volcanoes/kilauea-last.json` from `geology_collect.py`. Keep it. |
| Optional quake count | `2 - RootRecord-Database/Geology/Earthquakes/hawaii-last.json` field `kilauea_150km_count`, when that file is present. |
| Discord poller (agent 21) | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/Discord/` is on disk (2026-09-30). Package `Discord`. |
| Council persona (agent 03) | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/CouncilPersona/` is on disk (README). |
| Old source read | `/home/rootrecord/old ollama/old skills/kilauea/rr-kilauea/scripts/kilauea.py` and `queue_public_draft` in `old ollama/old skills/reports/scripts/reports.py`. |
| Old GitHub tree | Local checkout `/home/rootrecord/old ollama/old skills`, remote `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server`. Tracked path `kilauea/rr-kilauea/`. |
| Spoken desk, keep it | `voice_reports.py` `kilauea_report`, job gated `RR_VOICE_KILAUEA`. |
| Matrix | Row 3 stays partial because Grok is not ported. The draft-queue half is corrected. |

### 2.2 Completed so far

- [x] Old runner and `queue_public_draft` read. Live `kilauea-last.json` confirmed.
- [x] Folder name and the three paths named above.
- [x] Dependency folders checked. `Communications/Discord` and `Communications/CouncilPersona` are present.
- [x] Accepted build of `PublicDraftQueue` (2026-09-30).
- [x] Phase 4 archive and GitHub file deletion (`c1ea1dd5` on `online-safe-20260920`).
- [x] Result note and Library corrections.

### 2.3 Known friction

- Build ran after Alexander said to build. Sends, speaker playback, OBS, hardware, and cloud spend stayed off.
- `Communications/Discord` and `Communications/CouncilPersona` were present, so the dependency pause did not fire.
- `jobs.py` received only the gated `geology_kilauea_public_draft` block. `RR_KILAUEA_DRAFT` is unset. `master-key.env` was not edited.
- `reports/scripts/reports.py` is shared with weather, NWS, and the Cursor job. Leave it. The shim `origin/ns/apps/core/services/kilauea.py` and `kilauea/rr-kilauea/desk/scheduler.py` (symlink into the shared scheduler) stay too.

---

## 3. Tasks

Do these only after Alexander accepts this draft and says to build. Until then, stop.

1. Pause if `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/Discord` (agent 21) or `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/CouncilPersona` (agent 03) is missing. Name the missing function. Do not build it.
2. Create `Geology/PublicDraftQueue/` with package name `PublicDraftQueue`. Add `scripts/queue_draft.py` (stdlib). Read `2 - RootRecord-Database/Geology/Volcanoes/kilauea-last.json` only for the fingerprint and the body. Fingerprint is `status_notice_id` plus `alert_level`. No notice id does not overwrite the last hash. The first seen notice seeds `2 - RootRecord-Database/Geology/PublicDraftQueue/publish-last.json` and does not queue. An unchanged fingerprint does not queue. No `Logs/` directory on the server. No config directory.
3. On change, write one markdown file, at most 1900 characters, under `2 - RootRecord-Database/Geology/PublicDraftQueue/queue/`. Name pattern `YYYY-MM-DDTHHMMSS-kilauea-cron.md`. Header `**Ava kilauea report**`. Body from the JSON fields already collected: alert, color, headline, erupting, notice synopsis, and URL. Optional one line from `hawaii-last.json` `kilauea_150km_count` when that file is present. No HTTP. No Grok. No Discord, Slack, or Telegram call.
4. Log the decision (`seed`, `unchanged`, `queued`, or `no-notice`) under `2 - RootRecord-Database/Logs/Geology/PublicDraftQueue/`.
5. Do not edit `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Automations/scripts/jobs.py` unless this accepted build inserts only the gated block below. Do not set `RR_KILAUEA_DRAFT`. Do not add `geology_kilauea_public_draft` to the night-sleep never-skip list. It is a report draft, not a collector.

```python
{
    "id": "geology_kilauea_public_draft",
    "enabled": os.environ.get("RR_KILAUEA_DRAFT", "0") == "1",
    "description": "Queue a Kilauea public draft from Geology/Volcanoes/kilauea-last.json when the HVO notice id or alert level changes. No send.",
    "interval_sec": 3600,
    "builtin": "",
    "command": f'nice -n 10 python3 "{PACIFIC}/Geology/PublicDraftQueue/scripts/queue_draft.py"',
    "timeout_sec": 30,
    "cwd": f"{PACIFIC}/Geology/PublicDraftQueue",
    "env": {},
}
```

6. If `jobs.py` or `master-key.env` is already being edited, pause.
7. After the queue works: copy this function's old-repo source into `/home/rootrecord/RootRecord-Ecosystem/Old repos deleted and merged/Solar-Pacific-RootRecord-Server/kilauea/rr-kilauea/`, keeping the path it had inside the old repo. Copy `DAILY.md`, `INDEX.md`, `OFFLOADED`, `SKILL.md`, `references/migrate.md`, and `scripts/kilauea.py`. `__pycache__` beside that source goes into this archive too, and still does not go into Pacific, Database, the website, or git. After the archive copy is on disk, delete those same files from the old repo on this machine (`/home/rootrecord/old ollama/old skills`) and on GitHub (`rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server`). Commit that deletion and push it. Do not force-push. Do not delete the GitHub repository. If the archive copy fails, do not delete. Leave shared files: `reports/scripts/reports.py`, `origin/ns/apps/core/services/kilauea.py`, and `kilauea/rr-kilauea/desk/scheduler.py`.
8. Update this work order with the result note (what landed, the archive path, the GitHub deletion) and set the new status. Correct only these Library pages: `5 - RootRecord-Library/Documentation/00-architecture/Old-Repo-Migration-Matrix.md` row 3, `5 - RootRecord-Library/Documentation/00-architecture/G1-Scheduler-To-G3-Jobs-Map-2026-09-29.md`, `5 - RootRecord-Library/Documentation/00-architecture/Voice-Reports-G3.md`, and `5 - RootRecord-Library/Documentation/00-architecture/Geology-Domain-Ownership-Kilauea-Earthquakes-2026-09-28.md`. Do not rewrite unrelated work orders.

---

## 4. Non-goals

- Do not overwrite `geology_collect.py`, `kilauea_cams.py`, `voice_reports.py`, `Website/scripts/live_data_pages.py`, EcoFlow BLE, the Hawaiʻi weather poller, the globe collector, camera grabs, or Kokoro.
- Do not port Grok `report_generation`, `synth.polish`, TTS, blog publish, cam embeds, or subscriber DMs.
- Do not bring back the HANS HTML scrape.
- Do not build Council persona prompts or the Discord poller. Pause and name them if their folders are missing.
- Do not import logs, samples, last-state files, generated reports, collected images, radar frames, zip archives of collected data, database dumps, caches, virtualenvs, `node_modules`, or `__pycache__` into Pacific, Database, the website, or git.
- Do not send, play audio, touch OBS, switch hardware, delete live Ecosystem files, or spend cloud money.
- Do not set `RR_KILAUEA_DRAFT`. Do not enable `geology_kilauea_public_draft`.
- Do not add this job id to the night-sleep never-skip list.
- Do not add a public page or a second Vercel app.
- Do not edit other agents' files. Leave `reports/scripts/reports.py`, the `kilauea.py` shim, and the scheduler symlink.
- Do not delete the GitHub repository. Do not force-push.
- Do not restore files under `~/.ollama/skills/energy`, automations, or `coms/ssh/local-data-globe`.

---

## 5. Key file / path reference

| Path | Role |
|------|------|
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Geology/PublicDraftQueue/scripts` | Code. Landed. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Geology/PublicDraftQueue/scripts/queue_draft.py` | Stdlib queue writer. No HTTP. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Geology/PublicDraftQueue/README.md` | Folder note. Landed. |
| `2 - RootRecord-Database/Geology/PublicDraftQueue/publish-last.json` | Fingerprint seed. Written by a run, not by this draft file. |
| `2 - RootRecord-Database/Geology/PublicDraftQueue/queue/` | Draft markdown. One file per real change. |
| `2 - RootRecord-Database/Logs/Geology/PublicDraftQueue/` | Decision log. |
| `2 - RootRecord-Database/Geology/Volcanoes/kilauea-last.json` | Source JSON. Read only. |
| `2 - RootRecord-Database/Geology/Earthquakes/hawaii-last.json` | Optional `kilauea_150km_count` line. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Geology/scripts/geology_collect.py` | Live HANS collector. Do not replace. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Automations/scripts/jobs.py` | Gated block landed. `RR_KILAUEA_DRAFT` stays unset. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/Discord/` | Agent 21. Present. Do not edit. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/CouncilPersona/` | Agent 03. Present. Do not edit. |
| `/home/rootrecord/old ollama/old skills/kilauea/rr-kilauea/scripts/kilauea.py` | Removed from the old repo and from GitHub `c1ea1dd5`. Scheduler symlink left. |
| `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/kilauea/rr-kilauea/` | Phase 4 archive. Copied 2026-09-30. |
| `5 - RootRecord-Library/Documentation/00-architecture/Old-Repo-Migration-Matrix.md` | Row 3 corrected. Grok still not ported. |
| `5 - RootRecord-Library/Documentation/00-architecture/G1-Scheduler-To-G3-Jobs-Map-2026-09-29.md` | rr-kilauea row names the gated draft job. |
| `5 - RootRecord-Library/Documentation/00-architecture/Voice-Reports-G3.md` | Grok stays blocked. Draft queue named as separate. |
| `5 - RootRecord-Library/Documentation/00-architecture/Geology-Domain-Ownership-Kilauea-Earthquakes-2026-09-28.md` | Public draft queue marked landed. |

---

## 6. Open items

**Additional requirements:**

- `RR_KILAUEA_DRAFT` stays unset. Enabling the job, or any Discord, Slack, or Telegram send, needs a separate sign-off.
- Phase 4 is done. The GitHub repository remains.

---

## 7. Notes & constraints

- No force-push.
- Secrets stay out of git. This function has no key names. Do not print values from `master-key.env`. Do not add a second env file.
- Prefer small reversible steps.
- Sign-off before any send, speaker playback, OBS, hardware switch, deletion of live Ecosystem files, or cloud spend (no Grok). Phase 4 deletion is limited to this function's old files, and only after they are in `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/`. Do not delete the GitHub repository.
- Small test, 2026-09-30 00:56 HST: temp `RR_DATABASE_ROOT` with a copy of `kilauea-last.json`. First run printed `seed` and wrote `publish-last.json` with no queue file. Second run printed `unchanged`. After `status_notice_id` changed, the next run wrote one `*-kilauea-cron.md` (621 characters, header `**Ava kilauea report**`). `strace -e trace=network` showed no connect, send, or socket.
- Result note (2026-09-30 00:56 HST): Landed `Geology/PublicDraftQueue/` (`scripts/queue_draft.py`, package `PublicDraftQueue`, README). Gated job `geology_kilauea_public_draft` is in `jobs.py`. `RR_KILAUEA_DRAFT` stays unset. No send. Archived `kilauea/rr-kilauea/` source plus `scripts/__pycache__` to `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/kilauea/rr-kilauea/`. Removed those tracked files from `/home/rootrecord/old ollama/old skills` and pushed `c1ea1dd5` to `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server` branch `online-safe-20260920`. Left the scheduler symlink, `origin/ns/apps/core/services/kilauea.py`, and `reports/scripts/reports.py`. The GitHub repository was not deleted.

---

*Work order prepared 2026-09-30 HST. Update status when closed.*

---

## Archive / location note

This file is a draft. It is not on the active index. Do not auto-promote.

```text
Documentation/06-development/Work-Orders/drafts/Kilauea_public_draft_queue_Work_Order_WO-MIG-24-2026-09-29.md
```

See `drafts/README.md` and WO-WOGEN-001. Do not auto-promote.

**Closed WOs:** set Status → COMPLETE/CLOSED → `git mv` into:

```text
Documentation/06-development/Work-Orders/Complete/
```

Human session logs archive under `Documentation/01-operations/archive/YYYY-Www/` (WO-ARCH) — separate from closed work orders.
