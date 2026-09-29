# WO-RPT-001 — Action Plan

Companion to [WO-RPT-001-Reports-Worklog-Domain-Import.md](./WO-RPT-001-Reports-Worklog-Domain-Import.md).

## Phase A — Domain shell (DONE 2026-09-28)

- [x] Create Pacific `Reports/README.md`
- [x] Create this WO + index entry
- [x] Document dual path: Database machine / Library human

## Phase B — Path rewire (LIVE 2026-09-28 ~19:04 HST)

- [x] Port `worklog_lib.sh` (hygiene prunes + domain tags)
- [x] Port `worklog_once.sh`, `worklog_poller.sh`
- [x] Rewire `jobs.py` `worklog_scan` → Pacific `Reports/scripts/worklog_once.sh`
- [x] Desk: confirm `OK wrote/updated` + advancing `worklog_current.md`
- [x] Domain tags observed (`Automations`, `Reports`, `System`, `Database`, …)

## Phase C — Daily Library roll-up (OPEN)

- [ ] Script: summarize today’s WORKLOG segments → optional append under Library ops logs
- [ ] Use Session template placeholders; no secrets
- [ ] Job: `ON_AT` ~18:30 HST or operator-chosen
- [ ] Migration progress stub (domain status lines)

## Phase D — Weekly archive (OPEN)

- [ ] Implement WO-ARCH rules for **logs** → `01-operations/archive/YYYY-Www/`
- [ ] Closed WOs use `Work-Orders/Complete/` (not weekly trees)
- [ ] Schedule Sunday ~19:00 HST after manual proof

## Phase E — G1 hygiene (DONE 2026-09-28)

- [x] `MIGRATED.md` on G1 `reports/`
- [x] Update Old README status table (MIGRATED count → 4)

## Enhancement checklist

| Enhancement | Phase |
|-------------|-------|
| Dual-output design (Database + Library) | A docs; C job |
| Domain tags on Pacific-path events | **B LIVE** |
| Extra prunes (transcripts, credential-ish paths) | **B LIVE** |
| Weekly archive automation | D |
| Migration progress surface | C |
| Deny public-draft G1 bulk import | standing |
| G1 reports marker | **E DONE** |

*Phase B LIVE + E 2026-09-28 HST.*
