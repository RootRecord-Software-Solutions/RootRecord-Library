# Governance

Decisions copied from the G1 packets `governance/`, `origin-session/`, and `ecosystem-history/`. This folder is the live record. It is not a Pacific service.

| Page | What it keeps |
| --- | --- |
| [community-governance-decisions.md](./community-governance-decisions.md) | Flags and the self-update gate |
| [origin-session-decision.md](./origin-session-decision.md) | Desk session id, and the refusal to restore it |
| [ecosystem-history-decisions.md](./ecosystem-history-decisions.md) | Host and path decisions from `NARRATIVE.md`, labeled Historical |

Work order: `WO-MIG-06-2026-09-29`.

## Self-update gate

Community governance and self-update both default **off**. A Cursor self-update is refused unless both flags are on, origin uptime is at least one hour, and free context is known and above 25%. Boot never self-updates. The old code did not spawn Cursor even when the gate passed (`held_for_sdk`).

## Origin was not imported

`origin-session` is a five-file helper. The `origin/` app (~4342 paths) was not copied into Pacific, Database, the website, or this Library folder.

## No Pacific package

There is no `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Governance/` package, no Database folder, and no Logs folder. `jobs.py` has no `governance-daily`, `governance-boot`, or `governance-self-update` job.

## Refused

Not brought into the live Folders: `origin/`, `CURRENT.md`, `ecosystem-history/references/`, sqlite, `.env`, `governance-daily` DAILY telemetry, and every ecosystem-history script (including `delete_archives_trees.sh` and the TTS proofs).

Full trees, including generated notes and excluding `__pycache__`, were copied to:

`Old repos deleted and merged/Solar-Pacific-RootRecord-Server-Old/`

Those three tops were then removed from `Solar-Pacific-RootRecord-Server-Old`:

- `main` `fd0a9c0`
- `online-safe-20260920` `4fe7f7c4`
- `skills-rebuild` `c864821`

`origin/` is still on all three branches. The local clone's `origin` remote points at `Solar-Pacific-RootRecord-Server`, which never had these paths. Nothing was pushed there. The `online-safe-20260920` push also published two commits that were already on that local branch and not yet on GitHub: radar-archive (`8c9437d0`) and RAMMB sources (`e8c37881`).
