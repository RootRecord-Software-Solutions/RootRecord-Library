# WO-RPT-001 — Action Plan

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
- [ ] Desk: run once after sync to confirm file under Library ops logs

```bash
bash "/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server/Reports/scripts/daily_roll_up.sh"
```

## Phase D — Weekly log archive (SHIPPED 2026-09-28)

- [x] `Reports/scripts/weekly_archive_logs.sh` (WO-ARCH rules for logs)
- [x] Closed WOs stay on `Work-Orders/Complete/` path (not weekly)
- [x] Job `reports_weekly_archive` ON_AT **19:00** HST (safe daily; only moves pre-week files)
- [ ] Optional: `DRY_RUN=1` once on desk before first real move

## Phase E — G1 hygiene (DONE 2026-09-28)

- [x] `MIGRATED.md` on G1 `reports/` + Old README

*C/D scripts + schedules 2026-09-28 HST.*
