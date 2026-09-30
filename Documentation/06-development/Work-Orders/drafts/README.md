# Work-Orders / drafts

**Draft-only home** for work orders that are **not** on the active index yet.

| Field | Value |
| --- | --- |
| **Date** | 2026-09-28 (HST) |
| **Authority** | Library Work-Orders rules + Carly WO structure (Agent Context) |
| **Related** | [WO-WOGEN-001](../WO-WOGEN-001-Work-Order-Generator.md); [TEMPLATE Work Order](../../../01-operations/templates/TEMPLATE%20Work%20Order.md) |

---

## Purpose

- **Carly** (or operator) structured drafts before promotion  
- **WO-WOGEN-001** generator output (when accepted and implemented)  
- Anything with `Status: DRAFT` that must not clutter the active backlog table  

## Desk fact (2026-09-30)

`3 - RootRecord-Website` is gone. Do not recreate that folder, and do not start a local site on port 3001. Drafts that still name that checkout are describing the desk as it was when they were written. Promote one only when Alexander asks, and retarget it before any build.

## Hard rules

1. **Never auto-promote** a file from `drafts/` into the active index README.  
2. **Never** set COMPLETE / CLOSED / LIVE from a generator.  
3. **No secrets** in draft bodies (tokens, env values, private URLs with credentials).  
4. Prefer measured evidence blocks; use **Unknown / No data** when thin.  
5. Promotion = human (operator) decision: move/edit into parent `Work-Orders/`, set Status OPEN/IN PROGRESS, and add a row to the index.  
6. Rejection or stale drafts may be deleted or moved with a short note — do not leave contradictory “done” claims.  

## Filename suggestions

```text
DRAFT_WO-AUTO-YYYY-MM-DD-short-slug.md     # generator
DRAFT_WO-CARLY-YYYY-MM-DD-short-slug.md    # Carly structured draft
DRAFT_WO-AVA-YYYY-MM-DD-short-slug.md      # architecture draft if needed
```

## Empty is fine

This folder may contain only this README until the first sealed draft or generator dry-run.

---

*Created 2026-09-28 HST with WO-WOGEN-001. Docs only.*
