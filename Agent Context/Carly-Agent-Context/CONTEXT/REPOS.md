# Key Repositories

Short ownership map, not a copy: [08-repository-and-file-links.md](../../../../0%20-%20Master-Prompt/prompts/08-repository-and-file-links.md).

## Pack home (2026-09-29)

Canonical identity packs: `5 - RootRecord-Library/Agent Context/{Ava,Bruce,Carly}-Agent-Context/`.
`Documentation/02-agents/` is an index plus empty placeholders. Do not copy IDENTITY files there.
Personal GitHub mirrors (`AvaIvy`, `CarlyMal`) stay separate remotes. The Library pack is the org authority.

Automatic git sync is one timer: Pacific `github_sync_all` (WO-GH-001 Option B, 2026-09-29). Do not suggest a second pull timer. `Pull.sh` and `Push.sh` are manual only.

## Organizational / Canonical
| Repository | Purpose |
|------------|--------|
| `RootRecord-Software-Solutions/RootRecord-Ecosystem` | Public umbrella. On this desk it is the git root at `/home/rootrecord/RootRecord-Ecosystem` |
| `RootRecord-Software-Solutions/RootRecord-Pacific-Solar-Server` | Pacific runtime role. In this checkout that tree is a directory, not its own clone |
| `rootrecordsoftwaresolutions/US-Mainland-Server` | Secondary / recovery infrastructure node |
| `rootrecordsoftwaresolutions/RootRecord-Website` | Public Next.js foundation |
| `rootrecordsoftwaresolutions/RootRecord-Weather-Database` | Hawaiʻi weather data & media |
| `RootRecord-Software-Solutions/RootRecord-Library` | Knowledge role. In this checkout, `5 - RootRecord-Library/` is a directory of the umbrella |
| `RootRecord-Software-Solutions/RootRecord-Database` | Persistence role. In this checkout, `2 - RootRecord-Database/` is a directory of the umbrella |

## Legacy (superseded for Pacific runtime)
| Repository | Notes |
|------------|--------|
| `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server` | Prior skills-tree remote; Pacific runtime now under the org repo above |

## Product Surface (RootRecord account)
| Repository | Purpose |
|------------|--------|
| `RootRecord/rootrecord-weather-manager-download` | Weather Manager Windows releases |
| `RootRecord/rootrecord-business-manager-download` | Business Manager Windows releases |
| `RootRecord/Doc-Repo` | Developer documentation |

## Carly Identity
| Repository | Purpose |
|------------|--------|
| `CarlyMal/Agent-Context` | Historical identity & policy (mirrored into Library agent packs) |
