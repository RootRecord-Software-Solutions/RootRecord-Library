# WO-ECO-001 — Action Plan (Phase 1: EcoFlow Live Read)

| Field | Value |
|-------|--------|
| **Parent WO** | [WO-ECO-001](WO-ECO-001-Energy-Domain-Import.md) |
| **Phase** | 1 of N — live BLE/API read only |
| **Status** | **COMPLETE (Phase 1 LIVE)** — 2026-09-28 ~16:37 HST |
| **Target repo** | `RootRecord-Software-Solutions/RootRecord-Pacific-Solar-Server` |
| **Updated** | 2026-09-28 ~16:38 HST |

## Acceptance (met)

- [x] Read scripts on Pacific
- [x] jobs.py Energy on Pacific (quoted)
- [x] systemd poller on Pacific
- [x] `read_runner.py` + lib on desk Energy/
- [x] `ln -sfn Energy energy` at Pacific root
- [x] `lib/py` PYTHONPATH = vendor + Pacific parent
- [x] SUMMARY=delta2 and SUMMARY=river2pro in automations log

## Evidence

```text
SUMMARY=delta2 soc=39% solar=31W ac_out=65W usbc=55W src=api db=ok
SUMMARY=river2pro soc=100% solar=0W ac_out=46W usbc=0W src=api charge=battery_transfer db=ok
ENERGY status=live … src=sqlite
```

## Standing

- No old desk for Energy reads
- Symlink `energy` → `Energy` required on each checkout
- Phase 2: actions/, hybrid, commit lib to org, archive G2 energy

## Next (WO-SRV)

Import System (sys-stats) off `~/.ollama/skills`.
