# Work Orders — Active ops backlog

**Canonical active backlog** for ecosystem migration and Pacific runtime cutover.

Proposal drafts (accept-before-execute) live in the sibling folder: [`../Work-Orders/`](../Work-Orders/).

**Standing policy:** Do not run the old desk (`~/.ollama/skills`) as the poller host. Prefer Pacific under org `RootRecord-Pacific-Solar-Server`.

**Docs-only rule:** Index and status updates here do not migrate functions or change runtime code.

---

## Active backlog (updated 2026-09-28)

| ID | Title | Status |
| --- | --- | --- |
| [WO-ECO-2026-09-27](./Ecosystem_Migration_Work_Order_WO-ECO-2026-09-27.md) | Ecosystem migration & repository foundation | **IN PROGRESS** — Pacific + Energy + System LIVE |
| [WO-SRV-2026-09-27](./Servers_Cutover_Work_Order_WO-SRV-2026-09-27.md) | Pacific runtime path cutover (G2 skills → G3 Servers) | **IN PROGRESS** — Energy + System done; residual domains pending |
| [WO-MAP-2026-09-27](./MasterPrompt_RepoMap_Work_Order_WO-MAP-2026-09-27.md) | Master-Prompt repository ownership map | OPEN — Pacific name known |
| [WO-OLD-2026-09-28](./Old_Server_Selective_Recovery_Work_Order_WO-OLD-2026-09-28.md) | Selective recovery from Solar-Pacific-…-Old (G1) | OPEN — **blocked on G2→G3** |
| [WO-GH-2026-09-27](./GitHub_Catalog_Hygiene_Work_Order_WO-GH-2026-09-27.md) | GitHub catalog hygiene & non-canonical cleanup | OPEN |
| [WO-DATA-2026-09-27](./Database_Boundary_Work_Order_WO-DATA-2026-09-27.md) | Database boundary & publication policy | OPEN |
| [WO-AGENT-2026-09-27](./AgentContext_CanonicalHome_Work_Order_WO-AGENT-2026-09-27.md) | Agent context canonical home | OPEN |
| [WO-CF-2026-09-27](./Cloudflare_Tunnel_Recovery_Work_Order_WO-CF-2026-09-27.md) | Cloudflare tunnel credential recovery | OPEN |
| [WO-ARCH-2026-09-27](./Ops_Weekly_Archive_Work_Order_WO-ARCH-2026-09-27.md) | Weekly operations log archive | OPEN |
| [WO-AEYES-2026-09-27](./A-EYES_Work_Order_WO-AEYES-2026-09-27.md) | A-EYES capture rate & timelapse optimization | OPEN |

**WO-ECO-001 Energy Phase 1** and **System Phase 1** are live on org Pacific (see proposal folder for detailed action plans).

---

## Suggested attack order (remaining)

1. ~~Energy~~ ~~System~~ (done)
2. Worklog / reports **or** Github **or** plumbing — operator pick
3. Communications / Telegram → A-Eyes → Weather + Geology
4. Residual jobs path cleanup (zero `~/.ollama/skills` in jobs)
5. Retire G2 desk as poller host; close WO-ECO when foundation settles

Architecture maps:

- `Documentation/00-architecture/Migration-Lineage-Three-Generations-2026-09-28.md`
- `Documentation/00-architecture/Solar-Pacific-Old-Inventory-Map-2026-09-28.md`
- `Documentation/00-architecture/Pacific-Domain-Import-Playbook-2026-09-28.md`

---

## Live snapshot (ops)

```text
systemd   Pacific run-poller.sh
Energy    SUMMARY + ENERGY live
System    sys-sample on Pacific System/scripts/
Log       /home/rootrecord/Database/Logs/Automations/automations_current.log
```

---

## Rules

- One WO per coherent outcome; link related IDs.
- Keep **Status** accurate (`OPEN`, `IN PROGRESS`, `BLOCKED`, `CLOSED`).
- Closed WOs: weekly archive under `Documentation/06-development/archive/YYYY-Www/`.
- No secrets in WO text.
- **Never bulk-merge G1 `origin/` into G3 runtime.**
- Proposal WOs in `Work-Orders/` stay **document only** until explicitly accepted.
