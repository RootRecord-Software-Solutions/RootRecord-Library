# Test record — Geology collector (USGS earthquakes + HVO), earthquake voice report, Kīlauea cams, quake backfill

| Field | Value |
| --- | --- |
| **Date / time (HST)** | 2026-09-29 13:18–13:24 HST |
| **Tester** | Grok Bot (desk agent, migration-geology pass) |
| **Change under test** | New Pacific `Geology/scripts/{geology_collect,kilauea_cams,earthquakes_backfill}.py`; `voice_reports.py earthquake_report`; gated `jobs.py` entries `geology_collect`, `geology_kilauea_cams`, `voice_earthquake_report`. WO-SRV / WO-ECO; [matrix](../00-architecture/Old-Repo-Migration-Matrix.md) |
| **State** | **PASS** (one manual run each) · jobs **LANDED, gated OFF** (take effect only at the next poller start with the flag set) · earthquake WAV **VERIFY PENDING** (not rendered: no model load this pass) |
| **Evidence** | `2 - RootRecord-Database/Logs/Migration/migration-geology-evidence-20260929T2319Z.md` |
| **Commits** | see "Commits" below (auto-sync; checked with read-only `git log`) |
| **Backup** | `/home/rootrecord/Database/GITHUB/migration-geology.bak-20260929-131652/` |

## What was tested

1. `geology_collect.py all` — USGS FDSN Hawaiʻi bbox (M≥1, 24 h), USGS `2.5_day.geojson` global, HANS `getMonitoredVolcanoes` + `getNewestOrRecent` → Database `Geology/`.
2. Dedupe (second run) and failure path (1 ms timeout) — temp root `/tmp/rr-migr/dbtest` only.
3. `voice_reports.py earthquake_report --no-voice` twice (new-since-last-report state), plus the empty-data path and the `is_live` gate.
4. `kilauea_cams.py` (USGS V1/V2/V3 stills; second run in temp root for the conditional GET).
5. `earthquakes_backfill.py --days 1 --skip-global` (real) and `--days 2` (temp root).
6. `jobs.py` import check with flags unset / set.

## How (exact commands / procedure)

```bash
cd "/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server/Geology"
/usr/bin/time -f 'elapsed=%es maxrss=%MKB' nice -n 10 python3 scripts/geology_collect.py all
RR_DATABASE_ROOT=/tmp/rr-migr/dbtest nice -n 10 python3 scripts/geology_collect.py all            # dedupe
RR_DATABASE_ROOT=/tmp/rr-migr/dbtest RR_GEOLOGY_TIMEOUT=0.001 nice -n 10 python3 scripts/geology_collect.py quakes
cd ../Media/Voice/scripts && RR_VOICE_REPORT_OUT=/tmp/rr-migr/voice-test nice -n 10 python3 voice_reports.py earthquake_report --no-voice   # x2
cd ../../../Geology && nice -n 10 python3 scripts/kilauea_cams.py && nice -n 10 python3 scripts/earthquakes_backfill.py --days 1 --skip-global
python3 -c 'import importlib.util…jobs.py…'   # enabled flags, see evidence §8
```

## Pass criteria (written before running)

1. Collector rc 0, every source `ok`, each HTTP call < 10 s, last-json + Daily JSONL written under Database `Geology/`.
2. Kīlauea and Mauna Loa alert level / color code present and equal to HANS; no invented values.
3. Second run appends 0 duplicates; a failed source keeps its last good file.
4. Voice report text lists only events from the last-json; second run says "No new …"; no WAV, no delivery.
5. Jobs import with `enabled False` when flags are unset.

## Result

**PASS** on all five.

- Collector: rc 0, 2.64 s wall, 28 MB RSS; hawaii 633 ms (10 events, 1 new M≥2 `hv75045217` M2.35 14 km S of Fern Forest), global 303 ms (33, largest M5.6 southern Mid-Atlantic Ridge), HVO notices 1 029 ms (44), HVO status 572 ms (8 volcanoes).
- **Kīlauea WATCH / ORANGE** (Daily Update 2026-09-29 19:02 UTC: "Numerous rapid cycles of south vent overflows and drainback occurred overnight within Halema'uma'u crater…"; latest VAN/VONA: "…currently erupting small overflows from both the north and south vents…"), erupting `true`, multiplier 2.5. **Mauna Loa NORMAL / GREEN** (Monthly Update), erupting `null` (not stated).
- Dedupe: HVO notices new 0 on re-run; timeout run rc 1 with `URLError timed out` in `collector-last.json`, `hawaii-last.json` untouched.
- Voice: run 1 19 sentences, run 2 "USGS earthquake report at one twenty p.m. Hawaiian Standard Time. No new Hawaii earthquakes since the last report. Hawaii last twenty four hours: 0 magnitude 2.5 or greater. No new global earthquakes since the last report. Global last twenty four hours: 33 magnitude 2.5 or greater." `is_live` True; empty data → "Earthquake data is not on file.", `is_live` False.
- Cams: 3 × http 200 (325 865 / 188 366 / 331 908 B); temp-root re-run 3 × 304.
- Backfill: 11 Hawaiʻi rows (real, 1 day); temp root `--days 2`: 27 Hawaiʻi + 99 global upserted in ~18 s (1 s polite sleep per chunk).
- Jobs: `geology_collect False 300`, `geology_kilauea_cams False 600`, `voice_earthquake_report False [8]`; all True with the flags set.

## Resource impact

| When | Load (1/5/15) | MemAvailable | Swap used | Peak RSS |
| --- | --- | --- | --- | --- |
| before (13:18) | not recorded | 6 961 MB | not recorded | — |
| during | not recorded | not recorded | not recorded | 28 MB (collector) |
| after (13:30) | 1.50 / 1.66 / 1.71 | 6 776 MB | 491 MB | — |

## Cleanup confirmation

- [x] no test process left (all runs were foreground, rc returned)
- [x] no port opened; single-flight lock not used
- [x] no model loaded (WAV render not run)
- [x] temp roots `/tmp/rr-migr/dbtest`, `/tmp/rr-migr/voice-test` deleted at the end of the pass

## Open items / caveats

- **jobs.py registration is a sign-off item** (standing rule received 13:45 HST: jobs.py only on Alexander's request or a WO). The gated blocks were added before the rule arrived and are left in place, OFF; exact blocks in Database `Logs/Migration/migration-jobs-py-additions-20260929.md`.
- Poller PID 105444 was **not** restarted; nothing is scheduled until the next poller start with `RR_GEOLOGY=1` (and `RR_VOICE_QUAKE=1`, `RR_KILAUEA_CAMS=1`) — **sign-off**.
- Earthquake WAV render + by-ear check **VERIFY PENDING** (first run after sign-off, through `voice-render.sh`, single-flight).
- Git churn if enabled: `*-last.json` rewrite every 5 min + Daily append (Database auto-sync). Stills are git-ignored.
- Not ported (sign-off): Telegram/Discord posts, Grok drafts, playback, OBS.

## Addendum — G0 nearest-location tag (2026-09-29 13:49 HST)

- Change: `geology_collect.py` `nearest_location()` (port of G0 `old/operations/earthquakes/global/poller.py` `nearest()`, 250 km cut-off) adds `nearest` {location_id, name, country_code, admin1_code, km} to every event; dataset `Geology/config/global-locations.json` is a verbatim copy of G0 `old/config/locations/global-locations.json` (sha256 `5defe5c7c262efc2dc679fb3bf31503f307f556de6cf7a5cfd893d973348b49a`, 306 public places). Backup `/home/rootrecord/Database/GITHUB/migration-quake-locations.bak-20260929-134920/`.
- Pass criteria: rc 0; each tag ≤ 250 km; untagged events have `nearest: null`; no change to counts/dedupe.
- Temp root 13:49:45: rc 0, 1.10 s, 28 MB; Hawaiʻi 9/9 tagged (e.g. M1.72 "5 km SSW of Pāhala" → Volcano Village 40.5 km; M1.78 "1 km WNW of Captain Cook" → Kailua-Kona 16.3 km), global 14/34 (e.g. M4.5 Colombia → Bogotá 188.4 km; M4.8 Tonga → Nukuʻalofa 223.0 km; M4.7 Philippines untagged).
- Real run 13:49:55 (`quakes` only): rc 0, 1.09 s, 28 MB; Hawaiʻi new 1 (`hv75045507`, tagged), global new 1; Daily files 11 / 34 lines, no duplicates. **PASS.**
- Regression: `earthquake_report` text build unchanged (reads mag/place only).

## Commits

Pacific `0399076` (collector + voice), `b2c4973` (cams + backfill), `cd48536` (jobs gates); Database `e8854f0` (first Geology data), `101d05a` (`.gitignore` + cams); later doc commits in the worklog section.
