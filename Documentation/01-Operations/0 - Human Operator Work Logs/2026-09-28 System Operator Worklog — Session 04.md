# System Operator Worklogs — Session 04

**Date:** 2026-09-28  
**Session:** Residual rewire progress — Energy actions, Plumbing, stack reload policy  
**Timezone:** HST  
**Window:** ~20:30–21:00 HST  
**Status:** ACTIVE  
**Operator:** RootRecord  
**Agent assist:** BruceMonitor

---

## Purpose

Execute and verify the next residual path rewires from Session 03 order, and fix automated stack reload so the status window no longer tears down the poller after GitHub code pulls.

---

## Approximate timetable (2026-09-28 HST)

| Time (approx.) | Event |
| --- | --- |
| 20:30 | Energy actions constant rewired to Pacific `Energy/scripts/actions` |
| 20:40 | Plumbing placed under `System/scripts/plumbing/`; warmup jobs rewired |
| 20:45–20:55 | Diagnosed poller stop-after-sync: window close → full stack stop |
| 20:55 | `do-stack-reload.sh` updated — skip status window on automated reload |
| 20:58 | Verified live `jobs.py` residuals; docs refresh |

---

## Completed this session

### Path rewires

- [x] `ECOFLOW_ACTIONS` → `{PACIFIC}/Energy/scripts/actions`
- [x] Energy actions scripts present under Pacific `Energy/scripts/actions/`
- [x] Plumbing folder: `System/scripts/plumbing/` (ollama-warmup + flm-warmup)
- [x] `ollama_warmup` / `flm_npu_warmup` jobs point at Pacific plumbing paths

### Stack lifecycle

- [x] Root cause: automated reload opened status window; window exit stopped entire stack; `Restart=on-failure` did not recover clean stops
- [x] `do-stack-reload.sh`: default skip window (`OPEN_POLLER_WINDOW=1` to opt in)
- [x] Operator can still open viewer manually via `open-poller-window.sh`

### Explicit non-goals

- Telegram / council_relay (in progress next)
- A-Eyes import
- Weather enable
- No bulk G1 merge

---

## Blockers / residual items

| Item | Notes |
| --- | --- |
| Telegram / council_relay | Still skills path — next rewire |
| A-Eyes | Still skills path |
| Network globe cwd | Legacy cwd only |
| CLI `/home/rootrecord/rootserver-poller` | Missing (unit path is primary) |

---

## Decisions

> Plumbing lives under `System/scripts/plumbing/` rather than a top-level `Plumbing/` domain.

Rationale: Playbook prefers existing capitalized domain folders; warmup scripts are system/inference infrastructure.

> Automated stack reload does not open the status window.

Rationale: `poller-watch` treats window close as intentional full-stack stop; deferred terminal launches were exiting and killing the poller after every code pull.

---

## State at session close (~21:00 HST)

- **Runtime:** Poller healthy after manual verification; Energy + System + Reports + Github + Plumbing on Pacific paths
- **Library / docs:** WO-SRV residual list + this session log updated
- **Next useful step:** Telegram / council_relay → `Communications/`

**Status:** Energy actions + Plumbing complete. Stack reload policy fixed. Telegram next.

---

## Archive note

Filename:

```text
2026-09-28 System Operator Worklog — Session 04.md
```
