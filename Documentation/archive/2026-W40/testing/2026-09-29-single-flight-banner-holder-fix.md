# Test record — single-flight: RUN banner to stderr, holder.txt metadata only

| Field | Value |
| --- | --- |
| **Date / time (HST)** | 2026-09-29 04:20–04:23 HST |
| **Tester** | Grok Bot (executor, overnight build, pass 2) |
| **Change under test** | Pacific `System/scripts/plumbing/single-flight.sh` (`run()`), `run-infer.sh` (do_flm passes `RR_PROMPT_CHARS`), `run-ollama.sh` (exec passes `RR_PROMPT_CHARS`) |
| **State** | **LANDED, PASS** |
| **Evidence** | stdout of one real request; `holder.txt` sampled during the run; Database `Logs/AI/Inference/inference_current.jsonl` line for caller `sf-fix-test` |
| **Backup** | `/home/rootrecord/Database/GITHUB/g3-voice-reports2.bak-20260929-042153/` |

## Problem (found in pass 1)
`single-flight.sh run` printed `[ok] single-flight RUN <job>` on **stdout**, so it could end up inside a reply, and wrote `cmd=$*` to Database `Github/plumbing/state/holder.txt`. That argv included the prompt text while a request was running.

## Fix
- The banner goes to **stderr**.
- `holder.txt` is now one line of metadata: `job=<id> caller=${RR_CALLER:-<parent comm>} pid=<pid> ts=<ISO> cmd=<basename of argv[0]> prompt_chars=${RR_PROMPT_CHARS:--1}`. No argv, no prompt text.
- `run-infer.sh` and `run-ollama.sh` pass the prompt **length** only (`${#PROMPT}` / `${#FULL}`).

## Callers checked (all compatible, no change needed)
| Caller | How it uses single-flight | Result |
| --- | --- | --- |
| `run-infer.sh` | `status \| head -1 == IDLE` + `run` | OK |
| `run-ollama.sh` | `run` via exec | OK |
| `Communications/telegram/scripts/council-relay.py` | strips `[ok]`/`[warn]` lines from stdout | OK (nothing left to strip) |
| `Media/Voice/scripts/voice-render.sh` → `voice_generate.py`, `system_perf.py`, `voice_reports.py` | parse the last stdout line (JSON) | OK |
| `System/scripts/plumbing/npu-status.sh` | `status` only | OK |
| `Reports/template_fill.py` (other agent, new tonight) | `status` startswith IDLE; strips `[ok]` lines from run-infer stdout | OK |

## Result
1. Unit check (stand-in command, no model): rc 0, banner on stderr only, `holder.txt` held no argv.
2. Real request 04:22: `RR_CALLER=sf-fix-test run-infer.sh ava "<one-word prompt, 34 chars>"`

| Measure | Value |
| --- | --- |
| rc | **0** |
| stdout | exactly the model reply, one line, **no banner** |
| wall | 4.27 s (JSONL latency 4,241 ms) |
| `holder.txt` during the run | `job=infer:ava:20260929-042219 caller=sf-fix-test pid=… ts=… cmd=python3 prompt_chars=34` (no text) |
| FLM peak RSS | 2,007 MB (on demand, stopped after) |
| MemAvailable before / min / after | 11,550 / 9,764 / 10,927 MB |
| Load (1 min) max | 1.66 |

## Cleanup confirmation
- [x] 0 flm processes, port 52625 closed, single-flight **IDLE**, `holder.txt` removed, `ollama ps` empty. No restart, nothing sent.
