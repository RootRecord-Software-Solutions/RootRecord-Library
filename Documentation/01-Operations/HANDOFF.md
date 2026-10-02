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

- **Verified — River AC recovery ~03:48 HST:** the persistent 24/7 `rr-river2pro-ac-recover.timer` has `OnBootSec=45`, `Persistent=true`, and runs with `rootrecord` linger enabled. While AC is off, fresh SOC≥5% (≤5 min) **or** `ac_input_power`≥50W, whichever arrives first, triggers recovery; AC already on is a no-op. Master owns the EcoFlow/BLE path; ML stays clear.

- Sandbox chat answers. Read receipt is eyes, then inference, then typing, then text.
- Desk readings (Delta 2, River 2 Pro, host CPU/memory/load) refresh before a reply.
- State snapshot refreshes on the same path. Scope questions get the short slice, including configuration drift.
- Pack freshness is `observed`, `stale`, or `dead`. Dead means not transmitting. It is not a collector crash.
- NPU device is the council accelerator. FLM idle between replies is normal.
- Cloudflare tunnel process is part of the poller stack.
- GitHub sync is a poller job, not a resident daemon.
- Mainland One is radio only. `ssh ml1` and `ssh rr-aws` use `ml1.rootrecord.cloud` through cloudflared. Direct fallback `rr-aws-ip` is `3.140.195.32`. Mainland Two is tunnel + github-ops scaffolding, with **LIVE** geology + geology_kilauea_cams (USGS still intake only; no vision) + weather_us_states + weather_hawaii + radio_rss (hurricanes via weather_hawaii), local API + analytics, and **verified** Pacific DB stream (SSH → same Database path_rel LLMs read; Telegram datapack fallback) — **not** a YouTube station; ML2 data offload live with Pacific `RR_LOCAL_DATA_POLL=0`; toggle-not-replacement; globe `/api/state` arcs from Pacific LAN rebroadcast (`rr-ml2-globe-state-push`). Discord poller blocked on token; Telegram council-relay stays Pacific. `ssh ml2` uses `ml2.rootrecord.cloud`. Direct fallback `ml2-ip` is `3.149.238.83`. `api.rootrecord.cloud` → ML2 `:8091` is live (API/analytics). `ssh.rootrecord.cloud` is retired. `www` stays on Vercel. The listener stream is `https://radio.rootrecord.cloud/radio/live.mp3` and the Opus music bed is on the host. The Mainland One checkout is the radio tree at `9b7fccf`. Guides: `Documentation/01-Operations/2026-10-01-radio-station.md`, `Documentation/15-Domains-and-External-Systems/US-Mainland-Two.md`, `Documentation/01-Operations/2026-10-01-mainland-rename-and-ssh-tunnels.md`. Do not restart cloudflared over `ssh ml1`.

- **Alexander overnight asks (~03:21; status ~03:23 HST):** (1) **Receive / Telegram fallback — landed** (Mainland): SSH primary stream into Pacific Database path_rel; Telegram datapack fallback + `OFFLINE-TELEGRAM-BUFFER.md` (`08f6e05`); Pacific datapack-pickup allowlist expanded + `ml2_datapack_pickup` (timer+boot). (2) **Labels — partially landed** via clearer systemd Descriptions (`08f6e05`); AWS toggles / data-poll GTK label polish still open (coordinate with Master kill-switch labels). (3) **SSH→Database LLM-readable — landed**: stream writes same `path_rel` tree desks/LLMs already read; Pacific sole LLM-readable bank. **Still open:** Discord poller blocked on token; Discord/Telegram *poller* scaffolds not live (council-relay stays Pacific).

- **Verified ~03:31 HST:** First `*_current` bank is live. ML2 `geology_kilauea_cams` takes USGS stills only (no vision), is enabled under exclusive `RR_LOCAL_DATA_POLL=0` and remains in `LOCAL_DATA_POLL_JOBS` as a soft toggle, streams the handoff to Pacific, and wipes scratch after stream. Pacific `rr_db_stream_receive` archives any replaced filename containing `_current` as `archive/YYYYMMDD/<stem>_<HHMMSS><ext>`; live `_current` remains newest for LLM reads. EcoFlow stays Pacific forever. See Ideas kilauea-checker, US-Mainland-Two, voice-desk.

- **Verified ~03:33 HST:** Report Instructor confirmed the Kīlauea report blend: spoken/written output states whether a still was viewed (Y/N) and, when viewed, what conditions looked like. Bank paths, archive-on-replace, Pacific-only looking, and report blend are verified.

- **Working — RI next lane:** News freshness/rotate for RadioRss and the news hour, using the ML2-streamed bank while Pacific local polling is gated.
- **Measured PASS — post-reboot ~03:41 HST:** `RR_LOCAL_DATA_POLL=0`; intent `remote`; poller up; `:8799` HTTP 200; tunnels `rr-aws-fetch-tunnel` + `rr-ml2-db-tunnel` up; Internet OK. River B1 is ~29% and AC-on; Delta B2 is ~1% and dead. **ATTENTION / Working OPEN:** Mainland `radio_rss` and handoff drain still need verification; do not clear reboot Working until both are verified. If ML2 dies, use the temporary Pacific poller soft flip `RR_LOCAL_DATA_POLL=1`. News rotate stays RI.
- **Working — Alexander ~03:40–03:43 HST:** Overnight `overnight-station-check-till-7am` runs on cron `7,37 3-7`; ML1/ML2 rounds continue through about **06:40 HST** and self-clear after 07:00. A second station-check window is **10:00–12:00 HST**: Mainland arms ML1/ML2 at **:13/:43** from **10:13–11:43 HST**, then self-clears. AC-on if River dies remains a Master/EcoFlow decision.
- **Verified — Report Instructor ~03:42 HST:** Big Island weather map/report path is **live/verified** with **Mountain View, Volcano, and Kailua-Kona**. Formal change summary: `Media/Voice/scripts/voice_reports.py` (`zfp_temps`), `Weather/config/resources.yaml` (NDFD points), `Weather/reports/generator.py` (RWR Kona→Kailua-Kona PHKO), `Weather/config/report_counties.yaml`, and `Media/Voice/scripts/hawaiian_lexicon.py`. Smoke: `b_nws_weather` and `current_report` include all three; previously noted gaps are unchanged.
- **Verified — desk drift ~03:43 HST:** `zfp_temps` bands — Hilo shore, Mountain View range, Volcano elev; Honolulu/Lihue/Kahului/Kailua-Kona shore. See voice-desk.
- **Working — Mainland ~03:41 HST:** **PASS:** `ml2-db-stream` last OK **03:22** (**28 ACKed**); `RR_LOCAL_DATA_POLL=0`; reverse tunnel since **03:36**; weather bank fresh ~03:35–03:38. **ATTENTION / Working OPEN:** `radio_rss` ImportError (`cannot import name fetch_url from fetch`; `ml2-collectors` stuck activating); handoff queue ~656 files / 13 MB; cams `*_current` last **03:30 pre-reboot**; radio bank last **03:22**. Do not clear reboot Working until `radio_rss` + handoff drain verify. Overnight rounds continue through ~06:40 HST; the second 10:00–12:00 HST station-check window arms ML1/ML2 at :13/:43 through 11:43, then self-clears.

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

2026-10-02 ~03:48 HST: Master verified River 2 Pro AC auto-recover **LIVE** on desk: `rr-river2pro-ac-recover.timer` is persistent 24/7 with `OnBootSec=45` and `Persistent=true`; `rootrecord` linger is enabled (`linger=yes`). While AC is off, fresh SOC≥5% (≤5 min) **or** `ac_input_power`≥50W, whichever arrives first, calls `river2pro-ac-on.sh` with a 120-second cooldown. Verified at ~27.7% SOC, 0 W input, and AC on: no-op. Master owns the EcoFlow/BLE path; ML stays clear. Overnight, 10:00–12:00, and noon-final station routines remain armed. No commit/push.

2026-10-02 ~03:43 HST: Alexander → Wren — second station-check window is **10:00–12:00 HST**; Mainland arms ML1/ML2 at **:13/:43** from **10:13–11:43 HST**, then self-clears. Overnight rounds still run through ~06:40 HST. AC-on if River dies remains Master/EcoFlow. No commit/push.

2026-10-02 ~03:41 HST: Master + Mainland → Wren — measured post-reboot **PASS**: `RR_LOCAL_DATA_POLL=0`, intent `remote`, poller up, `:8799` HTTP 200; `rr-aws-fetch-tunnel` + `rr-ml2-db-tunnel` up; Internet OK; River B1 ~29% AC-on; Delta B2 ~1% dead. Mainland stream/bank **PASS**: `ml2-db-stream` last OK 03:22 (28 ACKed), reverse tunnel since 03:36, weather bank ~03:35–03:38. **ATTENTION / Working OPEN:** `radio_rss` ImportError (`cannot import name fetch_url from fetch`; `ml2-collectors` stuck activating), handoff queue ~656 files / 13 MB, cams `*_current` last 03:30 pre-reboot, radio bank last 03:22. Do not clear reboot Working until `radio_rss` + drain verify. Temporary Pacific poller if ML2 dies is soft flip `RR_LOCAL_DATA_POLL=1`. Overnight routine is cron `7,37 3-7` through 07:00 HST. No commit/push.

2026-10-02 ~03:43 HST: Wren desk drift — verified live `zfp_temps` bands after RI Big Island town promotion: Hilo shore, Mountain View range, Volcano elev (~4000 ft); other report towns shore. NDFD points and lexicon match. Folded into voice-desk + Voice-Reports-G3. No commit/push.

2026-10-02 ~03:42 HST: Report Instructor → Wren — Big Island weather sites promoted to **live/verified**: Mountain View, Volcano, and Kailua-Kona. Formal change paths: `Media/Voice/scripts/voice_reports.py` (`zfp_temps`), `Weather/config/resources.yaml` (NDFD points), `Weather/reports/generator.py` (RWR Kona→Kailua-Kona PHKO), `Weather/config/report_counties.yaml`, and `Media/Voice/scripts/hawaiian_lexicon.py`. Smoke: `b_nws_weather` / `current_report` include all three; previously noted gaps unchanged. No commit/push.

2026-10-02 ~03:40 HST: Alexander → Wren — overnight watch through 07:00 HST: Master owns 30-minute station checks; river/AC/temporary-Pacific-poller contingency applies. Report Instructor was wiring Mountain View, Volcano, and Kailua-Kona into Big Island weather reports (WIP at ~03:40 HST; superseded ~03:42 HST by live/verified promotion). Mainland self-checks ML1 radio plus ML2 collectors/stream every 30 minutes through ~06:40 HST; posts only off/all-clear, with the exclusive gate and Master coordination when the link returns. Alexander said solar reboot **done ~03:37 HST**; **superseded ~03:41 HST by measured post-reboot PASS, with `radio_rss` and handoff-drain ATTENTION still open**. No commit/push.

2026-10-02 ~03:31 HST: Mainland verified the first `*_current` bank. ML2 `geology_kilauea_cams` takes USGS stills only (no vision), runs under exclusive `RR_LOCAL_DATA_POLL=0`, streams to Pacific, and wipes scratch after stream. Live paths: `Geology/Volcanoes/Cams/v1cam_current.jpg`, `v2cam_current.jpg`, `v3cam_current.jpg`, and `cams_current.json` (`photo_viewed` plus per-camera `fetched_at`/`bytes`/`sha`/`ok`/`error`). Pacific archive-on-replace is verified for any filename containing `_current`; example `Geology/Volcanoes/Cams/archive/20261002/v3cam_current_033046.jpg`; `kilauea_look` prefers `*_current` and verified `source_kind=current`. SHAs (no push): ML2 `5f3d5c841a10145a33cb1723ee17e1097637f4a2`, Pacific `5bc07464631aa429c0d5813c55fe5db9455315bf`, Ecosystem `0bd1ecbd292863f8e39dea1696959a8bcf31ba70`. RI confirmed the report blend at ~03:33; EcoFlow stays Pacific and ML2 never runs vision.

2026-10-02 ~03:33 HST: Report Instructor confirmed the Kīlauea report blend: spoken/written output states whether a still was viewed (Y/N) and, when viewed, what conditions looked like. Bank/archive/current paths remain verified. RI’s next lane is News freshness/rotate for RadioRss and the news hour, using the ML2-streamed bank while Pacific local polling is gated.

2026-10-02 ~03:35 HST: Alexander — solar reboot pending. After return, verify `RR_LOCAL_DATA_POLL=0` (ML2-on exclusive gate), receive tunnel up, and services clean. ML2 keeps polling; Telegram handoff buffer is the Mainland fallback if the stream drops. News rotate stays RI. No commit/push.

2026-10-02 ~03:30 HST: Alexander clarified that ML2/Mainland only polls and banks stills as `*_current` for solar; Pacific LLMs do the looking/vision, no vision runs on the Mainland host. **Superseded ~03:31–03:33 HST** by verified bank and report-blend entries above; no commit/push.

2026-10-02 ~03:28 HST: Alexander → Wren — Kīlauea photo must be blended into spoken/written reports: state whether a still was viewed (Y/N) and, when viewed, the conditions. **Superseded ~03:33 HST** by RI-confirmed report blend; bank/archive details are superseded ~03:31 HST. No commit/push. See Ideas kilauea-checker, voice-desk, US-Mainland-Two.

2026-10-02 ~03:25 HST: Alexander → Wren — **WIP at the time; superseded ~03:31 HST:** Kīlauea USGS HVO stills are the first `*_current` consumer. The bank/archive verification is recorded above. See Ideas `2026-10-02-kilauea-checker-live-frame.md`, voice-desk, US-Mainland-Two. No commit/push.

2026-10-02 ~03:26 HST: Mainland → Wren — clarified the naming pattern (now verified ~03:31): archive-on-replace applies to every `*_current` product stream; live stays `_current` for LLM reads and dated `archive/` is history. Kīlauea is the first consumer. EcoFlow and cams stay forever-Pacific. No commit/push.

2026-10-02 ~03:23 HST: Mainland → Wren — `weather_hawaii` + `radio_rss` **LIVE** + SSH bank stream **verified** into same Pacific Database `path_rel` LLMs read (samples: `Weather/Hawai'i/ml2-collector-status.json` ok; hurricane tracks fresh; `Media/RadioRss` health/queue ok). LIVE inventory: geology + weather_us_states + weather_hawaii (600s oneshot; hurricanes via it) + radio_rss; runner exclusive `RR_LOCAL_DATA_POLL=0`. Local SHAs (no push): `ca39035` (weather_hawaii+radio_rss vendor), `6a6ebd8` (Discord/Telegram poller scaffolds + Telegram datapack fallback), `08f6e05` (OFFLINE-TELEGRAM-BUFFER.md + clearer systemd Descriptions), `8cb0456` (ml2-purge no-stack: wipe weather-bank archive/imagery scratch; handoff≈0). Discord poller blocked on token; Telegram council-relay stays Pacific. Pacific datapack-pickup allowlist + `ml2_datapack_pickup` (timer+boot). Stale-desk notes cleared (voice-desk / prior awaiting-stream Working). Alexander overnight asks partially addressed: receive/Telegram + SSH-LLM landed; labels partial via Descriptions. See US-Mainland-Two, voice-desk, Desk-Automations. No commit/push (Library desk only).

2026-10-02 ~03:21 HST: Report Instructor → Wren — Kīlauea 15-min image checker **LIVE on Pacific** (local, no commit). `Geology/scripts/kilauea_look.py` (Gemma / panel_look stack); `voice_reports` `kilauea_image_check` (Carly) + `voice_deliver` title; `jobs.py` `voice_kilauea_image_check` every 900 s; gate `RR_VOICE_KILAUEA_IMAGE` soft default `:-1` (on for soak) in `run-poller.sh`. **Not** in `LOCAL_DATA_POLL_JOBS` (report-side only). Bank: Database `Cams/kilauea-look-last.json` + `lava-fountain-ref.jpg`. Flow: USGS HVO still (prefer fresh Cams v3/v1/v2; else live GET) → Gemma vs optional fountain ref → Carly “Kilauea observation image was checked” + measured finding. **Needs poller restart** before gate takes effect. Ideas page flipped PROPOSED→LIVE. See Ideas `2026-10-02-kilauea-checker-live-frame.md`, voice-desk. No commit/push.

2026-10-02 ~03:21 HST: Alexander overnight asks (via RI room) → Wren — Working requirements filed. **Superseded ~03:23:** receive/Telegram + SSH-LLM landed (Mainland); labels partial via systemd Descriptions — see ~03:23 Recent + Working. No commit/push.

2026-10-02 ~03:15 HST: Alexander → Wren — idea (not built): new Kīlauea checker — live frame from official sources → image analyzer; volcano updates every 15 min; Carly voice “Kilauea observation image was checked”; check for fountaining (training image findable). Soft only — Report Instructor owns build. See `Documentation/08-Ideas/2026-10-02-kilauea-checker-live-frame.md`. No commit/push.

2026-10-02 ~03:14 HST: Master → Wren — Root Monitor data-poll **kill-switch fix** (desk only, no commit). Cause: Automations `job_enabled()` read panel env (gated jobs looked On while `live_raw=0`); apply without restart → DESIRED≠LIVE; intent YAML inline `#` comments broke `mode: remote`. Fix: Live binds to poller env; UI Automations → Data poll **Live=ML2 offload**, gated jobs Off + “ML2 owns”; drop-in + restart + sync-ml2 apply **both ways**. Touched Pacific `Automations/scripts/automation_control.py`, `Apps/Control-Panel/Lib/rr_data_poll.py` + `rr_settings.py`, `rr_automations_page.py`, `rr_control_panel.py`, Database `System/control-panel/settings.json`. Backups `/tmp/root-monitor-toggle-fix-bak/`; report `/tmp/root-monitor-toggle-fix/REPORT.md`. Verified both directions; **left overnight ML2-on:** `RR_LOCAL_DATA_POLL=0`, drop-in=0, intent=remote, ML2 timers active, poller `:8799` live. Soft only — EcoFlow/cams ungated. Settings `data_poll_restart_poller` + `data_poll_sync_ml2` enabled (Alexander can confirm later). AWS Fallback Status `deployed=1` secondary (tree restored earlier; press Status once). See Control-Panel-GTK, Desk-Automations, Operators Handbook, US-Mainland-Two, US-Mainland-One. No commit/push.

2026-10-02 ~03:12 HST: Mainland → Wren — desk `weather_hawaii` + `radio_rss` enabled under exclusive gate. **Superseded ~03:23** by stream-verify + LIVE inventory (see above). No commit/push.

2026-10-02 ~03:11 HST: Master → Wren — Alexander: Telegram + Discord pollers go on the **ML2 side under the exclusive gate**; Pacific jobs stay; soft toggle only. Mainland: weather_hawaii + radio_rss still first so voice unsticks, then port those pollers; clean bounce if needed. **Not live on ML2 yet** — planned overnight after weather_hawaii + radio_rss; do not claim Telegram/Discord pollers landed. Clean-restart rule (Alexander overnight): any solar poller bounce → bring back clean with flag/env verified. See US-Mainland-Two (scaffold WIP + exclusive-gate §). No commit/push.

2026-10-02 ~03:08–03:10 HST: Library drift — `voice_timing_report` rewrote `voice-timing.md` (284 runs) still using hardcoded `:12`/`:42` lead and “ten-desk” prose while the schedule table already showed `[22, 52]`. Fixed Pacific `Reports/Voice-Timing/scripts/voice_timing_report.py` to derive lead and start minutes from `jobs.py` STACK schedule (nine desks; lead **7m59s**); regenerated page: nine-desk median **314s** / avg **386s** / p90 **698s** (p90 longer than lead → recommend moving `:22`/`:52` earlier). Aligned `2026-09-30-voice-desk.md`. No commit; no poller restart (script picked up on next `:05` run).

2026-10-02 ~03:08–03:09 HST: Master → Wren — exclusive data-poll gate standing rule. **Exclusive:** AWS/ML2 on ⇒ solar (Pacific local) data-poll off; solar/local on ⇒ AWS/ML2 pollers off. Soft kill-switch only — do not delete or hardcode collectors; Pacific collectors stay installed; `RR_LOCAL_DATA_POLL` flips them. Pacific already gates on `RR_LOCAL_DATA_POLL`; Mainland wiring ML2 side of the same gate. Overnight Mainland WIP expanding first-test toward `weather_hawaii` then `radio_rss` — **not landed yet**; first-test inventory remains geology + US weather (+ API) only. **EcoFlow / Energy and smart cams stay Pacific forever** — outside the exclusive gate, not moving to ML2. See US-Mainland-Two (exclusive-gate § under toggle-not-replacement), Desk-Automations, Control-Panel-GTK, Operators Handbook. No commit/push.

2026-10-02 ~03:02–03:04 HST: Master → Wren — first-test inventory + AWS Fallback restore. **ML2 is the API** (`api.rootrecord.cloud` → `:8091`); panel AWS Fallback stays on ML1 `rr-aws-ip` — do not retarget without Alexander ask. ML1 `/home/ubuntu/rootrecord/fallback` **restored** (deploy `20261002-030103-92360344`); first activate rolled back (globe units masked on radio-only); flags globe_web/history/ingest/feed_8787=0; Status bindable again (`deployed=1`, Mem~1319 MB, disk~2280 MB). **First test real** for geology + US weather + API only — not a full poller move. ML2 live collectors: `geology` + `weather_us_states` only; Pacific gated while `RR_LOCAL_DATA_POLL=0` (survived reboot): geology_collect, geology_kilauea_cams, weather_poller, weather_us_states, weather_radar_zip, weather_retention, country_location_pollers, radio_rss_poll; forever Pacific: EcoFlow/Energy, network_globe LAN tap. Room: Master — Status ON/OFF, leave ML1, globe stay masked; Report Instructor — quake/Kīlauea from ML2 banks OK, NWS Hawaiʻi/hurricane/news hour go stale until scaffolds or local poll back, analytics pull ML2 fine; Cove — Vercel no trackers, Home/Live→ML2 API, Radio→ML1 only. See US-Mainland-Two, US-Mainland-One, Control-Panel-GTK, Desk-Automations, voice-desk, Operators Handbook. No commit/push.

2026-10-02 ~02:56–02:57 HST: Master → Wren — post-boot into ML2 mode (drop-in `RR_LOCAL_DATA_POLL=0` already on disk; flip LIVE ~02:50 stands). Master confirm: poller still `RR_LOCAL_DATA_POLL=0` through reboot; `:8799` HTTP 200; EcoFlow/cams Pacific matches toggle; radio up. Alexander: radio / EcoFlow / cameras online; no Vercel network trackers yet; API still needs work; globe initially missing ping-line connectors. Cove: `www` Vercel stays without client trackers (option C / ML2 logs only); Home ping lines are `/api/state`; if hard refresh still blanks after feed push, Cove checks `home.js` on desk. Globe `/api/state` fixed ~02:56: empty arcs were ML2 stub; now Pacific `local-data-globe` rebroadcast (`hawaii-current.ndjson`) → ML2 `var/cache/api/state.json` (11 arcs / 7 points); ops status-current refreshed; desk timer `rr-ml2-globe-state-push` every 2m. Desk ML2 `6c66bf1` + `819f68e` (ahead, no push). LAN capture + EcoFlow stay Pacific. Report Instructor measured (~02:58): poller active / `RR_LOCAL_DATA_POLL=0`; voice WAVs nws 02:24, solar_desk 02:28, bandwidth 02:31, current_report md 02:33 — all pre-reboot (no new voice cycle since boot); analytics as_of 02:28:35 daily present; automations log fresh 02:58, no recent voice_/report_ failures; next refresh expected at live `:22`/`:52`. See `Documentation/01-Operations/2026-09-30-voice-desk.md`, `Documentation/15-Domains-and-External-Systems/US-Mainland-Two.md`, `Agent Context/Web-Agent-Context/CONTEXT/SITE.md`.

2026-10-02 ~02:50 HST: Master → Wren — desk data-poll flipped to **ML2 LIVE**. Settings write mode, `data_poll_desired=ml2`; drop-in `~/.config/systemd/user/rr-rootserver-poller.service.d/rr-data-poll.conf` `Environment=RR_LOCAL_DATA_POLL=0`; intent `data_poll_mode.yaml` `mode=remote`; poller restarted. Verified `live_raw=0` / `live_label=ML2 offload`; `:8799` HTTP 200. Schema parity PASS (~02:39) still stands. Clears earlier “`RR_LOCAL_DATA_POLL` still not flipped” / default-local-ON-as-current-live notes; toggle-not-replacement (collectors stay installed; gate flipped). No git commit. See `Documentation/15-Domains-and-External-Systems/US-Mainland-Two.md`, `Documentation/11-Runtime-Jobs-and-Control/Desk-Automations-and-Service-Windows.md`, `Documentation/11-Runtime-Jobs-and-Control/Control-Panel-GTK.md`.

2026-10-02 ~02:15–02:33 HST: Pacific desk uptime + host power mode for `system_perf`. `System/scripts/uptime_log.py` now records offline/return samples and `connectivity-daily.json` (averages start at `recording_since`; old testing stamps ignored); `RR_UPTIME_LOG` defaults to 1 in `run-poller.sh` (`system_uptime_log` every 60 s). New read-only `System/scripts/power_profile.py` logs performance/balanced/energy saver into Database `System/power-profile/` (never sets a mode); each uptime tick calls it. Bruce `system_perf` speaks connectivity lines and “Host power mode is …”. Tests: `test_uptime_connectivity.py`, `test_power_profile.py`. Library: voice-desk, Voice-Reports-G3. No commit from this doc pass.

2026-10-02 ~02:39 HST: Mainland — schema parity PASS; ML2 geology + weather_us_states match Pacific last-file contracts. Quakes enriched `events[]`; volcanoes / `hvo-last` Pacific shape (`alert_level`/`color_code`/`erupting`/`latest_notice`/`at`); `collector-last` `sources{}`; `us-last` `{updated_at, location_count:77, rows}`. SHAs: desk ML2 `6425c8a`, host `087ee38`, Ecosystem `00985524`, Library `2fc7a47`. Prior schema-FAIL blocker cleared. At that sitting gate was not yet flipped; **live flip landed ~02:50** (see above). Local commits desk+host; no push; ML1 radio untouched. See `Documentation/15-Domains-and-External-Systems/US-Mainland-Two.md`.

2026-10-02 ~02:34 HST: Mainland verification-only FYI (no commits) — schema parity FAIL noted (quakes/volcano/us-last). **Superseded ~02:39** by schema parity PASS (see above).

2026-10-02 ~02:32 HST: Master → Wren — Root Monitor **data-poll toggle UI** landed desk-local under Pacific `Apps/Control-Panel/`. New `Lib/rr_data_poll.py`; updated `Lib/rr_settings.py` (defaults dry-run / desired=local / apply_dropin=false), `rr_automations_page.py` (Automations Local Pacific vs ML2), `rr_control_panel.py` Settings keys, README, Operators Handbook, `Automations/config/data_poll_mode.example.yaml`. Behavior: toggle not replacement; confirm before write; no auto poller restart; live collectors not flipped this session. **Alexander must restart Root Monitor to see the GTK.** Library: Control-Panel-GTK, Desk-Automations-and-Service-Windows, Operators Handbook, US-Mainland-Two (GTK pointer only). No commit/push.

2026-10-02 ~02:33 HST: Report Instructor — folded Mainland Home/Radio analytics into Pacific reports (schema 1.0.0, no page JS). New Pacific `Website/scripts/analytics_pull.py` → daily JSON under Database `Logs/Website/analytics/` (sample `daily/2026-10-02.json`; READMEs on bank + Website). Voice `bandwidth_desk` and `current_report` speak site traffic (api / home_proxy / radio; honest partial Home). Job `analytics_pull` gated `RR_ANALYTICS_PULL=1` (900 s); off until armed in `run-poller.sh`. No commit. See `Documentation/01-Operations/2026-09-30-voice-desk.md`, `Documentation/10-AI-and-Agent-Runtime/Voice-Reports-G3.md`, `Agent Context/Web-Agent-Context/CONTEXT/SITE.md`, and `Documentation/15-Domains-and-External-Systems/US-Mainland-Two.md`.

2026-10-02 ~02:29 HST: Mainland — ML2 analytics + bank path landed. SHAs: desk ML2 `484abe1`, host `559f90e`, Ecosystem `bfa9ff2f`. Analytics: `ANALYTICS.md` plus `/api/analytics/daily|period|current`; desk sink `Logs/Website/analytics/`. Stream verified: 7 handoffs → Pacific Geology + Weather/US-States via `ml2-db-stream` on desk `rr-ml2-db-tunnel` `:17022`. Collectors on: geology + weather_us_states. `RR_LOCAL_DATA_POLL` gate in Pacific `automation_control.py`, default local ON, not flipped. Toggle-not-replacement + local-mirror plan already on Library pages (~02:26); SHAs and live stream/analytics state attached. See `Documentation/15-Domains-and-External-Systems/US-Mainland-Two.md`.

2026-10-02 ~02:26 HST: Alexander — ML2 cutover is a **toggle**, not replacement. Pacific/home data polling stays installed; `RR_LOCAL_DATA_POLL` (or equiv; host `docs/TOGGLE.md`) turns local polling off while ML2 is healthy and back on if AWS/ML2 dies — never delete home collectors. Near-term: Mainland brings ML2 collectors + stream + API fully online with that toggle; Pacific remains sole long-term bank; SHAs when the working path lands. Later (document now, not building): mirror functions into desk repos `US-Mainland-One` and `US-Mainland-Two` for local failover parity if mainland servers go down. See `Documentation/15-Domains-and-External-Systems/US-Mainland-Two.md`.

2026-10-02 ~02:18 HST: Report Instructor — news hour refilled after sports cut. `news_update` now targets ~20–25 spoken minutes (`target_words: 3500`); Ava/Bruce/Carly share airtime via `balance_personas`. Mix: chips/NVIDIA/Microsoft/big tech, world news every continent (Asia, Australia, Africa, Europe, LatAm, ME, US/Canada), mainland weather, centrist mainland politics, universities, science breakthroughs. Sports filter kept; partisan patterns drop on centrist feeds. Pacific `Media/RadioRss/` touched: `categories.yaml`, `policy.yaml`, `feeds.yaml`, `news_hour.py`, `stories.py`, `pipeline.py`, `test_rss_radio.py` (passed), `README.md`. Library pages updated for the new hour shape. No commit. See `Documentation/01-Operations/2026-09-30-voice-desk.md`, `Documentation/01-Operations/2026-10-01-radio-station.md`, and `Documentation/10-AI-and-Agent-Runtime/Voice-Reports-G3.md`.

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
