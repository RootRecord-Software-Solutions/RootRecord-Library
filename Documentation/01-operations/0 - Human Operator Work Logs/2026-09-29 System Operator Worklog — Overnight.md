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
