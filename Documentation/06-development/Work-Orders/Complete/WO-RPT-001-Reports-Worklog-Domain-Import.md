# WO-RPT-001 — Reports / Worklog Domain Import

| Field | Value |
|-------|--------|
| **Priority** | P0 |
| **Status** | **COMPLETE** — signed off 2026-09-29 ~21:49 HST. Foundation A–E met. Daily roll-up wrote `2026-09-29 System Operator Worklog — Session auto.md`. Weekly archive first week: `2026-W40`, cutoff `2026-09-28`, 5 pre-week logs moved. Phase F radio/stream stays deferred and is out of this close. |
| **Target** | Pacific `Reports/` on org `RootRecord-Pacific-Solar-Server` |
| **Data home** | `/home/rootrecord/RootRecord-Ecosystem/2 - RootRecord-Database/Worklog/` (moved 2026-09-29; old `/home/rootrecord/Database/WORKLOG/` archived) |
| **Human narrative** | Library `Documentation/01-operations/` (templates + active logs) |
| **Related** | WO-ARCH-2026-09-27; WO-SRV-001; WO-COM-001/002; WO-AEYES; future AI-processing redesign |
| **Action plan** | [WO-RPT-001-Action-Plan.md](./WO-RPT-001-Action-Plan.md) |

## Goal

Move offline work auto-doc (worklog) off the G2 residual path onto org Pacific **`Reports/`**, keep Database as machine SOT, automate thin daily/weekly hygiene — and leave a **clean spine** for the old core function the messy AI report stack used to serve: **radio rundowns, live streaming, and public status**, without bringing the mess forward.

## Historical context (do not lose)

Legacy AIs **heavily automated reports** for on-air / stream workflows. That was a **core product function**, not only desk bookkeeping. Implementation was scattered (G1 `reports.py` draft queues, hourly-clip-reports, day-board, merged-morning, voice topics) and entangled with ops skills.

**This WO stabilizes intake + ops documentation.** It does **not** re-enable on-air automation. Future work must:

- Treat WORKLOG domain tags + LIVE domain status as **facts**
- Add digests / voice-safe summaries **on top** (Carly seal before public)
- Keep **A-Eyes** (capture), **Communications** (delivery), **Website** (boards) as separate owners
- Recover G1 draft-queue ideas only by **diff**, never bulk-merge

## Scope (in) — foundation

- Pacific `Reports/` + worklog scripts from G2
- `jobs.py` path rewire; domain tags; hygiene prunes
- Daily Library roll-up; weekly log archive; G1 `MIGRATED.md`

## Scope (out) — foundation

- Bulk-merge G1 `reports.py` public draft queue
- Owning A-Eyes / clips / timelapse
- Discord/Telegram notify (WO-COM-*)
- Full AI-authored session essays
- **Radio / live-stream rundown automation** (explicit future phase)

## Phases

| Phase | Work | Status |
|-------|------|--------|
| **A–E** | Domain, worklog LIVE, roll-up + archive scripts, G1 marker | **DONE** 2026-09-28 / worklog **PASS** 2026-09-29 |
| **F (future)** | Structured digests for radio/stream; seal path; link A-Eyes pointers | **DEFERRED** — after AI-processing redesign |

## Future fit (Phase F sketch)

```text
WORKLOG (measured) + domain LIVE
        → Reports digests (structured)
            → Carly seal (honesty)
                → Ava voice / Comms / stream overlay / radio rundown
A-Eyes clips ──────────────────────────→ stream segments (not owned by Reports)
```

Prefer Python + templates first; local LLM only after structure exists.

## Acceptance criteria (foundation)

1. [x] `worklog_scan` → Pacific `Reports/scripts/` only
2. [x] Desk soak: domain tags + `source_job=worklog_scan`
3. [x] Daily roll-up + weekly archive scripts scheduled
4. [x] G1 `reports/MIGRATED.md` + Old README
5. [x] Docs record radio/stream as **future** consumer of this spine

## Notes

- Machine worklog → Database; human sessions → Library; closed WOs → `Work-Orders/Complete/`
- Carly owns WO structure/drafts; Bruce builds accepted technical work
- One domain at a time; no bulk G1 merge

*Foundation 2026-09-28 HST. Radio/live-stream = Phase F after redesign.*
