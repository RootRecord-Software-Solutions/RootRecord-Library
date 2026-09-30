# Completed work orders

**Standing archive for CLOSED / COMPLETE work orders.**

When a WO is fully done (all acceptance criteria met, no further phases):

1. Set **Status** to `COMPLETE` or `CLOSED` in the file header.
2. `git mv` the file into this folder:

```text
Documentation/06-development/Work-Orders/Complete/
```

3. Remove or strike it from the **active** tables in `../README.md` (optionally keep a one-line pointer under a “Recently completed” section).
4. Leave companion action-plan files with the WO, or move them together.

## Rules

- **Do not** move OPEN or IN PROGRESS WOs here.
- **Do not** rewrite content on archive — move only.
- Prefer `git mv` so history stays traceable.
- Multi-phase WOs stay in the parent folder until the whole WO is closed.
- Human operator session logs still archive under `Documentation/01-operations/archive/YYYY-Www/` (WO-ARCH) — that path is for logs, not WOs.

## Archived 2026-09-30

- [WO-MIG-06](./Governance_and_origin_session_archive_Work_Order_WO-MIG-06-2026-09-29.md) — governance, origin-session, and ecosystem-history decisions in the Library. Full trees archived, then removed from Solar-Pacific-RootRecord-Server-Old. `origin/` not imported.

## Archived 2026-09-29 ~21:41 HST

- [WO-MAP-2026-09-27](./MasterPrompt_RepoMap_Work_Order_WO-MAP-2026-09-27.md) — ownership map written and linked.
- [WO-CF-2026-09-27](./Cloudflare_Tunnel_Recovery_Work_Order_WO-CF-2026-09-27.md) — tunnel ready and public URL HTTP 200.
- [WO-ECO-001 action plan](./WO-ECO-001-Action-Plan.md) — Phase 1 reads only. Parent stays active for actuating actions.
- [WO-RPT-001](./WO-RPT-001-Reports-Worklog-Domain-Import.md) and [action plan](./WO-RPT-001-Action-Plan.md) — foundation closed 2026-09-29 ~21:49 HST. Phase F radio/stream remains deferred, not open work on this order.
- [WO-ARCH-2026-09-27](./Ops_Weekly_Archive_Work_Order_WO-ARCH-2026-09-27.md) — first archive week `2026-W40`, cutoff `2026-09-28`, 5 logs moved.
- [WO-SYS-001](./WO-SYS-001-Poller-Observability.md) — observability close 2026-09-29. Telegram alerts remain on WO-COM-001.
- [WO-AGENT-2026-09-27](./AgentContext_CanonicalHome_Work_Order_WO-AGENT-2026-09-27.md) — canonical pack home recorded 2026-09-29. Placeholders kept.
- [WO-GH-001](./WO-GH-001-Github-Pull-Authority.md) — Option B, Alexander, 2026-09-29. One sync cycle observed at 22:01:03 HST.

## Created

Operator desk path (2026-09-28):

```text
/home/rootrecord/RootRecord-Ecosystem/5 - RootRecord-Library/Documentation/06-development/Work-Orders/Complete
```

*Standing convention 2026-09-28 HST.*
