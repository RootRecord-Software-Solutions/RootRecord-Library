# Workflow — Bruce Monitor

## Standard Development Loop

1. **Inspect** the real current file or path
2. **Trace** the actual flow involved
3. **Patch** the existing final path (surgical)
4. **Validate** the changed behavior
5. **Independently double-check** the result
6. **Hand off** with concise evidence

Do not stop after writing a file and call it fixed.

## Preferred Change Style
- Reuse existing files, services, and paths
- Prefer the smallest change that fits the current architecture
- Do not create parallel `v2` directories, alternate roots, or competing installers unless explicitly requested

## Deploy Path (standing rule)

| Step | Action |
|------|--------|
| 1 | Change lands on GitHub `main` |
| 2 | Desk `github_sync_all` (~300s) fetch/merge (no force-push, no hard reset) |
| 3 | Skills merge arms reload + schedules stack reload |
| 4 | Full stop of poller stack → start unit → reopen status window |
| 5 | New code runs |

Do **not**:
- Recommend manual poller restarts after ordinary pushes
- Start a second poller / tunnel / BLE owner
- Invent a competing deploy path

## File Layout Style
Operator-facing schedules and catalogs must remain **sectioned and templated**.

Canonical reference: `automations/scripts/jobs.py`

- `# SECTION:` banners
- Commented **TEMPLATE** blocks at the end of each section
- Header explaining how to add a job
- New live jobs go **above** the TEMPLATE

If a file that should follow this style has been compacted, restore the layout.

## Handoffs
Use the format in [HANDOFF-TEMPLATE.md](HANDOFF-TEMPLATE.md).

Every handoff should make the next agent (or the operator) clearer than when you started.
