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
- **Grok has no Kokoro voice.** Cloud Ara is a gated route in Pacific `Media/CloudTTS` (WO-MIG-33). The default engine stays Kokoro. A live xAI call needs `RR_CLOUD_TTS=1` and `--speak`, and was not run.
- The G1 clip-stitch TTS path and the prebuilt G1 chime/phoneme clips are **not used**. The G3 phrase cache (§4) is new, rendered fresh with the same voices, and was approved by Alexander (2026-09-29 ~04:00 HST) as the one exception to "no stitching".

## 2. Paths

| What | Where | Git |
| --- | --- | --- |
| Code | Pacific `Media/Voice/scripts/` — `voice_generate.py` (engine: render / stitch / clips / asr), `voice-render.sh` (lock wrapper), `speakers.py` (personas, gate, retire), `speakable.py`, `hawaiian_lexicon.py`, `test_hawaiian_lexicon.py`, `clip_catalog.py`, `voice_asr_check.py`, `system_perf.py`, `voice_reports.py` (batch-2 report templates, stdlib) | tracked |
| Venv | Pacific `Media/Voice/.venv` (uv CPython 3.12, 1.3 GB, incl. openai-whisper for QC) | ignored (`.venv/`) |
| Model | Database `AI/Kokoro/Kokoro-82M/` (weights, config, all 54 voice packs; 340 MB; copied from G1, source untouched) | ignored (`/AI/Kokoro/Kokoro-82M/`, `*.pth`, `*.pt`) |
| ASR model | Database `AI/Whisper/tiny.pt` (72 MB, on-demand QC only) | ignored (`*.pt`) |
| espeak-ng data | `~/.local/share/rootrecord/espeak-ng-data` (19 MB copy of the venv's) — espeak-ng silently ignores data paths over 160 chars and the venv path under Pacific is 163. Override: `RR_ESPEAK_DATA` | outside repos |
| Live audio | Database `Media/Audio/Voice/<report>_current.wav`; non-git `test-reports/Voice/<report>_current.read.txt` + `.speak.txt` | WAV cache ignored; text sidecars non-git |
| History | Database `Media/Audio/Voice/Archive/<report>_YYYYMMDDTHHMM.wav`; sidecars in `test-reports/Voice/Archive/` | WAV cache ignored; text sidecars non-git |
| Phrase clips | Database `Media/Audio/Voice/Clips/<Persona>/<slug>.wav` | ignored (`*.wav`) |
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

- **Catalog** (`clip_catalog.py`): 68 clips in pass 1, **83** after batch 2 (2026-09-29 04:27–04:41): +9 fixed lines (Ava "State forecast for today./tonight.", "Morning/Midday/Late report.", "End of report.", "EcoFlow is offline."; Carly "Energy desk report."; Bruce "No open tasks on file.") + 6 **PROPOSED** pronunciation clips (`Ava/proposed_*`: Kalākaua, Liliʻuokalani A/B, Nuʻuanu, Māhele A/B; catalog `proposed: true`, explicit `spoken`; the stitcher never uses them; see 07-testing `2026-09-29-pronunciation-candidates-proposed.md`). 83/83 format QC PASS. Pass-1 inventory: Ava 54 (48 half-hour chimes, "It's three p.m." etc., plus NWS/official/boot lines), Bruce 5 (hourly solar, EcoFlow offline, remaining tasks, system intro/outro), Carly 9 (quake none/intro, Kilauea intro + HVO notice, hurricane intro/quiet/outro, EcoFlow offline). Each entry names its G1 source template. Titles that carried a time in G1 ("Hawaii Earthquake Report at <time>.") are cached as the fixed sentence, and the time is spoken live as its own sentence.
- **Manifest** (`clips_manifest.json`, tracked): per clip `text`, `spoken`, `persona`, `voice`, `speed`, `sha256`, `duration_s`, `peak_dbfs`, `rms_dbfs`, `lead_silence_ms`, `trimmed_ms`, `qc`, `rendered` (ISO −10:00), engine versions, `source`, and `asr` (heard/score/verdict).
- **Stitch rule**: the text is split into sentences. A sentence whose exact text (case/space-normalized) matches a QC-PASS clip for that persona *and* voice is reused. Every other sentence (numbers, names, values), or any sentence whose clip is missing, is rendered live as a whole sentence. Joins: every part is trimmed (−45 dBFS, 25 ms kept), RMS-normalized on speech frames to **−20 dBFS**, peak-capped at **−1.5 dBFS**, 8 ms fades, **180 ms** silence between sentences (90 ms at the ends). Same 24 kHz / 16-bit / mono format as the clips.
- **Quality gate** (every clip): format 24000/1/PCM_16, duration > 0.2 s, peak < −1 dBFS, silence trimmed. Result: **68/68 PASS** (peak −6.7 … −2.0 dBFS, speech RMS −20.6 … −20.0 dBFS, 0.77–7.11 s). Whisper-tiny round trip: **59/68 match** (score ≥ 0.8). The 9 "review" clips are on the manual listen list in the QC test record: 2 chimes (02:00, noon) plus respelled Hawaiian names and NWS expansions that ASR can't judge.
- To re-render after a text change: `voice-render.sh clips --catalog --only-missing` (re-renders only changed or missing clips).

## 5. Reports: G1 → G3 map

| G1 report (job id) | G1 schedule (HST) | Persona | G3 data source | G3 output | Port status |
| --- | --- | --- | --- | --- | --- |
| system_perf (`system-performance`) | :06 hourly | Bruce | `/proc`, `/sys/class/power_supply`, `shutil.disk_usage` (stdlib) | `system_perf_current.wav` + `test-reports/Voice/system_perf_current.md` | **LANDED, PASS**, gated OFF (`RR_VOICE_SYSTEM_PERF=1`) |
| hourly_chime (`time-chime`) | :00 / :30 | Ava | clock only | `hourly_chime_current.wav` + `Reports/hourly_chime_current.md` | **LANDED, PASS** (fully cached, no model load, 0.3 s), gated OFF (`RR_VOICE_HOURLY_CHIME=1`). Useful mainly once playback exists |
| hourly-clip-reports (+ `hourly-clip-prebuild` :55) — solar / security / bandwidth desks | :02 hourly (G3 :04 / :11 / :12) | Bruce (solar), Carly (security, bandwidth) | Database `Energy/{soc,watts}` last JSON + `Energy/sun/sun-times-last.json`; `System/security/security-last.json` (host_desks.py); `System/network/` samples (host_desks.py net-sample) | `solar_desk_current.wav`, `security_desk_current.wav`, `bandwidth_desk_current.wav` | **LANDED 2026-09-29 14:01 HST** as `voice_reports.py solar_desk \| security_desk \| bandwidth_desk` (template, not G1 clip-stitch). Text PASS; WAV VERIFY PENDING. Jobs **PROPOSED, not in jobs.py** (`RR_VOICE_SOLAR`, `RR_VOICE_SECURITY`, `RR_VOICE_BANDWIDTH`) — [blocks](./Pending-Job-Registrations-2026-09-29.md). [Test](../07-testing/2026-09-29-old-repo-ports-breadth-batch4.md) |
| nws_hawaii (`nws-hawaii-counties`) | :07 :22 :37 :52 | Ava | Database `Weather/Hawai'i/hfo/api.weather.gov/alerts/active/area=HI/area=HI_current.json` + `Weather/Hawai'i/reports/0 Level Processing/sfp_state_forecast_current.md` (first period) | `nws_weather_current.wav` + `test-reports/Voice/nws_weather_current.md` | **LANDED, PASS** (report id `nws_weather`), gated OFF (`RR_VOICE_NWS=1`). Per-county breakdown not ported (API sample is state-wide) |
| official_weather_media | every 10 min | Ava | Database `Weather/Hawai'i/official/HLS_current.txt` (new `Weather/scripts/official_statement.py`, PROPOSED `RR_OFFICIAL_HLS` 600 s) else `Weather/Hawai'i/hfo/api.weather.gov/products/types/{HWO,AFD}/locations/HFO/HFO_current.txt` (weather poller); a product is used only if ≤ 24 h old | `official_weather_current.wav` | **LANDED 2026-09-29 14:28 HST** as `voice_reports.py official_weather` (header / UGC stripped, 4500-char cap, G1 no-statement wording). Text PASS (AFD path live; HLS + no-product paths unit-tested); WAV VERIFY PENDING. Job **PROPOSED, not in jobs.py** (`voice_official_weather`, `RR_VOICE_OFFICIAL`, :25). OBS overlay BLOCKED. [Test](../07-testing/2026-09-29-old-repo-ports-breadth-batch5.md#official-weather-voice-report) |
| earthquake_hourly (+ `earthquake-m2-poll` 10 min) | :08 hourly | Carly | Pacific `Geology/scripts/geology_collect.py` (USGS FDSN Hawaiʻi bbox + 2.5_day global) → Database `Geology/Earthquakes/{hawaii,global}-last.json` | `earthquake_report_current.wav` | **LANDED 2026-09-29 13:20 HST** as `voice_reports.py earthquake_report` (new-since-last-report via `earthquake_report_seen.json`; `RR_VOICE_QUAKE_DRY=1` skips the state write). Text PASS (`--no-voice`, temp output); WAV + by-ear **VERIFY PENDING**. Job `voice_earthquake_report` gated `RR_VOICE_QUAKE=1`; needs `RR_GEOLOGY=1` for fresh data. The M2 10-min poll is covered by the collector's 300 s pull (new ≥M2 ids in `hawaii-last.json`); its Telegram post stays BLOCKED. The Discord text post is `Geology/Earthquake-Discord` (dry-run 2026-09-30, job gated `RR_EARTHQUAKE_DISCORD=1`, live send still sign-off). Test: [07-testing](../07-testing/2026-09-29-geology-earthquakes-hvo-collector.md) |
| council_quake | every 2 min | Carly | same as above | `council_quake_current.wav` | **BLOCKED** — delivery-bound (G1 fed the Telegram council); data now exists (2026-09-29), not ported. Needs sign-off for Telegram |
| hurricane_desk (+ evening) | 05/09/12/20 :50, 16:55 | Carly | Database `Weather/Hawai'i/hurricanes/tracking/*/track.json` (weather poller, NHC CurrentStorms, Hawaiʻi-relevant only) + NWS HI alerts | `hurricane_desk_current.wav` | **LANDED 2026-09-29 13:43 HST** as `voice_reports.py hurricane_desk` (G1 Hawaiʻi block; global JTWC/RAMMB board not in G3). Text PASS; WAV VERIFY PENDING. Job `voice_hurricane_desk` gated `RR_VOICE_HURRICANE=1`. [Test](../07-testing/2026-09-29-voice-reports-batch3-hurricane-kilauea.md) |
| kilauea (hourly Kīlauea desk; G1 `hourly-clip-reports` + `rr-kilauea`) | :02 hourly (G3 :03) | Carly | Database `Geology/Volcanoes/{kilauea,mauna-loa}-last.json` + `Geology/Earthquakes/hawaii-last.json` | `kilauea_report_current.wav` | **LANDED 2026-09-29 13:43 HST** as `voice_reports.py kilauea_report` (template desk + HVO notice excerpt). Text PASS; WAV VERIFY PENDING. Job `voice_kilauea_report` gated `RR_VOICE_KILAUEA=1`. Optional cloud prose is `Reports/CloudNarrative` (WO-MIG-32, dry-run; spend still sign-off). The public draft queue is separate: `Geology/PublicDraftQueue` (job `geology_kilauea_public_draft`, gated `RR_KILAUEA_DRAFT`, no send). [Test](../07-testing/2026-09-29-voice-reports-batch3-hurricane-kilauea.md) |
| energy_report | every 30 min | Carly | Database `Energy/soc/{delta2,river2pro}-last.json` + `Energy/watts/…-last.json` (EcoFlow BLE) | `energy_report_current.wav` + `test-reports/Voice/energy_report_current.md` | **LANDED, PASS**, gated OFF (`RR_VOICE_ENERGY=1`) at :15/:45. Vision caption skipped (as asked). Stale (> 30 min) readings are said as such |
| remaining_tasks | :32 hourly | Bruce | Library `06-development/Work-Orders/*.md` unchecked `- [ ]` boxes (27 in 9 work orders today) | `remaining_tasks_current.wav` + `test-reports/Voice/remaining_tasks_current.md` | **LANDED, PASS**, gated OFF (`RR_VOICE_REMAINING=1`). Reads the Library read-only |
| morning / midday / late reports (+ `_play`, slots, merged-morning 10:20) | 09:00, 12:00, 21:00 (G3: 09:02 / 12:02 / 21:02) | Ava | Energy + Weather (alerts + SFP) + host `/proc` + work-order count | `morning_report_current.wav`, `midday_report_current.wav`, `late_report_current.wav` + `test-reports/Voice/*_current.md` | **LANDED, PASS**, template-first, gated OFF (`RR_VOICE_ROLLUPS=1`). Optional one-line LLM summary through `run-infer.sh` (`RR_VOICE_ROLLUP_LLM=1`, caller `voice_rollup`, lengths-only log) PASS once. Optional cloud prose is `Reports/CloudNarrative` (WO-MIG-32): dry-run package, no socket; merged copies today's morning narrative and does not call the model again; live spend still needs sign-off. G1 `day` (18:00) not ported (**PROPOSED**). 23:30 late-final is the same late roll-up, a second chance, gated OFF (`RR_VOICE_LATE_FINAL=1`, text only) |
| boot_brief / audio_request (`boot_prelims`) | on boot | Ava (boot) | `/proc/uptime`, `/proc` CPU/mem, Energy last JSON, NWS HI alerts, Geology Kīlauea last JSON, hurricane `track.json` | `boot_brief_current.wav` | **LANDED 2026-09-29 14:29 HST** as `voice_reports.py boot_brief` (morning edition before 12:00, midday after). Text PASS; WAV VERIFY PENDING. Job **PROPOSED, not in jobs.py** (ON_BOOT `voice_boot_brief`, `RR_VOICE_BOOT`, runs `geology_collect` first). Morning replay is `Media/MorningBootReplay/scripts/replay.py` (dry-run handoff to `Media/Playback`; speakers off). Sunrise restore LANDED 2026-09-30 as `Media/SunriseRestore` (request only, no speaker). [Test](../07-testing/2026-09-29-old-repo-ports-breadth-batch5.md#boot-brief-voice-report) |

## 6. Gates, and what enabling needs

- `voice_system_perf` job (Pacific `Automations/scripts/jobs.py`, EVERY_MINUTE `only_at_minutes=[6]`): `enabled = RR_VOICE_SYSTEM_PERF == "1"`. The flag is read once, when the poller imports `jobs.py`, so it **takes effect only at the next poller start** and does nothing tonight. It writes text + WAV and **delivers nothing**.
- **Telegram and AWS radio stay OFF.** Speaker playback is Pacific `Media/Playback/scripts/play.py` (WO-MIG-15, 2026-09-30): dry-run by default; live `aplay` needs `RR_PLAYBACK=1` and `--play`, quiet hours 22:00–06:00 HST, and a single-flight lock so a second caller gets `busy`. No periodic play job. A live speaker run has not been done.
  1. **Telegram**: a sendVoice step that converts WAV → OGG/Opus (the Bot API wants OGG/Opus for voice notes; the OGG goes in git-ignored `Archive/`), wired through the existing council relay / `Communications/telegram` (single `getUpdates` owner). It must not send when unchanged or when the gate skips. Still needs Alexander's sign-off.
  2. **Speakers**: the playback step is in place and stays gated. A live `aplay` run still needs Alexander's sign-off for that run.
- Batch 2 (2026-09-29 04:31, all in the same `jobs.py`, each `enabled = os.environ.get(FLAG, "0") == "1"`, read only at poller start, **no delivery**; command `nice -n 10 python3 {PACIFIC}/Media/Voice/scripts/voice_reports.py <report>`):

  | Job id | Schedule (HST) | Flag |
  | --- | --- | --- |
  | `voice_hourly_chime` | EVERY_MINUTE `only_at_minutes=[0, 30]` | `RR_VOICE_HOURLY_CHIME=1` |
  | `voice_nws_weather` | EVERY_MINUTE `[7, 22, 37, 52]` | `RR_VOICE_NWS=1` |
  | `voice_energy_report` | EVERY_MINUTE `[15, 45]` | `RR_VOICE_ENERGY=1` |
  | `voice_remaining_tasks` | EVERY_MINUTE `[32]` | `RR_VOICE_REMAINING=1` |
  | `voice_morning_report` / `voice_midday_report` / `voice_late_report` | ON_AT `09:02` / `12:02` / `21:02` | `RR_VOICE_ROLLUPS=1` (+ `RR_VOICE_ROLLUP_LLM=1` for the LLM summary line) |
  | `voice_late_final_report` (added 2026-09-29 ~23:59 HST) | ON_AT `23:30` | `RR_VOICE_LATE_FINAL=1` (text only; skips if the late slot is already done; `System/NightSleep` `should_run` when that module is present) |
  | `voice_earthquake_report` (added 2026-09-29 ~13:20 HST) | EVERY_MINUTE `[8]` | `RR_VOICE_QUAKE=1` (data from `geology_collect`, `RR_GEOLOGY=1`) |
  | `voice_kilauea_report` (added 2026-09-29 ~13:44 HST) | EVERY_MINUTE `[3]` | `RR_VOICE_KILAUEA=1` (data from `geology_collect`) |
  | `voice_hurricane_desk` (added 2026-09-29 ~13:43 HST) | ON_AT `05:50` `09:50` `12:50` `16:55` `20:50` | `RR_VOICE_HURRICANE=1` |
  | `voice_solar_desk` — **PROPOSED, not in jobs.py** | EVERY_MINUTE `[4]` | `RR_VOICE_SOLAR=1` |
  | `voice_security_desk` — **PROPOSED, not in jobs.py** | EVERY_MINUTE `[11]` | `RR_VOICE_SECURITY=1` |
  | `voice_bandwidth_desk` — **PROPOSED, not in jobs.py** | EVERY_MINUTE `[12]` | `RR_VOICE_BANDWIDTH=1` (needs `system_net_sample`, `RR_NET_SAMPLES=1`; `RR_VOICE_BANDWIDTH_DRY=1` skips the sample write) |
  | `voice_official_weather` — **PROPOSED, not in jobs.py** | EVERY_MINUTE `[25]` | `RR_VOICE_OFFICIAL=1` (fresh HLS needs `weather_official_hls`, `RR_OFFICIAL_HLS=1`) |
  | `voice_boot_brief` — **PROPOSED, not in jobs.py** | ON_BOOT (priority 20) | `RR_VOICE_BOOT=1` |
  | `reports_board_catchup` — **PROPOSED, not in jobs.py** | ON_AT `14:00` | `RR_REPORT_BOARD=1` (Pacific `Reports/scripts/report_board.py run-due`: re-runs a missed morning / midday roll-up as text; `--voice` renders WAV, never plays) |

  The three 2026-09-29 migration-pass registrations in `jobs.py` are a **sign-off item** (standing rule: `jobs.py` is edited only when Alexander asks or a work order requires it; left in place, not reverted). Exact blocks: Database `Logs/Migration/migration-jobs-py-additions-20260929.md`.

  If the single-flight lock is busy the text `_current.md` is still written and the WAV is skipped (rc 75 from `voice-render.sh`, logged in the JSON line). Not scheduled: council_quake (delivery-bound), hourly solar. official_weather and boot_brief are LANDED with PROPOSED jobs (above).

- **Text fixes 2026-09-29 14:18 HST** (breadth pass 2): `speakable.spoken_clock` says minutes 1–9 as "oh N" ("two oh one p.m."; shared by every report that speaks a clock — phrase clips use only :00 / :30, cache unchanged); `voice_reports.spoken_watts` ("zero watts" / "one watt" / rounded) used by solar_desk, energy_report and the roll-ups, with an all-zero device spoken as "idle"; `spoken_hhmm` speaks sun times as words ("six eleven a.m."). [Test](../07-testing/2026-09-29-old-repo-ports-breadth-batch5.md#voice-text-fixes).
- `Media/Voice/scripts/speech_scrub.py` (G1 persona scrub: drops vendor / "As an AI" / constraint sentences) is available as a library + stdin CLI; **not wired** into any report yet.

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
