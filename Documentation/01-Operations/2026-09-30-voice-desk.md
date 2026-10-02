# Voice desk — current as of 2026-10-02

Finished Hawaii reports go to the Mainland station. The station snapshots the playlist at `HH:29:59` and `HH:59:59`, then chimes on the hour and the half hour. Voice jobs render before that snapshot. The station is on the air at `https://radio.rootrecord.cloud/radio/live.mp3`. The operator page is [2026-10-01 radio station](./2026-10-01-radio-station.md).

This is the living description of the spoken reports. The 2026-09-29 port record is [Voice-Reports-G3](../10-AI-and-Agent-Runtime/Voice-Reports-G3.md). Where that file still says a job is off, has no delivery, or uses an old minute, this file wins. Trust `Automations/scripts/poller/run-poller.sh` and `Automations/scripts/jobs.py` over older “what stays off” lists.

## Current as of 2026-10-02 ~03:21 HST

Alexander’s operator copy, checked against live `jobs.py`, `run-poller.sh`, `voice_reports.py`, `status_cue.py`, `voice_deliver.py`, Discord `public_report.py` / `report-channels.json`, and `publish_report_pages.py`. As of ~01:41 HST the separate `energy_report` voice job is retired: pack watts, newest ch1 still, and the hourly camera look live inside Bruce’s `solar_desk` (title “Energy and solar”). `status_cue.TYPES` lists **nine** generating desks. As of ~01:57 HST those nine desks and the stack-closer cycle key moved from `:12` / `:42` to `:22` / `:52` in `jobs.py` and `status_cue.cycle_key` (tests updated). Live timing is [voice-timing.md](./voice-timing.md) (generated 2026-10-02 11:05 HST, 433 finished runs, nine-desk stack at `:22` / `:52`). The live Mainland mixer is release `stage-notice`. Do not kill the encoder mid-report. A `jobs.py` / `run-poller.sh` change needs a poller restart before the running process adopts the new minutes; script edits are picked up on the next job run.

Midday 2026-10-02: `midday_report_current.wav` was written at 12:10 HST (~37 s) and passed the voice check; the 12:02 job skipped audio while the renderer was busy on `current_report`, though the text was already written, and this does not claim the 12:40 hurricane slot ran.

Report Instructor ~12:29 HST: the new `solar_desk` clip is written with Energy folded into that one clip, not a second file; the local Opus is still yesterday’s; Mainland stopped around 12:31 HST; the solar-desk job is not running; Report Instructor stopped and is not touching the radio; listeners stay up, so the radio is not being staged or restarted and no new clip goes on the air unless Alexander says so; the clip was written and, as of 12:29, was described as not on the station; inside the script, Delta is a BLE read (17% charge, 76 W solar, AC out 0), while River’s file says `source: cloud` and its lines are cloud-stamped 12:25 (59% charge, 139 W solar, 92 W AC out), so despite the BLE footer this is not a BLE report or a River field sample, and River still has no field BLE sample since ~05:45. Corrected ~12:46 HST: Report Instructor read the ML1 playlist and left the station alone. The 12:29 solar file is already in that list, so the next cycle plays it, and Report Instructor will not remove it. Desk `solar_desk_current.wav` is stamped 12:29. Two desk clips are newer than the queued copies and were not pushed: `hurricane_desk_current.wav` is 09:42 HST (about 42 seconds) while the queued file is stamped 21:15, and `news_update_current.wav` is 05:49 (about 25 minutes) while the queued file is stamped 04:49. Mainland ~12:48 HST confirmed the mismatch and is not copying the newer desk hurricane and news files onto ML1. The playlist is what the next cycle queues. 2026-10-02 ~12:54 HST: Alexander ordered listeners off this radio mix onto YouTube, with no video. The station was not stopped. These clips still render here. The stills path is not built, and the wiped ML2 video stack stays wiped. ~12:56 HST: Report Instructor keeps reports as audio and will not make a video version or touch the station. Cove keeps the public Radio page on the live mp3 until a stills target exists, and will not embed video.

### Big Island weather report sites (LIVE/VERIFIED ~03:42 HST)

Report Instructor promoted **Mountain View, Volcano, and Kailua-Kona** onto the Big Island weather map/report path. Formal change summary paths: `Media/Voice/scripts/voice_reports.py` (`zfp_temps`); `Weather/config/resources.yaml` (NDFD points); `Weather/reports/generator.py` (RWR Kona→Kailua-Kona PHKO); `Weather/config/report_counties.yaml`; and `Media/Voice/scripts/hawaiian_lexicon.py`. Smoke passed: `b_nws_weather` and `current_report` include all three. Previously documented gaps are unchanged.

**ZFP bands (desk-verified ~03:43 HST):** `zfp_temps` still reads Big Island East once, then speaks three places with different bands — Hilo **shore**, Mountain View **range** (shore-to-elevation span), Volcano **elev** (~4000 ft). Honolulu, Lihue, Kahului, and Kailua-Kona stay **shore**. Helpers `_shore` / `_elev` / `_zone_range` / `_band_temp` implement that. NDFD points add Mountain View, Volcano, and Kailua-Kona beside HNL/LIH/OGG/ITO; lexicon adds Volcano + Kailua-Kona diagnose names.

### Station lock and lead time

The station locks the playlist at `HH:29:59` and `HH:59:59`, then plays the half-hour chime and every current report. A file that arrives after that lock waits for the next cycle. Generation used to start at `:00` and `:30`, which was too late. The nine generating desks share one poller thread and one Kokoro lock, so they run one after another.

From [voice-timing.md](./voice-timing.md) (generated 2026-10-02 11:05 HST, 433 finished runs, nine desks at `:22` / `:52`): stack sum median **318 s** (5m18s), average **379 s** (6m19s), p90 **647 s** (10m47s). Lead from `:22:00` to the `:29:59` lock is **7 minutes 59 seconds**; `:52` has the same lead before `:59:59`. Median fits that window; summed p90 does not — `voice_timing_report` recommends moving `:22` / `:52` earlier. Older 01:07 HST pass (303 runs, ten desks including retired Energy at `:12` / `:42`) was median 376s / p90 889s against a 17m59s lead. News stays at `:36` (after the `:22` stack, before `:52`). Hurricane stays at 05:40, 09:40, 12:40, 16:40, and 20:40. The hourly chime stays at `:00` and `:30` and is a replay of prebuilt files, not a render.

Daypart roll-ups cannot be uploaded before their window opens, or the upload deletes the roll-up that is still on the air. Morning **09:02**, midday **12:02**, late **21:02**, late final **23:02**. Those first air on the following half hour. `voice_timing_report` runs at minute **5**. It is not a model. It rewrites [voice-timing.md](./voice-timing.md) from the automations log and `jobs.py`. The poller imports `jobs.py` once at start, so a schedule change needs a restart of `rr-rootserver-poller.service` as user `rootrecord`.

### Shared pipeline

`jobs.py` → `voice_reports.py` / `system_perf.py` → build MD → `write_md` (+ Archive) → `voice-render.sh` / `voice_generate` mode_stitch (Kokoro, single-flight) → `voice_deliver` (Telegram when `RR_VOICE_DELIVER=1`) → `radio_push` (default on; set `RR_RADIO_PUSH=0` to skip) → Discord `report_relay` every 300 s → `publish_report_pages` → site `/reports/<slug>`.

Personas (Kokoro): Ava `af_heart`, Bruce `am_echo`, Carly `af_nova`. All speeds 1.0. Output is 24 kHz, 16-bit, mono WAV under Database `Media/Audio/Voice/`.

`RR_VOICE_DELIVER=1` and `RR_TELEGRAM_DEST=council` are the defaults in `run-poller.sh`. A council post is a voice note and the measured report. Unchanged spoken text is not sent again. Flags are read when the poller starts. A script edit is picked up on the next run of that job. A new `jobs.py` entry is not, until the poller is started again.

Kokoro is single-flight through `voice-render.sh`. A busy render returns **75**. Render one slug at a time. The spaCy venv needs the symlink `cli/Templates` pointing at `cli/templates` or the import fails. Do not remove that symlink.

### Nine generating desks (:22 / :52)

| Job | Persona | Spoken label |
| --- | --- | --- |
| `system_perf` | Bruce | System |
| `nws_weather` | Ava | NWS |
| `remaining_tasks` | Bruce | Remaining tasks |
| `earthquake_report` | Carly | Earthquake |
| `kilauea_report` | Carly | Kilauea |
| `solar_desk` | Bruce | Energy and solar |
| `security_desk` | Carly | Security |
| `bandwidth_desk` | Carly | Bandwidth |
| `current_report` | Ava | Current |

`solar_desk` is the combined energy + solar product: EcoFlow packs, sun times, newest channel-1 still, and this hour’s camera look (`panel_look.observe` when the hour has no reading). The old `energy_report` job and `RR_VOICE_ENERGY` flag are gone from `jobs.py` / `run-poller.sh`; `b_energy_report` remains a one-release alias that forwards to `b_solar_desk`. Discord and the public Energy area keep only `solar-desk`.

Armed flags (defaults 1 in `run-poller.sh`): `RR_VOICE_SYSTEM_PERF`, `RR_VOICE_NWS`, `RR_VOICE_REMAINING`, `RR_VOICE_QUAKE` (+ `RR_GEOLOGY`), `RR_VOICE_KILAUEA`, `RR_VOICE_SOLAR`, `RR_VOICE_SECURITY`, `RR_VOICE_BANDWIDTH` (+ `RR_NET_SAMPLES`), `RR_VOICE_CURRENT`. Also armed: roll-ups (`RR_VOICE_ROLLUPS`), late final (`RR_VOICE_LATE_FINAL`), hurricane (`RR_VOICE_HURRICANE`), and desk uptime log (`RR_UPTIME_LOG`). The news `:36` job is on as of the Report Instructor's ~11:53 HST read (`RR_RADIO_NEWS=1`). Soft-on for soak (needs poller restart): `RR_VOICE_KILAUEA_IMAGE` (`voice_kilauea_image_check` every 900 s) — see below.

### System perf connectivity and host power mode (2026-10-02 ~02:15–02:33 HST)

`system_uptime_log` (every 60 s, `RR_UPTIME_LOG` default **1** in `run-poller.sh`) runs Pacific `System/scripts/uptime_log.py tick`. Live stamps only: heartbeat gaps and boot_id changes write Database `System/uptime/` (`uptime-events.jsonl`, `uptime-last.json`, `presence.json`, `offline-samples.jsonl`, `return-samples.jsonl`, `connectivity-daily.json`). Averages start from `recording_since` on the first live tick after the job armed — pre-recording / testing stamps are not offline samples. Bruce’s `system_perf` speaks last-online, uptime percent, average offline, and average expected return when samples exist (`connectivity_lines` → `uptime_log.sentences`).

Host power mode is logged read-only by new `System/scripts/power_profile.py` (performance / balanced / energy saver via `powerprofilesctl` or ACPI platform profile; it never sets a mode). Bank: Database `System/power-profile/` (`mode-last.json`, `mode-segments.jsonl`, `mode-use.json`). Each uptime tick calls `power_profile.note`; `system_perf` also samples and speaks “Host power mode is …”. Tests: `test_uptime_connectivity.py`, `test_power_profile.py`.

### Site traffic in bandwidth / current (2026-10-02 ~02:33 HST)

Mainland Home/Radio analytics are folded into Pacific spoken reports (schema **1.0.0**, no page JS). Pacific `Website/scripts/analytics_pull.py` mirrors ML2 `GET /api/analytics/daily` into Database `Logs/Website/analytics/daily/` (plus `analytics-last.json`; sample `daily/2026-10-02.json`). Voice `bandwidth_desk` and `current_report` speak measured site traffic: **api** / **home_proxy** / **radio**, with honest partial Home (`home_proxy` is telemetry Referer www only; full `home.pageviews` stay null until edge analytics). Job `analytics_pull` is gated `RR_ANALYTICS_PULL=1` at 900 s; **not** exported in `run-poller.sh`, so a normal start leaves it off until armed. Desks can still refresh a stale day file themselves when speaking. READMEs: Database `Logs/Website/analytics/README.md` and Pacific `Website/README.md` Analytics section.


### Kīlauea 15-min image check (2026-10-02 ~03:21 HST)

**LIVE on Pacific** (local; no commit). Report-side only — **not** in `LOCAL_DATA_POLL_JOBS` (forever-Pacific / ungated by exclusive ML2 data-poll, EcoFlow/cams-style).

| Piece | Detail |
| --- | --- |
| Job | `voice_kilauea_image_check` every **900 s** in `jobs.py` |
| Gate | `RR_VOICE_KILAUEA_IMAGE` — soft default `:-1` (on for soak) in `run-poller.sh` |
| Look | Pacific `Geology/scripts/kilauea_look.py` (Gemma; same stack as `panel_look`) |
| Voice | `voice_reports` `kilauea_image_check` (Carly) + `voice_deliver` title |
| Bank | Database `Cams/kilauea-look-last.json` + `lava-fountain-ref.jpg` |

Flow: USGS HVO still (prefer fresh Cams v3/v1/v2; else live GET) → Gemma look vs optional fountain ref → Carly: “Kilauea observation image was checked” + measured finding. Smoke (glow on V3 Halemaʻumaʻu): *Kilauea observation image was checked. Measured finding: glow at the vent…*

**Verified Cams bank / looker path (~03:31 HST):** ML2 `geology_kilauea_cams` takes USGS stills only (no vision on the mainland host), streams them home under the exclusive `RR_LOCAL_DATA_POLL=0` gate (the Pacific `geology_kilauea_cams` job remains in `LOCAL_DATA_POLL_JOBS` as a soft toggle), and wipes scratch after stream. Pacific receives `Geology/Volcanoes/Cams/v1cam_current.jpg`, `v2cam_current.jpg`, `v3cam_current.jpg`, and `cams_current.json`; the manifest records `photo_viewed` plus per-camera `fetched_at`, `bytes`, `sha`, `ok`, and `error`. Pacific archive-on-replace applies to any filename containing `_current`: `archive/YYYYMMDD/<stem>_<HHMMSS><ext>`; the live `_current` is always newest for LLM reads. Example: `Geology/Volcanoes/Cams/archive/20261002/v3cam_current_033046.jpg`. `kilauea_look` prefers `*_current` over `*-last`; `v3cam_current.jpg` was verified with `source_kind=current`. Looking/vision is Pacific-only; EcoFlow stays Pacific forever.

**Verified report blend (~03:33 HST):** Report Instructor confirmed that the Kīlauea spoken/written report states whether a still was viewed (**Y/N**) and, when viewed, what conditions looked like. The bank, paths, archive-on-replace, Pacific-only looking, and report blend are verified.

**Poller restart required** before the gate/job takes effect in the running process. Soft default is on for soak in `run-poller.sh`; until restart, treat as not yet adopted by the live poller.

### Post-boot voice / analytics check (Report Instructor, ~02:58 HST)

Measured after desk reboot into ML2 mode (poller active; `RR_LOCAL_DATA_POLL=0` still set).

| Artifact | mtime (HST) | Note |
| --- | --- | --- |
| Voice WAV `nws` | 02:24 | pre-reboot |
| Voice WAV `solar_desk` | 02:28 | pre-reboot |
| Voice WAV `bandwidth` | 02:31 | pre-reboot |
| `current_report` md | 02:33 | pre-reboot |
| Analytics `as_of` | 02:28:35 | daily file present |
| Automations log | 02:58 | fresh; no recent `voice_` / `report_` failures |

**No new voice cycle since boot yet.** Live desk schedule remains **`:22` / `:52`** (nine desks; was `:12` / `:42` before ~01:57). Expect the next `:22` / `:52` stack to refresh spoken files from Database. Do not treat pre-reboot WAVs as post-boot proof.

### ML2 live banks — stale-desk notes cleared (~03:23 HST)

`RR_LOCAL_DATA_POLL=0` (exclusive gate; overnight ML2-on). ML2 **LIVE / stream-verified** collectors: **geology + `weather_us_states` + `weather_hawaii` + `radio_rss`** (hurricanes via `weather_hawaii`). SSH stream lands in the same Pacific Database `path_rel` tree desks/LLMs read. Prior “awaiting stream-verify / NWS HI / hurricane / news hour go stale” notes are **cleared**. Not a full poller move — Discord/Telegram pollers still scaffold. Detail: [US-Mainland-Two](../15-Domains-and-External-Systems/US-Mainland-Two.md).

| Desk / product | Bank path | Status |
| --- | --- | --- |
| Earthquake / Kīlauea | ML2→Pacific geology banks | Refresh OK |
| NWS Hawaiʻi (`nws_weather`) | ML2 `weather_hawaii` → Pacific `Weather/Hawai'i/` (sample `ml2-collector-status.json` ok) | **Unstuck** — stream verified |
| Hurricane | via `weather_hawaii` → Pacific reports/hurricane tracks | **Unstuck** — tracks fresh |
| Radio news hour | ML2 `radio_rss` → Pacific `Media/RadioRss/` (health/queue ok) | **Unstuck** — stream verified |
| Bandwidth / current analytics | ML2 `/api/analytics/*` | Pull still fine |

Report Instructor: Pacific local collectors stay gated while `RR_LOCAL_DATA_POLL=0`; banks fill from ML2→Pacific path_rel. Do not treat gated Pacific jobs as the live fill path.

### Always on (hard-enabled in jobs.py)

| Job | Schedule (HST) |
| --- | --- |
| `worklog_scan` | every 90 s |
| `discord_report_relay` | every 300 s |
| `voice_timing_report` | :05 |
| `reports_daily_roll_up` | 18:30 |
| `reports_weekly_archive` | 19:00 |
| `discord_report_8h` | 00:00, 08:00, 16:00 |
| `discord_report_24h` | 12:00 |

### OFF / gated (not exported in run-poller.sh, or hard-off)

| Flag / job | Report |
| --- | --- |
| `RR_ANALYTICS_PULL` | `analytics_pull` — mirror ML2 daily JSON → `Logs/Website/analytics/` every 900 s. Flag **not** in `run-poller.sh`; off until armed. |
| `RR_VOICE_HOURLY_CHIME` | :00 and :30 chimes. Job exists in `jobs.py`. Flag is **not** in `run-poller.sh`, so a normal start leaves it off. Station chime is separate. |
| `RR_AI_REPORT` | `ai_processing_report_hourly` |
| `RR_AI_USAGE` | `ai_usage_report` |
| `RR_TEMPLATE_REPORTS` | `template_reports_daily` (18:40) |
| `RR_HURRICANE_RADIO` | `media_hurricane_radio` |
| `RR_REPORT_BOARD` | `reports_board_catchup` |
| `RR_NOTE_DRAFT` | `note_work_draft` |
| `RR_BRUCE_STATS` | `bruce_stats_posts` |
| (no job) | `official_weather` — Discord route exists; **not** in `jobs.py` |
| (no job) | `boot_brief` — Discord route exists; **not** in `jobs.py` |

Speakers stay off. `Media/Playback` is dry-run unless `RR_PLAYBACK=1` and `--play`.

Scripts proposed only (README gates; not in `jobs.py`): News (hawaii/state/global), economy_brief, cloud_narrative. CloudNarrative README names a `cloud_narrative_dry_run` jobs.py entry; that id is absent.

### Known gaps (code wins)

1. Hourly chime gate is not in `run-poller.sh`.
2. `official_weather` / `boot_brief`: Discord `report-channels.json` routes yes; `jobs.py` entries no.
3. `current_report`: generated at :22/:52; missing from `Communications/Discord/config/report-channels.json` (site `publish_report_pages.py` still lists it in AREAS and has a separate CURRENT_MD path).
4. CloudNarrative README claims a `jobs.py` entry — absent.
5. `system_perf.py` docstring still says `only_at_minutes=[6]`; jobs schedule is `[22, 52]`.
6. `ai_processing_report.py` file header says out under Database `Logs/AI/Reports/`; live `OUT_DIR` default is ecosystem `test-reports/AI-Processing/`. `template_fill.py` header and jobs description say Database `Reports/Generated/`; live `OUT_DIR` default is ecosystem `test-reports/Templates/`.
7. Older ops “what stays off” lists that still name roll-ups, late-final, or hurricane as off are history. `run-poller.sh` arms them.

### Local status clips (desk speakers only)

Each of the nine desks has four local status lines, already rendered, played on the desk with `aplay`. `RR_VOICE_STATUS=0` skips them. They are **not** on the radio. Clips live under Database `Media/Audio/Voice/Clips/{Ava,Bruce,Carly}/`.

| Moment | Line | When |
| --- | --- | --- |
| Starting | “<Label> report is about to generate” | before render |
| Transit | “<Label> report has been generated and is in transit” | when the send starts |
| Failed | “<Label> report was generated but failed to send” | if the send fails |
| Sent | “<Label> report was sent successfully” | only after Mainland One has the file (`ffprobe` duration ≥ 0.2 s, then `mv`) |
| Stack closer | Ava: “All reports have been sent successfully. Heavy work may resume.” | once per `:22` / `:52` cycle after all nine desks have a Mainland receipt |

After each successful send, `status_cue.note_sent` records the desk in Database `Reports/Voice/stack-send.json` under that cycle key (`YYYY-MM-DDTHH:22` or `:52`; a run past the hour stays on the prior `:52`). When the set of nine is complete and the closer has not yet played this cycle, it plays `Clips/Ava/stack_all_sent.wav` once and marks `announced`. A skipped send, including a daypart outside its window, is not a failure and does not play the failure line. Code: `Media/Voice/scripts/status_cue.py`. Test: `test_status_stack.py`.

### Staged on-air cues (radio)

Each of the nine also has two staged lines, already rendered: “<Label> report has been staged for the hour” and “<Label> report has been staged for the half hour.” After a successful radio push, `radio_push.stage_on_air` encodes that wav to opus, copies it to Mainland One at `/home/ubuntu/rootrecord-radio/audio/cues/{report}-hour.opus` or `{report}-half.opus`, and writes a JSON note in `state/stage`. The next slot is this hour’s `:30` when the minute is under 30, otherwise the next hour’s `:00`. The station plays the cue after whatever report is speaking, or immediately if nothing is speaking. Music ducks while it plays.

The time mark on that cue is the **short notification sound only**, `Media/Voice/assets/deep-ui-chime.mp3` (~2 s), uploaded as `audio/cues/notify.opus`. The station plays the ding first, then the spoken staged line. It does **not** play the full spoken clock (“Report generated at…”, Mountain, Eastern, UTC). Those full chimes stay on the half-hour cycle as `hour-HH-MM.opus`.

### Generation clock (not air slot)

Each report says the Hawaii hour and minute when its text is built, not the air slot. “Report generated at twelve fourteen p.m.” means the text started then. Seconds are not spoken. The current report, remaining tasks, and the morning, midday, and late roll-ups used to snap to `:00`, `:30`, or 09:00 / 12:00 / 21:00. They no longer do. A morning report that starts at 09:02 says nine oh two a.m. The written heading uses the same timestamp. The half-hour station chime still announces the air time. The report announces when it was generated.

### Percent change lines

Numbers in the reports get a percent change when an earlier reading exists. Averages and raw counts both use percent. Periods: yesterday (24 h ± 6 h), last week (7 d ± 36 h), last month (30 d ± 3 d). Speech: “CPU up 8 percent from yesterday, down 2 percent from last week.” Flat is “unchanged.” A missing period is omitted. A zero baseline is omitted. If no period can be compared, the report does not mention a change. History appends to Database `Reports/Comparisons/metrics.jsonl`. Battery SoC, solar watts, and output watts can also use `Energy/samples/read-delta2` and `read-river2pro` files (back to 2026-09-29), so a day comparison can appear immediately; week and month stay silent until a reading falls in those windows. CPU, memory, disk, temperature, battery, GPU, NPU, alert counts, forecast highs and lows, earthquake M2.5 counts, security listener and sign-in counts, bandwidth totals, open work orders, next-hour task count, and hurricane distance and wind use the ledger, so those lines appear only after enough history. Ages, uptime, and the clock are not compared. Code: `Media/Voice/scripts/compare_span.py`, via `say_change` in `voice_reports.py` and directly from `system_perf.py`. Tests: `test_compare_span.py`.

## Hawaii, and host temperature

`Hawaii` and `Hawaiian` are spoken as those English words. The old syllable spelling is not used. Other place names still use the English respell in `hawaiian_lexicon.py` (Kīlauea is one token, `keelah-wayuh`; Mauna Loa is `mownah-lowah`; Maui is `mao wee`; Honolulu stays the plain English name). News hour (`Media/RadioRss/scripts/news_hour.py`) runs the same fold + pronounce path before Kokoro. A comma plus a USPS state code is spoken as the state name.

Alexander rule: **no sports in reports.** Sports was entering `news_update` through RadioRss general feeds (Star-Advertiser / Al Jazeera / BBC sports URLs, NFL, and similar). Pacific `Media/RadioRss` now drops sports from **every** feed: global `sports_patterns` in `config/policy.yaml`, `stories.sports()` drop on normalize, compose skip in `pipeline.py`, and a filter in `news_hour.py` before desks. `test_rss_radio.py` covers sports drop and transportation keep (passed). Voice desks, Discord report channels, and Website report pages have no dedicated sports sections — the filter is at ingest, not a desk layout change.

### News hour shape (as of 2026-10-02 ~04:30 HST)

The local build produced a **~22.7-minute** `news_update` sample, within the twenty-to-twenty-five-minute target. The standing 30-minute cycle plays all local reports first, longest first among locals, then gives news the remainder and cuts news at the boundary before an unplayed local report; the ML1 mixer is on the air as of the 12:02 HST `rr-radio-station` restart (live `stream.js` has locals first). `stories.py` now uses word-edge matching for `nfl`/`nba`/`mlb`/`sports` and expanded leagues, avoiding false hits such as conflict, influenza, and sportswear; 21 sports JSON items and archived SQLite rows were purged. Smoke found 0 sports in speak text and tests passed. Ava, Bruce, and Carly share airtime roughly evenly through `balance_personas` in `Media/RadioRss/scripts/news_hour.py`. Mix: markets, defence, SpaceX, Hawaii, chips/big tech, world, U.S. mainland weather, centrist politics, science, universities, and also; policy raises defence/politics budgets and feeds add `doj_news` and `defense_gov`. Solar remains separate at 5–7 minutes. The landing includes the `news_hour.py` docstring, `test_rss_radio.py`, and the `jobs.py` 2400-second `radio_news_update` timeout/comment. At the Report Instructor's ~11:53 HST read, `RR_RADIO_NEWS=1` and the news job is on; the soft poller restart note is only for that timeout. The soft data-poll gate and EcoFlow remain untouched. Living on-air note: [radio station](./2026-10-01-radio-station.md). Spoken-report wording twin: [Voice-Reports-G3](../10-AI-and-Agent-Runtime/Voice-Reports-G3.md).

2026-10-02 ~13:01 HST: the date is said once at the beginning. `news_hour.py` opens with "RootRecord news update for {month} {day}, {year}" and does not say the date on every story. `pipeline.py` says Published once on the cluster opener. That edit is on the Pacific desk tree and the ML2 vendor copy. The pacific worktree `news_hour.py` still dates every story, and that copy is not what gets spoken. No new news audio was rendered. An hour-long news block is an idea only; the cycle stays 30 minutes.

A bare `degrees` after a number is still spoken as Fahrenheit, because the weather numbers are Fahrenheit. The system report says `degrees Celsius` on purpose. The sensor is `acpitz`, in Celsius. The written row is `°C`.

## Energy speech

Readings older than 30 minutes are "out of range." A last reading of 5 percent or less that is older than 30 minutes is "discharged and powered off," and the report does not list that pack's watts. A current channel 1 still is not given an age. An older still is "N minutes old."

Generator and transfer use watts, and the same rules are in the voice, the BLE charge source, and the load categories:

| Reading | Meaning |
| --- | --- |
| Delta 2 AC in greater than 550 W | Generator. 550 itself is not. |
| River 2 Pro AC in greater than 300 W | Generator, unless the next row matches. 300 itself is not. |
| Delta AC out matches River AC in | Transfer from the Delta to the River, not a generator on the River. Both watts at least 20, and the gap no larger than 40 W or 12 percent of the larger number. |
| A stale file that says 0 W | Not a generator. |

## Channel 1 solar look

Once per clock hour, the `:22` `solar_desk` run asks `Security/Cameras/panel_look.py` and the local vision model `gemma4:e4b` about the newest channel 1 still, and only when that hour has no reading yet. The `:52` run reuses that sentence. The cache is Database `Energy/vision/ch1-look-last.json`. A failed look is not cached, so the next solar desk can try again. Bruce's combined solar desk speaks the last stored sentence, names its age when it is from an earlier hour, and attaches the still. It does not start a second look.

The model names the weather (rain, fog, overcast, clear, dark) and the tilt. Left side up is the morning position. Flat is the day position. Right side up is the evening position. Left and right are as channel 1 sees the array.

An infrared still is grayscale. The color span of that frame sits near 2, and a color frame sits above 11. A span under 6 is night, so weather is dark. The gray look is the infrared illuminator. It is not overcast. The tilt reading stays with the model. A color look from earlier in the same hour is replaced once the newest still is infrared.

| Part of the day | From the sun file | What is correct |
| --- | --- | --- |
| Morning | Two hours before sunrise through one hour after | Left side up, or flat. Right side up asks for a person. |
| Day | After that, until one hour before sunset | Flat. Any tilt asks for a person. In the later half of that window, left side up is fine when combined solar input is 20 W or less on a reading newer than 30 minutes. That line is "Solar staged for sunrise." |
| Evening | One hour before sunset through 45 minutes after | Right side up. Anything else asks for a person. Left side up with that same low solar input reads "Solar staged for sunrise." |
| Overnight | The rest of the night | Left side up, or flat. Right side up asks for a person. |

Morning tilt helps early capture and is not required. Overnight left tilt is the correct prep. The warning says a person is needed. Nothing moves the panels. Four corner actuators for this tilt are a desired upgrade, not a build: [four corner actuators](../09-Desired-Upgrades/2026-09-30-four-corner-sun-tilt-actuators.md).

## Spoken clock, change lines, and cues

See **Generation clock**, **Percent change lines**, **Local status clips**, and **Staged on-air cues** under Current as of 2026-10-02 ~02:18 HST above. This section is kept so older links land somewhere: generation clock (not air slot); `compare_span.py` percent lines; four desk `aplay` status phases plus Ava stack closer; two staged on-air phases with `notify.opus` first.

## Hourly chimes

Forty-eight files, `Database/Media/Audio/Voice/Chimes/hour-00-00.wav` through `hour-23-30.wav`, one for every hour and half hour. Each one starts with `Media/Voice/assets/deep-ui-chime.mp3`, then the voice. Midnight and 12:30 a.m. are Ava, 1:00 and 1:30 a.m. are Bruce, 2:00 and 2:30 a.m. are Carly, then it repeats. Playback copies the file. It does not call Kokoro.

Those desk files are WAV. The Mainland station library is Opus, and that bed is playing. A chime on the station is `hour-HH-MM.opus` at 48 kbps. A report there is `<report>_current.opus` at 24 kbps mono. Music there is `.opus` at 96 kbps and arrives with the git pull. Hawaii still renders a WAV, then `Media/Voice/scripts/radio_push.py` encodes that one report to Opus and replaces it on `/home/ubuntu/rootrecord-radio` over `ssh ml1`. Only the current daypart rollup is kept: morning 09:00–12:00, midday 12:00–21:00, late 21:00–09:00. The station deletes the other two daypart files when the current one arrives. The public mix stays `https://radio.rootrecord.cloud/radio/live.mp3`. Earthquake and hurricane reports stay Pacific poller jobs. The Pacific chime job below is separate from the station chime.

The sentence is the Hawaii time, then Mountain Daylight Time (four hours ahead), Eastern time (six hours ahead), and UTC (ten hours ahead). The minute is the same in each zone. Those offsets match daylight time. They are wrong after US standard time begins in November, and the files have to be rendered again.

The job is `:00` and `:30`. It stays off until `RR_VOICE_HOURLY_CHIME=1` is in the poller environment at start. Rebuild with:

```bash
PACIFIC="/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server"
"$PACIFIC/System/scripts/plumbing/single-flight.sh" run "voice:chimes:batch" -- \
  nice -n 10 "$PACIFIC/Media/Voice/.venv/bin/python" \
  "$PACIFIC/Media/Voice/scripts/hourly_chimes.py" --render
```
