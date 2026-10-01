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
| 2026-09-29 13:45 | [US-Mainland-Server import, layout setup, SSH path checks](./2026-09-29-us-mainland-import-and-ssh.md) | PASS import (clone `b61d63c`, clean) + read-only SSH to [redacted public IP]; `rr-aws` FAIL (Cloudflare 1033, no tunnel on AWS); `rr-aws-ip` FAIL (stale IP); AWS disk full in ≈ 40 h (flagged P0) |
| 2026-09-29 14:05 | [Old-repo ports breadth batch 4: web facts, live-wx, Hawaiʻi news, host net/security, solar / security / bandwidth voice desks](./2026-09-29-old-repo-ports-breadth-batch4.md) | PASS web facts + live-wx + host desks + 3 voice desks (text); Hawaiʻi news FAIL on content (0 posts, 25 × 404); WAV VERIFY PENDING; jobs PROPOSED (not in jobs.py) |
| 2026-09-29 14:02 | [RootRecord-Cloud website staging: nested clone, npm ci, production build, brief start](./2026-09-29-website-rootrecord-cloud-staging.md) | PASS (clone ignored by Pacific; build 293 pages in 33 s, min MemAvailable 5.7 GB; local pages 200, allowlist 404); origin data FAIL (530, external); no deploy |
| 2026-09-29 14:07 | [AWS Mainland: Hawaii feed trim + auto-trim cron, www.rootrecord.cloud tunnel restored](./2026-09-29-aws-hawaii-trim-and-cloudflared.md) | PASS: `hawaii.ndjson` 1.83 GB → 50.3 MB, free disk 1.5G → 3.2G; `ubuntu` crontab `*/15` auto-trimmed at 14:30 (67.5 → 50.3 MB); `www` 530 → 200 (tunnel [redacted tunnel ID], 4 connections); `rr-aws-ip` fixed. `rr-aws` PASS only with the verified host key (desk `known_hosts` stale) |
| 2026-09-29 14:24 | [Globe landing overlay: local preview + screenshots (desktop/mobile, mirror + AWS-runtime schema, failure view)](./2026-09-29-globe-landing-overlay-preview.md) | PASS preview (11 screenshots in `test-reports/Globe-Landing/`, cleanup 0 procs); drag/zoom VERIFY PENDING (headless paints no WebGL); AWS deploy PROPOSED; **P0 finding: live `www` serves `/server.js` + `/data/hawaii.ndjson` publicly** |
| 2026-09-29 14:18 | [Breadth batch 5 · voice text fixes (clock "two oh one", watts words, idle devices, spoken sun times)](./2026-09-29-old-repo-ports-breadth-batch5.md#voice-text-fixes) | PASS (text; 6 reports rc 0, 0.1–0.64 s); WAV VERIFY PENDING |
| 2026-09-29 14:25 | [Breadth batch 5 · Hawaiʻi news seed feeds (16 feeds, `RR_NEWS_SEEDS_ONLY`)](./2026-09-29-old-repo-ports-breadth-batch5.md#hawaiʻi-news-seed-feeds) | PASS: 278 posts (seeds-only 11.6 s; full 22.8 s); job PROPOSED `RR_HAWAII_NEWS`; seed list review pending |
| 2026-09-29 14:27 | [Breadth batch 5 · NWS HLS official statement fetcher (`official_statement.py`)](./2026-09-29-old-repo-ports-breadth-batch5.md#official-statement-fetcher-hls) | PASS (Nolo HLS 7014 chars; re-run changed=False); PROPOSED `RR_OFFICIAL_HLS` 600 s; correction: HWO already collected by the poller |
| 2026-09-29 14:28 | [Breadth batch 5 · official weather voice report (Ava, HLS/HWO/AFD)](./2026-09-29-old-repo-ports-breadth-batch5.md#official-weather-voice-report) | PASS (text, AFD path; fresh-HLS + no-product paths unit-tested); WAV VERIFY PENDING; PROPOSED `RR_VOICE_OFFICIAL` |
| 2026-09-29 14:29 | [Breadth batch 5 · boot brief voice report (Ava, G1 boot-prelims)](./2026-09-29-old-repo-ports-breadth-batch5.md#boot-brief-voice-report) | PASS (text, midday edition); WAV VERIFY PENDING; PROPOSED ON_BOOT `RR_VOICE_BOOT` |
| 2026-09-29 14:31 | [Breadth batch 5 · daily report board + catch-up ledger (`report_board.py`)](./2026-09-29-old-repo-ports-breadth-batch5.md#report-board-and-catch-up-ledger) | PASS (status / run-due / nothing_due / rollover / bad arg rc 2); text only, no playback; PROPOSED `RR_REPORT_BOARD` 14:00 |
| 2026-09-29 14:33 | [Breadth batch 5 · load categories (`load_categories.py`)](./2026-09-29-old-repo-ports-breadth-batch5.md#load-categories) | PASS (live 68 W Starlink/lights; night scenario); on demand; thresholds + missing fields check-later |
| 2026-09-29 14:34 | [Breadth batch 5 · global hurricane board (`global_board.py`, NHC + RAMMB + JTWC)](./2026-09-29-old-repo-ports-breadth-batch5.md#global-hurricane-board) | PASS (4/4 sources, 7 storms, 2.9 s); PROPOSED `RR_HURRICANE_GLOBAL`; label doubling check-later |
| 2026-09-29 14:35 | [Breadth batch 5 · host hardware (`host_hw.py`)](./2026-09-29-old-repo-ports-breadth-batch5.md#host-hardware) | PASS (48 °C, nvme 56.5%, GPU 1%, NPU 0%); on demand |
| 2026-09-29 14:36 | [Breadth batch 5 · speech scrub (`speech_scrub.py`)](./2026-09-29-old-repo-ports-breadth-batch5.md#speech-scrub) | PASS; on demand; not wired |
| 2026-09-29 14:37 | [Breadth batch 5 · G1 scheduler → G3 jobs map (verification)](./2026-09-29-old-repo-ports-breadth-batch5.md#scheduler-map-verification) | PASS (64 G1 job ids mapped). Night-sleep gate armed 2026-09-30 00:02 HST (`RR_NIGHT_SLEEP=1`); no `night-mode.json`, so jobs are not skipped |
| 2026-09-29 14:19 | [Android apps import into `6 - Android Development` (9 apps, 2 TB drive read-only)](./2026-09-29-android-apps-import.md) | PASS (9/9 copies 0 checksum diffs, 80.7 MB; 17 secrets 0600, 24/24 git-ignored; drive 0 I/O errors); build VERIFY PENDING (no SDK/Java on desk) |
| 2026-09-29 14:40 | [AWS globe `server.js`: static allowlist (close file exposure on www.rootrecord.cloud)](./2026-09-29-aws-globe-static-allowlist.md) | PASS: 22 real files exposed (206/416) + catch-all paths → 404 (source, `data/hawaii.ndjson`, sqlite, scripts, node_modules); `/` `/health` `/api/state` 200, data streaming; bind 127.0.0.1. No sign of a full feed download (web `wchar` 4.6 MB total). **Finding:** feed-server `:8787` still public (not changed) |
| 2026-09-29 15:00 | [AWS fallback rebuild · Phase 1 read-only inventory](./2026-09-29-aws-fallback-inventory.md) | PASS (read-only, 0 AWS changes). **Findings:** t3.micro **908 MB RAM (not 2 GB)**, ~445 MB avail, 3.1 GB disk free; 28–44 % iowait (history per-record commits); `github-poller` 1 s fetch 14,318 CPU-s; legacy poller 4 dead jobs; `:8787` still public (listed) |
| 2026-09-29 15:05 | [Root Monitor "AWS Fallback" page (per-function toggles, dry-run)](./2026-09-29-root-monitor-aws-fallback-page.md) | PASS dry-run: `--check` 14 pages 0 errors 0 leaks; +4.4 MB RSS; settings 103/103; unit 13/13; 3 screenshots; write mode NOT exercised (sign-off + Phase 2 deploy) |
| 2026-09-29 16:20 | [Root Monitor — switches → labelled buttons; camera viewer button visible](./2026-09-29-root-monitor-toggle-buttons.md) | PASS: cause = no control on Cameras page + wrong pointer + SwitchRow below the fold on Settings → Panel; run-check PASS 0 errors 0 leaks; settings 103/103; toggle tests 30/30 (AWS ssh stubbed); no RSS growth; 4 screenshots |
| 2026-09-29 15:58 | [Globe overlay v2: Stop/Resume spin, click-info card, hover highlight, fix for the 1 s mesh re-creation](./2026-09-29-globe-overlay-v2-spin-click-info.md) | PASS: jsdom 16/16, real globe.gl probe `wired · stableId`, 8 `v2-*.png`; real-browser mouse VERIFY PENDING (no WebGL in headless); AWS deploy PROPOSED (3 files + 1 line, no restart) |
| 2026-09-29 15:45 | [AWS globe history: batched SQLite commits + persisted cursor](./2026-09-29-aws-globe-history-batched-commits.md) | PASS: writes 43.9 → 1.6 MB/min (syscw 17,878 → 745/min); flows/counters update; in-place trim + restart no longer re-count (synthetic A–F) |
| 2026-09-29 16:15 | [AWS fallback Phase 2 · reclaim (reversible) + retention caps](./2026-09-29-aws-fallback-phase2-reclaim-retention.md) | PASS: legacy pollers + 6 OS units disabled/masked (re-enable steps listed); journald 100M/14 d, logrotate, backup retention; MemAvailable 447–464 → min 497 MB; iowait 7.4 % → 0.1 % |
| 2026-09-29 16:15 | [AWS fallback Phase 2 · runtime deploy + Root Monitor write mode](./2026-09-29-aws-fallback-phase2-runtime-deploy.md) | PASS: release `20260929-160245-5ee01b1e` health OK; rollback proven (first install + with prev); rollback-ownership bug found and fixed; `system_monitor` 0→1→0 round-trip with backups; www/health/api 200; trim cron runs |
| 2026-09-29 16:17 | [Globe overlay: AWS deploy + AWS Ohio node/link](./2026-09-29-globe-overlay-aws-deploy.md) | PASS: deploy LANDED 16:10 HST (3 files + 1 line, no restart, allowlist 404s hold); AWS Ohio point and desk↔AWS link LANDED 16:16 (jsdom 18/18); real-browser visual VERIFY PENDING; AWS-side collector PROPOSED |
| 2026-09-30 14:46 | [Interaction modes: identity, council cap, handoff, gated Cursor, recovery draft](./2026-09-30-interaction-modes.md) | PASS script + `verify.sh` + `WO-SRV-RELAY`; live relay seed VERIFY PENDING (process not restarted); Root Monitor clicks not exercised |

Related: [MIGRATION-DOCS-INDEX](../00-architecture/MIGRATION-DOCS-INDEX-2026-09-28.md) · [WO-SRV](../06-development/Work-Orders/Servers_Cutover_Work_Order_WO-SRV-2026-09-27.md) · [G3 Runtime Verification Checklist](../00-architecture/G3-Runtime-Verification-Checklist-2026-09-28.md)

*Folder created 2026-09-29 ~03:40 HST (docs only).*
