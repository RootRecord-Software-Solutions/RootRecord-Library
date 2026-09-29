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
3. `jobs.py` vs intake: re-checked — `jobs.py` only mentions intake in its header comment, already the canonical `2 - RootRecord-Database/intake/`; relay state is canonical too. Old `/home/rootrecord/Database/intake/council-relay/` remains (historical). `jobs.py` not touched.
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
