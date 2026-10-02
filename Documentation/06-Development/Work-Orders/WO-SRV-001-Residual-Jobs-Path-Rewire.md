# WO-SRV-001 — Residual Jobs Path Rewire

| Field | Value |
|-------|--------|
| **Priority** | P0 |
| **Status** | Draft — path check 2026-09-29 22:24 HST: `jobs.py` has no `~/.ollama/skills/` job path, and all 30 script paths in that file exist on disk. Not closed. The old→new session log is not assembled, and this draft is not the place to edit `jobs.py`. Energy actuation stays on WO-ECO-001. |
| **Target** | `RootRecord-Pacific-Solar-Server/Automations/scripts/jobs.py` |
| **Depends on** | Energy source first; then Geology/Weather/Github as imported |
| **Related** | Pacific-Jobs-Path-Inventory; Private-Repos-Feature-Map |

## Goal

Eliminate every residual absolute / G2 skill path in the poller job catalog so each scheduled job resolves only under Pacific domain folders (`Energy/`, `Weather/`, `Geology/`, `Github/`, `Communications/`, `System/`, etc.).

## Current known residuals (document-only inventory)

From live `jobs.py` and prior path inventory notes:

| Domain / skill | Typical residual pattern | Target after import |
|----------------|--------------------------|---------------------|
| Energy / EcoFlow | `~/.ollama/skills/energy/...` or absolute desk paths | `Energy/scripts/...` |
| A-Eyes / vision | skill tree under ollama | Out of scope until operator decides |
| Github pull | skill or Core-Processor timer path | `Github/` or keep Core-Processor as authority |
| Weather / NWS | partial under `Weather/` | Complete under `Weather/scripts/` |
| Kīlauea / geology | partial under `Geology/` | Complete under `Geology/scripts/` |
| Telegram / plumbing | communications skill paths | `Communications/` |

Exact line-level list should be re-diffed against current `jobs.py` at execution time (do not hardcode stale lines here).

## Scope (in)

- After each domain import lands, update only that domain’s job entries
- Prefer `REPO_ROOT` / relative resolution already used by poller engine
- Document retired residual paths in the domain README and this WO’s completion notes
- Keep job names stable where possible so logs stay comparable

## Scope (out)

- Changing poller engine scheduling logic
- Importing new domains in this WO (imports are separate WOs)
- Enabling jobs that have no source yet (leave disabled or commented with note)
- RootMC desktop paths

## Acceptance criteria

1. `jobs.py` contains zero references to `~/.ollama/skills/` for domains that have been imported
2. Each active job’s script path exists on disk under Pacific repo layout
3. One full poller cycle succeeds for rewritten jobs without path errors
4. Session log lists every path change (old → new)

## Suggested steps

1. Complete WO-ECO-001
2. Grep `jobs.py` for residual patterns; patch Energy block only
3. Live cycle verify
4. Repeat per domain in import order: Weather → Geology → Github (policy) → Communications extras
5. Final grep clean + close WO

## Risks

- Leaving a job enabled with a missing script (poller noise / FAIL codes)
- Dual writers if Core-Ops hybrid and Pacific Energy both schedule the same report
- Accidental enable of A-Eyes without hardware/policy approval

## Notes

This WO is a **wiring pass**, not a feature build. Execute only after sources exist under domain folders.
