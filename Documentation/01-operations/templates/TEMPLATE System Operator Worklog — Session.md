# System Operator Worklogs — Session {{SESSION_NN}}

**Date:** {{YYYY-MM-DD}}  
**Session:** {{SESSION_TITLE}}  
**Timezone:** HST  
**Window:** {{HH:MM}}–{{HH:MM}} HST  
**Status:** {{ACTIVE | CLOSED}}  
**Operator:** RootRecord

---

## Purpose

{{ONE_OR_TWO_SENTENCES — what this session is for}}

This is a manual operator worklog (not a full architecture redesign). Record what was actually done.

---

## Approximate timetable ({{YYYY-MM-DD}} HST)

| Time (approx.) | Event |
| --- | --- |
| {{HH:MM}} | {{Event}} |
| {{HH:MM}} | {{Event}} |
| {{HH:MM}} | {{Event}} |

---

## Completed this session

### {{AREA_1}}

- [ ] {{Item}}
- [ ] {{Item}}

### {{AREA_2}}

- [ ] {{Item}}
- [ ] {{Item}}

### Explicit non-goals

- {{Thing not authorized this session}}
- {{Thing deferred}}

---

## Blockers / residual items

| Item | Notes |
| --- | --- |
| {{Item}} | {{Status or next step}} |
| {{Item}} | {{Status or next step}} |

---

## Decisions (if any)

> {{Decision statement}}

Rationale: {{Brief why}}

---

## State at session close (~{{HH:MM}} HST)

- **Runtime:** {{poller / services summary}}
- **Library / docs:** {{what changed}}
- **GitHub / sync:** {{ok / issues}}
- **Next useful step:** {{single concrete next action}}

**Status:** {{One-line close status}}

---

## Archive note

Filename when saved:

```text
{{YYYY-MM-DD}} System Operator Worklog — Session {{SESSION_NN}}.md
```

Weekly archive: move closed sessions older than the current week into `Documentation/01-operations/archive/` (or dated weekly folder) without rewriting content.
