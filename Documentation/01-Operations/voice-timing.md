# Voice timing

2026-10-02 ~16:58 HST: the measurements below are still the half-hour lock. Alexander ordered a one-hour playlist at 13:44 HST. `jobs.py` was not moved to :50, and `stream.js` still locks at HH:29:59 and HH:59:59. Do not treat the ordered hour as these timings. Chimes remain every 30 minutes.

**Generated:** 2026-10-02 16:05 HST  
**Source:** automations log, job wall time from RUN to the result line  
**Model:** none  
**Template:** `5 - RootRecord-Library/Agent Context/Documenter-Agent-Context/HANDOFF-TEMPLATE.md`  

## Handoff — 2026-10-02 16:05 HST — voice_timing_report → Library

### Confirmed facts
- The station locks the playlist at HH:29:59 and HH:59:59, then chimes on the hour and the half hour.
- A file that arrives after that lock waits for the next cycle.
- The measured desks share one poller thread and one voice lock, so a set runs one after another.
- The lead from :45:00 to the :29:59 lock is 14 minutes 59 seconds. :45 has the same lead before :59:59.
- The 9-desk set sums to median 328s, average 410s, and p90 705s.
- That p90 sum fits inside the lead.
- The schedule table is copied from jobs.py.

### Pages updated

- `Documentation/01-Operations/voice-timing.md` (this page)

### Evidence

499 finished runs in 56 log files.

| Job | Scheduled |
| --- | --- |
| `voice_system_perf` | [45] |
| `voice_nws_weather` | [45] |
| `voice_remaining_tasks` | [45] |
| `voice_earthquake_report` | [45] |
| `voice_kilauea_report` | [45] |
| `voice_solar_desk` | [45] |
| `voice_security_desk` | [45] |
| `voice_bandwidth_desk` | [45] |
| `voice_current_report` | [45] |
| `voice_hurricane_desk` | ["05:45", "09:45", "12:45", "16:45", "20:45"] |
| `voice_morning_report` | — |
| `voice_midday_report` | — |
| `voice_late_report` | — |
| `voice_late_final_report` | — |
| `radio_news_update` | [8] |
| `voice_hourly_chime` | [0, 30] |

| Report | Job | Runs | Median | Average | p90 |
| --- | --- | ---: | ---: | ---: | ---: |
| System | `voice_system_perf` | 50 | 30s | 39s | 56s |
| NWS | `voice_nws_weather` | 103 | 38s | 41s | 81s |
| Remaining tasks | `voice_remaining_tasks` | 47 | 21s | 27s | 41s |
| Earthquakes | `voice_earthquake_report` | 46 | 32s | 42s | 68s |
| Kīlauea | `voice_kilauea_report` | 48 | 32s | 41s | 53s |
| Solar | `voice_solar_desk` | 44 | 50s | 62s | 118s |
| Security | `voice_security_desk` | 47 | 25s | 38s | 89s |
| Bandwidth | `voice_bandwidth_desk` | 45 | 28s | 38s | 73s |
| Current | `voice_current_report` | 49 | 72s | 81s | 126s |
| Hurricane | `voice_hurricane_desk` | 7 | 34s | 34s | 44s |
| Morning roll-up | `voice_morning_report` | 2 | 48s | 48s | 82s |
| Midday roll-up | `voice_midday_report` | 1 | 32s | 32s | 32s |
| Late roll-up | `voice_late_report` | 2 | 23s | 23s | 26s |
| Late final | `voice_late_final_report` | 1 | 0s | 0s | 0s |
| News | `radio_news_update` | 7 | 674s | 468s | 708s |
| Chime | `voice_hourly_chime` | 0 | — | — | — |

p90 is the nearest rank in that desk's own runs. The stack p90 is the sum of those ranks, not one measured batch.

### Still open / unresolved

- A slow energy camera look and a slow current report do not always land in the same pass. The summed p90 is the cautious figure.
- Daypart roll-ups are written only inside their Hawaii window, so the 09:00, 12:00, and 21:00 cycles still play the previous roll-up.

### Explicitly historical (do not treat as current)

- Any earlier sentence that quotes one log pass, including the 299-run note from 2026-10-01 23:48 HST, is that pass. This page is the current measurement.

### Next recommended action

- Keep the :45 and :45 start while the summed p90 still fits the lead.
