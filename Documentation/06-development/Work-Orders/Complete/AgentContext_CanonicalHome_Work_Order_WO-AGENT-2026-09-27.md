# WORK ORDER — Agent Context Canonical Home

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-AGENT-2026-09-27 |
| **Date** | 2026-09-27 (HST) |
| **Status** | **COMPLETE** — signed off 2026-09-29 ~21:56 HST. Canonical home is Library `Agent Context/`. `Documentation/02-agents/` stays an index. Placeholder folders were not deleted. Personal `AvaIvy` and `CarlyMal` remotes stay separate. |
| **Owner** | RootRecord |
| **Related** | Session 01 worklog §10; Library Agent Context packs |

**Scope:** Resolve observed duplication between `Agent Context/` and `Documentation/02-agents/` for Ava, Bruce, and Carly. Decide one canonical home; document the other as mirror, stub, or remove only after comparison.

---

## 1. Intent

Session 01 recorded duplication as a **fact to investigate**, not permission to reorganize. With Library online and auto-synced, the decision should be explicit so agents and operators stop maintaining two spines by accident.

---

## 2. Current reality

### 2.1 What exists

| Item | Location / status |
| --- | --- |
| Full packs | `5 - RootRecord-Library/Agent Context/{Ava,Bruce,Carly}-Agent-Context/` |
| Parallel tree | `Documentation/02-agents/{Ava,Bruce,Carly}-Agent-Context/` |
| Pack spine | IDENTITY, PRINCIPLES, ROLE-AND-BOUNDS, WORKFLOW, HANDOFF-TEMPLATE, CONTEXT/*, CHANGELOG, README |
| Desk skills agents | `~/.ollama/skills/agents/` (runtime; separate concern) |

### 2.2 Completed so far

- [x] Packs present under Library `Agent Context/`
- [x] Duplication noted in Session 01
- [x] Diff both trees file-by-file (2026-09-29: 34 vs 5 files; shared names are four identical `.gitkeep` files)
- [x] Choose canonical home — `Agent Context/`; `02-agents/` is the index
- [x] Update REPOS / handoff docs to point at one path

### 2.3 Known friction

- Deleting without diff risks losing unique notes
- Runtime agents under skills may still reference different paths

---

## 3. Tasks

1. Diff `Agent Context/*` vs `Documentation/02-agents/*` (names, sizes, unique files).
2. Propose canonical home (recommended default: `Agent Context/` as identity packs; `02-agents/` as index or thin pointers).
3. Implement with reversible steps (pointers first, delete later).
4. Update any Master-Prompt / REPOS.md links.
5. Log decision in a short ADR or architecture note under Library.

---

## 4. Non-goals

- Redesigning agent personas in this WO
- Merging skills/`agents/` runtime into Library in the same change
- Mass history import

---

## 5. Key file / path reference

| Path | Role |
| --- | --- |
| `Agent Context/Ava-Agent-Context/` | Candidate canonical pack |
| `Documentation/02-agents/` | Observed duplicate tree |
| Agent `CONTEXT/REPOS.md` | Must point at ownership map |

---

## 6. Open items

**Additional requirements:**

- Personal GitHub mirrors (`AvaIvy`, `CarlyMal`) remain separate remotes. Recorded 2026-09-29. This desk does not sync them.

---

## 7. Notes & constraints

- No force-push.
- Secrets stay out of git.
- Prefer small reversible steps.
- Observed duplication is not automatic error — verify first.

---

*Work order prepared 2026-09-27 HST. Update status when closed.*
