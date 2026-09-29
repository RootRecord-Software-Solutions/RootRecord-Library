# WO-ECO-001 — Energy Domain Import (EcoFlow + Hybrid Reports)

| Field | Value |
|-------|--------|
| **Priority** | P0 |
| **Status** | **Phase 1 LIVE** — Pacific reads OK (SUMMARY delta2 + river2pro 2026-09-28 ~16:37 HST) |
| **Target repo** | `RootRecord-Software-Solutions/RootRecord-Pacific-Solar-Server` (`Energy/`) |
| **Action plan** | [WO-ECO-001-Action-Plan.md](WO-ECO-001-Action-Plan.md) |

## Done (Phase 1)

- [x] Read scripts on Pacific
- [x] jobs.py EcoFlow commands on Pacific (quoted paths)
- [x] systemd poller on Pacific
- [x] Energy lib fill (`read_runner`, ble, api, db)
- [x] `energy` → `Energy` symlink + `lib/py` PYTHONPATH (Pacific root)
- [x] Manual + scheduled SUMMARY lines (api/db)

## Standing desk note

```bash
ln -sfn Energy energy   # at Pacific repo root (import energy.*)
```

## Phase 2+

actions/, hybrid reports, Core-Ops single-writer, commit non-secret lib to org git, archive G2 energy runtime use.

## Next migration (WO-SRV)

System (sys-stats) → then Github → Telegram → A-Eyes → Weather. Zero `~/.ollama/skills` in jobs.py.
