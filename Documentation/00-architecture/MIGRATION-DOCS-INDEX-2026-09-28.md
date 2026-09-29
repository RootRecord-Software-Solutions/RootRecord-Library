# Pacific Migration Documentation Index (2026-09-28)

Single entry point for agents and operators working the Pacific server cutover.

**Authority:** [RootRecord-Software-Solutions](https://github.com/RootRecord-Software-Solutions) — Library, Pacific, Database.

---

## Lineage & process

| Doc | Purpose |
| --- | --- |
| [Migration-Lineage-Three-Generations-2026-09-28.md](./Migration-Lineage-Three-Generations-2026-09-28.md) | G1 / G2 / G3 named; import order rule |
| [Pacific-Domain-Import-Playbook-2026-09-28.md](./Pacific-Domain-Import-Playbook-2026-09-28.md) | Step-by-step Phase 0–4; retirement stub pattern |
| [Pacific-Jobs-Path-Inventory-2026-09-28.md](./Pacific-Jobs-Path-Inventory-2026-09-28.md) | Every residual path in `jobs.py` |
| [Pacific-Server-Library-Dependency-Map-2026-09-28.md](./Pacific-Server-Library-Dependency-Map-2026-09-28.md) | Library files touched; domain status |
| [Pacific-Unmigrated-Domains-Notes-2026-09-28.md](./Pacific-Unmigrated-Domains-Notes-2026-09-28.md) | Plumbing / Reports lack G3 folders |

## G1 (Old) archive

| Doc | Purpose |
| --- | --- |
| [Solar-Pacific-Old-Inventory-Map-2026-09-28.md](./Solar-Pacific-Old-Inventory-Map-2026-09-28.md) | High-value packet → G3 mapping |
| [Solar-Pacific-Old-Full-TopLevel-Catalog-2026-09-28.md](./Solar-Pacific-Old-Full-TopLevel-Catalog-2026-09-28.md) | All **95** G1 tops classified |

### G1 scheduler skills — retired (2026-09-28)

Folders kept; `SKILL.md` kept; **`MIGRATED.md`** added on `-Old`. Do not run.

| G1 skill | Superseded by (org Pacific) |
| --- | --- |
| `hybrid-night-poller/` | `Automations/scripts/rootserver_poller.py` + stack |
| `heartbeat/` | `jobs.py` builtin `heartbeat` |
| `net-gate/` | `Automations/scripts/poller/internet_gate.py` + tunnel jobs |

Repo: `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server-Old`.

## Session records

| Doc | Purpose |
| --- | --- |
| [Grok-Pacific-Automations-Domain-Wiring-Session-2026-09-28.md](./Grok-Pacific-Automations-Domain-Wiring-Session-2026-09-28.md) | Automations wiring session |
| Ops worklog `2026-09-28 System Operator Worklog — Session 01.md` | Operator confirmation |

## Work orders

| ID | Focus |
| --- | --- |
| WO-SRV | G2 → G3 path cutover |
| WO-OLD | G1 selective recovery (blocked on G2) |
| WO-ECO | Ecosystem umbrella |
| WO-GH | repos.conf hygiene |
| WO-MAP | Master-Prompt map |
| WO-CF | Tunnel token |
| WO-AEYES | Capture rate |

See [`Documentation/06-development/Work-Orders/README.md`](../06-development/Work-Orders/README.md) (hyphen only — no space-named folder).

---

## Hard stops (cannot complete without operator)

1. **G2 domain source trees** still residual in `jobs.py` (plumbing, a-eyes, telegram, worklog, energy actions, weather)  
2. **Master-Prompt** file edits on desk `0 - Master-Prompt/` (not in Library)  
3. **repos.conf** on live Github scripts path  
4. **systemd unit** audit on desk  
5. **Secrets / tokens** restore (local only)  

**Done without operator tree:** Automations engine live on G3; G1 scheduler trio marked `MIGRATED.md` on `-Old`.

---

*Index updated 2026-09-28 ~18:13 HST — Automations G1 retirement + org authority.*
