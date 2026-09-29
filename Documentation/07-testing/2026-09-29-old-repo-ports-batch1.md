# Test record — Old-repo ports batch 1 (sun times, uptime log, MP4 converter)

| Field | Value |
| --- | --- |
| **Date / time (HST)** | 2026-09-29 13:26–13:29 HST |
| **Tester** | Grok Bot (desk agent, old-repo migration pass) |
| **Change under test** | Ports of G1 `hourly-solar-weather` sun times → Pacific `Energy/scripts/sun_times.py`; G1 `uptime-log` → `System/scripts/uptime_log.py`; G1 `mp4-converter` → `Media/Video/scripts/mp4_converter.py` (+ `Media/Video/README.md`). Gated jobs `energy_sun_times` (`RR_SUN_TIMES`), `system_uptime_log` (`RR_UPTIME_LOG`). [Matrix](../00-architecture/Old-Repo-Migration-Matrix.md) |
| **State** | **PASS** (one manual run each) · jobs **LANDED, gated OFF** until the next poller start with the flag set |
| **Evidence** | `2 - RootRecord-Database/Logs/Migration/migration-geology-evidence-20260929T2319Z.md` §5–§8 |
| **Commits** | Pacific `cd48536` (sun_times, uptime_log, jobs gates); Media/Video + READMEs in later auto-sync (see worklog) · Database `0a2364e` (sun + uptime outputs) |
| **Backup** | `/home/rootrecord/Database/GITHUB/migration-old-repos.bak-20260929-133118/` (+ `jobs.py` in the geology backup) |

## What was tested

1. `sun_times.py` — Open-Meteo daily sunrise/sunset for Volcano (19.43, −155.23) → Database `Energy/sun/sun-times-last.json`; second call same day must not fetch.
2. `uptime_log.py tick` — wall clock + `boot_id` heartbeat → Database `System/uptime/uptime-{last.json,events.jsonl}`; a simulated 600 s gap in a temp root.
3. `mp4_converter.py` — synthetic 2 s MP3 + 320×240 PNG in `/tmp` → MP4; missing-thumbnail path.
4. `jobs.py` import with flags unset / set.

## How (exact commands / procedure)

```bash
cd "/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server"
nice -n 10 python3 Energy/scripts/sun_times.py ; nice -n 10 python3 Energy/scripts/sun_times.py
nice -n 10 python3 System/scripts/uptime_log.py tick
RR_DATABASE_ROOT=/tmp/rr-migr/dbtest nice -n 10 python3 System/scripts/uptime_log.py tick   # after editing last_tick_epoch −600 s in the temp copy
nice -n 10 python3 Media/Video/scripts/mp4_converter.py --audio /tmp/rr-migr/t.mp3 --thumb /tmp/rr-migr/t.png --out /tmp/rr-migr/t.mp4
```

## Pass criteria (written before running)

1. Sun times rc 0, sunrise/sunset present and plausible for late September Hawaiʻi (≈06:1x / 18:1x); second call makes no network request.
2. Uptime tick rc 0, first tick logs origin; gap > threshold logs `heartbeat_gap` + `desk_up`.
3. MP4 has h264 video + aac audio, duration ≈ input; missing thumbnail → `ok false`, rc 1; nothing written outside `/tmp`.
4. Jobs `enabled False` with flags unset.

## Result

**PASS** on all four.

- Sun: sunrise **06:11**, sunset **18:10**, next sunrise 06:11 (2026-09-30), fetched 13:26:06 HST; second call `refreshed false`.
- Uptime: `origin_start` (inferred) logged, boot_id recorded; temp-root 600 s gap → `heartbeat_gap` + `desk_up after_gap_s 600`.
- MP4: h264 + aac, duration 2.000000 s, 0.22 s elapsed, 92 MB RSS; no-thumb path rc 1.
- Jobs: `system_uptime_log False 60`, `energy_sun_times False` (hourly list); True with `RR_UPTIME_LOG=1` / `RR_SUN_TIMES=1`.

## Resource impact

| When | Load (1/5/15) | MemAvailable | Swap used | Peak RSS |
| --- | --- | --- | --- | --- |
| before | not recorded | ≈ 6.9 GB | not recorded | — |
| during | not recorded | not recorded | not recorded | 92 MB (ffmpeg run) |
| after (13:30) | 1.50 / 1.66 / 1.71 | 6 776 MB | 491 MB | — |

## Cleanup confirmation

- [x] no test process left (foreground runs)
- [x] no port opened; no lock used
- [x] no model loaded
- [x] synthetic media and temp root under `/tmp/rr-migr` deleted at the end of the pass

## Open items / caveats

- **jobs.py registration is a sign-off item** (standing rule received 13:45 HST: jobs.py only on Alexander's request or a WO). The gated blocks were added before the rule arrived and are left in place, OFF; exact blocks in Database `Logs/Migration/migration-jobs-py-additions-20260929.md`.
- Enabling `RR_UPTIME_LOG` appends to `System/uptime/uptime-events.jsonl` only on events (start / gap), but rewrites `uptime-last.json` every 60 s → Database git churn; consider git-ignoring `uptime-last.json` (**sign-off**).
- G1 sun-times consumers (hourly solar voice report) not ported yet.
- MP4 converter is on demand only; G1 broadcast integration not ported (scope decision).
