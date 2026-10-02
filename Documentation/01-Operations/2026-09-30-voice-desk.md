# Voice desk — current as of 2026-10-02

Finished Hawaii reports go to the Mainland station. The station snapshots the playlist at `HH:29:59` and `HH:59:59`, then chimes on the hour and the half hour. Voice jobs render before that snapshot. The station is on the air at `https://radio.rootrecord.cloud/radio/live.mp3`. The operator page is [2026-10-01 radio station](./2026-10-01-radio-station.md).

This is the living description of the spoken reports. The 2026-09-29 port record is [Voice-Reports-G3](../10-AI-and-Agent-Runtime/Voice-Reports-G3.md). Where that file still says a job is off, has no delivery, or uses an old minute, this file wins. Trust `Automations/scripts/poller/run-poller.sh` and `Automations/scripts/jobs.py` over older “what stays off” lists.

## Current as of 2026-10-02 ~00:50 HST

Alexander’s operator copy, checked against live `jobs.py`, `voice-timing.md` (generated 2026-10-02 00:05 HST, 292 finished runs), `radio_push.stage_on_air`, `compare_span.py`, and `status_cue.py`. Nothing in that pass was committed. The poller was restarted earlier for the schedule and local status cues. `radio_push` is imported on each job, so the next successful push stages without another poller restart. The live Mainland mixer is release `stage-notice` (active symlink `/home/ubuntu/rootrecord-radio/releases/stage-notice`). Desk and ML1 REBUILD `status-api/stream.js` match. A quiet switch used `deploy-pending` and exit 75. Do not kill the encoder mid-report.

### Station lock and lead time

The station locks the playlist at `HH:29:59` and `HH:59:59`, then plays the half-hour chime and every current report. A file that arrives after that lock waits for the next cycle. Generation used to start at `:00` and `:30`, which was too late. The ten generating desks share one poller thread and one Kokoro lock, so they run one after another.

From [voice-timing.md](./voice-timing.md) (292 runs): ten-desk sum median **376 s** (6m16s), average **454 s** (7m34s), p90 **891 s** (14m51s). Lead from `:12:00` to the `:29:59` lock is **17 minutes 59 seconds**. `:42` has the same lead before `:59:59`. That p90 fits, with about three minutes spare. `:12` and `:42` stay. News stays at `:36`. Hurricane stays at 05:40, 09:40, 12:40, 16:40, and 20:40. The hourly chime stays at `:00` and `:30` and is a replay of prebuilt files, not a render.

Daypart roll-ups cannot be uploaded before their window opens, or the upload deletes the roll-up that is still on the air. Morning **09:02**, midday **12:02**, late **21:02**, late final **23:02**. Those first air on the following half hour. `voice_timing_report` runs at minute **5**. It is not a model. It rewrites [voice-timing.md](./voice-timing.md) from the automations log and `jobs.py`. The poller imports `jobs.py` once at start, so a schedule change needs a restart of `rr-rootserver-poller.service` as user `rootrecord`.

### Shared pipeline

`jobs.py` → `voice_reports.py` / `system_perf.py` → build MD → `write_md` (+ Archive) → `voice-render.sh` / `voice_generate` mode_stitch (Kokoro, single-flight) → `voice_deliver` (Telegram when `RR_VOICE_DELIVER=1`) → `radio_push` (default on; set `RR_RADIO_PUSH=0` to skip) → Discord `report_relay` every 300 s → `publish_report_pages` → site `/reports/<slug>`.

Personas (Kokoro): Ava `af_heart`, Bruce `am_echo`, Carly `af_nova`. All speeds 1.0. Output is 24 kHz, 16-bit, mono WAV under Database `Media/Audio/Voice/`.

`RR_VOICE_DELIVER=1` and `RR_TELEGRAM_DEST=council` are the defaults in `run-poller.sh`. A council post is a voice note and the measured report. Unchanged spoken text is not sent again. Flags are read when the poller starts. A script edit is picked up on the next run of that job. A new `jobs.py` entry is not, until the poller is started again.

Kokoro is single-flight through `voice-render.sh`. A busy render returns **75**. Render one slug at a time. The spaCy venv needs the symlink `cli/Templates` pointing at `cli/templates` or the import fails. Do not remove that symlink.

### Ten generating desks (:12 / :42)

| Job | Persona | Spoken label |
| --- | --- | --- |
| `system_perf` | Bruce | System |
| `nws_weather` | Ava | NWS |
| `energy_report` | Carly | Energy |
| `remaining_tasks` | Bruce | Remaining tasks |
| `earthquake_report` | Carly | Earthquake |
| `kilauea_report` | Carly | Kilauea |
| `solar_desk` | Bruce | Solar |
| `security_desk` | Carly | Security |
| `bandwidth_desk` | Carly | Bandwidth |
| `current_report` | Ava | Current |

Armed flags (defaults 1 in `run-poller.sh`): `RR_VOICE_SYSTEM_PERF`, `RR_VOICE_NWS`, `RR_VOICE_ENERGY`, `RR_VOICE_REMAINING`, `RR_VOICE_QUAKE` (+ `RR_GEOLOGY`), `RR_VOICE_KILAUEA`, `RR_VOICE_SOLAR`, `RR_VOICE_SECURITY`, `RR_VOICE_BANDWIDTH` (+ `RR_NET_SAMPLES`), `RR_VOICE_CURRENT`. Also armed: news `:36` (`RR_RADIO_NEWS`), roll-ups (`RR_VOICE_ROLLUPS`), late final (`RR_VOICE_LATE_FINAL`), hurricane (`RR_VOICE_HURRICANE`).

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
5. `system_perf.py` docstring still says `only_at_minutes=[6]`; jobs schedule is `[12, 42]`.
6. `ai_processing_report.py` file header says out under Database `Logs/AI/Reports/`; live `OUT_DIR` default is ecosystem `test-reports/AI-Processing/`. `template_fill.py` header and jobs description say Database `Reports/Generated/`; live `OUT_DIR` default is ecosystem `test-reports/Templates/`.
7. Older ops “what stays off” lists that still name roll-ups, late-final, or hurricane as off are history. `run-poller.sh` arms them.

### Local status clips (desk speakers only)

Each of the ten desks has four local status lines, already rendered, played on the desk with `aplay`. `RR_VOICE_STATUS=0` skips them. They are **not** on the radio. Clips live under Database `Media/Audio/Voice/Clips/{Ava,Bruce,Carly}/`.

| Moment | Line | When |
| --- | --- | --- |
| Starting | “<Label> report is about to generate” | before render |
| Transit | “<Label> report has been generated and is in transit” | when the send starts |
| Failed | “<Label> report was generated but failed to send” | if the send fails |
| Sent | “<Label> report was sent successfully” | only after Mainland One has the file (`ffprobe` duration ≥ 0.2 s, then `mv`) |

A skipped send, including a daypart outside its window, is not a failure and does not play the failure line. Code: `Media/Voice/scripts/status_cue.py`.

### Staged on-air cues (radio)

Each of the ten also has two staged lines, already rendered: “<Label> report has been staged for the hour” and “<Label> report has been staged for the half hour.” After a successful radio push, `radio_push.stage_on_air` encodes that wav to opus, copies it to Mainland One at `/home/ubuntu/rootrecord-radio/audio/cues/{report}-hour.opus` or `{report}-half.opus`, and writes a JSON note in `state/stage`. The next slot is this hour’s `:30` when the minute is under 30, otherwise the next hour’s `:00`. The station plays the cue after whatever report is speaking, or immediately if nothing is speaking. Music ducks while it plays.

The time mark on that cue is the **short notification sound only**, `Media/Voice/assets/deep-ui-chime.mp3` (~2 s), uploaded as `audio/cues/notify.opus`. The station plays the ding first, then the spoken staged line. It does **not** play the full spoken clock (“Report generated at…”, Mountain, Eastern, UTC). Those full chimes stay on the half-hour cycle as `hour-HH-MM.opus`.

### Generation clock (not air slot)

Each report says the Hawaii hour and minute when its text is built, not the air slot. “Report generated at twelve fourteen p.m.” means the text started then. Seconds are not spoken. The current report, remaining tasks, and the morning, midday, and late roll-ups used to snap to `:00`, `:30`, or 09:00 / 12:00 / 21:00. They no longer do. A morning report that starts at 09:02 says nine oh two a.m. The written heading uses the same timestamp. The half-hour station chime still announces the air time. The report announces when it was generated.

### Percent change lines

Numbers in the reports get a percent change when an earlier reading exists. Averages and raw counts both use percent. Periods: yesterday (24 h ± 6 h), last week (7 d ± 36 h), last month (30 d ± 3 d). Speech: “CPU up 8 percent from yesterday, down 2 percent from last week.” Flat is “unchanged.” A missing period is omitted. A zero baseline is omitted. If no period can be compared, the report does not mention a change. History appends to Database `Reports/Comparisons/metrics.jsonl`. Battery SoC, solar watts, and output watts can also use `Energy/samples/read-delta2` and `read-river2pro` files (back to 2026-09-29), so a day comparison can appear immediately; week and month stay silent until a reading falls in those windows. CPU, memory, disk, temperature, battery, GPU, NPU, alert counts, forecast highs and lows, earthquake M2.5 counts, security listener and sign-in counts, bandwidth totals, open work orders, next-hour task count, and hurricane distance and wind use the ledger, so those lines appear only after enough history. Ages, uptime, and the clock are not compared. Code: `Media/Voice/scripts/compare_span.py`, via `say_change` in `voice_reports.py` and directly from `system_perf.py`. Tests: `test_compare_span.py`.

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

## Spoken clock, change lines, and cues

See **Generation clock**, **Percent change lines**, **Local status clips**, and **Staged on-air cues** under Current as of 2026-10-02 above. This section is kept so older links land somewhere: generation clock (not air slot); `compare_span.py` percent lines; four desk `aplay` status phases; two staged on-air phases with `notify.opus` first.

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
