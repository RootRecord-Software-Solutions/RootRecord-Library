# Proposal — Weather retention and a Weather repo

| Field | Value |
| --- | --- |
| **Date (HST)** | 2026-09-29 |
| **State** | PROPOSED |
| **Grounding** | `g3-followups-evidence-20260929T124741Z.md` item 4 (320 MB at 02:44; ≈ 0.23 GB/day steady dated growth); retention text in Pacific `Weather/README.md` §Retention (PROPOSED); `sync-weather-database.sh` skips unless `Weather/` is its own git repo |
| **Needs sign-off from** | Alexander |

## Proposal
1. Approve (or amend) the retention policy already drafted in Pacific `Weather/README.md`.
2. Decide whether `2 - RootRecord-Database/Weather/` becomes its own RootRecord-Weather-Database repo. Weather data is local only today.

## Resource impact / safety
Retention reduces disk growth. A repo would add sync traffic, so size-check it before the first push.
