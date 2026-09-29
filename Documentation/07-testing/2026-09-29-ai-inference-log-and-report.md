# Test record — AI inference JSONL, FLM log redaction, AI processing report

| Field | Value |
| --- | --- |
| **Date / time (HST)** | 2026-09-29 03:58–04:00 HST |
| **Tester** | Grok Bot (executor, overnight build) |
| **Change under test** | `run-infer.sh` JSONL append + FLM redaction + `flm_stop` kill fix; `ai-log-rotate.sh`; `Reports/ai_processing_report.py`. Doc: `00-architecture/AI-Processing-Logs-and-Reports.md` |
| **State** | **PASS** (JSONL line, redaction, report, rotation). Own-session exit-code question resolved: **rc = 0** after the kill fix |
| **Evidence** | Database `Logs/AI/Inference/inference_current.jsonl` (1 line, git-ignored), `Logs/AI/Reports/ai-processing-report_current.md` + `Archive/ai-processing-report_2026-09-29T0358.md`, `Logs/AI/FLM/flm.log` tail |
| **Commits** | see overnight log entry (auto-sync) |
| **Backup** | `/home/rootrecord/Database/GITHUB/g3-voice-ailog.bak-20260929-035454/` |

## How
Same light pattern as the 03:29 1B test. One request, resources sampled every 0.5 s:
`RR_CALLER=g3-voice-ailog-test nice -n 10 bash run-infer.sh ava "Reply with exactly one word: ready"`

## Pass criteria
1. Exactly one JSON line with the listed fields and no prompt/reply text. 2. rc 0. 3. flm.log holds no request body or model output. 4. Nothing resident afterwards. 5. MemAvailable > 2 GB.

## Result
- **Run 1 (03:58)**: answered on the NPU ("I am RootRecord."), but **rc = 1**, no stop line, no JSON line. Root cause: `set -e` is active after the FLM call, and `kill -KILL` on the already-exited flm returned 1, which aborted the script inside `flm_stop`. This is the same failure the 03:29 test put down to the process group, so the `setsid` change was not the fix. flm had exited anyway (0 processes, :52625 closed, lock IDLE). Fix: `|| true` on both kills (one new change, so one more test).
- **Run 2 (03:59)**: **rc = 0**, 4.67 s wall, `[ok] FLM on-demand server stopped`. JSONL:
  `{"route":"npu-flm","model":"llama3.2:1b","prompt_chars":34,"reply_chars":16,"latency_ms":4641,"exit_code":0,"fallback":false,"flm_cold_start":true,"flm_peak_rss_mb":2007,"mem_avail_mb_before":7417,"mem_avail_mb_after":7281,…}`
  The logged latency_ms was first 4641411285: this desk's `date` (uutils) ignores `%3N`. Switched to bash `$EPOCHREALTIME` (unit-checked: a 250 ms sleep read 253 ms), and the one test line was corrected to the measured 4641 ms. No further model run.
- flm pid from `$!` = the process named `flm` (the monitor saw pid 453315 = `FLM_STARTED`), so VmHWM sampling hits the right process.
- flm.log for the request: `[LOG]  Body: [redacted 16 lines]` and `[FLM]  Model RAW Output: [redacted 1 lines]`. 0 `"content"`/`"role"` lines in the redacted output (awk also dry-run on the old log: 132 → 115 lines, 0 body lines).
- Report: run by hand on empty data (03:58, "Requests: 0"), then on the one line (NPU share 100 %, p50/p95/max 4,641 ms, FLM peak 2,007 MB, lowest avail 7,281 MB). The first copy was archived because the content changed. Rotation: `moved=0 kept=1`. Report run: 0.02 s, 13 MB RSS.

## Resource impact
| When | Load (1 min) | MemAvailable | Swap used | Peak RSS |
| --- | --- | --- | --- | --- |
| before run 1 03:58:33 | 1.75 | 7,385 MB | ~2.8 GB | — |
| during run 1 | ≤ 1.75 | min 5,660 MB | — | flm (not logged) |
| before run 2 03:59:30 | 1.62 | 7,420 MB | — | — |
| during run 2 | ≤ 1.62 | min 5,483 MB | — | flm VmHWM 2,007 MB |
| after 03:59:37 | 1.73 | 7,292 MB | — | — |

## Cleanup confirmation
- [x] 0 flm processes after each run; :52625 closed; single-flight IDLE
- [x] `ollama ps` empty (Ollama not used)

## Open items
- PROPOSED: `single-flight.sh` prints its RUN banner on stdout (it shows up in replies) and writes `cmd=$*`, including `RR_PROMPT`, to `holder.txt` during a run.
- The hourly job is gated OFF (`RR_AI_REPORT=1` at the next poller start).
