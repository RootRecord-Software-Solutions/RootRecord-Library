# Test record — Specialists: 2 live tiny requests (Ollama + FLM)

| Field | Value |
| --- | --- |
| **Date / time (HST)** | 2026-09-29 04:18:13 and 04:18:32 HST |
| **Tester** | agent pass g3-specialists |
| **Change under test** | Specialist models (`rr-energy` via Ollama) and the FLM system-message route (`rr-weather` SYSTEM block → `llama3.2:1b` on the NPU), each routed by `route-specialist.py` ([design](../00-architecture/AI-Specialist-Models-and-Routing.md)) |
| **State** | **PASS** (both answered through the DATA GATE; no resident model after) |
| **Evidence** | this record (numbers captured by the test harness, a throwaway script outside the repos) |
| **Commits** | see the design doc / final report (auto-sync) |
| **Backup** | `/home/rootrecord/Database/GITHUB/g3-specialists.bak-20260929-041126/` |

## What was tested
One request per backend. Both went through `route-specialist.py --shell --with-system --verify-model --voice bruce`, then ran under `single-flight.sh run`, with a MemAvailable/RSS sampler every 0.2 s (abort below 2 GB). The prompt came from a file, so it never appeared in the lock holder line. **`run-infer.sh` was not used** (another pass is editing it) and was not modified.

## How
1. Ollama: `single-flight.sh run … -- nice -n 10 curl /api/chat` with `model=rr-energy`, `keep_alive: 0`, user = `[desk: none]\nUser: What is the Delta 2 battery SOC right now?`
2. FLM: `setsid nice -n 10 flm serve llama3.2:1b --pmode balanced --ctx-len 4096 --port 52625` (log through `flm-log-redact.awk`), then one `/v1/chat/completions` with system = `rr-weather` SYSTEM block, temperature 0.2, max_tokens 256, user = `[desk: none]\nUser: Is Kīlauea erupting right now?`, then TERM/KILL.

## Pass criteria (written before running)
1. The router picks `rr-energy` / `rr-weather`.
2. The reply does not invent a reading (no desk block was attached).
3. MemAvailable stays above 2 GB.
4. Afterwards: `ollama ps` is empty, there are 0 flm processes, :52625 is closed, and the lock is IDLE.

## Result

| | Test 1 — Ollama `rr-energy` (qwen2.5 1.5B q8_0) | Test 2 — FLM `llama3.2:1b` + `rr-weather` system |
| --- | --- | --- |
| Route / confidence | `rr-energy` 1.0 (battery, soc, delta 2) | `rr-weather` 1.0 (kilauea, erupting) |
| Reply | "No data — I can't see the desk" | "No data — I can't see the desk." |
| End-to-end latency | **6348 ms** (cold load 2555 ms; 478 prompt tokens; 10 tokens in 444 ms) | **5142 ms** incl. cold start (server ready in 3 s; TTFT 0.47 s; prefill ~1039 tok/s; decode ~46.9 tok/s; 486 prompt / 10 completion tokens) |
| MemAvailable before → min → after | 11621 → **9857** → 10174 MB (11625 MB 2 s later) | 11609 → **9734** → 11487 MB |
| Peak model RSS | not recorded (the sampler did not match the Ollama runner process) | flm VmHWM 2055456 kB (~2007 MB); sampler 1988 MB |
| Load (1 min) before → after | 1.70 → 1.96 | 1.74 → 1.76 |
| rc | 0 | 0 |

## Resource impact
Both stayed above 9.7 GB MemAvailable (floor 2 GB, not hit). Swap was not touched by the tests (not separately recorded).

## Cleanup confirmation
- [x] `ollama ps` empty right after test 1, and again after test 2
- [x] 0 flm processes, port 52625 closed
- [x] single-flight lock IDLE; harness temp files removed

## Open items / caveats
- Test 2 obeyed the gate but did not name the official source (USGS HVO) that the `rr-weather` prompt asks for. This is a 1B quality limit.
- The routing JSONL lines for these two runs were not written: the harness shell had `RR_ROUTE_LOG=0` left over from the unit test. Logging was then verified with a separate routing-only call (no model) at 04:18:57 HST. Two metadata-only lines were written, with `model_verified: true`.
- Only 2 live requests, per policy. The other 8 specialists and the restored `*-telegram` models were built but not run live.
