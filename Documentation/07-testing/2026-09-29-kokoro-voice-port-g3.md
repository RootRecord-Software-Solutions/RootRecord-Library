# Test record — Kokoro-82M G3 port: one clip per persona

| Field | Value |
| --- | --- |
| **Date / time (HST)** | 2026-09-29 04:03–04:05 HST |
| **Tester** | Grok Bot (executor, overnight build) |
| **Change under test** | Pacific `Media/Voice/` (uv CPython 3.12 venv; kokoro 0.9.4, misaki[en] 0.9.4, torch 2.14.0+cpu, en_core_web_sm 3.8.0) + Database `AI/Kokoro/Kokoro-82M/`. Doc: `00-architecture/Voice-Reports-G3.md` |
| **State** | **PASS** (format, duration, resources) · by-ear **VERIFY PENDING** (clips not played, by rule) |
| **Evidence** | Database `Media/Audio/Voice/voice_test_{ava,bruce,carly}_current.wav` (+ sidecars) |
| **Backup** | `/home/rootrecord/Database/GITHUB/g3-voice-ailog.bak-20260929-035454/` |

## How
`bash Media/Voice/scripts/voice-render.sh render --report voice_test_<who> --kind <who> --text "Test from <Who>."` (single-flight lock, nice 10, one process per clip, exits after the render).

## Result
- First attempt (Ava 04:03): rc 1, `espeak-ng … phontab: No such file`. espeak-ng ignores data paths over 160 chars, and the venv's `espeak-ng-data` path under Pacific is 163. Fix: a 19 MB user-space copy at `~/.local/share/rootrecord/espeak-ng-data`, set after misaki import (`RR_ESPEAK_DATA`).

| Clip | Voice / speed | Render (incl. model load) | Wall | Peak RSS | ffprobe | Duration | Peak |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Ava | af_heart 0.82 | 5.06 s | 6.26 s | 1,242 MB | s16, 24000 Hz, 1 ch | 2.000 s | −9.3 dBFS |
| Bruce | am_echo 0.92 | 4.57 s | 5.74 s | 1,244 MB | s16, 24000 Hz, 1 ch | 2.025 s | −5.4 dBFS |
| Carly | af_nova 0.74 | 5.05 s | 6.18 s | 1,243 MB | s16, 24000 Hz, 1 ch | 2.950 s | −11.4 dBFS |

## Resource impact
| When | Load (1 min) | MemAvailable |
| --- | --- | --- |
| before 04:04:56 | 1.64 | 11,777 MB |
| during (3 renders) | max 2.06 | min 10,578 MB |
| after | ~1.7 | ~11.7 GB |

## Cleanup confirmation
- [x] 0 `voice_generate` processes; single-flight IDLE; no flm; `ollama ps` empty. Nothing played.
