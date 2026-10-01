# Private Repos Feature Map — Missed Capabilities vs G3 Pacific

| Field | Value |
| --- | --- |
| **Date** | 2026-09-28 (HST) |
| **Scope** | Private `rootrecordsoftwaresolutions/*` repos with ops/infra value **not** fully represented in public G1–G3 maps |
| **Rule** | Documentation only — do not bulk-merge private trees into G3 |
| **Prerequisite** | Public G1–G3 docs complete ([MIGRATION-DOCS-INDEX](./MIGRATION-DOCS-INDEX-2026-09-28.md)) |

---

## 1. Architecture families (private)

| Repo | Privacy | Role vs G3 Pacific |
| --- | --- | --- |
| **RootRecord-Core-Processor** | private | Hosted 24/7 processor: installers, read-only GitHub pull timer, boot self-check |
| **RootRecord-Core-Ops** | private | Operator desk processors: EcoFlow, WatchDog, Weather/Kilauea/EQ reports, migration ledger |
| **RootRecord-Cloud** | private | Next.js public cloud surface (goals, blog, status, chat proxy) |
| **all-connections** | private | Combined atlas: Ava desktop + FastAPI origin `:8787` + Workers + URL map |
| **ava-core-old** | private | Older Ava solar Root Server / GEO docs |
| **old** | private | Parallel G1-style skill dump (+ sites); forensic |
| **mirror-*** (many) | private | **Inventory mirrors Aug 2026** — not primary; do not treat as deploy source |

**Three-system boundary (from Core-Processor README):**

1. **Core-Node** — MIT self-hostable (if/when present)  
2. **Core-Ops** — local operator desk  
3. **Core-Processor** — hosted operational runtime  
4. **RootMC** — game network (separate)

**G3 Pacific Solar Server** is the current Hawaiʻi **domain-folder** runtime (Automations poller `:8799`). It is **not** the same checkout as Core-Processor or the Windows Ava desk, but must stay compatible with the four-operation contract documented in Core-Ops.

---

## 2. Features likely missed by public G1–G3-only planning

### 2.1 High priority for Pacific / energy / ops continuity

| Feature | Where it lives | Why it matters | Suggested home |
| --- | --- | --- | --- |
| **EcoFlow desk processors** | Core-Ops `Ecoflow/` (landed per migration ledger) | Parallel to G2 `skills/energy` and G1 `energy/ecoflow-*`; may hold **newer** desk logic | Diff vs G2 energy before G3 `Energy/` import |
| **WatchDog / single origin** | Core-Ops `WatchDog/` | One origin, one cloudflared, hung-process recycle | Align with G3 stack stop/reload; do not run two supervisors |
| **Read-only server pull** | Core-Processor `scripts/auto-pull-server.py` + `systemd/ava-github-pull.*` | FF-only pull every 10m; dirty checkout refuse | Compare to G2 `github_sync` / G3 Github domain |
| **Hosted install bootstrap** | Core-Processor `install.sh`, `core/boot.py` | Idempotent Ubuntu/Debian first-run | Reference for Pacific host rebuilds; not copy-paste into G3 git blindly |
| **Four-operation matrix** | Core-Ops `Processor_Migration_List_Readme_For_Agents.md` | Local desk · VPS nodes · Vercel · Cloudflare must all be documented per processor | Library standing rule for any new G3 domain |

### 2.2 Origin / API surface (older stack, still feature-rich)

| Feature | Where | Notes |
| --- | --- | --- |
| FastAPI origin **:8787** | `all-connections/ava-origin-python/` | Routes: status, solar, crons, chat, media, reports, minecraft, OBS, goals, economy |
| Cron catalog | `ava-origin-python/crons/` | kilauea, noaa, solar_weather, d1_sync, hourly_chime, overnight, player_economy, system_perf, vercel_builds, … |
| Electron **Ava desktop** | `all-connections/ava-desktop/` | Bridge, lifecycle, opsCommands, connectionConfig |
| URL atlas | `all-connections/README.md` | Full public hostname map (RootMC, Ava, Goals workers, tunnels) |
| Public boards | ava.rootmc.net, origin.avaivy.cloud → `:8787` | Distinct from G3 poller public `rootserver.rootrecord.cloud` → `:8799` |

**Risk:** two “origins” (8787 vs 8799). Standing rule from Core-Ops: **never start a second origin or second cloudflared** without explicit operator design.

### 2.3 Reports / hazards (partially in G1, richer in Core-Ops)

| Feature | Core-Ops | Public G1 |
| --- | --- | --- |
| Hybrid Tracking Reports | Landed | reports/sort cousins |
| Weather / NWS report files | `Weather/` + Chronology | weather/* |
| Kīlauea report files | `Kilauea/` | kilauea/* |
| Earthquake reports | `Earthquakes/` | earthquakes |
| Chronology dated report store | `Chronology/Reports/2026/…` | Not a G3 code concern — data/docs |

### 2.4 Still open on Core-Ops migration ledger (planned features)

Not yet “landed” as Core-Ops processors (from their own checklist):

- Status and Health  
- Backup / Restore / Rollback  
- Origin Lifecycle and Boot  
- Scheduler Control  
- Voice and Audio / Radio Program  
- Accounts and Identity / Inbox and D1 Sync  
- Economy and Finance / Governance  
- Public Node Connectivity / VPS Deployment  
- Vercel Site Flows / Cloudflare Fallback  
- Media and Workstations / Minecraft Node Apps  

These are **product/ops roadmap items**, not automatically G3 Pacific domains — but any G3 design should not invent conflicting schedulers.

### 2.5 Cloud / product (not Pacific server core)

| Repo | Features | Home |
| --- | --- | --- |
| RootRecord-Cloud | goals UI, blog, login, status, chat API, desk-api proxy | Website / Cloud product |
| mirror-rootrecord-* | Minecraft plugins, weather manager, solana, etc. | Product mirrors only |
| RootMC-Net | Game net site | RootMC |

---

## 3. Port collision / identity table

| Service | Port / host | Stack |
| --- | --- | --- |
| G3 poller HTTP | `127.0.0.1:8799` | Pacific Automations |
| G3 public | `rootserver.rootrecord.cloud` | CF tunnel + G3 |
| Ava origin | `127.0.0.1:8787` | all-connections / Core-Ops era |
| Ava public | `ava.rootmc.net`, `origin.avaivy.cloud` | tunnel → 8787 |
| A-EYES cam | `127.0.0.1:8791` | G2 a-eyes |
| Ollama | `127.0.0.1:11434` | plumbing |
| RootMC API | `api.rootmc.net` | Worker only (not FastAPI) |

---

## 4. Recommended recovery order (after G2→G3)

1. **Diff Core-Ops Ecoflow vs G2 energy** — pick winner scripts for G3 Energy.  
2. **Document single-supervisor policy** — G3 stack scripts vs Core-Ops WatchDog (no dual spawn).  
3. **Compare Core-Processor auto-pull vs G2 github sync** — one catalog story.  
4. **Mine all-connections cron list** for jobs missing from G3 `jobs.py` (kilauea, solar_weather, hourly_chime, d1_sync, …) — add only with operator approval.  
5. **Keep URL atlas** in Library or Master-Prompt; do not lose hostname map.  
6. **Ignore mirror-*** for code import.  
7. **old** private repo = forensic twin of G1; use only if public Old lacks a packet.  

---

## 5. Explicit non-goals

- Merging Electron desktop into G3 Pacific server git  
- Replacing G3 Automations with Windows Task Scheduler watchdog on Linux desk  
- Pointing `api.rootmc.net` at FastAPI (known historical breakage)  
- Committing secrets from any private checkout  

---

## 6. Related public docs

- [Migration-Lineage-Three-Generations](./Migration-Lineage-Three-Generations-2026-09-28.md)  
- [Solar-Pacific-Old-Full-TopLevel-Catalog](./Solar-Pacific-Old-Full-TopLevel-Catalog-2026-09-28.md)  
- [Pacific-Jobs-Path-Inventory](./Pacific-Jobs-Path-Inventory-2026-09-28.md)  
- [MIGRATION-DOCS-INDEX](./MIGRATION-DOCS-INDEX-2026-09-28.md)  

---

*Private feature map 2026-09-28 HST from accessible private repo trees and READMEs. Paths and checklists paraphrased for Library; private code stays private.*
