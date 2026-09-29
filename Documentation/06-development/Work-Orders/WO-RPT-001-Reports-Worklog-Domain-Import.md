# WO-RPT-001 — Reports / Worklog Domain Import

| Field | Value |
|-------|--------|
| **Priority** | P0 |
| **Status** | **Phase B LIVE** — desk soak confirmed 2026-09-28 ~19:04 HST |
| **Target** | Pacific `Reports/` on org `RootRecord-Pacific-Solar-Server` |
| **Data home** | `/home/rootrecord/Database/WORKLOG/` (unchanged) |
| **Human narrative** | Library `Documentation/01-operations/` (templates + active logs) |
| **Related** | WO-ARCH-2026-09-27; WO-SRV-001 residual rewire; WO-COM-001/002 (notify later) |
| **Action plan** | [WO-RPT-001-Action-Plan.md](./WO-RPT-001-Action-Plan.md) |

## Goal

Move offline work auto-doc (worklog) off the G2 residual path
`~/.ollama/skills/reports/` onto org Pacific **`Reports/`**, keep Database as machine SOT,
and layer enhancements so migration progress itself is documented automatically.

## Scope (in)

- Pacific domain shell `Reports/` + scripts port from G2
- Rewire `jobs.py` `worklog_scan` to Pacific paths (quoted)
- Hygiene: extra path prunes (agent transcripts, credential-shaped paths)
- Domain-tagged log lines when path sits under a known Pacific domain
- Spec + later jobs: daily Library roll-up, weekly archive (WO-ARCH)
- G1 `reports/` packet: `MIGRATED.md` only after Phase B soak (diff-only later)

## Scope (out)

- Bulk-merge G1 `reports.py` public draft queue
- Owning A-Eyes / hourly-clip / timelapse pipelines
- Discord/Telegram notify of worklog events (WO-COM-*)
- AI-authored full Session narratives (wait for AI processing redesign)
- Changing Database/WORKLOG layout contract beyond additive tags

## Phases

| Phase | Work | Status |
|-------|------|--------|
| **A** | `Reports/` shell + README on Pacific; Library WO + index | **DONE** 2026-09-28 |
| **B** | Port scripts; rewire `worklog_scan`; desk soak | **LIVE** 2026-09-28 ~19:04 HST |
| **C** | Daily roll-up → Library Session template (structured summary) | OPEN |
| **D** | Weekly archive job implementing WO-ARCH | OPEN |
| **E** | G1 `reports/` `MIGRATED.md` + Old README + inventory map | OPEN (B soak done — ready) |

## Acceptance criteria

1. [x] `worklog_scan` in Pacific `jobs.py` points only at `Reports/scripts/`
2. [x] Successful scan: `OK wrote/updated /home/rootrecord/Database/WORKLOG/worklog_current.md`
3. [x] Domain tags + `source_job=worklog_scan` present in log lines
4. [x] Library WO + Pacific README track live state
5. Phase C/D optional — do not block B LIVE

## Soak evidence (operator window, 2026-09-28 ~19:04 HST)

```text
OK wrote/updated /home/rootrecord/Database/WORKLOG/worklog_current.md
… domain=Database | source_job=worklog_scan
… domain=Automations | source_job=worklog_scan
… domain=Reports | source_job=worklog_scan
… domain=System | source_job=worklog_scan
NEW_DIR …/Reports | domain=Reports
```

## Source inventory

| Gen | Path | Role |
|-----|------|------|
| G2 residual | `Solar-Pacific-RootRecord-Server/reports/scripts/worklog_*.sh` | Superseded for live path |
| G1 archive | `Solar-Pacific-RootRecord-Server-Old/reports/` | Diff-only; Phase E marker |
| G1 cousins | `hourly-clip-reports/`, `day-board-boot/`, `merged-morning/` | Not this WO |
| Library | `01-operations/templates/` | Human templates |
| Library | WO-ARCH-2026-09-27 | Weekly archive → Phase D |

## Risks

- Double-running G2 standalone `worklog_poller.sh` if still enabled — prefer jobs only
- Scrub miss if secrets only in files not listed in master-key.env

## Notes

- Machine worklog stays under Database; Library holds human sessions/checkpoints/WOs
- A-Eyes clips link from Reports later; they are not owned here
- Standing policy: one domain at a time; no bulk G1 merge

*Phase B LIVE 2026-09-28 ~19:04 HST.*
