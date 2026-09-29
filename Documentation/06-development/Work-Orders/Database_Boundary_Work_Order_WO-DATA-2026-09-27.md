# WORK ORDER — Database Boundary & Publication Policy

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-DATA-2026-09-27 |
| **Date** | 2026-09-27 (HST) |
| **Status** | **IN PROGRESS** — canonical Database root standardized in active Pacific source; historical `/home/rootrecord/Database/` references remain only where explicitly preserved as historical/operator evidence. Poller source has now been corrected to the canonical root; remaining runtime confirmation is tracked in WO-SRV. |
| **Owner** | RootRecord |
| **Related** | WO-ECO; RootRecord-Weather-Database |

**Scope:** Make explicit what lives in `2 - RootRecord-Database` (local generated data), what may publish to GitHub (e.g. weather), and what must never enter Library or runtime git trees.

---

## 1. Intent

Ecosystem tree separates generated data from knowledge and code. Weather already publishes via RootRecord-Weather-Database. Other Database subtrees (Energy, System, Media, Users, Logs, Geology) need a clear local-only vs publish policy so migration does not accidentally git large binaries or PII.

---

## 2. Current reality

### 2.1 What exists

| Item | Location / status |
| --- | --- |
| Canonical Database tree | `/home/rootrecord/RootRecord-Ecosystem/2 - RootRecord-Database/` |
| Legacy desk root | `/home/rootrecord/Database/` (historical/runtime evidence only; not the active source boundary) |
| Weather GitHub | `rootrecordsoftwaresolutions/RootRecord-Weather-Database` |
| Library | Must not hold generated telemetry dumps |

### 2.2 Completed so far

- [x] Boundary stated in WO-ECO (generated → Database)
- [x] Weather publication path exists
- [x] Active Pacific source paths standardized on the canonical Ecosystem Database root
- [x] Database `.gitignore` now excludes generated/binary image, audio, video, and icon media
- [ ] Map each Database subtree to local-only / publish / archive-drive
- [ ] Confirm sync size guards remain correct

### 2.3 Known friction

- Historical evidence and older desk tooling still contain `/home/rootrecord/Database/` references; these must be treated as historical/operator paths unless separately verified as active.
- Media/timelapses can exceed git-friendly sizes; generated binary media is now gitignored in the Database repo.

---

## 3. Tasks

1. Inventory subtrees: Energy, Geology, Github, Logs, Media, System, Users, Weather.
2. Label each: local-only, publish-git, external-archive.
3. Document relationship between Ecosystem Database folder and `/home/rootrecord/Database`.
4. Ensure runtime `.gitignore` and sync size guards remain correct.
5. Record policy in Master-Prompt map (short) and optional Library data doc.

---

## 4. Non-goals

- Redesigning weather pipeline in this WO
- Importing 25 GB historical corpus into Database git

---

## 5. Key file / path reference

| Path | Role |
| --- | --- |
| `/home/rootrecord/RootRecord-Ecosystem/2 - RootRecord-Database/` | Canonical Ecosystem data home |
| `/home/rootrecord/Database/` | Legacy/historical desk root; not the active Pacific source boundary |
| Weather-Database repo | Published weather |
| `MAX_FILE_MB` in github scripts | Sync size guard |

---

## 6. Open items

**Additional requirements:**

- Users/PII retention rules
- Media retention vs timelapse masters

---

## 7. Notes & constraints

- No force-push.
- Secrets stay out of git.
- Prefer small reversible steps.
- Generated data is not documentation; Library is not a dump target.

---

*Work order prepared 2026-09-27 HST. Update status when closed.*
