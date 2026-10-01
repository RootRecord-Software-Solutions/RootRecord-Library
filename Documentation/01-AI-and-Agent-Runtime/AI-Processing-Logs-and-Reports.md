# AI Processing Logs and Reports (G3)

| Field | Value |
| --- | --- |
| **Date (HST)** | 2026-09-29 03:55–04:00 HST |
| **State** | Inference JSONL **LANDED + PASS** · FLM log redaction **LANDED + PASS** · report generator **LANDED + PASS** · hourly job **LANDED, gated OFF** (`RR_AI_REPORT=1`) |
| **Implements** | `08-ideas/2026-09-29-ai-processing-log-and-report.md` |
| **Test** | `07-testing/2026-09-29-ai-inference-log-and-report.md` |
| **Backup** | `/home/rootrecord/Database/GITHUB/g3-voice-ailog.bak-20260929-035454/` |

## 1. Per-request log (Pacific `System/scripts/plumbing/run-infer.sh`)

`run-infer.sh` appends **one JSON line per request** to Database `Logs/AI/Inference/inference_current.jsonl`. It is written after the reply is printed and after an on-demand FLM has been stopped.

| Field | Meaning |
| --- | --- |
| `ts` | ISO 8601 with `-10:00` (end of request) |
| `caller` | `RR_CALLER` env if set, else the parent process name |
| `target` | first arg (`ava` / `bruce` / `carly` / model) |
| `route` | `npu-flm` or `ollama` |
| `model` | FLM model (e.g. `llama3.2:1b`) or Ollama model (e.g. `ava-telegram`) |
| `prompt_chars` / `reply_chars` | **lengths only, never text** (the single-flight banner line is not counted) |
| `latency_ms` | whole request, including an FLM cold start |
| `exit_code` | the script's exit code |
| `fallback` | `true` when Ollama answered |
| `flm_cold_start` | `true` when this request started `flm serve` |
| `flm_peak_rss_mb` | `VmHWM` of the on-demand flm process, sampled just before it is stopped (host RAM only; NPU buffers not counted). `null` when FLM was not started by this request |
| `mem_avail_mb_before` / `_after` | `MemAvailable` from `/proc/meminfo` |

Fail-safe: the whole append is wrapped (`… 2>/dev/null || true`), the lock wait is capped at 2 s, and strings are reduced to `[A-Za-z0-9._:@/+-]`, so logging can never break or block inference. `RR_INFER_LOG=0` disables it, and `RR_INFER_LOG_FILE` overrides the path. Appends and rotation share `flock` on `inference_current.lock` (ignored by `*.lock`).

Timing note: this desk's `date` is uutils coreutils and ignores `%3N`, so the script uses bash `$EPOCHREALTIME`.

## 2. Rotation (`_current` convention)

`System/scripts/plumbing/ai-log-rotate.sh` (stdlib python in a bash wrapper, nice 10) moves every line dated before today (from its `ts`) into `Logs/AI/Inference/Archive/inference_YYYY-MM-DD.jsonl`. Today's lines stay live. It runs daily in effect, whenever the report job runs.

Git: `inference_current.jsonl` is ignored (high churn, like `automations_current.log`). Daily `Archive/` files are tracked (metadata only).

## 3. Report (`Pacific Reports/ai_processing_report.py`, stdlib only)

Reads the current JSONL plus the archive days inside the window (`RR_AI_REPORT_HOURS`, default 24). Writes non-git `test-reports/AI-Processing/ai-processing-report_current.md`. If the content changed (the Generated/Window lines are ignored), the previous copy is first moved to `test-reports/AI-Processing/Archive/ai-processing-report_YYYY-MM-DDTHHMM.md`.

Contents: time window, request count, requests by route and by route/model, NPU share, fallback count, FLM cold starts, errors (exit_code ≠ 0) with the last 20 listed, empty replies, unparsable lines, latency p50/p95/max, max FLM peak RSS, and the lowest MemAvailable seen.

A Grok spend section (WO-MIG-37) reads Database `Reports/AI-Usage/last-summary.json`. It lists xAI calls, tokens, and estimated USD, or `no ledger rows` when that file is missing or has no xAI rows. The ledger does not call xAI. `Reports/AI-Usage/scripts/ai_usage_report.py` writes the summary. Hourly job `ai_usage_report` stays off unless `RR_AI_USAGE=1`.

## 4. Gate

Pacific `Automations/scripts/jobs.py` → `EVERY_HOUR` id `ai_processing_report_hourly` (runs at :00):
`enabled = os.environ.get("RR_AI_REPORT", "0") == "1"`. The command is `ai-log-rotate.sh && nice -n 10 python3 Reports/ai_processing_report.py`.
`jobs.py` is imported once, so the flag **only takes effect at the next poller start**, and only if `RR_AI_REPORT=1` is in the poller's environment (for example the `rr-rootserver-poller` user unit's `Environment=`). Until then, run it by hand with the same command.

## 5. FLM server log privacy

FastFlowLM 1.0.6 prints each request's full JSON body (system + user prompt) and the raw model output to stdout. Database `Logs/AI/FLM/` was already git-ignored (`/Logs/AI/FLM/*`, verified with `git check-ignore`). The on-demand start in `run-infer.sh` now pipes FLM output through `System/scripts/plumbing/flm-log-redact.awk`, which:

- replaces `[LOG]  Body:` and its JSON lines with `[LOG]  Body: [redacted N lines]`
- replaces `Model RAW Output:` up to `NPU Lock Released` / `====` with `[redacted N lines]`
- keeps status, timing, target and error lines

`FLM_LOG_REDACT=0` restores the raw log. flm still runs as its own `setsid` session, and `$!` is still the flm pid (verified). Older lines already in `flm.log` (before 03:58 HST) are not rewritten. They are local-only and ignored.

## 6. Found and fixed along the way

- **rc=1 root cause**: `set -e` is re-enabled after the FLM call, and `kill -KILL` on an already-exited flm pid returned 1, which aborted `flm_stop` (and before this, the EXIT trap). So the earlier `setsid` change was not the fix. `|| true` on both kills fixes it: **exit code is now 0** (test 03:59).
- **LANDED, PASS 2026-09-29 04:22** (see [single-flight banner/holder test](../07-testing/2026-09-29-single-flight-banner-holder-fix.md)): the RUN banner now goes to **stderr**, and `holder.txt` holds metadata only: `job= caller= pid= ts= cmd=<basename of the command> prompt_chars=<length>` (callers set `RR_CALLER` / `RR_PROMPT_CHARS`; `run-infer.sh` and `run-ollama.sh` pass the length, never the text). Original finding: `single-flight.sh run` printed `[ok] single-flight RUN <job>` on **stdout**, so it ends up in the reply `run-infer.sh` prints. It also writes `cmd=$*` to `Github/plumbing/state/holder.txt`, which includes `RR_PROMPT=<prompt text>` while a request runs (git-ignored and deleted after the run, but it is prompt text on disk). Fix as above.
