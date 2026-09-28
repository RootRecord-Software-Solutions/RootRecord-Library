# {{EVENT_TITLE}}

**Date:** {{YYYY-MM-DD}}  
**Scope:** {{one-line scope}}  
**Timezone:** HST  
**Status:** {{IN PROGRESS | CLOSED}}

---

## Timeline

{{HH:MM}} — {{Event}}

{{HH:MM}} — {{Event}}

~{{HH:MM}} — {{Estimated event}}

{{HH:MM}} — {{Event}}

---

## Outcomes

- {{Outcome}}
- {{Outcome}}

---

## Artifacts / paths

| Path or artifact | Role |
| --- | --- |
| {{path}} | {{role}} |

---

## Notes

- Entries marked `~` are approximate.
- Confirmed operator times are preserved as stated.
- Do not expose secrets, tokens, or full credential values in this log.

---

## Close

**Closed:** {{YYYY-MM-DD}} {{HH:MM}} HST  
**Status:** {{One-line close status}}

---

## Archive note

Filename when saved:

```text
{{YYYY-MM-DD}} {{EVENT_TITLE}}.md
```

Examples:

```text
2026-09-26 System Reinstall Action Log.md
2026-09-27 Cloudflare Tunnel Recovery Log.md
```

Weekly archive: move closed event logs older than the current week into `Documentation/01-operations/archive/` without rewriting content.
