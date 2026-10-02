# Handoff

Read this before changing RootRecord. It is the continuity layer. Conversation history is not.

Checked against the live desk on 2026-09-30. Live numbers move. Re-run `bash verify.sh` from the ecosystem root. Do not treat this file as a watt reading.

## Current mission

Build a canonical machine-readable state of the Pacific desk, with small projections for local models and a later website. Ava, Bruce, and Carly may inspect. They may not restart, send, push, or build. A human build goes through an interaction request and stays short of Cursor until the `cursor_api` gate is opened.

Library is knowledge. Pacific is the executable runtime. Database is where bytes go. Ecosystem is the umbrella checkout. A git commit is not a deploy.

## Current architecture

```text
sources (jobs, energy files, processes, relay config, docs)
        │
        ▼
state-aggregate.py          desk-live.py
        │                         │
        ▼                         ▼
rootrecord-state.json       desk-live.txt
        │
        ├── projections/agent/{ava,bruce,carly}.json
        ├── projections/public.json          (empty of telemetry on purpose)
        └── projections/slices.json          (what a 3B model is allowed to see)
```

Council chat uses the NPU, on demand, `llama3.2:3b`, context 4096. One Telegram long-poll (`council-relay.py`, Ava's token). Sandbox replies are on. The live council and private DMs are quiet.

Generated files live in `2 - RootRecord-Database/System/status/`. That directory is on the GitHub sync skip list. Do not copy the snapshot into git.

## Working

- Sandbox chat answers. Read receipt is eyes, then inference, then typing, then text.
- Desk readings (Delta 2, River 2 Pro, host CPU/memory/load) refresh before a reply.
- State snapshot refreshes on the same path. Scope questions get the short slice, including configuration drift.
- Pack freshness is `observed`, `stale`, or `dead`. Dead means not transmitting. It is not a collector crash.
- NPU device is the council accelerator. FLM idle between replies is normal.
- Cloudflare tunnel process is part of the poller stack.
- GitHub sync is a poller job, not a resident daemon.
- Mainland One is radio only. `ssh ml1` and `ssh rr-aws` use `ml1.rootrecord.cloud` through cloudflared. Direct fallback `rr-aws-ip` is `3.140.195.32`. Mainland Two is tunnel + github-ops scaffolding only — **not** a YouTube station; polling later, not live. `ssh ml2` uses `ml2.rootrecord.cloud`. Direct fallback `ml2-ip` is `3.149.238.83`. `api.rootrecord.cloud` → ML2 `:8091` is route only. `ssh.rootrecord.cloud` is retired. `www` stays on Vercel. The listener stream is `https://radio.rootrecord.cloud/radio/live.mp3` and the Opus music bed is on the host. The Mainland One checkout is the radio tree at `9b7fccf`. Guides: `Documentation/01-Operations/2026-10-01-radio-station.md`, `Documentation/15-Domains-and-External-Systems/US-Mainland-Two.md`, `Documentation/01-Operations/2026-10-01-mainland-rename-and-ssh-tunnels.md`. Do not restart cloudflared over `ssh ml1`.

## Broken

Nothing in the 2026-09-30 verify set is a confirmed failure. Run verify before believing that. `health_unknown` is not broken. An empty incident list is not an all-clear: no incident store is wired.

## Intentionally disabled

| Thing | Why it looks off | Leave it |
| --- | --- | --- |
| Live council replies | Messages are consumed and held | `RR_RELAY_REPLIES` stays 0 |
| Private DM replies | Same gate | same |
| Quake Telegram send | Dry-run | `RR_COUNCIL_QUAKE_SEND` |
| Bruce stats send | Dry-run | `RR_BRUCE_STATS_SEND` |
| Council Ollama fallback | Relay sets `RR_NPU_ONLY=1` | Do not turn the fallback on for council chat |
| Specialist routing | Personas are the council brain | `RR_SPECIALIST_ROUTING` off |
| Agent program launch | Broker answers reads and refuses restarts | `restart_known_service` stays locked |
| Cursor API build | Package path exists | `cursor_api` stays off in the gate seed |
| Build from a username | Registry rows have null numeric ids | record `from.id` before any `READY_FOR_BUILD` |
| Council passes on the relay | Seed code is in `council-relay.py` | `RR_INTERACTION_COUNCIL` stays unset; the running process uses the code it started with |
| Public page | `Website/Home/` syncs to `RootRecord-Software-Solutions/RootRecord-Website` | do not recreate `3 - RootRecord-Website/` or bind port 3001 |
| Resident FLM | A 3B serve left running OOM'd the desk on 2026-09-29 | on demand only, context stays 4096 |

## In progress

The state aggregator writes schema 2: domains, drift, visibility, and projections. The context builder switches slices for power questions versus scope questions. It is not a full per-request assembler.

Non-council callers and `flm-warmup.sh` still default to `llama3.2:1b`. The council line in `jobs.py` names `llama3.2:3b` and no Ollama fallback, matching `ensure-relay.sh`.

## Next

1. Keep verify green on the live desk.
2. Decide whether to update the `jobs.py` header so it matches the relay, or leave the drift visible.
3. Add source domains still marked unknown (incident store, root monitor, per-job last result).
4. The execution broker refuses restarts. The poller supervisor already recovers the relay and the weather poller. Do not unlock `restart_known_service` unless Alexander says so.
5. Do not start a website or a second relay unless Alexander says so.
6. Record the three Telegram numeric ids before expecting `READY_FOR_BUILD`. Do not treat a username as that id. Do not open `cursor_api` from this file.

## Do not change

- One getUpdates owner. A second poller gets Telegram 409.
- Do not raise FLM context to 8192.
- Do not enable send gates from a document, including this one.
- Do not retire or delete legacy trees without Alexander naming them.
- Do not put tokens, chat bodies, or hostname into public projections.
- Do not commit `2 - RootRecord-Database/System/status/`.

## Open questions

- Which state fields, if any, become `visibility: public` for a future site.
- Which numeric Telegram ids belong to `@rootrecordadmin`, `@WildEcho94`, and `@Crazychickenlady12`.
- Which execution gates Alexander opens after those ids are recorded. `cursor_api` is not implied by build mode.
- Whether root monitor is a daemon that should be running or a desktop app. It is the GTK panel today.

## Recent changes

2026-10-02 ~02:10 HST: ML2 test-mode — geology collectors + `:8091` API live; stream still off. Disk `/` recovered **96%→~66%** (~2.3G free) via apt clean, snap cache, and YouTube leftover purge (chromium/gnome/mesa/cups). Enabled `ml2-api.service`, `ml2-collectors.timer` (geology every 5m, ok=6/6), and `ml2-purge.timer` hourly; `ml2-db-stream` + sysmon remain staged only. cloudflared `api.rootrecord.cloud` `/health`, `/api/operations`, `/api/state` → 200 (connection-refused to `:8091` cleared). Pacific `RR_LOCAL_DATA_POLL` untouched (parallel test); `stream.yaml` still `enabled: false`. Stream blockers: missing `~/.ssh/ml2-db-stream`, pacific-db SSH/Access, Pacific `home_receiver` + forced-command key; handoffs purge hourly until stream acks; `/api/operations` needs Pacific→ML2 refresh or desk re-seed. Desk SHA `84c4a37` (US-Mainland-Two); host SHA `3274fb3` (rsync deploy, no push). Toggle: host `docs/TOGGLE.md` test-mode §. Supersedes the ~01:58 disk-96% / dead-API live check. See `Documentation/15-Domains-and-External-Systems/US-Mainland-Two.md`.

2026-10-02 ~02:09 HST: Alexander rule — no sports in reports. Sports was entering `news_update` via RadioRss general feeds (Star-Advertiser / Al Jazeera / BBC sports URLs, NFL, etc.). Pacific `Media/RadioRss` now drops sports from every feed (`policy.yaml` `sports_patterns`; `stories.sports` on normalize; compose skip; `news_hour` filter before desks). `test_rss_radio.py` sports-drop / transportation-keep passed. Voice desks, Discord report channels, and Website report pages had no dedicated sports sections. See `Documentation/01-Operations/2026-09-30-voice-desk.md`, `Documentation/10-AI-and-Agent-Runtime/Voice-Reports-G3.md`, and `Documentation/01-Operations/2026-10-01-radio-station.md`.

2026-10-02 ~01:57 HST: Nine generating voice desks and the stack-closer cycle moved from `:12` / `:42` to `:22` / `:52` in `jobs.py` `only_at_minutes` and `status_cue.cycle_key` (nine desks after the earlier `energy_report` fold; news stays `:36`; tests `test_status_stack.py` / `test_voice_timing_report.py` updated). Lead to playlist lock is now **7m59s** (`:22`→`:29:59`, `:52`→`:59:59`); historical ten-desk p90 (~15m) no longer fits that window. Poller must be restarted to adopt the new minutes (not done in this doc pass). See `Documentation/01-Operations/2026-09-30-voice-desk.md` and `Documentation/10-AI-and-Agent-Runtime/Voice-Reports-G3.md`.

2026-10-02 ~01:56–01:58 HST: Alexander read-only Mainland check. ML1 air healthy (`rr-radio-station` since 01:39 after one clean restart; `live.mp3` 200; encoding + watchdog `watch_ok`; light `ffmpeg`/`stream.js`; disk 67%; cloudflared active with listener EOF churn); noisiest ML1 issue is dirty `status-api/stream.js` blocking `aws-git-pull` (behind origin by 6; deploy path left alone so live mixer not replaced; also failed `aws-readme-status`). ML2 idle post–YouTube wipe; disk `/` at **96%** (314M free) from snapd (~1.7G) + apt (~546M) caches, not app data; tunnel still aims API at dead `:8091` → connection refused spam; no failed units. Desk sysmon empty on both (staging only). No host config, restart, disk clean, or git fix. See `Documentation/15-Domains-and-External-Systems/US-Mainland-One.md`, `Documentation/15-Domains-and-External-Systems/US-Mainland-Two.md`, and `Documentation/01-Operations/2026-10-01-radio-station.md`.

2026-10-02 ~01:45 HST: Mainland desk sync direction fixed. Root cause of DUCK regression: `push-repo-once.sh` mirror mode rsynced Servers → worktree (`e101f21`). For `id=mainland` only, sync now starts worktree → Servers (never Servers → worktree); other mirrors unchanged. Docs: `US-Mainland-One.md` canonical-git row, `Repository-Ownership-Model.md`, ecosystem `.gitignore` note. Commits pacific `40e175e`, library `9a50ef4`, ecosystem `0e60ea7f` (not pushed by Mainland). DUCK verified `0.1` on desk+host active; host aws-git-pull left alone (dirty/behind). See `Documentation/15-Domains-and-External-Systems/US-Mainland-One.md`.

2026-10-02 ~01:41 HST: Separate `energy_report` voice job retired into Bruce’s combined `solar_desk` (title “Energy and solar”: packs, sun times, newest ch1 still, hour’s camera look). Removed from `jobs.py`, `run-poller.sh` (`RR_VOICE_ENERGY`), `status_cue.TYPES` (nine desks; stack closer waits on nine Mainland receipts), `voice_deliver`, Discord `public_report` / `report-channels.json`, `publish_report_pages` Energy area, and `voice_timing_report` STACK; `b_energy_report` stays a one-release alias. Lexicon: Maui `mao wee`, Honolulu plain name; `news_hour` folds places before render. Leapfrog EcoFlow read falls back to the other pack on failure and rewrites `desk-live.py`. See `Documentation/01-Operations/2026-09-30-voice-desk.md`, `Documentation/10-AI-and-Agent-Runtime/Voice-Reports-G3.md`, and `Documentation/01-Operations/2026-10-01-ecoflow-ble-reads.md`.

2026-10-02 ~01:38 HST: Live ML1 mixer bed duck corrected back to `0.1` (10%). Desk auto-sync `e101f21` had restored `DUCK = 0.25` after `1020933`; re-applied on desk ML1 + mainland worktree `status-api/stream.js`, live host active release + checkout, and `rr-radio-station` restarted (Mainland). Local commit `1a4c1bb`. See `Documentation/01-Operations/2026-10-01-radio-station.md`.

2026-10-02 ~01:28–01:30 HST: Verification found staged ML1 and ML2 collect → primary SSH NDJSON → Pacific receiver → Database → acknowledgement purge paths in Mainland commits `16645da` and `7065795`, with Telegram datapack fallback and Pacific pickup documented in `System/docs/MAINLAND-SYSMON-INTAKE.md` and `Communications/telegram/docs/DATAPACK-PICKUP.md`; the Database scaffold is `65dea848` (`System/metrics/{ml1,ml2}/`, `Network/datapacks/{inbox,processed,state}/`, and reserved ML1/ML2 log/intake areas). Both `config/sysmon-stream.yaml` files are `enabled: false`, all four Mainland sysmon units are staged but not installed, and the Pacific receiver/pickup units are likewise not installed. This is design/staging only: EcoFlow/Energy remains denied and Pacific-only, and no push, sync, publish, or live cutover was made.

2026-10-02 ~01:29 HST: Report talkover bed duck on ML1 mixer set from `0.25` (~25%) to `0.1` (10%) in `status-api/stream.js` (mainland worktree `1020933`). Library pages updated (`f526741` on library worktree; Ecosystem copies brought current). Desk auto-sync later restored `0.25` briefly; live correction at ~01:38 HST (`1a4c1bb`). See `Documentation/01-Operations/2026-10-01-radio-station.md`.

2026-10-02 ~01:24 HST: Public `/radio` and `/live` audio: after first Listen unlock, auto-resume and cache-bust reconnect on stall/pause/waiting/ended/error/offline→online/visibility (no TAP LISTEN on stream drop). 15-minute public limit and `/pro/radio` membership wall are future only. Website worktree `cdd9f0c`; Library note `fc06d15`; ML1 mixer untouched. Pacific `Website/Home/assets/radio.js` may still lag the website worktree until sync. See `Documentation/01-Operations/2026-10-01-radio-station.md`.

2026-10-02 ~01:20 HST: Mainland Two desk verification found staged collector modules for geology, weather, Kīlauea cams, and radio RSS plus clean SSH NDJSON handoff and hourly purge scaffolding in commits `737b583` and `abd4bd0`; `config/stream.yaml` remains `enabled: false`, the collector/stream/purge units are not installed, and Pacific remains the only long-term data bank. Raw ML2 pulls are ephemeral (`var/raw/` → process → `var/handoff/` → stream → delete on acknowledgement), API-circulated metrics stay in the local overwrite cache, and `config/stream_deny.yaml` excludes EcoFlow/Energy. The proposed Pacific `RR_LOCAL_DATA_POLL=0` / `data_poll_mode.yaml: mode: remote` kill switch is design-only; no Pacific cutover was made. The earlier YouTube wipe remains `04142d5` (host `6c5070d`), with tunnel `bd8e68a4-8a97-4b20-afd9-b058473a0a22` and `api.rootrecord.cloud` still route-only. See `Documentation/15-Domains-and-External-Systems/US-Mainland-Two.md`.

2026-10-02 ~01:19 HST: Alexander (via Master) set a fleet rule: whenever any agent finishes work that produced changes, they automatically send Wren a change summary for Library documentation. Recorded in Documenter `WORKFLOW.md` / `ROLE-AND-BOUNDS.md` and `Documentation/02-Agents/README.md`. Ecosystem stays local-desk only.

2026-10-02 ~01:07 HST: After every successful Mainland receipt, `status_cue.note_sent` tracks the ten :12/:42 desks in Database `Reports/Voice/stack-send.json`. When the set is complete for that cycle, Ava plays local closer `Clips/Ava/stack_all_sent.wav` once (“All reports have been sent successfully. Heavy work may resume.”); still desk-only, gated by `RR_VOICE_STATUS`. `voice_timing_report` rewrote `voice-timing.md` (303 runs; ten-desk median 376s / avg 459s / p90 889s). See `Documentation/01-Operations/2026-09-30-voice-desk.md` and `Documentation/10-AI-and-Agent-Runtime/Voice-Reports-G3.md`.

2026-10-02 ~00:50 HST: Alexander confirmed the voice operator copy (HST). Station locks at HH:29:59 / HH:59:59; ten desks at :12/:42 (median 376s / p90 891s from voice-timing.md 292 runs, 17m59s lead). News :36; hurricane five :40 slots; chime :00/:30 file replay. Roll-ups 09:02/12:02/21:02/late-final 23:02 first air next half hour. Generation clock (not air slot); `compare_span` percent lines; four desk status clips (`RR_VOICE_STATUS`); staged on-air cues with `notify.opus` then spoken line (mixer `stage-notice`). Nothing committed in that pass. See `Documentation/01-Operations/2026-09-30-voice-desk.md` and `voice-timing.md`.

2026-10-02 ~00:51 HST: Cove applied Alexander’s primary nav and sitewide footer on `Website/Home/` (39 pages plus `publish_report_pages.py` chrome). Current page is a span, not a link. Library `SITE.md`, Home README, and `Documentation/05-Public-Surface/README.md` already matched the lists; this note records the live page apply.

2026-10-02 ~00:49 HST: Alexander set public primary nav to Home, Products, Services, Solutions, About, Security, Status, Reports, Radio, Live (omit self-link). Footer sitewide: Account, Terms, Privacy, Data deletion. Report pages use the same primary; Ecosystem/Systems/Intelligence/Knowledge off primary. Cove applies in `Website/Home/`. Recorded in Web `CONTEXT/SITE.md`, Home README, and `Documentation/05-Public-Surface/README.md`.

2026-10-02 ~00:39 HST: Voice desks speak generation-clock stamps (not snapped :00/:30). Measured numbers may add percent-change lines vs yesterday / last week / last month (`Media/Voice/scripts/compare_span.py`, ledger Database `Reports/Comparisons/metrics.jsonl`; wired from `voice_reports.py` and `system_perf.py`). Staged on-air cues (`status_cue` staged_hour/staged_half via `radio_push.stage_on_air`) play the short notification sound first; the full spoken clock chime does not. `system_perf.py` docstring still says :06 while jobs stay `[12, 42]`. See `Documentation/01-Operations/2026-09-30-voice-desk.md` and `Documentation/10-AI-and-Agent-Runtime/Voice-Reports-G3.md`.

2026-10-02 ~00:29 HST: Mainland Two YouTube / rr-streaming experiment wiped (Mainland, desk+host). Station scrapped; Alexander owns any future process. Backup `/home/rootrecord/Downloads/ml2-youtube-backup-20261002.tar.gz` (31M, twin stamped). Kept: cloudflared tunnel `bd8e68a4-8a97-4b20-afd9-b058473a0a22`, github-ops pull scaffolding (timer not installed on host), SSH. Local commits ahead of origin (not pushed from wipe seat): desk `04142d5`, host `6c5070d`. See `Documentation/15-Domains-and-External-Systems/US-Mainland-Two.md`.

2026-10-02 00:20 HST: Master enhanced Root Monitor (desk-local; no commit/push/restart from that seat). `Apps/Control-Panel/rr_control_panel.py` — CRITICAL/LOW/STALE on battery header + Energy banner, Energy refresh stamp; `rr_aws_page.py` — clearer WRITE vs DRY-RUN and Status-first guidance; Settings help for editable `aws_fallback_mode`/`alias` and full `start_page` sidebar ids; `Lib/rr_migration.json` as_of 2026-10-02 00:20 HST with 6 BLOCKED / 8 VERIFY PENDING and updated energy-actions note; README + Operators Handbook aligned. Safety: risky_actions still off. Needs Alexander: restart Root Monitor for GTK; B2 ~1% check; migration closes remain his. See `Guides & Tutorials/Root-Monitor-Operators-Handbook/Root-Monitor-Operators-Handbook.md`.

2026-10-02 00:12 HST: Wren verified the Report Instructor desk map against live `jobs.py` and `run-poller.sh` (poller up since 00:09 HST). Voice :12/:42 desks, roll-ups, late-final, hurricane, news :36, Telegram deliver, and radio push are armed. Hourly chime, ai_processing, ai_usage, template_reports, and several others stay gated. Code corrections vs older ops lists: roll-ups/hurricane/late-final are on (not off); `RR_TELEGRAM_DEST` default is `council`; `system_perf`/`current_report` docstring minutes disagree with jobs `[12,42]`; `current_report` missing from `report-channels.json`; CloudNarrative README jobs id absent; template/ai_processing headers name different out paths than live `OUT_DIR`. See `Documentation/01-Operations/2026-09-30-voice-desk.md` and `Documentation/10-AI-and-Agent-Runtime/Voice-Reports-G3.md`.

2026-10-02 00:29 HST: Cove is the web seat. Pack: `Agent Context/Web-Agent-Context/`. The public page is Pacific `Website/Home/`, published by Vercel. `api.rootrecord.cloud` is aimed at Mainland Two and the process is not running, so a missing reading stays missing. The paste is `PROMPT.md` in that pack.

2026-10-02 00:10 HST: Ten desks each have four local status clips: about to generate, in transit, failed to send, and sent. The sent line plays only after Mainland One has the file. A skipped send does not play the failure line. The chime stays a file replay. `RR_VOICE_STATUS=0` keeps the clips quiet. The poller has been up since 00:09 HST. See `Documentation/01-Operations/2026-09-30-voice-desk.md`.

2026-10-01 23:48 HST: Voice desks render at `:12` and `:42`, before the station locks the playlist at `:29:59` and `:59:59`. Across 299 runs a full set is typically 6 to 8 minutes, and a slow energy camera look can reach about 15. News is `:36`. Hurricane is `:40`. Roll-ups stay at 09:02, 12:02, and 21:02 and first play on the following half hour. The poller has been up since 23:46 HST. The averages are on `Documentation/01-Operations/2026-09-30-voice-desk.md`.

2026-10-01 23:28 HST: Wren's Grok bot paste is `Agent Context/Documenter-Agent-Context/PROMPT.md`.

2026-10-01 23:26 HST: The documentation seat is named Wren. Pack: `Agent Context/Documenter-Agent-Context/`. Wren writes current facts into existing pages, is not a council hop, and is not a Telegram or Discord voice. The master prompt section is `0 - Master-Prompt/MASTER-PROMPT.md` §5a.

2026-10-01 23:20 HST: A pack whose last reading is 5 percent or less, and is older than 30 minutes, is discharged and powered off. Voice, the desk file, the state slice, and the public power page say that. They do not keep announcing watts or "reporting." See `Documentation/01-Operations/2026-10-01-ecoflow-ble-reads.md`.

2026-10-01 23:11 HST: EcoFlow reads stay on Bluetooth. A miss keeps the last BLE file for 3 minutes and does not publish quota. If both watt files are at least 3 minutes old, the leapfrog read power-cycles `hci0` once. The repeating read is user timer `rr-ecoflow-read.timer`. Poller job `ecoflow_read_cycle` stays off. See `Documentation/01-Operations/2026-10-01-ecoflow-ble-reads.md`.

2026-09-30 evening: voice desk brought current. Sandbox delivery is on for the armed reports. Host temperature is Celsius. Hawaii is the English word. Energy includes the hourly channel 1 look, generator and transfer watts, and "out of range" after 30 minutes. Twenty-four chime files exist; the chime job stays off. See `Documentation/01-Operations/2026-09-30-voice-desk.md`.

2026-09-30 afternoon: interaction modes, principal registry, sandbox request seed, council draft loop, Cursor handoff package, execution and verification report schemas, broker denial of `development.execute_work_order`, BLOCKED recovery drafts, Root Monitor execution gates. `cursor_api` and `restart_known_service` stay locked. See `Documentation/02-Agents/INTERACTION-MODES.md` and Decision 0006.

2026-09-30: sandbox replies, per-voice NPU personas, desk file, read receipt, state aggregator, drift line, agent/public/slice projections, this handoff, contracts, and `verify.sh`.

## Verification

From the ecosystem root, on the live desk:

```bash
bash verify.sh
```

`[PASS]` is measured or the source file says what we expect. `[WARN]` is intentional or unknown. `[FAIL]` means stop and look. A machine that is not running the poller skips process checks with a warning. That is not a failure of the clone.

## Where the rest of the memory lives

| Need | File |
| --- | --- |
| How a Telegram request becomes work | `5 - RootRecord-Library/Documentation/02-Agents/INTERACTION-MODES.md` |
| How the layers connect | `5 - RootRecord-Library/Documentation/12-Pacific-Server-Current-Architecture/SYSTEM-MAP.md` |
| Why a gate exists | `5 - RootRecord-Library/Documentation/00-Architecture/Decisions/` |
| Relay promise | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/telegram/CONTRACT.md` |
| State promise | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/System/CONTRACT.md` |
| Fact envelope | `5 - RootRecord-Library/Documentation/00-Architecture/Schemas/state-envelope.md` |
| Personas and bounds | `5 - RootRecord-Library/Agent Context/` |
| Wren, documentation seat | `5 - RootRecord-Library/Agent Context/Documenter-Agent-Context/` |
| Cove, public page | `5 - RootRecord-Library/Agent Context/Web-Agent-Context/` |
| Operator decisions still open | `5 - RootRecord-Library/Documentation/01-Operations/2026-09-30-whats-left-for-alexander.md` |
| Voice desk, current | `5 - RootRecord-Library/Documentation/01-Operations/2026-09-30-voice-desk.md` |
| EcoFlow BLE reads, current | `5 - RootRecord-Library/Documentation/01-Operations/2026-10-01-ecoflow-ble-reads.md` |
| Migration counts | `5 - RootRecord-Library/Documentation/13-Migration-and-Legacy-Recovery/Old-Repo-Migration-Matrix.md` |
