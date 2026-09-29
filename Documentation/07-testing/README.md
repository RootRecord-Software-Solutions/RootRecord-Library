# 07 — Testing

Record of every test run against the RootRecord ecosystem (Pacific runtime, Database, desk services).

Each test gets one file, `YYYY-MM-DD-<slug>.md`, created from [TEMPLATE.md](./TEMPLATE.md). A record states:

- date and time (HST, UTC-10)
- what was tested and how (exact command or procedure)
- pass criteria, written before the result
- result state
- resource impact (load, available memory, swap, peak RSS where measured)
- evidence link (usually `2 - RootRecord-Database/Logs/Migration/…`)
- commit SHAs (verified with `git log`)
- cleanup confirmation (no test process, port or model left behind)

**Status vocabulary (only these):** LANDED · VERIFY PENDING · PASS · FAIL · BLOCKED · RETIRED · PROPOSED · KEPT. Do not write LIVE/COMPLETE without evidence. Do not invent numbers. If a number is not in the evidence, write "not recorded".

## Test-safety policy (standing)

1. **Light tests only.** Use the smallest check that proves the gate.
2. **Watch RAM/CPU** before, during and after (`uptime`, `free -m`, peak RSS). The desk has about 14 GB of RAM.
3. **Stop anything that maxes resources** right away, and record it as FAIL with the numbers.
4. **Clean up every test process.** Confirm there is no leftover PID, open port or lock holder.
5. **No resident models.** Ollama uses `--keepalive 0`, FLM warmup is opt-in only (`FLM_WARMUP_RESIDENT=1`), and nothing stays loaded after a test.
6. **Prefer the NPU on demand** (`run-infer.sh` → `flm serve llama3.2:1b` per request, stopped on exit) over CPU models.
7. **One test per change.** Don't loop retries. If a test is blocked, record BLOCKED and stop.
8. Hardware-actuating tests (Energy arm/disarm, AC) and service restarts need Alexander's approval first.
9. Never write secrets into a record.

## Index

| Date | Record | State |
| --- | --- | --- |
| 2026-09-29 01:11 | [Poller realigned to new Database root](./2026-09-29-poller-database-root-realign.md) | PASS |
| 2026-09-29 01:49 | [Weather hook from Pacific with Weather/.venv](./2026-09-29-weather-pacific-venv-hook.md) | PASS |
| 2026-09-29 02:15 | [Status viewer: poller-dashboard single-window launcher; docs-only pulls don't reload](./2026-09-29-poller-dashboard-single-window.md) | PASS |
| 2026-09-29 02:33 | [Post-reboot (02:28 HST boot): all services](./2026-09-29-post-reboot-all-services.md) | PASS (NPU PARTIAL at the time, see next record) |
| 2026-09-29 02:56 | [NPU / FastFlowLM install and validate](./2026-09-29-npu-flm-install-validate.md) | PASS |
| 2026-09-29 03:09 | [Database Title-case folder rename (one stack restart)](./2026-09-29-database-titlecase-rename.md) | PASS |
| 2026-09-29 03:10 | [OOM incident: resident FLM warmup (llama3.2:3b)](./2026-09-29-oom-flm-warmup-resident.md) | FAIL → fixed; fix PASS |
| 2026-09-29 03:16 | [Laptop battery bar B3 on dashboard](./2026-09-29-laptop-battery-b3-dashboard.md) | LANDED / VERIFY PENDING |
| 2026-09-29 03:20 | [EcoFlow stale data: Energy/.venv](./2026-09-29-ecoflow-stale-data-energy-venv.md) | PASS (freshness); battery levels flagged |
| 2026-09-29 03:29 | [NPU route: llama3.2:1b on demand](./2026-09-29-npu-llama3.2-1b-on-demand.md) | PASS (route); own-session fix VERIFY PENDING |
| 2026-09-29 04:00 | [Weather + relay supervisor (dry run)](./2026-09-29-service-supervisor-dry-run.md) | PASS (logic); live VERIFY PENDING (next poller start) |
| 2026-09-29 04:00 | [Pacific npu-status.sh (idle)](./2026-09-29-npu-status-pacific-copy.md) | PASS (idle); lock-held run VERIFY PENDING |
| 2026-09-29 04:02 | [Relay quiet-mode inbox + replay (parse only)](./2026-09-29-relay-quiet-inbox-parse.md) | PASS (parse); live VERIFY PENDING (next poller start) |
| 2026-09-29 04:04 | [Weather retention dry run](./2026-09-29-weather-retention-dry-run.md) | PASS (dry run: 0 to move); apply OFF pending review |
| 2026-09-29 03:59 | [AI inference JSONL + FLM log redaction + AI processing report](./2026-09-29-ai-inference-log-and-report.md) | PASS; run-infer rc now 0 (kill fix); report job gated OFF |
| 2026-09-29 04:05 | [Kokoro-82M G3 port: one clip per persona](./2026-09-29-kokoro-voice-port-g3.md) | PASS (format/resources); by-ear VERIFY PENDING |
| 2026-09-29 04:12 | [Kokoro phrase-clip cache, stitcher, QC, system_perf](./2026-09-29-kokoro-phrase-clips-qc.md) | PASS (68/68 QC; ASR 59/68); listen list VERIFY PENDING; job gated OFF |
| 2026-09-29 04:14 | [Hawaiian place-name pronunciation sheet](./2026-09-29-hawaiian-pronunciation-sheet.md) | PASS (text 99/99); by-ear VERIFY PENDING |

Related: [MIGRATION-DOCS-INDEX](../00-architecture/MIGRATION-DOCS-INDEX-2026-09-28.md) · [WO-SRV](../06-development/Work-Orders/Servers_Cutover_Work_Order_WO-SRV-2026-09-27.md) · [G3 Runtime Verification Checklist](../00-architecture/G3-Runtime-Verification-Checklist-2026-09-28.md)

*Folder created 2026-09-29 ~03:40 HST (docs only).*
