# WO-ECO-001 — Energy Domain Import (EcoFlow + Hybrid Reports)

| Field | Value |
|-------|--------|
| **Priority** | P0 |
| **Status** | **Pacific poller + Energy job paths live** — fill `Energy/lib/read_runner.py` from G2; then soak; no old desk |
| **Target repo** | `RootRecord-Software-Solutions/RootRecord-Pacific-Solar-Server` (`Energy/`) |
| **Action plan** | [WO-ECO-001-Action-Plan.md](WO-ECO-001-Action-Plan.md) |

## Done

- Energy read scripts on org Pacific
- jobs.py EcoFlow commands → Ecosystem Energy (quoted paths)
- systemd `rr-rootserver-poller` → Pacific `run-poller.sh`
- Tunnel READY; ENERGY heartbeat from Database

## Operator next

1. `cp -an` G2 `energy/lib` (must include `read_runner.py`) → Pacific `Energy/lib`
2. Manual `delta2-read.sh` until exit 0
3. `systemctl --user restart rr-rootserver-poller.service`
4. Confirm SUMMARY / no structural cycle FAIL ≥15 min
5. Do not use G2 as poller host; archive G2 energy after soak

## Phase 2+

actions/, hybrid reports, Core-Ops single-writer policy.
