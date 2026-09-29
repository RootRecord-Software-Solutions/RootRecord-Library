# Work Orders — single index

**Canonical work-order home** for RootRecord (org Library).  
One active folder + **`Complete/`** for finished WOs. Docs-only updates do not migrate functions or change runtime code unless a WO is accepted for execution.

**Standing policy:** Do not run the old desk (`~/.ollama/skills`) as the poller host. Prefer Pacific under org `RootRecord-Pacific-Solar-Server`.

**Authority:** [RootRecord-Software-Solutions](https://github.com/RootRecord-Software-Solutions).

---

## Layout

```text
Work-Orders/
├─ README.md                 # this index (active only)
├─ Complete/                 # CLOSED / COMPLETE WOs (git mv here)
│   └─ README.md
├─ drafts/                   # generator / Carly drafts (not auto-promoted)
└─ WO-*.md / *_Work_Order_*.md
```

**Close a WO:** set Status → COMPLETE/CLOSED → `git mv` into [`Complete/`](./Complete/).

---

## Active ops backlog (updated 2026-09-28 ~20:55 HST)

| ID | Title | Status | File |
| --- | --- | --- | --- |
| WO-ECO-2026-09-27 | Ecosystem migration & repository foundation | **IN PROGRESS** — Pacific + Energy + System + Plumbing LIVE | [WO](./Ecosystem_Migration_Work_Order_WO-ECO-2026-09-27.md) |
| WO-SRV-2026-09-27 | Pacific runtime path cutover (G2 → G3) | **IN PROGRESS** — Pacific source paths landed for active residuals; runtime verification + legacy retirement remain | [WO](./Servers_Cutover_Work_Order_WO-SRV-2026-09-27.md) |
| **WO-RPT-001** | Reports / worklog domain import | **Foundation LIVE** (A–E) | [WO](./WO-RPT-001-Reports-Worklog-Domain-Import.md) · [Action Plan](./WO-RPT-001-Action-Plan.md) |
| WO-MAP-2026-09-27 | Master-Prompt repository ownership map | OPEN | [WO](./MasterPrompt_RepoMap_Work_Order_WO-MAP-2026-09-27.md) |
| WO-OLD-2026-09-28 | Selective recovery from Solar-Pacific-…-Old (G1) | OPEN — scheduler trio **MIGRATED**; other packets blocked on G2→G3 | [WO](./Old_Server_Selective_Recovery_Work_Order_WO-OLD-2026-09-28.md) |
| WO-GH-2026-09-27 | GitHub catalog hygiene | **IN PROGRESS** — Pacific `Github/` sync LIVE; website/mainland still disabled | [WO](./GitHub_Catalog_Hygiene_Work_Order_WO-GH-2026-09-27.md) |
| WO-DATA-2026-09-27 | Database boundary & publication policy | OPEN | [WO](./Database_Boundary_Work_Order_WO-DATA-2026-09-27.md) |
| WO-AGENT-2026-09-27 | Agent context canonical home | OPEN | [WO](./AgentContext_CanonicalHome_Work_Order_WO-AGENT-2026-09-27.md) |
| WO-CF-2026-09-27 | Cloudflare tunnel credential recovery | OPEN | [WO](./Cloudflare_Tunnel_Recovery_Work_Order_WO-CF-2026-09-27.md) |
| WO-ARCH-2026-09-27 | Weekly operations log archive | OPEN — implement under WO-RPT-001 Phase D | [WO](./Ops_Weekly_Archive_Work_Order_WO-ARCH-2026-09-27.md) |
| WO-AEYES-2026-09-27 | A-EYES capture rate & timelapse | OPEN | [WO](./A-EYES_Work_Order_WO-AEYES-2026-09-27.md) |

---

## Domain / feature proposals

| ID | Title | Priority | Status | File |
|----|-------|----------|--------|------|
| **WO-ECO-001** | Energy domain import (EcoFlow + hybrid reports) | P0 | Phase 1 **COMPLETE** on org Pacific — actions path LIVE | [WO](./WO-ECO-001-Energy-Domain-Import.md) · [Action Plan](./WO-ECO-001-Action-Plan.md) |
| **WO-SRV-001** | Residual jobs path rewire | P0 | Draft — blocked on WO-ECO-001 (and later domain imports); retained as reference while WO-SRV-2026-09-27 carries the active cutover | [WO](./WO-SRV-001-Residual-Jobs-Path-Rewire.md) |
| **WO-RPT-001** | Reports / worklog domain import | P0 | **Foundation LIVE** | [WO](./WO-RPT-001-Reports-Worklog-Domain-Import.md) · [Action Plan](./WO-RPT-001-Action-Plan.md) |
| **WO-WEB-001** | Public status / solar board alignment | P1 | Draft | [WO](./WO-WEB-001-Public-Status-Solar-Board.md) |
| **WO-COM-001** | Communications surface | P1 | Draft — Telegram residual next | [WO](./WO-COM-001-Communications-Surface.md) |
| **WO-COM-002** | Discord bot credential rotation (migration gate) | P1 | OPEN | [WO](./WO-COM-002-Discord-Bot-Credential-Rotation.md) |
| **WO-WXG-001** | Weather + Geology domain import | P1 | Draft — after Energy | [WO](./WO-WXG-001-Weather-Geology-Import.md) |
| **WO-SYS-001** | Poller observability & FAIL handling | P2 | Draft (System Phase 1 live) | [WO](./WO-SYS-001-Poller-Observability.md) |
| **WO-WOGEN-001** | Work order generator (measured friction → draft WOs) | P2 | **Draft** — architecture only; Carly seal + operator accept before implement | [WO](./WO-WOGEN-001-Work-Order-Generator.md) |
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

1. ~~Energy~~ ~~System~~ ~~Reports~~ ~~Plumbing / Energy actions~~ ~~Telegram~~ ~~A-Eyes~~ (Pacific source paths landed)  
2. **Runtime verification** → Telegram, A-Eyes, Energy actions, Pacific poller  
3. Retire each verified legacy runtime function immediately; preserve legacy `SKILL.md` documentation  
4. Final `jobs.py` grep + cwd cleanup  
5. Move completed WOs to `Complete/` only after acceptance criteria are satisfied  
6. **Later:** WO-WOGEN-001 (after Carly seal + operator accept; does not block cutover)  

Architecture maps (Library):

- `Documentation/00-architecture/Migration-Lineage-Three-Generations-2026-09-28.md`
- `Documentation/00-architecture/Solar-Pacific-Old-Inventory-Map-2026-09-28.md`
- `Documentation/00-architecture/Pacific-Domain-Import-Playbook-2026-09-28.md`
- `Documentation/00-architecture/MIGRATION-DOCS-INDEX-2026-09-28.md`

---

## Live snapshot (ops)

```text
systemd   Pacific run-poller.sh (reload skips status window)
Energy    reads + leapfrog + actions LIVE
System    sys-sample + plumbing warmups LIVE
Reports   foundation LIVE — worklog_scan → Pacific Reports/scripts
Github    setup-remotes + sync-all LIVE
Log       /home/rootrecord/Database/Logs/Automations/automations_current.log
G1 sched  hybrid-night-poller / heartbeat / net-gate → MIGRATED.md on -Old
Residual  runtime verification/legacy retirement · weather(disabled)
```

---

## Rules

- One WO per coherent outcome; link related IDs.
- Keep **Status** accurate (`OPEN`, `IN PROGRESS`, `BLOCKED`, `CLOSED`, `COMPLETE`, `DRAFT`).
- **Closed WOs:** `git mv` into [`Complete/`](./Complete/) — not a separate weekly tree.
- **Draft / generator WOs:** stay under `drafts/` or explicit DRAFT status until operator promotes — never auto-promote.
- **Human session logs:** weekly archive under `Documentation/01-operations/archive/YYYY-Www/` (WO-ARCH).
- No secrets in WO text.
- **Never bulk-merge G1 `origin/` into G3 runtime.**
- **No code import** without operator source tree; **one domain at a time**.
- Prefer **`MIGRATED.md`** over silent delete when a packet is fully superseded.
- Document only until a WO is explicitly accepted for execution.
- **Messaging credentials (Discord, Telegram, etc.):** issue fresh tokens on migration/enablement; never load tokens from archive/mirror history.
