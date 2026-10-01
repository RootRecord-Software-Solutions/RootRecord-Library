# Voice desk — current as of 2026-09-30 17:20 HST

This is the living description of the spoken reports. The 2026-09-29 port record is [Voice-Reports-G3](../01-AI-and-Agent-Runtime/Voice-Reports-G3.md). Where that file still says a job is off, has no delivery, or skips a vision line, this file wins.

Sandbox chat is `-1004406495175`. `RR_VOICE_DELIVER=1` and `RR_TELEGRAM_DEST=sandbox` are the defaults in `Automations/scripts/poller/run-poller.sh`. A sandbox post is a voice note, a transcript, and the measured report. A live chat would be voice and report only. The same spoken words are not sent again. Hourly chimes also remember the date and the slot (`HH:MM`), so the same sentence can send on the next day.

Flags are read when the poller starts. A script edit is picked up on the next run of that job. A new `jobs.py` entry is not, until the poller is started again.

Kokoro loads for one report and exits. Ava is `af_heart`, Bruce is `am_echo`, Carly is `af_nova`. All three speeds are 1.0. Output is 24 kHz, 16-bit, mono WAV under Database `Media/Audio/Voice/`.

## What is on

These flags default to 1 in `run-poller.sh`. The schedule is HST.

| Minute | Who | Report | What it says |
| --- | --- | --- | --- |
| :03 | Carly | Kīlauea | HVO alert and notice. Place names are respelled. She does not read raw JSON, and she does not say Hawaii after every line. |
| :04 | Bruce | Solar desk | Pack state of charge, solar, AC, generator or transfer. |
| :06 | Bruce | System | CPU, memory, disk, host battery, uptime, integrated graphics, NPU. Host temperature is degrees Celsius. |
| :07 :22 :37 :52 | Ava | NWS | Hawaii alerts and the forecast period on file. |
| :08 | Carly | Earthquakes | Hawaii first, then global. A stale file is named as stale. |
| :11 | Carly | Security | Firewall, ssh, listeners, failed sign-ins. No raw JSON. |
| :12 | Carly | Bandwidth | Byte samples. If there is no sample window yet, the note is not sent. |
| :15 :45 | Carly | Energy | Both packs, the channel 1 still, and the hourly solar look. |
| :32 | Bruce | Remaining tasks | Open report-board slots in the next hour. Morning 09:02, midday 12:02, late 21:02. |

Geology collection (`RR_GEOLOGY`) and network samples (`RR_NET_SAMPLES`) also default to 1, because the quake and bandwidth notes read those files.

## What stays off

Not exported in `run-poller.sh`, so a normal poller start leaves them off:

| Flag | Report |
| --- | --- |
| `RR_VOICE_HOURLY_CHIME` | The :00 and :30 chimes. The 48 files exist. The job does not play them until this flag is 1 at poller start. |
| `RR_VOICE_HURRICANE` | Hurricane desk. |
| `RR_VOICE_ROLLUPS` | Morning 09:02, midday 12:02, late 21:02. |
| `RR_VOICE_LATE_FINAL` | 23:30 second chance for the late roll-up. |
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

Readings older than 30 minutes are "out of range." A current channel 1 still is not given an age. An older still is "N minutes old."

Generator and transfer use watts, and the same rules are in the voice, the BLE charge source, and the load categories:

| Reading | Meaning |
| --- | --- |
| Delta 2 AC in greater than 550 W | Generator. 550 itself is not. |
| River 2 Pro AC in greater than 300 W | Generator, unless the next row matches. 300 itself is not. |
| Delta AC out matches River AC in | Transfer from the Delta to the River, not a generator on the River. Both watts at least 20, and the gap no larger than 40 W or 12 percent of the larger number. |
| A stale file that says 0 W | Not a generator. |

## Channel 1 solar look

Once per clock hour, during the energy report, `Security/Cameras/panel_look.py` asks the local vision model `gemma4:e4b` about the newest channel 1 still. The :45 report reuses that hour's sentence. The cache is Database `Energy/vision/ch1-look-last.json`. A failed look is not cached, so the next energy run can try again. The sentence is in the spoken note, the written report, and the photo caption.

The model names the weather (rain, fog, overcast, clear, dark) and the tilt. Left side up is the morning position. Flat is the day position. Right side up is the evening position. Left and right are as channel 1 sees the array.

| Part of the day | From the sun file | What is correct |
| --- | --- | --- |
| Morning | Two hours before sunrise through one hour after | Left side up, or flat. Right side up asks for a person. |
| Day | After that, until one hour before sunset | Flat. Any tilt asks for a person. In the later half of that window, left side up is fine when combined solar input is 20 W or less on a reading newer than 30 minutes. That line is "Solar staged for sunrise." |
| Evening | One hour before sunset through 45 minutes after | Right side up. Anything else asks for a person. Left side up with that same low solar input reads "Solar staged for sunrise." |
| Overnight | The rest of the night | Left side up, or flat. Right side up asks for a person. |

Morning tilt helps early capture and is not required. Overnight left tilt is the correct prep. The warning says a person is needed. Nothing moves the panels. Four corner actuators for this tilt are a desired upgrade, not a build: [four corner actuators](../09-desired-upgrades/2026-09-30-four-corner-sun-tilt-actuators.md).

## Hourly chimes

Forty-eight files, `Database/Media/Audio/Voice/Chimes/hour-00-00.wav` through `hour-23-30.wav`, one for every hour and half hour. Each one starts with `Media/Voice/assets/deep-ui-chime.mp3`, then the voice. Midnight and 12:30 a.m. are Ava, 1:00 and 1:30 a.m. are Bruce, 2:00 and 2:30 a.m. are Carly, then it repeats. Playback copies the file. It does not call Kokoro.

The sentence is the Hawaii time, then Mountain Daylight Time (four hours ahead), Eastern time (six hours ahead), and UTC (ten hours ahead). The minute is the same in each zone. Those offsets match daylight time. They are wrong after US standard time begins in November, and the files have to be rendered again.

The job is `:00` and `:30`. It stays off until `RR_VOICE_HOURLY_CHIME=1` is in the poller environment at start. Rebuild with:

```bash
PACIFIC="/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server"
"$PACIFIC/System/scripts/plumbing/single-flight.sh" run "voice:chimes:batch" -- \
  nice -n 10 "$PACIFIC/Media/Voice/.venv/bin/python" \
  "$PACIFIC/Media/Voice/scripts/hourly_chimes.py" --render
```
