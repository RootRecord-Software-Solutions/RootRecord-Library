# WORK ORDER — GitHub Catalog Hygiene & Non-Canonical Cleanup

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-GH-2026-09-27 |
| **Date** | 2026-09-27 (HST) |
| **Status** | OPEN |
| **Owner** | RootRecord |
| **Related** | WO-ECO; Session 03; `github/scripts/repos.conf` |

**Scope:** Keep `repos.conf` and GitHub org/user repos aligned with reality. Remove or archive the mistaken user-account Library repo; document org placement rules for future repos.

---

## 1. Intent

During Library bring-up, a repo was created under `rootrecordsoftwaresolutions/RootRecord-Library` before the canonical org home was confirmed. Canonical is `RootRecord-Software-Solutions/RootRecord-Library`. Catalog and remote hygiene prevent agents from pushing to the wrong home again.

---

## 2. Current reality

### 2.1 What exists

| Item | Location / status |
| --- | --- |
| Canonical Library | `RootRecord-Software-Solutions/RootRecord-Library` |
| Non-canonical | `rootrecordsoftwaresolutions/RootRecord-Library` (delete when convenient) |
| Catalog | `~/.ollama/skills/github/scripts/repos.conf` — library row points at org |
| Sync cycle | `github_sync_all` ~300s |

### 2.2 Completed so far

- [x] `repos.conf` library slug corrected to org
- [x] Desk remote retargeted; sync clean
- [ ] Delete non-canonical GitHub repo (UI or API)
- [ ] Standing rule: knowledge repos → `RootRecord-Software-Solutions` unless explicitly otherwise
- [ ] Process for adding new rows (template already in repos.conf)

### 2.3 Known friction

- Multiple GitHub identities/orgs in play
- New repos must choose org before first push

---

## 3. Tasks

1. Confirm no desk remote still points at non-canonical Library.
2. Delete `rootrecordsoftwaresolutions/RootRecord-Library` if empty/superseded.
3. Document org choice in WO-MAP / Master-Prompt when written.
4. For each new repo: create under correct org **without** auto-README if local history exists; add `repos.conf` row; `setup-remote`; first push.
5. Keep `jobs.py` descriptions in sync with enabled catalog ids.

---

## 4. Non-goals

- Migrating Weather-Database or Website between orgs in this WO
- Changing sync interval or merge safety rules

---

## 5. Key file / path reference

| Path | Role |
| --- | --- |
| `github/scripts/repos.conf` | Catalog |
| `github/scripts/setup-remote.sh` | Tokenized remote |
| `github/scripts/push-repo-once.sh` | Safe sync |
| `automations/scripts/jobs.py` | github_sync_all / setup-remotes |

---

## 6. Open items

**Additional requirements:**

- Org policy for future product vs infrastructure repos
- 

---

## 7. Notes & constraints

- No force-push.
- Secrets stay out of git.
- Prefer small reversible steps.
- Never init remote with README when local root commit already exists (avoids unrelated histories).

---

*Work order prepared 2026-09-27 HST. Update status when closed.*
