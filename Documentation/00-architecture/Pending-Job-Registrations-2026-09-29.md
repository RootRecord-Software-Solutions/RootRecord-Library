# Pending job registrations — old-repo migration (2026-09-29)

| Field | Value |
| --- | --- |
| **Standing rule** | `Pacific Automations/scripts/jobs.py` is edited only when Alexander asks or a work order requires it (received 13:45 HST). New gated jobs are listed here with the exact block to add. **Every row is a sign-off item.** |
| **Poller** | PID 105444 (started 03:13:28 HST) was not restarted; `jobs.py` is read only at poller start, so nothing here is active. |
| **Matrix** | [Old-Repo-Migration-Matrix](./Old-Repo-Migration-Matrix.md) |

## A. Already in jobs.py (added 13:21–13:44 HST, before the rule; left in place, all OFF)

| Job id | List | Schedule | Flag |
| --- | --- | --- | --- |
| `geology_collect` | EVERY_SECONDS | 300 s | `RR_GEOLOGY` |
| `geology_kilauea_cams` | EVERY_SECONDS | 600 s | `RR_KILAUEA_CAMS` |
| `system_uptime_log` | EVERY_SECONDS | 60 s | `RR_UPTIME_LOG` |
| `voice_earthquake_report` | EVERY_MINUTE | :08 | `RR_VOICE_QUAKE` |
| `voice_kilauea_report` | EVERY_MINUTE | :03 | `RR_VOICE_KILAUEA` |
| `energy_sun_times` | EVERY_HOUR | hourly | `RR_SUN_TIMES` |
| `voice_hurricane_desk` | ON_AT | 05:50 09:50 12:50 16:55 20:50 | `RR_VOICE_HURRICANE` |

Exact blocks and line numbers: Database `Logs/Migration/migration-jobs-py-additions-20260929.md`. Decision needed: keep (then set flags) or remove.

## B. Proposed, NOT in jobs.py (add only after sign-off)

Minutes are chosen to avoid the used minutes (0, 3, 6, 7, 8, 15, 22, 30, 32, 37, 45, 52) so two voice renders never race for the single-flight lock. G1 ran all hourly desks at :02.

### `EVERY_SECONDS`

```python
    {
        "id": "system_net_sample",
        "enabled": os.environ.get("RR_NET_SAMPLES", "0") == "1",
        "description": "Byte-counter sample of the default-route iface (G1 host-metrics port) -> Database System/network/.",
        "interval_sec": 300,
        "builtin": "",
        "command": f'nice -n 10 python3 "{PACIFIC}/System/scripts/host_desks.py" net-sample',
        "timeout_sec": 30,
        "cwd": f"{PACIFIC}/System/scripts",
        "env": {},
    },
```

### `EVERY_MINUTE`

```python
    {
        "id": "voice_solar_desk",
        "enabled": os.environ.get("RR_VOICE_SOLAR", "0") == "1",
        "description": "Bruce solar desk (EcoFlow SOC / solar W / AC out + sun times). No delivery.",
        "only_at_minutes": [4],
        "builtin": "",
        "command": f'nice -n 10 python3 "{PACIFIC}/Media/Voice/scripts/voice_reports.py" solar_desk',
        "timeout_sec": 300,
        "cwd": f"{PACIFIC}/Media/Voice/scripts",
        "env": {},
    },
    {
        "id": "voice_security_desk",
        "enabled": os.environ.get("RR_VOICE_SECURITY", "0") == "1",
        "description": "Carly security desk (ufw boot, sshd, listeners, failed sign-in counts). No delivery.",
        "only_at_minutes": [11],
        "builtin": "",
        "command": f'nice -n 10 python3 "{PACIFIC}/Media/Voice/scripts/voice_reports.py" security_desk',
        "timeout_sec": 300,
        "cwd": f"{PACIFIC}/Media/Voice/scripts",
        "env": {},
    },
    {
        "id": "voice_bandwidth_desk",
        "enabled": os.environ.get("RR_VOICE_BANDWIDTH", "0") == "1",
        "description": "Carly bandwidth desk (last hour / 24 h bytes; needs system_net_sample). No delivery.",
        "only_at_minutes": [12],
        "builtin": "",
        "command": f'nice -n 10 python3 "{PACIFIC}/Media/Voice/scripts/voice_reports.py" bandwidth_desk',
        "timeout_sec": 300,
        "cwd": f"{PACIFIC}/Media/Voice/scripts",
        "env": {},
    },
```

### `ON_AT`

```python
    {
        "id": "reports_hawaii_news",
        "enabled": os.environ.get("RR_HAWAII_NEWS", "0") == "1",
        "description": "Hawaii government news collector (G0 port + 16 seed feeds), daily. hawaii.gov + County of Maui feeds.",
        "at_times": ["10:00"],
        "builtin": "",
        "command": f'nice -n 10 python3 "{PACIFIC}/Reports/News/scripts/hawaii_news.py"',
        "timeout_sec": 300,
        "cwd": f"{PACIFIC}/Reports/News/scripts",
        "env": {"RR_NEWS_SEEDS_ONLY": "1"},  # seed feeds only (~12 s); drop to also run G0 portal discovery (~23 s, 25 x 404 today)
    },
```

## On-demand ports (no job needed)

`Geology/scripts/earthquakes_backfill.py`, `Media/Video/scripts/mp4_converter.py`, `Communications/web-facts/scripts/web_facts.py`, `Communications/live-wx/scripts/live_wx.py`, `System/scripts/host_desks.py security|net-usage`.

*Created 2026-09-29 ~14:08 HST (old-repo migration, breadth pass). Updated ~14:25 HST: `reports_hawaii_news` now seeded (278 posts in a temp-root run), env `RR_NEWS_SEEDS_ONLY=1`, timeout 300 s.*
