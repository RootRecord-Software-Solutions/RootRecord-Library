# Work Orders

Active implementation and migration work for RootRecord. Use the template at `Documentation/01-operations/templates/TEMPLATE Work Order.md` for new items.

---

## Active backlog (2026-09-27)

| ID | Title | Status |
| --- | --- | --- |
| [WO-ECO-2026-09-27](./Ecosystem_Migration_Work_Order_WO-ECO-2026-09-27.md) | Ecosystem migration & repository foundation | OPEN |
| [WO-MAP-2026-09-27](./MasterPrompt_RepoMap_Work_Order_WO-MAP-2026-09-27.md) | Master-Prompt repository ownership map | OPEN — blocked on repo name list |
| [WO-SRV-2026-09-27](./Servers_Cutover_Work_Order_WO-SRV-2026-09-27.md) | Pacific runtime path cutover (`skills` → `1 - Servers`) | OPEN |
| [WO-GH-2026-09-27](./GitHub_Catalog_Hygiene_Work_Order_WO-GH-2026-09-27.md) | GitHub catalog hygiene & non-canonical cleanup | OPEN |
| [WO-DATA-2026-09-27](./Database_Boundary_Work_Order_WO-DATA-2026-09-27.md) | Database boundary & publication policy | OPEN |
| [WO-AGENT-2026-09-27](./AgentContext_CanonicalHome_Work_Order_WO-AGENT-2026-09-27.md) | Agent context canonical home | OPEN |
| [WO-CF-2026-09-27](./Cloudflare_Tunnel_Recovery_Work_Order_WO-CF-2026-09-27.md) | Cloudflare tunnel credential recovery | OPEN |
| [WO-ARCH-2026-09-27](./Ops_Weekly_Archive_Work_Order_WO-ARCH-2026-09-27.md) | Weekly operations log archive | OPEN |
| [WO-AEYES-2026-09-27](./A-EYES_Work_Order_WO-AEYES-2026-09-27.md) | A-EYES capture rate & timelapse optimization | OPEN |

---

## Suggested attack order (fast evolution)

1. **WO-CF** — restore public tunnel (config only; high user visibility).
2. **WO-GH** — delete non-canonical Library; keep catalog clean.
3. **WO-AGENT** — one agent-context home (stops dual maintenance).
4. **WO-DATA** — label Database subtrees before anything large is moved.
5. **WO-MAP** — when new repo names exist, write the short ownership contract.
6. **WO-SRV** — path cutover only with inventory + rollback.
7. **WO-ARCH** — weekly archive once daily logs are routine.
8. **WO-AEYES** — capture/timelapse load (can parallelize anytime).
9. **WO-ECO** — umbrella; close when foundation items above settle.

---

## Rules

- One WO per coherent outcome; link related IDs.
- Keep **Status** accurate (`OPEN`, `BLOCKED`, `CLOSED`).
- Closed WOs: weekly archive under `Documentation/06-development/archive/YYYY-Www/`.
- No secrets in WO text.
