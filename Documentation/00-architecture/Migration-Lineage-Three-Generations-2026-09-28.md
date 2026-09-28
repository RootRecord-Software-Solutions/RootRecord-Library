# Migration Lineage — Three Generations of Pacific Runtime

| Field | Value |
| --- | --- |
| **Date** | 2026-09-28 (HST) |
| **Purpose** | Name the three runtime generations and the only safe import order |
| **Rule** | Documentation only — no bulk copy of Old into Pacific without staged domain review |

---

## 1. Generations (newest → oldest)

| Gen | GitHub | Role |
| --- | --- | --- |
| **G3 — Current** | `RootRecord-Software-Solutions/RootRecord-Pacific-Solar-Server` | Live Ecosystem runtime under `1 - Servers/…`; domain folders (Automations, Communications, …) |
| **G2 — Intermediate skills** | `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server` (+ desk `~/.ollama/skills`) | Lowercase skill tree that still powers residual jobs (energy, a-eyes, github, plumbing, …) |
| **G1 — Old skill archive** | `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server-Old` | Large historical skill packet tree (~7k paths); forensic / selective recovery source |

Also exists: `rootrecordsoftwaresolutions/old` (private; not the primary Old inventory used here).

---

## 2. Absolute rule

```text
Finish G2 residual domains into G3
  → only then selectively recover from G1 (Old)
    → never bulk-merge G1 over live G3
```

Reasons:

1. **G3 is live** — poller confirmed active on Ecosystem path.
2. **G2 matches today’s job paths** — `jobs.py` still calls `~/.ollama/skills/energy/…`, `a-eyes/…`, etc.
3. **G1 is a different shape** — skill packets (`energy/ecoflow-*`, `weather/hurricane-*`, `reports/sort/…`) not the G2/G3 domain layout.
4. **G1 is huge** — `origin/` alone is thousands of paths; blind import would bury the live tree.

---

## 3. What is already true on G3

| Domain | G3 state |
| --- | --- |
| Automations | Live (poller, jobs, stack) |
| Communications/network (cloudflare) | Live binary + config |
| Weather | Partial ensure scripts |
| Energy, Security, System, Github, Geology, Logs | Shells + residual-path READMEs |
| Messaging shells | Placeholders |

Residual job strings still execute G2 paths on disk. That is intentional until each domain is imported from **G2 first**.

---

## 4. G2 → G3 import order (unchanged priority)

1. Energy  
2. Github (repos.conf / sync)  
3. System-stats  
4. Weather (full daemon)  
5. Security / A-EYES  
6. Plumbing  
7. Telegram  
8. Reports / worklog  
9. Agents packets  

See: [Pacific-Jobs-Path-Inventory-2026-09-28.md](./Pacific-Jobs-Path-Inventory-2026-09-28.md).

---

## 5. When G1 (Old) is allowed

Only after the matching G2 domain is either:

- imported into G3 and stable, **or**
- explicitly abandoned in favor of an Old packet (documented exception),

and each Old packet is reviewed for:

- secrets / tokens  
- dead paths  
- supersession by G2/G3  
- size (media, origin dumps)  

Primary Old map: [Solar-Pacific-Old-Inventory-Map-2026-09-28.md](./Solar-Pacific-Old-Inventory-Map-2026-09-28.md).

---

## 6. Live path of truth

```text
/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server
```

GitHub of truth for runtime code: org **RootRecord-Pacific-Solar-Server**.  
Library holds migration docs, not the running code.

---

*Lineage doc 2026-09-28 HST.*
