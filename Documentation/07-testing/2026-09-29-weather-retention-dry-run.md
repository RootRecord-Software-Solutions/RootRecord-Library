# Test record — Weather retention dry run

| Field | Value |
| --- | --- |
| **Date / time (HST)** | 2026-09-29 04:03–04:04:41 HST |
| **Tester** | executor agent (g3-proposals-impl) |
| **Change under test** | Pacific `Weather/scripts/weather-retention.py` (policy in `Weather/README.md` §Retention, signed off), jobs.py ON_AT `weather_retention` (disabled). Proposal: [08-ideas weather retention](../08-ideas/2026-09-29-weather-retention-and-repo.md) |
| **State** | **PASS** (dry run; synthetic apply) · apply **VERIFY PENDING** (OFF until Alexander reviews) |
| **Evidence** | `2 - RootRecord-Database/Logs/Migration/g3-proposals-impl-evidence-20260929T140900Z.md` · report `2 - RootRecord-Database/Logs/Weather/Retention/weather-retention_dry-run_2026-09-29_0404.md` |
| **Commits** | Pacific `52573e7` · Database `a775c2f` (report) |
| **Backup** | `/home/rootrecord/Database/GITHUB/g3-proposals-impl.bak-20260929-035910/` |

## How (exact commands / procedure)

```bash
# 1) synthetic tree in /tmp (WEATHER_DATA_ROOT / WEATHER_RETENTION_ARCHIVE overrides), dry run, then --apply, then dry run
# 2) real data, dry run once:
/usr/bin/time -v python3 ".../Weather/scripts/weather-retention.py" --dry-run --json
```

## Pass criteria (written before running)
1. Synthetic: the dry run flags only the items past their window. `--apply` moves them to `Archive/Weather-<YYYYMM>/` and deletes nothing. The 11 MB log is rotated by copytruncate. A second dry run finds 0.
2. Real: a read-only run that saves a report with counts and bytes per class. Nothing is moved.

## Result
1. Synthetic: 4 items flagged: text 05-01 (> 90 d), imagery 09-01 (> 14 d), a 06-01 zip (> 90 d), and a report with mtime 08-01 (> 30 d). Recent, `_current` and hurricane files were kept. Apply moved all 4, with a README in each `Weather-<YYYYMM>`, and `weather-poller.log.1` was created. Second dry run: 0. **PASS**
2. Real (04:04:41): **would move 0 files / 0 bytes; would delete 0.** Kept: current 282 / 232,091,347 B; text_dated 255 / 14,876,501 B; imagery_dated 139 / 244,386,793 B; daily_zip 0; reports_archived 1,632 / 28,208,173 B; hurricanes 1 / 1,697 B; other 2 / 1,310,196 B. Weather/ total: 2,313 files / 521,137,050 B (497.0 MB). Disk free 201.3 GB. Log 30,192 B, so no rotation. No alarms. The oldest dated item is 2026-09-29. **PASS**

## Resource impact

| When | Load (1/5/15) | MemAvailable | Swap used | Peak RSS |
| --- | --- | --- | --- | --- |
| before | 1.54 / 1.54 / 1.46 | ~11.8 GB (12,054,108 kB) | not recorded | — |
| during | — | — | — | 17.8 MB (0.08 s wall) |
| after | 1.54 / 1.54 / 1.46 | not recorded | not recorded | — |

## Cleanup confirmation
- [x] synthetic tree `/tmp/rr-wx-ret-test.*` removed · [x] no process left · [x] no model

## Open items / caveats
- Apply stays OFF. The job is `enabled: False` and `--dry-run`. After Alexander reviews, enable it and switch to `--apply`.
- Daily zips mix text and imagery, so they follow the 90-day zip rule. Should zipped imagery leave after 14 days? (open question)
- The Weather repo is not approved and was not touched.
