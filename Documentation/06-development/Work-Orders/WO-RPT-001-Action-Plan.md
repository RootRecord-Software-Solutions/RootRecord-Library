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

### Desk verification (operator) — passed

```bash
bash "/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server/Reports/scripts/worklog_once.sh"
tail -n 30 /home/rootrecord/Database/WORKLOG/worklog_current.md
```

## Phase C — Daily Library roll-up (OPEN)

- [ ] Script: summarize today’s WORKLOG segments → optional append under Library ops logs
- [ ] Use Session template placeholders; no secrets
- [ ] Job: `ON_AT` ~18:30 HST or operator-chosen
- [ ] Migration progress stub (domain status lines)

## Phase D — Weekly archive (OPEN)

- [ ] Implement WO-ARCH rules in `Reports/scripts/weekly_archive.sh` (or Library-side)
- [ ] `git mv` closed logs → `01-operations/archive/YYYY-Www/`
- [ ] Closed WOs only → `06-development/archive/YYYY-Www/`
- [ ] Schedule Sunday ~19:00 HST after manual proof

## Phase E — G1 hygiene (OPEN — B soak done, ready)

- [ ] `MIGRATED.md` on G1 `reports/`
- [ ] Update Old README status table + Library inventory map

## Enhancement checklist

| Enhancement | Phase |
|-------------|-------|
| Dual-output design (Database + Library) | A docs; C job |
| Domain tags on Pacific-path events | **B LIVE** |
| Extra prunes (transcripts, credential-ish paths) | **B LIVE** |
| Weekly archive automation | D |
| Migration progress surface | C |
| Deny public-draft G1 bulk import | standing |

*Phase B LIVE 2026-09-28 ~19:04 HST.*
