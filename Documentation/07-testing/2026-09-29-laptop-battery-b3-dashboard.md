# Test record — Laptop battery bar B3 on the dashboard

| Field | Value |
| --- | --- |
| **Date / time (HST)** | 2026-09-29 03:16 HST (landed); read-only check 03:38 HST |
| **Change under test** | Dashboard B3 "System (laptop)" bar, plus a `LAP=<pct>/<status>/<AC>` field in the poller status line (sysfs, read-only) |
| **State** | **LANDED / VERIFY PENDING** |
| **Evidence** | WO-SRV entry "Laptop battery" |
| **Commits** | Pacific `0ea16cd` (03:16; `poller-dashboard.py`, `rootserver_poller.py`) |

## Pass criteria
After the next poller start, the status line in `2 - RootRecord-Database/Logs/Automations/automations_current.log` shows `LAP=`, and the dashboard shows the B3 bar with the same value.

## Result
- 03:38 HST: 0 lines containing `LAP=` in `automations_current.log`. The running poller (PID 105444) started at 03:13:28, before `0ea16cd`, so the status-line change is not live yet.
- Not restarted for this test (docs-only pass). Verify at the next natural poller start.

## Cleanup confirmation
Read-only.
