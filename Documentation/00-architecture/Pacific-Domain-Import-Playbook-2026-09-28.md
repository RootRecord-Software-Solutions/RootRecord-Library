# Pacific Domain Import Playbook

| Field | Value |
| --- | --- |
| **Date** | 2026-09-28 (HST) |
| **Applies to** | G2 → G3 imports; then selective G1 recovery |
| **Live runtime** | `RootRecord-Pacific-Solar-Server` on Ecosystem `1 - Servers/` |
| **Updated** | 2026-09-28 ~16:56 HST — domain naming SOP |

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
| Leave G2 lowercase names on disk in G3 | Rename/adapt to the G3 domain folder name |

### 2. Python packages match the domain folder

When G2 code used `import energy…` because the skill path was `skills/energy/`:

1. Copy into **`Energy/`** (existing domain shell).
2. Rewrite imports: `energy` → `Energy` (same for any future domain).
3. Set launcher `PYTHONPATH` to **Pacific repo root** (+ vendor as needed) so `import Energy…` resolves.
4. **Never** add a lowercase sibling symlink for import convenience.

Same pattern for future domains: folder name is the package name (e.g. `System`, `Weather`).

### 3. Paths with spaces

Ecosystem path contains `1 - Servers`. **Always double-quote** absolute paths in:

- `jobs.py` command strings
- systemd `ExecStart`
- shell wrappers

### 4. No old desk as runtime host

- systemd `ExecStart` → Pacific only
- After a domain is LIVE, jobs for that domain must not point at `~/.ollama/skills/…`
- G2 remains copy-source / archive until the operator removes it — not the live host

### 5. Data stays in Database

Code in Pacific domain folders. Bytes (logs, samples, ENERGY sqlite, frames) under `/home/rootrecord/Database/…`.

---

## Phase 0 — Preconditions

- [x] G3 repo under org
- [x] Domain folder shells exist (use those names — do not invent parallel ones)
- [x] Automations core + poller live on Pacific
- [x] Energy Phase 1 LIVE; System Phase 1 LIVE
- [ ] Operator source tree for the domain being imported

---

## Phase 1 — Import one G2 domain (template)

### Step 1.1 — Identify

| Field | Fill in |
| --- | --- |
| Domain name | **Must match existing Pacific folder** (e.g. `Energy`, not `energy`) |
| G2 source path | e.g. `~/.ollama/skills/energy/` |
| G3 destination | e.g. `Energy/` only |
| jobs.py ids | e.g. ecoflow_read_cycle |
| Data dirs (off-git) | e.g. Database/ENERGY |

### Step 1.2 — Inventory source

- Scripts, configs, SKILL.md
- Secrets (never commit)
- Absolute paths inside scripts
- Python `import <pkg>` names — plan rewrite to **domain folder name**

### Step 1.3 — Copy into G3

- Into the **existing** domain folder only
- Preserve useful structure (`scripts/`, `lib/`, `db/`)
- **No** lowercase duplicate dir/symlink for package hacks
- Update domain README
- `.gitignore` secrets/stores

### Step 1.4 — Adapt Python / shell

- Rewrite `import oldname` → `import DomainFolderName`
- Launcher: `PYTHONPATH=vendor:Pacific_root` (or domain-local if top-level modules)
- Quote all Pacific absolute paths

### Step 1.5 — Rewire jobs.py

- `command` + `cwd` → Ecosystem Pacific paths (quoted)
- Commit with or right after domain files

### Step 1.6 — Deploy

```text
push → pull on desk → schedule-stack-reload / systemctl --user restart rr-rootserver-poller
```

### Step 1.7 — Verify

- Poller: job uses Pacific path (not skills)
- Domain signals OK
- Tree shows **one** domain folder for that capability

### Step 1.8 — Document

- Domain README status LIVE
- WO-SRV residual row cleared for that domain

---

## Phase 2 — Remaining G2 domains

Recommended order (Energy + System done):

1. ~~Energy~~ ~~System~~
2. worklog (reports) **or** Github **or** plumbing
3. Telegram (Communications)
4. A-Eyes
5. Weather (re-enable when present)
6. Energy actions (Phase 2)

---

## Phase 3 — Selective G1 recovery

Only after matching G2→G3 for that capability. Never bulk-merge Old into G3. Same **one folder name** rule.

---

## Phase 4 — Catalog & Master-Prompt

- `repos.conf` → Ecosystem paths (WO-GH)
- Master-Prompt map (WO-MAP)
- Zero skills paths in jobs.py

---

## Rollback

- Revert domain commits; restore jobs to G2 only if emergency
- G2 on disk remains safety net until operator deletes it
- Do **not** “fix” imports by re-adding lowercase symlinks — fix package names instead

---

*Playbook 2026-09-28 HST. Domain naming SOP added same day.*
