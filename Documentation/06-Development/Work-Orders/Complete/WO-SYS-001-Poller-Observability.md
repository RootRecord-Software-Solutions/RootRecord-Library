# WO-SYS-001 — Poller Observability & FAIL Handling

| Field | Value |
|-------|--------|
| **Priority** | P2 |
| **Status** | **COMPLETE** — signed off 2026-09-29 ~21:55 HST. Log path, desk unit, dashboard banner, and FAIL policy are in place. Telegram alerts stay on WO-COM-001 and are not part of this close. |
| **Target** | Pacific Automations; Database Logs; optional Communications notify |
| **Depends on** | Live poller stable; WO-COM-001 if alerts desired |

## Log storage (canonical)

**Repo:** [RootRecord-Database](https://github.com/RootRecord-Software-Solutions/RootRecord-Database)  
**Desk:** `/home/rootrecord/RootRecord-Ecosystem/2 - RootRecord-Database/`  
`/home/rootrecord/Database/` remains the backup/flag root (`GITHUB/`), not the log desk.

| Stream | Path |
|--------|------|
| Poller / automations | `Logs/Automations/automations_current.log` |
| Stack reload | `Logs/Automations/stack_reload_current.log` |

Pacific defaults (`POLLER_LOG`, `STACK_RELOAD_LOG`) point at these. Archive policy: Database `Logs/*/Archive/README.md`.

Supersedes earlier draft paths under `Database/LOGS/...` and G2 `~/.ollama/skills/logs/store/`.

## Remaining scope

- [x] FAIL code meanings + thresholds — `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Automations/scripts/poller/README.md` section “FAIL policy”
- [x] Operator guide: “how to read the poller window” — same section
- Optional Telegram after WO-COM-001 (not part of this close)

## Acceptance

1. [x] Canonical paths under RootRecord-Database
2. [x] Pacific script defaults updated
3. [x] Desk unit + banner show `automations_current.log` — user unit `POLLER_LOG` set; dashboard header prints the file name (verified by rendering one frame)
4. [x] FAIL policy written — poller README, 2026-09-29
