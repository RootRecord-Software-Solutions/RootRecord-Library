# WO-WOGEN-001 — Work Order Generator (Measured Friction → Draft WOs)

| Field | Value |
|-------|--------|
| **Priority** | P2 (after G3 runtime verification residual; does not block cutover) |
| **Status** | **Draft** — architecture only; not accepted for execution |
| **Date** | 2026-09-28 (HST) |
| **Target** | Pacific `Reports/` (or thin helper under Automations) + Library `Work-Orders/drafts/` |
| **Depends on** | WO-RPT-001 foundation LIVE; Carly WO structure rules (Agent Context 0.1.2+); operator accept before implement |
| **Related** | WO-RPT-001; WO-SYS-001; WO-SRV; Carly ROLE-AND-BOUNDS (WO drafts); TEMPLATE Work Order |

## Goal

Give agents a **git-visible trail of measured friction** (poller FAILs, repeated path errors, domain worklog bursts) as **draft work orders** — without inventing status, without auto-execution, and without reading secrets.

Operators and agents can then see arising issues in near-real time *as structured drafts*, not only as raw log tails on the desk.

## Ownership

| Role | Responsibility |
|------|----------------|
| **Carly** | WO template fidelity, honesty seal, draft-only rules, promotion gate |
| **Ava** | Input/output architecture, what may become a WO vs log-only |
| **Bruce** | Implementation (script, paths, optional schedule) **after** operator accepts this WO |

Carly does **not** implement the generator. Bruce does **not** invent WO policy. Generator output is always **DRAFT** until operator (or explicit process) promotes.

## Scope (in) — v0

1. **Inputs (measured only)**
   - Tail of `/home/rootrecord/RootRecord-Ecosystem/2 - RootRecord-Database/Logs/Automations/automations_current.log` (FAIL / path-error patterns only; no full dump into git)
   - Optional: recent lines from `/home/rootrecord/RootRecord-Ecosystem/2 - RootRecord-Database/Worklog/worklog_current.md` filtered by `domain=` tags (path/size/mtime metadata already scrubbed by design)
   - Optional: presence of open residual markers from known WO-SRV residual list (static allowlist, not free invention)

2. **Processing**
   - Deterministic rules first (Python or bash + templates) — e.g. N FAILs of same job id in M minutes → one draft candidate
   - Deduplicate against existing `Work-Orders/*.md` titles/IDs (simple string match)
   - Fill [TEMPLATE Work Order](../../01-operations/templates/TEMPLATE%20Work%20Order.md) placeholders only from measured snippets; use **Unknown / No data** when thin
   - Local LLM **optional and off by default** for Scope/Intent prose only; never for Status or metrics

3. **Outputs**
   - Write under `Documentation/06-development/Work-Orders/drafts/` (create folder on first use)
   - Filename pattern: `DRAFT_WO-AUTO-{{YYYY-MM-DD}}-{{short-slug}}.md`
   - Front matter / header: `Status: DRAFT — generator; not accepted`
   - Include evidence block: log line excerpts (redacted), timestamps, job id if present
   - **Never** edit active index README to auto-promote
   - **Never** set COMPLETE / LIVE / CLOSED

4. **Safety**
   - Reuse worklog scrub patterns (no tokens, no env values, no agent-transcript paths)
   - Cap excerpt length; no binary; no full log attach
   - Rate limit: max N new drafts per hour (operator-configurable default, e.g. 3)

## Scope (out) — v0

- Auto-promote drafts to active backlog
- Auto-implement or schedule domain fixes
- Telegram / Discord notify (WO-COM-*)
- Replacing human session worklogs
- Bulk-scanning G1/G2 trees
- Inventing residual paths not present in logs or allowlist

## Current reality

| Item | State |
|------|--------|
| Reports worklog foundation | LIVE (WO-RPT-001 A–E) |
| Automations log path | Documented; desk-only bytes |
| WO template | Exists under `01-operations/templates/` |
| `Work-Orders/drafts/` | **Does not exist yet** |
| Generator script | **None** |
| Live desk log liveness | **Unknown from git** — confirm on desk before scheduling |

## Acceptance criteria (when accepted for execution)

1. [ ] `drafts/` folder exists; README states draft-only policy
2. [ ] Generator reads only configured log/worklog paths; refuses if missing (no invent)
3. [ ] Output matches template fields; Status always DRAFT
4. [ ] Secrets scrub pass (no values from master-key class patterns)
5. [ ] Dedup: second run does not spam duplicate drafts for same job+window
6. [ ] Carly seal note on policy (or explicit operator accept) recorded before first scheduled run
7. [ ] No change to active WO index without human edit

## Suggested phases

| Phase | Work | Owner after accept |
|-------|------|--------------------|
| **0** | This WO + Carly policy seal | Ava / Carly |
| **1** | `drafts/` + README; dry-run CLI (one log file in, one draft out) | Bruce |
| **2** | FAIL-pattern rules + dedup | Bruce |
| **3** | Optional low-frequency job in `jobs.py` (e.g. every 15–30 min) | Bruce |
| **4** | Optional worklog domain-burst rule | Bruce |

## Non-goals

- Real-time streaming UI
- Replacing WO-SYS-001 observability design
- Radio/stream digests (Reports Phase F)

## Key paths

| Path | Role |
|------|------|
| `/home/rootrecord/RootRecord-Ecosystem/2 - RootRecord-Database/Logs/Automations/automations_current.log` | Poller FAIL source |
| `/home/rootrecord/RootRecord-Ecosystem/2 - RootRecord-Database/Worklog/` | Measured file activity |
| `…/Pacific-Solar-Server/Reports/scripts/` | Existing intake spine |
| `Library/.../Work-Orders/drafts/` | Generator output only |
| `Library/.../templates/TEMPLATE Work Order.md` | Template |

## Notes & constraints

- No force-push. No secrets in git or draft bodies.
- Prefer small reversible steps; dry-run before schedule.
- Does **not** block WO-SRV runtime verification.
- Align notify policy: generator drafts are **not** notifications (WO-COM-001 separate).

---

*Draft opened 2026-09-28 HST by Ava (architecture). Awaiting Carly seal + operator accept before Bruce implements.*
