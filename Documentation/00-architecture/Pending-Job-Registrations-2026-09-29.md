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

Minutes are chosen to avoid the used minutes (0, 3, 6, 7, 8, 15, 22, 30, 32, 37, 45, 52; proposed 4, 11, 12, 25) so two voice renders never race for the single-flight lock. G1 ran all hourly desks at :02.

| Job id | List | Schedule (HST) | Flag | Added | Test |
| --- | --- | --- | --- | --- | --- |
| `system_net_sample` | EVERY_SECONDS | 300 s | `RR_NET_SAMPLES` | 14:08 | [batch 4](../07-testing/2026-09-29-old-repo-ports-breadth-batch4.md) |
| `voice_solar_desk` / `voice_security_desk` / `voice_bandwidth_desk` | EVERY_MINUTE | :04 / :11 / :12 | `RR_VOICE_SOLAR` / `RR_VOICE_SECURITY` / `RR_VOICE_BANDWIDTH` | 14:08 | batch 4 + [batch 5 fixes](../07-testing/2026-09-29-old-repo-ports-breadth-batch5.md#voice-text-fixes) |
| `reports_hawaii_news` | ON_AT | 10:00 | `RR_HAWAII_NEWS` (env `RR_NEWS_SEEDS_ONLY=1`) | 14:08, updated 14:25 | [batch 5](../07-testing/2026-09-29-old-repo-ports-breadth-batch5.md#hawaiʻi-news-seed-feeds) |
| `weather_official_hls` | EVERY_SECONDS | 600 s | `RR_OFFICIAL_HLS` | 14:42 | [batch 5](../07-testing/2026-09-29-old-repo-ports-breadth-batch5.md#official-statement-fetcher-hls) |
| `voice_official_weather` | EVERY_MINUTE | :25 | `RR_VOICE_OFFICIAL` | 14:42 | [batch 5](../07-testing/2026-09-29-old-repo-ports-breadth-batch5.md#official-weather-voice-report) |
| `weather_hurricane_global` | ON_AT | 05:40 09:40 12:40 16:40 20:40 | `RR_HURRICANE_GLOBAL` | 14:42 | [batch 5](../07-testing/2026-09-29-old-repo-ports-breadth-batch5.md#global-hurricane-board) |
| `reports_board_catchup` | ON_AT | 14:00 | `RR_REPORT_BOARD` | 14:42 | [batch 5](../07-testing/2026-09-29-old-repo-ports-breadth-batch5.md#report-board-and-catch-up-ledger) |
| `voice_boot_brief` | ON_BOOT | priority 20 | `RR_VOICE_BOOT` | 14:42 | [batch 5](../07-testing/2026-09-29-old-repo-ports-breadth-batch5.md#boot-brief-voice-report) |

Commands run through `bash -lc` in the poller (`rootserver_poller.py`), so the `;` chain in `voice_boot_brief` works. Minute :25 is also free of the proposed :04 / :11 / :12.

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
    {
        "id": "weather_official_hls",
        "enabled": os.environ.get("RR_OFFICIAL_HLS", "0") == "1",
        "description": "NWS HFO hurricane local statement (HLS) -> Database Weather/Hawai'i/official/ (G1 official-weather-media).",
        "interval_sec": 600,
        "builtin": "",
        "command": f'nice -n 10 python3 "{PACIFIC}/Weather/scripts/official_statement.py"',
        "timeout_sec": 60,
        "needs_internet": True,
        "cwd": f"{PACIFIC}/Weather/scripts",
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
    {
        "id": "voice_official_weather",
        "enabled": os.environ.get("RR_VOICE_OFFICIAL", "0") == "1",
        "description": "Ava official NWS Honolulu statement (HLS < 24 h, else HWO, else AFD; 4500-char cap). No delivery.",
        "only_at_minutes": [25],
        "builtin": "",
        "command": f'nice -n 10 python3 "{PACIFIC}/Media/Voice/scripts/voice_reports.py" official_weather',
        "timeout_sec": 600,
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
    {
        "id": "weather_hurricane_global",
        "enabled": os.environ.get("RR_HURRICANE_GLOBAL", "0") == "1",
        "description": "Worldwide TC board (NHC + RAMMB + JTWC ABPW/ABIO) -> Database Weather/Hawai'i/hurricanes/global/ (G1 hurricane-tracker).",
        "at_times": ["05:40", "09:40", "12:40", "16:40", "20:40"],
        "builtin": "",
        "command": f'nice -n 10 python3 "{PACIFIC}/Weather/hurricanes/scripts/global_board.py"',
        "timeout_sec": 120,
        "needs_internet": True,
        "cwd": f"{PACIFIC}/Weather/hurricanes/scripts",
        "env": {},
    },
    {
        "id": "reports_board_catchup",
        "enabled": os.environ.get("RR_REPORT_BOARD", "0") == "1",
        "description": "Daily report due ledger + catch-up (G1 daily-reports-catchup 14:00): text roll-up only, never plays.",
        "at_times": ["14:00"],
        "builtin": "",
        "command": f'nice -n 10 python3 "{PACIFIC}/Reports/scripts/report_board.py" run-due',
        "timeout_sec": 900,
        "cwd": f"{PACIFIC}/Reports/scripts",
        "env": {},
    },
```


### `ON_BOOT`

```python
    {
        "id": "voice_boot_brief",
        "enabled": os.environ.get("RR_VOICE_BOOT", "0") == "1",
        "priority": 20,
        "description": "G1 boot-prelims: refresh Kilauea / quakes first, then the Ava boot brief (file + WAV, no Grok, no playback).",
        "builtin": "",
        "command": f'nice -n 10 python3 "{PACIFIC}/Geology/scripts/geology_collect.py" ; nice -n 10 python3 "{PACIFIC}/Media/Voice/scripts/voice_reports.py" boot_brief',
        "timeout_sec": 600,
        "needs_internet": True,
        "cwd": f"{PACIFIC}/Media/Voice/scripts",
        "env": {},
    },
```

## C. AWS fallback desk jobs: proposed blocks only (added 2026-09-29 16:15 HST, sign-off)

These come from the [AWS fallback rebuild](../08-ideas/2026-09-29-aws-fallback-rebuild.md) Phase 2. **Neither the job nor its script exists yet.** The AWS side is deployed and works without them: `desk_watch` uses the `hawaii.ndjson` mtime, and the desk can pull the spool by hand.

| Job id | List | Schedule | Flag | What it does |
| --- | --- | --- | --- | --- |
| `aws_heartbeat_push` | EVERY_SECONDS | 60 s | `RR_AWS_HEARTBEAT` | `ssh rr-aws-ip 'touch ~/rootrecord/fallback/state/desk-heartbeat'`, a second desk-online signal beside the feed mtime |
| `aws_catchup` | EVERY_SECONDS | 600 s | `RR_AWS_CATCHUP` | rsync-pull `spool/outbox/*.zip`, verify the manifest sha256, ingest idempotently (ledger `Database/Logs/Mainland/aws-ingest-ledger.jsonl`), then write `state/desk-ack.json {"pack_seq": N}` |

```python
    {
        "id": "aws_heartbeat_push",
        "enabled": os.environ.get("RR_AWS_HEARTBEAT", "0") == "1",
        "description": "Desk-online heartbeat for the AWS fallback desk_watch (touch state/desk-heartbeat).",
        "interval_sec": 60,
        "builtin": "",
        "command": "timeout 15 ssh -o BatchMode=yes -o ConnectTimeout=8 rr-aws-ip 'touch /home/ubuntu/rootrecord/fallback/state/desk-heartbeat'",
        "timeout_sec": 20,
        "needs_internet": True,
        "cwd": PACIFIC,
        "env": {},
    },
    {
        "id": "aws_catchup",
        "enabled": os.environ.get("RR_AWS_CATCHUP", "0") == "1",
        "description": "Pull + verify + ingest AWS fallback relay packets, then ack (desk catch-up; idempotent).",
        "interval_sec": 600,
        "builtin": "",
        "command": 'nice -n 10 python3 "/home/rootrecord/RootRecord-Ecosystem/1 - Servers/2 - RootRecord-US-Mainland-Server/fallback/desk/aws_catchup.py"',
        "timeout_sec": 300,
        "needs_internet": True,
        "cwd": PACIFIC,
        "env": {},
    },
```

`fallback/desk/aws_catchup.py` is **not written yet** (Phase 3, sign-off). Its test must show that a second ingest adds 0 records and that the ack prunes the outbox.

## On-demand ports (no job needed)

`Geology/scripts/earthquakes_backfill.py`, `Media/Video/scripts/mp4_converter.py`, `Communications/web-facts/scripts/web_facts.py`, `Communications/live-wx/scripts/live_wx.py`, `Energy/scripts/load_categories.py`, `System/scripts/host_hw.py`, `Media/Voice/scripts/speech_scrub.py` (library), `Reports/scripts/report_board.py status`, `System/scripts/host_desks.py security|net-usage`.

*Created 2026-09-29 ~14:08 HST (old-repo migration, breadth pass). Updated ~14:25 HST: `reports_hawaii_news` now seeded (278 posts in a temp-root run), env `RR_NEWS_SEEDS_ONLY=1`, timeout 300 s. Updated ~14:42 HST (breadth pass 2): + `weather_official_hls`, `voice_official_weather`, `weather_hurricane_global`, `reports_board_catchup`, `voice_boot_brief`.*

*Status at pause 2026-09-29 16:25 HST: nothing registered since. §A: 7 blocks in `jobs.py`, all OFF (keep/remove is a sign-off). §B: 10 PROPOSED blocks. §C: 2 PROPOSED AWS desk jobs (`aws_catchup.py` not written). All are sign-off items.*
