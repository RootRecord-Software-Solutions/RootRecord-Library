# WO-ECO-001 — Action Plan (Phase 1: EcoFlow Live Read)

| Field | Value |
|-------|--------|
| **Parent WO** | [WO-ECO-001](../WO-ECO-001-Energy-Domain-Import.md) |
| **Phase** | 1 of N |
| **Status** | **COMPLETE** — signed off 2026-09-29 ~21:30 HST (live reads) and archived 21:41 HST. Phase 2 stays on the parent order. |
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

## Re-verification — 2026-09-29 ~21:30 HST

Alexander sign-off for Phase 1 reads only. Tested on the live desk:

- Poller PID 105444, Pacific `rootserver_poller.py`, up since 03:13 HST.
- `delta2-last.json` age about 5 min, `soc` 7.0, `source` api.
- `river2pro-last.json` age about 2 min, `soc` 100.0, `source` api.
- Jobs call `Energy/` directly. The old `energy` → `Energy` symlink is absent and is not required by current `jobs.py`.

Phase 2 (actuating actions, hybrid reports) stays open on the parent work order. This phase plan is archived because its own acceptance list is met.

## Next

**WO-SRV** — System domain (sys-stats) import. Parent phase 2 remains open.
