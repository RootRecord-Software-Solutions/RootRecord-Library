# Test record: old-repo ports, breadth batch 5 (voice fixes, Hawaiʻi news seeds, HLS, official / boot voice reports, report board, load categories, global hurricane board, host hardware, speech scrub, scheduler map)

| Field | Value |
| --- | --- |
| **Date / time (HST)** | 2026-09-29 14:16–14:40 HST |
| **Tester** | Grok Bot (desk agent, old-repo migration breadth pass 2; documentation steering 14:27) |
| **Change under test** | Fixes to the pass-1 voice text in `Media/Voice/scripts/speakable.py` and `voice_reports.py`. News: `Reports/News/scripts/{_collector,hawaii_news}.py` seed feeds. New ports from G1: `official-weather-media` (HLS part) → `Weather/scripts/official_statement.py` plus voice `official_weather`; `boot` prelims → voice `boot_brief`; `reports/sort/daily-report-board` + `daily-reports-catchup` → `Reports/scripts/report_board.py`; `load-categories` → `Energy/scripts/load_categories.py`; `weather/hurricane-tracker` → `Weather/hurricanes/scripts/global_board.py`; `host-metrics` (temp / drives / GPU / NPU) → `System/scripts/host_hw.py`; `persona/scripts/speech_scrub.py` → `Media/Voice/scripts/speech_scrub.py`. Plus the new verification doc [G1-Scheduler-To-G3-Jobs-Map](../00-architecture/G1-Scheduler-To-G3-Jobs-Map-2026-09-29.md). See the [Matrix](../00-architecture/Old-Repo-Migration-Matrix.md). |
| **State** | **PASS** on all 11 smoke tests. The voice reports are PASS on text only; their WAV renders are **VERIFY PENDING** because no model loads were done. All new jobs are **PROPOSED and not registered** (standing rule: no jobs.py edits). The blocks are in [Pending-Job-Registrations-2026-09-29](../00-architecture/Pending-Job-Registrations-2026-09-29.md). |
| **Gate flags (proposed)** | `RR_OFFICIAL_HLS`, `RR_VOICE_OFFICIAL`, `RR_VOICE_BOOT`, `RR_REPORT_BOARD`, `RR_HURRICANE_GLOBAL`. `reports_hawaii_news` gains env `RR_NEWS_SEEDS_ONLY=1`. |
| **Backup** | `/home/rootrecord/Database/GITHUB/migration-breadth2.bak-20260929-141732/` holds pre-edit copies of 24 files. |
| **Rules kept** | nice 10. MemAvailable stayed ≈ 6.6–7.0 GB. No sends, no playback, no model loads. No poller or service restart (PID 105444 untouched). No git writes, since auto-sync commits. G1 / G0 code kept (nothing retired). Temp roots under `/tmp/rr-migr2/` were deleted after the pass. |

Common prefix for every command: `cd "/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server"`.

## Voice text fixes

Fixes the three pass-1 check-later items ([batch 4](./2026-09-29-old-repo-ports-breadth-batch4.md#check-later-alexander)).

```bash
python3 -c 'import sys; sys.path.insert(0,"Media/Voice/scripts"); import speakable as s; print(s.spoken_clock(14,1), s.spoken_clock(9,5), s.spoken_clock(0,7))'
for r in solar_desk security_desk bandwidth_desk energy_report morning_report kilauea_report; do RR_VOICE_REPORT_OUT=/tmp/rr-migr2/voice nice -n 10 python3 Media/Voice/scripts/voice_reports.py $r --no-voice; done
```

| Fix | Result | Observed |
| --- | --- | --- |
| Clock minutes 1–9 (`speakable.spoken_clock`) | **PASS** | Now "two oh one p.m.", "nine oh five a.m.", "twelve oh seven a.m." (before: "two one p.m."). The phrase-clip catalog uses only :00 / :30, so no cached clip changes. |
| Watts wording (`spoken_watts`) | **PASS** | 0 / 0.0 → "zero watts", 1 → "one watt", others are rounded ("144 watts"). An all-zero device is spoken as "idle"; the `.md` keeps the "N W" figures. |
| Sun times (`spoken_hhmm`) | **PASS** | "Sunrise was six eleven a.m., sunset is six ten p.m." The simulated 19:05 run gives "Sunset was six ten p.m.; next sunrise six eleven a.m.". The ".." double period is fixed. |
| Re-smoke of 6 reports | **PASS** | All rc 0, 0.1–0.64 s, ≈ 21 MB RSS. Solar desk: "Delta 2: state of charge 49%, solar input 144 watts, AC out 86 watts. River 2 Pro: state of charge 100%, idle." Energy report: "solar input zero watts, output zero watts." |

**Check later**
- [ ] `spoken_clock` is shared, so the new wording also reaches `system_perf`, `voice_asr_check`, `hourly_chime` and the `speakable` dates. Listen to one of each once WAVs are allowed.
- [ ] WAV renders VERIFY PENDING (Bruce / Carly / Ava).

## Hawaiʻi news seed feeds

```bash
RR_DATABASE_ROOT=/tmp/rr-migr2/news-seeds-only RR_NEWS_SEEDS_ONLY=1 nice -n 10 python3 Reports/News/scripts/hawaii_news.py
RR_DATABASE_ROOT=/tmp/rr-migr2/news-full nice -n 10 python3 Reports/News/scripts/hawaii_news.py
```

| Item | Result | Observed |
| --- | --- | --- |
| Seeds-only run | **PASS** | rc 0, 11.6 s, 32 MB. All 16 feeds ok, **278 posts**: Maui County 134, 10 each from most state departments, tax 9, HI-EMA 5. The oldest post is from 2013-11-02 (Maui archive). |
| Full run (seeds + G0 discovery) | **PASS** | rc 0, 22.8 s. Same 278 posts, plus the same 25 × HTTP 404 from discovery (harmless). |
| Newest posts | OK | Maui SMA meeting reminder; Hawaiʻi National Guard on Hurricane Nolo; the Governor's Land Use Commission appointments. |
| Seed list (`SEED_FEEDS`, each checked for 200 with items) | — | governor, ltgov, health/news, dlnr, hidot, dod/hiema, dod, ag, labor, cca, humanservices, energy, dbedt, dab (hdoa redirects to it), tax, plus Maui County `RSSFeed.aspx?ModID=1&CID=All-newsflash.xml`. |
| Rejected | — | 200 but 0 items: health `/feed/`, the dlnr blog, honolulu.gov. 403: dcr, Hawaiʻi County. 404: Kauaʻi. |

**Check later**
- [ ] Review the seed list. The Maui County feed is not hawaii.gov, and there are no working Honolulu / Hawaiʻi County / Kauaʻi feeds.
- [ ] Confirm the target Database `Reports/News/hawaii/` (DB git-ignored; `hawaii-news-last.json` is tracked when run for real, which has not happened yet).
- [ ] Register `reports_hawaii_news` (`RR_HAWAII_NEWS`, 10:00, env `RR_NEWS_SEEDS_ONLY=1`, timeout 300).

## Official statement fetcher (HLS)

```bash
RR_DATABASE_ROOT=/tmp/rr-migr2/wx nice -n 10 python3 Weather/scripts/official_statement.py   # twice
nice -n 10 python3 Weather/scripts/official_statement.py   # one real run 14:27 (git-ignored path)
```

| Item | Result | Observed |
| --- | --- | --- |
| First run | **PASS** | 1.1–1.7 s, 26 MB. The api.weather.gov HLS (HFO) issued 2026-09-27T03:15Z (2026-09-26 17:15 HST, Nolo advisory 26), 7014 chars. Writes `Weather/Hawai'i/official/HLS_current.txt` and `official-last.json`. |
| Second run | **PASS** | `changed=False` (same product id). |
| Real Database run | OK | 14:27 HST. Under `/Weather/`, which is git-ignored, so no churn. |

**Correction:** the G3 weather poller already fetches HWO (log: "no products in @graph", meaning none is issued now) and AFD / SFP / ZFP / CWF / NOW. Only HLS was missing: it was defined in `hurricanes/scripts/sources.py` but never fetched. This script fills that gap and leaves the poller's product list unchanged.

**Check later**
- [ ] Register `weather_official_hls` (`RR_OFFICIAL_HLS`, 600 s).
- [ ] The api.weather.gov → product.php fallback path has not been exercised live.

## Official weather voice report

```bash
RR_VOICE_REPORT_OUT=/tmp/rr-migr2/voice nice -n 10 python3 Media/Voice/scripts/voice_reports.py official_weather --no-voice
```

| Item | Result | Observed |
| --- | --- | --- |
| Live data | **PASS (text)** | The HLS was 69 h old (more than 24 h, `OFFICIAL_MAX_H`) and no HWO was issued, so the report used the AFD. `_speech_product` strips the WMO header and UGC codes; the text is capped at 4500 chars and uses the G1 fallback wording. |
| Fresh-HLS path / no-product path | **PASS** | Unit-tested with a fresh stub HLS (used first) and with no products (G1 "no official statement" line). |

**Check later**
- [ ] 24 h freshness rule for the HLS: is that right?
- [ ] A full AFD is long (4500-char cap) and full of NWS abbreviations. Trim to the synopsis?
- [ ] HWO path untested live (none issued).
- [ ] Register `voice_official_weather` (`RR_VOICE_OFFICIAL`, :25), or trigger it on an HLS change instead. WAV VERIFY PENDING.

## Boot brief voice report

```bash
RR_VOICE_REPORT_OUT=/tmp/rr-migr2/voice nice -n 10 python3 Media/Voice/scripts/voice_reports.py boot_brief --no-voice
```

| Item | Result | Observed |
| --- | --- | --- |
| Midday edition | **PASS (text)** | "Boot report, midday edition… came up at two twenty eight a.m., about 12 hours ago… Kilauea alert level watch, erupting. Hurricane Nolo is about 270 nautical miles from Līhuʻe…" plus batteries and CPU / memory. |
| Import | **PASS** | The `BUILD` dict was moved below the new builders (fixing a NameError). The module imports cleanly with 15 reports. |

**Check later**
- [ ] Wording of "about N hours ago" / minutes.
- [ ] Register ON_BOOT `voice_boot_brief` (`RR_VOICE_BOOT`). The command runs `geology_collect.py` first so Kīlauea data is fresh. WAV VERIFY PENDING. Morning replay landed 2026-09-30 as `Media/MorningBootReplay` (dry-run only; speakers off).

## Report board and catch-up ledger

```bash
RR_DATABASE_ROOT=/tmp/rr-migr2/board RR_VOICE_REPORT_OUT=/tmp/rr-migr2/board/out nice -n 10 python3 Reports/scripts/report_board.py status
RR_DATABASE_ROOT=/tmp/rr-migr2/board RR_VOICE_REPORT_OUT=/tmp/rr-migr2/board/out nice -n 10 python3 Reports/scripts/report_board.py run-due   # twice
nice -n 10 python3 Reports/scripts/report_board.py bogus   # rc 2
```

| Item | Result | Observed |
| --- | --- | --- |
| `status` | **PASS** | rc 0. Slots are morning 09:02 and midday 12:02 (mandatory, with catch-up) and late 21:02 (optional). |
| `run-due` | **PASS** | Midday was due, so it ran the text roll-up (0.65 s, 21 MB). The second run gave `nothing_due`. |
| Day rollover (simulated) | **PASS** | Yesterday's morning report was marked missed; late gave `skipped_optional`. |
| Bad argument | **PASS** | rc 2 usage. |

**Check later**
- [ ] Should `Reports/board/daily-reports-due.json` be tracked in git? So far it was written only to a temp root.
- [ ] Slot times follow the G3 roll-ups (09:02 / 12:02 / 21:02), not the G1 board times.
- [ ] `--voice` renders the WAV (no playback). Keep it off in the job until WAVs are verified.
- [ ] Register `reports_board_catchup` (`RR_REPORT_BOARD`, 14:00).

## Load categories

```bash
nice -n 10 python3 Energy/scripts/load_categories.py
nice -n 10 python3 Energy/scripts/load_categories.py --input /tmp/rr-migr2/lc-night.json
```

| Item | Result | Observed |
| --- | --- | --- |
| Live BLE last-files | **PASS** | real 0.05 s, 14 MB. "Starlink / lights 68 W", "house AC \| PV charging". |
| Night scenario | **PASS** | transfer 290 W, E-Batt callout 120 W. |

**Check later**
- [ ] G3 has no USB-A / 12 V / car fields (`car_w` = 0). The G1 thresholds need Alexander's check.
- [ ] G1 `append_history` was not ported, because it deleted old logs.

## Global hurricane board

```bash
RR_DATABASE_ROOT=/tmp/rr-migr2/gb nice -n 10 python3 Weather/hurricanes/scripts/global_board.py
```

| Item | Result | Observed |
| --- | --- | --- |
| Sources | **PASS** | 2.9 s, 30 MB. NHC, RAMMB, JTWC ABPW and ABIO all ok. |
| Storms | **PASS** | 7: Nolo (ep, 80 kt, 270 nm), TD Nineteen-E, Fay, Hanna, Polo, Rachel, Surigae (wp, from RAMMB). |

**Check later**
- [ ] G1 labels double up ("Fay Fay", "Tropical Storm Surigae SURIGAE").
- [ ] Confirm the target folder `Weather/Hawai'i/hurricanes/global/` (git-ignored) and the schedule (G1 05/09/12/16/20 :40).
- [x] RAMMB per-storm pages / track tables and the storm plot landed 2026-09-29 in `Weather/hurricanes/scripts/storm_track.py`, `storm_plot.py`, and `global_board.refresh()`. Fixture test PASS (no live network). OBS wiring is still a later function.

## Host hardware

```bash
nice -n 10 python3 System/scripts/host_hw.py
```

| Item | Result | Observed |
| --- | --- | --- |
| Snapshot | **PASS** | 0.22 s, 18.5 MB. Temp 48.0 °C (acpitz). nvme0n1 56.5% (250.6 / 467.3 GB). GPU "AMD Krackan2 (rev c8)" 1%. NPU present, 0%. |

**Check later**
- [ ] NPU busy % reads `/proc/*/fdinfo`, which covers only processes this user can read.
- [ ] Not ported: `reset_series.py` (moves live history files, BLOCKED), laptop battery, and the Windows PDH counters.

## Speech scrub

```bash
printf 'Here is the forecast. As an AI language model I cannot feel. Rain tonight.' | nice -n 10 python3 Media/Voice/scripts/speech_scrub.py
```

| Item | Result | Observed |
| --- | --- | --- |
| Scrub | **PASS** | Vendor, "As an AI" and constraint sentences are removed; the rest is kept. Empty input gives ''. |

**Check later**
- [ ] Not wired into `voice_reports.py` or the chat path. Decide whether to apply it to Grok / LLM text before TTS.

## Scheduler map verification

Read-only comparison of the G1 `scheduler-clock` `add_job` calls against G3 `jobs.py` and the Pending doc → [G1-Scheduler-To-G3-Jobs-Map-2026-09-29](../00-architecture/G1-Scheduler-To-G3-Jobs-Map-2026-09-29.md).

| Item | Result | Observed |
| --- | --- | --- |
| Coverage | **PASS** | All 64 unique G1 job ids (73 `add_job` calls) are mapped to LIVE / GATED / PROPOSED / ON DEMAND / BLOCKED / OUT. |

**Check later**
- [x] G3 night-sleep gate armed 2026-09-30 00:02 HST (`RR_NIGHT_SLEEP=1` in `run-poller.sh`, WO-MIG-01). `--check` PASS 23:59 HST. Live restart active; no `night-mode.json`, so no night-sleep skips.
- [x] The G1 23:30 late-final report was re-added 2026-09-29 as gated `voice_late_final_report` (`RR_VOICE_LATE_FINAL`). Dry-run PASS 23:59 HST: `would-run` (late slot open), no `late_report_current.md`, no WAV.

## Reviewed, still BLOCKED / OUT

- Kīlauea cams YouTube live-id scraping: used only for OBS embeds, so it falls under the OBS blocker.
- Sunrise-restore, morning boot replay, report readiness: speaker playback.
- Council health / Bruce stats: bot tokens, a model load and Telegram sends.
- python-drop-runner (runs arbitrary code), fs-index (private paths), broadcast (file browser): security scope or design. Context session builder: WO-MIG-43 library, no listener (2026-09-30).
- Host `reset_series.py`: moves live history files aside (data-moving).
- Row 21 Ollama idle-stop: superseded by keepalive 0. Row 88 audio clips: regenerated in G3. Rows 69 / 78 / 90: Library or archive decisions. Product / website rows: OUT of scope.
