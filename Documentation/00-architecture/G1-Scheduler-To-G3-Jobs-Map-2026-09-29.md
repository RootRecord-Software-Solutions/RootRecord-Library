# G1 scheduler → G3 jobs map (scheduler-clock verification)

| Field | Value |
| --- | --- |
| **Source** | G1 `Solar-Pacific-RootRecord-Server-Old/scheduler-clock/scripts/scheduler.py` (APScheduler). 73 `add_job` calls, 64 unique job ids (parsed 2026-09-29 ~14:33 HST from a read-only shallow clone). G1 KEPT, unchanged |
| **G3 registry** | Pacific `Automations/scripts/jobs.py` (read at poller start). Proposed-only blocks: [Pending-Job-Registrations-2026-09-29](./Pending-Job-Registrations-2026-09-29.md) |
| **Purpose** | Matrix row 15 ("Scheduler clock — verify-only"). This is the verification: every G1 job, where it lives in G3 and its gate. |

States: **LIVE** = enabled in G3 now · **GATED** = in jobs.py, OFF until its flag is set at a poller start · **PROPOSED** = script ported, block in the Pending doc (not in jobs.py) · **ON DEMAND** = ported, no job · **BLOCKED** = needs Alexander (reason) · **OUT** = out of Pacific scope.

| G1 job id | G1 trigger (HST) | G3 | State / flag |
| --- | --- | --- | --- |
| heartbeat | every 60 s | `heartbeat` builtin | LIVE |
| rr-noaa | every 60 min | `weather_poller` daemon (Pacific `Weather/`) | LIVE |
| radar-archive | every 10 min | `weather_poller` (`Weather/fetch/radar.py`, 14-day dated archive); all-time zip `weather_radar_zip` (`Weather/RadarZip/scripts/radar_zip.py`, 600 s) | LIVE fetch; zip GATED `RR_RADAR_ZIP` |
| official-weather-media | every 10 min | `Weather/scripts/official_statement.py` (HLS) + `voice_reports.py official_weather` | PROPOSED `RR_OFFICIAL_HLS`, `RR_VOICE_OFFICIAL`; OBS BLOCKED |
| nws-hawaii-counties | :07 :22 :37 :52 | `voice_nws_weather` | GATED `RR_VOICE_NWS` |
| rr-kilauea | every 60 min | `geology_collect` (HVO) + `voice_kilauea_report` + `geology_kilauea_public_draft` (`Geology/PublicDraftQueue/scripts/queue_draft.py`, 3600 s) | GATED `RR_GEOLOGY`, `RR_VOICE_KILAUEA`, `RR_KILAUEA_DRAFT`; draft queues from `kilauea-last.json` and does not send; Grok draft BLOCKED |
| time-chime | :00 :30 | `voice_hourly_chime` | GATED `RR_VOICE_HOURLY_CHIME` |
| remaining-tasks | :32 | `voice_remaining_tasks` | GATED `RR_VOICE_REMAINING` |
| morning-boot-replay | :32 | `Media/MorningBootReplay/scripts/replay.py` | PROPOSED `RR_MORNING_BOOT_REPLAY` (not in jobs.py). Dry-run handoff to `Media/Playback`. Speaker still off |
| hourly-clip-reports (+ hourly-clip-prebuild :55) | :02 | `voice_solar_desk` / `voice_security_desk` / `voice_bandwidth_desk` / `voice_kilauea_report` | PROPOSED / GATED; playback BLOCKED |
| earthquake-hourly | :08 | `voice_earthquake_report` | GATED `RR_VOICE_QUAKE` |
| earthquake-m2-poll | every 10 min | `geology_collect` (300 s) | GATED `RR_GEOLOGY` |
| council-quake | every 2 min | `council_quake_telegram` | GATED `RR_COUNCIL_QUAKE` (120 s, dry-run). Send BLOCKED until `RR_COUNCIL_QUAKE_SEND=1`. WAV off. |
| council-bruce-stats | 07:18 15:18 21:18 | `bruce_stats_posts` | GATED `RR_BRUCE_STATS`. Dry-run. Send BLOCKED until `RR_BRUCE_STATS_SEND=1`. |
| hourly-solar-weather | :04 | `voice_solar_desk` + `energy_sun_times` | PROPOSED `RR_VOICE_SOLAR`; GATED `RR_SUN_TIMES` |
| solar-notes-quarter-hour | every 30 min | Energy BLE poller (G3 Energy db) | LIVE (capability) |
| hybrid-charge-status | every 30 min | Energy BLE poller | LIVE (capability) |
| system-performance | :06 | `voice_system_perf` | GATED `RR_VOICE_SYSTEM_PERF` |
| player-economy-report | every 60 min | — | OUT (RootMC product) |
| morning-report | 09:00 | `voice_morning_report` 09:02 | GATED `RR_VOICE_ROLLUPS` |
| report-readiness | every 5 min | `Reports/scripts/report_board.py status` | PROPOSED `RR_REPORT_BOARD`; readiness playback BLOCKED |
| report-periodic-audio | every 5 min | `Media/Playback/scripts/play.py` on demand | GATED `RR_PLAYBACK`; old 5-minute replay not restored (WO-MIG-15) |
| morning-report-play / midday-report-play / late-report-play | 09:05 / 12:05 / 21:08 | `Media/Playback/scripts/play.py` on demand | GATED `RR_PLAYBACK`; old play crons not restored (WO-MIG-15) |
| day-reports-morning / -midday / -evening | 09:10 / 13:00 / 18:00 | G3 roll-ups (text) | GATED `RR_VOICE_ROLLUPS` (slot reports = same roll-ups; evening slot removed in G1) |
| midday-report | 12:00 | `voice_midday_report` 12:02 | GATED `RR_VOICE_ROLLUPS` |
| daily-reports-catchup | 14:00 | `Reports/scripts/report_board.py run-due` | PROPOSED `RR_REPORT_BOARD` (text only; play BLOCKED) |
| late-report / late-final-report | 21:00 / 23:30 | `voice_late_report` 21:02 / `voice_late_final_report` 23:30 | GATED `RR_VOICE_ROLLUPS` / `RR_VOICE_LATE_FINAL` (23:30 is a text-only second chance for the same late slot; skips if that slot is done) |
| merged-morning-summary | 10:20 | covered by `voice_morning_report` | GATED |
| cursor-fallback | 10:22 16:22 | `System/ApiPrices/scripts/job.py cursor-drain` | GATED `enabled: False` (WO-MIG-35). No agent unless `RR_API_SPEND=1`. No report write. |
| governance-daily | 10:23 | — | OUT (Library content) |
| api-prices | 10:25 | `System/ApiPrices/scripts/job.py refresh` | GATED `enabled: False` (WO-MIG-35). No HTTP unless `RR_API_PRICES=1`. |
| code-review | 11:20 17:20 | `CodeReview/scripts/code_review.py` on demand | WO-MIG-34. Evidence only. `RR_CODE_REVIEW_CODER` unset. Gated `code_review_pack` not in jobs.py (file already being edited). Old clock not restored. |
| economy-brief | 15:00 | `Reports/Economy-Brief/scripts/economy_brief.py` on demand | PROPOSED `RR_ECONOMY_BRIEF` (not in jobs.py). Discord send not signed off. |
| adsense-eod / admob-eod | 21:00 / 21:05 | `adsense_eod` / `admob_eod` | GATED `RR_ADSENSE` / `RR_ADMOB` (WO-MIG-38). No key writes `not_configured` and does not call Google |
| overnight-relay | 22:20 | `Communications/Inbox/scripts/inbox.py overnight` | GATED `RR_OVERNIGHT_RELAY` (WO-MIG-31). File write only. No Discord post. |
| minecraft-live | every 10 min | — | OUT (RootMC) |
| hurricane-fetch | 05/09/12/16/20 :40 | `weather_poller` (`Weather/hurricanes/`, NHC CurrentStorms) | LIVE; JTWC/RAMMB global board not in G3 (source decision) |
| hurricane-desk / hurricane-desk-evening | 05/09/12/20 :50, 16:55 | `voice_hurricane_desk` | GATED `RR_VOICE_HURRICANE` |
| hurricane-radio-am / -mid / -pm | 06:35 / 13:12 / 17:02 | `media_hurricane_radio` | GATED `RR_HURRICANE_RADIO` (in jobs.py, off). Dry-run handoff to Playback. Speaker and AWS radio off. |
| ecoflow-quota | every 2 min | Pacific `Energy/` BLE poller; cloud fallback `Energy/Cloud-Quota/scripts/quota_poll.py` | LIVE via BLE. Cloud GATED `RR_ECOFLOW_CLOUD` (off). Job not inserted (`jobs.py` already edited). Archived; GitHub deletion `50d3b0a6`. |
| drive-automation | every 30 min | — | BLOCKED (actuation) |
| panels-cam | every 15 min | Pacific `Security/Cameras/` grab | partial; power session BLOCKED (actuation) |
| energy-report | every 30 min | `voice_energy_report` :15 :45 | GATED `RR_VOICE_ENERGY` |
| council-health | every 5 min | `council_health` 300 s | GATED `RR_COUNCIL_HEALTH`. Report only. No send, no model probe. |
| public-health | every 5 min | — | OUT (website) |
| fs-index | every 15 min | `path_index` | GATED off (`enabled: False`, 900 s). Pacific `System/PathIndex`. Four source trees only. WO-MIG-42 |
| host-sample | every 1 min | `System/scripts/host_desks.py net-sample` (300 s) + `System/lib/sample.py` | PROPOSED `RR_NET_SAMPLES` |
| log-cleanup | 04:20 | `log_retention` | GATED off (`enabled: False`, `--dry-run`). WO-MIG-41. Move, never delete. Live `--apply` needs `RR_LOG_RETENTION_APPLY=1` |
| user-qrcodes / account-import | every 6 h | — | OUT (identity; personal data) |
| d1-sync | every 6 h | — | BLOCKED (D1 credentials) |
| inbox-drain | every 5 min | `inbox_drain` 300 s | GATED `RR_INBOX_DRAIN` (WO-MIG-31). Local copy of Relay-Inbox. No D1. No send. |
| stripe-poll | 30 min | `stripe_poll` 1800 s | GATED `RR_STRIPE` (WO-MIG-10). No key writes `not_configured` and does not call Stripe |
| ltc-pending | 30 min | — | OUT (payments; not WO-MIG-10) |
| vercel-builds | 5 min | `vercel_builds` 300 s | GATED `RR_VERCEL_BUILDS` (WO-MIG-10). No token writes nothing and does not call Vercel |

Counts over the 64 ids: every id is accounted for above (grouped rows cover several ids). Nothing in G1's scheduler lacks a G3 decision; the remaining gaps are the BLOCKED / OUT rows.

G1 extras not in the table: `AVA_CRON_WAVE` clone guard and night-sleep gating (`Ecoflow/state/night-mode.json sleeping` skipped jobs). G3 night-sleep gate is armed on the live poller as of 2026-09-30 00:02 HST (`RR_NIGHT_SLEEP=1` in `run-poller.sh`, WO-MIG-01). There is no `night-mode.json`, so jobs are not skipped.

*Created 2026-09-29 ~14:35 HST (old-repo migration, breadth pass 2). 2026-09-30 WO-MIG-10: stripe-poll and vercel-builds rows now match the gated jobs. ltc-pending stays OUT. 2026-09-30 WO-MIG-31: inbox-drain and overnight-relay are gated file writers. The Cloudflare drain stays paused.*
