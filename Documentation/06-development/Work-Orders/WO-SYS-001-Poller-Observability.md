# WO-SYS-001 — Poller Observability & FAIL Handling

| Field | Value |
|-------|--------|
| **Priority** | P2 |
| **Status** | **Log path slice complete** — wired to RootRecord-Database |
| **Target** | Pacific Automations; Database Logs; optional Communications notify |
| **Depends on** | Live poller stable; WO-COM-001 if alerts desired |

## Log storage (canonical)

**Repo:** [RootRecord-Database](https://github.com/RootRecord-Software-Solutions/RootRecord-Database)  
**Desk:** `/home/rootrecord/Database/`

| Stream | Path |
|--------|------|
| Poller / automations | `Logs/Automations/automations_current.log` |
| Stack reload | `Logs/Automations/stack_reload_current.log` |

Pacific defaults (`POLLER_LOG`, `STACK_RELOAD_LOG`) point at these. Archive policy: Database `Logs/*/Archive/README.md`.

Supersedes earlier draft paths under `Database/LOGS/...` and G2 `~/.ollama/skills/logs/store/`.

## Remaining scope

- FAIL code meanings + thresholds
- Operator guide: “how to read the poller window”
- Optional Telegram after WO-COM-001

## Acceptance

1. [x] Canonical paths under RootRecord-Database
2. [x] Pacific script defaults updated
3. [ ] Desk unit + banner show `automations_current.log`
4. [ ] FAIL policy written
