# WORK ORDER — Weekly Operations Log Archive

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-ARCH-2026-09-27 |
| **Date** | 2026-09-27 (HST) |
| **Status** | OPEN — Spec ready for automation |
| **Owner** | RootRecord |
| **Related** | `Documentation/01-operations/templates/README.md` |

**Scope:** Implement a weekly archive pass so active worklog and work-order folders stay uncluttered. Move closed material only; never rewrite content; never touch templates or OPEN work orders.

---

## 1. Intent

Operator logs will grow daily. Templates and naming are standing. Archive weekly under `YYYY-Www` so humans and agents always see a thin active set.

---

## 2. Current reality

### 2.1 What exists

| Item | Location / status |
| --- | --- |
| Active logs | `Documentation/01-operations/0 - Human Operator Work Logs/` |
| Templates | `Documentation/01-operations/templates/` |
| Active WOs | `Documentation/06-development/Work-Orders/` |
| Archive dirs | Not yet created (create on first pass) |

### 2.2 Completed so far

- [x] Filename convention and templates documented
- [x] Archive rules written in templates README
- [ ] Create archive folder structure
- [ ] Automation or scripted weekly job
- [ ] First successful archive week

### 2.3 Known friction

- Must not archive OPEN work orders
- Must not move templates
- Library sync must pick up moves cleanly (git mv preferred)

---

## 3. Tasks

1. Create `Documentation/01-operations/archive/` and `Documentation/06-development/archive/`.
2. Define “older than current calendar week (HST)” precisely in the script.
3. Move closed sessions, checkpoints, event logs → `01-operations/archive/YYYY-Www/`.
4. Move closed work orders only → `06-development/archive/YYYY-Www/`.
5. Commit via Library git / normal `library` sync.
6. Optional: schedule from poller or a weekly ON_AT job once proven manual.

---

## 4. Non-goals

- Deleting historical logs
- Rewriting or compressing log content
- Archiving OPEN WOs or templates

---

## 5. Key file / path reference

| Path | Role |
| --- | --- |
| `Documentation/01-operations/templates/README.md` | Rules |
| `Documentation/01-operations/archive/YYYY-Www/` | Log archive |
| `Documentation/06-development/archive/YYYY-Www/` | Closed WO archive |

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

*Work order prepared 2026-09-27 HST. Update status when closed.*
