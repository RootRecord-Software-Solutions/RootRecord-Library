# Pacific Domain Import Playbook

| Field | Value |
| --- | --- |
| **Date** | 2026-09-28 (HST) |
| **Applies to** | G2 → G3 imports; then selective G1 recovery |
| **Live runtime** | `RootRecord-Pacific-Solar-Server` on Ecosystem `1 - Servers/` |
| **Updated** | 2026-09-28 ~17:00 HST — Geology ownership |

---

## Standing rules (always)

### 1. One domain folder — the name the tree already uses

Pacific domains are the **capitalized** folders already in the repo:

```text
Automations/  Communications/  Energy/  System/  Weather/
Github/  Geology/  Security/  Logs/
```

**Do not** create a second parallel folder or symlink just to match a legacy Python package name (e.g. no `energy` → `Energy` symlink).

| Wrong | Right |
| --- | --- |
| `Energy/` **and** `energy/` (symlink) | Only `Energy/` |
| Import package `energy` via fake path | Import package **`Energy`** (matches folder) |
| Top-level `Kilauea/` or `Earthquakes/` for runtime | **`Geology/`** with optional subfolders |
| Leave G2 lowercase names on disk in G3 | Rename/adapt to the G3 domain folder name |

### 2. Python packages match the domain folder

When G2 code used `import energy…` because the skill path was `skills/energy/`:

1. Copy into **`Energy/`** (existing domain shell).
2. Rewrite imports: `energy` → `Energy` (same for any future domain).
3. Set launcher `PYTHONPATH` to **Pacific repo root** (+ vendor as needed) so `import Energy…` resolves.
4. **Never** add a lowercase sibling symlink for import convenience.

Same pattern for future domains: folder name is the package name (e.g. `System`, `Weather`, **`Geology`**).

### 3. Paths with spaces

Ecosystem path contains `1 - Servers`. **Always double-quote** absolute paths in `jobs.py`, systemd `ExecStart`, and shell wrappers.

### 4. No old desk as runtime host

- systemd `ExecStart` → Pacific only
- After a domain is LIVE, jobs must not point at `~/.ollama/skills/…`
- G2 remains copy-source / archive — not the live host

### 5. Data stays in Database

Code in Pacific domain folders. Bytes under `/home/rootrecord/Database/…`.

### 6. Geology owns volcano + earthquakes

**`Geology/`** is the home for **Kīlauea** and **all earthquake functions** (Hawaiʻi-local and global). Details: [Geology-Domain-Ownership-Kilauea-Earthquakes-2026-09-28.md](./Geology-Domain-Ownership-Kilauea-Earthquakes-2026-09-28.md).

---

## Phase 0 — Preconditions

- [x] G3 repo under org; domain shells exist
- [x] Automations + poller live on Pacific
- [x] Energy Phase 1 LIVE; System Phase 1 LIVE
- [x] Geology ownership documented (import when source ready)

---

## Phase 1 — Import one G2 domain (template)

(Same steps as before: identify → inventory → copy into **existing** domain folder only → adapt imports → rewire jobs → deploy → verify → document.)

Domain name **must** match existing Pacific folder (`Energy`, `System`, `Geology`, …).

---

## Phase 2 — Remaining work

1. ~~Energy~~ ~~System~~
2. worklog / Github / plumbing (operator pick)
3. Telegram → A-Eyes → Weather
4. **Geology** — import Kīlauea + earthquake scripts from G1/G2 when ready
5. Energy actions (Phase 2)
6. Zero skills paths in jobs.py

---

## Phase 3 — Selective G1 recovery

G1 `kilauea/*` and `earthquakes` packets → **`Geology/`** only (not Weather root, not new top-level domains).

---

## Phase 4 — Catalog & Master-Prompt

- `repos.conf` → Ecosystem paths (WO-GH)
- Master-Prompt map includes Geology ownership (WO-MAP)

---

## Rollback

Revert domain commits; fix package names rather than re-adding lowercase symlinks.

---

*Playbook 2026-09-28 HST.*
