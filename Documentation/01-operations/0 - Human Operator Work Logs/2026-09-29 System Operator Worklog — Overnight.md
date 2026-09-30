# System Operator Worklogs — Overnight

**Date:** 2026-09-29  
**Session:** Overnight — Library full documentation pass (G2→G3)  
**Timezone:** HST  
**Window:** 03:36– HST  
**Status:** ACTIVE  
**Operator:** RootRecord (desk agent for Alexander Storey)

---

## Purpose

A docs-only pass that brings the RootRecord Library in line with tonight's G2→G3 migration state. It adds a Testing thread and an Ideas/Proposals section. No runtime code, services, poller (PID 105444), models or `jobs.py` were touched. Nothing was restarted, and no git commands were run by hand (desk auto-sync commits).

Backup of every file edited: `/home/rootrecord/Database/GITHUB/library-full-doc-pass.bak-20260929-033930/` (the `*.pre-ideas-*` copies were taken before the second round of edits).

---

## Timetable (2026-09-29 HST)

| Time | Step |
| --- | --- |
| 03:36 | Inspected the Library layout (numbered `Documentation/00–06`) and git state. `rg` is not installed, so grep/find were used. |
| 03:37 | Read the evidence in `2 - RootRecord-Database/Logs/Migration/` (post-reboot, NPU/FLM + addenda, Title-case rename, poller realign, viewer, weather/archive, follow-ups, residual survey). |
| 03:37 | Verified every cited SHA with `git log --all`. All were found; `0b7be45` is Pacific and `66cbae7` is Database, not Library. |
| 03:38 | Read-only checks: poller MainPID 105444, NRestarts 11, active since 03:13:28. 0 `LAP=` lines in `automations_current.log`. MemAvailable ~7.8 GB, load 1.65/1.16/1.53. |
| 03:39 | Read-only SOC check: B2 47.56% (03:39:05, ble), B1 5.23% (03:38:10, ble). |
| 03:39:30 | Backup folder created (17 files). |
| 03:40–03:41 | Created `Documentation/07-testing/` (README with policy + index, TEMPLATE, 10 records). Auto-sync `a6ddc69` (03:41:20), `6b4df92` (03:42:23). |
| 03:43 | MIGRATION-DOCS-INDEX: Testing row + full evidence list. Auto-sync `e25bc5e` (03:43:23). |
| 03:44 | WO-SRV / WO-ECO / WO-GH status summaries; checklist, runbook, retirement table refreshes. Auto-sync `125aefd` (03:44:23). |
| 03:44–03:45 | Handoff §11, Library README status + repo map, stale-path fixes (Agent Context INFRASTRUCTURE ×3, WO-RPT-001, WO-WOGEN-001, WO README, Import Playbook, Unmigrated Notes). Auto-sync `e768a29` (03:45:25). |
| 03:46 | Parent steering: add Ideas/Proposals and this worklog. |
| 03:48 | Created `Documentation/08-ideas/` (README index, TEMPLATE, 6 PROPOSED items) and this worklog. Added pointers in the README and MIGRATION-DOCS-INDEX. |
| 03:48:26 | Auto-sync `1136224`: `08-ideas/` (README, TEMPLATE, 6 proposals). |
| 03:49:23 | Auto-sync `6794683`: this worklog, plus the Ideas/worklog pointers in the README and MIGRATION-DOCS-INDEX. |
| ~03:49 | **External drive incident (reported by the parent agent; this pass ran no drive commands):** `/dev/sda1` (NTFS, label DATABASE) disconnected during the 4.67 GB tar of `G2-old-root-20260929`. The kernel re-attached it, but ntfs3 refuses to mount it ("volume is dirty"). The GITHUB-backup tar was created (sha256 `e774daa6…`), but **no copy is verified** and the drive may hold partial files. All internal originals are untouched. **BLOCKED.** |
| 03:51:59 | Second docs pass: backup `/home/rootrecord/Database/GITHUB/library-camera-live-pass.bak-20260929-035159/` (7 files). Read-only check: `jobs.py` runs every camera job from Pacific `Security/Cameras/`, and `cam_server.py` cwd = `Security/Cameras`. Pacific `A-Eyes/` holds only a stale, git-ignored `__pycache__` `.pyc` (09-28 21:06), so it is legacy and KEPT. |
| 03:52 | WO-AEYES current-state paths → `Security/Cameras/` (job `security_camera_frame_grab`, `Media/Images`, `Media/Timelapses`). Ava INFRASTRUCTURE: Security/Cameras canonical, `A-Eyes/` KEPT. Bruce INFRASTRUCTURE: `poller-dashboard.py` is the default viewer via `open-poller-window.sh`, and `poller-watch.py` still exists. LIVE → PASS / VERIFY PENDING with evidence in the Work-Orders README (snapshot + status rows), WO-RPT-001, Ava INFRASTRUCTURE (Energy) and Unmigrated Notes. Auto-sync `794ccc6` (03:53:12). |
| 03:54 | This worklog updated (timetable + sign-off list). |
| 03:55 | **Approved-proposals pass (g3-proposals-impl).** Alexander approved four 08-ideas items: auto-recovery, Pacific `npu-status.sh`, relay quiet-mode inbox, and the weather retention policy (the Weather repo is NOT approved). This pass changes runtime code **with approval**. No restarts, no sudo, no hardware, no Telegram sends, no deletions, no git commands by hand. Backup `/home/rootrecord/Database/GITHUB/g3-proposals-impl.bak-20260929-035910/`. |
| 03:59:54 | `Automations/scripts/supervise-services.sh`. Dry run: weather alive (106159), relay alive (105964). Simulated death: 3× WOULD-RESPAWN, then WOULD-BLOCK. No process was killed. **PASS** (logic). |
| 04:00:26 | Pacific `System/scripts/plumbing/npu-status.sh` (G2 copy KEPT). Idle run: accel0, XRT 2.25.0, lock IDLE, FLM idle (normal). **PASS.** |
| 04:01–04:02 | `council-relay.py` quiet-mode hold → `Database/Logs/Communications/Relay-Inbox/relay-inbox_current.jsonl` (hourly `Archive/`, mode 0600), plus `relay-inbox-replay.py`. The replay script sends only with `--send` + `RR_RELAY_REPLIES=1`. Parse test on synthetic data **PASS**, with `--send` refused (rc 3). |
| 04:02:54 | Auto-sync Pacific `5353e1f`: supervisor, relay, replay, npu-status. |
| 04:03:03 | Auto-sync Database `57172d0`: `.gitignore` `/Logs/Communications/Relay-Inbox/*` (README tracked) + Relay-Inbox README. `git check-ignore -v` confirmed. |
| 04:04:41 | `Weather/scripts/weather-retention.py` dry run on real data: **0 files / 0 bytes** would move, 0 would be deleted. Weather/ = 2,313 files / 497.0 MB, disk free 201.3 GB, no alarms. Report: `Logs/Weather/Retention/weather-retention_dry-run_2026-09-29_0404.md`. Synthetic apply moved items and deleted nothing: **PASS**. |
| 04:05–04:06 | `jobs.py` minimal edit (+22 lines): EVERY_SECONDS `service_supervisor` (300 s, enabled) and ON_AT `weather_retention` (00:30, **disabled**, `--dry-run`). Also updated `Weather/README.md` (§Retention signed off) and the telegram README. |
| 04:06:53 | Auto-sync Pacific `52573e7`: jobs.py, READMEs, weather-retention.py. |
| 04:07:02 | Auto-sync Database `a775c2f`: dry-run report. |
| 04:09–04:12 | Evidence `Logs/Migration/g3-proposals-impl-evidence-20260929T140900Z.md`. 08-ideas: four items → LANDED / VERIFY PENDING, plus the README index. 07-testing: four records plus index rows. Read-only check: relay and weather run in the poller unit cgroup (`KillMode=control-group`), so they reload with the next poller start. |

---

## Needs Alexander sign-off

- [ ] **Poller restart.** Makes `LAP=` (`0ea16cd`) and the other next-start fixes take effect. The running poller predates them.
- [ ] **sudo: `OLLAMA_KEEP_ALIVE=0` in `ollama.service`.** Server default is 5m; the CLI wrappers already pass `--keepalive 0`.
- [ ] **Hardware tests:** Energy arm/disarm and AC always-on (actuating). Also the B1 physical check (both batteries low).
- [ ] **Enabling voice output or Telegram sends.** Relay quiet by default (`RR_RELAY_REPLIES=0`, messages consumed, not answered later). `*-telegram` models are missing.
- [ ] **Removing internal copies after the external-drive backup** to `/run/media/rootrecord/DATABASE/RootRecord-Backups/`. The drive showed `GITHUB-Backups/` and `Previous-Datasets/` at 03:48. Nothing removed. Now blocked by the drive incident below.
- [ ] **Security remediation:** camera stills in the public Database repo; `CONNECTION.json` in Pacific history (`6328af6`); G2 tracking `a-eyes/store/CONNECTION.json`.
- [ ] **External drive `/dev/sda1` (DATABASE) — BLOCKED.** It is dirty and won't mount after the ~03:49 disconnect. Options:
  - (a) `sudo ntfsfix -d /dev/sda1` (or chkdsk on Windows), then remount.
  - (b) Reformat as ext4. This is destructive, but the drive held only tonight's copies.
  - Either way, check the USB cable, port and power first. Then re-run the copy with sha256 verification. Until that passes, **no internal copy may be removed**.
- [ ] G2 retirement of any file (all KEPT). Weather repo decision (PROPOSED, not approved).
- [ ] **Poller restart** also activates `service_supervisor` and the relay quiet-mode inbox (both LANDED / VERIFY PENDING).
- [ ] **Weather retention apply:** review `Logs/Weather/Retention/weather-retention_dry-run_2026-09-29_0404.md`, then enable `weather_retention` and switch it to `--apply`. Open question: should zipped imagery follow the 14-day rule?
- [ ] **Relay replay sends:** `relay-inbox-replay.py --send` with `RR_RELAY_REPLIES=1`.

---

## Not done / left for review

- Ambiguous stale references, listed rather than changed. See the final report and WO-SRV "Status summary — 2026-09-29 ~03:45 HST".
- **WO-SRV open items need updating** for the 04:00 landings (supervisor job, relay inbox, npu-status copy, retention script/job). WO-SRV itself was not edited in this pass.

---

## g3-voice-ailog pass (AI processing log + Kokoro voice port + phrase cache), 03:50–04:17 HST

Runtime code changed with approval. No restarts, no sudo, no playback, no Telegram/AWS sends, no deletions of G1/G2 files, no git commands by hand. Backup: `/home/rootrecord/Database/GITHUB/g3-voice-ailog.bak-20260929-035454/`. The `*.pre-edit-*` copies of jobs.py and this worklog were taken because other agents edited them concurrently. Docs: `00-architecture/Voice-Reports-G3.md`, `00-architecture/AI-Processing-Logs-and-Reports.md`.

| Time | Step |
| --- | --- |
| 03:55 | Database `.gitignore`: `/AI/Kokoro/Kokoro-82M/`, `*.pth`, `*.pt`, `inference_current.jsonl`, `/Media/Audio/Voice/Archive/`. Kokoro-82M copied from G1 (340 MB; `.pth` sha256 `496dba11…ad1e4`, matches the source; G1 untouched). `git check-ignore` confirmed. |
| 03:57 | `run-infer.sh`: one JSON line per request → `Logs/AI/Inference/inference_current.jsonl` (lengths only). FLM output goes through `flm-log-redact.awk` (drops request bodies and model output). New `ai-log-rotate.sh` (daily `Archive/`) and `Reports/ai_processing_report.py`. Pacific auto-sync `b17780c`. |
| 03:58 | AI report run by hand on empty data: **PASS**. Inference test 1: NPU answered, but **rc=1**. Root cause: `set -e` + `kill -KILL` on the already-dead flm pid; the earlier `setsid` change was not the fix. Fixed with `|| true`. |
| 03:59 | Inference test 2: **rc=0**, 4.64 s, FLM peak RSS 2,007 MB, MemAvailable min 5,483 MB. 1 JSON line; flm.log body/output redacted. Clean: 0 flm, :52625 closed, lock IDLE, `ollama ps` empty. Latency field fixed to `$EPOCHREALTIME` (uutils `date` ignores `%3N`). Pacific `5353e1f`. |
| 04:03 | Voice venv `Media/Voice/.venv` (uv CPython 3.12, kokoro 0.9.4, misaki 0.9.4, torch 2.14.0+cpu, spaCy sm). The first render failed because espeak-ng ignores data paths over 160 chars; fixed with a short copy in `~/.local/share/rootrecord/espeak-ng-data`. |
| 04:05 | One clip per persona: **PASS**. Ava / Bruce / Carly 5.1 / 4.6 / 5.1 s, peak RSS ~1.24 GB each, s16 / 24 kHz / mono, 2.0 / 2.0 / 2.95 s. |
| 04:06–04:08 | Steering from Alexander: phrase-clip cache. 68 clips rendered in 3 batches (Bruce 5, Carly 9, Ava 54 incl. 48 chimes), peak RSS ≤ 1,968 MB, load ≤ 4.05. QC **68/68 PASS**. Manifest tracked: Database `a775c2f`, `88b2396`. |
| 04:09 | whisper-tiny round trip (on demand, 576 MB): 59/68 match. 9 clips on the listen list. |
| 04:11 | `system_perf` (Bruce, template + stitch): **PASS**, 23.4 s WAV, 11.6 s wall. All-cached chime stitch: 0.2 s, model not loaded. |
| 04:12 | `jobs.py`: `voice_system_perf` (:06, `RR_VOICE_SYSTEM_PERF=1`) and `ai_processing_report_hourly` (`RR_AI_REPORT=1`), both **disabled by default**, taking effect only at the next poller start. Pacific `d6c3f8f`. |
| 04:14–04:16 | Library docs + 4 test records (07-testing README rows) + MIGRATION-DOCS-INDEX links. Library `3b39824`. |

**Needs Alexander:**
- Listen to the 9-clip list (start with `chime_0200`, `chime_1200`) and the test clips.
- Sign off on voice delivery (Telegram sendVoice needs OGG/Opus; speaker playback) and set the two env gates.
- Respellings for Kalākaua / Liliʻuokalani / Nuʻuanu / Māhele.
- A Grok voice: none exists (open question).
- PROPOSED `single-flight.sh` fix: the RUN banner goes to stdout, and `holder.txt` stores `RR_PROMPT` during a run.

---

## g3-specialists pass (AI specialist models + keyword router), 04:06–04:25 HST

Alexander's request: one isolated Modelfile per function (execution, reasoning, topic, specialty), plus a keyword/topic router that sends each request to the right specialist, loaded on demand only. No restarts, no sudo, no Telegram sends, no model pulls, no hand-run git commands, no G1/G2 files deleted. **`run-infer.sh`, `jobs.py`, the relay and `Media/Voice` were not edited.** Backup: `/home/rootrecord/Database/GITHUB/g3-specialists.bak-20260929-041126/` (Database `.gitignore`, Library 08-ideas/07-testing READMEs, MIGRATION-DOCS-INDEX, this worklog).

| Time | Step |
| --- | --- |
| 04:06–04:10 | Inventory. `ollama list`: no `*-telegram`, no `llama3.2:1b` (that model exists only in FLM). Old Modelfiles found in `/home/rootrecord/old ollama/agents/{ava,bruce,carly}/` (lanes.conf, `FROM dolphin-mistral:latest`, not installed). `~/.ollama/modelfiles` → Database `AI/Ollama/Modelfiles/` (Archive/Development/Production were empty). Reused the G2 council `classify.py` heuristics and Library Agent Context packs + Pacific domain READMEs for grounding. |
| 04:11–04:12 | Wrote 10 specialists to `Database/AI/Ollama/Modelfiles/Specialists/`: `rr-exec`, `rr-reason`, `rr-energy`, `rr-weather`, `rr-system`, `rr-security`, `rr-cameras`, `rr-council-{ava,bruce,carly}`. Bases: `qwen2.5:1.5b-instruct-q8_0` or `llama3.2:3b-instruct-q4_K_M`; `num_ctx` ≤ 4096; exec temp 0.1. Restored `ava/bruce/carly-telegram` into `Modelfiles/Production/`: base changed to 3B, ctx 8192→4096, ideologies block dropped. |
| 04:12 | `ollama create` ×13, all success, disk only. `ollama ps` empty. **The `*-telegram` models now exist**, so the run-infer/relay Ollama fallback resolves again (the relay stays quiet by default). `ava`/`bruce`/`carly` fallback models not rebuilt. |
| 04:13–04:17 | Pacific `System/config/specialist-routes.json` + `System/scripts/plumbing/route-specialist.py` (stdlib; `--explain/--json/--shell/--list/--system`, `--verify-model`; metadata-only JSONL → `Database/Logs/AI/Routing/routing_current.jsonl`, git-ignored) + `test-route-specialist.py`. Auto-sync Pacific `b9044b1` (04:18:57), Database `63bd396` (04:15:00, Modelfiles) and `2da4fa2` (04:19:06: `.gitignore` + Routing README + test table). |
| 04:16 | Router unit test (no models): **35/35 labelled, privacy PASS**. Held-out 5/8 (informational). Table: `Logs/AI/Routing/router-test-2026-09-29.md`. |
| 04:18:13 | Live 1: Ollama `rr-energy`, keep_alive 0, nice 10, single-flight. "No data — I can't see the desk". 6.35 s (cold load 2.56 s). MemAvailable min 9,857 MB. `ollama ps` empty after. |
| 04:18:32 | Live 2: FLM `llama3.2:1b` + `rr-weather` SYSTEM as the system message. "No data — I can't see the desk." 5.14 s incl. cold start; VmHWM ~2,007 MB; MemAvailable min 9,734 MB. After: 0 flm, :52625 closed, lock IDLE. |
| 04:19–04:25 | Library: `00-architecture/AI-Specialist-Models-and-Routing.md` (design, table, config, **gated hook**, resource policy, how to add), 08-ideas record (LANDED / gated), 2 × 07-testing records + index rows, MIGRATION-DOCS-INDEX row. The proposed hook was simulated in isolation: gate off = unchanged; explicit model targets are never overridden. |

**Needs Alexander:**
- Approve applying the 2-line hook to `run-infer.sh` (text in the design doc §4) after the JSONL-logging pass settles, then set `RR_SPECIALIST_ROUTING=1`.
- Decide whether `prefer=ollama` routes (reason/security/council) should skip the NPU (phase-2 hook).
- The sign-off line above ("`*-telegram` models are missing") is superseded: they were rebuilt at 04:12 on `llama3.2:3b-instruct-q4_K_M`.

## g3-template-reports pass (Library templates filled from measured data), 04:27–04:37 HST

- **Built:** Pacific `Reports/template_fill.py` (stdlib) and `Reports/template_validate.py`. They fill all 4 templates in `01-operations/templates/`
  with the same headings, tables, field order, date formats and status vocabulary. Sources are the 07-testing index, the inference JSONL,
  the poller log and hourly archive, host/SOC/camera/weather freshness, the work orders and this worklog's sign-off list.
  Design: [Template-Report-Generation.md](../../00-architecture/Template-Report-Generation.md).
- **Output:** Database `Reports/Generated/<Template-Name>_current.md` with `Archive/` rotation and a validation JSON. **Nothing is written into the Library** (guarded).
- **Validator:** rejects heading, table-column, field, vocabulary and leftover-placeholder mismatches, and flags numbers not in the sources.
  Negative tests: the 3 structural mutations were rejected and the invented numbers were flagged.
- **Samples (04:31–04:34):** 4/4 valid with 0 unsupported numbers. 3 light model calls, all `rr-exec` → NPU on demand, 5969–9217 ms each,
  FLM peak about 2.0 GB, MemAvailable minimum 9879 MB. The worklog used the model's free text. The work order fell back twice because the 1B model
  ignored the `KEY:` format under `run-infer.sh`'s generic voice system prompt. Afterwards `ollama ps` was empty and no flm was running.
  Record: [2026-09-29-template-report-samples.md](../../07-testing/2026-09-29-template-report-samples.md).
- **Fixed during the test:** cloudflared detection (the path contains spaces, so it now uses `/proc/*/comm`). The worklog "Next useful step" must now
  name a real sign-off item (the model wrote a bare "Restart the poller.").
- **jobs.py:** added ON_AT `template_reports_daily` 18:40. `enabled` only if `RR_TEMPLATE_REPORTS=1` at poller start (default off).
  The file was re-read and backed up first (`jobs.py.pre-template-reports`). The poller was **not** restarted.
- **Not touched:** `run-infer.sh`, the relay, `Media/Voice`, `~/Desktop/old txt`.

**Needs Alexander:**
- Decide whether to enable `RR_TEMPLATE_REPORTS=1`. This needs a poller restart (already on the sign-off list).
- The specialist hook (`RR_SPEC_SYSTEM`) would give the NPU path the `rr-exec` format rules. Without it, most drafts fall back to fixed text.
- Promoting generated files into the Library stays manual (copy by hand after review).

## g3-voice-reports2 pass (single-flight fix + 7 more voice reports + pronunciation candidates), 04:20–04:45 HST

Backup: `/home/rootrecord/Database/GITHUB/g3-voice-reports2.bak-20260929-042153/` (with `.pre-edit-*` copies of the files other agents changed concurrently: `jobs.py`, the 07-testing README and this worklog).

| Time (HST) | What | State |
| --- | --- | --- |
| 04:20–04:23 | `single-flight.sh run`: the RUN banner goes to **stderr**. `holder.txt` holds metadata only (`job caller pid ts cmd=<basename> prompt_chars`). `run-infer.sh` / `run-ollama.sh` pass `RR_PROMPT_CHARS` (the length only). Callers checked: run-infer, run-ollama, council-relay, voice-render/voice_generate/system_perf/voice_reports, npu-status, template_fill. One real request: rc 0, 4.27 s, stdout = the reply only, FLM peak 2,007 MB. [Record](../../07-testing/2026-09-29-single-flight-banner-holder-fix.md) | **LANDED, PASS** |
| 04:24–04:35 | New Pacific `Media/Voice/scripts/voice_reports.py`: hourly_chime, nws_weather, energy_report, remaining_tasks, morning/midday/late roll-ups. Output: text `Reports/<report>_current.md` + stitched WAV, Archive rotation, **no delivery**. 13 new catalog clips, 83/83 QC PASS. One test each: 7/7 rc 0, WAV s16/24000/1 QC PASS. Roll-up LLM summary once via run-infer (6.2 s, FLM 2.0 GB). Bug fixed: "Delta 2 36%" was spoken as a clock time. [Record](../../07-testing/2026-09-29-voice-reports-batch2.md) | **PASS**; by-ear VERIFY PENDING |
| 04:31 | `jobs.py` (re-read, backed up): `voice_hourly_chime` [0,30], `voice_nws_weather` [7,22,37,52], `voice_energy_report` [15,45], `voice_remaining_tasks` [32], `voice_morning/midday/late_report` 09:02/12:02/21:02. Flags `RR_VOICE_HOURLY_CHIME`, `RR_VOICE_NWS`, `RR_VOICE_ENERGY`, `RR_VOICE_REMAINING`, `RR_VOICE_ROLLUPS` (+ `RR_VOICE_ROLLUP_LLM`). All default OFF, read at poller start; the poller was **not** restarted | **LANDED** (gated OFF) |
| — | earthquake_hourly / council_quake: no USGS data in Database `Geology/` (empty) and no collector in Pacific `Geology/` (README only). Skipped; no network collector added | **BLOCKED** |
| 04:27–04:41 | Pronunciation Kalākaua, Liliʻuokalani, Nuʻuanu, Māhele: no respellings found anywhere. IPA found for Nuʻuanu/Māhele (Wiktionary, G1 store) and an English-style Liliuokalani in misaki us_gold. 6 candidate clips rendered (`Clips/Ava/proposed_*`, excluded from the stitcher, **not** in the lexicon) and added to the listen list. [Record](../../07-testing/2026-09-29-pronunciation-candidates-proposed.md) | **PROPOSED** |
| 04:42 | Docs: `Voice-Reports-G3.md` §2/§4/§5/§6 (report map statuses, flags), `AI-Processing-Logs-and-Reports.md` §6 (single-flight fix LANDED), 3 new 07-testing records + README rows. Database `.gitignore` + `/Media/Audio/Voice/Reports/Archive/` | LANDED |

**Needs Alexander:**
- Listen to the 6 PROPOSED pronunciation clips (A/B for Liliʻuokalani and Māhele) and the batch-2 report WAVs. Approved respellings then go into `hawaiian_lexicon.py`.
- Pick which voice-report flags to set. Each needs a poller restart (already on the sign-off list). Delivery (Telegram / speakers) is still off and still needs its own decision.
- Earthquake reports need a USGS collector first (a new network poller): yes or no.
- **04:46 HST:** Repointed generated template, AI-processing, and voice text reports to the non-git `RootRecord-Ecosystem/test-reports/{Templates,AI-Processing,Voice}/` tree; copied the existing Database reports without moving or deleting them. No restart, model call, send, or git command.
- [ ] **Untrack generated reports (Alexander approval required):** review the remaining tracked copies in `Database/Reports/Generated/`, `Database/Logs/AI/Reports/`, `Database/Media/Audio/Voice/Reports/`, and the voice `.read.txt`/`.speak.txt` sidecars, then use `git rm --cached` plus `.gitignore`; not performed in this pass.
- **04:49 HST:** Voice Markdown and `.read.txt`/`.speak.txt` outputs now use non-git `test-reports/Voice/`; WAVs and clip cache remain in Database `Media/Audio/Voice/`. Fully cached `hourly_chime` test was run with no model load.

## g3-specialists hook + router v2 pass, 04:49–05:04 HST

- **`run-infer.sh` hook landed (04:56), OFF by default.** The file was re-read first (JSONL logging and single-flight already in) and backed up (`run-infer.sh.pre-hook`).
  - With `RR_SPECIALIST_ROUTING=1`, voices are routed by prompt, and `RR_SPECIALIST=<rr-name>` or TARGET `rr-*` forces a specialist (new `route-specialist.py --force`).
  - Ollama uses the specialist model; FLM/NPU gets the specialist's Modelfile SYSTEM plus its temperature and max tokens. The JSONL gains `specialist` and `route_confidence`.
  - **Flag-off verified byte-identical without a model:** new `System/scripts/plumbing/test-run-infer-hook.sh` (fake FLM server plus stub Ollama): 8/8 identical, 7/7 flag-on checks pass, and a mutated reference is caught.
  - Design: [AI-Specialist-Models-and-Routing.md](../../00-architecture/AI-Specialist-Models-and-Routing.md) §4.
- **Router v2 (04:51–04:55):** keywords and synonyms from the Library domain docs, plus a tightened liveness regex.
  - Fresh held-out set of 27 prompts, written before tuning: **11/27 → 27/27**. That is optimistic, because its failures were visible during tuning.
  - **Blind set of 22 prompts, written after tuning and scored once: 17/22 → 17/22 (no gain).**
  - Original 35 labelled cases stay 35/35; old held-out stays 5/8.
- **`template_fill.py`:** its draft call now passes `RR_SPECIALIST_ROUTING=1 RR_SPECIALIST=rr-exec` (two lines; output-path lines untouched, as owned by the test-reports pass).
- **Live calls (2 total):**
  1. 04:58 work-order re-run → NPU with the `rr-exec` SYSTEM, 7364 ms. The free text **still fell back**: "No data" plus the desk-layout paths, which the number check rejected.
  2. 04:59 `bruce` "rain in Hilo" → `rr-weather` 0.5 → NPU, "No data — I can't see the desk.", 4687 ms.
  - FLM peak about 2.0 GB; MemAvailable minimum 7643 MB. Afterwards `ollama ps` was empty, no flm was running, and the lock was IDLE.
  - Record: [2026-09-29-specialist-hook-and-router-v2.md](../../07-testing/2026-09-29-specialist-hook-and-router-v2.md).

**Needs Alexander:**
- Whether to set `RR_SPECIALIST_ROUTING=1` for the relay and voices. That needs their environment changed and probably a restart.
- Template drafting: pick a facts `DESK_LIVE_FILE` block or a small `rr-draft` specialist (one re-test).
- Router next step: structural fixes plus a new blind set, not more synonyms.

## g3-router-v3 pass (router structural fixes + template desk file), 05:07–05:15 HST

- **Router v3 (router 3.0, config v3):** keyword matching now ignores space/hyphen/underscore differences, so "master key" matches `master-key`. Added energy unit words (kilowatt, kWh, watts, amps, volts, percent) and an rr-reason `comparison_frame` rule, so "better to X or Y" goes to reasoning.
  - A new blind set of 21 prompts was written at 05:08, before any change, and scored once.
  - **Results:** labelled 35/35 kept; new blind **14/21 → 20/21**; 04:55 blind 17/22 → 21/22 (optimistic); old held-out 5/8 unchanged.
- **Template drafting:** `template_fill.py` writes its facts to a temporary desk file (mode 0600, deleted afterwards) and passes it as `DESK_LIVE_FILE`. The `RR_TEMPLATE_SPECIALIST_HOOK=0` off-switch is kept.
  - **2 live NPU calls:** 9580 ms and 7028 ms, FLM peak 2006 MB, MemAvailable minimum 7603 MB.
  - Call 1 was blanked by `run-infer.sh` `sanitize()`.
  - Call 2 got **INTENT accepted but partly unsupported** ("…to ensure accurate data"); SCOPE fell back.
  - Afterwards `ollama ps` was empty, no flm was running, and no temp files were left.
  - Record: [2026-09-29-router-v3-and-template-desk-file.md](../../07-testing/2026-09-29-router-v3-and-template-desk-file.md).

**Needs Alexander:**
- Model free text still needs human review; the number check cannot catch word-only claims.
- Decide whether to add a claim/overlap check or keep templates deterministic-only (`--draft none`).

## control-panel pass (native GTK4 panel + Conky readout), 11:53–12:16 HST

No daytime worklog exists for 2026-09-29, so this section is added here. Backup: `/home/rootrecord/Database/GITHUB/control-panel.bak-20260929-115632/`. It holds the 07-testing README, this worklog, and copies plus sha256 of every existing viewer, dashboard and script.

| Time (HST) | What | State |
| --- | --- | --- |
| 11:53–11:58 | Survey (read-only) of `poller-dashboard.py` (B1/B2/B3 laptop bars, 8 service rows, SYS, SUN, log; 5 s snapshot), `poller-watch.py`, `open-poller-window.sh`, autostart + Desktop launchers, the poller ENERGY status line (heartbeat every 60 s, `/health`) and `npu-status.sh`. Toolkit: system python3 3.14.4 has gi 3.56.2, Gtk 4.22.4 and Adw 1.9. **conky is not installed** | done |
| 12:03 | New Pacific `Apps/Control-Panel/`: `rr_control_panel.py`, `Lib/rr_sources.py`, `Lib/rr_settings.py`, `settings.json`, `Conky/`, `Packaging/`, `Tests/run-check.sh`, `README.md`. Read-only; one 5 s GLib timeout refreshes the header plus the visible page. There are 9 pages: Energy, Weather, System, NPU, AI log, Poller/services, Cameras, Controls, Settings (Known URLs, camera toggles). The camera viewer is OFF by default | **LANDED** |
| 12:03–12:09 | `--check` viewer off: PASS, peak RSS 73.8 MB, camera work 0 (strace: 0 `Media/Images`, 0 `:8791`, 0 `CONNECTION.json`). Viewer on: PASS, 4/4 stills, 87.8 MB. Real window (Alexander away, permitted): 30 s at 85.0 MB with the cairo renderer (default renderer ~180 MB). All 10 page screenshots are in `RootRecord-Ecosystem/test-reports/Control-Panel/20260929-120924-*.png`. Window closed; no process left. [Record](../../07-testing/2026-09-29-control-panel-gtk.md) · [Architecture](../../00-architecture/Control-Panel-GTK.md) | **PASS**; window RSS over the 80 MB target (flagged) |
| 12:10 | `.desktop` launcher installed to `~/.local/share/applications/rootrecord-control-panel.desktop` (validated). The systemd --user unit is written to the repo only (not installed or enabled). The Conky config is in the repo only (conky missing) | LANDED; autostart + Conky **VERIFY PENDING** |
| 12:12 | Existing files re-hashed: all 10 unchanged. Poller PID 105444 is still up (not restarted). No sudo, apt, sends, playback, model loads or git writes | PASS |

**Needs Alexander:**
- `sudo apt install conky-all`, then `bash Apps/Control-Panel/Packaging/install-launcher.sh` and `conky -c ~/.config/conky/rootrecord.conkyrc`. Autostarting Conky is a separate decision.
- Enable the panel autostart: copy the unit, then `systemctl --user daemon-reload && systemctl --user enable --now rootrecord-control-panel.service`.
- Risky panel actions (poller restart; Telegram, voice and `RR_*` are not wired): set `risky_actions_enabled` and per-action `signed_off` in `settings.json` only after sign-off.
- Accept the ~85 MB window RSS against the 80 MB target, or ask for a slimmer build.
- Note: SUN is empty in both the dashboard and the panel, because today's row is missing from `solar_calculation_table_current.md` (existing data issue, not changed).

## root-monitor pass (rename + Running / Network / SSH / Not-migrated pages + every setting), 12:35–13:10 HST

Backup: `/home/rootrecord/Database/GITHUB/control-panel-settings.bak-20260929-123505/` (+ `Control-Panel-before-root-monitor-1244.tgz`). No daytime worklog exists, so this section is added here.

| Time (HST) | What | State |
| --- | --- | --- |
| 12:35–12:44 | Discovery (read-only): config sources across Pacific / Database / home configs, env vars used by scripts, `~/.ssh/config` (aliases only), Library WO / retirement / checklist docs. Starlink dish reachable at 192.168.100.1:9200; no Starlink tooling in the repos | done |
| 12:45 | `Apps/Control-Panel/Starlink/.venv` (uv, py3.12, `starlink-grpc-core` 1.2.5 — `starlink-grpc-tools` is not on PyPI) + read-only `starlink_status.py` (get_status only): CONNECTED, ~54 ms, 0.07 % obstructed | **PASS** |
| 12:47 | One read-only SSH check each: `rr-aws` FAIL (ProxyCommand binary `~/.local/bin/cloudflared` missing), `rr-aws-ip` FAIL (5 s timeout) | FAIL (config / remote side) |
| 12:50–13:03 | App renamed **Root Monitor** (title, header, `.desktop` Name; paths + app id kept). New pages Running, Network (+ Starlink), SSH, Not migrated (23 placeholders), Settings hub with 10 sub-pages from `Lib/rr_registry.py` (1,590 settings, secrets masked, masked diff → confirm → 0600 backup → atomic write, never restarts). New launcher "Poller Dashboard (terminal)"; `swap-default-viewer.sh` (status/apply/revert) + `root-monitor-autostart.desktop` written, **not applied** | **LANDED** |
| 12:56–13:08 | `Tests/run-check.sh`: `--check` off/on PASS, strace camera-off 0/0, secret leak tests 0, settings editor 103/103 on temp copies (no real setting saved). Window render of 24 pages with a secret guard (0 matches). `--check` RSS 84.5 MB (> 80 MB target), window 85.7 MB. Existing 10 viewer files byte-identical; poller 105444 untouched. [Record](../../07-testing/2026-09-29-root-monitor-settings-running-network-ssh.md) · [Architecture](../../00-architecture/Control-Panel-GTK.md) | **PASS**; RSS **FAIL** (flagged) |

**Needs Alexander:** apply the viewer swap (`Packaging/swap-default-viewer.sh apply`, reversible) or enable the user unit; start Conky (`conky-all` is now installed; config in `~/.config/conky/`); accept ~85 MB RSS; create `rr-flags.conf` before RR_* edits; fix the `rr-aws` ProxyCommand path and add a Mainland Host alias; review 7 security items (cloudflare snapshot fields in git; relay.conf `SECRETS_1/2` are path refs).

## smart-devices pass (WiZ bulbs + Tuya BSD01 plugs foundation in Energy), 13:24–13:40 HST

Backup: `/home/rootrecord/Database/GITHUB/smart-devices.bak-20260929-132525/` (Pacific `.gitignore`, `jobs.py` + pre-edit copy, `Energy/README.md` + pre-edit copy, Database `.gitignore`, Library 07/08 READMEs, this worklog). No daytime worklog exists, so this section is added here.

Commits (auto-sync, verified with `git log`): Pacific `cd48536` (13:29, .gitignore + wiz.py + tuya.py + example config) · `11e7f2d` (13:33, collector, jobs.py gated job, READMEs) · Database `2818128` (13:33, `Energy/Smart-Devices/*-last.json` + README) · Library `225c36f` (13:37, these docs).

| Time (HST) | What | State |
| --- | --- | --- |
| 13:25 | Pacific `.gitignore`: Smart-Devices secrets entries (`config/*.local.json`, `tuya-cloud.env`, tinytuya wizard `tinytuya.json`/`devices.json`/`tuya-raw.json`/`snapshot.json`, `.venv/`) **before** any secrets file; verified with `git check-ignore` | LANDED |
| 13:26–13:28 | `Energy/Smart-Devices/scripts/wiz.py` (stdlib). Broadcast discovery 0 replies (ufw DROP eats broadcast replies) → added `--sweep` unicast; sweep of .1–.254: **0 WiZ bulbs**. LAN (`ip neigh`): .1 router, .33 Night Owl, .35 Delta 2 Wi-Fi (Espressif), .192 private-MAC phone, .210 Espressif (not WiZ, TCP 6668 refused → not Tuya) | **BLOCKED** (no bulbs) |
| 13:28 | `nmcli dev wifi list` (read-only): only `Bmwfarm`; **no `SmartLife-XXXX` AP** (plug likely in EZ fast-blink mode). Desk stayed on Bmwfarm; no Wi-Fi/NM change | BLOCKED |
| 13:29 | Gitignored `.venv` + `tinytuya` 1.20.0; `scripts/tuya.py` scaffold (listen / config-check / status / on / off; reads gitignored `config/tuya-devices.local.json`; template `tuya-devices.example.json`). 20 s listen UDP 6666/6667/7000: 0 packets (ufw drops inbound broadcasts — inconclusive) | LANDED · control **BLOCKED** |
| 13:30 | `scripts/smart_devices_collect.py --discover` → Database `Energy/Smart-Devices/{wiz,plugs,collector}-last.json` (both sources BLOCKED, count 0, exit 0). Mock bulb on 127.0.0.1: save → dim/off/temp → restore → SAME | **PASS** |
| 13:31 | jobs.py `EVERY_SECONDS` `smart_devices_collect` (300 s, nice 10, no internet), `enabled = RR_SMART_DEVICES=="1"`: default False, gated True. Poller 105444 **not** restarted (start 03:13:28 unchanged). Energy README row added (after the concurrent Sun-times row) | LANDED (gated OFF) |
| 13:32–13:36 | Library: [architecture](../../00-architecture/Smart-Devices-Energy.md) (incl. future Root Monitor Energy → Devices page design, BLE relation), [test record](../../07-testing/2026-09-29-smart-devices-foundation.md), [idea: load shedding](../../08-ideas/2026-09-29-smart-plug-load-shedding.md); Database `Energy/Smart-Devices/README.md`. MemAvailable ≥ 6.7 GB throughout; no BLE, sudo, restarts, sends, models or git writes; `Apps/Control-Panel/` not touched | LANDED |

**Needs Alexander:**
- WiZ: check the bulbs are on (wall switch) and on `Bmwfarm`, WiZ app → *Allow local communication* ON, note their IPs; then the single save/dim/restore test can run.
- Plugs: choose **Path A** (pair BSD01 in Smart Life on 2.4 GHz → iot.tuya.com cloud project, Western America, link app account → give Access ID/Secret to the desk via `.venv/bin/python -m tinytuya wizard`, outputs gitignored) or **Path B** (flash Tasmota/ESPHome — confirm ESP8266 vs Beken first).
- Optional: `sudo ufw allow in on wlo1 proto udp from 192.168.1.0/24 to any port 6666:6667` for passive Tuya discovery.
- Enable the collector: `RR_SMART_DEVICES=1` in the poller environment at the next ordinary stack reload.

## migration-geology + old-repo ports pass, 13:12–14:45 HST

Backups: `/home/rootrecord/Database/GITHUB/migration-geology.bak-20260929-131652/` (Pacific `jobs.py`, Geology + Voice READMEs, `voice_reports.py`; Library WOs, checklist, runbook, retirement table, Voice/Geology/Index docs, 07 README, this worklog; Database README + `.gitignore`) and `/home/rootrecord/Database/GITHUB/migration-old-repos.bak-20260929-133118/` (Energy + System READMEs, `jobs.py` after the geology edits). Old repos read from shallow `/tmp/rr-migr` clones (deleted at the end). Poller 105444 **not** restarted; nothing sent, played or loaded.

| Time (HST) | What | State |
| --- | --- | --- |
| 13:12–13:16 | Survey: G1 `Solar-Pacific-RootRecord-Server-Old` (97 tops) + G0 `old` vs Pacific / Database / checklist | done |
| 13:19 | `Geology/scripts/geology_collect.py` real run: Hawaiʻi 10 quakes (largest M2.35 14 km S of Fern Forest), global 33 (M5.6 southern Mid-Atlantic Ridge), HVO 8 volcanoes / 44 notices; **Kīlauea WATCH/ORANGE erupting**, **Mauna Loa NORMAL/GREEN**; rc 0, 2.64 s, 28 MB. Dedupe + timeout paths in temp root | **PASS** |
| 13:20 | `voice_reports.py earthquake_report --no-voice` (temp output) ×2; empty-data gate | **PASS** (text); WAV VERIFY PENDING |
| 13:24 | `kilauea_cams.py` 3 × 200, re-run 304; `earthquakes_backfill.py --days 1 --skip-global` 11 rows (`quakes.db` git-ignored) | **PASS** |
| 13:21–13:31 | `jobs.py` gated entries: `geology_collect` (`RR_GEOLOGY`), `geology_kilauea_cams` (`RR_KILAUEA_CAMS`), `voice_earthquake_report` (`RR_VOICE_QUAKE`), `energy_sun_times` (`RR_SUN_TIMES`), `system_uptime_log` (`RR_UPTIME_LOG`); import check all False unset / True set, no duplicate ids (coexists with `smart_devices_collect`) | LANDED |
| 13:26 | `Energy/scripts/sun_times.py` (06:11 / 18:10), `System/scripts/uptime_log.py tick` (+ gap sim) | **PASS** |
| 13:29 | `Media/Video/scripts/mp4_converter.py` synthetic 2 s → h264 + aac | **PASS** |
| 13:33–13:38 | Library: [Old-Repo-Migration-Matrix](../../00-architecture/Old-Repo-Migration-Matrix.md) (23 migrated / 29 partial / 38 missing of 90), test records [geology](../../07-testing/2026-09-29-geology-earthquakes-hvo-collector.md) + [batch 1](../../07-testing/2026-09-29-old-repo-ports-batch1.md), WO-SRV/ECO/GH, checklist, runbook, retirement table (all **KEPT**), Voice-Reports-G3, Geology ownership, index. Database evidence `Logs/Migration/migration-geology-evidence-20260929T2319Z.md` | LANDED |
| 13:39 | Backup 3 `/home/rootrecord/Database/GITHUB/migration-hurricane-desk.bak-20260929-133959/` (`voice_reports.py`, `jobs.py`, Voice README, Voice-Reports-G3, matrix, 07 README) | done |
| 13:41–13:44 | `voice_reports.py hurricane_desk` (Hurricane Nolo 273 nm W of Līhuʻe, 85 kt, moving N ~8 kt; no tropical NWS alerts) + `kilauea_report` (WATCH/orange, erupting, VAN excerpt, 10 quakes ≤150 km, Mauna Loa normal); empty-data gates; regression earthquake/nws. [Record](../../07-testing/2026-09-29-voice-reports-batch3-hurricane-kilauea.md) | **PASS** (text); WAV VERIFY PENDING |
| 13:43–13:44 | jobs.py `voice_hurricane_desk` (`RR_VOICE_HURRICANE`), `voice_kilauea_report` (`RR_VOICE_KILAUEA`), gated OFF; import check OK, 42 ids, no duplicates | LANDED |
| 13:45 | **Standing rule received:** no jobs.py edits unless Alexander asks or a WO requires it. The 7 blocks already added are left in place (not reverted), all OFF; exact blocks in Database `Logs/Migration/migration-jobs-py-additions-20260929.md`. No jobs.py edits after this | KEPT (sign-off item) |
| 13:46–13:50 | Docs: Voice README, Voice-Reports-G3, matrix (13 rows touched; sign-off list), WO-SRV addendum, checklist, retirement table (KEPT) | LANDED |
| 13:49 | Backup 4 `/home/rootrecord/Database/GITHUB/migration-quake-locations.bak-20260929-134920/`; G0 nearest-location tag ported into `geology_collect.py` + dataset `Geology/config/global-locations.json` (verbatim G0 copy). Temp + one real `quakes` run: Hawaiʻi 9/9, global 14/34 tagged; matrix now 24 / 28 / 38 | **PASS** |
| 13:53 | **Steering received:** breadth over depth. Port every remaining item that can be done cleanly, gated off, with a light smoke test each; record BLOCKED items and move on | noted |
| 13:57 | Backup 5 `/home/rootrecord/Database/GITHUB/migration-breadth.bak-20260929-135720/` (voice_reports.py, domain READMEs, Database `.gitignore` + README, Library docs) | done |
| 13:58 | `Communications/web-facts/scripts/web_facts.py` (G1, logic unchanged): USGS version `2.7.0`; non-allowlisted host + http refused | **PASS** |
| 13:59 | `Reports/News/scripts/{_collector,hawaii_news}.py` (G0), temp root: rc 0, 12.3 s, 31 MB; 25 × HTTP 404, 0 posts | **FAIL** (content) |
| 14:00 | `System/scripts/host_desks.py` net-sample / net-usage / security (G1 host-metrics), temp root: wlo1, 56.7 MB/h simulated; counts-only security snapshot | **PASS** |
| 14:01 | `voice_reports.py solar_desk` (Bruce) / `security_desk` / `bandwidth_desk` (Carly), `--no-voice`, temp output | **PASS** (text); WAV VERIFY PENDING |
| 14:02–14:05 | Database `.gitignore` (+ News `*.db*`, `System/network/Daily/`); System / Communications / Reports / Voice / Geology READMEs; new [Pending-Job-Registrations-2026-09-29](../../00-architecture/Pending-Job-Registrations-2026-09-29.md) (5 PROPOSED blocks; **no jobs.py edit**) | LANDED |
| 14:09 | `Communications/live-wx/scripts/live_wx.py` (G1 live-wx): `--offline` 0.12 s 26 MB; live 2.07 s 29 MB — NWS "This Afternoon, 78F, Isolated Rain Showers", High Surf Advisory (Big Island), Hurricane Nolo 270 nm from Līhuʻe | **PASS** |
| 14:06–14:12 | Matrix rows 17 / 34 / 35 / 39 / 42 / 48 / 50 / 60 / 76 / 79 (now **27 / 27 / 36**, 23 touched); [breadth test record](../../07-testing/2026-09-29-old-repo-ports-breadth-batch4.md) with a check-later list; Voice-Reports-G3, checklist, retirement table (KEPT), index, WO-SRV / ECO / GH addenda | LANDED |
| 14:10 | Reviewed, BLOCKED: council health / Bruce stats (bot tokens, chat-probe model load, alert sends), load categories (field map), official-weather-media (HLS/HWO not collected + OBS), report ledger / catch-up / readiness (playback + report_generation), sunrise-restore (playback), economy brief (MySQL + Discord) | BLOCKED |
| 14:16 | User request (breadth pass 2): fix the 3 voice text items, seed Hawaiʻi news, port the remaining unblocked rows (gated / on demand, smoke each, check-later list), update matrix counts + docs. Backup `/home/rootrecord/Database/GITHUB/migration-breadth2.bak-20260929-141732/` (24 files). Fresh G1/G0 shallow clones in `/tmp/rr-migr2/` | started |
| 14:18 | Voice fixes: `speakable.spoken_clock` "two oh one p.m."; `voice_reports.spoken_watts` ("zero watts", idle devices); `spoken_hhmm` sun times. Re-smoke solar / security / bandwidth / energy / morning / kilauea rc 0 (0.1–0.64 s, ≈ 21 MB) — [batch 5](../../07-testing/2026-09-29-old-repo-ports-breadth-batch5.md) | **PASS** (text) |
| 14:25 | Hawaiʻi news: `_collector.run(seed_feeds=…)` + 16 `SEED_FEEDS` (each 200 with items; `RR_NEWS_SEEDS_ONLY=1`). Seeds-only 11.6 s → **278 posts**; full 22.8 s, same + 25 × 404 (temp roots). News README + Pending block updated | **PASS** |
| 14:27 | Steering (Alexander via parent): document everything in the Library as you go — 07-testing record + README row per smoke test, worklog, matrix, docs per function + gate flag | noted |
| 14:27 | `Weather/scripts/official_statement.py` (G1 official-weather-media HLS): Nolo HLS 7014 chars, re-run changed=False; one real run (git-ignored `/Weather/`). **Correction:** poller already collects HWO; only HLS was missing | **PASS** |
| 14:28 | Voice `official_weather` (Ava; HLS ≤ 24 h → HWO → AFD) text PASS on AFD; `boot_brief` (Ava, G1 boot-prelims) text PASS (BUILD-order NameError fixed; 15 reports import) | **PASS** (text); WAV VERIFY PENDING |
| 14:31 | `Reports/scripts/report_board.py status\|run-due` (G1 board + 14:00 catch-up, text only): midday caught up 0.65 s; second run nothing_due; rollover; bad arg rc 2 (temp root) | **PASS** |
| 14:33–14:36 | `Energy/scripts/load_categories.py` (68 W Starlink/lights; night scenario), `Weather/hurricanes/scripts/global_board.py` (4/4 sources, 7 storms, 2.9 s, temp root), `System/scripts/host_hw.py` (48 °C, nvme 56.5%, GPU 1%, NPU 0%), `Media/Voice/scripts/speech_scrub.py` | **PASS** |
| 14:37 | Library `00-architecture/G1-Scheduler-To-G3-Jobs-Map-2026-09-29.md`: 64 G1 job ids → G3 state (matrix row 15) | done |
| 14:38–14:45 | Docs: Pending (5 new PROPOSED blocks + summary table: `RR_OFFICIAL_HLS`, `RR_VOICE_OFFICIAL`, `RR_VOICE_BOOT`, `RR_REPORT_BOARD`, `RR_HURRICANE_GLOBAL`), matrix (**35 / 22 / 33**, explicit buckets, blockers 7/9/10 closed), [batch 5](../../07-testing/2026-09-29-old-repo-ports-breadth-batch5.md) + 11 README rows, batch 4 update note, Voice-Reports-G3, Pacific Voice / Weather / Energy / System / Reports READMEs, checklist, retirement table (7 rows KEPT), index, WO-SRV / ECO / GH, Database jobs-additions addendum. jobs.py untouched | done |
| 14:45 | Reviewed, still BLOCKED / OUT: cams YouTube ids (OBS), sunrise-restore / replay / readiness (playback), council health (tokens + sends), drop-runner / fs-index / broadcast / FastAPI session builder (security scope), `reset_series.py` (data-moving), product / website. No clean candidates left | reviewed |

**Needs Alexander:** keep or remove the 7 jobs.py registrations (sign-off item; standing rule), then set `RR_GEOLOGY=1`, `RR_KILAUEA_CAMS=1`, `RR_VOICE_QUAKE=1`, `RR_VOICE_KILAUEA=1`, `RR_VOICE_HURRICANE=1`, `RR_SUN_TIMES=1`, `RR_UPTIME_LOG=1` at the next poller start; approve deliveries (council-quake Telegram, Discord, speakers — BLOCKED); approve a full-range quake backfill; accept Geology last-json commit churn; retirement of G1/G0 sources stays KEPT until you sign off. Breadth batch: register (or not) the 5 PROPOSED jobs in [Pending-Job-Registrations-2026-09-29](../../00-architecture/Pending-Job-Registrations-2026-09-29.md); pick Hawaiʻi news seed feeds; work the check-later list in the [breadth test record](../../07-testing/2026-09-29-old-repo-ports-breadth-batch4.md). Breadth pass 2 (14:45): also decide the 10 PROPOSED blocks in Library `00-architecture/Pending-Job-Registrations-2026-09-29.md`, review the 16 Hawaiʻi news seed feeds, and decide whether `Reports/board/daily-reports-due.json` is tracked.

## us-mainland-import pass (US-Mainland-Server desk checkout + AWS read-only check), 13:45–14:00 HST

Backup: `/home/rootrecord/Database/GITHUB/us-mainland-import.bak-20260929-134629/` (target folder tgz + listing, `~/.ssh/config`, clone originals `README.md`/`.gitignore`/`communications/.env.example` + HEAD, Library 07/08 READMEs, this worklog, WO-SRV).

| Time (HST) | What | State |
| --- | --- | --- |
| 13:45 | Pre-checks: target existed with only an empty `Communications/` (2026-09-27, not a repo); `gh` logged in (`rootrecordsoftwaresolutions`, keyring); repo PUBLIC, `main` `b61d63c` | done |
| 13:47 | Cloned to a staging sibling (git refuses a non-empty dir), moved every entry incl. `.git` into the target after a per-entry conflict check, removed the empty staging dir. Remote token-free HTTPS, status clean; placeholder kept | **PASS** |
| 13:47 | Auto-sync: Pacific `github_sync_all` → `sync-all.sh` → `repos.conf`; row `mainland` is **disabled** and points at the empty G2 `~/.ollama/skills/us-mainland-server`. Not changed (sign-off line in the [architecture doc](../../00-architecture/US-Mainland-Server.md)) | BLOCKED (sign-off) |
| 13:47 | `~/.ssh/config`: only the `rr-aws` ProxyCommand path → Pacific `Communications/network/cloudflare/bin/cloudflared` (quoted). One `ssh -o BatchMode=yes -o ConnectTimeout=5 rr-aws uptime`: `websocket: bad handshake`, exit 255; tunnel hostnames return Cloudflare 1033 (no connector on AWS). `rr-aws-ip` [redacted public IP]: TCP timeout | **FAIL** (remote / stale IP) |
| 13:49 | One read-only SSH to the collector's AWS address [redacted public IP]: up 3 d, 514 MB RAM avail, disk 77 % (1.6 G free); running poller + globe feed/history + github-poller only; **`hawaii.ndjson` 1.82 GB, +39 MB/h, trim script missing → disk full ≈ 40 h** | **PASS** (read) · finding **urgent** |
| 13:50–13:52 | Checkout setup (uncommitted): root `.env.example` (57 names, no values), README *Desk checkout layout* section with proposed Title-case mapping (no rename — AWS pulls every minute and references lowercase paths), `.gitignore` `__pycache__/` + `*.py[cod]` | LANDED |
| 13:52–13:58 | Library: [architecture](../../00-architecture/US-Mainland-Server.md), [test record](../../07-testing/2026-09-29-us-mainland-import-and-ssh.md), [AWS plan](../../08-ideas/2026-09-29-aws-mainland-improvement-plan.md), WO-SRV addendum. No sudo, restarts, sends, models, AWS mutation, jobs.py or Control-Panel edits | LANDED |

**Needs Alexander:**
- **Urgent (≤ 1 day):** OK to deploy `network-globe/maintain-hawaii-feed.sh` to AWS `…/network-globe/network-globe/scripts/` and run it once (plan P0-1, exact commands) — frees ~1.7 GB.
- Enable auto-sync: replace the `mainland` row in Pacific `Github/scripts/repos.conf` with the line in the architecture doc (3 pending files then push and reach AWS in ~60 s).
- Elastic IP (or accept dynamic IP) and update `rr-aws-ip` HostName to [redacted public IP]; restore cloudflared on AWS for `rr-aws` / `www.rootrecord.cloud`.
- Decide: Title-case rename (coordinated with AWS paths), repo public vs private, root git pull on AWS, `github-poller`/`ip-notify.sh` not in repo.

## website-staging pass (RootRecord-Cloud Vercel site → Pacific `Communications/website/`), 14:01–14:15 HST

Backup: `/home/rootrecord/Database/GITHUB/website-staging.bak-20260929-140240/` (empty-folder listing, Pacific `.gitignore`, `Communications/README.md`, Library 07 README + this worklog, plus pre-edit copies taken after concurrent edits).

| Time (HST) | What | State |
| --- | --- | --- |
| 14:01–14:02 | Inspect (read-only): target `Communications/website/` **empty** (created 13:28); repo PUBLIC, Next.js 15 App Router, `vercel.json` `{"framework":"nextjs"}`, Vercel Git integration (vercel[bot] Production deploy of `84dec4a` success); `scripts/auto-push.py` commits + pushes (never run) | done |
| 14:02 | Decision **Option B**: own clone in a Pacific-gitignored subfolder (Vercel deploys from that repo; Pacific ignores `*.jpg`; avoids a second source of truth). `.gitignore` entry added and `git check-ignore` verified **before** the clone so auto-sync cannot record a gitlink | LANDED |
| 14:03 | `git clone` → `Communications/website/RootRecord-Cloud/` @ `84dec4a` (50 files, 1.2 MB); Pacific shows it only as `!!` | **PASS** |
| 14:03 | `npm ci --ignore-scripts` at nice 10 under a 2 GB memory watch: 30 packages, 8 s, min 6.5 GB avail | **PASS** |
| 14:04 | `npm run build`: Next.js 15.5.23, 293 static pages, 33 s, min 5.7 GB avail, peak RSS 505 MB | **PASS** |
| 14:05 | `next start` 127.0.0.1:3099 ~5 s: `/`, `/blog`, `/status` 200; `/api/not-allowed` 404; `/api/health` 530 from `origin.avaivy.cloud`. Stopped; port closed | **PASS** · origin **FAIL** |
| 14:05–14:12 | Pacific `Communications/website/{README.md,.env.example}` (6 env names, no values) + `Communications/README.md` row; Library [architecture](../../00-architecture/Website-RootRecord-Cloud-Staging.md) + [test record](../../07-testing/2026-09-29-website-rootrecord-cloud-staging.md). Read-only live checks: vercel.app 200; `rootrecord.cloud` → `www` → 530 (AWS globe tunnel down) | LANDED |

No deploy, push, Vercel settings, jobs.py, Control-Panel, AWS, sudo, restarts, sends or models.

**Needs Alexander:**
- Decide what serves `www.rootrecord.cloud` (Vercel site vs AWS globe tunnel) — today the apex redirects to a dead tunnel.
- Pick a live-data origin for the site (`origin.avaivy.cloud` is down; `rootserver.rootrecord.cloud` has no `/api/*` contract), then set `AVA_ORIGIN_URL` in Vercel.
- Optional `repos.conf` row `cloud` (line in the architecture doc) — keep **disabled**: enabling = auto-deploy on every desk edit, and `is_runtime_code_tree` would arm Pacific stack reloads for pulls into this path.
- Retire/guard `scripts/auto-push.py` upstream (requires a push = deploy).

## AWS Mainland pass: Hawaii feed trim, auto-trim, www tunnel restored, `rr-aws-ip` fixed (14:05–14:35 HST)

Approved by Alexander: deploy and run the trim script once, make trimming automatic, restore the tunnel for `www` (keep `www` on the AWS globe, leave Vercel alone), and fix the `rr-aws-ip` HostName. Backups: AWS `/home/ubuntu/rootrecord/bin.bak-hawaii-trim-20260929-140641/` (old script, units, crontab state, timers, stat/df, last 64 MiB of `hawaii.ndjson`) and `/home/ubuntu/rootrecord/bin.bak-cloudflared-20260929-141048/` (mirror config, the leftover `cloudflared-update.{service,timer}`, dir/listener/memory/service snapshots; there were no creds on AWS to back up). Desk: `~/.ssh/config.bak-20260929-140612` and `/home/rootrecord/Database/GITHUB/aws-hawaii-trim-cloudflared.bak-20260929-141557/`. Record: [test record](../../07-testing/2026-09-29-aws-hawaii-trim-and-cloudflared.md).

| Time (HST) | What | State |
| --- | --- | --- |
| 14:05 | Read-only: AWS disk 1.6G free (77 %). The desk collector's writer (`cat >>`, pid 222029) holds the feed open. The script was missing at `scripts/`, which the desk collector calls (journal: exit 127 at 13:40 and 13:55). The repo script was found to be identical to the stray copy in the `network-globe/` root. No `ubuntu` crontab. Passwordless sudo OK | done |
| 14:06 | Desk `~/.ssh/config`: only the `rr-aws-ip` HostName changed, [redacted public IP] → [redacted public IP]. `ssh -o BatchMode=yes -o ConnectTimeout=5 rr-aws-ip uptime` → up 3 days 9:23 | **PASS** |
| 14:06:41 | AWS backup folder created, including a 64 MiB tail of the feed | done |
| 14:07 | Deployed `scripts/maintain-hawaii-feed.sh` (sha256 matches the repo, `chmod +x`, `bash -n` OK). Reviewed it: flock, truncate-in-place on the same inode (the writer keeps appending), and a sub-second window in which appended lines may be lost | **PASS** |
| 14:07:38 | One run at `nice -n 10`: `trimmed 1827611155 -> 50331325 bytes; offset reset`, 0.53 s. Free disk **1.5G → 3.2G** (78 % → 53 %). Feed-server and connection-history both active, and the writer is still appending | **PASS** |
| 14:08 | `ubuntu` crontab: `*/15 * * * * nice -n 10 /bin/bash …/scripts/maintain-hawaii-feed.sh 67108864 50331648 2>&1 \| /usr/bin/logger -t maintain-hawaii-feed`, mirrored in Mainland `network-globe/cron/maintain-hawaii-feed.crontab` | LANDED |
| 14:10 | Tunnel diagnosis: cloudflared was **not installed**. It had been purged on 2026-09-26 02:41 HST, together with its unit and `/etc/cloudflared`; before that it ran the token tunnel `rootserver` [redacted tunnel ID], not the globe. `config-globe.yml` points at tunnel `network-globe` **[redacted tunnel ID]**, but its creds JSON was missing on AWS. The globe web server (`server.js`, expects :8090) was not running; only feed-server :8787 was. `cloudflared tunnel list` on the desk (existing origin cert) showed [redacted tunnel ID] with **0 connections**, which explains the 1033 on `www` | done |
| 14:11 | Official cloudflared .deb 2026.9.3 installed. The [redacted tunnel ID] creds JSON was copied from the desk's old aws-sync mirror to `~ubuntu/.cloudflared/` at 0600 (contents never printed). Ingress validated (`www → 127.0.0.1:8090`, `ssh → ssh://localhost:22`, 404) | LANDED |
| 14:11 | `network-globe-web.service` (User=ubuntu, PORT=8090) enabled and started; origin `curl 127.0.0.1:8090/` → 200 | **PASS** |
| 14:12 | `cloudflared-network-globe.service` enabled and started; 4 tunnel connections registered. `https://www.rootrecord.cloud/` **530 → 200**, and `rootrecord.cloud` returns 301 → `www`. No tunnel created, no DNS change, Vercel untouched | **PASS** |
| 14:13 | `ssh rr-aws uptime` through the tunnel: the host key presented is the AWS key (`[redacted SSH host-key fingerprint]`, checked against `/etc/ssh/ssh_host_ed25519_key.pub` over direct SSH), and it passes with that key pinned. With the desk `known_hosts` it fails: line 11 still holds the pre-rebuild key (`[redacted SSH host-key fingerprint]`, same as [redacted public IP]). `known_hosts` was **not** edited | PASS (pinned) / FAIL (desk known_hosts) |
| 14:15:02 | First cron fire: `feed 55736202 bytes <= 67108864 -- no trim`. The poller, feed-server, history, web, cloudflared, github-poller and cron are all active. MemAvailable 446 MB (512 MB before), load 1.39/1.17/0.74, no swap | **PASS** |
| 14:30:03 | **First automatic trim from the AWS cron:** `trimmed 67465261 -> 50343031 bytes; offset reset`. Inode 291042 is unchanged and the writer (pid 222029) is still appending. Free disk 3.1G; feed-server, history, web, cloudflared and the poller are active; MemAvailable 456 MB; `www` 200 | **PASS** |
| 14:16–14:28 | Mainland checkout, uncommitted (no git writes): `network-globe/cron/maintain-hawaii-feed.crontab`, `network-globe/network-globe-web.service`, `network-globe/cloudflared-network-globe.service`, `mirror/.cloudflared/config-globe.yml` (+ssh rule), and a README section. Library: test record, 07 README row, AWS plan P0-1 and P0-4 marked LANDED/PASS, a change log plus `rr-aws-ip`/`rr-aws` rows in [US-Mainland-Server](../../00-architecture/US-Mainland-Server.md), and a WO-SRV addendum. **No DNS record changed** (`www` was already routed to [redacted tunnel ID]), no tunnel created, Vercel untouched | LANDED |

Not touched: the poller, the Elastic IP, the `rootserver` tunnel (its connectors are on the desk), Cloudflare DNS/tunnels, Vercel, and the leftover disabled `cloudflared-update.{service,timer}`. There were no desk git writes, desk sudo or restarts.

**Needs Alexander:**
- OK to replace the stale `ssh.rootrecord.cloud` entry in the desk `~/.ssh/known_hosts`: `ssh-keygen -R ssh.rootrecord.cloud`, then pin `[redacted SSH host-key fingerprint]`. After that, `ssh rr-aws uptime` works.
- Enable `mainland` auto-sync (or commit by hand) so the mirrored units and crontab reach GitHub.
- Optional: fix the `connection-history.py` re-ingest after a trim (it inflates daily counters).

## globe-landing pass: glass overlay cards on the Network Globe (`www.rootrecord.cloud` landing), 14:19–14:40 HST

This follows Alexander's design brief: the globe becomes the landing page, with Sign-up / Website Home / Status glass cards and an optional rail, all vanilla JS/CSS. Backup: `/home/rootrecord/Database/GITHUB/globe-landing.bak-20260929-141948/` (`mainland/` originals; `library/` README/worklog copies, with fresh pre-edit copies taken because other agents had edited them; `aws-runtime-readonly/` holds read-only copies of the live AWS `index.html` + `server.js`). Design: [08-ideas/2026-09-29-globe-landing-overlay](../../08-ideas/2026-09-29-globe-landing-overlay.md). Record: [07-testing/2026-09-29-globe-landing-overlay-preview](../../07-testing/2026-09-29-globe-landing-overlay-preview.md).

| Time (HST) | What | State |
| --- | --- | --- |
| 14:19 | Backup taken. Globe source: Mainland checkout `mirror/network-globe/network-globe/` (vanilla, `globe.gl` from unpkg) | done |
| 14:19–14:22 | Sign-up flow check: Vercel `/login` 200, but its API `api-goals.rootrecord.info` is unreachable and `api.rootrecord.info` returns 503, so the card uses **placeholder** mode (badged "Preview · not live", submits nowhere). `rootserver…/health` is plain text with a path, so it is not used | done |
| 14:20–14:33 | Added `overlay/overlay.{js,css}`, `overlay-config.json`, `README.md`, and the desk-only `preview-server.js` + `sample-state.json`. Also +1 `<script>` line in `index.html` and +17 lines in the mirror `server.js` (3-path allowlist) | LANDED (uncommitted; Mainland is not in auto-sync) |
| 14:24–14:26 | Preview on 127.0.0.1:8794 (8791 belonged to another agent's python3). Headless Firefox shots at 1440×900, 1280×540, 390×844 and 360×640. Mobile dock overlapped the HUD, so it was moved to a bottom row and re-shot | PASS |
| 14:27–14:29 | `www` now returns 200 (after the AWS pass). Read-only check: the live AWS globe is a **different Express `server.js`/`index.html`** from the repo mirror (`/health`, not `/healthz`; HTML fallback on every path). The status card was made schema-tolerant (`healthUrls: ["/healthz","/health"]`, `hawaii-feed` collector) | done |
| 14:29 | **P0 security finding:** the live runtime's `express.static(__dirname)` serves `/server.js`, `/package.json`, `/README.md` and `/data/hawaii.ndjson` publicly (206 on a 1-byte range; contents not read). Not changed (AWS change + restart need sign-off) | **FAIL (security) / PROPOSED fix** |
| 14:30–14:31 | Preview B (AWS runtime schema + runtime page copy, production flags) and C (503 failure view) | PASS |
| 14:31 | Cleanup: 0 preview/firefox/memwatch processes, port 8794 closed, min MemAvailable 6.21 GB. One `pkill -f` also killed its own shell; the leftovers were rechecked (0) and the later runs used a PID-based stop | PASS |
| 14:33–14:40 | Design doc, test record, and 07/08 README rows | LANDED |

Screenshots (11): `/home/rootrecord/RootRecord-Ecosystem/test-reports/Globe-Landing/`, covering `desktop-1440x900-{rail,rail-open-status-closed,production-flags,status-down}.png`, `desktop-1280x540-short-cards-closed.png`, `mobile-390x844-{rail,cards-closed,production-flags}.png`, `mobile-360x640-short.png` and `awsruntime-{desktop-1440x900,mobile-390x844}-production-flags.png`. The globe canvas is blank in every shot (no WebGL in headless `--screenshot`), so **drag/zoom under the cards is VERIFY PENDING** in a real browser.

Production flags: `enabled:true`, `rail.enabled:false`, `legacyHud:"compact"`, `cards.signup {enabled:true, mode:"placeholder"}`, **`cards.home.enabled:false`** (until Vercel `/home` is routed), `cards.status {enabled:true, pollSec:15}`, `allowUrlOverrides:false`.

Not touched: AWS (read-only only), `jobs.py`, `Control-Panel`, the poller, DNS/tunnels, Vercel, and the other agent's uncommitted Mainland files. There were no git writes, sudo or restarts.

**Needs Alexander:**
- **Deploy (PROPOSED).** Copy only `overlay/overlay.{js,css}` + `overlay-config.json` to AWS `…/network-globe/network-globe/overlay/` after a host backup, and add 1 include line to the **runtime** `index.html`. No restart is needed. Exact commands are in the design doc and in `overlay/README.md`. Do not copy the mirror `server.js`/`index.html`.
- **Security fix (P0).** Replace `app.use(express.static(__dirname))` with `app.use('/overlay', express.static(path.join(__dirname,'overlay')))`, then restart `network-globe-web.service`.
- Reconcile the mirror with the AWS runtime globe code, and commit the Mainland checkout (enable auto-sync or commit by hand).
- When ready, turn on `cards.home.enabled` (needs `/home` → Vercel routing) and switch `cards.signup.mode` to `link` (needs the goals auth API).

## Android import pass (2 TB drive read-only → `6 - Android Development`), 14:19–14:50 HST

Backup: `/home/rootrecord/Database/GITHUB/android-import.bak-20260929-143931/` (07 README + this worklog). The target was empty before the pass. Records: [inventory](../../00-architecture/Android-Apps-Inventory.md) · [test record](../../07-testing/2026-09-29-android-apps-import.md). Alexander's steering during the pass: the drive is the old home layout, **not** the dying drive; copy only what's needed; 40 GB budget; Kilauea and Weather first; document everything.

| Time (HST) | What | State |
| --- | --- | --- |
| 14:19 | `lsblk`: `sda1` 1.8 T NTFS (WD20EARZ, MAYA enclosure), auto-mounted by udisks at `/run/media/rootrecord/6CD8FA150F0B0035` (ntfs3, rw, relatime). `journalctl -k`: clean attach, no "dirty" line. The 03:50–03:55 dirty/disconnect lines belong to a different 128 GB JMicron drive. `dmesg` not readable | done |
| 14:20–14:23 | Drive inventory with `nice`/`ionice` `find` and heavy dirs pruned (46 s, 0 errors): 39 markers. The only Android "source" is 0-byte symlink remnants in `Solar-Pacific-RootRecord-Server(-Old)-main` zip extracts. Real items: RootMC AAB 1.0.31/1.0.32, RootMC APK 1.0.27–1.0.30, Weather APK ×3 (2026-04-25), `ava-ops-android.tgz` (2026-09-15). No `AndroidStudioProjects`; `Desktop/` empty | done |
| 14:21–14:24 | Desk: `~/AndroidStudioProjects` absent; `~/Database` holds backups only; `~/master` holds an env file only. Full projects found in `~/old ollama/` (4 identical copies each of Kilauea 1.0.47, RootMC 1.0.31, Ava-Ops 0.2.0; `old skills/` is the only one with signing files) | done |
| 14:24–14:31 | GitHub read-only (`gh`): tree scan of 90 repos. Newest Capacitor apps in `mirror-rootrecord-monorepo` `Mobile/` (Weather **1.0.46**, Business 1.0.42, Goals 1.0.9, Farms 1.0.9, Token 0.1.2, Account Hub 0.1.3). Older in `mirror-rootrecord-mobile-development-2026` and the others. Cloned 2 public repos read-only to staging | done |
| 14:33–14:36 | Copied 9 apps (rsync, `--ignore-existing`, excludes build/cache/artifacts, 95 MB `.exe` and `.mp4` dropped from Root-Farms), then Releases/ (7 artifacts; the RootMC 1.0.32 AAB is the only file read from the drive, `--open-noatime`) | **PASS** |
| 14:35–14:38 | `.gitignore` written **before** any secret landed. 17 secrets set to 0600, 24/24 secret and artifact paths `check-ignore`d. The folder isn't a repo and isn't in `repos.conf`, `Push.sh` or `Pull.sh` | **PASS** |
| 14:38 | Capacitor web sources (`Web/apps/<app>-web`, no `node_modules/` or `build/`) added as `<App>/Web-Source/` for the 6 Capacitor apps. Checksum compare 0 diffs. Total **80.7 MB**, 1,033 files | **PASS** |
| 14:37–14:50 | `6 - Android Development/README.md`, Library inventory, test record, 07 README row, this section | LANDED |

Android SDK / Studio / Java: **none on the desk**, so no build (VERIFY PENDING). Library commits (auto desk sync): `1e85c1e` (inventory, test record, 07 row), `7ab947f` (this section). No sudo, remounts, fsck/chkdsk/ntfsfix, drive writes, git writes in any existing repo, restarts, sends or models. `Desktop/old txt` and `I'll sort these models tomorrow` were pruned from every search.

**Needs Alexander:**
- **Security:** some Android signing material is in GitHub repos that aren't private (details in the operator report, not repeated in this public page). Decide on making them private and rotating keys, or accept the risk.
- The Kilauea project folder contains a `github-recovery-codes.txt` (now 0600, ignored). Move it to a password manager.
- Install JDK 17 + Android SDK (+ Studio if wanted) before the first build; fix `sdk.dir` in 3 `local.properties` and Capacitor `webDir`.
- Optional: remount the 2 TB drive `ro` (needs you) or unplug it. Remove the staging clones (`~/.cache/rr-android-import-20260929/`, `/tmp/android-inv/`) when satisfied.

## AWS globe `server.js` static allowlist: closed the file exposure on www.rootrecord.cloud (14:39–14:50 HST)

This was a P0 follow-up under Alexander's AWS approval. Once the tunnel came back at 14:12, the globe server's `express.static(__dirname)` made its whole folder public. Record: [test record](../../07-testing/2026-09-29-aws-globe-static-allowlist.md). Backups: AWS `/home/ubuntu/rootrecord/bin.bak-globe-static-allowlist-20260929-144149/` (server.js, index.html, unit, sha256, access-evidence snapshot); desk `/home/rootrecord/Database/GITHUB/globe-static-allowlist.bak-20260929-144459/`.

| Time (HST) | What | State |
| --- | --- | --- |
| 14:40 | Before probe (1-byte range, body discarded) of 29 paths via www: 22 real files returned **206/416**, including `server.js`, `package*.json`, `README.md`, `collector.js`, `telegram-relay.js`, the scripts, `data/hawaii.ndjson`, `data/hawaii-connections.sqlite3`, `data/geo-cache.json` and `node_modules/**`. `/.env`, `/.git/config`, `/.cloudflared/…` and unknown paths got the catch-all `index.html` (no such files, and dotfiles are ignored, so they didn't leak) | FAIL (exposure confirmed) |
| 14:41 | Read the AWS `index.html` (not the repo copy): it has no local assets, only unpkg `globe.gl` plus the earth texture, and polls `/api/state` every 1 s with no WS/SSE. Backup taken, along with cloudflared counters and the web and feed-server `/proc/io` | done |
| 14:42 | Patch: removed the root static serve; allowlisted `/`, `/index.html`, `/overlay/{overlay.js,overlay.css,overlay-config.json}` (served from `./overlay/` when present), `/health` and `/api/state`; catch-all now 404; `x-powered-by` off; bind `127.0.0.1`. `node --check` passed, then the patch was tested as a throwaway copy on 127.0.0.1:8099 (traversal probes returned 404), then swapped in atomically | **PASS** |
| 14:43:29 | `systemctl restart network-globe-web`: listening on 127.0.0.1:8090 and bootstrapped the feed | **PASS** |
| 14:43–14:44 | After probe: every sensitive path **404**. `/`, `/index.html`, `/?embed=1` **200**; `/health` JSON; `/api/state` flows 119 → 123 (streaming); unpkg assets reachable. Web, cloudflared, feed-server, history and poller all active; MemAvailable 467 MB | **PASS** |
| 14:44 | Outside-access check: no per-request logs exist anywhere. The tunnel counted 55 requests in total from 14:12 to 14:41, and at least 33 were my own checks. The web process's socket-write total over the whole exposure was 4.6 MB, so the 50–66 MB feed was **not** downloaded in full; small files can't be ruled out. **Finding:** `feed-server.js` is public at `http://[redacted public IP]:8787/hawaii.ndjson` (pre-existing since 09-26; only 5.5 KB served in total). Not changed | done · finding |
| 14:45–14:50 | Mainland mirror (backed up first; the repo `server.js`/`index.html`, which are the overlay work, were not touched): added `mirror/network-globe/network-globe/server.aws-live-2026-09-29-allowlist.js` (the AWS copy, sha256 `4ba42236…`) and `AWS-LIVE-SERVER.md` (why, what, diff). Library: test record, 07 README row, this section, and a US-Mainland-Server change-log entry | LANDED |

**Needs Alexander:** close the public feed-server on `:8787`, either with `Environment=GLOBE_BIND=127.0.0.1` in `network-globe-feed-server.service` or by closing TCP 8787 in the security group, once it's confirmed nothing external reads it.

## AWS fallback rebuild, Phase 1: plan, read-only inventory, Root Monitor "AWS Fallback" page in dry-run (14:57–15:20 HST)

This follows Alexander's new direction. The desk is the main copy, and AWS gets rebuilt as a **small fallback**: comms hold, status, the globe, current-only hazards, and buffer-to-relay when the desk is offline. It is not a full offload. Proposal: [08-ideas AWS fallback rebuild](../../08-ideas/2026-09-29-aws-fallback-rebuild.md). Records: [inventory](../../07-testing/2026-09-29-aws-fallback-inventory.md) · [Root Monitor page](../../07-testing/2026-09-29-root-monitor-aws-fallback-page.md). Desk backup: `/home/rootrecord/Database/GITHUB/aws-fallback-phase1.bak-20260929-150225/`. **No AWS changes in Phase 1.**

| Time (HST) | What | State |
| --- | --- | --- |
| 14:57–15:00 | Read-only AWS inventory (`rr-aws-ip`). **t3.micro, 908 MB RAM (not 2 GB)**, no swap, ~445 MB available; 3.1 GB of 6.7 GB disk free; 28–44 % iowait from `connection-history.py` per-record commits; `github-poller` runs `git fetch` every 1 s (14,318 CPU-s); `rr-rootserver-poller` runs 4 dead jobs every 1 s; ports 22 + **8787 public** (feed-server, listed and not changed); only the trim cron; `.env` has 23 keys (names only) | **PASS** (read-only) |
| 15:00–15:02 | Desk survey (read only, `jobs.py` not edited): council-relay 15.9 MB (quiet hold), geology 28 MB / 2.6 s, live_wx / web_facts / hawaii_news 20–31 MB, weather scheduler 420 MB / 2.9 GB (**doesn't fit**). Built an 18-function catalog with RAM, disk, network, fits and default | done |
| 15:02–15:05 | Pacific `Apps/Control-Panel`: added `rr_aws_page.py`, `Lib/rr_aws_fallback.{py,json}`; registered the page after SSH in `rr_control_panel.py` (built on visit, released on leave); `rr_settings.py` defaults `aws_fallback_mode=dry-run`, `aws_fallback_alias=rr-aws-ip`; README | LANDED (dry-run) |
| 15:05–15:10 | Tests: `--check` 14 pages 0 errors 0 leaks; RSS +4.4 MB (80.9 → 85.3); settings 103/103; unit 13/13; live read-only Status (`deployed=0`, avail 439 MB, disk 3170 MB); 3 screenshots in `test-reports/Control-Panel/aws-fallback-20260929/`. The confirm dialog was not confirmed, so nothing was written | **PASS** |
| 15:10–15:20 | Library: proposal, 2 test records + 07 rows, 08 row, this section, Control-Panel-GTK §2 addendum, US-Mainland-Server change-log pointer | LANDED |

**Proposed default-ON:** tunnel, globe_ingest, globe_web, globe_history, desk_watch, status_health, system_monitor, relay_buffer, telegram_hold (only while the desk is offline), geology_current, nws_current, public_ip_notify. globe_feed_8787 stays as it is until you decide. **OFF:** basic_replies (sign-off), hawaii_news, github_poller + legacy_poller (retire), weather_scheduler (doesn't fit).

**Budget:** with the default set on the current t3.micro, only ~279 MB stays free, **below the 512 MB floor**. On t3.small (2 GB), ~1,419 MB stays free. Disk with the caps: ~4.0 GB used, ~2.7 GB free (floor 1.5 GB).

**Needs Alexander (in order):**
1. Elastic IP, then resize to t3.small (or accept a trimmed micro profile)
2. `:8787`
3. Retire `github-poller` and `rr-rootserver-poller`
4. Batch the history commits
5. Phase 2 runtime deploy
6. Desk jobs `aws_heartbeat_push` + `aws_catchup` (`jobs.py` registration)
7. Telegram bot for telegram_hold; basic_replies stays OFF
8. Root Monitor write mode
9. Cut down the AWS `.env`
10. Globe `/api/state` at 5 s + gzip before the Vercel background launch

Commits (auto desk sync). Library: `cc396fc` (proposal, 2 test records, 07 and 08 rows), `fe48f49` (this section, Control-Panel-GTK addendum, US-Mainland-Server change log). Pacific: `890a799` (page, lib, catalog, `rr_control_panel.py`, `rr_settings.py`), `f0836d0` (Control-Panel README). No desk git writes, sudo or restarts; nothing changed on AWS; `jobs.py` untouched.

## globe-overlay v2 pass: Stop/Resume spin, click-info card, hover highlight, fix for the 1 s mesh re-creation (15:43–16:06 HST)

Follow-up to the globe-landing pass. Everything stays inside `overlay.js`, `overlay.css` and `overlay-config.json`: no new server route, and the AWS `index.html` still gets only the one include line. Backup: `/home/rootrecord/Database/GITHUB/globe-overlay-v2.bak-20260929-154351/`. Design: [08-ideas/2026-09-29-globe-landing-overlay §v2](../../08-ideas/2026-09-29-globe-landing-overlay.md). Record: [07-testing/2026-09-29-globe-overlay-v2-spin-click-info](../../07-testing/2026-09-29-globe-overlay-v2-spin-click-info.md).

| Time (HST) | What | State |
| --- | --- | --- |
| 15:43 | Backup of the overlay, mirror `index.html`/`server.js`, `AWS-LIVE-SERVER.md`, the Library docs and the worklog | done |
| 15:44–15:47 | Read-only AWS check. `index.html` md5 is still `f3d03774…`; `server.js` sha256 is `4ba42236…` (allowlist); no `overlay/` on AWS yet; public `/overlay/overlay.js`, `/server.js` and `/data/hawaii.ndjson` return 404. The live page source has `const globe` as a global lexical binding and **no** click or hover handlers. Live `/api/state` key names were recorded (no values) | done |
| 15:48–15:55 | `overlay.js` v2: `findGlobe()` (TDZ-safe); the `⏸ Stop spin / ▶ Resume spin` pill stored as `rr-globe-overlay:v1:spin`; the click-info card (chained `onArcClick`/`onPointClick`/`onGlobeClick`, Esc/× close, 2 s refresh, HST last-seen); hover highlight keyed by flow; escaped tooltips; strict visibility rules (public IPs only, desk-link IP, origin coordinates and process names hidden). New `globe.*` flags in the config | LANDED (uncommitted; Mainland not in auto-sync) |
| 15:55 | Cause of the flaky interaction, found in the globe.gl 2.46.2 / three-globe 2.45.2 source. The page's 1 s `arcsData()`/`pointsData()` refresh uses fresh objects, three-globe joins by object identity, and transitions last 1000 ms, so every mesh was re-created and re-animated every second. Fixed via the overlay (`globe.stableData`: reuse the same object per flow key) | LANDED |
| 15:56–16:01 | jsdom tests (agent box scratch dir, not the desk): **16/16 PASS**. File `overlay/test/overlay.test.js`; log `test-reports/Globe-Landing/v2-unit-test-run.log` | PASS |
| 15:58–15:59 | Desk preview on 127.0.0.1:8794, with the live AWS page copy + allowlist schema and the mirror page. A preview-only probe called the handlers registered on the **real** globe.gl and reported `wired=true · arcClick/pointClick=function · stableId=true`. 8 `v2-*.png` screenshots. On the phone the info card overlapped the stack, so the stack now hides while the card is open; re-shot | PASS |
| 16:00 | Cleanup: 0 processes (PID-based stop), port closed, temp tarballs removed; min MemAvailable 6.08 GB | PASS |
| 16:01–16:06 | `overlay/README.md` (flags, v2 notes, deploy steps for the allowlist server), design doc (§v2, new deploy section, finding 1 marked FIXED, findings 7 and 8), v2 test record + 07 README row, a follow-up note in the v1 record | LANDED |

Real-browser mouse interaction (drag/zoom, click, hover over WebGL) is **VERIFY PENDING**, because headless Firefox paints no WebGL. `index.html` and `server.js` are unchanged in v2. Not touched: AWS (read-only only), `jobs.py`, `Control-Panel`, the poller, DNS, Vercel. There were no git writes, sudo or restarts.

**Needs Alexander:**
- **Deploy (PROPOSED).** Take a host backup, scp `overlay.js`, `overlay.css` and `overlay-config.json` into AWS `…/network-globe/network-globe/overlay/`, and add 1 include line to the AWS `index.html`. No restart. Then do a hand check in a real browser.
- Pin `globe.gl` in `index.html` (unpinned unpkg, 2.46.2 today). The proper tooltip fix also belongs in `index.html`.
- Optional: have the server send a per-flow `lastSeen` on arcs, so the card's "Last seen" is exact instead of the overlay's observed time.

- 16:04 HST — Added desktop launcher `~/Desktop/Root-Monitor.desktop` (copy of `~/.local/share/applications/rootrecord-control-panel.desktop`, chmod +x, gio trusted, desktop-file-validate clean). Opens Root Monitor; revert by deleting the file.

## 16:07–16:20 HST — Root Monitor: switches → labelled buttons; camera viewer button made visible

Request (Alexander): "make toggles buttons. I can't see the camera toggle."

| Time (HST) | Step | Result |
| --- | --- | --- |
| 16:07 | Backup: whole `Apps/Control-Panel` + `~/Desktop/Root-Monitor.desktop` → `Database/GITHUB/2026-09-29_160737_control-panel-toggle-buttons-backup/` (docs added before editing) | DONE |
| 16:08 | Cause: the Cameras page had **no control**, only a hint pointing at Settings → *Cameras* (the camera config-file page). The real `Adw.SwitchRow` was in Settings → **Panel**, third group, **below the fold** inside a nested scroller | FOUND |
| 16:09–16:12 | `rr_ui.state_toggle` (ToggleButton "Name: On" green / "Name: Off" red outline). Big "Camera viewer: Off" button on the Cameras page; the Cameras group moved first on Settings → Panel (same button, synced). Starlink, Still fallback, Show ch1–4, Risky actions (confirm kept) → buttons. `rr_aws_page.py`: minimal swap of `Gtk.Switch` → `state_toggle` (re-read + md5 check right before writing; the other worker's code is otherwise unchanged) | LANDED |
| 16:12–16:13 | `run-check.sh` PASS (viewer OFF/ON, 0 errors, 0 leaks, strace OFF = 0 image syscalls / 0 :8791 connects); `test_settings_io` **103/103**; new `test_toggle_buttons.py` **30/30** (AWS ssh stubbed, nothing written); `rr_aws_fallback` unit checks 12/12 (re-created); RSS no growth (85.4 vs 85.7 MB) | PASS |
| 16:14 | Screenshots, separate NON_UNIQUE instance at nice 10: `test-reports/Control-Panel/toggle-buttons-20260929-161253/` (cameras off/on, settings panel, AWS). Alexander's instance PID 3221324 untouched | PASS |
| 16:15–16:20 | Docs: 07-testing record + README row, Control-Panel README, `Control-Panel-GTK.md` | LANDED |

No git writes, no sudo, `jobs.py`/`settings.json`/`Lib/rr_aws_fallback*` not edited, nothing written on AWS. Stopped here at Alexander's pause request; the fix is complete. **Needs Alexander:** close and reopen Root Monitor (the open window runs the pre-16:10 code).


## 16:09–16:17 HST: globe overlay deployed to AWS + AWS Ohio node

- 16:10 **LANDED**: overlay v2 is on AWS (3 files in `overlay/` plus 1 include line in `index.html`, now md5 `6d9b5af6…`). No restart. Public checks PASS; allowlist 404s hold. AWS backup `/home/ubuntu/backups/globe-landing-20260930-020957/`; desk backup `/home/rootrecord/Database/GITHUB/globe-overlay-deploy.bak-20260929-160933/`.
- 16:12: investigated "no lines from Ohio". Cause: the live `server.js` renders only the desk (Hawaiʻi) feed and has no AWS point, link or collector. The overlay and hiding rules dropped nothing.
- 16:16 **LANDED**: overlay adds an AWS Ohio point and a Hawaiʻi desk → AWS link client-side, with no IP. Flag `globe.awsNode`. Tests 18/18. `overlay.js` sha256 `e08a20e2…`. `/api/state` unchanged.
- **PROPOSED**: a tiny `ss` timer on AWS for AWS's own flows (about 2–5 MB transient, no daemon). Needs a `server.js` change and a restart, so it needs sign-off.
- Caveat: browsers may cache `overlay.js` for up to 4 h. Real-browser visual check VERIFY PENDING.
- Record: `07-testing/2026-09-29-globe-overlay-aws-deploy.md`.

## AWS fallback Phase 2: trimmed-micro profile deployed, then paused in a stable, verified state (15:40–16:20 HST)

Alexander kept the t3.micro and chose the trimmed 7-function profile; AWS changes were approved. At 16:13 the parent passed on that he wants to pause soon, so no new phase was started. **AWS is stable: nothing is half-deployed.** Records:
- [reclaim + retention](../../07-testing/2026-09-29-aws-fallback-phase2-reclaim-retention.md)
- [history batching](../../07-testing/2026-09-29-aws-globe-history-batched-commits.md)
- [runtime deploy + Root Monitor write](../../07-testing/2026-09-29-aws-fallback-phase2-runtime-deploy.md)
- [proposal Phase 2 section](../../08-ideas/2026-09-29-aws-fallback-rebuild.md)

Backups: AWS `~/rootrecord/bin.bak-fallback-phase2-20260929-154333/` (before any change), plus `bin.bak-fallback-deploy-*` for each deploy and `bin.bak-fallback-flags-*` for each flag write. Desk `/home/rootrecord/Database/GITHUB/aws-fallback-phase2.bak-20260929-154400/`.

| Time (HST) | What | State |
| --- | --- | --- |
| 15:41–15:44 | Before metrics: MemAvailable 447–464 MB, disk free 3,166 MB, iowait 7.4 %, writes ~2.2 MB/s | done |
| 15:45 | `github-poller` + `rr-rootserver-poller` disabled (files kept). OS trims: ModemManager / fwupd / udisks2 masked, multipathd + fwupd-refresh.timer disabled | LANDED |
| 15:45–15:50 | `connection-history.py`: batched commits + persisted cursor. Copy test, synthetic trim/restart test, then live. Writes 43.9 → 1.6 MB/min | **PASS** |
| 15:55–16:03 | Desk `deploy-aws-fallback.sh`: dry-run, then apply. The first apply failed the tick and **rolled back by itself**. Fixed, then deployed. A forced-failure test found a restore-ownership bug, which I fixed at once (all files root-owned again, contents verified unchanged). Redeployed and re-tested. Live release `20260929-160245-5ee01b1e` | **PASS** |
| 15:59–16:00 | networkd-dispatcher and the unattended-upgrades shutdown helper disabled (daily upgrades still run); `apt-get clean` −105 MB; journald + logrotate caps | LANDED |
| 16:04–16:09 | Root Monitor `settings.json` set to `aws_fallback_mode=write`; catalog set to trimmed-micro. `system_monitor` 0→1→0 round-trip with 2 dated backups. The GUI test window was closed from outside (someone at the desk), so no more pop-ups | **PASS** |
| 16:13–16:16 | Verify: MemAvailable min 497 MB (0 samples < 485), iowait 0.1 %, disk free 3,278 MB, www `/` `/health` `/api/state` 200, feed-trim cron ran at 16:00 and 16:15 | **PASS** |

**Where I stopped / what's left:**
- Nothing is in progress on AWS.
- Not exercised: a real FALLBACK on AWS and any Data Relay send.
- Still pending sign-off: `:8787` · `telegram_hold` + `basic_replies` (OFF) · `relay_send` (OFF) · AWS `.env` trim · the desk jobs `aws_heartbeat_push` + `aws_catchup` (blocks only, in [Pending-Job-Registrations §C](../../00-architecture/Pending-Job-Registrations-2026-09-29.md); `aws_catchup.py` not written) · globe poll at 5 s + gzip.
- The Mainland checkout `fallback/` is uncommitted (not in auto-sync).

## State at pause, 16:25 HST (2026-09-29)

Docs-only consolidation, 16:24–16:35 HST: no system changes, no git writes by hand, no sudo or restarts, `jobs.py` untouched. Backup of every Library file edited: `/home/rootrecord/Database/GITHUB/library-state-at-pause.bak-20260929-162640/`. Every state below comes from the test records and the sections above.

### LANDED today (afternoon)

| Item | State | Record |
| --- | --- | --- |
| AWS Hawaii feed trim (1.83 GB → 50.3 MB) + `ubuntu` crontab `*/15` auto-trim (first automatic trim 14:30; runs seen at 16:00 and 16:15) | LANDED · **PASS** | [trim + cloudflared](../../07-testing/2026-09-29-aws-hawaii-trim-and-cloudflared.md) |
| cloudflared tunnel restored on AWS (existing globe tunnel, no DNS change); `www.rootrecord.cloud` 530 → **200** | LANDED · **PASS** | same record |
| P0 fix: globe `server.js` static allowlist (source, feed, sqlite, scripts → 404) | LANDED · **PASS** | [static allowlist](../../07-testing/2026-09-29-aws-globe-static-allowlist.md) |
| Globe overlay v2 deployed to AWS (Stop/Resume spin, click-info card, hover highlight, stable meshes) + AWS Ohio node and desk → AWS link | LANDED 16:10 / 16:16 · jsdom 18/18 **PASS** · real browser VERIFY PENDING | [AWS deploy](../../07-testing/2026-09-29-globe-overlay-aws-deploy.md) · [v2](../../07-testing/2026-09-29-globe-overlay-v2-spin-click-info.md) |
| AWS fallback Phase 2 on the trimmed-micro profile (t3.micro, 908 MB RAM): legacy pollers disabled (reversible), history batching fix (writes 43.9 → 1.6 MB/min), release `20260929-160245-5ee01b1e`, Root Monitor write mode (`system_monitor` 0→1→0 round-trip) | LANDED · **PASS** (MemAvailable min 497 MB, iowait 0.1 %) | [reclaim](../../07-testing/2026-09-29-aws-fallback-phase2-reclaim-retention.md) · [history](../../07-testing/2026-09-29-aws-globe-history-batched-commits.md) · [deploy](../../07-testing/2026-09-29-aws-fallback-phase2-runtime-deploy.md) |
| Root Monitor: switches → labelled toggle buttons; visible camera viewer button | LANDED · **PASS** (toggle tests 30/30); the open window runs the pre-16:10 code until it is reopened | [toggle buttons](../../07-testing/2026-09-29-root-monitor-toggle-buttons.md) |
| Desktop launcher `~/Desktop/Root-Monitor.desktop` | LANDED 16:04 (desktop-file-validate clean) | 16:04 line above |
| 9 Android apps imported into `6 - Android Development` (80.7 MB, 1,033 files) | LANDED · copy **PASS**; build VERIFY PENDING (no SDK/Java on the desk) | [Android import](../../07-testing/2026-09-29-android-apps-import.md) · [inventory](../../00-architecture/Android-Apps-Inventory.md) |
| Old-repo migration pass 2: matrix **35 migrated / 22 partial / 33 missing** (90 rows) | LANDED (ports gated OFF; jobs PROPOSED) | [breadth batch 5](../../07-testing/2026-09-29-old-repo-ports-breadth-batch5.md) · [matrix](../../00-architecture/Old-Repo-Migration-Matrix.md) |

### VERIFY PENDING

- **Globe in a real browser:** drag/zoom, click info, hover and the Ohio node over WebGL (headless paints no WebGL; browsers may cache `overlay.js` for up to 4 h).
- **A real fallback on AWS:** desk offline → AWS functions take over → desk catch-up. Not exercised.
- **Relay send:** no Data Relay send has been exercised (`relay_send` is OFF on AWS; desk `relay-inbox-replay.py --send` has not been run).

### Pending sign-offs (consolidated, 16:25 HST)

This is the 16:25 HST pause list. The current operator list is [What's left for Alexander](../2026-09-30-whats-left-for-alexander.md) (refreshed 2026-09-30 02:35 HST). Root Monitor login swap was applied 2026-09-30 02:33. Conky was not started.

- [ ] **`:8787` feed server** on AWS is still publicly reachable: bind it to localhost or close the port in the security group.
- [ ] **Telegram:** `telegram_hold` and `basic_replies` on AWS (both OFF), and a Telegram bot for the hold.
- [ ] **Relay test send:** one approved Data Relay send (`relay_send`, OFF) and/or `relay-inbox-replay.py --send` with `RR_RELAY_REPLIES=1`.
- [ ] **AWS `.env` trim** down to the keys the fallback profile needs (names only are in the inventory record).
- [ ] **Desk jobs `aws_heartbeat_push` + `aws_catchup`:** blocks in [Pending-Job-Registrations §C](../../00-architecture/Pending-Job-Registrations-2026-09-29.md); `aws_catchup.py` is not written yet.
- [ ] **Globe `/api/state` poll 1 s → 5 s + gzip** before the Vercel background launch.
- [ ] **AWS own-connections collector** (a small `ss` timer; needs a `server.js` change and a restart): PROPOSED.
- [ ] **Android signing material** in GitHub repos that aren't private, and a **recovery-codes file** inside an app project folder (now 0600 and git-ignored): make private / rotate, and move the codes to a password manager. Details stay in the operator report, not in this public page.
- [ ] **`rr-aws` known_hosts:** replace the stale desk entry for the tunnel SSH host with the verified AWS host key (see the 14:05 AWS section).
- [ ] **Mainland auto-sync** (repoint + enable the `mainland` row in `repos.conf`) or a hand commit: the Mainland checkout (units, crontab, overlay, `fallback/`) is uncommitted.
- [ ] **The 10 PROPOSED job blocks** in [Pending-Job-Registrations §B](../../00-architecture/Pending-Job-Registrations-2026-09-29.md), plus keep/remove for the 7 gated blocks already in `jobs.py` (§A).
- [ ] **Hawaiʻi news seeds:** review the 16 seed feeds before `RR_HAWAII_NEWS` is registered.
- [ ] **Report board file in git:** keep `Reports/board/daily-reports-due.json` tracked, or ignore it.
- [x] **Root Monitor login swap** applied 2026-09-30 02:33 HST. Conky is still not started. `rr-flags.conf` is created on the first confirmed flag save; it was not created by that swap.
- [ ] **`git rm --cached` of generated reports** (Database `Reports/Generated/`, `Logs/AI/Reports/`, the voice report copies and sidecars) plus `.gitignore` rules.
- [ ] **`OLLAMA_KEEP_ALIVE=0`** in `ollama.service` (sudo).
- [ ] **Pronunciation approvals:** the 4 PROPOSED candidates (Kalākaua, Liliʻuokalani, Nuʻuanu, Māhele) and the by-ear checks.
- [ ] **Retention rules:** Weather retention apply (enable `weather_retention` and switch it to `--apply`; open question: should zipped imagery follow the 14-day rule?).
- [ ] **PAT rotation and the other security items:** rotate the GitHub PAT; camera stills in the public Database repo; `CONNECTION.json` in Pacific history; G2 tracking `a-eyes/store/CONNECTION.json`; the 7 security items from the root-monitor pass.
- [ ] **B1 battery physical check** (River 2 Pro; both batteries were low overnight).

Still open from the overnight list above, unchanged: the poller restart (activates the next-start fixes and any flags), the Energy hardware tests, the external-drive decision, G2 retirement (everything KEPT) and the Weather repo decision.

**Where things stopped:** nothing is in progress on AWS or on the desk. Library docs refreshed in this pass: MIGRATION-DOCS-INDEX (new-docs section), the Library README ("Where things stand"), WO-SRV / WO-ECO / WO-GH, the G3 runtime checklist, US-Mainland-Server (current AWS state table), the retirement table, the migration matrix, Pending-Job-Registrations, the 08-ideas README and the globe design doc state.
