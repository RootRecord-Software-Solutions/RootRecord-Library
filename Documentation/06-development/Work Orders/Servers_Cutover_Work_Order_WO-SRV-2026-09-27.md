# WORK ORDER — Pacific Runtime Path Cutover (`skills` → `1 - Servers`)

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-SRV-2026-09-27 |
| **Status** | **IN PROGRESS** — Energy + **System LIVE**; next residual domains |
| **Updated** | 2026-09-28 ~16:50 HST |

**Policy:** Do not run the old desk as the poller host.

---

## Locked on Pacific

| Item | Status |
| --- | --- |
| systemd ExecStart | Pacific `run-poller.sh` (quoted) |
| Energy Phase 1 | LIVE (SUMMARY); watch for code=126 after restarts → chmod + energy symlink |
| **System Phase 1** | **LIVE** — `sys_stats_cycle` → `System/scripts/sys-sample.sh` |

## Residual G2

| Domain | Jobs |
| --- | --- |
| reports | worklog_scan |
| github | setup + sync_all |
| plumbing | ollama / flm |
| telegram | council_relay |
| a-eyes | cam, grab, timelapse |
| Weather | disabled |
| energy actions | Phase 2 |

## Next

1. Confirm Energy cycle OK after chmod/symlink if needed
2. worklog or github or plumbing (pick smallest)
3. Zero skills paths in jobs.py
