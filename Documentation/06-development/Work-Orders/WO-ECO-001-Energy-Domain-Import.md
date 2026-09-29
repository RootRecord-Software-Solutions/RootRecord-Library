# WO-ECO-001 — Energy Domain Import (EcoFlow + Hybrid Reports)

| Field | Value |
|-------|--------|
| **Priority** | P0 |
| **Status** | **Phase 1 on org Pacific** — read scripts + jobs rewire pushed 2026-09-28 |
| **Target repo** | `RootRecord-Software-Solutions/RootRecord-Pacific-Solar-Server` (`Energy/`) |
| **Action plan** | [WO-ECO-001-Action-Plan.md](WO-ECO-001-Action-Plan.md) |

## Phase 1 commits (org Pacific)

- Energy read scripts under `Energy/scripts/read/`
- Partial `Energy/lib/` + jobs.py rewire to Ecosystem Energy paths
- `ENERGY_EFLIB_PATH` → live G2 vendor for BLE

## Operator next (desk)

1. `git pull` on Ecosystem Pacific checkout (org remote)
2. Ensure `Energy/lib/read_runner.py`, `ble_client.py`, `ecoflow_api.py`, `db/`, `config/devices.conf` exist — copy from `~/.ollama/skills/energy/` if still missing after pull
3. Stack reload
4. Watch SUMMARY / ENERGY lines ≥15 min
5. Do not delete G2 skill tree until soak OK

## Phase 2+

actions/, hybrid reports, Core-Ops single-writer policy.
