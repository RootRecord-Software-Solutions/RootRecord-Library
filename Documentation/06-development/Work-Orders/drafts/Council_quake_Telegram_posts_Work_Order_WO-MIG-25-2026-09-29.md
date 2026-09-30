# WORK ORDER — Council quake Telegram posts

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-MIG-25-2026-09-29 |
| **Date** | 2026-09-30 (HST) |
| **Status** | OPEN — draft, not accepted for execution |
| **Owner** | RootRecord |
| **Related** | Agent 25, wave D. Depends on Folder 3, Council persona prompts (`Communications/CouncilPersona`). Later functions that wait on this Folder: 26 Bruce stats posts; 27 Council health alerts. Matrix row 6. |

**Scope:** Read the live Hawaiʻi quake file and prepare Carly’s per-quake Telegram notice (fixed text, optional WAV, at most four new events per tick, first run seeds and sends nothing). Keep `geology_collect.py`, Kokoro, the quiet relay, and the hourly earthquake voice rollup. This draft does not authorize runtime edits, a `jobs.py` change, a Telegram send, a WAV render, speaker playback, a poller restart, or a GitHub deletion.

---

## 1. Intent

Old `council/council-quake/scripts/quake_watch.py` posted each new Hawaiʻi quake at M≥2.0 as Carly. The body was a fixed template (`format_quake` / `spoken_quake`), not an LLM reply. A Carly Nova WAV could ride with the notice. At most four posts per tick. The first run marked the current catalog seen and sent nothing. The same script also pulled a worldwide M≥5 feed. That second fetch is not this function.

Live detection already writes `new_local_m2_ids` and the event list in `2 - RootRecord-Database/Geology/Earthquakes/hawaii-last.json` from `Geology/scripts/geology_collect.py`. That collector stays. Kokoro stays: `Media/Voice/scripts/speakers.py` already maps `earthquake` to Carly. The relay stays quiet (`RR_RELAY_REPLIES=0`). The hourly spoken rollup `voice_reports.py earthquake_report` is a different function and stays.

This function reads that existing quake file and prepares the per-quake Telegram notice. It does not fetch USGS again.

---

## 2. Current reality

### 2.1 What exists

Folder name, used in all three places: `CouncilQuake` (inside Communications). No lowercase twin. No second top-level domain. Geology stays the collector.

| Item | Location / status |
| --- | --- |
| Server code | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/CouncilQuake/scripts` — not created yet. Package name `CouncilQuake`. No `Logs/` directory on the server. |
| Database data | `2 - RootRecord-Database/Communications/CouncilQuake/` — not created yet. Seen ids and last dry-run stamp only. |
| Database logs | `2 - RootRecord-Database/Logs/Communications/CouncilQuake/` — not created yet. One JSON line per tick. |
| Live detection (keep) | `2 - RootRecord-Database/Geology/Earthquakes/hawaii-last.json`, written by `Geology/scripts/geology_collect.py`. Do not replace the collector. |
| Live voice map (keep) | `Media/Voice/scripts/speakers.py` — `earthquake` → Carly (`af_nova`). Do not replace Kokoro. |
| Live hourly rollup (keep) | `Media/Voice/scripts/voice_reports.py earthquake_report`. No delivery. Different function. |
| Live relay (keep) | `Communications/telegram/scripts/council-relay.py`. Quiet unless `RR_RELAY_REPLIES=1`. Chat id key: `COUNCIL_CHAT_ID` in `Communications/telegram/config/relay.conf`. |
| Persona homes (already on disk) | Library `Agent Context/{Ava,Bruce,Carly}-Agent-Context/` (canonical packs, WO-AGENT). Telegram models: `2 - RootRecord-Database/AI/Ollama/Modelfiles/Production/{ava,bruce,carly}-telegram.Modelfile`. Council specialists: `Modelfiles/Specialists/rr-council-{ava,bruce,carly}.Modelfile`. Documented in `AI-Specialist-Models-and-Routing.md` and `Documentation/02-agents/README.md`. This notice does not copy them. |
| Unbuilt copy | `Communications/CouncilPersona/` is agent 03’s planned copy. It is not the persona home. This function does not create it. |
| Old source | `/home/rootrecord/old ollama/old skills/council/council-quake/` — tracked in `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server` |
| `master-key.env` keys | `TELEGRAM_CARLY_TOKEN` only, allowlisted the way `Energy/lib/envload.py` allowlists EcoFlow keys. Never print the value. No second env file. Dry-run does not load the key. |

### 2.2 Completed so far

- [x] Old `quake_watch.py` and `job.py` read. Live `hawaii-last.json`, collector, speakers map, and relay read.
- [x] This draft written. Not on the active work-order index.
- [x] Persona homes confirmed in Library Agent Context and Database Production Modelfiles. `Communications/CouncilPersona` is not required for this notice.
- [x] `CouncilQuake` dry-run script, README, and gated `jobs.py` block added. Send and WAV stay off.
- [ ] Alexander has not accepted this draft for execution.
- [x] Offline `--self-test` passed 2026-09-30: one M2.4 notice, second run zero, no send, live `hawaii-last.json` untouched.
- [x] Phase 4 archive is on disk. Old-repo commit `f05ec568` pushed to `online-safe-20260920`. Shared `notify.py` and `report_cast.py` left in place.
- [x] Phase 5 result note written. Matrix row 6, the scheduler map, and the Geology ownership page corrected.

### 2.3 Known friction

- `new_local_m2_ids` is only the collector’s latest run. A post job that watches that field alone drops events between polls. Candidates are events in `hawaii-last.json` with mag ≥ 2.0, deduped against this function’s own seen list.
- Council chat personas already live in Library `Agent Context/` and in the Production `*-telegram` Modelfiles. `Communications/CouncilPersona` is agent 03’s unbuilt copy, not the home this function waits on. The quake body stays the fixed template and does not call `run-infer`.
- Discord, Slack, and Telegram share a pipe owned across wave D. This function is the Telegram leg only. If a shared Communications send module exists when the build starts, call it. If not, a gated `sendMessage` in `CouncilQuake` is enough. Do not add Discord or Slack.
- Old `quake_watch.py` imports shared files (`council-telegram/scripts/notify.py`, `report_cast.py`, plus speakers and the OBS quake fetch). Those stay in the old repo. Phase 4 removes only `council/council-quake/`.
- If `jobs.py`, `council-relay.py`, or `master-key.env` is already being edited when the build starts, pause and name the file.

---

## 3. Tasks

Do not start these until Alexander accepts this draft and says to build.

1. Persona homes are already on disk (Library Agent Context packs and Production `*-telegram` Modelfiles). Do not build `Communications/CouncilPersona`. Pause if `jobs.py`, `council-relay.py`, or `master-key.env` is already being edited.
2. Add `Communications/CouncilQuake/scripts/quake_posts.py`. Read `hawaii-last.json`. Candidates are events with mag ≥ 2.0. First run seeds the seen list and posts nothing. Later runs post at most 4 new ids. Seen list lives under `2 - RootRecord-Database/Communications/CouncilQuake/`, not on the server.
3. Add `Communications/CouncilQuake/scripts/envload.py` with allowlist `TELEGRAM_CARLY_TOKEN` only. Dry-run does not load it.
4. Add `Communications/CouncilQuake/README.md` naming the Folder and the three paths.
5. Propose one gated block in `jobs.py` only: id `council_quake_telegram`, about every 2 minutes, `enabled` only when `RR_COUNCIL_QUAKE=1`, command is the dry-run script. Default stays off. It is not skipped by night sleep, matching the old job. Do not restart the poller.
6. Send and WAV stay off. `RR_COUNCIL_QUAKE_SEND=1` is the Telegram `sendMessage` gate. `RR_COUNCIL_QUAKE_WAV=1` is the Kokoro render gate, using the existing Carly voice, and still does not play speakers. Both need Alexander’s sign-off. This draft does not turn them on.
7. Run the offline test in Notes. No network, no token, no write to the live `hawaii-last.json`.
8. After that test passes: archive the old `council/council-quake/` tree (source plus the `__pycache__` beside it) under `/home/rootrecord/RootRecord-Ecosystem/Old repos deleted and merged/Solar-Pacific-RootRecord-Server/`, keeping the path each file had inside the old repo. Then delete only those paths from `/home/rootrecord/old ollama/old skills` and from GitHub `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server`. Commit that deletion and push it. Do not force-push. Do not delete the GitHub repository. If the archive copy fails, do not delete.
9. Leave shared files in the old repo: `council/council-telegram/scripts/notify.py`, `council/council-telegram/scripts/report_cast.py`, and anything else this function only imported. Name them in the phase 5 result note.
10. Then add the phase 5 result note to this work order and correct only the Library lines this function made stale: matrix row 6 in `Old-Repo-Migration-Matrix.md`, the `council-quake` line in `G1-Scheduler-To-G3-Jobs-Map-2026-09-29.md`, and the “not ported” council-quake mention in `Geology-Domain-Ownership-Kilauea-Earthquakes-2026-09-28.md`.

---

## 4. Non-goals

- Do not replace `geology_collect.py`, the EcoFlow BLE poller, Hawaiʻi weather, the globe collector, camera grabs, or Kokoro.
- Do not replace `speakers.py`, `voice_reports.py earthquake_report`, or the quiet relay loop.
- Do not build agent 26 (Bruce stats posts) or 27 (Council health alerts).
- Do not build Council persona prompts, the Discord poller, the Slack poller, or the earthquake Discord post.
- Do not post worldwide M≥5, do not call `_fetch_quakes`, and do not attach radar or photos.
- Do not open a second top-level domain. Do not add a `Logs/` directory on the server. Do not add a second env file.
- Do not import logs, samples, last-state files, or other generated runtime output into Pacific, Database source trees beyond this function’s seen store and log line, the website, or git.
- Do not send Telegram, render or play audio, switch hardware, restart the poller, or spend cloud money in this draft.
- Do not edit `jobs.py` until the build is accepted, and then only the one gated block above.

---

## 5. Key file / path reference

| Path | Role |
|------|------|
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/CouncilQuake/scripts` | New code. Package `CouncilQuake`. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/CouncilQuake/scripts/quake_posts.py` | Read `hawaii-last.json`, format the fixed notice, seed, cap at 4. Dry-run by default. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/CouncilQuake/scripts/envload.py` | Allowlist `TELEGRAM_CARLY_TOKEN` only. Never print the value. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/CouncilQuake/README.md` | Folder name and the three paths. |
| `2 - RootRecord-Database/Communications/CouncilQuake/` | Seen ids and last dry-run stamp. |
| `2 - RootRecord-Database/Logs/Communications/CouncilQuake/` | One JSON line per tick. |
| `2 - RootRecord-Database/Geology/Earthquakes/hawaii-last.json` | Existing detection. Read only. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Geology/scripts/geology_collect.py` | Keep. Do not replace. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Media/Voice/scripts/speakers.py` | Keep. Carly voice for a later signed-off WAV. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/telegram/config/relay.conf` | Existing `COUNCIL_CHAT_ID`. Do not add a second chat config. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/telegram/scripts/council-relay.py` | Keep. Pause if it is already being edited. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Automations/scripts/jobs.py` | Build only: one gated `council_quake_telegram` block, default off. |
| `/home/rootrecord/master/master-key.env` | `TELEGRAM_CARLY_TOKEN` only. Do not commit. Do not print. |
| `/home/rootrecord/old ollama/old skills/council/council-quake/` | Old function. Archive, then delete these paths only. |
| `council/council-telegram/scripts/notify.py` | Shared. Leave in the old repo. |
| `council/council-telegram/scripts/report_cast.py` | Shared. Leave in the old repo. |
| `5 - RootRecord-Library/Documentation/00-architecture/Old-Repo-Migration-Matrix.md` | Phase 5 only: correct row 6. |
| `5 - RootRecord-Library/Documentation/00-architecture/G1-Scheduler-To-G3-Jobs-Map-2026-09-29.md` | Phase 5 only: correct the `council-quake` line. |
| `5 - RootRecord-Library/Documentation/00-architecture/Geology-Domain-Ownership-Kilauea-Earthquakes-2026-09-28.md` | Phase 5 only: correct the “not ported” council-quake mention. |

---

## 6. Open items

**Additional requirements:**

- Alexander accepts this draft and says to build before any file outside this draft is written.
- Do not build `Communications/CouncilPersona`. Persona homes are Library `Agent Context/` and the Production `*-telegram` Modelfiles.
- If `jobs.py`, `council-relay.py`, or `master-key.env` is already being edited at build time, pause and name the file.
- `RR_COUNCIL_QUAKE_SEND=1` and `RR_COUNCIL_QUAKE_WAV=1` stay off until a separate sign-off. Enabling the dry-run job is not a send.
- Phase 4 deletes only `council/council-quake/` after the archive copy is on disk. Shared imports stay. If the archive copy fails, do not delete.
- Phase 5 result note is empty until the build and the archive copy exist.

---

## 7. Notes & constraints

- No force-push. Do not delete the GitHub repository `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server`.
- Secrets stay out of git. The plan lists `TELEGRAM_CARLY_TOKEN` by name only. Never print the value. Never add a second env file.
- Prefer small reversible steps.
- Sign-off gate: do not call Telegram `sendMessage` or `sendVoice`, do not set `RR_COUNCIL_QUAKE_SEND=1` or `RR_COUNCIL_QUAKE_WAV=1`, do not render Kokoro, do not play speakers, do not switch hardware, do not restart the poller, and do not spend cloud money. The proposed job runs the dry-run script only, and only when `RR_COUNCIL_QUAKE=1` at the next poller start Alexander chooses.
- Proof test, offline only: a temp copy of one M2.4 event and an empty seen file prints one formatted notice and records the id; a second run prints zero. No network. No token load. No write to the live `hawaii-last.json`.
- Phase 4 archive root: `/home/rootrecord/RootRecord-Ecosystem/Old repos deleted and merged/Solar-Pacific-RootRecord-Server/`. Keep each file’s path from inside the old repo, including `__pycache__` that sat beside the source. Generated data stays in that archive and out of the live Folders. If the archive copy fails, do not delete.
- After phase 4, add a short result note here (what landed, archive path, what was removed on GitHub) and correct only the three Library pages named in section 5.

---

*Work order prepared 2026-09-30 HST. Update status when closed.*

---

## Archive / location note

This file is a draft. It is not on the active index. Do not auto-promote.

```text
Documentation/06-development/Work-Orders/drafts/Council_quake_Telegram_posts_Work_Order_WO-MIG-25-2026-09-29.md
```

See `drafts/README.md` and WO-WOGEN-001. Promotion is Alexander's decision: move into `Documentation/06-development/Work-Orders/`, set Status, and add an index row.

**Closed WOs:** set Status → COMPLETE/CLOSED → `git mv` into `Documentation/06-development/Work-Orders/Complete/`.

Human session logs archive under `Documentation/01-operations/archive/YYYY-Www/` (WO-ARCH) — separate from closed work orders.

### Phase 4 / phase 5 result

Landed 2026-09-30: `Communications/CouncilQuake/scripts/quake_posts.py` reads `hawaii-last.json`, seeds on the live path, and stays dry. Job `council_quake_telegram` is gated `RR_COUNCIL_QUAKE=1` (off) and is on the night-sleep allow list. `--self-test` PASS: one M2.4 notice, second run zero, no Telegram, live quake file untouched.

Archived to `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/council/council-quake/` (source plus `__pycache__`). Removed those tracked paths from `/home/rootrecord/old ollama/old skills` and from GitHub `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server` branch `online-safe-20260920`, commit `f05ec568`. The repository was not deleted. Shared files left in the old repo: `council/council-telegram/scripts/notify.py`, `council/council-telegram/scripts/report_cast.py`.

Library corrections: matrix row 6, the `council-quake` scheduler row, and the Geology ownership “not imported” line. Send and WAV remain off.
