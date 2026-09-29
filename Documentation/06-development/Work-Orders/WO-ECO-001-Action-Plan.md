# WO-ECO-001 — Action Plan (Phase 1: EcoFlow Live Read)

| Field | Value |
|-------|--------|
| **Parent WO** | [WO-ECO-001](WO-ECO-001-Energy-Domain-Import.md) |
| **Phase** | 1 of N |
| **Status** | **COMPLETE (LIVE + soak)** — 2026-09-28 ~16:40 HST |
| **Target repo** | `RootRecord-Software-Solutions/RootRecord-Pacific-Solar-Server` |

## Acceptance (all met)

- [x] Read scripts on Pacific
- [x] jobs.py Energy on Pacific (quoted)
- [x] systemd poller on Pacific
- [x] `read_runner.py` + lib on desk Energy/
- [x] `ln -sfn Energy energy` at Pacific root
- [x] `lib/py` PYTHONPATH = vendor + Pacific parent
- [x] SUMMARY loop in automations log / poller window (≥1 min continuous)

## Soak evidence

```text
16:39:27  SUMMARY=river2pro … src=api db=ok
16:39:44  SUMMARY=delta2 … src=api db=ok
16:39:58  ENERGY status=live …
16:40:13  SUMMARY=delta2 …
16:40:29  SUMMARY=river2pro …
16:40:44  SUMMARY=delta2 …
```

## Standing ops

- No old desk for Energy reads
- Symlink `energy` → `Energy` on each checkout
- Phase 2: actions/, hybrid, org lib commit optional

## Next

**WO-SRV** — System domain (sys-stats) import.
