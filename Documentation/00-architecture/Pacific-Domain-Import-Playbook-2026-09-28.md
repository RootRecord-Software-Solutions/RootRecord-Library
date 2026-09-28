# Pacific Domain Import Playbook

| Field | Value |
| --- | --- |
| **Date** | 2026-09-28 (HST) |
| **Applies to** | G2 → G3 imports; then selective G1 recovery |
| **Live runtime** | `RootRecord-Pacific-Solar-Server` on Ecosystem `1 - Servers/` |

---

## Phase 0 — Preconditions (already mostly met)

- [x] G3 repo exists under org  
- [x] Domain folder shells exist  
- [x] Automations core wired and poller live  
- [x] Library path inventory for residual jobs  
- [x] G1 Old inventory mapped  
- [ ] Operator provides **source tree** for the domain being imported  

Do not start Phase 1 without source (or an explicit path on the desk to copy from).

---

## Phase 1 — Import one G2 domain (template)

### Step 1.1 — Identify

| Field | Fill in |
| --- | --- |
| Domain name | e.g. Energy |
| G2 source path | e.g. `~/.ollama/skills/energy/` |
| G3 destination | e.g. `Energy/` |
| jobs.py ids touched | e.g. ecoflow_read_boot, ecoflow_read_cycle |
| Data dirs (off-git) | e.g. Database/ENERGY |

### Step 1.2 — Inventory source

- List scripts, configs, SKILL.md  
- Mark secrets (never commit)  
- Note absolute paths inside scripts  

### Step 1.3 — Copy into G3

- Place under domain folder  
- Preserve useful structure (`scripts/read/`, etc.)  
- Add/update domain README  
- Ensure `.gitignore` covers secrets/store  

### Step 1.4 — Rewire jobs.py

- Point command + cwd at Ecosystem Servers paths (or relative once standardized)  
- Keep ECOFLOW_LOCK-style local locks  
- Commit jobs change **with** or immediately after domain files  

### Step 1.5 — Deploy

```text
push → github_sync_all → schedule-stack-reload
```

### Step 1.6 — Verify

- Poller window: job OK lines  
- Domain-specific signals (EcoFlow SUMMARY, SYSTEM samples, …)  
- No new FAIL storms  

### Step 1.7 — Document

- Short Library note or WO-SRV checkbox  
- Update path inventory row to “migrated”  

---

## Phase 2 — Repeat for next G2 domain

Recommended order:

1. Energy  
2. Github  
3. System-stats  
4. Weather full  
5. A-EYES / Security  
6. Plumbing  
7. Telegram  
8. Reports  
9. Agents  

---

## Phase 3 — Selective G1 (Old) recovery

Only after Phase 1–2 for that capability (or explicit waiver).

### Step 3.1 — Pick packet

From [Solar-Pacific-Old-Inventory-Map-2026-09-28.md](./Solar-Pacific-Old-Inventory-Map-2026-09-28.md).

### Step 3.2 — Diff

- G1 packet vs current G3 domain  
- Keep only unique useful scripts  

### Step 3.3 — Integrate

- Same as Phase 1.3–1.7  
- Label commit `G1 recovery: <packet>`  

### Step 3.4 — Never

- Bulk-copy `origin/` or `ecosystem-history/` into G3  
- Commit tokens, RTSP passwords, bot secrets  
- Enable two Telegram getUpdates owners  

---

## Phase 4 — Catalog & Master-Prompt

When most residual jobs are G3-native:

- Align `repos.conf` local_path to Ecosystem Servers (WO-GH)  
- Write Master-Prompt `08-repository-and-file-links.md` (WO-MAP)  
- Close WO-SRV residual items  

---

## Rollback

- Revert the domain commit(s) on G3  
- Restore jobs.py paths to G2 skills strings  
- schedule-stack-reload  
- G2 tree on disk remains safety net until operator removes it  

---

*Playbook 2026-09-28 HST.*
