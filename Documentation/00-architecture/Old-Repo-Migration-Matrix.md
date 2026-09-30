# Old-Repo Migration Matrix (G1 `Solar-Pacific-RootRecord-Server-Old` + G0 `old` → G3)

| Field | Value |
| --- | --- |
| **Date** | 2026-09-29 (HST), pass started 13:12 HST |
| **Sources (read-only)** | https://github.com/rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server-Old (G1, 97 top-level packets, 4 193 files) · https://github.com/rootrecordsoftwaresolutions/old (G0, 3 811 files). Shallow clones in `/tmp/rr-migr/` for reading, deleted after the pass. Nothing written to either repo. |
| **Compared against** | Pacific `1 - RootRecord-Pacific-Solar-Server` (G3), Database `2 - RootRecord-Database`, [G1 README status list](https://github.com/rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server-Old/blob/main/README.md), [Solar-Pacific-Old-Inventory-Map](./Solar-Pacific-Old-Inventory-Map-2026-09-28.md), [G3 Runtime Verification Checklist](./G3-Runtime-Verification-Checklist-2026-09-28.md), WO-ECO §4 migration checklist |
| **Rule** | Copy and port only. Nothing retired, moved or deleted (retirement needs Alexander's explicit sign-off). Every periodic port is gated OFF in `jobs.py`. |
| **Test records** | [Geology earthquakes + HVO](../07-testing/2026-09-29-geology-earthquakes-hvo-collector.md) · [Old-repo ports batch 1](../07-testing/2026-09-29-old-repo-ports-batch1.md) · [Voice batch 3 (hurricane + Kīlauea)](../07-testing/2026-09-29-voice-reports-batch3-hurricane-kilauea.md) |
| **Evidence** | `2 - RootRecord-Database/Logs/Migration/migration-geology-evidence-20260929T2319Z.md` |

**Status words:** *migrated* = the capability exists in G3 (LANDED or better; each row says whether it is gated) · *partial* = some of it exists in G3, the rest is listed · *missing* = not in G3. "THIS PASS" marks rows changed on 2026-09-29 13:12 HST onward. "Bucket" in the counts: core = Pacific runtime scope, geology = priority-1 scope, library = docs/agent context, product = product/website repos (out of Pacific scope), archive = archive-only.

## Summary counts

| Rows | migrated | partial | missing | touched this pass |
|---|---|---|---|---|
| 90 | 27 | 27 | 36 | 23 |

| Bucket | migrated | partial | missing |
|---|---|---|---|
| geology | 6 | 3 | 0 |
| core | 18 | 21 | 16 |
| library | 0 | 2 | 3 |
| product | 0 | 0 | 15 |
| archive | 0 | 2 | 4 |

Bucket table is as of 13:50 HST; breadth-pass changes since then (all core bucket): rows 39, 48 and 76 → migrated, row 79 → partial; rows 17, 34, 35, 42, 50, 60 reviewed without a status change.

Grouped rows: related G1 packets that share one G3 target are one row (e.g. the 11 public-site packets). The 97 G1 tops + the G0 operations tree map onto these 90 rows.

## Migrated in this pass (all LANDED; one light manual test each; periodic jobs gated OFF)

| Port | G3 path | Gate / schedule | Test |
| --- | --- | --- | --- |
| USGS Hawaiʻi + global earthquakes, HVO Kīlauea / Mauna Loa status + notices | Pacific `Geology/scripts/geology_collect.py` → Database `Geology/{Earthquakes,Volcanoes}/` | `RR_GEOLOGY=1`, 300 s | PASS |
| Earthquake voice report (Carly) | `Media/Voice/scripts/voice_reports.py earthquake_report` | `RR_VOICE_QUAKE=1`, :08 | PASS (text); WAV VERIFY PENDING |
| Kīlauea cams catalog + USGS stills | `Geology/scripts/kilauea_cams.py` → Database `Geology/Volcanoes/Cams/` | `RR_KILAUEA_CAMS=1`, 600 s | PASS |
| USGS backfill → SQLite | `Geology/scripts/earthquakes_backfill.py` → Database `Geology/Earthquakes/quakes.db` (git-ignored) | on demand | PASS (`--days 1`) |
| Sun times | `Energy/scripts/sun_times.py` → Database `Energy/sun/` | `RR_SUN_TIMES=1`, hourly (1 fetch/day) | PASS |
| Uptime log | `System/scripts/uptime_log.py` → Database `System/uptime/` | `RR_UPTIME_LOG=1`, 60 s | PASS |
| MP4 converter | `Media/Video/scripts/mp4_converter.py` → Database `Media/Video/` | on demand | PASS |
| Hurricane desk voice report (Carly, Hawaiʻi block) | `Media/Voice/scripts/voice_reports.py hurricane_desk` | `RR_VOICE_HURRICANE=1`, 05:50/09:50/12:50/16:55/20:50 | PASS (text); WAV VERIFY PENDING |
| Kīlauea voice report (Carly, hourly desk + HVO notice) | `Media/Voice/scripts/voice_reports.py kilauea_report` | `RR_VOICE_KILAUEA=1`, :03 | PASS (text); WAV VERIFY PENDING |
| G0 nearest-location tag on quakes (≤ 250 km) | `Geology/scripts/geology_collect.py` + `Geology/config/global-locations.json` | rides `RR_GEOLOGY` | PASS |
| Web facts (allowlisted HTTPS GET) | `Communications/web-facts/scripts/web_facts.py` | on demand | PASS |
| Hawaiʻi news collector (G0 RSS discovery) | `Reports/News/scripts/{_collector,hawaii_news}.py` → Database `Reports/News/hawaii/` | PROPOSED `RR_HAWAII_NEWS=1`, 10:00 (not in jobs.py) | rc 0 but FAIL on content (0 posts) |
| Host net counters / usage windows / security snapshot | `System/scripts/host_desks.py` → Database `System/{network,security}/` | PROPOSED `RR_NET_SAMPLES=1`, 300 s (not in jobs.py) | PASS |
| Solar / security / bandwidth desk voice reports | `voice_reports.py solar_desk` (Bruce), `security_desk`, `bandwidth_desk` (Carly) | PROPOSED `RR_VOICE_SOLAR` :04, `RR_VOICE_SECURITY` :11, `RR_VOICE_BANDWIDTH` :12 (not in jobs.py) | PASS (text); WAV VERIFY PENDING |
| Live weather lines for chat (G1 live-wx) | `Communications/live-wx/scripts/live_wx.py` | on demand (`--offline` = no HTTP) | PASS |

Breadth rows (13:58–14:09 HST): test record [2026-09-29-old-repo-ports-breadth-batch4](../07-testing/2026-09-29-old-repo-ports-breadth-batch4.md); proposed job blocks: [Pending-Job-Registrations-2026-09-29](Pending-Job-Registrations-2026-09-29.md).

## Matrix

| # | Item | Old path | G3 status | Target path | Blockers / notes |
|---|---|---|---|---|---|
| 1 | USGS earthquake poll Hawaiʻi + global (earthquake-hourly fetch, M≥2 poll) | `Solar-Pacific-RootRecord-Server-Old/earthquakes/earthquake-hourly/scripts/earthquake_hourly.py` | **migrated** | Pacific `Geology/scripts/geology_collect.py` → Database `Geology/Earthquakes/` | THIS PASS. Job `geology_collect` gated `RR_GEOLOGY=1` (300 s). Discord post + speaker play not ported (sign-off). |
| 2 | Earthquake hourly spoken report (Carly) | `Solar-Pacific-RootRecord-Server-Old/earthquakes/earthquake-hourly/scripts/earthquake_hourly.py (build_spoken)` | **migrated** | Pacific `Media/Voice/scripts/voice_reports.py earthquake_report` | THIS PASS. Job `voice_earthquake_report` gated `RR_VOICE_QUAKE=1` (:08). Text tested; WAV render not run (no model load). No delivery. |
| 3 | Kīlauea HVO poll (alert level, notice, headline, multiplier, quakes ≤150 km) | `Solar-Pacific-RootRecord-Server-Old/kilauea/rr-kilauea/scripts/kilauea.py` | **partial** | Pacific `Geology/scripts/geology_collect.py` → Database `Geology/Volcanoes/`; spoken desk `voice_reports.py kilauea_report` | THIS PASS (data + template voice). Uses HANS public API instead of HTML scrape. Voice job `voice_kilauea_report` gated `RR_VOICE_KILAUEA=1` (:03). NOT ported: Grok report_generation, public Discord draft queue (needs cloud spend + posting sign-off). |
| 4 | Mauna Loa / all HVO volcano status | `(new — HVO scope requested)` | **migrated** | Database `Geology/Volcanoes/{hvo,mauna-loa}-last.json` | THIS PASS (same collector). |
| 5 | Kīlauea cams (USGS V1/V2/V3 catalog + still fallback) | `Solar-Pacific-RootRecord-Server-Old/kilauea/kilauea-cams/scripts/kilauea_cams.py` | **partial** | Pacific `Geology/scripts/kilauea_cams.py` → Database `Geology/Volcanoes/Cams/` | THIS PASS. Job `geology_kilauea_cams` gated `RR_KILAUEA_CAMS=1` (600 s). OBS push BLOCKED (no OBS in G3); YouTube id scraping not ported. |
| 6 | Council quake Telegram posts (per-quake, Carly WAV) | `Solar-Pacific-RootRecord-Server-Old/council/council-quake/scripts/quake_watch.py` | **partial** | Detection: `hawaii-last.json new_local_m2_ids`; delivery: Communications/telegram (not built) | BLOCKED: Telegram send needs Alexander sign-off + relay replies BLOCKED (models). |
| 7 | Kīlauea Alerts Android app | `Solar-Pacific-RootRecord-Server-Old/kilauea/kilauea-alerts` | **missing** | Product repo | Out of Pacific scope (Play app). |
| 8 | weather-kilauea topic map | `Solar-Pacific-RootRecord-Server-Old/kilauea/weather-kilauea` | **partial** | Library / Pacific `Geology/README.md` | Docs-only packet; Geology README now lists the scripts. |
| 9 | USGS quake backfill → SQLite | `old/operations/backfillquakes.py` | **migrated** | Pacific `Geology/scripts/earthquakes_backfill.py` → Database `Geology/Earthquakes/quakes.db` (git-ignored) | THIS PASS. On demand only (no job). Full G0 default range = thousands of requests: operator decision. |
| 10 | 5-min quake poller → SQLite | `old/operations/cronologicals/since-last-fire/every-5-minutes/quakes.py` | **migrated** | Superseded by `geology_collect.py` (JSON last + Daily JSONL) | THIS PASS (capability). SQLite live table not kept; backfill script covers SQLite. |
| 11 | Global quake poller + nearest-location tag | `old/operations/earthquakes/global/poller.py` | **migrated** | `geology_collect.py` global + Hawaiʻi feeds; dataset Pacific `Geology/config/global-locations.json` (verbatim G0 copy) | THIS PASS. Every event gets `nearest` (location_id, name, country_code, admin1_code, km ≤ 250) like the G0 SQLite columns; real run 13:49 HST: Hawaiʻi 9/9 tagged, global 14/34. |
| 12 | Hybrid night poller | `Solar-Pacific-RootRecord-Server-Old/hybrid-night-poller` | **migrated** | Pacific `Automations/scripts/rootserver_poller.py` | MIGRATED.md 2026-09-28. |
| 13 | Heartbeat | `Solar-Pacific-RootRecord-Server-Old/heartbeat` | **migrated** | `jobs.py` builtin `heartbeat` | MIGRATED.md 2026-09-28. |
| 14 | Net gate | `Solar-Pacific-RootRecord-Server-Old/net-gate` | **migrated** | `Automations/scripts/poller/internet_gate.py` | MIGRATED.md 2026-09-28. |
| 15 | Scheduler clock (APScheduler map) | `Solar-Pacific-RootRecord-Server-Old/scheduler-clock` | **partial** | G3 `jobs.py` + poller | Superseded by design; verify-only. |
| 16 | Python drop runner (timed folders) | `Solar-Pacific-RootRecord-Server-Old/python-drop-runner` | **missing** | — | Not ported: runs arbitrary dropped .py; needs design + sign-off. |
| 17 | Host metrics / NPU probe | `Solar-Pacific-RootRecord-Server-Old/host-metrics` | **partial** | Pacific `System/lib/sample.py`, `System/scripts/plumbing/npu-status.sh`, `System/scripts/host_desks.py` (net counters + security snapshot) | THIS PASS (breadth): net byte counters, usage windows, security snapshot ported (`host_desks.py`, smoke PASS; sampler job PROPOSED `RR_NET_SAMPLES`). Still not ported: series reset / wattage helpers, Windows PDH GPU/NPU counters (not applicable on Linux). |
| 18 | System perf snapshot (job system-performance) | `Solar-Pacific-RootRecord-Server-Old/system-perf` | **migrated** | Pacific `Media/Voice/scripts/system_perf.py` | g3-voice-ailog, gated `RR_VOICE_SYSTEM_PERF`. |
| 19 | Uptime log (desk up/down events) | `Solar-Pacific-RootRecord-Server-Old/uptime-log/scripts/uptime_log.py` | **migrated** | Pacific `System/scripts/uptime_log.py` → Database `System/uptime/` | THIS PASS. Job `system_uptime_log` gated `RR_UPTIME_LOG=1` (60 s). psutil → /proc; wall clock + boot_id. |
| 20 | Log cleanup (delete stale logs) | `Solar-Pacific-RootRecord-Server-Old/log-cleanup` | **missing** | Database Logs policy | BLOCKED: deletes files — conflicts with never-delete rule; needs Alexander sign-off + retention design (cf. weather_retention dry run). |
| 21 | Ollama client / env / lifecycle | `Solar-Pacific-RootRecord-Server-Old/ollama-client, ollama-env, ollama-lifecycle` | **partial** | Pacific `System/scripts/plumbing/` (run-infer, run-ollama, warmups, keepalive 0) | Idle-stop-after-15-min lifecycle not ported (models non-resident already). |
| 22 | Model pick | `Solar-Pacific-RootRecord-Server-Old/model-pick` | **partial** | `System/scripts/plumbing/route-specialist.py` | Cloud model choice not ported (no cloud spend). |
| 23 | Launch / idle-stop / recycle-origin / ensure-ava-runtime | `Solar-Pacific-RootRecord-Server-Old/launch, idle-stop, recycle-origin, ensure-ava-runtime` | **partial** | Pacific `Automations/scripts/stack/*`, poller window | Origin :8787 does not exist in G3; stack stop/start replaces. |
| 24 | Feature toggles / ops banner | `Solar-Pacific-RootRecord-Server-Old/feature-toggles, ops-banner` | **partial** | G3 env gates in `jobs.py`; Pacific `Apps/Control-Panel/` (other agent) | Not touched (Control-Panel owned by another agent). |
| 25 | Boot prelims / day-board-boot / morning-boot-replay / sunrise-restore | `Solar-Pacific-RootRecord-Server-Old/boot, day-board-boot, morning-boot-replay, sunrise-restore` | **missing** | Automations ON_BOOT | Tied to origin + speaker playback; replay = playback (not allowed). Needs design. |
| 26 | fs-index (full-machine path index) | `Solar-Pacific-RootRecord-Server-Old/fs-index, live-directories` | **missing** | System | Not ported: full-disk scan is heavy and would index private paths; needs scope sign-off. |
| 27 | Core-ops install | `Solar-Pacific-RootRecord-Server-Old/core-ops-install` | **missing** | — | Obsolete (Core Ops store gone); archive. |
| 28 | EcoFlow BLE poller | `Solar-Pacific-RootRecord-Server-Old/energy/ecoflow-ble-poller` | **migrated** | Pacific `Energy/` (read path, ble-owner) | LIVE via G2→G3. |
| 29 | EcoFlow automations map | `Solar-Pacific-RootRecord-Server-Old/energy/ecoflow-automations` | **partial** | Pacific `Energy/` | Map doc; action scripts in `Energy/scripts/actions/`. |
| 30 | AC / solar USB-C gate (400 W) | `Solar-Pacific-RootRecord-Server-Old/energy/ecoflow-ac-solar-gate` | **partial** | `Energy/scripts/actions/solar-gate-*.sh` | Actuation VERIFY PENDING (needs approval). |
| 31 | EcoFlow quota (cloud API) | `Solar-Pacific-RootRecord-Server-Old/energy/ecoflow-quota` | **partial** | `Energy/lib/ecoflow_api.py` | Needs EcoFlow API keys (env) — sign-off; BLE is primary. |
| 32 | River car DC drive automation | `Solar-Pacific-RootRecord-Server-Old/energy/ecoflow-river-car` | **missing** | Pacific `Energy/` | Actuates DC power — needs Alexander sign-off. |
| 33 | Sun times (sunrise/sunset HST) | `Solar-Pacific-RootRecord-Server-Old/reports/sort/hourly-solar-weather/scripts/sun_times.py` | **migrated** | Pacific `Energy/scripts/sun_times.py` → Database `Energy/sun/` | THIS PASS. Job `energy_sun_times` gated `RR_SUN_TIMES=1` (hourly, 1 fetch/day). |
| 34 | Hourly solar + weather report | `Solar-Pacific-RootRecord-Server-Old/reports/sort/hourly-solar-weather/scripts/job.py` | **partial** | voice `solar_desk` + `energy_report` + `nws_weather`; `Energy/scripts/sun_times.py` | THIS PASS (breadth): `solar_desk` (Bruce, SOC / solar W / AC out + sun times) text smoke PASS, job PROPOSED `RR_VOICE_SOLAR`. Not ported: EcoFlow cloud quota signing, D1 push, SQLite/host history charts (cloud keys; G3 Energy db already covers history). |
| 35 | Load categories (solar desk labels) | `Solar-Pacific-RootRecord-Server-Old/load-categories/scripts/load_categories.py` | **missing** | Pacific `Energy/` | BLOCKED: keyed to G1 EcoFlow cloud-quota field names (pd.usb1Watts…); G3 last-files carry only `ac_output_power`, `ac_input_power`, `usbc_output_power`, `solar_input_power`, `charge_source` (THIS PASS review 14:10) — the transfer / e-batt / Starlink / emergency roles need a field map + Alexander check of the thresholds. |
| 36 | EcoFlow cronologicals (1min…yearly rollups) | `old/operations/cronologicals/since-last-fire/*/ecoflow-*.py` | **partial** | Pacific `Energy/db/aggregate.py`, `condense.py` | Layers exist in G3 Energy db. |
| 37 | System per-second / per-minute (cronologicals) | `old/operations/cronologicals/since-last-fire/every-second/system.py, every-minute/system-min.py` | **migrated** | Pacific `System/scripts/sys-sample.sh` | LIVE via G2→G3. |
| 38 | Uptime per-minute (cronologicals) | `old/operations/cronologicals/since-last-fire/every-minute/uptime.py` | **migrated** | Pacific `System/scripts/uptime_log.py` | THIS PASS (same capability as G1 uptime-log). |
| 39 | NWS Hawaiʻi counties / rr-noaa / live-wx | `Solar-Pacific-RootRecord-Server-Old/weather/nws-hawaii, rr-noaa, live-wx` | **migrated** | Pacific `Weather/` (fetch, alerts, county_map, reports); `Communications/live-wx/scripts/live_wx.py` | Weather daemon LIVE. THIS PASS (breadth, 14:09 HST): live_wx chat helper ported (on demand, `--offline` = no HTTP), smoke PASS; not wired to council chat (BLOCKED). |
| 40 | Hurricane fetch / tracker / desk | `Solar-Pacific-RootRecord-Server-Old/weather/hurricane-fetch, hurricane-tracker, hurricane-desk` | **partial** | Pacific `Weather/hurricanes/` (fetch/track); desk `Media/Voice/scripts/voice_reports.py hurricane_desk` | THIS PASS (desk). Hawaiʻi block ported from G3 `track.json` + NWS HI alerts; job `voice_hurricane_desk` gated `RR_VOICE_HURRICANE=1` (05:50/09:50/12:50/16:55/20:50). Still missing: G1 global JTWC/RAMMB board (G3 tracks only Hawaiʻi-relevant NHC storms), storm plot. |
| 41 | Hurricane OBS / radio | `Solar-Pacific-RootRecord-Server-Old/weather/hurricane-obs, hurricane-radio` | **missing** | — | BLOCKED: OBS + radio playback not in G3 (no playback allowed). |
| 42 | Radar archive / official weather media | `Solar-Pacific-RootRecord-Server-Old/weather/radar-archive, official-weather-media` | **partial** | Pacific `Weather/fetch/radar.py` (HAWAII_loop.gif, `archive/` 14 days), `maps.py` | THIS PASS (review): radar-archive capability already covered by G3 weather (dated archive; G1's all-time zip not ported, disk). official-weather-media **BLOCKED**: G3 weather collects AFD/SFP/CWF/ZFP but not HLS/HWO (adding them = weather poller product-list change, other domain) and its OBS overlay push has no G3 target. |
| 43 | US weather fetch (all states) | `old/operations/weather/fetch_us_weather.py + every-hour/fetch-us-weather.py` | **missing** | Website data (avaivy.cloud) | Product/website dataset; out of Pacific scope. |
| 44 | Reports worklog | `Solar-Pacific-RootRecord-Server-Old/reports` | **migrated** | Pacific `Reports/` | MIGRATED.md 2026-09-28 (WO-RPT-001). |
| 45 | Morning / midday / late reports (generate) | `Solar-Pacific-RootRecord-Server-Old/reports/sort/morning-report, midday-report, late-report, report-generation` | **partial** | voice_reports.py roll-ups (template-first) | Grok/cloud generation not ported (no cloud spend). |
| 46 | Report play jobs (morning/midday/late/evening play, periodic audio, replay) | `Solar-Pacific-RootRecord-Server-Old/reports/sort/*-play, report-periodic-audio, evening-*` | **missing** | — | BLOCKED: speaker playback not allowed. |
| 47 | Remaining tasks / day board | `Solar-Pacific-RootRecord-Server-Old/remaining-tasks` | **migrated** | voice `remaining_tasks` | g3-voice-reports2. |
| 48 | Hourly clip reports / chimes | `Solar-Pacific-RootRecord-Server-Old/hourly-clip-reports` | **migrated** | voice `hourly_chime`, `kilauea_report`, `solar_desk`, `security_desk`, `bandwidth_desk` (+ `system_perf`, `nws_weather` for the host / weather desks) | THIS PASS: every G1 desk has a G3 text builder (smoke PASS); WAVs VERIFY PENDING; `kilauea_report` gated in jobs.py (`RR_VOICE_KILAUEA`), solar / security / bandwidth jobs PROPOSED (not in jobs.py). Playback not ported (row 46). |
| 49 | Energy report (Carly) | `Solar-Pacific-RootRecord-Server-Old/reports/sort/energy-report` | **migrated** | voice `energy_report` | Vision caption not used. |
| 50 | Daily report board / catch-up / day-reports / readiness / merged-morning | `Solar-Pacific-RootRecord-Server-Old/reports/sort/daily-*, day-reports*, report-readiness; Solar-Pacific-RootRecord-Server-Old/merged-morning` | **missing** | Reports/ | THIS PASS (review): tied to G1 `report_generation`, `day_board`, `voice_events` and playback (`report_periodic_audio.play_if_due`); fixed-time roll-ups already exist in G3 (ON_AT 09:02 / 12:02 / 21:02). Due-ledger + catch-up not ported — needs a G3 design; readiness playback BLOCKED (no speakers). |
| 51 | Economy brief (+Discord) | `Solar-Pacific-RootRecord-Server-Old/reports/sort/economy-brief` | **missing** | — | Discord delivery → sign-off. |
| 52 | Report blog / audio manual / hybrid reports | `Solar-Pacific-RootRecord-Server-Old/reports/sort/report-blog, report-audio-manual, hybrid-reports` | **missing** | Website / Reports | Blog = public site (product). |
| 53 | Kokoro TTS | `Solar-Pacific-RootRecord-Server-Old/kokoro` | **migrated** | Pacific `Media/Voice/scripts/` | kokoro-voice-port-g3. |
| 54 | Synth (Ara/Grok/Cursor TTS routing) | `Solar-Pacific-RootRecord-Server-Old/synth` | **partial** | Pacific `Media/Voice/` (local Kokoro only) | Cloud TTS not ported (spend). |
| 55 | MP4 converter (still+MP3) | `Solar-Pacific-RootRecord-Server-Old/mp4-converter/scripts/mp4_converter.py` | **migrated** | Pacific `Media/Video/scripts/mp4_converter.py` → Database `Media/Video/` | THIS PASS. On demand only (no job); WAV accepted. |
| 56 | OBS studio helpers | `Solar-Pacific-RootRecord-Server-Old/obs-studio` | **missing** | — | BLOCKED: no OBS in G3. |
| 57 | Persona / speech scrub | `Solar-Pacific-RootRecord-Server-Old/persona` | **partial** | `Media/Voice/scripts/speakers.py`; Library Agent Context | Persona docs → Library. |
| 58 | Telegram helpers / council telegram | `Solar-Pacific-RootRecord-Server-Old/communications/telegram, council/council-telegram` | **partial** | Pacific `Communications/telegram/scripts/council-relay.py` | Replies BLOCKED (models); council skills not ported. |
| 59 | Discord / Slack pollers | `Solar-Pacific-RootRecord-Server-Old/communications/discord, slack` | **missing** | Pacific `Communications/{discord,slack}/` (README only) | BLOCKED: needs tokens (env) + posting sign-off (WO-COM-002). |
| 60 | Council health / Bruce stats | `Solar-Pacific-RootRecord-Server-Old/council/council-health, council-bruce-stats` | **missing** | Communications/ | THIS PASS (review 14:10): BLOCKED — checks need the three Telegram bot tokens (`getMe`), a live chat probe (model load) and alert sends to the council group; Bruce stats posts to Telegram. A G3 version needs sign-off. |
| 61 | Network globe / local-data-globe | `Solar-Pacific-RootRecord-Server-Old/network-globe, local-data-globe` | **migrated** | Pacific `Communications/network/local-data-globe/` | LIVE. |
| 62 | Cloudflare workers | `Solar-Pacific-RootRecord-Server-Old/cloudflare-workers` | **missing** | Website / edge repo | Out of Pacific runtime scope. |
| 63 | Inbox / inbox-drain / overnight-relay / reply-feedback | `Solar-Pacific-RootRecord-Server-Old/inbox, inbox-drain, overnight-relay, reply-feedback` | **missing** | Communications/ | Cloudflare D1 + DMs → secrets + sign-off. |
| 64 | Panels cam (Night Owl rear shed) | `Solar-Pacific-RootRecord-Server-Old/panels-cam` | **partial** | Pacific `Security/Cameras/` (ch1–4 grab) | River DC power-session for cam not ported (actuation). |
| 65 | Git auto-push | `Solar-Pacific-RootRecord-Server-Old/git-auto-push` | **migrated** | Pacific `Github/scripts/` (sync-all, push-once) | LIVE via G2→G3. |
| 66 | GitHub auto-push (G0) | `old/operations/system-tools/github-auto-push.py, every-hour/github-auto-push.py` | **migrated** | Pacific `Github/scripts/` | Superseded. |
| 67 | Code review pack | `Solar-Pacific-RootRecord-Server-Old/code-review` | **missing** | — | Needs LLM; next pass design. |
| 68 | Database / d1 / d1-sync / mysql / db-facts / data-layout / state / desk-data-reader | `Solar-Pacific-RootRecord-Server-Old/database/*, mysql, state, desk-data-reader` | **partial** | Database repo layout (WO-DATA) | D1/MySQL need credentials; policy docs only. |
| 69 | Ecosystem index / governance / goals / topics / skill-creator / root-record-registry / research-oa / history | `Solar-Pacific-RootRecord-Server-Old/ecosystem-index, governance, goals, topics, skill-creator, root-record-registry, research-oa, history` | **missing** | Library / Agent Context | Library content, not runtime. |
| 70 | People / users / account-import / subscribers | `Solar-Pacific-RootRecord-Server-Old/people, users, account-import, subscribers` | **missing** | Product (identity) | Personal data — do not copy into repos without sign-off. |
| 71 | Advertising (AdMob/AdSense EOD) | `Solar-Pacific-RootRecord-Server-Old/advertising` | **missing** | Product | Needs ad account secrets. |
| 72 | API prices / external AI API (xAI, Cursor fallback) | `Solar-Pacific-RootRecord-Server-Old/api` | **missing** | — | Cloud spend + keys → sign-off. |
| 73 | Clients / companions / fern-forest / finance-desk / pantry / product-prices / look | `Solar-Pacific-RootRecord-Server-Old/clients, companions, fern-forest, finance-desk, pantry, product-prices, look` | **missing** | Product / Library | Out of Pacific scope. |
| 74 | Minecraft / RootMC / player-economy / rcon / rootmc-android | `Solar-Pacific-RootRecord-Server-Old/minecraft, player-economy, rcon, rootmc-android` | **missing** | RootMC product | Out of Pacific scope. |
| 75 | Public site: live-data-pages / public-* / site-* / vercel-builds / websites / holding / stripe-poll | `Solar-Pacific-RootRecord-Server-Old/live-data-pages, public-chat, public-edge, public-finance, public-health, site-backgrounds, site-ops, vercel-builds, websites, holding, stripe-poll` | **missing** | Website repo | Out of Pacific scope; Stripe/Vercel keys. |
| 76 | Web facts (allowlisted GET for council) | `Solar-Pacific-RootRecord-Server-Old/websites/web-facts` | **migrated** | Pacific `Communications/web-facts/scripts/web_facts.py` | THIS PASS (breadth): logic unchanged, on demand; smoke PASS (allowed USGS URL ok; non-allowlisted host / http refused). Not wired to the council relay (council chat BLOCKED). |
| 77 | origin (Ava-Core app, ~2.4k files) | `Solar-Pacific-RootRecord-Server-Old/origin` | **partial** | Archive-only | Voice plugins / quake services mined for this pass; never bulk-import. |
| 78 | ecosystem-history / origin-session | `Solar-Pacific-RootRecord-Server-Old/ecosystem-history, origin-session` | **missing** | Archive-only | Library archive decision. |
| 79 | Hawaiʻi news collector (RSS discovery) | `old/operations/news/collect_hawaii_news.py, _collector.py, hawaii/news.py` | **partial** | Pacific `Reports/News/scripts/{_collector,hawaii_news}.py` → Database `Reports/News/hawaii/` (DB git-ignored) | THIS PASS (breadth): ported (timeouts capped 10 s); smoke rc 0 but **FAIL on content** — 25 × HTTP 404, 0 posts (hawaii.gov news links not discoverable). Job PROPOSED `RR_HAWAII_NEWS` 10:00. Needs: seed feeds (e.g. governor.hawaii.gov/feed/) + target decision. 49 other states / global news = product data, not ported. |
| 80 | State + global news builders (50 states) | `old/operations/news/*/news.py, build_state_news.py, build_global_news.py` | **missing** | Website data | Out of Pacific scope. |
| 81 | Location pollers (~250 countries) | `old/operations/locations/**/poller.py` | **missing** | Website data | Out of Pacific scope. |
| 82 | Ava-core cronologicals runner | `old/operations/cronologicals/ava-core.py, operations/ava-core.py` | **migrated** | Pacific poller | Superseded by G3 poller. |
| 83 | Broadcast (EcoFlow API + /directory browser) | `old/operations/broadcast.py` | **missing** | — | Serves a file-tree browser — security review needed; not ported. |
| 84 | AI usage / ecosystem report (Grok) | `old/operations/system-tools/ai_usage*.py, operations/api-ai-tasks/ecosystem_report.py` | **partial** | Pacific `Reports/ai_processing_report.py` | Grok key path = secret; cloud spend not ported. |
| 85 | Context session builder (FastAPI) | `old/operations/context_session_builder` | **missing** | Library / Apps | Needs FastAPI service design. |
| 86 | Meta AI chat | `old/operations/meta/meta.py` | **missing** | — | Third-party chat client; not ported. |
| 87 | Directory printer / sync / visual CLI / database-root-migrate / uploader / mapper / create_migration | `old/operations/system-tools/*, core_uploader.py, file_mapper.py, create_migration.py, tools/build-global-routes.py` | **missing** | — | One-off ava-core tooling (/home/ava-core paths); archive. |
| 88 | Audio clip library (numbers, time clips, voice) | `old/audio` | **partial** | Pacific `Media/Voice/` phrase-clip cache | G3 regenerated clips with Kokoro; binary audio not copied. |
| 89 | Web sites / cloudflare config / thumbnails | `old/web, Thumbnails` | **missing** | Website repo | Out of Pacific scope. |
| 90 | Config (routes, locations) / context docs | `old/config, context, AGENTS.md` | **missing** | Library / website | Docs + website data. |

## Blockers (BLOCKED — need Alexander)

1. **Delivery / posting:** council-quake Telegram posts, earthquake Discord post, rr-kilauea public draft queue, council health alerts, Discord/Slack pollers, economy brief — sends need explicit sign-off (and relay replies are BLOCKED on missing `*-telegram` models).
2. **Playback:** report play jobs, hurricane radio, morning boot replay — speaker playback not allowed.
3. **OBS:** kilauea-cams OBS push, hurricane OBS, obs-studio — no OBS in G3.
4. **Destructive:** log-cleanup deletes files — conflicts with never-delete; needs a retention design like `weather_retention` (dry run first).
5. **Actuation:** river-car DC drive, panels-cam power session, solar gate arm/disarm — hardware changes need approval.
6. **Secrets / cloud spend:** EcoFlow cloud quota, API prices / xAI / Cursor fallback, Grok report generation, AdMob/AdSense, Stripe, D1/MySQL — need keys (env var names only) and a spend decision.
7. **Field mapping:** load-categories uses G1 cloud-quota keys; G3 BLE last-files differ.
8. **Scope decisions:** fs-index (full-disk index of private paths), python-drop-runner (runs arbitrary dropped code), broadcast (serves a file-tree browser), Hawaiʻi news collector target folder.
9. **Weather products not collected:** official-weather-media needs HLS / HWO; G3 weather collects AFD / SFP / CWF / ZFP only — changing the weather poller product list is another domain's change.
10. **Hawaiʻi news source:** G0 discovery finds 0 posts (25 × HTTP 404 on hawaii.gov news links); needs seed feeds chosen by Alexander.
11. **Report ledger / catch-up / readiness, sunrise-restore, economy brief:** depend on G1 report_generation + speaker playback, MySQL credentials and Discord posting.

## Sign-off items (Alexander)

1. **jobs.py registrations** — 7 gated blocks added by this pass before the standing rule arrived (left in place, OFF): keep or remove. Exact blocks: `2 - RootRecord-Database/Logs/Migration/migration-jobs-py-additions-20260929.md`.
2. **Flags** at the next poller start: `RR_GEOLOGY`, `RR_KILAUEA_CAMS`, `RR_VOICE_QUAKE`, `RR_VOICE_KILAUEA`, `RR_VOICE_HURRICANE`, `RR_SUN_TIMES`, `RR_UPTIME_LOG`.
8. **Proposed job registrations (not in jobs.py)** — `system_net_sample` (`RR_NET_SAMPLES`), `voice_solar_desk` (`RR_VOICE_SOLAR`), `voice_security_desk` (`RR_VOICE_SECURITY`), `voice_bandwidth_desk` (`RR_VOICE_BANDWIDTH`), `reports_hawaii_news` (`RR_HAWAII_NEWS`); exact blocks in [Pending-Job-Registrations-2026-09-29](Pending-Job-Registrations-2026-09-29.md). Standing rule: jobs.py edited only on Alexander's request or a WO.
3. Any delivery (Telegram / Discord / speakers / radio) for the new voice reports.
4. Full-range quake backfill (G0 defaults 2010 / 2020 → thousands of USGS requests).
5. `kilauea_cams.py --keep-dated` archiving (disk).
6. Database git churn from `Geology/*-last.json` (5 min) and `System/uptime/uptime-last.json` (60 s) once enabled — keep tracked or git-ignore.
7. Retirement of any G1/G0 source (all **KEPT**).

## Next candidates (safe, not done this pass)

G1 global hurricane board (needs a JTWC/RAMMB source decision), official_weather_media voice (after HLS/HWO collection), web-facts wiring into council chat (after relay replies), load-categories (after field map), daily report ledger (after a G3 design), Hawaiʻi news seed feeds, host series-reset / wattage helpers.

*Created 2026-09-29 (migration pass). Update this file and the [G1 README](https://github.com/rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server-Old/blob/main/README.md) status tables together — the G1 README was **not** edited in this pass (no writes to old repos).*
