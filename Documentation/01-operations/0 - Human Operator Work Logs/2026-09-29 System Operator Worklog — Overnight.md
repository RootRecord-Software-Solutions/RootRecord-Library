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
