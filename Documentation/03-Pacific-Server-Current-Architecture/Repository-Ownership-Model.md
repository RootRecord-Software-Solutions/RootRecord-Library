# Repository ownership model

Short boot map: [08-repository-and-file-links.md](../../../0%20-%20Master-Prompt/prompts/08-repository-and-file-links.md). This page is the why. Work order: WO-MAP-2026-09-27.

## Why the split exists

RootRecord kept separate homes so public context, operational knowledge, runtime, and persistent data do not collapse into one role. On this desk those homes are directories of one git repository, `/home/rootrecord/RootRecord-Ecosystem`, published as `RootRecord-Software-Solutions/RootRecord-Ecosystem`. The GitHub source repositories still name the roles. They are not nested clones here.

## Where a change goes

- A guide, work order, agent rule, or architecture decision goes in `5 - RootRecord-Library/`.
- A service, job, monitor, or runtime script goes in `1 - Servers/1 - RootRecord-Pacific-Solar-Server/`.
- A log, sample, database, or media file goes in `2 - RootRecord-Database/`.
- A sentence meant for anyone who clones the public umbrella goes in the ecosystem README or another public doc, without secrets or live telemetry.
- The public page goes in `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Website/Home/`. That folder is the Vercel repository.

Sync flags are under `2 - RootRecord-Database/Github/flags/`. `/home/rootrecord/Database/` is not on this desk.

## What this desk syncs

`Github/scripts/repos.conf` enables six rows: `ecosystem` (inplace) and `pacific`, `database`, `library`, `website`, and `website-personal` (mirror). The live Pacific, Database, and Library folders have no `.git`. Mirror checkouts are `Github-worktrees/pacific`, `Github-worktrees/database`, `Github-worktrees/library`, `Github-worktrees/website`, and `Github-worktrees/website-personal`. Both website rows publish `Website/Home/`. `website` goes to `RootRecord-Software-Solutions/RootRecord-Website` (Vercel). `website-personal` goes to `rootrecordsoftwaresolutions/RootRecord-Website`. `github_sync_all` pulls and pushes both. `skills` and `mainland` are disabled (`enabled=0`). Their configured paths are under `Old repos deleted and merged/ollama-skills-g2-2026-09-30`, not the live Mainland directory. The Mainland tree is a directory inside the umbrella. It is not a separate git repository on this desk. GitHub still has `rootrecordsoftwaresolutions/US-Mainland-Server`.

The sync runs as poller job `github_sync_all`. There is no RootRecord systemd timer for it. `Pull.sh` and `Push.sh` are manual. They look for `.git` inside Pacific, Database, and Library, do not find one, and do not pull or push the umbrella.

## What stays out of the public umbrella

Live telemetry, sqlite databases, logs, and worklogs listed in `ecosystem-skip-autocommit.txt` stay on disk. Secrets and private infrastructure identifiers stay out of git. Generated weather bytes under Database `Weather/` are local. GitHub still has `rootrecordsoftwaresolutions/RootRecord-Weather-Database`. That repository is not a nested clone on this desk.

## History

Earlier desks used separate git repositories and the personal-account remote `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server`. That remote still exists. It is historical for current Pacific runtime. The `skills` sync row is disabled. `~/.ollama/skills` is present on this desk and is not the path named by that disabled row.
