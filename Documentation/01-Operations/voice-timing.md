# Voice timing

**Generated:** 2026-10-02 02:05 HST  
**Source:** automations log, job wall time from RUN to the result line  
**Model:** none  
**Template:** `5 - RootRecord-Library/Agent Context/Documenter-Agent-Context/HANDOFF-TEMPLATE.md`  

## Handoff — 2026-10-02 02:05 HST — voice_timing_report → Library

### Confirmed facts
- The station locks the playlist at HH:29:59 and HH:59:59, then chimes on the hour and the half hour.
- A file that arrives after that lock waits for the next cycle.
- The measured desks share one poller thread and one voice lock, so a set runs one after another.
- The lead from :12:00 to the :29:59 lock is 17 minutes 59 seconds. :42 has the same lead before :59:59.
- The ten-desk set sums to median 310s, average 375s, and p90 689s.
- That p90 sum fits inside the lead.
- The schedule table is copied from jobs.py.

### Pages updated

- `Documentation/01-Operations/voice-timing.md` (this page)

### Evidence

275 finished runs in 43 log files.

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
| System | `voice_system_perf` | 26 | 31s | 38s | 51s |
| NWS | `voice_nws_weather` | 79 | 34s | 37s | 89s |
| Remaining tasks | `voice_remaining_tasks` | 23 | 22s | 25s | 40s |
| Earthquakes | `voice_earthquake_report` | 22 | 32s | 44s | 74s |
| Kīlauea | `voice_kilauea_report` | 24 | 32s | 39s | 85s |
| Solar | `voice_solar_desk` | 20 | 34s | 43s | 93s |
| Security | `voice_security_desk` | 23 | 25s | 39s | 89s |
| Bandwidth | `voice_bandwidth_desk` | 21 | 27s | 28s | 39s |
| Current | `voice_current_report` | 26 | 74s | 82s | 129s |
| Hurricane | `voice_hurricane_desk` | 4 | 42s | 42s | 52s |
| Morning roll-up | `voice_morning_report` | 1 | 82s | 82s | 82s |
| Midday roll-up | `voice_midday_report` | 0 | — | — | — |
| Late roll-up | `voice_late_report` | 2 | 23s | 23s | 26s |
| Late final | `voice_late_final_report` | 1 | 0s | 0s | 0s |
| News | `radio_news_update` | 3 | 197s | 154s | 210s |
| Chime | `voice_hourly_chime` | 0 | — | — | — |

p90 is the nearest rank in that desk's own runs. The stack p90 is the sum of those ranks, not one measured batch.

### Still open / unresolved

- A slow energy camera look and a slow current report do not always land in the same pass. The summed p90 is the cautious figure.
- Daypart roll-ups are written only inside their Hawaii window, so the 09:00, 12:00, and 21:00 cycles still play the previous roll-up.

### Explicitly historical (do not treat as current)

- Any earlier sentence that quotes one log pass, including the 299-run note from 2026-10-01 23:48 HST, is that pass. This page is the current measurement.

### Next recommended action

- Keep the :12 and :42 start while the summed p90 still fits the lead.
