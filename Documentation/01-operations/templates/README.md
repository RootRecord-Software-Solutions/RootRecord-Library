# Operations templates

Standing templates for RootRecord operator logs and work orders. Match the live style used in Session 01–03, checkpoints, and WO-ECO / WO-AEYES.

Automation may copy a template, replace `{{PLACEHOLDERS}}`, and write under the paths below. Humans may do the same.

---

## Templates

| Template | Use for | Output path |
| --- | --- | --- |
| [TEMPLATE System Operator Worklog — Session.md](./TEMPLATE%20System%20Operator%20Worklog%20%E2%80%94%20Session.md) | Daily / session narrative + timetable | `../0 - Human Operator Work Logs/{{YYYY-MM-DD}} System Operator Worklog — Session {{NN}}.md` |
| [TEMPLATE RootRecord Checkpoint.md](./TEMPLATE%20RootRecord%20Checkpoint.md) | Point-in-time verified state | `../0 - Human Operator Work Logs/{{YYYY-MM-DD}} RootRecord Checkpoint — {{HH_MM}} HST.md` |
| [TEMPLATE Event Action Log.md](./TEMPLATE%20Event%20Action%20Log.md) | Reinstall, incident, one-shot recovery day | `../0 - Human Operator Work Logs/{{YYYY-MM-DD}} {{Event Title}}.md` |
| [TEMPLATE Work Order.md](./TEMPLATE%20Work%20Order.md) | Scoped implementation / migration work | `../../06-development/Work-Orders/{{Name}}_Work_Order_WO-{{CODE}}-{{YYYY-MM-DD}}.md` |

---

## Placeholder rules

- `{{YYYY-MM-DD}}` — ISO date, HST calendar day of the work
- `{{HH:MM}}` — 24h HST clock; use `~` only when approximate
- `{{HH_MM}}` — same time for **filenames** (underscore, no colon)
- `{{SESSION_NN}}` — zero-padded session number for that day or series (`01`, `02`, …)
- Leave checkboxes as `- [ ]` / `- [x]`
- Never write tokens, passwords, or full secret file contents into logs

---

## Filename convention (standing)

```text
YYYY-MM-DD System Operator Worklog — Session NN.md
YYYY-MM-DD RootRecord Checkpoint — HH_MM HST.md
YYYY-MM-DD System Reinstall Action Log.md
YYYY-MM-DD <Event Title>.md
```

Work orders:

```text
<Short_Name>_Work_Order_WO-<CODE>-YYYY-MM-DD.md
```

---

## Archive rules

### Human operator logs (weekly)

Keep `0 - Human Operator Work Logs/` thin:

1. Identify closed sessions, checkpoints, and event logs **older than the current calendar week** (HST).
2. Move (do not rewrite) into:

```text
Documentation/01-operations/archive/YYYY-Www/
```

Example: `archive/2026-W39/` for week 39 of 2026.

3. Leave `templates/` in place.
4. Commit via normal Library sync (`library` / `github_sync_all`). No force-push.

### Completed work orders (standing folder)

When a WO is fully **COMPLETE** / **CLOSED** (no open phases):

```text
git mv Documentation/06-development/Work-Orders/<file>.md \
       Documentation/06-development/Work-Orders/Complete/
```

See [`Work-Orders/Complete/README.md`](../../06-development/Work-Orders/Complete/README.md). Do **not** put closed WOs under weekly `YYYY-Www` trees.

---

## Style notes (keep stable)

- Tables for timetable, status matrices, path maps
- Short **Purpose** / **Scope** at top
- Checklists for completed work
- Explicit **non-goals** and **deferred** sections
- One-line **Status** at close
- HST only unless the operator states another timezone
- Prefer structure over essay length for anything automation will fill daily
