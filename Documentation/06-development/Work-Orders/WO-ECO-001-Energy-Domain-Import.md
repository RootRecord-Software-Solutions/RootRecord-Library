# WO-ECO-001 — Energy Domain Import (EcoFlow + Hybrid Reports)

| Field | Value |
|-------|--------|
| **Priority** | P0 |
| **Status** | **Phase 1 desk fill done** — org scripts + jobs rewire + desk lib/db/config fill 2026-09-28; stack reload + soak pending |
| **Target repo** | `RootRecord-Software-Solutions/RootRecord-Pacific-Solar-Server` (`Energy/`) |
| **Action plan** | [WO-ECO-001-Action-Plan.md](WO-ECO-001-Action-Plan.md) |

## Phase 1 commits (org Pacific)

- Energy read scripts under `Energy/scripts/read/`
- Partial `Energy/lib/` + jobs.py rewire to Ecosystem Energy paths
- `ENERGY_EFLIB_PATH` → live G2 vendor for BLE (until soak / vendor policy)

## Desk log (2026-09-28 HST)

1. [x] `git pull` on Ecosystem Pacific — already up to date
2. [x] `Energy/lib`, `Energy/db`, `Energy/config` filled from G2 (`cp -an`)
3. [ ] Stack reload (`Automations/scripts/stack/schedule-stack-reload.sh`)
4. [ ] Watch SUMMARY / ENERGY lines ≥15 min
5. [ ] Do not delete G2 skill tree until soak OK

## Phase 2+

actions/, hybrid reports, Core-Ops single-writer policy.
