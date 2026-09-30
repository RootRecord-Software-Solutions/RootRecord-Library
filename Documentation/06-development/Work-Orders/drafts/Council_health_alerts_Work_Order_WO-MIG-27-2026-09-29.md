# WORK ORDER — Council health alerts

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-MIG-27-2026-09-29 |
| **Date** | 2026-09-30 (HST) |
| **Status** | BUILT — gated off. Not promoted to the active index. |
| **Owner** | RootRecord |
| **Related** | Agent 27, wave D. No later function depends on this one. Build waits on Folders from agent 03 (Council persona prompts) and agent 25 (Council quake Telegram posts). Matrix row 60. Scheduler map row `council-health`. |

**Scope:** Add a Council health check under Communications that reports whether the live relay is the single poller, whether the three Telegram bots answer `getMe`, and whether the relay log shows a `409`. Alerts, when later signed off, post through the current relay quiet gate. This draft does not authorize runtime edits, a job enablement, a relay restart, a Telegram send, a model load, or a GitHub deletion.

---

## 1. Intent

Old `council/council-health` (`scripts/council_health.py`, `scripts/job.py`, `SKILL.md`, `DAILY.md`) ran every 5 minutes. While the AVA console was up it checked one `apps.council` process, Telegram `getMe` for Ava, Bruce, and Carly, a FastFlowLM chat probe, origin `:8787` (and could run `recycle-origin`), and `409` lines in `~/.ollama/skills/logs`. Failures posted to the council group as Ava, with a 30-minute cooldown.

The live system already has one getUpdates owner: `Communications/telegram/scripts/council-relay.py`, started by job `council_relay`. `RR_RELAY_REPLIES` stays `0` (poll and log only). Chat id and voice token names already live in `relay.conf` and `voices.conf`. Inference is `System/scripts/plumbing/run-infer.sh`. A chat probe loads a model, so the default check does not call it. `service_supervisor` already restarts a dead relay. Those stay. This function does not replace the relay and does not start a second poller.

---

## 2. Current reality

### 2.1 What exists

Folder name, used in all three places: `CouncilHealth` (inside Communications). No lowercase twin. No second top-level domain. No `Logs/` directory on the server.

| Item | Location / status |
| --- | --- |
| Server code | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/CouncilHealth/scripts` — not created yet. Package name `CouncilHealth`. |
| Database data | `2 - RootRecord-Database/Communications/CouncilHealth/` — not created yet. `latest.json` and `state.json` (cooldown). |
| Database logs | `2 - RootRecord-Database/Logs/Communications/CouncilHealth/` — not created yet. |
| Live relay (keep) | `Communications/telegram/scripts/council-relay.py`. One getUpdates. Do not edit. |
| Relay config (read) | `Communications/telegram/config/relay.conf` (`COUNCIL_CHAT_ID`). `Communications/telegram/config/voices.conf` (token env names). |
| Relay log to tail | `2 - RootRecord-Database/Logs/Communications/council-relay.log` (written by `ensure-relay.sh`). Do not read `~/.ollama/skills`. |
| Infer (keep) | `System/scripts/plumbing/run-infer.sh`. Probe only when explicitly armed. |
| Job gate (proposed, not added) | `Automations/scripts/jobs.py` id `council_health`, off unless `RR_COUNCIL_HEALTH=1`. |
| `master-key.env` key names | `TELEGRAM_AVA_TOKEN`, `TELEGRAM_BRUCE_TOKEN`, `TELEGRAM_CARLY_TOKEN`. Allowlist only. Names already present. Do not print values. Do not add a second env file. `~/.config/ava-council/secrets.env` is absent. |
| Old source | GitHub `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server-Old` path `council/council-health/`. Not installed on Pacific. |

### 2.2 Completed so far

- [x] Old `council_health.py`, `job.py`, `SKILL.md`, and `DAILY.md` read from GitHub. Live relay, `relay.conf`, `voices.conf`, and `jobs.py` `council_relay` read.
- [x] This draft written. Not on the active work-order index.
- [x] Shell folders staged for Council persona prompts (`Communications/CouncilPersona`) and Council quake Telegram posts (`Communications/CouncilQuake`). Those functions were not built.
- [x] `CouncilHealth` code, Database README, and Logs directory created.
- [x] `jobs.py` gated block added. `RR_COUNCIL_HEALTH` stays unset.
- [x] Offline `--no-network` test passed (exit 0, bots `skipped`, `alerted` false).
- [x] Phase 4 archive and GitHub deletion `55e9c84` done. Matrix row 60, the scheduler map, and `Communications/README.md` corrected. Bruce stats left missing.

### 2.3 Known friction

- Council persona prompts and Council quake Telegram posts have shell folders only (`CouncilPersona`, `CouncilQuake`). The functions were not built.
- `jobs.py`, the Vercel app shell, and `master-key.env` are shared. If any of them is already being edited at build time, pause and name the file.
- Old checks for `apps.council`, origin `:8787`, `recycle-origin`, and `~/.ollama/skills` logs do not match the live relay. Do not restore those paths.
- A model probe through `run-infer.sh` loads a model. It stays off unless `RR_COUNCIL_HEALTH_PROBE=1` and `--probe`.
- An alert is a `sendMessage`. It stays off unless `RR_RELAY_REPLIES=1` and `--alert`, and the 30-minute cooldown has elapsed.
- Phase 4 leaves shared references in old `scheduler-clock/scripts/scheduler.py` and `origin/scripts/routes/crons.py`. Those files are not this function.

---

## 3. Tasks

Do not start these until Alexander accepts this draft and says to build.

1. Pause if `Communications/CouncilPersona` or the Council quake Telegram posts Folder is missing. Name the missing function. Do not build it.
2. Pause if `jobs.py`, the Vercel app shell, or `master-key.env` is already being edited.
3. Add `Communications/CouncilHealth/lib/envload.py`. Allowlist only `TELEGRAM_AVA_TOKEN`, `TELEGRAM_BRUCE_TOKEN`, and `TELEGRAM_CARLY_TOKEN` from `/home/rootrecord/master/master-key.env`. Never print values.
4. Add `Communications/CouncilHealth/scripts/council_health.py`. Write `latest.json` and `state.json` under `2 - RootRecord-Database/Communications/CouncilHealth/`. Append a run line under `2 - RootRecord-Database/Logs/Communications/CouncilHealth/`. Do not call `getUpdates`. Do not edit `council-relay.py`.
5. Checks: exactly one `council-relay.py` process (missing or duplicate is a problem; do not start or kill it); `getMe` for the three tokens (`--no-network` records `skipped`); tail `council-relay.log` since the latest listen line for `409`.
6. Model probe only with `--probe` and `RR_COUNCIL_HEALTH_PROBE=1`, via `run-infer.sh`. No raw `:52625` call. No origin recycle.
7. Alert only with `--alert`, `RR_RELAY_REPLIES=1`, and a 30-minute cooldown since `state.json`. Same Ava token and `COUNCIL_CHAT_ID` as the relay. Default path does not send.
8. If `jobs.py` is free, add one gated block: id `council_health`, `interval_sec` 300, `enabled` only when `RR_COUNCIL_HEALTH=1` (default off), command `council_health.py --no-alert --no-probe`. Do not turn the gate on.
9. Add `Communications/CouncilHealth/README.md` naming the Folder and the three paths.
10. Run the proof test in Notes. Do not set `RR_RELAY_REPLIES`, `RR_COUNCIL_HEALTH`, or `RR_COUNCIL_HEALTH_PROBE`. Do not restart the relay.
11. After that test passes: copy `council/council-health/` (`SKILL.md`, `DAILY.md`, `scripts/council_health.py`, `scripts/job.py`) into `/home/rootrecord/RootRecord-Ecosystem/Old repos deleted and merged/Solar-Pacific-RootRecord-Server-Old/council/council-health/`, keeping the path from inside the old repo. Generated `DAILY.md` goes to that archive and does not go into Pacific, Database, the website, or git. If the archive copy fails, do not delete. After the copy is on disk, delete those same files from the old repo on this machine and on GitHub. Commit that deletion and push it. Do not force-push. Do not delete the GitHub repository. Leave `scheduler-clock/scripts/scheduler.py` and `origin/scripts/routes/crons.py` and name them in the result note.
12. Then add the phase 5 result note to this work order. Correct only Library matrix row 60, the scheduler map `council-health` row, and `Communications/README.md`.

---

## 4. Non-goals

- Do not build Bruce stats posts, Discord, Slack, the economy brief, or the inbox/D1 drain.
- Do not build Council persona prompts or Council quake Telegram posts.
- Do not replace `council-relay.py`, `ensure-relay.sh`, `relay.conf`, `voices.conf`, the poller, EcoFlow BLE, Hawaiʻi weather, the globe collector, camera grabs, Kokoro, or `geology_collect.py`.
- Do not restore origin `:8787`, `recycle-origin`, AVA console files, or `apps.council`.
- Do not set `RR_RELAY_REPLIES=1` or `RR_COUNCIL_HEALTH=1`.
- Do not edit `master-key.env` or add a second env file.
- Do not open a second top-level domain. Do not add a `Logs/` directory on the server.
- Do not import logs, samples, last-state files, or other generated runtime output into Pacific, Database source, the website, or git. `latest.json`, `state.json`, and the CouncilHealth log line are the only runtime records, and they stay under Database.
- Do not send Telegram, play speakers, switch hardware, load a model, or spend cloud money from this draft.
- Do not delete the GitHub repository. Do not delete shared scheduler or origin files.

---

## 5. Key file / path reference

| Path | Role |
|------|------|
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/CouncilHealth/scripts/council_health.py` | New check. Report only by default. No `getUpdates`. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/CouncilHealth/lib/envload.py` | Allowlist loader for the three Telegram token names. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/CouncilHealth/README.md` | Folder name and the three paths. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Automations/scripts/jobs.py` | Proposed gated block only, if the file is not already being edited. Default off. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/telegram/scripts/council-relay.py` | Keep. Do not edit. Quiet gate and single poller. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/telegram/config/relay.conf` | Read `COUNCIL_CHAT_ID`. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/telegram/config/voices.conf` | Read token env names. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/System/scripts/plumbing/run-infer.sh` | Probe target only when `RR_COUNCIL_HEALTH_PROBE=1` and `--probe`. |
| `2 - RootRecord-Database/Communications/CouncilHealth/` | `latest.json`, `state.json`. |
| `2 - RootRecord-Database/Logs/Communications/CouncilHealth/` | One run line per check. |
| `2 - RootRecord-Database/Logs/Communications/council-relay.log` | Existing relay log. Tail for `409`. |
| `/home/rootrecord/master/master-key.env` | Read allowlisted key names only. Do not edit. |
| `council/council-health/` on `Solar-Pacific-RootRecord-Server-Old` | Old source. Archive, then delete those files only. |
| `scheduler-clock/scripts/scheduler.py` (old repo) | Shared. Leave. Name in the result note. |
| `origin/scripts/routes/crons.py` (old repo) | Shared. Leave. Name in the result note. |
| `5 - RootRecord-Library/Documentation/00-architecture/Old-Repo-Migration-Matrix.md` | Phase 5 only: correct row 60. |
| `5 - RootRecord-Library/Documentation/00-architecture/G1-Scheduler-To-G3-Jobs-Map-2026-09-29.md` | Phase 5 only: correct the `council-health` row. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/README.md` | Phase 5 only: note the gated check. |

---

## 6. Open items

**Additional requirements:**

- Alexander accepts this draft and says to build before any file outside this draft is written.
- At build time, pause if Council persona prompts or Council quake Telegram posts has no Folder. Name that function. Do not build it.
- At build time, pause if `jobs.py`, the Vercel app shell, or `master-key.env` is already being edited.
- Sends, model loads, relay restarts, and turning `RR_COUNCIL_HEALTH` on need a separate sign-off. This draft does not give it.
- Phase 4 deletes only `council/council-health/` after the archive copy is on disk. Shared scheduler and origin files stay.
- Phase 5 result note is empty until the build, the archive, and the GitHub deletion exist.

---

## 7. Notes & constraints

- No force-push.
- Secrets stay out of git. Key names only: `TELEGRAM_AVA_TOKEN`, `TELEGRAM_BRUCE_TOKEN`, `TELEGRAM_CARLY_TOKEN`.
- Prefer small reversible steps.
- Sign-off gate: do not set `RR_RELAY_REPLIES=1`, `RR_COUNCIL_HEALTH=1`, or `RR_COUNCIL_HEALTH_PROBE=1`. Do not call Telegram `sendMessage`, call `run-infer.sh`, restart the relay, play speakers, switch hardware, or spend cloud money.
- Proof test, no send and no model load: `python3 "1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/CouncilHealth/scripts/council_health.py" --no-alert --no-probe --no-network --json` exits 0 and writes `2 - RootRecord-Database/Communications/CouncilHealth/latest.json` with each bot `skipped` and `alerted` false.
- Phase 4 archive root: `/home/rootrecord/RootRecord-Ecosystem/Old repos deleted and merged/Solar-Pacific-RootRecord-Server-Old/council/council-health/`. If the archive copy fails, do not delete.
- After phase 4, add a short result note here (what landed, archive path, GitHub deletion commit) and correct only matrix row 60, the scheduler map `council-health` row, and `Communications/README.md`.

---

*Work order prepared 2026-09-30 HST. Update status when closed.*

---

## Archive / location note

This file is a draft. It is not on the active index. Do not auto-promote.

```text
Documentation/06-development/Work-Orders/drafts/Council_health_alerts_Work_Order_WO-MIG-27-2026-09-29.md
```

See `drafts/README.md` and WO-WOGEN-001. Promotion is Alexander's decision: move into `Documentation/06-development/Work-Orders/`, set Status, and add an index row.

**Closed WOs:** set Status → COMPLETE/CLOSED → `git mv` into `Documentation/06-development/Work-Orders/Complete/`.

Human session logs archive under `Documentation/01-operations/archive/YYYY-Www/` (WO-ARCH) — separate from closed work orders.

### Phase 4 / phase 5 result

Landed 2026-09-30: `Communications/CouncilHealth/scripts/council_health.py` and `lib/envload.py`. Job `council_health` is in `jobs.py` and stays off. Proof: `--no-alert --no-probe --no-network --json` exited 0, wrote `latest.json` with each bot `skipped` and `alerted` false. One live `council-relay.py` was seen. No send and no model load.

Archive: `/home/rootrecord/RootRecord-Ecosystem/Old repos deleted and merged/Solar-Pacific-RootRecord-Server-Old/council/council-health/` (`SKILL.md`, `DAILY.md`, `scripts/council_health.py`, `scripts/job.py`).

GitHub: `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server-Old` commit `55e9c84` deleted those four files. The repository was not deleted. Shared `scheduler-clock/scripts/scheduler.py` and `origin/scripts/routes/crons.py` were left. `/home/rootrecord/old ollama/old skills` is a different remote (`Solar-Pacific-RootRecord-Server`) and was not pushed.

Shells only, not the functions: `Communications/CouncilPersona` and `Communications/CouncilQuake`.
