# Pacific hour

## Current — 2026-10-03 ~08:26 HST

Read this section. The sections after “historical grid” are the 2026-10-02 sitting. They still name separate `voice_*` minutes and say schedule JSON owns the clock. That is not what the 08:18 HST process is doing.

The live poller is `rr-rootserver-poller.service`, up since 08:18 HST. Log: `scheduler MODE=jobs.py exact_time=34`. It fires `Automations/scripts/jobs.py` `EXACT_TIME`. `RR_LOCAL_DATA_POLL=0` remains the systemd drop-in. Do not restart the poller to publish this page. The 08:35 news and 08:36 batch had not fired yet when this was written.

### The three jobs

They share one Kokoro lock: `Media/Voice/scripts/voice-render.sh` runs `voice_generate.py` through `System/scripts/plumbing/single-flight.sh`. The lock refuses with exit 75. It does not queue. The loser does not get a WAV.

| Clock | id | Script | Notes |
| --- | --- | --- | --- |
| :35:00 | `news_cycle` | `Media/News/scripts/run_news_cycle.py` | Priority 1. Enabled. Timeout 1800s. Job env `RR_RADIO_PUSH=0`. Banks `news_update_current.wav`. Does not push. |
| :36:00 | `voice_hour_batch` | `Media/Voice/scripts/generate_hour_reports.py` | Priority 0. Enabled. `nice -n 0`. Timeout 2400s. Job env `RR_VOICE_DELIVER=0`, `RR_VOICE_STATUS=0`, `RR_HOUR_BATCH_PUSH=1`. |
| :55:00 | `radio_push_hour` | `Media/Voice/scripts/radio_push.py --all` | Priority 1. Catch-up. If the WAVs are already gone, result is `mode: noop`. |

`jobs.py` `voice_hour_batch_at_minute()` returns `RR_VOICE_HOUR_BASE_MINUTE` only. Default 36. `Timing/hour_batch_schedule.json` is written after a batch as a record. A suggested minute in that file does not change the next fire.

### What the batch runs, in order

`generate_hour_reports.py` `HOUR_REPORTS`:

| Order | Report | Voice |
| --- | --- | --- |
| 1 | `boot_brief` | Ava |
| 2 | `nws_weather` | Ava |
| 3 | `current_report` | Ava |
| 4 | `solar_desk` | Bruce |
| 5 | `remaining_tasks` | Bruce |
| 6 | `system_perf` | Bruce |
| 7 | `custom_msg` | Bruce |
| 8 | `earthquake_report` | Carly |
| 9 | `hurricane_desk` | Carly |
| 10 | `kilauea_image_check` | Carly |
| 11 | `kilauea_report` | Carly |
| 12 | `security_desk` | Carly |
| 13 | `bandwidth_desk` | Carly |

Then `news_update` if `news_update_current.wav` is from this cycle. Then one `report_current` WAV and ogg. Then `radio_push.push_hour_batch()` to ML1 as `report_current.opus`. Then delete `.wav` / `.txt` / `.tx` under `Media/Audio/Voice/` (keeps `custom_msg_current.txt`). Then rename this run’s `*_current.ogg` and zip them to `Media/Audio/Voice/Archive/audio_reports_YYYYMMDDTHHMMSS.zip`. Then write Timing.

A desk WAV counts only if its mtime is after this process started. The file `kilauea_image_check_current.wav` stamped 08:17 HST is a leftover from the standalone image check and is not this batch.

### News and the lock

`news_cycle` catch-up is :35 through :39, once a minute on the :00 second, until that hour’s done mark is set. If the process exits with no fresh WAV, the mark is removed and catch-up can try again.

`voice_hour_batch` waits up to 1700 seconds (`RR_HOUR_NEWS_TTS_WAIT_SEC`) for `news_cycle` to exit before the first desk, and again before each later desk if news is still running. A desk that still gets exit 75 retries up to four times, 20 seconds apart. News TTS retries a busy lock up to eight times, 15 seconds apart, then fails that lane and does not bank a WAV.

A news WAV is this cycle when it is at or after the latest :35 and not older than two hours. A finish just after the next :00 still belongs to the hour the job started. The done key uses that start hour. It does not mark the next hour done.

### Files

| Path | Role |
| --- | --- |
| `2 - RootRecord-Database/Media/Audio/Voice/news_update_current.wav` | :35 bank. Folded in, then deleted after a successful push. |
| `2 - RootRecord-Database/Media/Audio/Voice/report_current.wav` | Combined desks + news. Deleted after a successful push. |
| `2 - RootRecord-Database/Media/Audio/Voice/generate_hour_reports_last.json` | Last batch summary. |
| `2 - RootRecord-Database/Media/Audio/Voice/Timing/hour_batch_schedule.json` | Record of the last finish. `at_minute` is pinned to 36 when the batch writes it. |
| `2 - RootRecord-Database/Media/Audio/Voice/Timing/hour_batch_averages.json` | Wall-time averages. Suggestion only. |
| `2 - RootRecord-Database/Media/Audio/Voice/Timing/hour_batch_history.jsonl` | One JSON line per full batch. |
| `2 - RootRecord-Database/Media/Audio/Voice/Archive/audio_reports_*.zip` | Ogg archive after a successful push. |
| `2 - RootRecord-Database/Logs/Automations/hour_workflow_done.json` | `news_cycle\|date\|HH`, `voice_hour_batch\|date\|HH`, `radio_push_hour\|date\|HH`. Survives a poller restart. |
| `2 - RootRecord-Database/Logs/Automations/automations_current.log` | Poller log. |

### Poller rules that keep :35 and :36 from being skipped

Code is `Automations/scripts/rootserver_poller.py`.

- Hour workflow ids: `news_cycle`, `voice_hour_batch`, `radio_push_hour`. On a tick where one of them is due, these are deferred to the next tick: `security_camera_frame_grab`, `delta2_read`, `river2pro_read`, `hawaii_to_ml2`, `geology_kilauea_cams`, `energy_consolidate_minutes`, `energy_consolidate_hours`, `system_consolidate_minutes`, `system_consolidate_hours`.
- `voice_hour_batch` catch-up is :36–:54. `radio_push_hour` catch-up is :55–:59. Both only on second 0, and only if that hour is not already marked done.
- A watchdog in the same window starts `voice_hour_batch` if the exact second was missed and the hour is not marked done.
- “Already running” is a live `python*` argv containing `generate_hour_reports.py`. A shell or sandbox line that only mentions the path does not count. That false match used to mark the hour done and skip the real fire.
- If the batch process exits and `hour_batch_schedule.json` was not written during that run, the voice done mark is cleared so :36–:54 can try again.
- A schedule stamp seeds “this hour already ran” only when its minute is 36 or later. A finish at :05 belongs to the previous hour.
- A job timeout kills the process group (`start_new_session` plus `killpg`), not only the `bash -lc` parent. Otherwise Kokoro kept the lock after the shell was killed.
- `voice_kilauea_image_check` is enabled (`RR_VOICE_KILAUEA_IMAGE=1`) every 15 minutes at second 30. It is skipped from :30 through :54, and whenever `generate_hour_reports.py` is already running.
- Chimes at :00 and :30 (`voice_hourly_chime`) play a prebuilt file. They do not call Kokoro.

### Env on the 08:18 process

`RR_VOICE_HOUR_BASE_MINUTE=36`, `RR_VOICE_HOUR_BATCH=1`, `RR_NEWS_CYCLE=1`, `RR_RADIO_PUSH=1`, `RR_VOICE_HOURLY_CHIME=1`, `RR_VOICE_KILAUEA_IMAGE=1`, `RR_VOICE_DELIVER=1` for jobs that do not override it. The hour batch itself sets `RR_VOICE_DELIVER=0`. News sets `RR_RADIO_PUSH=0`.

`run-poller.sh` is what exports those defaults. `jobs.py` is imported once at poller start. A change to `jobs.py` or `rootserver_poller.py` is not in the running process until the next start. A change to `generate_hour_reports.py` or `run_news_cycle.py` is read when that job starts.

### Measured

2026-10-03 07:51:16 HST, manual/catch-up batch, not the :36 clock: 13 desks, 0 failed, wall 470.6 seconds, remote push `report_current.opus` 1475768 bytes, archive `audio_reports_20261003T075116.zip`. Combined `"news": false`. `hour_batch_schedule.json` stayed `at_minute` 36. That run is not proof that :35 news folded in. The 08:35 / 08:36 clock fire had not happened when this page was written.

### Code

| File | What changed for this lane |
| --- | --- |
| `Automations/scripts/jobs.py` | `news_cycle` :35 enabled priority 1. `voice_hour_batch` :36 enabled priority 0, `nice -n 0`, timeout 2400. `radio_push_hour` :55. Start minute is the env base only. |
| `Automations/scripts/rootserver_poller.py` | Hour lane first, stack defer, catch-up windows, persisted done marks, python-only “already running” check, process-group kill on timeout, Kīlauea voice skip :30–:54. |
| `Automations/scripts/poller/run-poller.sh` | Defaults: base minute 36, hour batch on, news cycle on, radio push on. |
| `Media/Voice/scripts/generate_hour_reports.py` | Wait for news, hold before each desk, reject a WAV from before this process, stitch, push, cleanup, archive, pin the written schedule minute to 36. |
| `Media/News/scripts/run_news_cycle.py` | :35 entry. Push stays off. |
| `Media/News/radiorss/scripts/news_hour.py` | Lane TTS retries a busy Kokoro lock. |
| `Media/Voice/scripts/radio_push.py` | `--all` with no local WAVs returns `noop`. |

## Written 2026-10-02 ~21:52 HST — historical grid

**What that sitting recorded:** `jobs.py` `EXACT_TIME`, and a copy in `schedules/pacific.json`.  
**Poller then:** not started from that sitting. `rr-rootserver-poller.service` was enabled and inactive. That is no longer the process state. The 08:18 HST process above is the live one. The 2026-10-02 note that schedule JSON owns the clock is not what the 08:18 process logged.

The working grid Alexander has open is `Desktop/Manual Audit Documentation/New Hourly Sequence.txt`. If that file and this page disagree, `jobs.py` and `pacific.json` are the ones the poller reads.

## How a reboot runs — 2026-10-02 note

The next paragraph says the poller uses schedule JSON instead of `jobs.py`. The 08:18 HST process logged `MODE=jobs.py`. Trust the current section at the top.

`run-poller.sh` does not wait. Camera frames, host stats, GitHub sync, and the EcoFlow leapfrog start as soon as the process is up. AI reports (`ai_processing_report_hourly`, `ai_usage_report`, `cloud_narrative_merged`, `cloud_narrative_kilauea`, `cursor_fallback`) are not replayed if boot misses their minute. They run the next time the clock reaches their slot. Night sleep defaults off, so a running poller does not skip jobs.

The poller then uses schedule JSON, not the `at_minute` lines in `jobs.py`, because `pacific.json` is version 1 and has entries. Both the global flag and `pacific.json` are armed and not disconnected. A Root Monitor Save writes JSON only and forces armed off. This sitting did not use that Save path.

Enabled flags in the JSON match `run-poller.sh` defaults. The systemd drop-in still sets `RR_LOCAL_DATA_POLL=0` before the script. Voice desks that render a WAV set `RR_RADIO_PUSH=0` on that job so they do not SSH by themselves.

If boot finishes a few seconds after the minute, one-shots already due in that minute still run once. The every-5s and every-10s stacks do not replay.

## The hour — 2026-10-02 grid, not the live voice lane

The repeating stack below is still the shape of the every-5s / every-10s work. The voice sentences in this section are the 2026-10-02 grid. The live voice lane is the 2026-10-03 section at the top.

**:00–:29** is only the repeating stack, plus the hour chime at **:00:00**.

| Every | Phase | Job |
| --- | --- | --- |
| 5s | second 0, 5, 10… | `sys_stats_cycle`, `github_sync_all` |
| 10s | second 0, 10, 20, 30, 40, 50 | `delta2_read`, `security_camera_frame_grab` |
| 10s | second 5, 15, 25, 35, 45, 55 | `river2pro_read` |

Delta 2 and River 2 Pro leapfrog. One battery per 5-second slot. Camera frames are the whole hour, on the same seconds as Delta 2.

`voice_hourly_chime` is also at **:30:00**. The script plays only when the minute is 0 or 30. `RR_VOICE_HOURLY_CHIME` now defaults to 1 in `run-poller.sh`.

Text and voice **generation** are staged to finish by **:55**. **:55:00** is `radio_push_hour`: `radio_push.py --all` encodes the finished hour-desk WAVs and SCPs that set to ML1 in one send. Speakers stay off. A Telegram voice note still depends on `RR_VOICE_DELIVER` (default 1). The Mainland mixer was not edited. It still locks the playlist at **:29:59** and **:59:59**.

`system_net_sample` at **:31:00** stores one interface counter snapshot. The hour and day figures are `rx`+`tx` since the earlier snapshot. They are not an all-time sum.

`reports_weekly_archive` runs only at **00:30:30**. Noon 30:30 does not run it.

`energy_sun_times` and `geology_collect` are off this hour. ML2's `geology` collector already owns the quake/HVO fetch. Sun times is a row on the ML2 catalog with no clock and no collector script. The ML2 schedule stays disarmed. EcoFlow reads stay on Pacific.

Morning, midday, and late CloudNarrative, and `discord_report_8h`, are gone. `cloud_narrative_merged` and `cloud_narrative_kilauea` are still on the grid and still gated off.

## On after a reboot

Boot, in priority order: `self_terminal`, `cloudflare_tunnel`, `github_setup_remotes`, `ollama_warmup`, `flm_npu_warmup`, `council_relay`, `security_camera_server`, `security_timelapse_catchup`, `weather_poller`, `network_globe_hawaii`. Then once: `ecoflow_read_boot`.

| Clock | Job |
| --- | --- |
| :00:00 and :30:00 | `voice_hourly_chime` |
| :30:00 | `automations_log_hourly_archive` |
| :30:05 | `heartbeat` |
| :30:10 | `system_uptime_log` |
| :30:15 | `ensure_tunnel_online` |
| :31:00 | `system_net_sample` |
| :32:50 | `energy_moon_phase` |
| :33:25 | `ml2_datapack_pickup` |
| :46:05 | `voice_system_perf` |
| :46:50 | `voice_nws_weather` |
| :47:40 | `voice_remaining_tasks` |
| :48:15 | `voice_earthquake_report` |
| :49:00 | `voice_kilauea_report` |
| :49:45 | `voice_solar_desk` |
| :50:50 | `voice_security_desk` |
| :51:25 | `voice_bandwidth_desk` |
| :53:30 | `voice_hurricane_desk` |
| :54:15 | `voice_kilauea_image_check` |
| :55:00 | `radio_push_hour` |
| :55:25 | `status_snapshot` |
| :55:30 | `live_picture` |
| :55:35 | `radio_rss_poll` |
| :55:40 | `radio_news_update` |
| 00:30:30 only | `reports_weekly_archive` |
| :59:55 | `discord_report_relay`, `reports_daily_roll_up`, `voice_timing_report`, `worklog_scan`, `service_supervisor`, `security_timelapse_hourly_compile`, `security_timelapse_daily_render` |

`radio_news_update` is about 11 minutes and does not fit before the text block, so it sits at **:55:40**, after the send.

## Placed, still off

These have a clock and will not run. Their `RR_*` flag still defaults to 0, or the job is hardcoded off (`voice_current_report`).

| Clock | Job |
| --- | --- |
| :33:35 | `geology_kilauea_cams` |
| :33:40 | `geology_kilauea_public_draft` |
| :33:45 | `ai_processing_report_hourly` |
| :35:55 | `ai_usage_report` |
| :37:05 | `template_reports_event` |
| :37:45 | `template_reports_worklog` |
| :38:25 | `template_reports_checkpoint` |
| :39:05 | `template_reports_workorder` |
| :39:45 | `cloud_narrative_merged` |
| :40:25 | `cloud_narrative_kilauea` |
| :41:05 | `economy_brief` |
| :41:45 | `cursor_fallback` |
| :44:55 | `api_prices` |
| :52:05 | `voice_current_report` |
| :55:05 | `kilauea_draft_count` |
| :55:10 | `earthquake_discord_post` |
| :55:15 | `council_quake_telegram` |
| :55:20 | `analytics_pull` |
| :55:45 | `media_hurricane_radio` |
| :59:55 | `note_work_draft`, `reports_pipeline_tick`, `reports_board_catchup`, `bruce_stats_posts`, `adsense_eod`, `admob_eod`, `overnight_relay`, `discord_report_24h`, `weather_retention`, `log_retention`, `path_index`, `weather_us_states`, `smart_devices_collect`, `weather_radar_zip`, `country_location_pollers`, `stripe_poll`, `vercel_builds`, `discord_poller`, `communications_slack`, `system_python_drop`, `council_health`, `inbox_drain`, `public_health`, `energy_river_car_drive` |

## Handoff — 2026-10-02 ~21:52 HST — hour grid → Library

Superseded 2026-10-03. The current section at the top of this file is the live hour. The bullets below are that night’s sitting only.

### Confirmed facts
- Recurring work is `EXACT_TIME`. That night this page said schedule JSON is what a running poller fires. The 08:18 HST process logged `MODE=jobs.py`.
- The poller was not started. The unit is enabled and inactive. That was true for that sitting. It is not the 2026-10-03 process state.
- 8-hour CloudNarrative and `discord_report_8h` are not on the hour.

### Pages updated
- `Documentation/01-Operations/2026-10-02-hourly-sequence.md` (this page)
- `Documentation/01-Operations/HANDOFF.md`
- `Documentation/01-Operations/2026-10-01-radio-station.md`
- `Documentation/01-Operations/voice-timing.md`
- `Documentation/15-Domains-and-External-Systems/US-Mainland-Two.md`
- Pacific `Energy/README.md` sun-times row
- Documenter `CONTEXT/WHERE-TO-WRITE.md`

### Evidence
- `Automations/scripts/jobs.py` `EXACT_TIME`
- `schedules/pacific.json` armed, 48 enabled entries
- `run-poller.sh` start window and `RR_*` defaults
- Due-job check without starting the poller: `:00:00` includes the chime and Delta 2; `:00:05` is River 2 Pro; `:31:00` is `system_net_sample`; `00:30:30` includes the weekly archive and `12:30:30` does not; `:55:00` includes `radio_push_hour`

### Still open
- AI, template, CloudNarrative, economy, and `voice_current_report` stay off until their flags are turned on.
- Sun times has no ML2 clock and no ML2 script.
- The mixer lock times were not changed.

### Explicitly historical
- Voice desks at minute 45, news at minute 8, and the 17:07 voice-timing schedule table.
- `energy_sun_times` as an `EVERY_HOUR` Pacific job.

### Next recommended action
- Reboot at the top of the hour if that is still the start. Do not start the poller from an agent seat unless Alexander says to.
