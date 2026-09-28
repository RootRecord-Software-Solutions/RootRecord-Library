# Pacific Server ↔ Library Dependency Map

| Field | Value |
| --- | --- |
| **Date** | 2026-09-28 (HST) |
| **Purpose** | Inventory every Library file that references Pacific server paths/layout; record updates |
| **Runtime repo** | `RootRecord-Software-Solutions/RootRecord-Pacific-Solar-Server` |
| **Live path** | `/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server` |
| **Rule** | Update only confirmed current-state references; preserve historical session logs as written |
| **Companion** | [Pacific-Jobs-Path-Inventory-2026-09-28.md](./Pacific-Jobs-Path-Inventory-2026-09-28.md) |

---

## 1. Canonical path dictionary

| Concept | Current | Historical (preserve in notes) |
| --- | --- | --- |
| GitHub runtime | `RootRecord-Software-Solutions/RootRecord-Pacific-Solar-Server` | `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server` |
| Local runtime root | `…/1 - Servers/1 - RootRecord-Pacific-Solar-Server` | `~/.ollama/skills` |
| Job catalog | `Automations/scripts/jobs.py` | `automations/scripts/jobs.py` |
| Poller engine | `Automations/scripts/rootserver_poller.py` | `automations/scripts/rootserver_poller.py` |
| cloudflared | `Communications/network/cloudflare/bin/cloudflared` | `automations/bin/cloudflared` |
| Energy scripts | *(target)* `Energy/scripts/…` | `~/.ollama/skills/energy/` |
| Library desk path | `…/5 - RootRecord-Library` | (unchanged) |

---

## 2. Library inventory — files that reference server paths/layout

### 2.1 Updated 2026-09-28

| File | Action |
| --- | --- |
| Agent CONTEXT REPOS + INFRASTRUCTURE + README + CHANGELOG (×3 agents) | Current-state paths |
| WO-SRV / WO-ECO / WO-CF / WO-MAP / WO-GH / WO-AEYES | Path + status updates |
| Work Orders README | Status table |
| Library README | Runtime links |
| Grok session doc + ops worklog Session 01 | Session record |
| **Pacific-Jobs-Path-Inventory-2026-09-28.md** | Full jobs.py residual table |
| **This dependency map** | Pass A–C |

### 2.2 Historical — not rewritten

2026-09-26/27 worklogs, multi-model Session 1 architecture transcripts, PRODUCTS/WORKFLOW/IDENTITY packs without path claims.

---

## 3. Commit log trail

### Pass A — post poller confirmation
Agent maps, WO-SRV/ECO/CF, README, changelogs, session doc, ops worklog.

### Pass B — dependency mapping
WO-MAP, WO-GH, WO-AEYES, agent READMEs, this map (initial).

### Pass C — residual path documentation (docs only)

| Item | Repo |
| --- | --- |
| Jobs path inventory | Library |
| WO-SRV inventory checkbox closed | Library |
| Energy / Security / System / Github / Weather / Automations / Communications / Logs / Geology / telegram READMEs | **Pacific-Solar-Server** |
| Dependency map Pass C | Library |

---

## 4. Pacific server domains — migration status

| Domain | In Pacific repo | Path-wired | Legacy jobs |
| --- | --- | --- | --- |
| **Automations** | Yes | Yes (helpers relative; some abs strings remain) | Partial abs strings |
| **Communications/network** | Yes | Mostly | cwd globe legacy; CF abs string |
| **Weather** | Partial | Ensure present | abs string skills-prefixed |
| **Energy** | Shell + README | No | **Yes** |
| **Security / A-EYES** | Shell + README | No | **Yes** |
| **Github** | Shell + README | No | **Yes** |
| **System** (system-stats) | Shell + README | No | **Yes** |
| **Plumbing** | No domain folder | No | **Yes** (ollama/flm) |
| **Telegram** | Shell + README | No | **Yes** |
| **Reports** | No domain folder | No | **Yes** (worklog) |
| **Geology** | Shell | N/A | No jobs |
| **Logs** | Shell + README | N/A | Log path residual |

---

## 5. Remaining unmigrated domains (import order)

1. **Energy** — blocked on operator source  
2. **Github** (catalog + sync)  
3. **System-stats**  
4. **Weather** full daemon  
5. **Security / A-EYES**  
6. **Plumbing** (may need new domain or System subfolder decision)  
7. **Telegram**  
8. **Reports / worklog** (may need System or Automations subfolder decision)  
9. **Agents** packets  

---

## 6. Documentation stop condition (met)

- Current-state Library references updated or annotated  
- Exhaustive `jobs.py` residual path table published  
- Every Pacific domain shell has residual/import notes  
- No code import without source  
- Historical logs preserved  

**Next operator action:** provide Energy source tree when ready for code import; until then desk continues on residual paths safely.

---

*Map updated Pass C 2026-09-28 HST.*
