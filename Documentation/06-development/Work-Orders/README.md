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

## Active ops backlog (updated 2026-09-29 22:21 HST)

| ID | Title | Status | File |
| --- | --- | --- | --- |
| WO-ECO-2026-09-27 | Ecosystem migration & repository foundation | **IN PROGRESS** — Pacific + Energy reads + System + Plumbing PASS (2026-09-29 evidence; see WO-SRV status summary) | [WO](./Ecosystem_Migration_Work_Order_WO-ECO-2026-09-27.md) |
| WO-SRV-2026-09-27 | Pacific runtime path cutover (G2 → G3) | **IN PROGRESS** — reads, system, reports, GitHub, globe, and `LAP=` PASS tonight. Open: energy actuation, timelapse, Telegram replies. G2 kept. | [WO](./Servers_Cutover_Work_Order_WO-SRV-2026-09-27.md) |
| WO-OLD-2026-09-28 | Selective recovery from Solar-Pacific-…-Old (G1) | OPEN — scheduler trio **MIGRATED**. Live jobs run on G3. Next G1 packet still waiting. G2 code kept. | [WO](./Old_Server_Selective_Recovery_Work_Order_WO-OLD-2026-09-28.md) |
| WO-GH-2026-09-27 | GitHub catalog hygiene | **IN PROGRESS** — desk sync is the `ecosystem` row plus `skills`; `pacific` / `database` / `library` disabled (flattened tree, no nested `.git`); website/mainland still disabled | [WO](./GitHub_Catalog_Hygiene_Work_Order_WO-GH-2026-09-27.md) |
| WO-DATA-2026-09-27 | Database boundary & publication policy | **IN PROGRESS** — canonical Database path landed; public-umbrella publication list still open | [WO](./Database_Boundary_Work_Order_WO-DATA-2026-09-27.md) |
| WO-AEYES-2026-09-27 | A-EYES capture rate & timelapse | OPEN — grabs PASS 22:21. Interval still 1s (proposed 5s, not applied). Timelapse empty until the daylight window. | [WO](./A-EYES_Work_Order_WO-AEYES-2026-09-27.md) |

---

## Domain / feature proposals

| ID | Title | Priority | Status | File |
|----|-------|----------|--------|------|
| **WO-ECO-001** | Energy domain import (EcoFlow + hybrid reports) | P0 | Phase 1 signed off and archived. Actuating actions still open | [WO](./WO-ECO-001-Energy-Domain-Import.md) · [Action Plan](./Complete/WO-ECO-001-Action-Plan.md) |
| **WO-SRV-001** | Residual jobs path rewire | P0 | Draft — 22:24 HST: 30 job scripts exist; no `~/.ollama/skills/` job path. Not closed. Cutover stays on WO-SRV-2026-09-27. | [WO](./WO-SRV-001-Residual-Jobs-Path-Rewire.md) |
| **WO-WEB-001** | Public status / solar board alignment | P1 | Draft | [WO](./WO-WEB-001-Public-Status-Solar-Board.md) |
| **WO-COM-001** | Communications surface | P1 | Draft — tunnel, globe, and quiet relay are Pacific (22:23). Replies stay off. Discord still WO-COM-002. Notify policy unsealed. | [WO](./WO-COM-001-Communications-Surface.md) |
| **WO-COM-002** | Discord bot credential rotation (migration gate) | P1 | OPEN | [WO](./WO-COM-002-Discord-Bot-Credential-Rotation.md) |
| **WO-WXG-001** | Weather + Geology domain import | P1 | Draft — Weather poller **PASS**; Geology/voice jobs landed and **OFF** until sign-off | [WO](./WO-WXG-001-Weather-Geology-Import.md) |
| **WO-WOGEN-001** | Work order generator (measured friction → draft WOs) | P2 | **Draft** — architecture only; Carly seal + operator accept before implement | [WO](./WO-WOGEN-001-Work-Order-Generator.md) |
| **WO-WEB-002** | Public site foundation pass | P2 | Draft | [WO](./WO-WEB-002-Public-Site-Foundation.md) |

## Recently completed (2026-09-29 ~21:49 HST)

- [WO-RPT-001](./Complete/WO-RPT-001-Reports-Worklog-Domain-Import.md) and [action plan](./Complete/WO-RPT-001-Action-Plan.md) — roll-up written; Phase F stays deferred.
- [WO-ARCH-2026-09-27](./Complete/Ops_Weekly_Archive_Work_Order_WO-ARCH-2026-09-27.md) — first week archived, cutoff 2026-09-28.
- [WO-SYS-001](./Complete/WO-SYS-001-Poller-Observability.md) — log path, unit, banner, and FAIL policy. Telegram stays on WO-COM-001.
- [WO-AGENT-2026-09-27](./Complete/AgentContext_CanonicalHome_Work_Order_WO-AGENT-2026-09-27.md) — `Agent Context/` is the pack home. `02-agents/` stays an index.
- [WO-GH-001](./Complete/WO-GH-001-Github-Pull-Authority.md) — Option B. Pacific `github_sync_all` is the only automatic pull.

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
3. Keep G2/G1 code in place. Retire a legacy function only after Alexander's explicit sign-off; preserve legacy `SKILL.md` documentation  
4. Final `jobs.py` grep + cwd cleanup  
5. Move completed WOs to `Complete/` only after acceptance criteria are satisfied  
6. **Later:** WO-WOGEN-001 (after Carly seal + operator accept; does not block cutover)  

Architecture maps (Library):

- `Documentation/00-architecture/Migration-Lineage-Three-Generations-2026-09-28.md`
- `Documentation/00-architecture/Solar-Pacific-Old-Inventory-Map-2026-09-28.md`
- `Documentation/00-architecture/Pacific-Domain-Import-Playbook-2026-09-28.md`
- `Documentation/00-architecture/MIGRATION-DOCS-INDEX-2026-09-28.md`

---

## Live snapshot (ops) — 2026-09-29 22:21 HST

```text
systemd   Pacific run-poller.sh. Poller pid 743471. Reload skips the status window.
Energy    API reads live. B1 100%, B2 7%, laptop 43% discharging. Actuating actions still open.
System    sys_stats_cycle wrote sys-20260929-222117.json. cpu 13%, load 1.42, mem 70%.
Cameras   ch1–ch4 grabbed at 22:21. cam_server pid 743888 cwd is Pacific Security/Cameras. ch4 is a dark night frame, not a failed grab. Timelapse folders empty (no daylight-window frames).
Weather   poller pid 1378124 since 22:04. County reports written 22:13. Some NOAA pages returned HTML errors, 500, or 403.
Reports   WO-RPT-001 and WO-ARCH complete. Worklog scan steady state is a few seconds (22:15, 22:13:37).
Github    WO-GH-001 complete. github_sync_all is the only automatic pull (ecosystem + skills).
NPU       llama3.2:1b on-demand own-session PASS 22:16. No flm left running.
Log       automations_current.log is the live poller log. WO-SYS-001 complete. Telegram alerts still wait on WO-COM-001.
G2        Code kept. Do not retire without Alexander's sign-off.
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
