# WORK ORDER — Night-sleep scheduler gate

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-MIG-01-2026-09-29 |
| **Date** | 2026-09-29 (HST) |
| **Status** | ARMED — `RR_NIGHT_SLEEP=1` on the live poller since 2026-09-30 00:02 HST. No `night-mode.json`, so jobs are not skipped. Not on the active index. |
| **Owner** | RootRecord |
| **Related** | Agent 01, Wave A. Later function that depends on this gate: 2, 23:30 late-final report. Old source: `old ollama/old skills/scheduler-clock/scripts/scheduler.py` (`night_sleeping`, `NIGHT_POLL`). Live map: `Documentation/00-architecture/G1-Scheduler-To-G3-Jobs-Map-2026-09-29.md`. |

**Scope:** Add a night-sleep skip gate on the live Pacific poller, reading a `sleeping` flag and leaving every enabled job running until that gate is explicitly turned on. In scope is the gate module, its Database state and log paths, and one call from `run_job()`. Out of scope is writing the flag, sunrise math, audio mute, hardware switching, a new periodic job, and any other agent's function. Built 2026-09-29 with the gate default off. This file stays in drafts. Do not promote it onto the active index.

---

## 1. Intent

The old APScheduler clock wrapped every job. `night_sleeping()` read `~/.ollama/skills/ecoflow-ble-poller/store/state/night-mode.json`. When `sleeping` was true it skipped the job unless the id was in `NIGHT_POLL` (quakes, NWS/NOAA, Kīlauea, radar archive, hurricane fetch/desk, hourly clip prebuild, fs-index). A missing or unreadable file meant not sleeping. The EcoFlow BLE poller wrote that flag for midnight-to-sunrise. This function is only the skip.

The live poller in `rootserver_poller.py` must stay. `run_job()` already skips disabled jobs, jobs after SIGTERM, and `needs_internet` jobs while offline, and it runs every other enabled job around the clock. EcoFlow BLE, Hawaiʻi weather, the globe collector, camera grabs, and `geology_collect.py` stay in place. Nobody in the live tree writes `night-mode.json`. The new gate sits in that poller. It does not replace the poller or those collectors.

---

## 2. Current reality

### 2.1 What exists

Folder name: **NightSleep**, under the System domain. One capitalized folder. No lowercase twin and no symlink.

| Item | Location / status |
| --- | --- |
| Folder | `NightSleep` — installed under System |
| Server code | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/System/NightSleep/scripts/night_sleep.py` |
| Database data | `2 - RootRecord-Database/System/NightSleep/` — last skip written by `--check`; no live `night-mode.json` (missing means not sleeping). Git-ignored. |
| Database logs | `2 - RootRecord-Database/Logs/System/NightSleep/night-sleep.log` — one skip line from `--check`. Git-ignored. |
| master-key.env | No keys. This function reads no secrets. |
| Package / module | `NightSleep` |
| Old skip | `night_sleeping()` and `NIGHT_POLL` inside shared `scheduler.py` |
| Old flag writer | `write_night_state` / `in_starlink_sleep` in the old EcoFlow BLE poller — not this function |
| Live poller | `Automations/scripts/rootserver_poller.py` `run_job()` calls the gate only when `RR_NIGHT_SLEEP=1` at process start |
| Live job map | Gate is armed (`RR_NIGHT_SLEEP=1` since 2026-09-30 00:02 HST). No `night-mode.json`, so enabled jobs still run. |

### 2.2 Completed so far

- [x] Old skip behavior read from `scheduler.py` only
- [x] Live poller `run_job()` read; no newer night-sleep gate existed to enhance
- [x] `NightSleep` module, Database paths, and the `run_job()` call (gate default off)
- [x] Offline test of `should_run` — PASS 2026-09-29 23:59 HST
- [x] Phase 4: no file belongs only to this gate; nothing archived or deleted
- [x] Library pages corrected
- [x] `RR_NIGHT_SLEEP=1` on the live poller (signed off 2026-09-30; restarted 00:02 HST; no night-sleep skips because the flag file is absent)

### 2.3 Known friction

- `scheduler.py`, `SKILL.md`, and `CURRENT.md` under `old ollama/old skills/scheduler-clock/` belong to the whole G1 clock, not to this gate alone.
- The live EcoFlow reader does not write `sleeping`. A missing flag leaves the gate open, matching the old reader.
- `jobs.py` and `rootserver_poller.py` are shared. If either is already being edited when the build starts, pause.
- Turning the gate on changes which jobs run. That needs Alexander's sign-off.

---

## 3. Tasks

Build only after Alexander accepts this draft and says to build. Until then, do not edit runtime files, restart services, send messages, actuate hardware, or spend cloud money.

1. Confirm `System/NightSleep/` does not already exist. This gate does not depend on another Folder. Function 2 (23:30 late-final report) depends on this gate later; do not build that report. If `rootserver_poller.py` or `jobs.py` is already being edited, pause and name the file.
2. Add `System/NightSleep/scripts/night_sleep.py`. Read `sleeping` from `2 - RootRecord-Database/System/NightSleep/night-mode.json`. A missing or invalid file means not sleeping. Never print secret values. There are no master-key.env keys.
3. Allowlist the live ids that match `NIGHT_POLL`: `weather_poller`, `geology_collect`, `geology_kilauea_cams`. Also never skip poller survival jobs the live system must keep: `heartbeat`, `ecoflow_read_boot`, `ecoflow_read_cycle`, `ensure_tunnel_online`, `service_supervisor`, `sys_stats_cycle`, `network_globe_hawaii`, `security_camera_server`, `security_camera_frame_grab`. When the gate is on and `sleeping` is true, skip voice, reports, GitHub sync, and other Ava-style jobs.
4. Call the gate from `run_job()` only. Default off via `RR_NIGHT_SLEEP` unset or `0`, so today's jobs keep running. Do not add a periodic job. Do not edit `jobs.py` unless it is free and the only change is a gated comment that the flag is read at poller start.
5. Do not write `sleeping`, compute sunrise, mute audio, or switch hardware. The old writer stays out of scope. A missing flag is not a missing Folder.
6. Prove it without restarting the poller: a temp JSON with `sleeping: true` lets `weather_poller` run and skips `voice_late_report`; with the file absent, both run. Write the last skip record under Database `System/NightSleep/` and any log line under `Logs/System/NightSleep/` only.
7. After the gate works, archive only files that belong to this function alone into `Old repos deleted and merged/<old-repo-name>/`, keeping the old-repo path. `scheduler.py`, `SKILL.md`, and `CURRENT.md` are shared — leave them. Do not delete the EcoFlow poller or its `night-mode.json`. If no file belongs only to this gate, the archive copy and the GitHub deletion are empty; name that here. If the archive copy fails, do not delete. Do not force-push. Do not delete the GitHub repository. Commit and push only a real deletion.
8. Then update this work order with what landed, the archive path, the GitHub deletion, and the new status. Correct only the Library pages this function made stale: `G1-Scheduler-To-G3-Jobs-Map-2026-09-29.md`, `Old-Repo-Migration-Matrix.md`, `2026-09-29-old-repo-ports-breadth-batch5.md`, and the testing README row. Do not rewrite unrelated work orders.

---

## 4. Non-goals

- Do not replace EcoFlow BLE, the poller, Hawaiʻi weather, the globe collector, camera grabs, Kokoro, or `geology_collect.py`.
- Do not copy the old APScheduler clock over the poller.
- Do not write `night-mode.json` from the BLE poller, compute the sleep window, mute PulseAudio, or switch Starlink, USB, or AC.
- Do not add a new periodic job, and do not enable `RR_NIGHT_SLEEP` on the live poller in this draft.
- Do not edit other agents' files or build function 2 (23:30 late-final report).
- Do not import logs, samples, last-state files, generated reports, images, radar frames, archives, dumps, caches, virtualenvs, `node_modules`, or `__pycache__` into Pacific, Database, the website, or git.
- Do not delete shared `scheduler-clock` files, the EcoFlow poller, or the GitHub repository.
- Do not restore files under `~/.ollama/skills/energy`, automations, or `coms/ssh/local-data-globe`.

---

## 5. Key file / path reference

| Path | Role |
|------|------|
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/System/NightSleep/scripts/night_sleep.py` | New gate module `NightSleep` |
| `2 - RootRecord-Database/System/NightSleep/night-mode.json` | `sleeping` flag; missing means not sleeping |
| `2 - RootRecord-Database/System/NightSleep/` | Last skip record |
| `2 - RootRecord-Database/Logs/System/NightSleep/` | Gate logs only |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Automations/scripts/rootserver_poller.py` | Extend `run_job()` with the gate call; pause if already being edited |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Automations/scripts/jobs.py` | No new job. Optional gated comment only if the file is free |
| `old ollama/old skills/scheduler-clock/scripts/scheduler.py` | Old skip source; shared; do not delete |
| `5 - RootRecord-Library/Documentation/00-architecture/G1-Scheduler-To-G3-Jobs-Map-2026-09-29.md` | Correct after phase 4 only |
| `5 - RootRecord-Library/Documentation/00-architecture/Old-Repo-Migration-Matrix.md` | Correct after phase 4 only |
| `5 - RootRecord-Library/Documentation/07-testing/2026-09-29-old-repo-ports-breadth-batch5.md` | Correct after phase 4 only |
| `5 - RootRecord-Library/Documentation/07-testing/README.md` | Correct the night-sleep row after phase 4 only |

---

## 6. Open items

**Additional requirements:**

- Live launcher `Automations/scripts/poller/run-poller.sh` exports `RR_NIGHT_SLEEP=1` unless already set. Poller restarted 2026-09-30 00:02 HST (pid 372971). Tunnel registered. Scheduler resumed at 00:03:03. No `SKIP — night sleep` lines. `night-mode.json` is still absent, so the armed gate does not skip jobs.
- `jobs.py` was not edited. The flag is read in `rootserver_poller.py` at process start.
- Phase 4 archive path: none. GitHub deletion: none. Shared files left in place: `old ollama/old skills/scheduler-clock/scripts/scheduler.py`, `SKILL.md`, `CURRENT.md`. EcoFlow poller and its `night-mode.json` were not deleted. No commit and no push. Repository `Solar-Pacific-RootRecord-Server-Old` was not deleted.

---

## 7. Notes & constraints

- No force-push.
- Secrets stay out of git. No master-key.env keys for this function.
- Prefer small reversible steps.
- Sends, speaker playback, OBS, hardware switching, deletion of live Ecosystem files, and cloud spend need Alexander's sign-off. This draft does none of those.
- Sign-off gate: enabling `RR_NIGHT_SLEEP` on the live poller. The offline test does not restart the poller.
- Test: temp `night-mode.json` with `sleeping: true` — `weather_poller` runs, `voice_late_report` does not. Remove the file — both run.
- New periodic jobs stay gated off. This gate is not a new job.
- Result (2026-09-29 23:59 HST): `night_sleep.py` and a default-off call in `run_job()` landed. `--check` PASS: with a temp `sleeping: true` file, `weather_poller` runs and `voice_late_report` skips (`last-skip.json` and `night-sleep.log` at 23:59:14-10:00); with the file absent, both run. No live `night-mode.json`. Archive: none. GitHub deletion: none.

---

*Work order prepared 2026-09-29 HST. Update status when closed.*

---

## Archive / location note

**Active / accepted WOs** — filename when saved:

```text
Night_sleep_scheduler_gate_Work_Order_WO-MIG-01-2026-09-29.md
```

Location after acceptance (do not move this file there yet):

```text
Documentation/06-development/Work-Orders/
```

**Drafts (not on active index)** — this file:

```text
Documentation/06-development/Work-Orders/drafts/Night_sleep_scheduler_gate_Work_Order_WO-MIG-01-2026-09-29.md
```

See `drafts/README.md` and WO-WOGEN-001. Do not auto-promote.

**Closed WOs:** set Status → COMPLETE/CLOSED → `git mv` into:

```text
Documentation/06-development/Work-Orders/Complete/
```

Human session logs archive under `Documentation/01-operations/archive/YYYY-Www/` (WO-ARCH) — separate from closed work orders.
