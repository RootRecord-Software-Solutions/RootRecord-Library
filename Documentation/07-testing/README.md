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
| 2026-09-29 04:16 | [Specialist router unit test (no models)](./2026-09-29-specialist-router-unit-test.md) | PASS (35/35 labelled; held-out 5/8 informational; log privacy PASS) |
| 2026-09-29 04:18 | [Specialists: 2 live tiny requests (Ollama rr-energy + FLM rr-weather system message)](./2026-09-29-specialist-live-tiny-requests.md) | PASS (gate honoured; 6.3 s / 5.1 s; nothing resident after) |
| 2026-09-29 04:31 | [Template reports: one sample per Library template (3 light model calls)](./2026-09-29-template-report-samples.md) | PASS (4/4 structure-valid, 0 unsupported numbers; model text used for worklog, fallback for work order) |
| 2026-09-29 04:58 | [Specialist hook in run-infer.sh + router v2 (model-free diff, 2 live calls)](./2026-09-29-specialist-hook-and-router-v2.md) | PASS hook (flag-off byte-identical 8/8, flag-on 7/7, 2 live routed); router blind 17/22 → 17/22 (no gain); template free text still falls back |
| 2026-09-29 05:10 | [Router v3 structural fixes + template drafting through a desk file (2 live NPU calls)](./2026-09-29-router-v3-and-template-desk-file.md) | PASS router (35/35 kept; new blind 14/21 → 20/21); PARTIAL drafting (INTENT accepted but partly unsupported, SCOPE fell back) |
| 2026-09-29 04:22 | [single-flight: RUN banner to stderr, holder.txt metadata only](./2026-09-29-single-flight-banner-holder-fix.md) | PASS (rc 0, clean one-line reply, no prompt text in holder) |
| 2026-09-29 04:35 | [G3 voice reports batch 2: 7 ported reports (jobs gated OFF)](./2026-09-29-voice-reports-batch2.md) | PASS (7/7 rc 0, WAV QC PASS, rotation PASS, LLM summary PASS once); earthquake BLOCKED (no USGS data); by-ear VERIFY PENDING |
| 2026-09-29 04:41 | [Pronunciation candidates: Kalākaua, Liliʻuokalani, Nuʻuanu, Māhele](./2026-09-29-pronunciation-candidates-proposed.md) | PROPOSED (6 clips rendered, format QC only; not in lexicon) |
| 2026-09-29 12:09 | [Control Panel GTK4 + Conky readout (read-only, alongside existing viewers)](./2026-09-29-control-panel-gtk.md) | PASS (`--check` off/on, camera-off strace 0, all pages rendered); Conky + autostart VERIFY PENDING; window RSS 85 MB > 80 MB target |
| 2026-09-29 13:08 | [Root Monitor: rename + Running / Network (Starlink) / SSH / Not-migrated pages + full Settings registry](./2026-09-29-root-monitor-settings-running-network-ssh.md) | PASS (`--check` off/on, camera-off strace 0, secret leak tests 0, settings editor 103/103 on temp copies, 24 pages rendered); FAIL on RSS (`--check` 84.5 MB > 80 MB); swap/autostart/Conky start VERIFY PENDING; SSH rr-aws/rr-aws-ip FAIL |
| 2026-09-29 13:26 | [Smart Devices foundation: WiZ discovery + driver, Tuya passive scan, collector (job gated OFF)](./2026-09-29-smart-devices-foundation.md) | PASS driver (mock bulb restore SAME) + collector; real WiZ toggle BLOCKED (0 bulbs on LAN); plugs BLOCKED (no `local_key`, no SmartLife AP) |
| 2026-09-29 13:19 | [Geology collector: USGS earthquakes + HVO Kīlauea / Mauna Loa, earthquake voice report, Kīlauea cams, quake backfill](./2026-09-29-geology-earthquakes-hvo-collector.md) | PASS (manual runs; collector rc 0 2.64 s 28 MB; Kīlauea WATCH/ORANGE, Mauna Loa NORMAL/GREEN); jobs LANDED gated OFF (`RR_GEOLOGY`, `RR_KILAUEA_CAMS`, `RR_VOICE_QUAKE`); earthquake WAV VERIFY PENDING |
| 2026-09-29 13:26 | [Old-repo ports batch 1: sun times, uptime log, MP4 converter](./2026-09-29-old-repo-ports-batch1.md) | PASS (manual runs); jobs LANDED gated OFF (`RR_SUN_TIMES`, `RR_UPTIME_LOG`) |
| 2026-09-29 13:43 | [Voice reports batch 3: hurricane desk + Kīlauea report](./2026-09-29-voice-reports-batch3-hurricane-kilauea.md) | PASS (text, live Nolo + HVO data, empty-data gate); WAV VERIFY PENDING; jobs LANDED gated OFF (`RR_VOICE_HURRICANE`, `RR_VOICE_KILAUEA`) — jobs.py registration is a sign-off item |
| 2026-09-29 13:49 | [Geology: G0 nearest-location tag on quake events (addendum in the geology record)](./2026-09-29-geology-earthquakes-hvo-collector.md#addendum--g0-nearest-location-tag-2026-09-29-1349-hst) | PASS (temp + one real `quakes` run; Hawaiʻi 9/9, global 14/34 tagged ≤ 250 km) |
| 2026-09-29 13:45 | [US-Mainland-Server import, layout setup, SSH path checks](./2026-09-29-us-mainland-import-and-ssh.md) | PASS import (clone `b61d63c`, clean) + read-only SSH to 18.118.30.226; `rr-aws` FAIL (Cloudflare 1033, no tunnel on AWS); `rr-aws-ip` FAIL (stale IP); AWS disk full in ≈ 40 h (flagged P0) |
| 2026-09-29 14:05 | [Old-repo ports breadth batch 4: web facts, live-wx, Hawaiʻi news, host net/security, solar / security / bandwidth voice desks](./2026-09-29-old-repo-ports-breadth-batch4.md) | PASS web facts + live-wx + host desks + 3 voice desks (text); Hawaiʻi news FAIL on content (0 posts, 25 × 404); WAV VERIFY PENDING; jobs PROPOSED (not in jobs.py) |
| 2026-09-29 14:02 | [RootRecord-Cloud website staging: nested clone, npm ci, production build, brief start](./2026-09-29-website-rootrecord-cloud-staging.md) | PASS (clone ignored by Pacific; build 293 pages in 33 s, min MemAvailable 5.7 GB; local pages 200, allowlist 404); origin data FAIL (530, external); no deploy |

Related: [MIGRATION-DOCS-INDEX](../00-architecture/MIGRATION-DOCS-INDEX-2026-09-28.md) · [WO-SRV](../06-development/Work-Orders/Servers_Cutover_Work_Order_WO-SRV-2026-09-27.md) · [G3 Runtime Verification Checklist](../00-architecture/G3-Runtime-Verification-Checklist-2026-09-28.md)

*Folder created 2026-09-29 ~03:40 HST (docs only).*
