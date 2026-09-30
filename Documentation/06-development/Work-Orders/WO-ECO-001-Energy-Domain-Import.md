# WO-ECO-001 — Energy Domain Import (EcoFlow + Hybrid Reports)

| Field | Value |
|-------|--------|
| **Priority** | P0 |
| **Status** | **IN PROGRESS** — Phase 1 reads signed off and archived 2026-09-29 ~21:41 HST. Phase 2 actuating actions remain open. |
| **Target repo** | `RootRecord-Software-Solutions/RootRecord-Pacific-Solar-Server` (`Energy/`) |
| **Action plan** | [WO-ECO-001-Action-Plan.md](Complete/WO-ECO-001-Action-Plan.md) |

## Phase 1 — done

- [x] Read scripts on Pacific org git
- [x] jobs.py EcoFlow commands on Pacific (quoted paths)
- [x] systemd poller on Pacific only
- [x] Energy lib fill (`read_runner`, ble, api, db, config)
- [x] `energy` → `Energy` symlink + `lib/py` PYTHONPATH
- [x] Manual SUMMARY + scheduled alternating SUMMARY in poller window
- [x] ENERGY status=live from Database

## Evidence (operator window)

```text
SUMMARY=delta2 soc=39% solar=35W ac_out=… src=api db=ok
SUMMARY=river2pro soc=100% … src=api charge=battery_transfer db=ok
ENERGY  status=live  B2=41.1%  B1=98.9%  …
```

## Standing

```bash
ln -sfn Energy energy   # Pacific repo root, every checkout
```

## Phase 2+

actions/, hybrid reports, Core-Ops single-writer, optional commit of non-secret lib to org, archive G2 energy runtime.

## Next ecosystem step

**WO-SRV** → import **System** (sys-stats) off `~/.ollama/skills`.
