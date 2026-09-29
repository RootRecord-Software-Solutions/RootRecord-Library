# Work Orders — Index

Draft proposals for improvements and website development. Status: **proposal only** until operator accepts and supplies sources/approvals — except **WO-ECO-001 Phase 1**, which is already executing on org Pacific.

**Canonical home:** `RootRecord-Software-Solutions` org (not personal account).

## Active proposals

| ID | Title | Priority | Status | File |
|----|-------|----------|--------|------|
| **WO-ECO-001** | Energy domain import (EcoFlow + hybrid reports) | **P0** | Phase 1 on **org** Pacific (scripts + jobs rewire) | [WO](WO-ECO-001-Energy-Domain-Import.md) · [**Action Plan**](WO-ECO-001-Action-Plan.md) |
| **WO-SRV-001** | Residual jobs path rewire | **P0** | Blocked on Energy (+ later domains) | [WO-SRV-001](WO-SRV-001-Residual-Jobs-Path-Rewire.md) |
| **WO-WEB-001** | Public status / solar board alignment | **P1** | Draft | [WO-WEB-001](WO-WEB-001-Public-Status-Solar-Board.md) |
| **WO-COM-001** | Communications surface (tunnel, Telegram, network) | **P1** | Draft | [WO-COM-001](WO-COM-001-Communications-Surface.md) |
| **WO-WXG-001** | Weather + Geology domain import | **P1** | Draft — after Energy | [WO-WXG-001](WO-WXG-001-Weather-Geology-Import.md) |
| **WO-SYS-001** | Poller observability & FAIL handling | **P2** | Draft (can parallel Energy) | [WO-SYS-001](WO-SYS-001-Poller-Observability.md) |
| **WO-WEB-002** | RootRecord public site foundation pass | **P2** | Draft | [WO-WEB-002](WO-WEB-002-Public-Site-Foundation.md) |
| **WO-GH-001** | GitHub pull authority & timer policy | **P2** | Draft | [WO-GH-001](WO-GH-001-Github-Pull-Authority.md) |

## Recommended order

1. **WO-ECO-001 Phase 1** — desk pull + lib fill + stack reload (see Action Plan)
2. **WO-SRV-001** (Energy slice) — residual cleanup after rewire
3. **WO-COM-001** — policy + README; optional Telegram later
4. **WO-WEB-001** — status contract (can draft in parallel with Energy)
5. **WO-SYS-001** — FAIL policy / how to read the poller window (parallel OK)
6. **WO-WXG-001** — Weather then Geology
7. **WO-GH-001** — pull timer authority (prefer Core-Processor until Pacific stabilizes)
8. **WO-WEB-002** — public site foundation after status truth exists

## Architecture context

- `Documentation/00-architecture/` (org Library)
- Pacific: `RootRecord-Software-Solutions/RootRecord-Pacific-Solar-Server`

## Rules

- **No code import** without operator source tree
- **One domain at a time**
- **Document only** until a WO is explicitly accepted for execution
- Preserve historical paths in notes when retiring residuals
