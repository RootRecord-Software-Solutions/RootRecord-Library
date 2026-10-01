# Repository ownership model

Short boot map: [08-repository-and-file-links.md](../../../0%20-%20Master-Prompt/prompts/08-repository-and-file-links.md). This page is the why. Work order: WO-MAP-2026-09-27.

## Why the split exists

RootRecord kept separate homes so public context, operational knowledge, runtime, and persistent data do not collapse into one role. On this desk those homes are directories of one git repository, `/home/rootrecord/RootRecord-Ecosystem`, published as `RootRecord-Software-Solutions/RootRecord-Ecosystem`. The GitHub source repositories still name the roles. They are not nested clones here.

## Where a change goes

- A guide, work order, agent rule, or architecture decision goes in `5 - RootRecord-Library/`.
- A service, job, monitor, or runtime script goes in `1 - Servers/1 - RootRecord-Pacific-Solar-Server/`.
- A log, sample, database, or media file goes in `2 - RootRecord-Database/`.
- A sentence meant for anyone who clones the public umbrella goes in the ecosystem README or another public doc, without secrets or live telemetry.

`/home/rootrecord/Database/` holds sync flags and backups (`GITHUB/`). It is not the live data desk.

## What this desk syncs

`Github/scripts/repos.conf` enables `ecosystem` (inplace) plus `pacific`, `database`, and `library` (mirror publishes; the live folders have no `.git` of their own). `skills` stays enabled. `website` and `mainland` stay disabled until each is a real checkout outside this snapshot. `Pull.sh` remains the manual pull path.

## What stays out of the public umbrella

Live telemetry, sqlite databases, logs, and worklogs listed in `ecosystem-skip-autocommit.txt` stay on disk. Secrets and private infrastructure identifiers stay out of git. Generated weather bytes under Database `Weather/` are local. Published Hawaiʻi weather products belong to `rootrecordsoftwaresolutions/RootRecord-Weather-Database`, not to a dump inside Library.

## History

Earlier desks used separate git repositories and the personal-account remote `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server`. That remote is historical for Pacific runtime. G2 files under `~/.ollama/skills` stay until Alexander signs off on retirement. The `skills` sync row stays enabled for that reason.
