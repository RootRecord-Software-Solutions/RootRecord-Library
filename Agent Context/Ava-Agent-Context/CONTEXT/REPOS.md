# Key Repositories

Short ownership map, not a copy: [08-repository-and-file-links.md](../../../../0%20-%20Master-Prompt/prompts/08-repository-and-file-links.md).

## Pack home (2026-09-29)

Canonical identity packs: `5 - RootRecord-Library/Agent Context/{Ava,Bruce,Carly}-Agent-Context/`.
`Documentation/02-agents/` is the interaction index (modes, requests, handoff, capabilities). Do not copy IDENTITY files there. The agent-named folders under it contain only `.gitkeep`.
Personal GitHub mirrors (`AvaIvy`, `CarlyMal`) stay separate remotes. The Library pack is the org authority.

Automatic git sync is the poller job `github_sync_all` (WO-GH-001 Option B, 2026-09-29). It is not a systemd timer. Do not add a second timer. `Pull.sh` and `Push.sh` are manual scripts. On this desk they do not pull or push the umbrella, because Pacific, Database, Library, and `Website/Home` have no `.git` of their own. The `website` mirror publishes `Website/Home/` to the org from `Github-worktrees/website`. The `website-personal` mirror publishes the same folder to `rootrecordsoftwaresolutions/RootRecord-Website` from `Github-worktrees/website-personal`.

## Organizational / Canonical
| Repository | Purpose |
|------------|--------|
| `RootRecord-Software-Solutions/RootRecord-Ecosystem` | Public umbrella. On this desk it is the git root at `/home/rootrecord/RootRecord-Ecosystem` |
| `RootRecord-Software-Solutions/RootRecord-Pacific-Solar-Server` | Pacific runtime role. In this checkout that tree is a directory, not its own clone |
| `RootRecord-Software-Solutions/US-Mainland-One` | Continuity node. Desk folder `1 - Servers/2 - RootRecord-US-Mainland-One/`, published by the `mainland` row. Not its own git repository |
| `RootRecord-Software-Solutions/US-Mainland-Two` | YouTube station. Desk folder `1 - Servers/3 - RootRecord-US-Mainland-Two/`. Own repository. The umbrella gitignores it |
| `RootRecord-Software-Solutions/RootRecord-Website` | Public home page. Mirror of Pacific `Website/Home/` (row `website`). Vercel builds this repository. The same folder also syncs to `rootrecordsoftwaresolutions/RootRecord-Website` (row `website-personal`). AWS is not the site. Production is `https://www.rootrecord.cloud/`. `ssh.rootrecord.cloud` is A `18.118.30.226`. The page requests `https://api.rootrecord.cloud` (A `18.118.30.226`, Caddy to `127.0.0.1:8091`). Reports are at `https://www.rootrecord.cloud/reports/`. Data contract: Pacific `Website/HANDOFF-vercel-homepage-2026-09-30.md`. The page is not a nested git checkout |
| `RootRecord-Ecosystem/2 - RootRecord-Database/Weather/` | Hawaiʻi weather data & media inside the umbrella checkout |
| `RootRecord-Software-Solutions/RootRecord-Library` | Knowledge role. In this checkout, `5 - RootRecord-Library/` is a directory of the umbrella |
| `RootRecord-Software-Solutions/RootRecord-Database` | Persistence role. In this checkout, `2 - RootRecord-Database/` is a directory of the umbrella |

## Legacy (superseded for Pacific runtime)
| Repository | Notes |
|------------|--------|
| `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server` | Historical prior skills-tree remote; current Pacific runtime is under the org repo above |

## Product Surface (RootRecord account)
| Repository | Purpose |
|------------|--------|
| `RootRecord/rootrecord-weather-manager-download` | Weather Manager Windows releases |
| `RootRecord/rootrecord-business-manager-download` | Business Manager Windows releases |
| `RootRecord/Doc-Repo` | Developer documentation |

## Ava Identity
| Repository | Purpose |
|------------|--------|
| `AvaIvy/AvaIvy-Agent-Context` | GitHub full name. `AvaIvy/Agent-Context` resolves to this repository. Historical identity, mirrored into the Library pack |
| Ava Ivy Cloud (avaivy.cloud) | Public chat / identity surface |
