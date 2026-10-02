# Voice timing

**Generated:** 2026-10-02 11:05 HST  
**Source:** automations log, job wall time from RUN to the result line  
**Model:** none  
**Template:** `5 - RootRecord-Library/Agent Context/Documenter-Agent-Context/HANDOFF-TEMPLATE.md`  

## Handoff — 2026-10-02 11:05 HST — voice_timing_report → Library

### Confirmed facts
- The station locks the playlist at HH:29:59 and HH:59:59, then chimes on the hour and the half hour.
- A file that arrives after that lock waits for the next cycle.
- The measured desks share one poller thread and one voice lock, so a set runs one after another.
- The lead from :22:00 to the :29:59 lock is 7 minutes 59 seconds. :52 has the same lead before :59:59.
- The 9-desk set sums to median 318s, average 379s, and p90 647s.
- That p90 sum is longer than the lead.
- The schedule table is copied from jobs.py.

### Pages updated

- `Documentation/01-Operations/voice-timing.md` (this page)

### Evidence

433 finished runs in 52 log files.

| Job | Scheduled |
| --- | --- |
| `voice_system_perf` | [22, 52] |
| `voice_nws_weather` | [22, 52] |
| `voice_remaining_tasks` | [22, 52] |
| `voice_earthquake_report` | [22, 52] |
| `voice_kilauea_report` | [22, 52] |
| `voice_solar_desk` | [22, 52] |
| `voice_security_desk` | [22, 52] |
| `voice_bandwidth_desk` | [22, 52] |
| `voice_current_report` | [22, 52] |
| `voice_hurricane_desk` | ["05:40", "09:40", "12:40", "16:40", "20:40"] |
| `voice_morning_report` | ["09:02"] |
| `voice_midday_report` | ["12:02"] |
| `voice_late_report` | ["21:02"] |
| `voice_late_final_report` | ["23:02"] |
| `radio_news_update` | [36] |
| `voice_hourly_chime` | [0, 30] |

| Report | Job | Runs | Median | Average | p90 |
| --- | --- | ---: | ---: | ---: | ---: |
| System | `voice_system_perf` | 43 | 28s | 37s | 51s |
| NWS | `voice_nws_weather` | 96 | 38s | 39s | 81s |
| Remaining tasks | `voice_remaining_tasks` | 40 | 21s | 26s | 41s |
| Earthquakes | `voice_earthquake_report` | 39 | 32s | 38s | 48s |
| Kīlauea | `voice_kilauea_report` | 41 | 30s | 37s | 50s |
| Solar | `voice_solar_desk` | 37 | 49s | 57s | 109s |
| Security | `voice_security_desk` | 40 | 22s | 35s | 87s |
| Bandwidth | `voice_bandwidth_desk` | 38 | 27s | 31s | 51s |
| Current | `voice_current_report` | 43 | 70s | 80s | 129s |
| Hurricane | `voice_hurricane_desk` | 6 | 37s | 34s | 44s |
| Morning roll-up | `voice_morning_report` | 2 | 48s | 48s | 82s |
| Midday roll-up | `voice_midday_report` | 0 | — | — | — |
| Late roll-up | `voice_late_report` | 2 | 23s | 23s | 26s |
| Late final | `voice_late_final_report` | 1 | 0s | 0s | 0s |
| News | `radio_news_update` | 5 | 210s | 368s | 705s |
| Chime | `voice_hourly_chime` | 0 | — | — | — |

p90 is the nearest rank in that desk's own runs. The stack p90 is the sum of those ranks, not one measured batch.

### Still open / unresolved

- A slow energy camera look and a slow current report do not always land in the same pass. The summed p90 is the cautious figure.
- Daypart roll-ups are written only inside their Hawaii window, so the 09:00, 12:00, and 21:00 cycles still play the previous roll-up.

### Explicitly historical (do not treat as current)

- Any earlier sentence that quotes one log pass, including the 299-run note from 2026-10-01 23:48 HST, is that pass. This page is the current measurement.

### Next recommended action

- Move the :22 and :52 start earlier. The summed p90 no longer fits the lead.
