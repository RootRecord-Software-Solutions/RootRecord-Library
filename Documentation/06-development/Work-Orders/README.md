# Work Orders — single index

**Canonical work-order home** for RootRecord (org Library).  
One folder only. Docs-only updates do not migrate functions or change runtime code.

**Standing policy:** Do not run the old desk (`~/.ollama/skills`) as the poller host. Prefer Pacific under org `RootRecord-Pacific-Solar-Server`.

**Authority:** [RootRecord-Software-Solutions](https://github.com/RootRecord-Software-Solutions).

---

## Active ops backlog (updated 2026-09-28 ~18:50 HST)

| ID | Title | Status | File |
| --- | --- | --- | --- |
| WO-ECO-2026-09-27 | Ecosystem migration & repository foundation | **IN PROGRESS** — Pacific + Energy + System LIVE; Automations engine sole authority | [WO](./Ecosystem_Migration_Work_Order_WO-ECO-2026-09-27.md) |
| WO-SRV-2026-09-27 | Pacific runtime path cutover (G2 → G3) | **IN PROGRESS** — Energy + System done; G1 schedulers retired | [WO](./Servers_Cutover_Work_Order_WO-SRV-2026-09-27.md) |
| WO-MAP-2026-09-27 | Master-Prompt repository ownership map | OPEN | [WO](./MasterPrompt_RepoMap_Work_Order_WO-MAP-2026-09-27.md) |
| WO-OLD-2026-09-28 | Selective recovery from Solar-Pacific-…-Old (G1) | OPEN — scheduler trio **MIGRATED** (no run); other packets still blocked on G2→G3 | [WO](./Old_Server_Selective_Recovery_Work_Order_WO-OLD-2026-09-28.md) |
| WO-GH-2026-09-27 | GitHub catalog hygiene | OPEN | [WO](./GitHub_Catalog_Hygiene_Work_Order_WO-GH-2026-09-27.md) |
| WO-DATA-2026-09-27 | Database boundary & publication policy | OPEN | [WO](./Database_Boundary_Work_Order_WO-DATA-2026-09-27.md) |
| WO-AGENT-2026-09-27 | Agent context canonical home | OPEN | [WO](./AgentContext_CanonicalHome_Work_Order_WO-AGENT-2026-09-27.md) |
| WO-CF-2026-09-27 | Cloudflare tunnel credential recovery | OPEN | [WO](./Cloudflare_Tunnel_Recovery_Work_Order_WO-CF-2026-09-27.md) |
| WO-ARCH-2026-09-27 | Weekly operations log archive | OPEN | [WO](./Ops_Weekly_Archive_Work_Order_WO-ARCH-2026-09-27.md) |
| WO-AEYES-2026-09-27 | A-EYES capture rate & timelapse | OPEN | [WO](./A-EYES_Work_Order_WO-AEYES-2026-09-27.md) |

---

## Domain / feature proposals

| ID | Title | Priority | Status | File |
|----|-------|----------|--------|------|
| **WO-ECO-001** | Energy domain import (EcoFlow + hybrid reports) | P0 | Phase 1 **COMPLETE** on org Pacific | [WO](./WO-ECO-001-Energy-Domain-Import.md) · [Action Plan](./WO-ECO-001-Action-Plan.md) |
| **WO-SRV-001** | Residual jobs path rewire | P0 | In progress after Energy/System | [WO](./WO-SRV-001-Residual-Jobs-Path-Rewire.md) |
| **WO-WEB-001** | Public status / solar board alignment | P1 | Draft | [WO](./WO-WEB-001-Public-Status-Solar-Board.md) |
| **WO-COM-001** | Communications surface | P1 | Draft | [WO](./WO-COM-001-Communications-Surface.md) |
| **WO-COM-002** | Discord bot credential rotation (migration gate) | P1 | OPEN | [WO](./WO-COM-002-Discord-Bot-Credential-Rotation.md) |
| **WO-WXG-001** | Weather + Geology domain import | P1 | Draft — after Energy | [WO](./WO-WXG-001-Weather-Geology-Import.md) |
| **WO-SYS-001** | Poller observability & FAIL handling | P2 | Draft (System Phase 1 live) | [WO](./WO-SYS-001-Poller-Observability.md) |
| **WO-WEB-002** | Public site foundation pass | P2 | Draft | [WO](./WO-WEB-002-Public-Site-Foundation.md) |
| **WO-GH-001** | GitHub pull authority & timer policy | P2 | Draft | [WO](./WO-GH-001-Github-Pull-Authority.md) |

---

## Automations / G1 scheduler note (2026-09-28)

Org Pacific **Automations** is production. On `Solar-Pacific-RootRecord-Server-Old`:

| G1 skill | Marker |
| --- | --- |
| `hybrid-night-poller/` | `MIGRATED.md` → `rootserver_poller` |
| `heartbeat/` | `MIGRATED.md` → jobs builtin |
| `net-gate/` | `MIGRATED.md` → `internet_gate` |

Folder + `SKILL.md` retained. Skills were functional packets (poor original design); AI processing redesign is planned — do not treat G1/G2 skill shells as the long-term agent model.

---

## Suggested attack order (remaining)

1. ~~Energy~~ ~~System~~ (done)  
2. Worklog / reports **or** Github **or** plumbing — operator pick  
3. **WO-SRV-001** residual path cleanup (zero `~/.ollama/skills` in jobs where domains land on Pacific)  
4. Communications / Telegram / Discord (**WO-COM-002** token gate before Discord LIVE) → A-Eyes → Weather + Geology  
5. Retire G2 desk as residual host; close WO-ECO when foundation settles  

Architecture maps (Library):

- `Documentation/00-architecture/Migration-Lineage-Three-Generations-2026-09-28.md`
- `Documentation/00-architecture/Solar-Pacific-Old-Inventory-Map-2026-09-28.md`
- `Documentation/00-architecture/Pacific-Domain-Import-Playbook-2026-09-28.md`
- `Documentation/00-architecture/MIGRATION-DOCS-INDEX-2026-09-28.md`

---

## Live snapshot (ops)

```text
systemd   Pacific run-poller.sh
Energy    SUMMARY + ENERGY live
System    sys-sample on Pacific System/scripts/
Log       /home/rootrecord/Database/Logs/Automations/automations_current.log
G1 sched  hybrid-night-poller / heartbeat / net-gate → MIGRATED.md on -Old
```

---

## Rules

- One WO per coherent outcome; link related IDs.
- Keep **Status** accurate (`OPEN`, `IN PROGRESS`, `BLOCKED`, `CLOSED`, `COMPLETE`).
- Closed WOs: weekly archive under `Documentation/06-development/archive/YYYY-Www/`.
- No secrets in WO text.
- **Never bulk-merge G1 `origin/` into G3 runtime.**
- **No code import** without operator source tree; **one domain at a time**.
- Prefer **`MIGRATED.md`** over silent delete when a packet is fully superseded.
- Document only until a WO is explicitly accepted for execution.
- **Messaging credentials (Discord, Telegram, etc.):** issue fresh tokens on migration/enablement; never load tokens from archive/mirror history.
