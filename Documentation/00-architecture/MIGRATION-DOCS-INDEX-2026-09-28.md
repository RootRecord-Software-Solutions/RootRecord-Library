# Pacific Migration Documentation Index (2026-09-28)

Single entry point for agents and operators working the Pacific server cutover.

---

## Lineage & process

| Doc | Purpose |
| --- | --- |
| [Migration-Lineage-Three-Generations-2026-09-28.md](./Migration-Lineage-Three-Generations-2026-09-28.md) | G1 / G2 / G3 named; import order rule |
| [Pacific-Domain-Import-Playbook-2026-09-28.md](./Pacific-Domain-Import-Playbook-2026-09-28.md) | Step-by-step Phase 0–4 |
| [Pacific-Jobs-Path-Inventory-2026-09-28.md](./Pacific-Jobs-Path-Inventory-2026-09-28.md) | Every residual path in `jobs.py` |
| [Pacific-Server-Library-Dependency-Map-2026-09-28.md](./Pacific-Server-Library-Dependency-Map-2026-09-28.md) | Library files touched; domain status |
| [Pacific-Unmigrated-Domains-Notes-2026-09-28.md](./Pacific-Unmigrated-Domains-Notes-2026-09-28.md) | Plumbing / Reports lack G3 folders |

## G1 (Old) archive

| Doc | Purpose |
| --- | --- |
| [Solar-Pacific-Old-Inventory-Map-2026-09-28.md](./Solar-Pacific-Old-Inventory-Map-2026-09-28.md) | High-value packet → G3 mapping |
| [Solar-Pacific-Old-Full-TopLevel-Catalog-2026-09-28.md](./Solar-Pacific-Old-Full-TopLevel-Catalog-2026-09-28.md) | All **95** G1 tops classified |

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

See `Documentation/06-development/Work Orders/README.md`.

---

## Hard stops (cannot complete without operator)

1. **G2 domain source trees** (Energy first) for code import  
2. **Master-Prompt** file edits on desk `0 - Master-Prompt/` (not in Library)  
3. **repos.conf** on live github scripts path  
4. **systemd unit** audit on desk  
5. **Secrets / tokens** restore (local only)  

Everything else that can be done in Library + G3 domain README documentation is complete as of this index.

---

*Index 2026-09-28 HST.*
