# Voice timing

**Generated:** 2026-10-03 14:10 HST  
**Source:** automations log, job wall time from RUN to the result line  
**Model:** none  
**Template:** `5 - RootRecord-Library/Agent Context/Documenter-Agent-Context/HANDOFF-TEMPLATE.md`  

## Handoff — 2026-10-03 14:10 HST — voice_timing_report → Library

### Confirmed facts
- The station locks the playlist at HH:29:59 and HH:59:59, then chimes on the hour and the half hour.
- A file that arrives after that lock waits for the next cycle.
- The measured desks share one poller thread and one voice lock, so a set runs one after another.
- The lead from :22:00 to the :29:59 lock is 7 minutes 59 seconds. :52 has the same lead before :59:59.
- The 9-desk set is incomplete in this log, so no stack sum is stated.
- The schedule table is copied from jobs.py.

### Pages updated

- `Documentation/01-Operations/voice-timing.md` (this page)

### Evidence

7 finished runs in 9 log files.

| Job | Scheduled |
| --- | --- |
| `voice_system_perf` | — |
| `voice_nws_weather` | — |
| `voice_remaining_tasks` | — |
| `voice_earthquake_report` | — |
| `voice_kilauea_report` | — |
| `voice_solar_desk` | — |
| `voice_security_desk` | — |
| `voice_bandwidth_desk` | — |
| `voice_current_report` | — |
| `voice_hurricane_desk` | — |
| `voice_morning_report` | — |
| `voice_midday_report` | — |
| `voice_late_report` | — |
| `voice_late_final_report` | — |
| `radio_news_update` | — |
| `voice_hourly_chime` | — |

| Report | Job | Runs | Median | Average | p90 |
| --- | --- | ---: | ---: | ---: | ---: |
| System | `voice_system_perf` | 2 | 42s | 42s | 80s |
| NWS | `voice_nws_weather` | 2 | 19s | 19s | 35s |
| Remaining tasks | `voice_remaining_tasks` | 0 | — | — | — |
| Earthquakes | `voice_earthquake_report` | 0 | — | — | — |
| Kīlauea | `voice_kilauea_report` | 0 | — | — | — |
| Solar | `voice_solar_desk` | 0 | — | — | — |
| Security | `voice_security_desk` | 0 | — | — | — |
| Bandwidth | `voice_bandwidth_desk` | 0 | — | — | — |
| Current | `voice_current_report` | 0 | — | — | — |
| Hurricane | `voice_hurricane_desk` | 0 | — | — | — |
| Morning roll-up | `voice_morning_report` | 0 | — | — | — |
| Midday roll-up | `voice_midday_report` | 0 | — | — | — |
| Late roll-up | `voice_late_report` | 0 | — | — | — |
| Late final | `voice_late_final_report` | 0 | — | — | — |
| News | `radio_news_update` | 0 | — | — | — |
| Chime | `voice_hourly_chime` | 3 | 0s | 0s | 1s |

p90 is the nearest rank in that desk's own runs. The stack p90 is the sum of those ranks, not one measured batch.

### Still open / unresolved

- A slow energy camera look and a slow current report do not always land in the same pass. The summed p90 is the cautious figure.
- Daypart roll-ups are written only inside their Hawaii window, so the 09:00, 12:00, and 21:00 cycles still play the previous roll-up.

### Explicitly historical (do not treat as current)

- Any earlier sentence that quotes one log pass, including the 299-run note from 2026-10-01 23:48 HST, is that pass. This page is the current measurement.

### Next recommended action

- Keep the :22 and :52 start while the summed p90 still fits the lead.
