# WORK ORDER — GitHub Catalog Hygiene & Non-Canonical Cleanup

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-GH-2026-09-27 |
| **Date** | 2026-09-27 (HST) |
| **Status** | OPEN |
| **Owner** | RootRecord |
| **Related** | WO-ECO; WO-SRV; Session 03; `repos.conf` |
| **Updated** | 2026-09-28 (HST) |

**Scope:** Keep `repos.conf` and GitHub org/user repos aligned with reality. Remove or archive the mistaken user-account Library repo; document org placement rules for future repos; align Pacific runtime catalog row with Ecosystem path when ready.

---

## 1. Intent

During Library bring-up, a repo was created under `rootrecordsoftwaresolutions/RootRecord-Library` before the canonical org home was confirmed. Canonical is `RootRecord-Software-Solutions/RootRecord-Library`. Pacific runtime is now also under the org as `RootRecord-Pacific-Solar-Server`.

---

## 2. Current reality (2026-09-28)

### 2.1 What exists

| Item | Location / status |
| --- | --- |
| Canonical Library | `RootRecord-Software-Solutions/RootRecord-Library` |
| Canonical Pacific runtime | `RootRecord-Software-Solutions/RootRecord-Pacific-Solar-Server` |
| Non-canonical Library | `rootrecordsoftwaresolutions/RootRecord-Library` (delete when convenient) |
| **Historical** Pacific remote | `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server` (superseded) |
| Catalog | Often still under legacy `…/github/scripts/repos.conf` until github domain is imported into Pacific tree |
| Live Pacific path | `…/1 - Servers/1 - RootRecord-Pacific-Solar-Server` |
| Sync cycle | `github_sync_all` ~300s (job still may reference legacy skills path) |

### 2.2 Completed so far

- [x] `repos.conf` library slug corrected to org
- [x] Desk remote retargeted; sync clean
- [x] Pacific org repo online; runtime under Ecosystem Servers
- [ ] Delete non-canonical GitHub Library repo (UI or API)
- [ ] Align pacific/skills `repos.conf` local_path to Ecosystem Servers path
- [ ] Standing rule: knowledge + Pacific runtime → `RootRecord-Software-Solutions` unless explicitly otherwise
- [ ] Process for adding new rows documented in WO-MAP

### 2.3 Known friction

- Multiple GitHub identities/orgs in play
- Catalog scripts may still live under legacy skills tree until **Github** domain import
- **Historical path:** `automations/scripts/jobs.py` → now `Automations/scripts/jobs.py` on Pacific repo

---

## 3. Tasks

1. Confirm no desk remote still points at non-canonical Library.
2. Delete `rootrecordsoftwaresolutions/RootRecord-Library` if empty/superseded.
3. Update `repos.conf` pacific/skills row: local_path → Ecosystem Servers path; slug → org Pacific repo.
4. Document org choice in WO-MAP / Master-Prompt when written.
5. Keep `Automations/scripts/jobs.py` descriptions in sync with enabled catalog ids.

---

## 4. Non-goals

- Migrating Weather-Database or Website between orgs in this WO
- Changing sync interval or merge safety rules
- Moving github scripts into Pacific repo (separate domain import)

---

## 5. Key file / path reference

| Path | Role |
| --- | --- |
| `repos.conf` (catalog) | Source of truth for sync ids |
| `setup-remote.sh` / `push-repo-once.sh` | Safe sync (legacy location until Github domain import) |
| `Automations/scripts/jobs.py` | github_sync_all / setup-remotes job text |
| **Historical:** `~/.ollama/skills/github/scripts/` | Prior catalog home |

---

## 6. Notes & constraints

- No force-push.
- Secrets stay out of git.
- Prefer small reversible steps.
- Never init remote with README when local root commit already exists.

---

*Work order prepared 2026-09-27 HST. Updated 2026-09-28 HST for Pacific org runtime.*
