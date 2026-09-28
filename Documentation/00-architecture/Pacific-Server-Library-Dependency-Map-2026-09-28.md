# Pacific Server ↔ Library Dependency Map

| Field | Value |
| --- | --- |
| **Date** | 2026-09-28 (HST) |
| **Purpose** | Inventory every Library file that references Pacific server paths/layout; record updates |
| **Runtime repo** | `RootRecord-Software-Solutions/RootRecord-Pacific-Solar-Server` |
| **Live path** | `/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server` |
| **Rule** | Update only confirmed current-state references; preserve historical session logs as written |

---

## 1. Canonical path dictionary

| Concept | Current | Historical (preserve in notes) |
| --- | --- | --- |
| GitHub runtime | `RootRecord-Software-Solutions/RootRecord-Pacific-Solar-Server` | `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server` |
| Local runtime root | `…/1 - Servers/1 - RootRecord-Pacific-Solar-Server` | `~/.ollama/skills` |
| Job catalog | `Automations/scripts/jobs.py` | `automations/scripts/jobs.py` |
| Poller engine | `Automations/scripts/rootserver_poller.py` | `automations/scripts/rootserver_poller.py` |
| cloudflared | `Communications/network/cloudflare/bin/cloudflared` | `automations/bin/cloudflared` |
| Library desk path | `…/5 - RootRecord-Library` | (unchanged) |

---

## 2. Library inventory — files that reference server paths/layout

### 2.1 Updated this migration pass (2026-09-28)

| File | Reference type | Action |
| --- | --- | --- |
| `Agent Context/*/CONTEXT/REPOS.md` (×3) | Repo names | Updated earlier session + verified |
| `Agent Context/*/CONTEXT/INFRASTRUCTURE.md` (×3) | Live paths, domains | Updated earlier session + verified |
| `Agent Context/*/CHANGELOG.md` (×3) | Version notes | 0.1.1 |
| `Agent Context/*/README.md` (×3) | Live packet path | **Updated this pass** |
| `Documentation/06-development/Work Orders/Servers_Cutover_…` | Cutover status | Updated earlier session |
| `…/Ecosystem_Migration_…` | Ownership contract | Updated earlier session |
| `…/Cloudflare_Tunnel_Recovery_…` | cloudflared path | Updated earlier session |
| `…/MasterPrompt_RepoMap_…` | Blocking status / repo list | **Updated this pass** |
| `…/GitHub_Catalog_Hygiene_…` | catalog + Pacific slug | **Updated this pass** |
| `…/A-EYES_…` | jobs.py + a-eyes paths | **Updated this pass** (annotations only) |
| `…/Work Orders/README.md` | Status table | Updated earlier session |
| `README.md` (Library root) | Related repos | Updated earlier session |
| `Documentation/00-architecture/Grok-Pacific-Automations-…` | Session record | Created earlier session |
| `Documentation/01-operations/…/2026-09-28 … Session 01.md` | Ops worklog | Created earlier session |
| **This file** | Dependency map | **Created this pass** |

### 2.2 Reviewed — no change required

| File | Why left alone |
| --- | --- |
| `Agent Context/*/CONTEXT/PRODUCTS.md` | Product surface only; no server paths |
| `Agent Context/*/WORKFLOW.md`, `IDENTITY.md`, `PRINCIPLES.md`, `ROLE-AND-BOUNDS.md`, `HANDOFF-TEMPLATE.md` | No absolute server path claims |
| `Documentation/06-development/Work Orders/Database_Boundary_…` | Database paths already correct; no skills tree claim |
| `Documentation/06-development/Work Orders/AgentContext_CanonicalHome_…` | Notes `~/.ollama/skills/agents/` as residual runtime — still accurate |
| `Documentation/06-development/Work Orders/Ops_Weekly_Archive_…` | Ops process; no server layout claims |
| `Documentation/01-operations/0 - Human Operator Work Logs/2026-09-26*` | **Historical** reinstall log |
| `…/2026-09-27 System Operator Worklog — Session 0{1,2,3}.md` | **Historical** — leave as written |
| `…/2026-09-27 RootRecord Checkpoint — 09_27 HST.md` | **Historical** |
| `Documentation/00-architecture/RootRecord Restructuring… Session 1/**` | **Historical** multi-model exploration |
| `Guides & Tutorials/**` | Process guides; no Pacific path claims |
| Templates under `01-operations/templates/` | Templates only |

### 2.3 Intentionally not rewritten

Historical architecture session transcripts and 2026-09-27 worklogs still mention `Solar-Pacific-RootRecord-Server` and `~/.ollama/skills`. Those statements were true when written. Current-state maps (CONTEXT, WOs, this dependency map) supersede them for operators and agents.

---

## 3. Commit log (Library) — documentation migration trail

### Pass A — after live poller confirmation (earlier 2026-09-28)

| # | Commit message (summary) | Files |
| --- | --- | --- |
| 1–6 | Ava/Bruce/Carly REPOS + INFRASTRUCTURE | 6 |
| 7–9 | WO-SRV, WO-CF, WO-ECO | 3 |
| 10 | Library README runtime links | 1 |
| 11–13 | Agent CHANGELOGs 0.1.1 | 3 |
| 14 | Grok session architecture doc | 1 |
| 15 | Work Orders README status | 1 |
| 16 | Ops worklog 2026-09-28 Session 01 | 1 |

### Pass B — dependency mapping (this pass)

| # | Commit message (summary) | Files |
| --- | --- | --- |
| 17 | WO-MAP unblocked / Pacific name | 1 |
| 18 | WO-GH Pacific + catalog notes | 1 |
| 19 | WO-AEYES path annotations | 1 |
| 20–22 | Ava/Bruce/Carly README runtime paths | 3 |
| 23 | **This dependency map** | 1 |

---

## 4. Pacific server domains — migration status

| Domain | In Pacific repo | Path-wired | Still on legacy skills jobs |
| --- | --- | --- | --- |
| **Automations** | Yes | Yes | No (core) |
| **Communications/network** | Yes (cloudflare + ensure script) | Yes | Partial (globe cwd may be legacy) |
| **Weather** | Yes (ensure + sync helpers) | Yes | Weather daemon code may be residual |
| **Energy** | Shell only | No | **Yes** — EcoFlow scripts |
| **Security / A-EYES** | Shell only | No | **Yes** |
| **Github (sync scripts)** | Shell only | No | **Yes** — repos.conf / sync-all |
| **Plumbing** (ollama/flm) | Not present | No | **Yes** |
| **Telegram / coms** | Shell under Communications | No | **Yes** — ensure-relay |
| **System-stats / reports** | Not present | No | **Yes** |
| **Agents packets** | Not present | No | Residual under skills/agents |

---

## 5. Remaining unmigrated domains (recommended import order)

1. **Energy** — already producing live EcoFlow SUMMARY/ENERGY lines; highest payoff for path cleanup in `jobs.py`
2. **Github** (catalog + sync scripts) — unblocks `repos.conf` local_path alignment (WO-GH)
3. **System-stats** — high-frequency job; small surface
4. **Weather** (full daemon, not only ensure scripts)
5. **Security / A-EYES** — cameras + timelapse (WO-AEYES)
6. **Plumbing** (ollama/flm warmup)
7. **Telegram / messaging** under Communications
8. **Reports / worklog** scripts
9. **Agents** runtime packets (if retained on desk)

---

## 6. Stop condition

Documentation and dependency mapping for Library references to Pacific server paths is **complete** for this checkpoint:

- All *current-state* operational docs that asserted outdated homes were updated or annotated
- Historical logs and multi-model session archives were preserved
- No Pacific server code was restructured in this pass

**Next operator action:** provide Energy domain source for import; then rewire EcoFlow job paths on the Pacific repo (code change authorized in a future step).

---

*Map authored 2026-09-28 HST. Do not treat historical Session 1–3 worklogs as current path truth.*
