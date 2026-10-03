# Voice Reports — G3 (Kokoro-82M port + phrase-clip cache)

2026-10-03 ~08:22 HST: this file is the port record. The live hour is `news_cycle` at :35 and `generate_hour_reports.py` at :36. Living page: [voice desk](../01-Operations/2026-09-30-voice-desk.md). Clock: [hourly sequence](../01-Operations/2026-10-02-hourly-sequence.md).

2026-10-02 ~16:58 HST: the news hour no longer reads The Guardian, the BBC, MarketWatch, Honolulu Civil Beat, the Honolulu Star-Advertiser, Hawaii News Now, NPR National, NPR Politics, or the Department of Justice feed. A publisher is limited to two items on one desk. National Hurricane Center coordinate tables and forecast discussions are not spoken. The one-hour air order is still not the mixer. Living page: [voice desk](../01-Operations/2026-09-30-voice-desk.md). No new audio, no commit.

2026-10-02 ~15:14–15:42 HST: earthquake speech now includes M2.5 day/week change; remaining-tasks speaks open work orders; morning/midday/late roll-up builders and their `jobs.py` rows are removed; `run-poller.sh` soft-defaults `RR_VOICE_ROLLUPS` and `RR_VOICE_LATE_FINAL` to 0 (was 1). `solar_desk` wakes a stagnant pack via `leapfrog-read.sh` before speaking. Living schedule detail: [voice desk](../01-Operations/2026-09-30-voice-desk.md). No new audio, no poller restart from this seat.

2026-10-02 ~14:53 HST: hurricane desk speech now drops lines already on the latest NWS report. `Media/Voice/scripts/voice_reports.py` calls `Reports/pipeline/owners.trim_hurricane` after `b_hurricane_desk`; empty keep becomes one pointer sentence to the weather report. Spoken markdown is rewritten to match. Voice and system_perf also write a canonical `*.report.json` sidecar; store errors do not erase markdown or WAV. No new audio, no commit.

2026-10-02 ~14:33 HST: Report Instructor changed the hurricane desk speech, no new audio, no commit. `Media/Voice/scripts/voice_reports.py` `b_hurricane_desk` speaks sentences: the storm, distance from the nearest island, movement, winds, and whether Honolulu has a watch. It does not speak coordinates, bearings, or the nearest-hurricane dump. The markdown table still has the raw track, including position and bearing. `2 - RootRecord-Database/Media/Audio/Voice/hurricane_desk_current.wav` is stamped 12:52 HST, so that clip is the old wording. The next `voice_hurricane_desk` time in `jobs.py` is 16:45, and the job stays off unless `RR_VOICE_HURRICANE=1`. No commit.

2026-10-02 ~14:22 HST: short weekdays speak in full. `Media/Voice/scripts/speakable.py` turns mon through sat into Monday through Saturday. Sun stays sun so a solar line does not become Sunday. The poller was restarted at 14:22 HST and loaded the :45 schedule. Locals stay minute [45], news [8] (part1+part2 only), `current_report` enabled False. Clocks in `poller-dashboard.py` and `rr_control_panel.py` use `%A`. No commit.

2026-10-02 ~14:12 HST: locals are minute [45] in `jobs.py`, news is [8] and pushes only part 1 and part 2, and the current report is off. The poller is still frozen, so this does not run until a clean start.

Mainland ~13:58 HST: 2:00 and 2:30 chimes are on the station, and the solar file landed as one battery at 40 percent across two live packs. That figure is Mainland’s read.

2026-10-02 ~13:44 HST: the hour cycle is the order. Desk `jobs.py` local voice jobs are minute [50], chimes [0, 30], news still one job at :36. Daypart `enabled` lines are broken (`False, "0") == "1"` at `voice_morning_report` and the same shape on midday, late, and late-final), That break was closed ~13:57 HST. The file parses, and those four jobs are `enabled` False. Merged battery is ordered and not the spoken script yet. Mainland’s mixer report and the viewer count of 1 are Mainland’s, not a desk measurement.

| Field | Value |
| --- | --- |
| **Date (HST)** | 2026-09-29 port record. **Current behavior is [2026-09-30 voice desk](../01-Operations/2026-09-30-voice-desk.md) (updated 2026-10-02).** |
| **State** | Engine **LANDED**. Speeds are all **1.0**. Telegram delivery is **ON** (`RR_VOICE_DELIVER=1`, dest `council` in `run-poller.sh`). Host temperature is spoken as **Celsius**. Pack watts and channel-1 solar look live in Bruce’s combined `solar_desk` (former `energy_report` retired 2026-10-02). Hourly chime files exist; the chime job stays **OFF** (`RR_VOICE_HOURLY_CHIME` not exported by `run-poller.sh`). Roll-ups, late-final, and hurricane are **armed** in `run-poller.sh` as of 2026-10-02. |
| **Backup** | `/home/rootrecord/Database/GITHUB/g3-voice-ailog.bak-20260929-035454/` |
| **Tests** | `07-Testing/2026-09-29-kokoro-voice-port-g3.md` · `07-Testing/2026-09-29-kokoro-phrase-clips-qc.md` · `07-Testing/2026-09-29-hawaiian-pronunciation-sheet.md` |


## Current as of 2026-10-02 ~03:21 HST

Operator schedule and armed flags live in [2026-09-30 voice desk](../01-Operations/2026-09-30-voice-desk.md). This page is the 2026-09-29 port record. Where the sections below still name an old minute (`system_perf` docstring :06), list a separate `energy_report`, or say roll-ups / hurricane / late-final are gated off, the voice-desk page and live `jobs.py` / `run-poller.sh` win. As of ~01:41 HST: nine desks (`energy_report` folded into `solar_desk`); as of ~01:57 HST those desks run at `:22` / `:52` (was `:12` / `:42`); generation-clock stamps; `compare_span.py` percent lines; four desk status clips plus Ava stack closer after all nine Mainland receipts; staged on-air cues (`notify.opus` ding first). Living detail: [voice desk](../01-Operations/2026-09-30-voice-desk.md).

2026-10-02 ~13:41 HST PARTIAL: desk `voice_reports.py` is mid-rewrite toward a merged-battery `solar_desk` (average charge, totaled watts). Builders `b_solar_desk` / `b_security_desk` / `b_current_report` are missing on the working tree versus HEAD, so the merge is not the spoken script yet. See HANDOFF and the voice-desk Energy speech note.

**Pipeline (live):** `jobs.py` → `voice_reports.py` / `system_perf.py` → MD (+ Archive under `test-reports/Voice/`) → `voice-render.sh` stitch (Kokoro single-flight) → `voice_deliver` when `RR_VOICE_DELIVER=1` → `radio_push` unless `RR_RADIO_PUSH=0` → Discord `report_relay` (300 s) → `publish_report_pages` → `/reports/<slug>`.

**Personas:** Ava `af_heart`, Bruce `am_echo`, Carly `af_nova`.

**Armed from `run-poller.sh` (default 1):** system_perf, nws, remaining, quake, kilauea, solar (combined energy+solar), security, bandwidth, current (all :22/:52); roll-ups 09:02/12:02/21:02; late_final 23:02; hurricane five slots; geology + net samples; `RR_UPTIME_LOG` desk heartbeat; Telegram deliver; radio RSS. The radio news job is on as of the Report Instructor's ~11:53 HST read (`RR_RADIO_NEWS=1`). `RR_VOICE_ENERGY` removed. `RR_ANALYTICS_PULL` stays unset (off) until armed.

Midday 2026-10-02: `midday_report_current.wav` was written at 12:10 HST (~37 s) and passed the voice check; the 12:02 job skipped audio while the renderer was busy on `current_report`, though the text was already written, and this does not claim the 12:40 hurricane slot ran.

Report Instructor ~12:29 HST: the new `solar_desk` clip is written with Energy folded into that one clip, not a second file; the local Opus is still yesterday’s; Mainland stopped around 12:31 HST; the solar-desk job is not running; Report Instructor stopped and is not touching the radio; listeners stay up, so the radio is not being staged or restarted and no new clip goes on the air unless Alexander says so; the clip was written and, as of 12:29, was described as not on the station; inside the script, Delta is a BLE read (17% charge, 76 W solar, AC out 0), while River’s file says `source: cloud` and its lines are cloud-stamped 12:25 (59% charge, 139 W solar, 92 W AC out), so despite the BLE footer this is not a BLE report or a River field sample, and River still has no field BLE sample since ~05:45. Corrected ~12:46 HST: Report Instructor read the ML1 playlist and left the station alone. The 12:29 solar file is already in that list, so the next cycle plays it, and Report Instructor will not remove it. Desk `solar_desk_current.wav` is stamped 12:29. Two desk clips are newer than the queued copies and were not pushed: `hurricane_desk_current.wav` is 09:42 HST (about 42 seconds) while the queued file is stamped 21:15, and `news_update_current.wav` is 05:49 (about 25 minutes) while the queued file is stamped 04:49. Mainland ~12:48 HST confirmed the mismatch and is not copying the newer desk hurricane and news files onto ML1. The playlist is what the next cycle queues. 2026-10-02 ~12:54 HST: Alexander ordered listeners off this radio mix onto YouTube, with no video. The station was not stopped. These clips still render here. The stills path is not built, and the wiped ML2 video stack stays wiped. ~12:56 HST: Report Instructor keeps reports as audio and will not make a video version or touch the station. Cove’s ~12:56 hold (keep the Radio page on the live mp3 and do not embed) is superseded ~13:27 HST: the Radio page is to embed the active livestream at https://www.youtube.com/@rootmcnews, picture `1 - Servers/ML1 REBUILD/youtube-thumb.png`, ML1 broadcasting the local mix in parallel. The public Radio page embed landed ~13:31 HST. The ML1 broadcast is not verified on the air. Reports stay audio.

**RadioRss / news_update (~04:30 HST):** sports is dropped from every feed before desks. `stories.py` uses word-edge matching for `nfl`/`nba`/`mlb`/`sports` and expanded leagues, avoiding false hits such as conflict, influenza, and sportswear; 21 sports JSON items and archived SQLite rows were purged. Smoke found 0 sports in speak text and tests passed. The sample is ~22.7 spoken minutes; Ava/Bruce/Carly share airtime via `balance_personas`. The standing 30-minute cycle plays all local reports first, longest first among locals, then gives `news_update` only the remainder and cuts news at the boundary before an unplayed local report; the ML1 mixer is on the air as of the 12:02 HST `rr-radio-station` restart (live `stream.js` has locals first). Mix: markets, defence, SpaceX, Hawaii, chips/big tech, world, mainland weather, centrist politics, science, universities, and also; policy budgets raise defence/politics and feeds add `doj_news`/`defense_gov`. Solar remains separate at 5–7 minutes. At the Report Instructor's ~11:53 HST read, `RR_RADIO_NEWS=1` and the news job is on; only a soft restart is needed for the `jobs.py` `radio_news_update` timeout change to 2400 seconds. Living detail: [voice desk](../01-Operations/2026-09-30-voice-desk.md).

2026-10-02 ~13:01 HST: the date is said once at the beginning of the news, not on every article. Pacific `Media/RadioRss/scripts/news_hour.py` and the ML2 vendor copy open with the month, day, and year. `pipeline.py` says Published once on the cluster opener. The pacific worktree `news_hour.py` still dates every story. That copy is not what gets spoken. The builder the desk runs says the date once. No new audio was rendered. An hour-long block is an idea only; the cycle stays 30 minutes.

**Site traffic (2026-10-02 ~02:33 HST):** `bandwidth_desk` and `current_report` speak Mainland Home/Radio analytics (api / home_proxy / radio; honest partial Home) from Database `Logs/Website/analytics/` via Pacific `Website/scripts/analytics_pull.py` (schema 1.0.0; no page JS). Job `analytics_pull` gated `RR_ANALYTICS_PULL=1` (900 s); off until armed in `run-poller.sh`. Living detail: [voice desk](../01-Operations/2026-09-30-voice-desk.md).


**Big Island weather towns (2026-10-02 ~03:42 HST):** NWS/`zfp_temps` speaks Mountain View (range), Volcano (elev), and Kailua-Kona (shore) with Honolulu/Lihue/Kahului/Hilo; Weather NDFD points + county aliases + lexicon updated. Living detail: [voice desk](../01-Operations/2026-09-30-voice-desk.md).

**Kīlauea image check (2026-10-02 ~03:31 HST):** `voice_kilauea_image_check` every 900 s; Carly “Kilauea observation image was checked” + measured finding; gate `RR_VOICE_KILAUEA_IMAGE` soft default on for soak (`:-1`); **not** in `LOCAL_DATA_POLL_JOBS`; needs poller restart. The separate ML2 `geology_kilauea_cams` collector is now **verified** for USGS still intake only (no mainland vision), exclusive `RR_LOCAL_DATA_POLL=0`, stream-to-Pacific, and post-stream scratch wipe. Pacific live bank: `Geology/Volcanoes/Hawaii/Cams/v1cam_current.jpg`, `v2cam_current.jpg`, `v3cam_current.jpg`, `cams_current.json`; Pacific archives replaced `_current` files as `archive/YYYYMMDD/<stem>_<HHMMSS><ext>`, and `v3cam_current.jpg` verified `source_kind=current`. Living detail: [voice desk](../01-Operations/2026-09-30-voice-desk.md). **Report blend verified (~03:33 HST):** Report Instructor confirmed the text states whether a still was viewed (Y/N) and, when viewed, what conditions looked like.

**Always on:** worklog_scan 90 s, discord_report_relay 300 s, voice_timing_report :05, reports_daily_roll_up 18:30, reports_weekly_archive 19:00, Discord 8 h (00/08/16) + 24 h (12:00).

**OFF / gated:** analytics_pull (`RR_ANALYTICS_PULL` not in `run-poller.sh`), hourly_chime (`RR_VOICE_HOURLY_CHIME` not in `run-poller.sh`), ai_processing, ai_usage, template_reports_daily, media_hurricane_radio, reports_board_catchup, note_work_draft, bruce_stats_posts. `official_weather` / `boot_brief` have Discord routes and builders, no `jobs.py` entry. News / economy_brief / cloud_narrative are README-proposed only; CloudNarrative README’s `cloud_narrative_dry_run` jobs id is absent. `current_report` is generated but missing from `report-channels.json`.

## 1. Voice map (locked, unchanged from G1)

| Persona | Kokoro voice | Speed | Report kinds (G1 `speakers.KIND_AGENT`) |
| --- | --- | --- | --- |
| **Ava** (default) | `af_heart` | 1.0 | morning, midday, evening, late, summary, weather, nws, chime, official, boot |
| **Bruce** | `am_echo` | 1.0 | solar (incl. energy packs), system, remaining, hourly |
| **Carly** | `af_nova` | 1.0 | earthquake, kilauea, hurricane, alerts, security, bandwidth, net |

- Model: hexgrad **Kokoro-82M** (`kokoro-v1_0.pth`, sha256 `496dba118d1a58f5f3db2efc88dbdc216e0483fc89fe6e47ee1f2c53f18ad1e4`), kokoro **0.9.4**, misaki[en] **0.9.4**, torch **2.14.0+cpu**, spaCy `en_core_web_sm` 3.8.0, American English (`lang_code="a"`).
- Output: **24 kHz, 16-bit PCM, mono WAV**.
- Pronunciation: place names use English respells in `hawaiian_lexicon.py`. Kokoro is not fed IPA. As of 2026-09-30, `Hawaii` and `Hawaiian` stay those English words. As of 2026-10-02, Maui is `mao wee` and Honolulu is the plain name (spaced `hoh noh loo loo` dropped). News hour applies the same lexicon before render. The 2026-09-29 sheet still lists older syllable spellings: `07-Testing/2026-09-29-hawaiian-pronunciation-sheet.md`.
- **Grok has no Kokoro voice.** Cloud Ara is a gated route in Pacific `Media/CloudTTS` (WO-MIG-33). The default engine stays Kokoro. A live xAI call needs `RR_CLOUD_TTS=1` and `--speak`, and was not run.
- The G1 clip-stitch TTS path and the prebuilt G1 chime/phoneme clips are **not used**. The G3 phrase cache (§4) is new, rendered fresh with the same voices, and was approved by Alexander (2026-09-29 ~04:00 HST) as the one exception to "no stitching".

## 2. Paths

| What | Where | Git |
| --- | --- | --- |
| Code | Pacific `Media/Voice/scripts/` — `voice_generate.py` (engine: render / stitch / clips / asr), `voice-render.sh` (lock wrapper), `speakers.py` (personas, gate, retire), `speakable.py`, `hawaiian_lexicon.py`, `test_hawaiian_lexicon.py`, `clip_catalog.py`, `voice_asr_check.py`, `system_perf.py`, `voice_reports.py` (batch-2 report templates, stdlib), `compare_span.py` + `test_compare_span.py` (percent change vs yesterday/week/month), `status_cue.py` + `test_status_stack.py` (local status + stack closer), `radio_push.py` | tracked |
| Venv | Pacific `Media/Voice/.venv` (uv CPython 3.12, 1.3 GB, incl. openai-whisper for QC) | ignored (`.venv/`) |
| Model | Database `AI/Kokoro/Kokoro-82M/` (weights, config, all 54 voice packs; 340 MB; copied from G1, source untouched) | ignored (`/AI/Kokoro/Kokoro-82M/`, `*.pth`, `*.pt`) |
| ASR model | Database `AI/Whisper/tiny.pt` (72 MB, on-demand QC only) | ignored (`*.pt`) |
| espeak-ng data | `~/.local/share/rootrecord/espeak-ng-data` (19 MB copy of the venv's) — espeak-ng silently ignores data paths over 160 chars and the venv path under Pacific is 163. Override: `RR_ESPEAK_DATA` | outside repos |
| Live audio | Database `Media/Audio/Voice/<report>_current.wav`; non-git `test-reports/Voice/<report>_current.read.txt` + `.speak.txt` | WAV cache ignored; text sidecars non-git |
| History | Database `Media/Audio/Voice/Archive/<report>_YYYYMMDDTHHMM.wav`; sidecars in `test-reports/Voice/Archive/` | WAV cache ignored; text sidecars non-git |
| Phrase clips | Database `Media/Audio/Voice/Clips/<Persona>/<slug>.wav` | ignored (`*.wav`) |
| Compare ledger | Database `Reports/Comparisons/metrics.jsonl` (`compare_span.py`) | ignored with Database status paths |
| Stack-send state | Database `Reports/Voice/stack-send.json` (`status_cue.note_sent`) | ignored with Database status paths |
| Desk uptime / connectivity | Database `System/uptime/` (`uptime_log.py`; `RR_UPTIME_LOG`) | ignored with Database status paths |
| Host power-profile use | Database `System/power-profile/` (`power_profile.py`; read-only log) | ignored with Database status paths |
| Clip manifest | Database `Media/Audio/Voice/Clips/clips_manifest.json` | **tracked** |
| system_perf text | `test-reports/Voice/system_perf_current.md` → `test-reports/Voice/Archive/system_perf_YYYYMMDDTHHMM.md` (non-git) | non-git |
| Voice report text (batch 2) | `test-reports/Voice/<report>_current.md` → `test-reports/Voice/Archive/<report>_YYYYMMDDTHHMM.md` (WAV history remains in `Media/Audio/Voice/Archive/` as above) | non-git; Archive retained |

Env overrides: `RR_DATABASE_ROOT`, `RR_KOKORO_MODEL_DIR`, `RR_VOICE_OUT_DIR`, `RR_VOICE_REPORT_OUT`, `RR_VOICE_THREADS` (default 4 of 8 cores), `RR_VOICE_GAP_MS` (180), `RR_VOICE_PY`, `RR_WHISPER_DIR`, `RR_ESPEAK_DATA`. No `~/.ollama/skills/…`, `~/Media/…` or `/origin` paths remain.

## 3. How a render runs (performance rules)

`voice-render.sh <mode> …` → `single-flight.sh run voice:<mode>:<ts>` (the same inference lock as `run-infer.sh`; refuses with rc 75 when busy) → `nice -n 10 .venv/bin/python voice_generate.py …`. The model lives only inside that one process and is freed when it exits. There is no resident TTS server and no warmup. `HF_HUB_OFFLINE=1`, so nothing is fetched at render time.

- `render` — the whole text in one Kokoro pass (G1 behaviour). Measured: 4.6–5.1 s per one-sentence clip including model load, **peak RSS ≈ 1.24 GB**.
- `stitch` — the phrase cache (§4). If every sentence is cached, the model is **not loaded**: a chime took **0.2 s, 37 MB**.
- `clips --catalog [--persona P] [--only-missing]` — batch-render the catalog, one process per persona batch.
- `asr [--limit N]` — whisper-tiny round trip QC.

Retire pattern (G1 `_current` kept): the new WAV is rendered to a hidden temp file first. Only then is the old `<report>_current.wav` (and its sidecars) moved to `Archive/<report>_YYYYMMDDTHHMM.wav`, stamped with the old file's own mtime (HST), and the new file moved into place. A failed render never destroys the live copy.

Live-facts gate: G1 `speakers.is_live` is kept. Text with no live facts does not produce a WAV (`skipped: no_live_data`). `--no-gate` is for tests and for chimes (G1 chimes bypassed the gate too; spelled-out times have no digits).

## 4. Phrase-clip cache (stitcher)

- **Catalog** (`clip_catalog.py`): 68 clips in pass 1, **83** after batch 2 (2026-09-29 04:27–04:41): +9 fixed lines (Ava "State forecast for today./tonight.", "Morning/Midday/Late report.", "End of report.", "EcoFlow is offline."; Carly "Energy desk report."; Bruce "No open tasks on file.") + 6 **PROPOSED** pronunciation clips (`Ava/proposed_*`: Kalākaua, Liliʻuokalani A/B, Nuʻuanu, Māhele A/B; catalog `proposed: true`, explicit `spoken`; the stitcher never uses them; see 07-Testing `2026-09-29-pronunciation-candidates-proposed.md`). 83/83 format QC PASS. Pass-1 inventory: Ava 54 (48 half-hour chimes, "It's three p.m." etc., plus NWS/official/boot lines), Bruce 5 (hourly solar, EcoFlow offline, remaining tasks, system intro/outro), Carly 9 (quake none/intro, Kilauea intro + HVO notice, hurricane intro/quiet/outro, EcoFlow offline). Each entry names its G1 source template. Titles that carried a time in G1 ("Hawaii Earthquake Report at <time>.") are cached as the fixed sentence, and the time is spoken live as its own sentence.
- **Manifest** (`clips_manifest.json`, tracked): per clip `text`, `spoken`, `persona`, `voice`, `speed`, `sha256`, `duration_s`, `peak_dbfs`, `rms_dbfs`, `lead_silence_ms`, `trimmed_ms`, `qc`, `rendered` (ISO −10:00), engine versions, `source`, and `asr` (heard/score/verdict).
- **Stitch rule**: the text is split into sentences. A sentence whose exact text (case/space-normalized) matches a QC-PASS clip for that persona *and* voice is reused. Every other sentence (numbers, names, values), or any sentence whose clip is missing, is rendered live as a whole sentence. Joins: every part is trimmed (−45 dBFS, 25 ms kept), RMS-normalized on speech frames to **−20 dBFS**, peak-capped at **−1.5 dBFS**, 8 ms fades, **180 ms** silence between sentences (90 ms at the ends). Same 24 kHz / 16-bit / mono format as the clips.
- **Quality gate** (every clip): format 24000/1/PCM_16, duration > 0.2 s, peak < −1 dBFS, silence trimmed. Result: **68/68 PASS** (peak −6.7 … −2.0 dBFS, speech RMS −20.6 … −20.0 dBFS, 0.77–7.11 s). Whisper-tiny round trip: **59/68 match** (score ≥ 0.8). The 9 "review" clips are on the manual listen list in the QC test record: 2 chimes (02:00, noon) plus respelled Hawaiian names and NWS expansions that ASR can't judge.
- To re-render after a text change: `voice-render.sh clips --catalog --only-missing` (re-renders only changed or missing clips).

## 5. Reports: G1 → G3 map (inventory as of 2026-09-29; schedules corrected 2026-10-02 above)

| G1 report (job id) | G1 schedule (HST) | Persona | G3 data source | G3 output | Port status |
| --- | --- | --- | --- | --- | --- |
| system_perf (`system-performance`) | :22 and :52 (docstring still says :06; jobs.py wins) | Bruce | `/proc`, `/sys/class/power_supply`, `shutil.disk_usage`, host temperature in Celsius (`acpitz`); desk connectivity via `System/scripts/uptime_log.py` (Database `System/uptime/`); host power mode via `System/scripts/power_profile.py` (Database `System/power-profile/`, read-only) | `system_perf_current.wav` + `test-reports/Voice/system_perf_current.md` | **ON** in `run-poller.sh` (`RR_VOICE_SYSTEM_PERF=1`). Speaks Celsius, last-online / uptime% / avg offline / avg return when samples exist, and “Host power mode is …”. Uptime job `system_uptime_log` gated `RR_UPTIME_LOG` (default 1). Sandbox delivery when `RR_VOICE_DELIVER=1`. |
| hourly_chime (`time-chime`) | :00 and :30 | Ava, Bruce, Carly leapfrog by the hour | prebuilt `Media/Audio/Voice/Chimes/hour-00-00.wav` … `hour-23-30.wav` (48 files) | plays the file; no Kokoro at chime time | **:00 files rendered 2026-09-30. :30 files rendered the same day.** Job stays **OFF** until `RR_VOICE_HOURLY_CHIME=1` at poller start. |
| hourly-clip-reports (+ `hourly-clip-prebuild` :55) — solar / security / bandwidth desks | :22 / :52 (G3) | Bruce (combined energy+solar), Carly (security, bandwidth) | Database `Energy/{soc,watts}` last JSON + `Energy/sun/sun-times-last.json` + ch1 still + `Energy/vision/ch1-look-last.json`; `System/security/security-last.json`; `System/network/` samples | `solar_desk_current.wav`, `security_desk_current.wav`, `bandwidth_desk_current.wav` | **In `jobs.py` and ON** (`RR_VOICE_SOLAR`, `RR_VOICE_SECURITY`, `RR_VOICE_BANDWIDTH`, `RR_NET_SAMPLES`). `solar_desk` title “Energy and solar”; refreshes the hour’s camera look when needed. Bandwidth is not sent until a real byte window exists. |
| nws_hawaii (`nws-hawaii-counties`) | :07 :22 :37 :52 | Ava | Database `Weather/Hawai'i/hfo/api.weather.gov/alerts/active/area=HI/area=HI_current.json` + `Weather/Hawai'i/reports/0 Level Processing/sfp_state_forecast_current.md` (first period) | `nws_weather_current.wav` + `test-reports/Voice/nws_weather_current.md` | **ON** (`RR_VOICE_NWS=1`). Sandbox delivery. Per-county breakdown not ported. |
| official_weather_media | every 10 min | Ava | Database `Weather/Hawai'i/official/HLS_current.txt` (new `Weather/scripts/official_statement.py`, PROPOSED `RR_OFFICIAL_HLS` 600 s) else `Weather/Hawai'i/hfo/api.weather.gov/products/types/{HWO,AFD}/locations/HFO/HFO_current.txt` (weather poller); a product is used only if ≤ 24 h old | `official_weather_current.wav` | **LANDED 2026-09-29 14:28 HST** as `voice_reports.py official_weather` (header / UGC stripped, 4500-char cap, G1 no-statement wording). Text PASS (AFD path live; HLS + no-product paths unit-tested); WAV VERIFY PENDING. Job **PROPOSED, not in jobs.py** (`voice_official_weather`, `RR_VOICE_OFFICIAL`, :25). OBS overlay BLOCKED. [Test](../07-Testing/2026-09-29-old-repo-ports-breadth-batch5.md#official-weather-voice-report) |
| earthquake_hourly (+ `earthquake-m2-poll` 10 min) | :08 hourly | Carly | Pacific `Geology/scripts/geology_collect.py` → Database `Geology/Earthquakes/{hawaii,global}-last.json` | `earthquake_report_current.wav` | **ON** (`RR_VOICE_QUAKE=1`, `RR_GEOLOGY=1`). The per-quake Telegram post stays off (`RR_COUNCIL_QUAKE`). |
| council_quake | every 2 min | Carly | same as above | `council_quake_current.wav` | **BLOCKED** — delivery-bound (G1 fed the Telegram council); data now exists (2026-09-29), not ported. Needs sign-off for Telegram |
| hurricane_desk (+ evening) | 05/09/12/20 :50, 16:55 | Carly | Database `Weather/Hawai'i/hurricanes/tracking/*/track.json` (weather poller, NHC CurrentStorms, Hawaiʻi-relevant only) + NWS HI alerts | `hurricane_desk_current.wav` | **LANDED 2026-09-29 13:43 HST** as `voice_reports.py hurricane_desk` (G1 Hawaiʻi block; global JTWC/RAMMB board not in G3). Text PASS; WAV VERIFY PENDING. Job `voice_hurricane_desk` gated `RR_VOICE_HURRICANE=1`. [Test](../07-Testing/2026-09-29-voice-reports-batch3-hurricane-kilauea.md) |
| kilauea (hourly Kīlauea desk) | :03 | Carly | Database `Geology/Volcanoes/{kilauea,mauna-loa}-last.json` + `Geology/Earthquakes/hawaii-last.json` | `kilauea_report_current.wav` | **ON** (`RR_VOICE_KILAUEA=1`). Spoken place names, no raw JSON. The public draft queue stays separately gated. |
| energy_report (retired into `solar_desk`) | was :12/:42 (retired before :22/:52 move) | was Carly | same Energy sources; content now in Bruce `solar_desk` | n/a (alias forwards) | **Retired 2026-10-02 ~01:41 HST.** Job and `RR_VOICE_ENERGY` removed from `jobs.py` / `run-poller.sh`. `b_energy_report` is a one-release alias to `b_solar_desk`. Discord `energy-report` channel row and public Energy area slug removed; use `solar-desk`. Generator / out-of-range / powered-off rules still apply inside `solar_desk`. |
| remaining_tasks | :32 hourly | Bruce | `Reports/scripts/report_board.py status` | `remaining_tasks_current.wav` | **ON** (`RR_VOICE_REMAINING=1`). Speaks open slots in the next hour. |
| morning / midday / late reports (+ `_play`, slots, merged-morning 10:20) | 09:00, 12:00, 21:00 (G3: 09:02 / 12:02 / 21:02) | Ava | Energy + Weather (alerts + SFP) + host `/proc` + work-order count | `morning_report_current.wav`, `midday_report_current.wav`, `late_report_current.wav` + `test-reports/Voice/*_current.md` | **LANDED, PASS**, template-first, gated OFF (`RR_VOICE_ROLLUPS=1`). Optional one-line LLM summary through `run-infer.sh` (`RR_VOICE_ROLLUP_LLM=1`, caller `voice_rollup`, lengths-only log) PASS once. Optional cloud prose is `Reports/CloudNarrative` (WO-MIG-32): dry-run package, no socket; merged copies today's morning narrative and does not call the model again; live spend still needs sign-off. G1 `day` (18:00) not ported (**PROPOSED**). 23:30 late-final is the same late roll-up, a second chance, gated OFF (`RR_VOICE_LATE_FINAL=1`, text only) |
| boot_brief / audio_request (`boot_prelims`) | on boot | Ava (boot) | `/proc/uptime`, `/proc` CPU/mem, Energy last JSON, NWS HI alerts, Geology Kīlauea last JSON, hurricane `track.json` | `boot_brief_current.wav` | **LANDED 2026-09-29 14:29 HST** as `voice_reports.py boot_brief` (morning edition before 12:00, midday after). Text PASS; WAV VERIFY PENDING. Job **PROPOSED, not in jobs.py** (ON_BOOT `voice_boot_brief`, `RR_VOICE_BOOT`, runs `geology_collect` first). Morning replay is `Media/MorningBootReplay/scripts/replay.py` (dry-run handoff to `Media/Playback`; speakers off). Sunrise restore LANDED 2026-09-30 as `Media/SunriseRestore` (request only, no speaker). [Test](../07-Testing/2026-09-29-old-repo-ports-breadth-batch5.md#boot-brief-voice-report) |

## 6. Gates, as of 2026-09-30 (history — see Current as of 2026-10-02 above)

The schedule and which flags default on are in [2026-09-30 voice desk](../01-Operations/2026-09-30-voice-desk.md). Flags are read when the poller starts.

Telegram delivery is on (`RR_VOICE_DELIVER=1`). `run-poller.sh` sets `RR_TELEGRAM_DEST=council` (voice note and measured report). Unchanged spoken text is not sent again. Speaker playback stays dry-run unless `RR_PLAYBACK=1` and `--play`.

Earthquake and hurricane voice reports are Pacific poller jobs. They are not the Mainland globe. The desk still writes WAV. The Mainland station library is a different file. Hawaii still renders a WAV. `Media/Voice/scripts/radio_push.py` encodes that one report to Opus and replaces `<report>_current.opus` on `/home/ubuntu/rootrecord-radio`. Reports in that library are 24 kbps mono Opus. Chimes there are `hour-HH-MM.opus` at 48 kbps. Music there is `.opus` at 96 kbps. The public mix is `https://radio.rootrecord.cloud/radio/live.mp3` (`audio/mpeg`, 128 kbps). The Opus music bed is on the live Mainland host. Only the current Hawaii daypart rollup is saved and pushed: morning 09:00–12:00, midday 12:00–21:00, late 21:00–09:00. The runtime deletes the other two daypart files when the current one arrives. `RR_RADIO_SSH` is `ml1`.

`voice_solar_desk`, `voice_security_desk`, and `voice_bandwidth_desk` are in `jobs.py` and default on. `voice_hourly_chime` is :00 and :30 and stays off until `RR_VOICE_HOURLY_CHIME=1` (that flag is still not in `run-poller.sh`). `official_weather` and `boot_brief` still have no `jobs.py` entry. `reports_board_catchup` stays gated. **Correction 2026-10-02:** roll-ups (`RR_VOICE_ROLLUPS`), late-final (`RR_VOICE_LATE_FINAL`), and hurricane (`RR_VOICE_HURRICANE`) default to 1 in `run-poller.sh` and are armed. See the Current section above.

If the single-flight lock is busy, the text file is still written and the WAV is skipped (rc 75).

- **Text fixes 2026-09-29 14:18 HST** (breadth pass 2): `speakable.spoken_clock` says minutes 1–9 as "oh N". `voice_reports.spoken_watts` says "zero watts" / "one watt". `spoken_hhmm` speaks sun times as words. [Test](../07-Testing/2026-09-29-old-repo-ports-breadth-batch5.md#voice-text-fixes).
- **2026-09-30:** Hawaii and Hawaiian are the English words. Host temperature is Celsius. A bare "degrees" with no unit is still Fahrenheit, for the weather numbers. `speech_scrub.py` is still not wired into a report.

## 7. Naming and formats standard — **PROPOSED**

Based on the conventions already in the Database: Weather `_current` + `archived/`, and automations `Logs/Automations/automations_current.log` + `Archive/automations_YYYY-MM-DD_HH00.log`. **Existing live files are not renamed.**

| Rule | Standard | Example |
| --- | --- | --- |
| Folders | Title-case (Database; Pacific top-level domains) | `Media/Audio/Voice/Clips/Ava/` |
| Live file | `<name>_current.<ext>`, name in lower_snake_case | `system_perf_current.wav`, `inference_current.jsonl` |
| History | `Archive/<name>_YYYYMMDDTHHMM.<ext>` (moment the live copy was made, HST) | `Archive/system_perf_20260929T0410.wav` |
| Rotated logs | `Archive/<name>_YYYY-MM-DD.<ext>` (daily) or `_YYYY-MM-DD_HH00` (hourly, existing automations) | `Archive/inference_2026-09-29.jsonl` |
| Timestamps | ISO 8601 with offset `-10:00` | `2026-09-29T04:10:57-10:00` |
| Machine logs | JSONL, one object per line, metadata only | `Logs/AI/Inference/…` |
| Reports | Markdown | `test-reports/AI-Processing/ai-processing-report_current.md` |
| Audio | 24 kHz 16-bit mono WAV in Database; `.read.txt` / `.speak.txt` sidecars in non-git `test-reports/Voice/` | WAV cache and model weights are git-ignored |

Existing exceptions, kept as they are: `ai-processing-report_current.md` (hyphenated name, as specified), `Archive/ai-processing-report_YYYY-MM-DDTHHMM.md`, Weather `archived/`, G2/G1 names.
