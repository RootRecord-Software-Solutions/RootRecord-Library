# Voice desk — current as of 2026-10-02

Finished Hawaii reports go to the Mainland station. The station snapshots the playlist at `HH:29:59` and `HH:59:59`, then chimes on the hour and the half hour. Voice jobs render before that snapshot. The station is on the air at `https://radio.rootrecord.cloud/radio/live.mp3`. The operator page is [2026-10-01 radio station](./2026-10-01-radio-station.md).

This is the living description of the spoken reports. The 2026-09-29 port record is [Voice-Reports-G3](../10-AI-and-Agent-Runtime/Voice-Reports-G3.md). Where that file still says a job is off, has no delivery, or uses an old minute, this file wins. Trust `Automations/scripts/poller/run-poller.sh` and `Automations/scripts/jobs.py` over older “what stays off” lists.

## Current as of 2026-10-02 00:39 HST

Verified against live Pacific `Automations/scripts/jobs.py` and `Automations/scripts/poller/run-poller.sh` after the poller start at 00:09 HST. Spoken change lines and staged on-air cues checked against `Media/Voice/scripts/` as of 00:34 HST. Database root is `2 - RootRecord-Database`. Voice MD default is ecosystem `test-reports/Voice/` (`RR_VOICE_REPORT_OUT`).

### Shared pipeline

`jobs.py` → `voice_reports.py` / `system_perf.py` → build MD → `write_md` (+ Archive) → `voice-render.sh` / `voice_generate` mode_stitch (Kokoro, single-flight) → `voice_deliver` (Telegram when `RR_VOICE_DELIVER=1`) → `radio_push` (default on; set `RR_RADIO_PUSH=0` to skip) → Discord `report_relay` every 300 s → `publish_report_pages` → site `/reports/<slug>`.

Personas (Kokoro): Ava `af_heart`, Bruce `am_echo`, Carly `af_nova`. All speeds 1.0. Output is 24 kHz, 16-bit, mono WAV under Database `Media/Audio/Voice/`.

`RR_VOICE_DELIVER=1` and `RR_TELEGRAM_DEST=council` are the defaults in `run-poller.sh`. A council post is a voice note and the measured report. Unchanged spoken text is not sent again. Flags are read when the poller starts. A script edit is picked up on the next run of that job. A new `jobs.py` entry is not, until the poller is started again.

### Always on (hard-enabled in jobs.py)

| Job | Schedule (HST) |
| --- | --- |
| `worklog_scan` | every 90 s |
| `discord_report_relay` | every 300 s |
| `voice_timing_report` | :05 |
| `reports_daily_roll_up` | 18:30 |
| `reports_weekly_archive` | 19:00 |
| `discord_report_8h` | 00:00, 08:00, 16:00 |
| `discord_report_24h` | 12:00 |

### Armed voice desks (`run-poller.sh` defaults these flags to 1)

| Minute / time | Who | Report | Flag |
| --- | --- | --- | --- |
| :12 and :42 | Bruce | System | `RR_VOICE_SYSTEM_PERF` |
| :12 and :42 | Ava | NWS | `RR_VOICE_NWS` |
| :12 and :42 | — | Energy look | `RR_VOICE_ENERGY` (refreshes camera look; no separate voice note; Bruce speaks it on solar) |
| :12 and :42 | Bruce | Remaining tasks | `RR_VOICE_REMAINING` |
| :12 and :42 | Carly | Earthquakes | `RR_VOICE_QUAKE` (+ `RR_GEOLOGY`) |
| :12 and :42 | Carly | Kīlauea | `RR_VOICE_KILAUEA` |
| :12 and :42 | Bruce | Solar desk | `RR_VOICE_SOLAR` |
| :12 and :42 | Carly | Security | `RR_VOICE_SECURITY` |
| :12 and :42 | Carly | Bandwidth | `RR_VOICE_BANDWIDTH` (+ `RR_NET_SAMPLES`) |
| :12 and :42 | Ava | Current | `RR_VOICE_CURRENT` |
| :36 | rotating | News update | `RR_RADIO_NEWS` |
| 09:02, 12:02, 21:02 | Ava | Daypart roll-ups | `RR_VOICE_ROLLUPS` |
| 23:02 | Ava | Late final (text) | `RR_VOICE_LATE_FINAL` |
| 05:40, 09:40, 12:40, 16:40, 20:40 | Carly | Hurricane | `RR_VOICE_HURRICANE` |

The desks share one poller thread and one voice lock, so they run one after another. Energy runs before the solar desk. The current report runs last. `:12` and `:42` start 18 minutes before the station locks the playlist at `:29:59` and `:59:59`. A file that arrives after the snapshot waits for the next cycle.

Morning, midday, and late roll-ups stay at 09:02, 12:02, and 21:02. The 09:00 snapshot is taken at 08:59:59, while the late roll-up is still the one on the air, so the new morning file first plays at 09:30. Noon first plays at 12:30. Nine at night first plays at 21:30.

News at `:36` and the hurricane desk at `:40` finish before the top-of-hour stack.

### OFF / gated (not exported in run-poller.sh, or hard-off)

| Flag / job | Report |
| --- | --- |
| `RR_VOICE_HOURLY_CHIME` | :00 and :30 chimes. Job exists in `jobs.py`. Flag is **not** in `run-poller.sh`, so a normal start leaves it off. Station chime is separate. |
| `RR_AI_REPORT` | `ai_processing_report_hourly` |
| `RR_AI_USAGE` | `ai_usage_report` |
| `RR_TEMPLATE_REPORTS` | `template_reports_daily` (18:40) |
| `RR_HURRICANE_RADIO` | `media_hurricane_radio` |
| `RR_REPORT_BOARD` | `reports_board_catchup` |
| `RR_NOTE_DRAFT` | `note_work_draft` |
| `RR_BRUCE_STATS` | `bruce_stats_posts` |
| (no job) | `official_weather` — Discord route exists; **not** in `jobs.py` |
| (no job) | `boot_brief` — Discord route exists; **not** in `jobs.py` |

Speakers stay off. `Media/Playback` is dry-run unless `RR_PLAYBACK=1` and `--play`.

Scripts proposed only (README gates; not in `jobs.py`): News (hawaii/state/global), economy_brief, cloud_narrative. CloudNarrative README names a `cloud_narrative_dry_run` jobs.py entry; that id is absent.

### Known gaps (code wins)

1. Hourly chime gate is not in `run-poller.sh`.
2. `official_weather` / `boot_brief`: Discord `report-channels.json` routes yes; `jobs.py` entries no.
3. `current_report`: generated at :12/:42; missing from `Communications/Discord/config/report-channels.json` (site `publish_report_pages.py` still lists it in AREAS and has a separate CURRENT_MD path).
4. CloudNarrative README claims a `jobs.py` entry — absent.
5. `system_perf.py` docstring still says `only_at_minutes=[6]`; jobs schedule is `[12, 42]`. `voice_reports.py` module doc now matches generation-clock stamping and the 09:02 / 12:02 / 21:02 roll-ups (no longer claims `current_report` at :00/:30).
6. `ai_processing_report.py` file header says out under Database `Logs/AI/Reports/`; live `OUT_DIR` default is ecosystem `test-reports/AI-Processing/`. `template_fill.py` header and jobs description say Database `Reports/Generated/`; live `OUT_DIR` default is ecosystem `test-reports/Templates/`.
7. Older ops “what stays off” lists that still name roll-ups, late-final, or hurricane as off are history. `run-poller.sh` arms them.

### How long a desk takes

The current measurement is [voice timing](./voice-timing.md). `voice_timing_report` rewrites that page from the automations log at :05. It follows the Documenter handoff template and does not call a model.

Geology collection (`RR_GEOLOGY`) and network samples (`RR_NET_SAMPLES`) also default to 1, because the quake and bandwidth notes read those files.

## Hawaii, and host temperature

`Hawaii` and `Hawaiian` are spoken as those English words. The old syllable spelling is not used. Other place names still use the English respell in `hawaiian_lexicon.py` (Kīlauea is one token, `keelah-wayuh`; Mauna Loa is `mownah-lowah`). A comma plus a USPS state code is spoken as the state name.

A bare `degrees` after a number is still spoken as Fahrenheit, because the weather numbers are Fahrenheit. The system report says `degrees Celsius` on purpose. The sensor is `acpitz`, in Celsius. The written row is `°C`.

## Energy speech

Readings older than 30 minutes are "out of range." A last reading of 5 percent or less that is older than 30 minutes is "discharged and powered off," and the report does not list that pack's watts. A current channel 1 still is not given an age. An older still is "N minutes old."

Generator and transfer use watts, and the same rules are in the voice, the BLE charge source, and the load categories:

| Reading | Meaning |
| --- | --- |
| Delta 2 AC in greater than 550 W | Generator. 550 itself is not. |
| River 2 Pro AC in greater than 300 W | Generator, unless the next row matches. 300 itself is not. |
| Delta AC out matches River AC in | Transfer from the Delta to the River, not a generator on the River. Both watts at least 20, and the gap no larger than 40 W or 12 percent of the larger number. |
| A stale file that says 0 W | Not a generator. |

## Channel 1 solar look

Once per clock hour, the `:12` energy run asks `Security/Cameras/panel_look.py` and the local vision model `gemma4:e4b` about the newest channel 1 still, and only when that hour has no reading yet. The `:42` run reuses that sentence and does not send a note. The cache is Database `Energy/vision/ch1-look-last.json`. A failed look is not cached, so the next energy run can try again. Bruce's hourly solar desk speaks the last stored sentence, names its age when it is from an earlier hour, and attaches the still. It does not start a second look.

The model names the weather (rain, fog, overcast, clear, dark) and the tilt. Left side up is the morning position. Flat is the day position. Right side up is the evening position. Left and right are as channel 1 sees the array.

An infrared still is grayscale. The color span of that frame sits near 2, and a color frame sits above 11. A span under 6 is night, so weather is dark. The gray look is the infrared illuminator. It is not overcast. The tilt reading stays with the model. A color look from earlier in the same hour is replaced once the newest still is infrared.

| Part of the day | From the sun file | What is correct |
| --- | --- | --- |
| Morning | Two hours before sunrise through one hour after | Left side up, or flat. Right side up asks for a person. |
| Day | After that, until one hour before sunset | Flat. Any tilt asks for a person. In the later half of that window, left side up is fine when combined solar input is 20 W or less on a reading newer than 30 minutes. That line is "Solar staged for sunrise." |
| Evening | One hour before sunset through 45 minutes after | Right side up. Anything else asks for a person. Left side up with that same low solar input reads "Solar staged for sunrise." |
| Overnight | The rest of the night | Left side up, or flat. Right side up asks for a person. |

Morning tilt helps early capture and is not required. Overnight left tilt is the correct prep. The warning says a person is needed. Nothing moves the panels. Four corner actuators for this tilt are a desired upgrade, not a build: [four corner actuators](../09-Desired-Upgrades/2026-09-30-four-corner-sun-tilt-actuators.md).

## Spoken clock and change lines

Spoken time and report headings use the Hawaii clock when the text is built, not a snapped :00 or :30 slot. Daypart roll-ups still run at 09:02, 12:02, and 21:02, and they say that clock.

After a measured number, desks may add a short percent-change line against yesterday, last week, and last month when an earlier reading exists. A missing period, or a zero baseline, is omitted. Example shape: `CPU up 50 percent from yesterday, down 25 percent from last week.` The helper is `Media/Voice/scripts/compare_span.py` (ledger `Database/Reports/Comparisons/metrics.jsonl`; energy keys can also read `Energy/samples`). `voice_reports.py` calls it through `say_change`; `system_perf.py` calls it directly. Unit checks: `test_compare_span.py`.

## Status clips

Sixty lines, one clip at a time, for the ten desks that render (six phases each). The Pacific hourly chime job stays a file replay and does not get these lines. News, the hurricane desk, and the daypart roll-ups are not in this set.

Bruce speaks system, solar, and remaining tasks. Ava speaks NWS and the current report. Carly speaks energy, earthquakes, Kīlauea, security, and bandwidth. The type word in the clip is System, NWS, Energy, Remaining tasks, Earthquake, Kilauea, Solar, Security, Bandwidth, or Current.

| Moment | Line | When it plays |
| --- | --- | --- |
| Starting | "<Type> report is about to generate." | Before the voice render |
| Transit | "<Type> report has been generated and is in transit." | As the send to Mainland One starts |
| Failed | "<Type> report was generated but failed to send." | If that send does not land |
| Sent | "<Type> report was sent successfully." | After Mainland One has the file |
| Staged hour | "<Type> report has been staged for the hour." | On-air cue for the next :00 slot |
| Staged half | "<Type> report has been staged for the half hour." | On-air cue for the next :30 slot |

The sent line is the receipt. It plays only after the remote file checks out and is moved into place. A skipped send does not play the failure line.

`radio_push.stage_on_air` uploads the staged cue for the next Hawaii :00 or :30. On the station, the short notification sound plays first; the full spoken clock chime does not. Local desk playback of starting/transit/failed/sent still uses `aplay`.

The clips are Database `Media/Audio/Voice/Clips/<Persona>/<report>_<phase>.wav`. `RR_VOICE_STATUS` defaults on. Set `RR_VOICE_STATUS=0` before the poller starts to keep them quiet. The code is `Media/Voice/scripts/status_cue.py` and `radio_push.py`.

## Hourly chimes

Forty-eight files, `Database/Media/Audio/Voice/Chimes/hour-00-00.wav` through `hour-23-30.wav`, one for every hour and half hour. Each one starts with `Media/Voice/assets/deep-ui-chime.mp3`, then the voice. Midnight and 12:30 a.m. are Ava, 1:00 and 1:30 a.m. are Bruce, 2:00 and 2:30 a.m. are Carly, then it repeats. Playback copies the file. It does not call Kokoro.

Those desk files are WAV. The Mainland station library is Opus, and that bed is playing. A chime on the station is `hour-HH-MM.opus` at 48 kbps. A report there is `<report>_current.opus` at 24 kbps mono. Music there is `.opus` at 96 kbps and arrives with the git pull. Hawaii still renders a WAV, then `Media/Voice/scripts/radio_push.py` encodes that one report to Opus and replaces it on `/home/ubuntu/rootrecord-radio` over `ssh ml1`. Only the current daypart rollup is kept: morning 09:00–12:00, midday 12:00–21:00, late 21:00–09:00. The station deletes the other two daypart files when the current one arrives. The public mix stays `https://radio.rootrecord.cloud/radio/live.mp3`. Earthquake and hurricane reports stay Pacific poller jobs. The Pacific chime job below is separate from the station chime.

The sentence is the Hawaii time, then Mountain Daylight Time (four hours ahead), Eastern time (six hours ahead), and UTC (ten hours ahead). The minute is the same in each zone. Those offsets match daylight time. They are wrong after US standard time begins in November, and the files have to be rendered again.

The job is `:00` and `:30`. It stays off until `RR_VOICE_HOURLY_CHIME=1` is in the poller environment at start. Rebuild with:

```bash
PACIFIC="/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server"
"$PACIFIC/System/scripts/plumbing/single-flight.sh" run "voice:chimes:batch" -- \
  nice -n 10 "$PACIFIC/Media/Voice/.venv/bin/python" \
  "$PACIFIC/Media/Voice/scripts/hourly_chimes.py" --render
```
