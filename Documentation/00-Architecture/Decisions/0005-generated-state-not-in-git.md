# 0005 — Generated state stays out of git

Date: 2026-09-30.

## Decision

`state-aggregate.py` writes `2 - RootRecord-Database/System/status/rootrecord-state.json` and `projections/`. That directory is listed in `Github/scripts/ecosystem-skip-autocommit.txt`. Durable memory is the handoff, this decision set, the contracts, and the schemas.

## Reason

The snapshot changes every reply. Committing it would bloat the public umbrella and would publish pids and host details. A clone should learn the architecture from docs and learn the live numbers by running verify on the desk.

## Do not remove without reconsidering

- The public repository is sanitized
- Hostname is `visibility: private`
- High-volume samples already live under Database energy and system paths that are also skipped
