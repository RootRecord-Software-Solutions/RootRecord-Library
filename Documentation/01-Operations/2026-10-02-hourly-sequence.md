# Pacific hour — 2026-10-02

**Written:** 2026-10-02 ~21:52 HST  
**What fires:** `jobs.py` `EXACT_TIME`, copied into `2 - RootRecord-Database/System/control-panel/schedules/pacific.json`  
**Poller:** not started from this sitting. `rr-rootserver-poller.service` is enabled, inactive, linger on. A reboot is what starts it.

The working grid Alexander has open is `Desktop/Manual Audit Documentation/New Hourly Sequence.txt`. If that file and this page disagree, `jobs.py` and `pacific.json` are the ones the poller reads.

## How a reboot runs

`run-poller.sh` does not wait. Camera frames, host stats, GitHub sync, and the EcoFlow leapfrog start as soon as the process is up. AI reports (`ai_processing_report_hourly`, `ai_usage_report`, `cloud_narrative_merged`, `cloud_narrative_kilauea`, `cursor_fallback`) are not replayed if boot misses their minute. They run the next time the clock reaches their slot. Night sleep defaults off, so a running poller does not skip jobs.

The poller then uses schedule JSON, not the `at_minute` lines in `jobs.py`, because `pacific.json` is version 1 and has entries. Both the global flag and `pacific.json` are armed and not disconnected. A Root Monitor Save writes JSON only and forces armed off. This sitting did not use that Save path.

Enabled flags in the JSON match `run-poller.sh` defaults. The systemd drop-in still sets `RR_LOCAL_DATA_POLL=0` before the script. Voice desks that render a WAV set `RR_RADIO_PUSH=0` on that job so they do not SSH by themselves.

If boot finishes a few seconds after the minute, one-shots already due in that minute still run once. The every-5s and every-10s stacks do not replay.

## The hour

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

### Confirmed facts
- Recurring work is `EXACT_TIME`. Schedule JSON is what a running poller fires.
- The poller was not started. The unit is enabled and inactive.
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
