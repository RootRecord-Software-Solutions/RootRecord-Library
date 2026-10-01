# G3 Runtime Verification Checklist

| Field | Value |
| --- | --- |
| **Date** | 2026-09-28 (HST) |
| **Authority** | Supports WO-SRV-2026-09-27 |
| **Rule** | Docs only. Bruce (or operator with shell) runs this. No retirement until each row passes — and even then only with Alexander's explicit sign-off (standing rule 2026-09-29). |

---

## Operator runbook

Use the companion [G3 Runtime Verification Runbook](./G3-Runtime-Verification-Runbook-2026-09-28.md) for exact desk commands, family-specific pass/fail criteria, evidence capture, and retirement gates.

## Purpose

Static path audits are complete. This checklist is the **runtime gate** before retiring corresponding legacy functions on G1/G2 trees.

Run from the Pacific desk (or any host that can see live processes and `jobs.py`).

---

## Preconditions

- [ ] Pacific poller is the only production poller host
- [ ] No second cloudflared / second council-relay intentionally running
- [ ] Desk has shell access to Pacific Ecosystem path and process list

---

## Per-surface checks

### A. Telegram / council_relay

| Step | Pass criteria |
| --- | --- |
| 1 | `council_relay` job points at Pacific `Communications/telegram/` (not `~/.ollama/skills/coms/…`) |
| 2 | Process started from Pacific path; `ps` / status shows no legacy skills path |
| 3 | One inbound or outbound cycle succeeds (or status script reports healthy) |
| 4 | Inference calls resolve via Pacific `System/scripts/plumbing/run-infer.sh` (or equivalent single-flight) |
| 5 | No second getUpdates owner |

**Pass →** eligible to retire legacy telegram/relay executable (keep legacy `SKILL.md`).

### B. Security/Cameras

| Step | Pass criteria |
| --- | --- |
| 1 | Active jobs use `Security/Cameras/` paths (hourly wrapper, ensure, grab as scheduled) |
| 2 | One hourly or catchup cycle completes without path error |
| 3 | Cam server ensure (if enabled) starts from Pacific path |
| 4 | No active scheduler entry still on `~/.ollama/skills/a-eyes/…` |

**Pass →** eligible to retire corresponding legacy A-Eyes executables (keep `SKILL.md`).

### C. Energy actions (spot check)

| Step | Pass criteria |
| --- | --- |
| 1 | `ECOFLOW_ACTIONS` / action scripts resolve under Pacific `Energy/` |
| 2 | One read or action cycle OK; no legacy skills path in FAIL text |

Already marked LIVE in WO-SRV; this is confirmation only.

### D. Poller full cycle

| Step | Pass criteria |
| --- | --- |
| 1 | One full poller cycle completes |
| 2 | No path-related FAIL for domains already imported |
| 3 | Log path remains under Database (`…/Database/Logs/Automations/…`) |

---

## After all applicable rows pass

1. For each verified surface: retire **executable** legacy function only — **only with Alexander's explicit sign-off** (2026-09-29 rule; a PASS or "no live references" is not enough)  
2. Leave legacy `SKILL.md` in place  
3. Prefer `MIGRATED.md` on old packet over silent delete  
4. Record old → new in the Residual Path Retirement Table  
5. Only then move WO-SRV toward Complete

---

## Explicit non-goals

- Do not enable disabled Weather job during this checklist  
- Do not rotate Discord tokens here (WO-COM-002)  
- Do not invent parallel domain folders  

*Additive support doc for Bruce / operator. 2026-09-28 HST.*


## Status refresh — 2026-09-29

The checklist remains the runtime gate, but its earlier summary is stale. Current verified state is:

- **PASS / retired:** Security camera server + frame grab, System sampling, Reports worklog.
- **PASS / retired:** Network Globe runtime and Energy BLE owner runtime.
- **VERIFY PENDING:** Security timelapse and Energy actions.
- **VERIFY PENDING:** Telegram relay — operator has provisioned the required Telegram tokens; live relay/model verification remains outstanding.
- **VERIFY PENDING:** non-NPU plumbing and final Pacific poller acceptance while dependent failures remain.
- Canonical Database root for active Pacific source is `/home/rootrecord/RootRecord-Ecosystem/2 - RootRecord-Database`.
- The human `/home/rootrecord/RootRecord-Ecosystem/Pull.sh` workflow is intentionally retained and is **not** a failure condition.

The older line that described Energy actions as already LIVE is superseded by the current runtime evidence: **Energy action retirement verification is still pending.**

## Status refresh — 2026-09-29 ~01:37 HST

Supersedes the "PASS / retired" wording above: those surfaces are **PASS / G2 KEPT** — all tonight's G2 retirements were reverted (skills `1dcee66`).

**Standing rule (Alexander, 2026-09-29):** never retire or delete G2/legacy code. "No live references" is not grounds — unimported automations (e.g. the older repo `rootrecordsoftwaresolutions/old`) may need it. Retirement happens only with Alexander's explicit sign-off.

| Row | State | Evidence |
| --- | --- | --- |
| A. Telegram / council_relay | Login/polling **PASS**; replies **BLOCKED** (`*-telegram` models missing) | relay quoting fix `f27604d`; `2 - RootRecord-Database/Logs/Migration/g3-poller-realign-evidence-20260929T111731Z.md` |
| B. Security timelapse | VERIFY PENDING (window 05:00–19:00 HST) | — |
| C. Energy actions | read-only `solar-gate-status` PASS; actuating VERIFY PENDING; B1 0% needs physical check | — |
| D. Poller full cycle | Poller realign **PASS** (`d9f074b`); log now canonical `2 - RootRecord-Database/Logs/Automations/automations_current.log` (untracked, `eabe62e`) | `2 - RootRecord-Database/Logs/Migration/g3-poller-realign-evidence-20260929T111731Z.md` |
| Plumbing NPU/FLM | PASS | `2 - RootRecord-Database/Logs/Migration/g3-npu-flm-evidence-20260929T125429Z.md` |

**Open findings:**
1. Relay PID 821015 was started from the desk agent session (cgroup `app-grok-bot-*.scope`), not the poller unit; if it dies it only returns at the next poller start (boot job `council_relay`).
2. Poller stop takes 30 s and is SIGKILLed (TimeoutStopSec) on every restart/reload; an auto-pull stack reload (01:19 HST) also kills the relay because it lives in the poller cgroup.
3. `jobs.py` vs intake: re-checked — `jobs.py` only mentions intake in its header comment, already the canonical `2 - RootRecord-Database/Intake/`; relay state is canonical too. Old `/home/rootrecord/Database/intake/council-relay/` remains (historical). `jobs.py` not touched.
4. `Logs/Communications/council-relay.log` is 0 bytes because the relay's stdout is block-buffered (nohup to file); stderr errors would still appear.
5. `devices.conf` G2 `log_dir`/`state_dir`/`skill_root` — fixed in `58ee023` (see above).
6. Security timelapse check must wait for the 05:00–19:00 HST window.
7. B1 (River 2 Pro) reads 0% — needs a physical check.
8. FLM/NPU BLOCKED (no FLM binary/service).
9. Needs decision: `Energy/db/store.py` still defaults to old-root `ROOTRECORD/rootrecord.db` (no canonical copy); `push-repo-once.sh` still treats `~/.ollama/skills` pulls as runtime code (arms a stack reload).


## NPU installation update — 2026-09-29

- [x] AMD XDNA2/XRT prerequisite packages installed
- [x] `/dev/accel/accel0` present
- [x] `modinfo amdxdna` resolves installed driver/firmware entries
- [x] Reboot completed; in-tree `amdxdna` 0.7.0 loaded (DKMS build not needed)
- [x] FastFlowLM runtime installed (1.0.6) + `libxrt-utils` (`xrt-smi`)
- [x] `flm validate` passes
- [x] Approved NPU inference gate passes (02:52 HST, llama3.2:1b, 1.04 s, parallel refused) — `2 - RootRecord-Database/Logs/Migration/g3-npu-flm-evidence-20260929T125429Z.md`

**Current state:** prerequisite stack installed; NPU runtime is not yet VERIFIED. The installer reported a `BUILD_EXCLUSIVE` mismatch for kernel `7.0.0-34-generic` and requires post-reboot validation.

## Pre-reboot status — 2026-09-29 ~02:08 HST

| Row | State |
| --- | --- |
| Weather | **PASS** — Pacific daemon + venv, job enabled; reports **PASS** (01:59:13 HST); ≈ 3 GB/day, git-ignored |
| Telegram relay | login/polling PASS; retry fix `b3754fb` active after next relay start; replies BLOCKED (models) |
| NPU / FLM | **PASS** 02:52 HST (see NPU section) |

Post-reboot list: WO-SRV "Pre-reboot checkpoint 2026-09-29". Snapshot `2 - RootRecord-Database/Logs/Migration/g3-pre-reboot-checkpoint-20260929T120755Z.md`.

## Status refresh — 2026-09-29 ~03:45 HST

Supersedes open findings 1 (relay 821015 is gone; relay now runs under the poller unit), 8 (FLM/NPU now PASS) and 9 (`store.py` → canonical `RootRecord/`, `abc78b2`; G2 pulls no longer reload, `abc78b2`) in the ~01:37 block. Per-test records: [`Documentation/07-testing/`](../07-testing/README.md).

| Row | State | Evidence |
| --- | --- | --- |
| A. Telegram / council_relay | login/polling PASS; replies BLOCKED (models); quiet mode default (`RR_RELAY_REPLIES=0`) | `ebc32a7`; WO-SRV |
| B. Security timelapse | VERIFY PENDING (after 05:00 HST) | — |
| C. Energy actions | read-only PASS; arm/disarm + AC VERIFY PENDING (need approval); data freshness PASS via `Energy/.venv`; B1/B2 low, B1 physical check | [EcoFlow record](../07-testing/2026-09-29-ecoflow-stale-data-energy-venv.md) |
| D. Poller full cycle | PASS on the new root with Title-case folders; log `2 - RootRecord-Database/Logs/Automations/automations_current.log` | [realign](../07-testing/2026-09-29-poller-database-root-realign.md), [rename](../07-testing/2026-09-29-database-titlecase-rename.md) |
| Plumbing NPU/FLM | PASS (install/validate); on-demand `llama3.2:1b` route PASS; own-session fix VERIFY PENDING | [NPU](../07-testing/2026-09-29-npu-flm-install-validate.md), [1b on demand](../07-testing/2026-09-29-npu-llama3.2-1b-on-demand.md) |
| Resident-model safety | OOM FAIL → fixed; fix PASS (non-resident warmup, keepalive 0) | [OOM record](../07-testing/2026-09-29-oom-flm-warmup-resident.md) |
| G2 legacy | KEPT (retire only with Alexander sign-off) | skills `1dcee66` |

**Preconditions for any re-run (current state):**
- **Database root:** `/home/rootrecord/RootRecord-Ecosystem/2 - RootRecord-Database` with Title-case top-level folders `Energy/`, `System/`, `Weather/`, `Github/`, `RootRecord/`, `Worklog/`, `Intake/` (plus `AI/`, `Archive/`, `Logs/`, `Geology/`, `Media/`, `Users/`). Upper-case `ENERGY/`, `SYSTEM/`, `WEATHER/`, `GITHUB/`, `ROOTRECORD/`, `WORKLOG/` and lower-case `intake/` under the new root are historical names (Database `92bd69c`). The old root `/home/rootrecord/Database/` is **not** a data path any more: it holds only `GITHUB/` (backups, flags, worktrees) and `README.md`; the old data is archived in `2 - RootRecord-Database/Archive/Previous-Datasets/G2-old-root-20260929/`.
- **NPU inference:** `llama3.2:1b` **on demand**. `System/scripts/plumbing/run-infer.sh` starts `flm serve` (via `setsid nice -n 10`, `--pmode balanced`, `--ctx-len ${FLM_CTX_LEN:-4096}`, port 52625) only for a request and stops it on exit; `FLM_ON_DEMAND=0` disables this. An idle desk therefore shows **no** FLM process and a closed :52625 — that is expected, not a failure. `llama3.2:3b` is installed but not the default.
- **No resident models:** the FLM warmup is non-resident unless `FLM_WARMUP_RESIDENT=1` (Pacific `ff298b2`, after the 03:10–03:13 HST OOM loop). Ollama CLI calls use `--keepalive ${OLLAMA_KEEP_ALIVE:-0}` (`3039c3f`). `OLLAMA_KEEP_ALIVE=0` in `ollama.service` is still open (needs sudo).
- **Relay quiet mode is the default:** `ensure-relay.sh` exports `RR_RELAY_REPLIES=${RR_RELAY_REPLIES:-0}` (Pacific `ebc32a7`). Caveat: in quiet mode incoming Telegram messages are consumed (marked read) and **will not be answered later**. Replies also stay BLOCKED until the `*-telegram` models exist and Alexander opts in (`RR_RELAY_REPLIES=1`).
- **Required venvs (git-ignored):** `Pacific/Energy/.venv` (without it `ecdsa`/eflib are missing and readings fall back to frozen cloud values) and `Pacific/Weather/.venv` (from `Weather/requirements.txt`).
- Weather and relay start only at poller boot (ON_BOOT); a mid-session crash is not re-ensured until the next poller start.

## Geology + old-repo ports — 2026-09-29 ~13:40 HST

| Row | Pacific path | Gate (read at poller start) | Manual test | State |
| --- | --- | --- | --- | --- |
| USGS earthquakes (Hawaiʻi bbox + global M2.5) + HVO Kīlauea / Mauna Loa status, notices | `Geology/scripts/geology_collect.py` → Database `Geology/{Earthquakes,Volcanoes}/` | `geology_collect` 300 s, `RR_GEOLOGY=1` | 13:19 HST rc 0, 2.64 s, 28 MB | **PASS** (manual) · poller cycle **VERIFY PENDING** |
| Kīlauea cams stills | `Geology/scripts/kilauea_cams.py` → `Geology/Volcanoes/Cams/` | `geology_kilauea_cams` 600 s, `RR_KILAUEA_CAMS=1` | 13:24 3 × 200, re-run 304 | **PASS** (manual) · cycle **VERIFY PENDING** |
| Quake backfill (SQLite) | `Geology/scripts/earthquakes_backfill.py` | on demand | `--days 1` 11 rows | **PASS** |
| Earthquake voice report | `Media/Voice/scripts/voice_reports.py earthquake_report` | `voice_earthquake_report` :08, `RR_VOICE_QUAKE=1` | text 2 runs | **PASS** (text) · WAV **VERIFY PENDING** |
| Sun times | `Energy/scripts/sun_times.py` → `Energy/sun/` | `energy_sun_times` hourly, `RR_SUN_TIMES=1` | 06:11 / 18:10 | **PASS** (manual) |
| Uptime log | `System/scripts/uptime_log.py` → `System/uptime/` | `system_uptime_log` 60 s, `RR_UPTIME_LOG=1` | tick + gap sim | **PASS** (manual) |
| MP4 converter | `Media/Video/scripts/mp4_converter.py` | on demand | 2 s synthetic | **PASS** |

Close the "VERIFY PENDING" cells only after the next poller start with the flag set (Alexander's sign-off): check `Geology/collector-last.json` `at` advances every ~5 min and the poller log shows the job rc 0. Records: [geology](../07-testing/2026-09-29-geology-earthquakes-hvo-collector.md), [batch 1](../07-testing/2026-09-29-old-repo-ports-batch1.md); [migration matrix](./Old-Repo-Migration-Matrix.md); evidence `2 - RootRecord-Database/Logs/Migration/migration-geology-evidence-20260929T2319Z.md`.

Addendum ~13:46 HST: `voice_reports.py hurricane_desk` (`RR_VOICE_HURRICANE`) and `kilauea_report` (`RR_VOICE_KILAUEA`) — text **PASS**, WAV **VERIFY PENDING** ([record](../07-testing/2026-09-29-voice-reports-batch3-hurricane-kilauea.md)). The jobs.py registrations for all rows in this section are a **sign-off item** (standing rule: jobs.py only on Alexander's request or a WO); blocks in `2 - RootRecord-Database/Logs/Migration/migration-jobs-py-additions-20260929.md`.

Addendum ~14:10 HST (breadth batch 4, [record](../07-testing/2026-09-29-old-repo-ports-breadth-batch4.md)): `web_facts.py` + `live_wx.py` on demand **PASS**; `host_desks.py` net + security **PASS** (temp root); `voice_reports.py solar_desk` / `security_desk` / `bandwidth_desk` text **PASS**, WAV **VERIFY PENDING**; `hawaii_news.py` rc 0 but **FAIL on content** (0 posts). Their jobs are **PROPOSED only** (not in jobs.py): [Pending-Job-Registrations-2026-09-29.md](./Pending-Job-Registrations-2026-09-29.md). After registration + next poller start: check `System/network/net-last.json` advances every ~5 min and each voice `_current.md` appears at :04 / :11 / :12.

Addendum ~14:40 HST (breadth batch 5, [record](../07-testing/2026-09-29-old-repo-ports-breadth-batch5.md)): voice text fixes (clock "oh N", watts words, spoken sun times) **PASS**; `hawaii_news.py` with 16 seed feeds **PASS** (278 posts, temp root); `official_statement.py` (HLS) **PASS** (one real run, git-ignored path); `voice_reports.py official_weather` / `boot_brief` text **PASS**, WAV **VERIFY PENDING**; `report_board.py` **PASS** (temp root); `load_categories.py`, `global_board.py` (temp root), `host_hw.py`, `speech_scrub.py` **PASS**. New jobs **PROPOSED, not in jobs.py**: `weather_official_hls` (`RR_OFFICIAL_HLS`), `voice_official_weather` (`RR_VOICE_OFFICIAL`), `voice_boot_brief` (`RR_VOICE_BOOT`, ON_BOOT), `reports_board_catchup` (`RR_REPORT_BOARD`), `weather_hurricane_global` (`RR_HURRICANE_GLOBAL`). Correction: the weather poller already collects HWO; only HLS was missing.

## Status at pause — 2026-09-29 16:25 HST

Rows B–D: no new runtime evidence since the ~03:45 block, so those states stand. New rows from today's afternoon work (docs-only refresh):

| Row | State | Evidence |
| --- | --- | --- |
| A. Telegram / council_relay (desk) | quiet mode default; replies OFF until Alexander opts in (`*-telegram` models rebuilt 04:12, see the worklog g3-specialists pass) | worklog |
| A2. AWS `telegram_hold` / `basic_replies` | OFF (sign-off) | [fallback proposal](../08-ideas/2026-09-29-aws-fallback-rebuild.md) |
| AWS Hawaii feed trim + `*/15` cron | **PASS** | [record](../07-testing/2026-09-29-aws-hawaii-trim-and-cloudflared.md) |
| AWS tunnel / `www` 200 | **PASS** | same record |
| AWS globe static allowlist (P0) | **PASS** | [record](../07-testing/2026-09-29-aws-globe-static-allowlist.md) |
| Globe overlay v2 + AWS Ohio node | LANDED · real-browser check **VERIFY PENDING** | [record](../07-testing/2026-09-29-globe-overlay-aws-deploy.md) |
| AWS fallback Phase 2 (trimmed-micro) | **PASS** (deploy, rollback, write round-trip) · real fallback **VERIFY PENDING** · relay send **VERIFY PENDING** | [record](../07-testing/2026-09-29-aws-fallback-phase2-runtime-deploy.md) |
| Root Monitor toggle buttons + camera button | **PASS** | [record](../07-testing/2026-09-29-root-monitor-toggle-buttons.md) |
| Geology / old-repo port rows above | unchanged: manual PASS; poller cycle VERIFY PENDING (flags + poller restart are sign-off items) | — |

Sign-offs: worklog section "State at pause, 16:25 HST".

## Status refresh — 2026-09-30 02:35 HST

| Row | State | Evidence |
| --- | --- | --- |
| Root Monitor login window | **LANDED** 02:33 HST. Terminal autostart saved. Conky not started. | `Packaging/swap-default-viewer.sh apply` |
| Not migrated list | 16 open (7 BLOCKED, 9 VERIFY PENDING). Seven closed work orders removed from the panel list. | `Apps/Control-Panel/Lib/rr_migration.json` |
| Weather poller | Recycled 02:24:58 HST. Reports regenerated 02:34. `noaa_homepage` still FAILED (bot-check) at 02:33. | `2 - RootRecord-Database/Weather/Hawai'i/logs/weather-poller.log` |
| Geology / voice jobs | Still gated. Do not enable from this refresh. | jobs.py `RR_*` defaults |
| Local website | Removed. Do not recreate `3 - RootRecord-Website` or bind port 3001. | operator list |
| G2 identical skills copies | Removed where the hash matched Pacific. Unique files and the 27 GB old-skills tree stayed. | skills `6483586` (02:16 HST) |
| B. Timelapse / C. Energy actuation / A. Telegram replies | Unchanged at 02:35: still waiting on Alexander | operator list |

## Status refresh — 2026-09-30 afternoon

Supersedes the NPU-default and "replies off" bullets in the 2026-09-29 preconditions, and the 02:35 "Telegram replies" cell, for the council path only. Older rows stay as the record of that morning.

| Row | State | Evidence |
| --- | --- | --- |
| Council inference | NPU `llama3.2:3b`, context 4096, on demand, `RR_NPU_ONLY=1`. Non-council callers and `flm-warmup.sh` still default to `llama3.2:1b`. | `ensure-relay.sh`, `jobs.py` header |
| Sandbox replies | On (`SANDBOX_REPLIES=1`). Live council and private DMs stay quiet. | `relay.conf` |
| Desk | `Intake/desk-live.txt` refreshed before each reply. | `desk-live.py` |
| Canonical state | `System/status/rootrecord-state.json` plus agent/public/slice projections. Not auto-committed. | `state-aggregate.py`, Decisions/0005 |
| Execution | Broker answers reads and refuses restarts and agent builds. `cursor_api` ships off. Poller `service_supervisor` still recovers weather and the relay. | `Automations/execution/`, WO-SRV-RELAY, Decision 0006 |
| Continuity | `Documentation/01-operations/HANDOFF.md`. Desk check: `bash verify.sh` from the ecosystem root. | HANDOFF |
