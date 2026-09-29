# Test record — Kokoro phrase-clip cache, stitcher, QC gate, system_perf

| Field | Value |
| --- | --- |
| **Date / time (HST)** | 2026-09-29 04:06–04:12 HST |
| **Tester** | Grok Bot (executor, overnight build) |
| **Change under test** | `clip_catalog.py`, `voice_generate.py` clips/stitch/asr modes, `voice_asr_check.py`, `system_perf.py` (Pacific `Media/Voice/scripts/`). Approved exception to "no stitching" (Alexander, ~04:00 HST). Doc: `00-architecture/Voice-Reports-G3.md` §4 |
| **State** | QC gate **PASS** 68/68 · ASR round trip 59/68 match, 9 on the listen list (**VERIFY PENDING**, Alexander by ear) · stitch **PASS** · system_perf **PASS** (job gated OFF) |
| **Evidence** | Database `Media/Audio/Voice/Clips/clips_manifest.json` (tracked), `Clips/<Persona>/*.wav` (ignored), `system_perf_current.wav`, `System/Reports/system_perf_current.md`, `hourly_chime_current.wav` |
| **Backup** | `/home/rootrecord/Database/GITHUB/g3-voice-ailog.bak-20260929-035454/` |

## How
Batches, one process each, through `voice-render.sh` (lock + nice 10):
`clips --catalog --persona Bruce` → `Carly` → `Ava`, then `asr` (whisper tiny, on demand), then `nice -n 10 python3 system_perf.py` (stitch), then `stitch --report hourly_chime --kind chime --no-gate --text "It's four thirty a.m."`.

## Pass criteria
Every clip: 24000 Hz / mono / PCM_16, duration > 0.2 s, peak < −1 dBFS, leading/trailing silence trimmed. MemAvailable > 2 GB and CPU not pegged. Nothing resident afterwards.

## Result
| Batch | Clips | Total | Per clip | Peak RSS |
| --- | --- | --- | --- | --- |
| Bruce | 5 | 7.3 s | 0.6–4.7 s (first includes model load) | 1,305 MB |
| Carly | 9 | 16.7 s | — | 1,831 MB |
| Ava | 54 | 42.8 s | 0.55 s typical chime | 1,968 MB |
| ASR (whisper tiny, 72 MB download once) | 68 | 28.3 s (load 5.7 s) | ~0.3 s | 576 MB |

- QC: **68/68 PASS**. Duration 0.77–7.11 s, peak −6.7 … −2.0 dBFS, speech RMS −20.6 … −20.0 dBFS. Trimmed up to 411 ms lead and 1,011 ms tail of raw Kokoro silence. 6.1 MB on disk.
- Chime text: the G1 template produced "It's three p.m.." (double period). The catalog text was fixed and the 46 manifest texts updated. Audio unchanged, because the spoken text was identical.
- ASR scoring: word ratio against the text or its speakable respelling, with clock digits folded ("330pm" → "three thirty p.m."). 59 match.
- **system_perf (stitch)**: rc 0, 11.6 s wall, 2 clips + 6 live sentences, 23.35 s WAV (s16 / 24000 / 1), peak −1.5 dBFS, RMS −20.2 dBFS, peak RSS 1,473 MB. Text report written.
- **All-cached stitch (chime)**: 1 clip, 0 live, **model not loaded**, 0.2 s wall, 37 MB RSS, 1.67 s WAV, QC PASS.

## Manual listen list (for Alexander — not played by the agent)
| Clip | Text | Spoken as | Whisper tiny heard | Score |
| --- | --- | --- | --- | --- |
| `Ava/chime_0200` | It's two a.m. | It's two a.m. | It gets to AM. | 0.286 |
| `Ava/chime_1200` | It's noon. | It's noon. | It's new, huh? | 0.4 |
| `Ava/nws_by_county` | NWS Hawaii by county. | National Weather Service hah wye ee by county. | National Weather Service, Hawaii by County. | 0.714 |
| `Ava/nws_report_intro` | NWS Hawaii Report. | National Weather Service hah wye ee Report. | National Weather Service, Hawaii Report. | 0.667 |
| `Bruce/system_outro` | End of system report. | End of system report. | and of system report. | 0.75 |
| `Carly/hurricane_outro` | Stay with NWS Honolulu for watches and warnings. | Stay with National Weather Service hoh noh loo loo for watches and warnings. | Stay with National Weather Service, hone no Lulu for watches and warnings. | 0.72 |
| `Carly/kilauea_intro` | Kilauea Report. | Kill ah way uh Report. | Kill our way of report. | 0.6 |
| `Carly/quake_hi_intro` | Hawaii Earthquake Report. | hah wye ee Earthquake Report. | How why E earthquake report? | 0.5 |
| `Carly/quake_hi_none` | No new Hawaii earthquakes since the last report. | No new hah wye ee earthquakes since the last report. | No new Haw-Wi-E earthquakes since the last report. | 0.778 |

### Added 2026-09-29 04:41 (pass 2) — **PROPOSED** pronunciation candidates (not PASS; not live)
| Clip | Text | Spoken as | State |
| --- | --- | --- | --- |
| `Ava/proposed_kalakaua` | Kalākaua. | kah lah kow ah. | **PROPOSED** |
| `Ava/proposed_liliuokalani` | Liliʻuokalani. | lee lee oo oh kah lah nee. | **PROPOSED** (A) |
| `Ava/proposed_liliuokalani_b_misaki` | Liliʻuokalani. | Liliuokalani. (Kokoro's own us_gold entry) | **PROPOSED** (B) |
| `Ava/proposed_nuuanu` | Nuʻuanu. | noo oo ah noo. | **PROPOSED** |
| `Ava/proposed_mahele` | Māhele. | mah heh leh. (G2P reads the end as "lay") | **PROPOSED** (A) |
| `Ava/proposed_mahele_b_ipa` | Māhele. | inline phonemes mˌɑhˈɛlɛ | **PROPOSED** (B) |

Details and sources: [pronunciation candidates](./2026-09-29-pronunciation-candidates-proposed.md). Batch-2 report WAVs to spot-check: [voice reports batch 2](./2026-09-29-voice-reports-batch2.md#listen-list-additions-verify-pending-by-ear).

Suggested order: `chime_0200` and `chime_1200` first (possible real issues). The rest are Hawaiian respellings or ASR limits. Also spot-check a few "match" clips, plus `system_perf_current.wav` for the join quality.

## Resource impact
| When | Load (1 min) | MemAvailable |
| --- | --- | --- |
| clips batches 04:06–04:08 | max 4.05 (8 cores) | min 9,781 MB |
| ASR 04:09 | before 2.39, max 3.13 | before 11,703, min 11,078 MB |
| system_perf 04:11 | before 1.75, max 2.81 | before 11,777, min 10,311 MB |
| after 04:13 | 2.76 | 11,067 MB |

## Cleanup confirmation
- [x] 0 `voice_generate` / whisper processes; single-flight IDLE; no flm; `ollama ps` empty. Nothing played or sent.
