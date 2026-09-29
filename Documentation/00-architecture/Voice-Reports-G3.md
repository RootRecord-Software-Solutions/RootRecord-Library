# Voice Reports — G3 (Kokoro-82M port + phrase-clip cache)

| Field | Value |
| --- | --- |
| **Date (HST)** | 2026-09-29 (overnight build, 03:50–04:20 HST) |
| **State** | Engine **LANDED + PASS** · phrase cache **LANDED + PASS** (by-ear **VERIFY PENDING**) · `system_perf` **LANDED, gated OFF** · delivery **OFF** pending Alexander sign-off |
| **Backup** | `/home/rootrecord/Database/GITHUB/g3-voice-ailog.bak-20260929-035454/` |
| **Tests** | `07-testing/2026-09-29-kokoro-voice-port-g3.md` · `07-testing/2026-09-29-kokoro-phrase-clips-qc.md` · `07-testing/2026-09-29-hawaiian-pronunciation-sheet.md` |

## 1. Voice map (locked, unchanged from G1)

| Persona | Kokoro voice | Speed | Report kinds (G1 `speakers.KIND_AGENT`) |
| --- | --- | --- | --- |
| **Ava** (default) | `af_heart` | 0.82 | morning, midday, evening, late, summary, weather, nws, chime, official, boot |
| **Bruce** | `am_echo` | 0.92 | solar, system, remaining, hourly |
| **Carly** | `af_nova` | 0.74 | energy, earthquake, kilauea, hurricane, alerts, security, bandwidth, net |

- Model: hexgrad **Kokoro-82M** (`kokoro-v1_0.pth`, sha256 `496dba118d1a58f5f3db2efc88dbdc216e0483fc89fe6e47ee1f2c53f18ad1e4`), kokoro **0.9.4**, misaki[en] **0.9.4**, torch **2.14.0+cpu**, spaCy `en_core_web_sm` 3.8.0, American English (`lang_code="a"`).
- Output: **24 kHz, 16-bit PCM, mono WAV**.
- Pronunciation: Ava/Ayeva/Avaivy fixes (`ˈAvə`, `ˈAvəˈIvi`) + G1 `hawaiian_lexicon.py` / `speakable.py` copied verbatim (99 place names respelled to plain English; Kokoro is never fed IPA). Sheet: `07-testing/2026-09-29-hawaiian-pronunciation-sheet.md`.
- **Grok has no Kokoro voice** (cloud Ara retired). Not mapped — **open question for Alexander**.
- The G1 clip-stitch TTS path and the prebuilt G1 chime/phoneme clips are **not used**. The G3 phrase cache (§4) is new, rendered fresh with the same voices, and was approved by Alexander (2026-09-29 ~04:00 HST) as the one exception to "no stitching".

## 2. Paths

| What | Where | Git |
| --- | --- | --- |
| Code | Pacific `Media/Voice/scripts/` — `voice_generate.py` (engine: render / stitch / clips / asr), `voice-render.sh` (lock wrapper), `speakers.py` (personas, gate, retire), `speakable.py`, `hawaiian_lexicon.py`, `test_hawaiian_lexicon.py`, `clip_catalog.py`, `voice_asr_check.py`, `system_perf.py` | tracked |
| Venv | Pacific `Media/Voice/.venv` (uv CPython 3.12, 1.3 GB, incl. openai-whisper for QC) | ignored (`.venv/`) |
| Model | Database `AI/Kokoro/Kokoro-82M/` (weights, config, all 54 voice packs; 340 MB; copied from G1, source untouched) | ignored (`/AI/Kokoro/Kokoro-82M/`, `*.pth`, `*.pt`) |
| ASR model | Database `AI/Whisper/tiny.pt` (72 MB, on-demand QC only) | ignored (`*.pt`) |
| espeak-ng data | `~/.local/share/rootrecord/espeak-ng-data` (19 MB copy of the venv's) — espeak-ng silently ignores data paths over 160 chars and the venv path under Pacific is 163. Override: `RR_ESPEAK_DATA` | outside repos |
| Live audio | Database `Media/Audio/Voice/<report>_current.wav` + `.read.txt` (text as written) + `.speak.txt` (text as spoken) | WAV ignored; sidecars tracked (small) |
| History | Database `Media/Audio/Voice/Archive/<report>_YYYYMMDDTHHMM.wav` (+ sidecars) | ignored (`/Media/Audio/Voice/Archive/`) |
| Phrase clips | Database `Media/Audio/Voice/Clips/<Persona>/<slug>.wav` | ignored (`*.wav`) |
| Clip manifest | Database `Media/Audio/Voice/Clips/clips_manifest.json` | **tracked** |
| system_perf text | Database `System/Reports/system_perf_current.md` → `Archive/system_perf_YYYYMMDDTHHMM.md` | tracked |

Env overrides: `RR_DATABASE_ROOT`, `RR_KOKORO_MODEL_DIR`, `RR_VOICE_OUT_DIR`, `RR_VOICE_THREADS` (default 4 of 8 cores), `RR_VOICE_GAP_MS` (180), `RR_VOICE_PY`, `RR_WHISPER_DIR`, `RR_ESPEAK_DATA`. No `~/.ollama/skills/…`, `~/Media/…` or `/origin` paths remain.

## 3. How a render runs (performance rules)

`voice-render.sh <mode> …` → `single-flight.sh run voice:<mode>:<ts>` (the same inference lock as `run-infer.sh`; refuses with rc 75 when busy) → `nice -n 10 .venv/bin/python voice_generate.py …`. The model lives only inside that one process and is freed when it exits. There is no resident TTS server and no warmup. `HF_HUB_OFFLINE=1`, so nothing is fetched at render time.

- `render` — the whole text in one Kokoro pass (G1 behaviour). Measured: 4.6–5.1 s per one-sentence clip including model load, **peak RSS ≈ 1.24 GB**.
- `stitch` — the phrase cache (§4). If every sentence is cached, the model is **not loaded**: a chime took **0.2 s, 37 MB**.
- `clips --catalog [--persona P] [--only-missing]` — batch-render the catalog, one process per persona batch.
- `asr [--limit N]` — whisper-tiny round trip QC.

Retire pattern (G1 `_current` kept): the new WAV is rendered to a hidden temp file first. Only then is the old `<report>_current.wav` (and its sidecars) moved to `Archive/<report>_YYYYMMDDTHHMM.wav`, stamped with the old file's own mtime (HST), and the new file moved into place. A failed render never destroys the live copy.

Live-facts gate: G1 `speakers.is_live` is kept. Text with no live facts does not produce a WAV (`skipped: no_live_data`). `--no-gate` is for tests and for chimes (G1 chimes bypassed the gate too; spelled-out times have no digits).

## 4. Phrase-clip cache (stitcher)

- **Catalog** (`clip_catalog.py`): 68 clips. Ava 54 (48 half-hour chimes, "It's three p.m." etc., plus NWS/official/boot lines), Bruce 5 (hourly solar, EcoFlow offline, remaining tasks, system intro/outro), Carly 9 (quake none/intro, Kilauea intro + HVO notice, hurricane intro/quiet/outro, EcoFlow offline). Each entry names its G1 source template. Titles that carried a time in G1 ("Hawaii Earthquake Report at <time>.") are cached as the fixed sentence, and the time is spoken live as its own sentence.
- **Manifest** (`clips_manifest.json`, tracked): per clip `text`, `spoken`, `persona`, `voice`, `speed`, `sha256`, `duration_s`, `peak_dbfs`, `rms_dbfs`, `lead_silence_ms`, `trimmed_ms`, `qc`, `rendered` (ISO −10:00), engine versions, `source`, and `asr` (heard/score/verdict).
- **Stitch rule**: the text is split into sentences. A sentence whose exact text (case/space-normalized) matches a QC-PASS clip for that persona *and* voice is reused. Every other sentence (numbers, names, values), or any sentence whose clip is missing, is rendered live as a whole sentence. Joins: every part is trimmed (−45 dBFS, 25 ms kept), RMS-normalized on speech frames to **−20 dBFS**, peak-capped at **−1.5 dBFS**, 8 ms fades, **180 ms** silence between sentences (90 ms at the ends). Same 24 kHz / 16-bit / mono format as the clips.
- **Quality gate** (every clip): format 24000/1/PCM_16, duration > 0.2 s, peak < −1 dBFS, silence trimmed. Result: **68/68 PASS** (peak −6.7 … −2.0 dBFS, speech RMS −20.6 … −20.0 dBFS, 0.77–7.11 s). Whisper-tiny round trip: **59/68 match** (score ≥ 0.8). The 9 "review" clips are on the manual listen list in the QC test record: 2 chimes (02:00, noon) plus respelled Hawaiian names and NWS expansions that ASR can't judge.
- To re-render after a text change: `voice-render.sh clips --catalog --only-missing` (re-renders only changed or missing clips).

## 5. Reports: G1 → G3 map

| G1 report (job id) | G1 schedule (HST) | Persona | G3 data source | G3 output | Port status |
| --- | --- | --- | --- | --- | --- |
| system_perf (`system-performance`) | :06 hourly | Bruce | `/proc`, `/sys/class/power_supply`, `shutil.disk_usage` (stdlib) | `system_perf_current.wav` + `System/Reports/system_perf_current.md` | **LANDED, PASS**, gated OFF (`RR_VOICE_SYSTEM_PERF=1`) |
| hourly_chime (`time-chime`) | :00 / :30 | Ava | clock only | `hourly_chime_current.wav` | clips 48/48 cached, stitch **PASS**. Job **PROPOSED**: it only makes sense with playback |
| hourly-clip-reports (+ `hourly-clip-prebuild` :55) | :02 hourly | Bruce (hourly/solar) | Database `Energy/` (soc, watts last JSON) + Weather | `hourly_solar_current.wav` | **PROPOSED** (rebuild as template + stitch, not G1 clip-stitch) |
| nws_hawaii (`nws-hawaii-counties`) | :07 :22 :37 :52 | Ava | Database `Weather/Hawai'i/` (Pacific weather poller) | `nws_hawaii_current.wav` | **PROPOSED**; intro/county/no-alerts clips cached |
| official_weather_media | every 10 min | Ava | `Weather/Hawai'i/hurricanes` + NWS products | `official_weather_current.wav` | **PROPOSED**; no-statement clip cached |
| earthquake_hourly (+ `earthquake-m2-poll` 10 min) | :08 hourly | Carly | Pacific `Geology` domain (USGS) → Database `Geology/` (empty today) | `earthquake_hourly_current.wav` | **PROPOSED**; intro/none clips cached |
| council_quake | every 2 min | Carly | same as above | `council_quake_current.wav` | **PROPOSED** (G1 fed the Telegram council, so delivery-bound) |
| hurricane_desk (+ evening) | 05/09/12/20 :50, 16:55 | Carly | `Weather/Hawai'i/hurricanes` | `hurricane_desk_current.wav` | **PROPOSED**; intro/quiet/outro clips cached |
| energy_report | every 30 min | Carly | Database `Energy/` (Delta 2 / River 2 Pro last JSON) | `energy_report_current.wav` | **PROPOSED** |
| remaining_tasks | :32 hourly | Bruce | Library work orders / Database `Worklog/` | `remaining_tasks_current.wav` | **PROPOSED** (G3 task source not defined) |
| morning / midday / late / day reports (+ `_play`, slots, merged-morning 10:20) | 09:00 (+:05, 09:10), 12:00 (+12:05, 13:00), 18:00, 21:00 (+21:08), 23:30 | Ava | Energy + Weather + System + Worklog | `morning_report_current.wav`, `midday_report_current.wav`, `late_report_current.wav`, … | **PROPOSED**: G1 wrote these with an LLM, so they need a `run-infer.sh` route decision first |
| boot_brief / audio_request (`boot_prelims`) | on boot | Ava (boot) | System + Energy last JSON | `boot_brief_current.wav` | **PROPOSED**; boot status clips cached |

## 6. Gates, and what enabling needs

- `voice_system_perf` job (Pacific `Automations/scripts/jobs.py`, EVERY_MINUTE `only_at_minutes=[6]`): `enabled = RR_VOICE_SYSTEM_PERF == "1"`. The flag is read once, when the poller imports `jobs.py`, so it **takes effect only at the next poller start** and does nothing tonight. It writes text + WAV and **delivers nothing**.
- **Delivery is OFF** everywhere: no Telegram `sendVoice`, no AWS radio push (G1 `_push_aws_radio`/`publish_current` were deliberately not ported), and no speaker playback. Enabling needs Alexander's sign-off plus:
  1. **Telegram**: a sendVoice step that converts WAV → OGG/Opus (the Bot API wants OGG/Opus for voice notes; the OGG goes in git-ignored `Archive/`), wired through the existing council relay / `Communications/telegram` (single `getUpdates` owner). It must not send when unchanged or when the gate skips.
  2. **Speakers**: a playback step (e.g. `pw-play`/`aplay`) behind its own flag, with quiet hours and a queue so two reports never overlap.
- Scheduled report jobs other than `system_perf` are not added (see §5).

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
| Reports | Markdown | `Logs/AI/Reports/ai-processing-report_current.md` |
| Audio | 24 kHz 16-bit mono WAV + `.read.txt` / `.speak.txt` sidecars. Audio and model weights are git-ignored | — |

Existing exceptions, kept as they are: `ai-processing-report_current.md` (hyphenated name, as specified), `Archive/ai-processing-report_YYYY-MM-DDTHHMM.md`, Weather `archived/`, G2/G1 names.
