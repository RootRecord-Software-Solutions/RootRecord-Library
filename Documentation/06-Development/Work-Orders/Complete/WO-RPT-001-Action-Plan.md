# WO-RPT-001 — Action Plan

**Status:** COMPLETE — signed off 2026-09-29 ~21:49 HST. Phases A–E desk boxes are done. Phase F is deferred on the parent and is out of this close.

Companion to [WO-RPT-001-Reports-Worklog-Domain-Import.md](./WO-RPT-001-Reports-Worklog-Domain-Import.md).

## Phase A — Domain shell (DONE 2026-09-28)

- [x] Create Pacific `Reports/README.md`
- [x] Create this WO + index entry
- [x] Document dual path: Database machine / Library human

## Phase B — Path rewire (LIVE 2026-09-28 ~19:04 HST)

- [x] Port worklog scripts; rewire `worklog_scan`; desk soak confirmed

## Phase C — Daily Library roll-up (SHIPPED 2026-09-28)

- [x] `Reports/scripts/daily_roll_up.sh` — measured counts → Session auto.md
- [x] Job `reports_daily_roll_up` ON_AT **18:30** HST
- [x] Desk: run once after sync to confirm file under Library ops logs (2026-09-29 21:49 HST; `2026-09-29 System Operator Worklog — Session auto.md`)

```bash
bash "/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server/Reports/scripts/daily_roll_up.sh"
```

## Phase D — Weekly log archive (SHIPPED 2026-09-28)

- [x] `Reports/scripts/weekly_archive_logs.sh` (WO-ARCH rules for logs)
- [x] Closed WOs stay on `Work-Orders/Complete/` path (not weekly)
- [x] Job `reports_weekly_archive` ON_AT **19:00** HST (safe daily; only moves pre-week files)
- [x] `DRY_RUN=1` once on desk before first real move (2026-09-29 21:49 HST). Cutoff is Monday of the current HST week (`date +%u`, not GNU “monday this week”). First real move: week `2026-W40`, cutoff `2026-09-28`, 5 files (2026-09-26 and 2026-09-27). Seven current-week logs stayed active.

## Phase E — G1 hygiene (DONE 2026-09-28)

- [x] `MIGRATED.md` on G1 `reports/` + Old README

*C/D scripts + schedules 2026-09-28 HST.*
