# Migration Lineage — Three Generations of Pacific Runtime

| Field | Value |
| --- | --- |
| **Date** | 2026-09-28 (HST) |
| **Updated** | 2026-09-28 ~18:13 HST — G1 scheduler skills retired via MIGRATED.md |
| **Purpose** | Name the three runtime generations and the only safe import order |
| **Rule** | Documentation only — no bulk copy of Old into Pacific without staged domain review |
| **Authority** | Org [RootRecord-Software-Solutions](https://github.com/RootRecord-Software-Solutions) |

---

## 1. Generations (newest → oldest)

| Gen | GitHub | Role |
| --- | --- | --- |
| **G3 — Current** | `RootRecord-Software-Solutions/RootRecord-Pacific-Solar-Server` | Live Ecosystem runtime under `1 - Servers/…`; domain folders (Automations, Communications, …) |
| **G2 — Intermediate skills** | `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server` (+ desk `~/.ollama/skills`) | Lowercase skill tree that still powers residual jobs (energy actions, a-eyes, github, plumbing, …). Poor original skill design; AI processing redesign planned. Not the poller host. |
| **G1 — Old skill archive** | `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server-Old` | Large historical skill packet tree; forensic / selective recovery source. Scheduler trio marked retired (see §3). |

Also exists: `rootrecordsoftwaresolutions/old` (private; not the primary Old inventory used here).

---

## 2. Absolute rule

```text
Finish G2 residual domains into G3
  → only then selectively recover from G1 (Old)
    → never bulk-merge G1 over live G3
```

Reasons:

1. **G3 is live** — poller confirmed active on Ecosystem path; **org is authority**.
2. **G2 matches today’s residual job paths** — `jobs.py` still calls `~/.ollama/skills/…` for non-engine domains.
3. **G1 is a different shape** — skill packets, not the G2/G3 domain layout.
4. **G1 is huge** — `origin/` alone is thousands of paths; blind import would bury the live tree.

---

## 3. What is already true on G3

| Domain | G3 state |
| --- | --- |
| **Automations** | **Live / authoritative** — poller, jobs, stack, internet_gate |
| Communications/network (cloudflare) | Live binary + config |
| Energy | LIVE (read path) |
| System | LIVE (sys-sample) |
| Weather | Partial ensure scripts |
| Security, Github, Geology | Shells + residual-path READMEs |
| Messaging shells | Placeholders |

### G1 scheduler skills — retired (do not run)

On `-Old`, folders + `SKILL.md` retained; **`MIGRATED.md`** points at org Pacific:

| G1 folder | G3 replacement |
| --- | --- |
| `hybrid-night-poller/` | `rootserver_poller.py` + `rr-rootserver-poller.service` |
| `heartbeat/` | jobs builtin `heartbeat` |
| `net-gate/` | `poller/internet_gate.py` + tunnel builtins |

Residual job strings may still execute **G2** paths for other domains. That is intentional until each domain is imported or redesign lands. Auto-sync from GitHub updates desk trees the catalog owns.

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

## 5. When G1 (Old) is allowed

Only after the matching G2 domain is either:

- imported into G3 and stable, **or**
- explicitly abandoned (documented exception),

and each Old packet is reviewed for secrets, dead paths, supersession, and size.

**Exception already taken:** G1 scheduler trio above — superseded by G3 Automations; marked `MIGRATED.md` only (no bulk delete of folder shells).

Primary Old map: [Solar-Pacific-Old-Inventory-Map-2026-09-28.md](./Solar-Pacific-Old-Inventory-Map-2026-09-28.md).

---

## 6. Live path of truth

```text
/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server
```

GitHub of truth for runtime code: org **RootRecord-Pacific-Solar-Server**.  
Library holds migration docs, not the running code.

---

*Lineage doc updated 2026-09-28 ~18:13 HST.*
