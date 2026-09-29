# G3 Runtime Verification Checklist

| Field | Value |
| --- | --- |
| **Date** | 2026-09-28 (HST) |
| **Authority** | Supports WO-SRV-2026-09-27 |
| **Rule** | Docs only. Bruce (or operator with shell) runs this. No retirement until each row passes. |

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

1. For each verified surface: retire **executable** legacy function only  
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
