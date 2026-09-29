# WO-RPT-001 — Reports / Worklog Domain Import

| Field | Value |
|-------|--------|
| **Priority** | P0 |
| **Status** | **IN PROGRESS** — Phase A+B started 2026-09-28 ~19:00 HST |
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
| **B** | Port `worklog_lib.sh` / `worklog_once.sh` / `worklog_poller.sh`; rewire `worklog_scan` | **DONE** (await desk soak) |
| **C** | Daily roll-up → Library Session template (structured summary) | OPEN |
| **D** | Weekly archive job implementing WO-ARCH | OPEN |
| **E** | G1 `reports/` `MIGRATED.md` + Old README + inventory map | OPEN after B soak |

## Acceptance criteria

1. `worklog_scan` in Pacific `jobs.py` points only at `Reports/scripts/` (no `~/.ollama/skills/reports`)
2. One successful scan writes/updates `Database/WORKLOG/worklog_current.md` under poller
3. Secrets/transcript paths remain pruned; scrub_log still runs against master-key.env
4. Library WO status tracks phases; Pacific `Reports/README.md` matches live state
5. Phase C/D optional until operator schedules them — do not block B LIVE on C/D

## Source inventory

| Gen | Path | Role |
|-----|------|------|
| G2 live residual | `Solar-Pacific-RootRecord-Server/reports/scripts/worklog_*.sh` | Import source |
| G1 archive | `Solar-Pacific-RootRecord-Server-Old/reports/` | Diff-only later |
| G1 cousins | `hourly-clip-reports/`, `day-board-boot/`, `merged-morning/` | Not this WO |
| Library | `01-operations/templates/` | Human templates |
| Library | WO-ARCH-2026-09-27 | Weekly archive rules |

## Risks

- Path spaces on Pacific Ecosystem tree — always double-quote bash strings
- Double-running G2 poller + Pacific job if both enabled
- Scrub miss if secrets only in files not listed in master-key.env

## Notes

- Machine worklog stays under Database; Library holds human sessions/checkpoints/WOs
- A-Eyes clips link from Reports later; they are not owned here
- Standing policy: one domain at a time; no bulk G1 merge

*Opened and Phase A+B executed 2026-09-28 HST.*
