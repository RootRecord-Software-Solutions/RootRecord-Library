# WORK ORDER — Weekly Operations Log Archive

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-ARCH-2026-09-27 |
| **Date** | 2026-09-27 (HST) |
| **Status** | **COMPLETE** — signed off 2026-09-29 ~21:49 HST. First week `2026-W40`, cutoff `2026-09-28` (Monday of the current HST week). Moved 5 logs dated 2026-09-26 and 2026-09-27 into `Documentation/01-operations/archive/2026-W40/`. Seven current-week logs stayed active. |
| **Owner** | RootRecord |
| **Related** | `Documentation/01-operations/templates/README.md`; [WO-RPT-001](./WO-RPT-001-Reports-Worklog-Domain-Import.md); [Complete/](./Complete/) |

**Scope:** Implement a weekly archive pass so **human operator logs** stay uncluttered. Move closed log material only; never rewrite content; never touch templates or OPEN work orders.

**Closed work orders** do **not** use weekly folders — they go to [`Work-Orders/Complete/`](./Complete/) via `git mv` when the whole WO is done (standing operator convention 2026-09-28).

---

## 1. Intent

Operator logs will grow daily. Templates and naming are standing. Archive weekly under `YYYY-Www` so humans and agents always see a thin active set of **session / checkpoint / event** files.

**Implementation note (2026-09-28):** Script + schedule land under Pacific `Reports/` as WO-RPT-001 Phase D (after worklog path rewire soaks).

---

## 2. Current reality

### 2.1 What exists

| Item | Location / status |
| --- | --- |
| Active logs | `Documentation/01-operations/0 - Human Operator Work Logs/` |
| Templates | `Documentation/01-operations/templates/` |
| Active WOs | `Documentation/06-development/Work-Orders/` |
| **Completed WOs** | `Documentation/06-development/Work-Orders/Complete/` |
| Log archive dirs | Not yet created (create on first pass) |
| Worklog engine | Pacific `Reports/` (WO-RPT-001 Phase B LIVE) |

### 2.2 Completed so far

- [x] Filename convention and templates documented
- [x] Archive rules written in templates README
- [x] Linked to WO-RPT-001 Phase D
- [x] `Work-Orders/Complete/` standing home for closed WOs
- [x] Create `01-operations/archive/` folder structure (`archive/2026-W40/`, 2026-09-29)
- [x] Automation or scripted weekly job for **logs** (`reports_weekly_archive` at 19:00 HST)
- [x] First successful log-archive week (2026-09-29: 5 files, cutoff 2026-09-28)

### 2.3 Known friction

- Must not archive OPEN work orders into weekly log trees
- Must not move templates
- Library sync must pick up moves cleanly (git mv preferred)

---

## 3. Tasks

1. Create `Documentation/01-operations/archive/`.
2. Define “older than current calendar week (HST)” precisely in the script.
3. Move closed sessions, checkpoints, event logs → `01-operations/archive/YYYY-Www/`.
4. **Do not** weekly-archive WOs — closed WOs → `Work-Orders/Complete/` only.
5. Commit via Library git / normal `library` sync.
6. Optional: schedule from poller or a weekly ON_AT job once proven manual.

---

## 4. Non-goals

- Deleting historical logs
- Rewriting or compressing log content
- Archiving OPEN WOs or templates
- Moving completed WOs into `YYYY-Www` (use `Complete/` instead)

---

## 5. Key file / path reference

| Path | Role |
| --- | --- |
| `Documentation/01-operations/templates/README.md` | Rules |
| `Documentation/01-operations/archive/YYYY-Www/` | **Log** archive |
| `Documentation/06-development/Work-Orders/Complete/` | **Closed WO** archive |
| Pacific `Reports/scripts/` | Future weekly log archive script (Phase D) |

---

## 6. Open items

**Additional requirements:**

- Day-of-week for the pass (e.g. Sunday 19:00 HST)
- Whether checkpoints from “today” stay active even if week boundary is awkward

---

## 7. Notes & constraints

- No force-push.
- Secrets stay out of git.
- Prefer small reversible steps.
- Use `git mv` so history stays traceable.

---

*Work order prepared 2026-09-27 HST. Complete/ convention 2026-09-28.*
