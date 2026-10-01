# Migration Lineage — Generations of Pacific Runtime

| Field | Value |
| --- | --- |
| **Date** | 2026-09-28 (HST) |
| **Updated** | 2026-09-28 ~18:28 HST — G0 (`old`) named |
| **Purpose** | Name runtime generations and the only safe import order |
| **Rule** | Documentation only — no bulk copy of archives into Pacific without staged domain review |
| **Authority** | Org [RootRecord-Software-Solutions](https://github.com/RootRecord-Software-Solutions) |

---

## 1. Generations (newest → oldest)

| Gen | GitHub | Role |
| --- | --- | --- |
| **G3 — Current** | `RootRecord-Software-Solutions/RootRecord-Pacific-Solar-Server` | Live Ecosystem runtime under `1 - Servers/…`; domain folders (Automations, Communications, …) |
| **G2 — Intermediate skills** | `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server` (+ desk `~/.ollama/skills`) | Lowercase skill tree that still powers residual jobs. Not the poller host. AI processing redesign planned. |
| **G1 — Grouped skill archive** | `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server-Old` | ~95 grouped packets; forensic / selective recovery. Scheduler trio marked `MIGRATED.md`. |
| **G0 — Deepest archive** | `rootrecordsoftwaresolutions/old` | ~200 **flattened** skill tops; feature scavenger only. [G0 README](https://github.com/rootrecordsoftwaresolutions/old/blob/main/README.md). |

---

## 2. Absolute rule

```text
Finish G2 residual domains into G3
  → only then selectively recover from G1
    → only then G0 diff-only for unique scripts
      → never bulk-merge G1 or G0 over live G3
```

Reasons:

1. **G3 is live** — org is authority.  
2. **G2 matches today’s residual job paths.**  
3. **G1 is a different shape** (grouped packets).  
4. **G0 is deeper and noisier** (flattened tops + older AVA notes) — high noise, low urgency until residuals settle.  
5. Blind import of either archive would bury the live tree.

---

## 3. What is already true on G3

| Domain | G3 state |
| --- | --- |
| **Automations** | **Live / authoritative** |
| Communications/network (cloudflare) | Live binary + config |
| Energy | LIVE (read path) |
| System | LIVE (sys-sample) |
| Weather | Partial ensure scripts |
| Security, Github, Geology | Shells + residual-path READMEs |

### G1 scheduler skills — retired (do not run)

| G1 folder | G3 replacement |
| --- | --- |
| `hybrid-night-poller/` | `rootserver_poller.py` + `rr-rootserver-poller.service` |
| `heartbeat/` | jobs builtin `heartbeat` |
| `net-gate/` | `poller/internet_gate.py` + tunnel builtins |

G0 may still contain flat cousins of the same names — still archive only.

---

## 4. G2 → G3 import order (remaining)

1. ~~Energy~~ (Phase 1 done)  
2. Github (repos.conf / sync)  
3. ~~System-stats~~ (Phase 1 done)  
4. Weather (full daemon)  
5. Security / A-EYES  
6. Plumbing  
7. Telegram  
8. Reports / worklog  
9. Agents / AI processing redesign (planned)  

See: [Pacific-Jobs-Path-Inventory-2026-09-28.md](./Pacific-Jobs-Path-Inventory-2026-09-28.md).

---

## 5. When G1 / G0 is allowed

**G1:** after matching G2 domain imported or waived; review secrets, dead paths, supersession, size. Prefer `MIGRATED.md`.

**G0:** only after G1 pass for that theme, or as an explicit scavenger (broadcast, day-reports, hurricane, voice, agents, crypto nodes). See [MIGRATION-DOCS-INDEX § G0](./MIGRATION-DOCS-INDEX-2026-09-28.md).

Primary G1 map: [Solar-Pacific-Old-Inventory-Map-2026-09-28.md](./Solar-Pacific-Old-Inventory-Map-2026-09-28.md).

---

## 6. Live path of truth

```text
/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server
```

GitHub of truth for runtime code: org **RootRecord-Pacific-Solar-Server**.  
Library holds migration docs, not the running code.

---

*Lineage doc updated 2026-09-28 ~18:28 HST.*
