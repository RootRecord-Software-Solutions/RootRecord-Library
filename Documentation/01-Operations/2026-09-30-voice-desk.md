# Voice desk — current as of 2026-10-01

Finished Hawaii reports go to the Mainland station. The station snapshots the playlist at `HH:29:59` and `HH:59:59`, then chimes on the hour and the half hour. Voice jobs render before that snapshot. The station is on the air at `https://radio.rootrecord.cloud/radio/live.mp3`. The operator page is [2026-10-01 radio station](./2026-10-01-radio-station.md).

This is the living description of the spoken reports. The 2026-09-29 port record is [Voice-Reports-G3](../10-AI-and-Agent-Runtime/Voice-Reports-G3.md). Where that file still says a job is off, has no delivery, or skips a vision line, this file wins.

Sandbox chat is `-1004406495175`. `RR_VOICE_DELIVER=1` and `RR_TELEGRAM_DEST=sandbox` are the defaults in `Automations/scripts/poller/run-poller.sh`. A sandbox post is a voice note, a transcript, and the measured report. A live chat would be voice and report only. The same spoken words are not sent again. Hourly chimes also remember the date and the slot (`HH:MM`), so the same sentence can send on the next day.

Flags are read when the poller starts. A script edit is picked up on the next run of that job. A new `jobs.py` entry is not, until the poller is started again.

Kokoro loads for one report and exits. Ava is `af_heart`, Bruce is `am_echo`, Carly is `af_nova`. All three speeds are 1.0. Output is 24 kHz, 16-bit, mono WAV under Database `Media/Audio/Voice/`.

## What is on

These flags default to 1 in `run-poller.sh`. The schedule is HST.

| Minute | Who | Report | What it says |
| --- | --- | --- | --- |
| :12 and :42 | Bruce | System | CPU, memory, disk, host battery, uptime, integrated graphics, NPU. Host temperature is degrees Celsius. |
| :12 and :42 | Ava | NWS | Hawaii alerts and the forecast period on file. |
| :12 and :42 | — | Energy look | Refreshes the camera look before the solar desk. It does not send a voice note. Bruce speaks that sentence on the solar desk in the same pass. |
| :12 and :42 | Bruce | Remaining tasks | Open report-board slots. |
| :12 and :42 | Carly | Earthquakes | Hawaii first, then global. A stale file is named as stale. |
| :12 and :42 | Carly | Kīlauea | HVO alert and notice. Place names are respelled. She does not read raw JSON, and she does not say Hawaii after every line. |
| :12 and :42 | Bruce | Solar desk | Pack state of charge, solar, AC, USB-C, generator or transfer, sun times, the channel 1 still, and the last stored camera look. |
| :12 and :42 | Carly | Security | Firewall, ssh, listeners, failed sign-ins. No raw JSON. |
| :12 and :42 | Carly | Bandwidth | Byte samples. If there is no sample window yet, the note is not sent. |
| :12 and :42 | Ava | Current | Full current report after the other desks. |
| :36 | rotating | News | Hourly news update, before the :42 stack. |
| 09:02, 12:02, 21:02 | Ava | Daypart roll-up | Morning, midday, and late. Rendered inside the window so the next half-hour snapshot can play it. |
| 05:40, 09:40, 12:40, 16:40, 20:40 | Carly | Hurricane | Before the following hour snapshot. Off unless `RR_VOICE_HURRICANE=1`. |
| :00 and :30 | rotating | Chime | Prebuilt file. The job stays off until `RR_VOICE_HOURLY_CHIME=1`. The station chime is separate and stays on the hour and the half hour. |

The desks share one poller thread and one voice lock, so they run one after another. Energy runs before the solar desk. The current report runs last. `:12` and `:42` start 18 minutes before the station locks the playlist at `:29:59` and `:59:59`. A file that arrives after the snapshot waits for the next cycle. Starting on the hour or the half hour was too late.

News at `:36` and the hurricane desk at `:40` finish before the top-of-hour stack.

Morning, midday, and late roll-ups cannot be written before their window opens, so they stay at 09:02, 12:02, and 21:02. The 09:00 snapshot is taken at 08:59:59, while the late roll-up is still the one on the air, so the new morning file first plays at 09:30. Noon first plays at 12:30. Nine at night first plays at 21:30.

The poller was started again at 23:46 HST on 1 October 2026 and is on this schedule. The next render after that start is 00:12, for the 00:30 announcement.

## How long a desk takes

The current measurement is [voice timing](./voice-timing.md). `voice_timing_report` rewrites that page from the automations log at :05. It follows the Documenter handoff template and does not call a model.

Geology collection (`RR_GEOLOGY`) and network samples (`RR_NET_SAMPLES`) also default to 1, because the quake and bandwidth notes read those files.

## What stays off

Not exported in `run-poller.sh`, so a normal poller start leaves them off:

| Flag | Report |
| --- | --- |
| `RR_VOICE_HOURLY_CHIME` | The :00 and :30 chimes. The 48 files exist. The job does not play them until this flag is 1 at poller start. |
| `RR_VOICE_HURRICANE` | Hurricane desk. |
| `RR_VOICE_ROLLUPS` | Morning 09:02, midday 12:02, late 21:02. |
| `RR_VOICE_LATE_FINAL` | 23:02 second chance for the late roll-up. |
| `RR_VOICE_OFFICIAL` | Official weather. The job is still not in `jobs.py`. |
| `RR_VOICE_BOOT` | Boot brief. The job is still not in `jobs.py`. |
| `RR_PUBLIC_HEALTH` | Origin radio and port 8787 check. Send needs a second flag. |
| `RR_KILAUEA_DRAFT_ANNOUNCE` | Draft count. Send needs a second flag. |
| `RR_NOTE_DRAFT` | A note turned into a work-order draft. It does not build. |
| `RR_SUN_TIMES` | The sunrise job. The tilt check uses the sun file already on disk. |

Speakers stay off. `Media/Playback` is dry-run unless `RR_PLAYBACK=1` and `--play`.

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
