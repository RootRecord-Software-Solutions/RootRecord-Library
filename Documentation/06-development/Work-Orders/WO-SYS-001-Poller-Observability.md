# WO-SYS-001 — Poller Observability & FAIL Handling

| Field | Value |
|-------|--------|
| **Priority** | P2 |
| **Status** | Draft |
| **Target** | Pacific Automations + Logs; optional Communications notify |
| **Depends on** | Live poller stable; WO-COM-001 if alerts desired |
| **Related** | Live log sample 2026-09-28 (`ecoflow_read_cycle FAIL code=-15`) |

## Goal

Make poller health easy to read at a glance and define what happens on repeated job FAIL without spamming the operator.

## Observed signal (from operator live window)

- SUMMARY lines for river2pro / delta2 (BLE + API)
- SYSTEM samples written under Database/SYSTEM/samples
- ENERGY status live from sqlite
- worklog_scan OK
- Occasional `ecoflow_read_cycle FAIL code=-15`

## Scope (in)

- Document FAIL code meanings when known (or mark unknown for operator to fill)
- Propose thresholds: e.g. N consecutive FAILs → log escalate; optional Telegram only after WO-COM-001
- Confirm log path authority (`rootserver-poller.log` vs Library Logs domain)
- Optional: daily one-line health rollup in WORKLOG
- System domain README: what the poller banner fields mean (public URL, local URL, systemd, jobs path)

## Scope (out)

- Rewriting the poller engine
- Metrics backends (Prometheus etc.) unless operator requests
- Auto-restart loops that fight systemd

## Acceptance criteria

1. Short operator guide: “how to read the poller window”
2. FAIL policy written (ignore / log / notify)
3. No new secret storage
4. Does not require Energy import to complete (can land anytime)

## Suggested deliverables

- `System/README.md` or Automations section: banner + log legend
- Optional snippet in worklog_scan output for last FAIL summary

## Risks

- Over-alerting on transient BLE `-15`
- Treating sqlite ENERGY status as substitute for live BLE without labeling source

## Notes

Can run in parallel with WO-ECO-001. Useful while Energy source is still pending.
