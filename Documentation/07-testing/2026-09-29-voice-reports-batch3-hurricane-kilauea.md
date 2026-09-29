# Test record — Voice reports batch 3: hurricane desk + Kīlauea report (text only)

| Field | Value |
| --- | --- |
| **Date / time (HST)** | 2026-09-29 13:41–13:44 HST |
| **Tester** | Grok Bot (desk agent, old-repo migration pass) |
| **Change under test** | Pacific `Media/Voice/scripts/voice_reports.py`: new builders `hurricane_desk` (G1 `weather/hurricane-desk/scripts/hurricane_desk.py` Hawaiʻi block) and `kilauea_report` (G1 `hourly-clip-reports` Kīlauea desk, `persona._kilauea_line` wording, + cached clip "Here is the latest Hawaiian Volcano Observatory notice, unedited for honesty."). Gated jobs `voice_hurricane_desk` (`RR_VOICE_HURRICANE`) and `voice_kilauea_report` (`RR_VOICE_KILAUEA`). [Matrix](../00-architecture/Old-Repo-Migration-Matrix.md) |
| **State** | **PASS** (text, `--no-voice`, temp output) · WAV + by-ear **VERIFY PENDING** (no model load this pass) · jobs **LANDED, gated OFF**; keeping the jobs.py registration is a **sign-off item** |
| **Evidence** | this record; jobs.py blocks in `2 - RootRecord-Database/Logs/Migration/migration-jobs-py-additions-20260929.md` |
| **Commits** | see the worklog section (auto-sync) |
| **Backup** | `/home/rootrecord/Database/GITHUB/migration-hurricane-desk.bak-20260929-133959/` (`voice_reports.py`, `jobs.py`, Voice README, Voice-Reports-G3, matrix, 07 README) |

## What was tested

1. `hurricane_desk` against the live G3 data (one tracked storm, Nolo) and against an empty Database root (no tracks, no alerts file).
2. `kilauea_report` against Database `Geology/` (collector run 13:19 HST) and against an empty root.
3. `speakers.is_live` for both kinds (real → True; empty → False, so no WAV is made from an empty desk).
4. Regression: `earthquake_report` (`RR_VOICE_QUAKE_DRY=1`) and `nws_weather` still build.
5. jobs.py import with flags unset / set; no duplicate ids.

## How

```bash
cd "/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server/Media/Voice/scripts"
RR_VOICE_REPORT_OUT=/tmp/rr-migr/voice-test nice -n 10 python3 voice_reports.py hurricane_desk --no-voice
RR_VOICE_REPORT_OUT=/tmp/rr-migr/voice-test nice -n 10 python3 voice_reports.py kilauea_report --no-voice
RR_DATABASE_ROOT=/tmp/rr-migr/emptydb RR_VOICE_REPORT_OUT=/tmp/rr-migr/voice-test nice -n 10 python3 voice_reports.py hurricane_desk --no-voice   # and kilauea_report
```

## Pass criteria (written before running)

1. rc 0; every number in the text is present in the source files (no invented storms, levels or counts).
2. Empty data → an explicit "not on file" / "no system" sentence and `is_live` False.
3. No write outside `/tmp/rr-migr/voice-test`; no WAV; no delivery.

## Result

**PASS.**

- `hurricane_desk` (0.08 s, 20 MB RSS): "Hurricane global desk, Pacific Root Server. Nearest Hurricane from a Hawaiian island. Hurricane Nolo is about 273 nautical miles from Līhuʻe. Center 21.3 north, 164.2 west. It bears west of Līhuʻe. Moving north at about 8 knots, holding roughly steady relative to Hawaii. Maximum sustained winds 85 knots. No tropical watches or warnings for Hawaii in the last NWS pull. Stay with NWS Honolulu for watches and warnings." Source: `Nolo_20260929T015012…/track.json` (44 polls, 4 distinct fixes 20.1→21.3 N, 100→85 kt, last poll 13:26:29 HST); NWS HI alerts: High Surf Advisory only (not tropical).
- Empty root: "…No tropical system with a mapped position is on the board. NWS Hawaii alert data is not on file…" (`is_live` False). The "not on file" wording was added after the first empty run said "no watches in the last NWS pull" with no NWS file present.
- `kilauea_report` (0.12 s, 20 MB RSS): "Kilauea Report. It's one forty three p.m. Hawaiian Standard Time. Kilauea volcano alert level: watch, aviation color code orange. Kilauea is erupting. Here is the latest Hawaiian Volcano Observatory notice, unedited for honesty. The Halemaʻumaʻu eruption of Kīlauea volcano is currently erupting small overflows from both the north and south vents. It is not possible to forecast the onset of episode 55 fountains or if they will occur. USGS: 10 earthquakes magnitude 1 or greater within 150 kilometers of Kilauea in the last 24 hours. Mauna Loa alert level: normal." Empty root → "Kilauea: DOWN." (`is_live` False, G1 wording).
- Regression: `earthquake_report` 7 sentences, `nws_weather` 5 sentences, rc 0.
- jobs: `voice_hurricane_desk False`, `voice_kilauea_report False` unset; True with flags set; 42 ids, no duplicates.

## Deviations from G1 (documented, deliberate)

- Hurricane: G1 read a global NHC/RAMMB/JTWC board; G3 tracks only Hawaiʻi-relevant NHC storms, so the G1 "Around the world right now, N tropical systems" sentence is replaced by a Hawaii-tracking-board sentence (only when > 1 storm). Movement speed/direction is estimated from the last two distinct fixes (G1 used the feed's movement fields, which G3 `track.json` does not store). Coordinates are spoken as "21.3 north, 164.2 west" instead of "21.3N 164.2W". G1 radio sign-off / OBS / Telegram `notify_report` not ported.
- Kīlauea: G1 `rr-kilauea` public report used Grok generation + a Discord draft queue — **BLOCKED** (spend + posting). This port is the template desk only. Schedule :03 (G1 :02) so it never shares the single-flight lock with the :02 roll-ups.

## Resource impact

| When | Load (1/5/15) | MemAvailable | Swap used | Peak RSS |
| --- | --- | --- | --- | --- |
| before (13:39) | not recorded | 6 985 MB | not recorded | — |
| during | not recorded | not recorded | not recorded | 20 MB |
| after (13:45) | 1.66 / 1.78 / 1.77 | 6 949 MB | 492 MB | — |

## Cleanup confirmation

- [x] no process left (foreground runs)
- [x] no port, lock or model used
- [x] `/tmp/rr-migr/voice-test`, `/tmp/rr-migr/emptydb` deleted at the end of the pass

## Open items

- WAV render + by-ear check for both (first run after sign-off, via `voice-render.sh`, single-flight) — VERIFY PENDING.
- "Kilauea"/"Hawaii" spelled without ʻokina in spoken text (matches the other G3 reports and G1 clip catalog); pronunciation review is a lexicon item.
