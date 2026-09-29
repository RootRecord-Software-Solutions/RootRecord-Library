# Proposal — Weather retention and a Weather repo

| Field | Value |
| --- | --- |
| **Date (HST)** | 2026-09-29 |
| **State** | **Retention: LANDED / VERIFY PENDING (dry-run only; apply OFF pending review)** · Weather repo: PROPOSED (not approved) |
| **Grounding** | `g3-followups-evidence-20260929T124741Z.md` item 4 (320 MB at 02:44; ≈ 0.23 GB/day steady dated growth); retention text in Pacific `Weather/README.md` §Retention (PROPOSED); `sync-weather-database.sh` skips unless `Weather/` is its own git repo |
| **Needs sign-off from** | Alexander |

## Proposal
1. Approve (or amend) the retention policy already drafted in Pacific `Weather/README.md`.
2. Decide whether `2 - RootRecord-Database/Weather/` becomes its own RootRecord-Weather-Database repo. Weather data is local only today.

## Resource impact / safety
Retention reduces disk growth. A repo would add sync traffic, so size-check it before the first push.

## Implementation (2026-09-29 ~04:05 HST) — retention only
- Alexander signed off the policy in Pacific `Weather/README.md` §Retention (updated). The **Weather repo is NOT approved**, so it was not touched.
- `Weather/scripts/weather-retention.py` (new) runs `--dry-run` by default. `--apply` **moves** data past its window to `2 - RootRecord-Database/Archive/Previous-Datasets/Weather-<YYYYMM>/` (git-ignored except each README) and never deletes. Windows: dated text/HTML 90 d, daily zips 90 d, imagery dated folders 14 d, `reports/*/archived/` 30 d (mtime). Hurricanes and `_current` files are kept. The log rotates at 10 MB × 5 by copytruncate, and the oldest copy is moved, not deleted. Budget WARN if Weather/ > 20 GB or free space < 50 GB.
- `jobs.py`: ON_AT job `weather_retention` (00:30) is **`enabled: False`**, and its command is `--dry-run`.
- Commits: Pacific `52573e7` (04:06:53) · Database `a775c2f` (dry-run report, 04:07:02). Backup `/home/rootrecord/Database/GITHUB/g3-proposals-impl.bak-20260929-035910/`.
- Dry run 04:04:41: **0 files / 0 bytes** would move and 0 would be deleted. Everything is still inside its window (the oldest dated item is 2026-09-29). Weather/ holds 2,313 files / 497.0 MB, disk free is 201.3 GB, and no alarms fired. Report: `2 - RootRecord-Database/Logs/Weather/Retention/weather-retention_dry-run_2026-09-29_0404.md`. Test: [07-testing record](../07-testing/2026-09-29-weather-retention-dry-run.md).
- Open question: daily zips mix text and imagery, so they follow the 90-day zip rule. Should zipped imagery leave after 14 days?
- Pending: Alexander reviews the dry run. Only then enable the job and switch it to `--apply`.
