# Geology Domain Ownership — Kīlauea & Earthquakes

| Field | Value |
| --- | --- |
| **Date** | 2026-09-28 (HST) |
| **Runtime home** | `RootRecord-Pacific-Solar-Server` → **`Geology/`** |
| **Desk path** | `…/1 - Servers/1 - RootRecord-Pacific-Solar-Server/Geology/` |
| **Status** | Ownership declared. **2026-09-29 ~13:20 HST:** first scripts imported (LANDED, manual PASS, jobs gated OFF) — see the status note at the end |

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

## Status note — 2026-09-29 ~13:40 HST

- **Imported (copy/port only; G1 `kilauea/*`, `earthquakes`, G0 `backfillquakes.py` KEPT unchanged):** `Geology/scripts/geology_collect.py` (USGS FDSN Hawaiʻi bbox 18.5–22.5 N / 160.5–154.5 W + `2.5_day` global feed; USGS HANS HVO status + notices), `kilauea_cams.py` (V1/V2/V3 stills), `earthquakes_backfill.py` (SQLite, on demand).
- **Layout used:** flat `Geology/scripts/` (the "Suggested layout" above stays a future option). Database: `Geology/Earthquakes/{hawaii,global}-last.json` + `Daily/*.jsonl`, `Geology/Volcanoes/{hvo,kilauea,mauna-loa}-last.json` + `Daily/hvo-notices-*.jsonl` + `Cams/`, `Geology/collector-last.json`. Event DB `quakes.db` and cam JPGs are git-ignored (rule 5).
- **Gates:** `RR_GEOLOGY=1` (300 s), `RR_KILAUEA_CAMS=1` (600 s), `RR_VOICE_QUAKE=1` (voice :08). All OFF until Alexander signs off and the poller restarts.
- **Council quake notices:** dry-run landed as Pacific `Communications/CouncilQuake/` (WO-MIG-25). Reads `hawaii-last.json`. Telegram send and Carly WAV stay off until sign-off.
- **Public draft queue:** landed 2026-09-30 as Pacific `Geology/PublicDraftQueue/` (WO-MIG-24). Reads `kilauea-last.json`. Job `geology_kilauea_public_draft` gated `RR_KILAUEA_DRAFT`. No send.
- **Not imported (BLOCKED / sign-off):** Discord posts, Grok drafts, OBS cam push, YouTube scraping, G0 nearest-location enrichment (needs a dataset).
- Records: [geology test](../07-testing/2026-09-29-geology-earthquakes-hvo-collector.md), [migration matrix](./Old-Repo-Migration-Matrix.md).
