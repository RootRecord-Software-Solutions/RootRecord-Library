# Test record — G3 voice reports batch 2 (7 ported G1 reports, gated OFF)

| Field | Value |
| --- | --- |
| **Date / time (HST)** | 2026-09-29 04:27–04:35 HST |
| **Tester** | Grok Bot (executor, overnight build, pass 2) |
| **Change under test** | New Pacific `Media/Voice/scripts/voice_reports.py` (stdlib; text + stitched WAV via `voice-render.sh stitch`); `clip_catalog.py` +13 entries; `voice_generate.py` (catalog `spoken` override + `proposed` flag, stitcher skips proposed); 7 jobs in `Automations/scripts/jobs.py` (all OFF); Database `.gitignore` `/Media/Audio/Voice/Reports/Archive/`. Doc: `00-architecture/Voice-Reports-G3.md` §5–6 |
| **State** | **PASS** (7/7 reports rc 0, WAV QC PASS, text written, rotation works) · jobs **LANDED, gated OFF** (take effect only at the next poller start with a flag set) · by-ear **VERIFY PENDING** · earthquake **BLOCKED** (no data) |
| **Evidence** | Database `Media/Audio/Voice/<report>_current.wav` (+ `.read.txt` / `.speak.txt`) and `Media/Audio/Voice/Reports/<report>_current.md` |
| **Backup** | `/home/rootrecord/Database/GITHUB/g3-voice-reports2.bak-20260929-042153/` |

## Data sources (only what already exists)
| Report | Persona | Source | State |
| --- | --- | --- | --- |
| hourly_chime | Ava | clock; 48 cached clips | PASS |
| nws_weather | Ava | Database `Weather/Hawai'i/hfo/api.weather.gov/alerts/active/area=HI/area=HI_current.json` (1 High Surf Advisory) + `Weather/Hawai'i/reports/0 Level Processing/sfp_state_forecast_current.md` | PASS |
| earthquake_hourly | Carly | USGS — **none collected** (Database `Geology/` empty, Pacific `Geology/` README only) | **BLOCKED, skipped**. No collector added |
| energy_report | Carly | Database `Energy/soc/*-last.json` + `Energy/watts/*-last.json` (EcoFlow BLE: Delta 2, River 2 Pro). Vision caption skipped | PASS |
| remaining_tasks | Bruce | Library `06-development/Work-Orders/*.md` unchecked `- [ ]` (27 across 9) | PASS |
| morning / midday / late | Ava | Energy + Weather + `/proc` + work-order count; optional one-line LLM summary (`RR_VOICE_ROLLUP_LLM=1`) | PASS |

## Clip pre-render (quality gate)
`voice-render.sh clips --catalog --only-missing` 04:27: 13 rendered, 68 skipped, rc 0, 12.9 s wall, peak RSS 1,646 MB. **81/81 QC PASS**. The new fixed lines: Ava "State forecast for today." / "…tonight.", "Morning report.", "Midday report.", "Late report.", "End of report.", "EcoFlow is offline."; Carly "Energy desk report."; Bruce "No open tasks on file."; + 4 PROPOSED pronunciation clips (separate record). ASR round trip was **not** re-run for the new clips (the plain-English lines are the same kind as the pass-1 "match" set); add them to a spot check.

## Per-report test (one run each, `nice -n 10 python3 voice_reports.py <report>`)
| Report | Time | rc | Wall | Clips / live sentences | Model loaded | Peak RSS | WAV (ffprobe) | Duration | QC | MemAvailable before → min | Load max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hourly_chime | 04:28 | 0 | 0.31 s | 1 / 0 | no | 37 MB | s16 / 24000 / 1 | 1.67 s | PASS | 9,318 → 9,305 MB | 2.64 |
| nws_weather | 04:28 | 0 | 16.5 s | 2 / 9 | yes | 1,562 MB | s16 / 24000 / 1 | 28.57 s | PASS | 9,313 → 9,135 MB | 3.69 |
| energy_report | 04:28 | 0 | 10.7 s | 1 / 2 | yes | 1,484 MB | s16 / 24000 / 1 | 16.77 s | PASS | 11,405 → 10,044 MB | 3.83 |
| remaining_tasks | 04:28 | 0 | 8.1 s | 1 / 2 | yes | 1,359 MB | s16 / 24000 / 1 | 9.29 s | PASS | 11,011 → 10,290 MB | 3.83 |
| morning_report | 04:34 | 0 | 15.6 s | 2 / 7 | yes | 1,594 MB | s16 / 24000 / 1 | 28.03 s | PASS | 11,945 → 10,275 MB | 2.18 |
| midday_report | 04:34 | 0 | 14.3 s | 2 / 7 | yes | 1,557 MB | s16 / 24000 / 1 | 28.07 s | PASS | 11,385 → 10,220 MB | 2.51 |
| late_report | 04:35 | 0 | 14.4 s | 2 / 7 | yes | 1,561 MB | s16 / 24000 / 1 | 27.86 s | PASS | 11,426 → 10,220 MB | 2.64 |

Load during 04:28–04:30 includes other agents' work on the desk (browser + specialist builds). MemAvailable before the first two runs was lower (~9.3 GB) for the same reason.

- **Bug found and fixed (04:34)**: the first roll-up runs (04:28) spoke "Delta two thirty six a.m.%". The text "Delta 2 36%" hit the G1 clock rule in `speakable.py`. The spoken line now says "Battery levels: Delta 2 at 35 percent, River 2 Pro at 5 percent." (the G1 rule is unchanged). The three roll-ups were re-run; the table shows the re-runs. Also fixed before the test: work-order codes are spelled for Kokoro ("WO-ECO" → "E C O").
- **Rotation**: a second `hourly_chime` at 04:29:42 moved the old copy to `Reports/Archive/hourly_chime_20260929T0428.md` and `Media/Audio/Voice/Archive/hourly_chime_20260929T0428.wav` (+ sidecars). PASS.
- **LLM summary (once)**: `RR_VOICE_ROLLUP_LLM=1 voice_reports.py morning_report` 04:30: rc 0, 24.5 s wall, run-infer route npu-flm llama3.2:1b cold start, latency 6,163 ms, prompt 95 chars / reply 60 chars (lengths only in the JSONL, caller `voice_rollup`), FLM peak 2,006 MB, MemAvailable 11,793 → min 9,933 MB, load max 5.00. The summary restated only the given facts ("The batteries are at 36% and 5%. The solar input is 0 watts."). PASS.
- **Delivery**: none. No Telegram, no radio push, no playback.

## Jobs (Pacific `Automations/scripts/jobs.py`, all OFF)
`import jobs` check: all 7 `enabled False` with no flags set; with `RR_VOICE_NWS=1` only `voice_nws_weather` turns on. Flags: `RR_VOICE_HOURLY_CHIME`, `RR_VOICE_NWS`, `RR_VOICE_ENERGY`, `RR_VOICE_REMAINING`, `RR_VOICE_ROLLUPS` (+ `RR_VOICE_ROLLUP_LLM`). The poller was **not** restarted.

## Listen list additions (VERIFY PENDING, by ear)
`nws_weather_current.wav` (Niʻihau/Kauaʻi respellings in a live sentence), `energy_report_current.wav`, `remaining_tasks_current.wav` ("E C O 6, G H 4"), `morning_report_current.wav` (join quality across 2 clips + 7 live sentences).

## Cleanup confirmation
- [x] 0 kokoro / voice_generate / whisper / flm processes; `ollama ps` empty; single-flight **IDLE**; port 52625 closed. Nothing played or sent.
