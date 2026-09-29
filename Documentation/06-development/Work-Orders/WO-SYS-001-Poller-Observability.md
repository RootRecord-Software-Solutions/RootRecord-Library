# WO-SYS-001 — Poller Observability & FAIL Handling

| Field | Value |
|-------|--------|
| **Priority** | P2 |
| **Status** | **Log path slice complete** (2026-09-28); FAIL policy still draft |
| **Target** | Pacific Automations + Logs; optional Communications notify |
| **Depends on** | Live poller stable; WO-COM-001 if alerts desired |
| **Related** | Live log sample 2026-09-28 (`ecoflow_read_cycle FAIL code=-15`) |

## Goal

Make poller health easy to read at a glance and define what happens on repeated job FAIL without spamming the operator.

## Log storage cutover (done)

| Stream | Old default (G2 residual) | New default |
|--------|---------------------------|-------------|
| Poller | `~/.ollama/skills/logs/store/rootserver-poller.log` | `/home/rootrecord/Database/LOGS/Automations/rootserver-poller.log` |
| Stack reload | `~/.ollama/skills/logs/store/stack-reload.log` | `/home/rootrecord/Database/LOGS/Automations/stack-reload.log` |

Updated on **org** `RootRecord-Pacific-Solar-Server`: poller-watch, open-poller-window, run-poller, do-stack-reload, schedule-stack-reload. Contracts in `Logs/README.md` + `Logs/Automations/README.md`.

**Operator still must:** `mkdir` Database path, optional `cp -an` old log, align **systemd unit** if it hardcodes the old path, pull + stack reload.

## Observed signal (from operator live window)

- SUMMARY lines for river2pro / delta2 (BLE + API)
- SYSTEM samples under Database/SYSTEM/samples
- ENERGY status live from sqlite
- worklog_scan OK
- Occasional `ecoflow_read_cycle FAIL code=-15`

## Remaining scope

- Document FAIL code meanings when known
- Thresholds: N consecutive FAILs → log escalate; optional Telegram after WO-COM-001
- Operator guide: “how to read the poller window”
- Optional daily one-line health rollup in WORKLOG

## Scope (out)

- Rewriting the poller engine
- Metrics backends unless operator requests
- Auto-restart loops that fight systemd

## Acceptance criteria

1. [x] Canonical log paths under Database + code defaults updated
2. [ ] Short operator guide: “how to read the poller window”
3. [ ] FAIL policy written (ignore / log / notify)
4. [ ] Desk unit aligned + window shows new path

## Notes

Path cutover can land without Energy Phase 1 completion. FAIL policy can follow after desk confirms the new log path is live.
