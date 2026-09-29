# Work Orders

Active implementation and migration work for RootRecord. Use the template at `Documentation/01-operations/templates/TEMPLATE Work Order.md` for new items.

---

## Active backlog (updated 2026-09-28 ~16:15 HST)

| ID | Title | Status |
| --- | --- | --- |
| [WO-ECO-2026-09-27](./Ecosystem_Migration_Work_Order_WO-ECO-2026-09-27.md) | Ecosystem migration & repository foundation | **IN PROGRESS** — Pacific under `1 - Servers`; Energy Phase 1 desk fill done |
| [WO-SRV-2026-09-27](./Servers_Cutover_Work_Order_WO-SRV-2026-09-27.md) | Pacific runtime path cutover (G2 skills → G3 Servers) | **IN PROGRESS** — Energy desk fill done; residual non-Energy paths remain |
| [WO-MAP-2026-09-27](./MasterPrompt_RepoMap_Work_Order_WO-MAP-2026-09-27.md) | Master-Prompt repository ownership map | OPEN — Pacific name known |
| [WO-OLD-2026-09-28](./Old_Server_Selective_Recovery_Work_Order_WO-OLD-2026-09-28.md) | Selective recovery from Solar-Pacific-…-Old (G1) | OPEN — **blocked on G2→G3** |
| [WO-GH-2026-09-27](./GitHub_Catalog_Hygiene_Work_Order_WO-GH-2026-09-27.md) | GitHub catalog hygiene & non-canonical cleanup | OPEN |
| [WO-DATA-2026-09-27](./Database_Boundary_Work_Order_WO-DATA-2026-09-27.md) | Database boundary & publication policy | OPEN |
| [WO-AGENT-2026-09-27](./AgentContext_CanonicalHome_Work_Order_WO-AGENT-2026-09-27.md) | Agent context canonical home | OPEN |
| [WO-CF-2026-09-27](./Cloudflare_Tunnel_Recovery_Work_Order_WO-CF-2026-09-27.md) | Cloudflare tunnel credential recovery | OPEN |
| [WO-ARCH-2026-09-27](./Ops_Weekly_Archive_Work_Order_WO-ARCH-2026-09-27.md) | Weekly operations log archive | OPEN |
| [WO-AEYES-2026-09-27](./A-EYES_Work_Order_WO-AEYES-2026-09-27.md) | A-EYES capture rate & timelapse optimization | OPEN |

**Related (hyphen set):** [WO-ECO-001](../Work-Orders/WO-ECO-001-Energy-Domain-Import.md) Phase 1 desk fill **done**; stack reload + soak still operator.

---

## Suggested attack order

1. **WO-ECO-001 / WO-SRV** — complete Energy soak; then clear residual Energy rows; next domain import.
2. **WO-CF** — token + tunnel verify after rebuilds.
3. **WO-GH** — `repos.conf` → Ecosystem path.
4. **WO-MAP** — short ownership contract in Master-Prompt.
5. **WO-OLD** — only after matching G2 domains are in G3; packet-by-packet from Old archive.
6. **WO-AGENT** / **WO-DATA** / **WO-ARCH** / **WO-AEYES** as parallelizable.
7. **WO-ECO** — close when foundation settles.

Architecture maps:

- `Documentation/00-architecture/Migration-Lineage-Three-Generations-2026-09-28.md`
- `Documentation/00-architecture/Solar-Pacific-Old-Inventory-Map-2026-09-28.md`
- `Documentation/00-architecture/Pacific-Domain-Import-Playbook-2026-09-28.md`

---

## Rules

- One WO per coherent outcome; link related IDs.
- Keep **Status** accurate (`OPEN`, `IN PROGRESS`, `BLOCKED`, `CLOSED`).
- Closed WOs: weekly archive under `Documentation/06-development/archive/YYYY-Www/`.
- No secrets in WO text.
- **Never bulk-merge G1 `origin/` into G3 runtime.**
- Canonical Work Orders directory is `Work Orders/` (space). Hyphenated `Work-Orders/` is transitional for proposal IDs.
