# Solar-Pacific-RootRecord-Server-Old — Inventory & G3 Mapping

| Field | Value |
| --- | --- |
| **Date** | 2026-09-28 (HST) |
| **Source repo** | https://github.com/rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server-Old |
| **Tree snapshot** | main @ inventory (~7286 paths) |
| **Generation** | **G1** — see [Migration-Lineage-Three-Generations-2026-09-28.md](./Migration-Lineage-Three-Generations-2026-09-28.md) |
| **Rule** | Forensic map only — do not bulk-import into live G3 |

---

## 1. What this tree is

G1 is a **skill-packet archive**: many top-level folders each with `SKILL.md` / `DAILY.md` / `INDEX.md` / `scripts/` / `references/migrate.md` patterns. It is **not** the same layout as:

- G2 lowercase skills (`energy/scripts/read/…`, `a-eyes/…`, `automations/…`), or  
- G3 domain tree (`Automations/`, `Communications/`, `Energy/`, …).

Largest tops by path count (approx.):

| Paths | Top-level |
| --- | --- |
| ~4342 | `origin/` |
| ~473 | `ecosystem-history/` |
| ~263 | `reports/` |
| ~208 | `council/` |
| ~179 | `persona/` |
| ~154 | `rootmc-android/` |
| ~153 | `kilauea/` |
| ~127 | `topics/` |
| ~97 | `weather/` |
| ~92 | `energy/` |
| ~58 | `boot/` |
| ~49 | `cloudflare-workers/` |
| ~47 | `companions/`, `public-edge/` |
| … | many smaller skill packets |

**Do not** import `origin/` or `ecosystem-history/` into G3 runtime git without an explicit archive decision (prefer Library archive or external storage).

---

## 2. High-value packets → proposed G3 home

### 2.1 Energy (G1 `energy/`)

| G1 packet | Notes | Proposed G3 |
| --- | --- | --- |
| `energy/ecoflow-ble-poller` | BLE polling ancestry | `Energy/` (after G2 energy import) |
| `energy/ecoflow-automations` | Automation helpers | `Energy/` |
| `energy/ecoflow-ac-solar-gate` | AC/solar gating | `Energy/` |
| `energy/ecoflow-quota` | Quota logic | `Energy/` |
| `energy/ecoflow-river-car` | River/car specific | `Energy/` or retire |

**Order:** Import **G2** `~/.ollama/skills/energy/` first (matches live jobs). Then diff G1 packets for missing features only.

### 2.2 Weather (G1 `weather/`)

| G1 packet | Proposed G3 |
| --- | --- |
| `weather/live-wx`, `nws-hawaii`, `rr-noaa` | `Weather/` |
| `weather/hurricane-*` | `Weather/` or product-specific |
| `weather/radar-archive`, `official-weather-media` | Data policy — often Database / Weather-Database, not G3 git |

### 2.3 Communications

| G1 | Proposed G3 |
| --- | --- |
| `communications/telegram`, `discord`, `slack` | `Communications/{telegram,discord,slack}/` |
| `council/council-telegram` | Communications + council policy |
| `network-globe/` | `Communications/network/` (globe) |
| `cloudflare-workers/` | Communications or Website edge — not poller cloudflared binary |
| `public-edge/` | Website / public surface, not necessarily G3 |

### 2.4 System / host

| G1 | Proposed G3 |
| --- | --- |
| `host-metrics/` | `System/` (align with G2 system-stats) |
| `heartbeat/` | Often engine builtin now — compare before import |
| `system-perf/`, `uptime-log/`, `log-cleanup/` | `System/` or `Logs/` |
| `scheduler-clock/` | Superseded by G3 Automations poller? **Verify before merge** |
| `boot/` | Historical boot — Master-Prompt / ops docs, not blind runtime |

### 2.5 Reports / worklog ancestry

| G1 | Proposed G3 |
| --- | --- |
| `reports/` (+ `reports/sort/…`) | Future Reports domain or Automations helpers |
| Prefer G2 `reports/scripts/worklog_once.sh` for live job first | |

### 2.6 Security / cameras / geology

| G1 | Proposed G3 |
| --- | --- |
| `kilauea/kilauea-cams` | Security or Geology product path |
| `kilauea/kilauea-alerts`, `weather-kilauea` | Product / Weather / Geology |
| `panels-cam/` | Security |
| No G1 `a-eyes/` top-level | A-EYES is **G2** artifact — do not expect it in Old |

### 2.7 Agents / persona / council

| G1 | Destination |
| --- | --- |
| `persona/` | Library Agent Context + optional G3 agents domain |
| `council/` | Ops / Communications / Library — not bulk into G3 |
| `companions/` | Product or Library |

### 2.8 Github / git

| G1 | Proposed G3 |
| --- | --- |
| `git-auto-push/` | `Github/` (compare to G2 github/scripts first) |

### 2.9 Data / database

| G1 | Destination |
| --- | --- |
| `database/` | Policy → Ecosystem `2 - RootRecord-Database` / WO-DATA — **not** G3 code tree |

### 2.10 Products (usually not G3 server runtime)

| G1 tops | Prefer |
| --- | --- |
| `rootmc-android/`, `minecraft/`, `goals/`, `advertising/`, `finance-desk/`, `websites/`, `clients/` | Product repos / Website / Library — not Pacific server core |

### 2.11 Archive-only (do not put in G3 runtime)

| G1 tops | Prefer |
| --- | --- |
| `origin/` (~4k paths) | External archive or Library `Documentation/archive/` decision |
| `ecosystem-history/` | Library archive |
| `history/`, `holding/`, `remaining-tasks/` | Ops archive |

---

## 3. Gaps: what G2 has that G1 may not

Live residual jobs depend on G2 paths that are **not** top-level G1 names:

| G2 residual | In G1? |
| --- | --- |
| `a-eyes/` | **No** top-level — cameras evolved later |
| `automations/` poller stack | **No** — G3 Automations is the modern engine |
| `github/scripts/repos.conf` modern catalog | Compare `git-auto-push` only |
| `plumbing/` ollama/flm | Partial cousins (`ollama-*` packets) — map carefully |
| `system-stats/` | Closest: `host-metrics` |

Therefore: **G1 cannot replace G2 for current jobs.** G1 is supplemental history.

---

## 4. Staged recovery procedure (when authorized)

For each packet:

1. Confirm G2 domain for that capability is imported or waived.  
2. List G1 packet files; strip secrets.  
3. Diff against G2/G3.  
4. Copy only unique useful scripts into the G3 domain folder.  
5. Update `jobs.py` only if a job should call the recovered script.  
6. Document in Library (session note or WO).  
7. One domain at a time; reload stack after path changes.  

---

## 5. Related docs

| Doc | Role |
| --- | --- |
| [Migration-Lineage-Three-Generations-2026-09-28.md](./Migration-Lineage-Three-Generations-2026-09-28.md) | Order of operations |
| [Pacific-Jobs-Path-Inventory-2026-09-28.md](./Pacific-Jobs-Path-Inventory-2026-09-28.md) | G2 residual job paths |
| [Pacific-Server-Library-Dependency-Map-2026-09-28.md](./Pacific-Server-Library-Dependency-Map-2026-09-28.md) | G3/Library status |
| WO-SRV / WO-ECO | Cutover work orders |

---

*Inventory derived from GitHub tree listing of Solar-Pacific-RootRecord-Server-Old main, 2026-09-28 HST. Path counts approximate.*
