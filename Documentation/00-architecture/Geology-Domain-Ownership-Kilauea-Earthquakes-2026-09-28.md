# Geology Domain Ownership — Kīlauea & Earthquakes

| Field | Value |
| --- | --- |
| **Date** | 2026-09-28 (HST) |
| **Runtime home** | `RootRecord-Pacific-Solar-Server` → **`Geology/`** |
| **Desk path** | `…/1 - Servers/1 - RootRecord-Pacific-Solar-Server/Geology/` |
| **Status** | Ownership declared; folder shell present; scripts not yet imported |

---

## Decision

**`Geology/` is the single Pacific domain** for:

1. **Kīlauea** — volcano observation, alert ingest, related desk tooling  
2. **Earthquakes — local** — Hawaiʻi / regional Pacific  
3. **Earthquakes — global** — worldwide catalog and significant-event functions  

No separate top-level Pacific folders for `Kilauea/` or `Earthquakes/` as runtime homes. Subfolders **inside** `Geology/` are encouraged for clarity.

This follows the standing domain naming SOP (one capitalized domain folder; no parallel lowercase symlink; package name matches folder when Python is used). See [Pacific-Domain-Import-Playbook-2026-09-28.md](./Pacific-Domain-Import-Playbook-2026-09-28.md).

---

## Authority split

| Layer | Role |
| --- | --- |
| **Pacific `Geology/`** | Code: scripts, pollers, lib, config, job entrypoints |
| **Database** | Bytes: event stores, snapshots, logs under operator-chosen `Database/…` trees |
| **Library** | Meaning: this ownership note, WOs, product context |
| **Product / Website repos** | Public-facing apps; must not replace desk runtime ownership |

---

## Adjacency

| Topic | Domain |
| --- | --- |
| General weather (non-volcano product ops) | `Weather/` |
| Cams purely for security / A-Eyes | `Security/` or A-Eyes domain |
| Volcano-specific weather hooks for Kīlauea ops | Prefer **`Geology/`** (or thin call into Weather helpers without moving ownership) |

---

## Migration when importing

1. Inventory G1 `kilauea/*`, `earthquakes` and any G2 skill paths.  
2. Copy into `Geology/` only (subfolders OK).  
3. Rewrite imports / paths; quote Pacific paths with spaces.  
4. Add `jobs.py` entries pointing at `Geology/…`.  
5. Data writes → Database; never commit measured event DBs to git.  
6. Mark residual inventory rows migrated; do not leave long-term runtime under `~/.ollama/skills`.

---

## Suggested layout (future)

```text
Geology/
  README.md
  scripts/
    kilauea/
    earthquakes/
      local/
      global/
  lib/
  config/
```

---

*Declared 2026-09-28 HST. Align Master-Prompt / WO-MAP when domain is imported.*
