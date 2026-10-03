# 2026-10-01 — Radio station

2026-10-02 ~14:12 HST: locals are minute [45] in `jobs.py`, news is [8] and pushes only part 1 and part 2, and the current report is off. The poller is still frozen, so this does not run until a clean start.

2026-10-02 ~14:09 HST hold: Alexander stopped rootserver ops. The poller is frozen and the current report render is dropped. The hour cycle is still in `jobs.py`, and it does not run until he says ops are back on.

Mainland ~13:58 HST: 2:00 and 2:30 chimes are on the station, and the solar file landed as one battery at 40 percent across two live packs. That figure is Mainland’s read.

2026-10-02 ~13:44 HST: the hour cycle is the order. Desk `jobs.py` local voice jobs are minute [50], chimes [0, 30], news still one job at :36. Daypart `enabled` lines are broken (`False, "0") == "1"` at `voice_morning_report` and the same shape on midday, late, and late-final), That break was closed ~13:57 HST. The file parses, and those four jobs are `enabled` False. Merged battery is ordered and not the spoken script yet. Mainland’s mixer report and the viewer count of 1 are Mainland’s, not a desk measurement.

| Field | Value |
| --- | --- |
| **When** | 2026-10-01 evening HST, brought current 2026-10-02 ~02:18 HST |
| **Operator** | Alexander |
| **State** | Mainland One is the clean radio tree at `9b7fccf`. One station is on the air and playing the Opus music bed. Read-only check ~01:56–01:58 HST: `rr-radio-station` up since 01:39 HST (one clean restart); `live.mp3` 200; air healthy; encoding + watchdog `watch_ok`; public stream OK; light `ffmpeg` + `stream.js` |
| **Secrets** | None in this file. No tunnel credential JSON, API tokens, or private keys |

This is how the station works. Listeners join one live mix. They do not pick tracks.

2026-10-02 ~12:54 HST: Alexander said this mix is causing trouble for other users, so listeners move to YouTube, and video is not allowed. Mainland is not touching this station. The YouTube path is stills only and is not built. The wiped ML2 video stack stays wiped. `rr-radio-station` and `live.mp3` stay as they are until that path exists. Superseded ~13:27 HST: Alexander reopened YouTube on ML1. Picture is `1 - Servers/ML1 REBUILD/youtube-thumb.png`, not the live website. Radio page is to embed the active livestream at https://www.youtube.com/@rootmcnews. ML1 renders the local mix and YouTube in parallel. Mainland is wiring it. Not live yet. The wiped ML2 tree stays wiped. ~12:56 HST: Report Instructor keeps reports as audio and will not make a video version or touch the station. Cove’s ~12:56 hold (keep the Radio page on the live mp3 and do not embed) is superseded by this ~13:27 order. Cove landed the embed ~13:31 HST in `Website/Home/radio/index.html` (channel UC6M7U4fXAWuVYhgm_veKecA, `https://www.youtube.com/embed/live_stream?channel=UC6M7U4fXAWuVYhgm_veKecA`). The page no longer plays `live.mp3` or loads `radio.js`. `Website/Home/assets/site.css` styles `.radio-frame`. The ML1 broadcast itself is not verified on the air. Superseded ~14:30 HST: the iframe is `https://www.youtube.com/embed/2STpx2YzOQA`. The channel-wide live_stream URL showed unavailable. This id does not follow the next broadcast. The sentence above the frame is: This page plays the Root Record livestream that is on now, from the Root Record channel. The meta description is: The Root Record livestream that is on now. No commit. Reports stay audio.

## What listeners hit

There is one station, one mix, and one encoder. The public page is `https://www.rootrecord.cloud/radio` (and `/live` audio via `live-radio.js`). That page plays `https://radio.rootrecord.cloud/radio/live.mp3` and reads `https://radio.rootrecord.cloud/radio/now.json`. Browsers often block autoplay. The Listen button is only for the first unlock; after that the client auto-resumes and cache-bust reconnects on pause, stall, waiting, ended, error, offline→online, and visibility, so a stream drop does not put TAP LISTEN back on screen. The stream itself is already audible at the mp3 URL. A 15-minute public limit and `/pro/radio` membership wall are future only — not implemented. ML1 mixer untouched. Website worktree local commit `cdd9f0c` (`Github-worktrees/website/`, not pushed by Mainland); Library note commit `fc06d15`. Earlier Listen-button commit was `36ab4a0`. Pacific `Website/Home/assets/radio.js` may lag the website worktree until desk sync; Vercel may lag GitHub.

The listener stream is always `audio/mpeg`, 128 kbps, 44.1 kHz, stereo PCM encoded by ffmpeg `libmp3lame`. Library files are not what the browser plays. The engine decodes each library file to raw samples, mixes them, and encodes one continuous MP3. A new listener receives the bytes the encoder is producing now, plus a short preroll of recent MP3 frames, and stays on that socket. The page does not start a track from the beginning, and it does not offer a skip.

`now.json` is `Cache-Control: no-store`. The body is:

| Field | Meaning |
| --- | --- |
| `music` | Title of the open music file. Empty when no music file is open |
| `description` | Description from `audio/library.json` for that file, or empty |
| `report` | Spoken title of the report on air. The string `Time` while a chime is playing |
| `chime` | True while a Hawaii chime is the voice |
| `duck` | `0.1` from the second before a chime through the last report in that cycle. `1` when the cycle is idle |
| `phase` | `NORMAL`, `DUCK`, `CHIME`, or `REPORTS` |
| `reportState` | `NONE` or `ACTIVE` |
| `musicPid` | Process id of the open music decoder. `0` when none is open |
| `listeners` | Open `live.mp3` sockets |

`GET /health` on the same port reports whether the encoder process is still up, plus `phase` and `reportState`. That path is for the host. The public page uses the two URLs above.

The encoder listens on `127.0.0.1:8092`. Cloudflare publishes that port as `radio.rootrecord.cloud`. The browser does not open the AWS address.

## Where the files live

Mainland One is the radio tree. As of ~13:27 HST it is also the ordered YouTube broadcaster (public page embed landed ~13:31 HST; the broadcast is not verified on the air).

| What | Value |
| --- | --- |
| Direct SSH address | `3.140.195.32` (`rr-aws-ip`) |
| Host | `ip-172-31-10-115` |
| Checkout | `/home/ubuntu/US-Mainland-Server` |
| Runtime | `/home/ubuntu/rootrecord-radio` |
| Listener bind | `127.0.0.1:8092` |
| Tunnel | Mainland-One, id `939b16f7-7d13-4776-bd4d-80fe8021fc72` |

The connector ignores a local config file. The dashboard ingress wins. The live routes on that tunnel are:

| Hostname | Service |
| --- | --- |
| `ml1.rootrecord.cloud` | `ssh://localhost:22` |
| `radio.rootrecord.cloud` | `http://127.0.0.1:8092` |

`ssh.rootrecord.cloud` is retired. `www.rootrecord.cloud` stays on Vercel. Leave `www` off this tunnel.

Mainland Two is a different machine and a different tunnel. It is **not** the radio station. The video experiment stays wiped ([US-Mainland-Two](../15-Domains-and-External-Systems/US-Mainland-Two.md)). The ~12:54 stills-only path is superseded by the ~13:27 ML1 order. This station was not stopped. Live role: Cloudflare tunnel + github-ops pull scaffolding only. Polling later, not live.

| What | Value |
| --- | --- |
| Direct SSH address | `3.149.238.83` (`ml2-ip`) |
| Tunnel id | `bd8e68a4-8a97-4b20-afd9-b058473a0a22` |
| SSH name | `ml2.rootrecord.cloud` |
| API name on that tunnel | `api.rootrecord.cloud` → `http://127.0.0.1:8091` |

The API process is not running on Mainland Two. That hostname is a route only. It is not a live API.

The Pacific desk stays on rootserver. Earthquake speech is the job `voice_earthquake_report`. Hurricane speech is the job `voice_hurricane_desk`. Those are Pacific poller jobs. They are not the Mainland globe. Stopping the old globe on the mainland does not stop them.

Desk SSH, from `~/.ssh/config`:

| Alias | Hostname | Use |
| --- | --- | --- |
| `ml1` | `ml1.rootrecord.cloud` | `cloudflared access ssh` |
| `rr-aws` | `ml1.rootrecord.cloud` | same tunnel as `ml1` |
| `rr-aws-ip` | `3.140.195.32` | direct SSH, port 22 |
| `ml2` | `ml2.rootrecord.cloud` | `cloudflared access ssh` |
| `ml2-ip` | `3.149.238.83` | direct SSH, port 22 |

Use `rr-aws-ip` when a change would restart `cloudflared`. Restarting the tunnel drops an `ml1` session. The same rule applies to `ml2`: use `ml2-ip` if the change would restart the Mainland Two connector.

### Runtime layout

Paths come from the runtime directory that contains `audio/`. `RADIO_ROOT` overrides that. The engine does not need `/home/ubuntu` hardcoded when the script lives in the runtime. The systemd unit on the host does use that prefix: `WorkingDirectory=/home/ubuntu/rootrecord-radio` and `ExecStart=/home/ubuntu/rootrecord-radio/radio-run.sh`, with `HOST=127.0.0.1` and `PORT=8092`.

| Path under the runtime | Role |
| --- | --- |
| `active` | Symlink to the release that is on the air |
| `releases/<id>/` | One copy of `stream.js` and `radio.js` |
| `releases/staged` | Id of the release most recently staged |
| `deploy-pending` | Id the running engine should switch to at a quiet boundary |
| `radio-run.sh` | Process that starts `active/stream.js` and applies exit 75 |
| `audio/music/` | Music bed |
| `audio/reports/` | Spoken reports |
| `audio/chimes/` | Hawaii half-hour chimes |
| `audio/library.json` | Optional titles and descriptions for music files |
| `state/heartbeat` | Written about once a second by the mixer |
| `plays.log` | Play lines. Emptied every hour. No archive |
| `state/station.log` | Used when the watchdog starts the mixer without systemd |

The active release is `rootrecord-radio/active`, and that directory contains `stream.js` and `radio.js`.

### Library format

One library type: Opus (`.opus`).

| Kind | Path | Encode |
| --- | --- | --- |
| Reports | `audio/reports/<report>_current.opus` | 24 kbps mono, `libopus`, application `voip` |
| Chimes | `audio/chimes/hour-HH-MM.opus` | 48 kbps. Hawaii `:00` and `:30` only |
| Music | `audio/music/<track>.opus` | 96 kbps |

Chime names match `hour-` plus a 24-hour clock and either `00` or `30`, for example `hour-09-00.opus` and `hour-21-30.opus`. A chime is about 11 seconds. Music names are a single file name ending in `.opus`. Report names are lowercase words separated by underscores, ending in `_current.opus`.

The mixer only schedules `*_current.opus`. An `.ogg` file sitting beside it is not a track.

## How a report gets on the air

Hawaii writes a WAV under the voice database, `2 - RootRecord-Database/Media/Audio/Voice/<report>_current.wav`. The script is `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Media/Voice/scripts/radio_push.py`. It encodes that one report to Opus on the desk and replaces one file over SSH on the runtime reports directory, `/home/ubuntu/rootrecord-radio/audio/reports/<report>_current.opus`. It does not download.

`news_update` is built on Pacific `Media/RadioRss` (`news-hour` → replace `news_update_current.wav` → push). As of 2026-10-02 ~04:30 HST a local sample was **~22.7 spoken minutes** within the twenty-to-twenty-five-minute target (`target_words: 3600` in `config/policy.yaml`), with Ava/Bruce/Carly balanced via `balance_personas`. Mix: markets, defence, SpaceX, Hawaii, chips/big tech, world, mainland weather, centrist politics, science, universities, and also; policy raises defence/politics budgets and feeds add `doj_news`/`defense_gov`. Sports is dropped from every feed before desks; `stories.py` uses word-edge matching for `nfl`/`nba`/`mlb`/`sports` and expanded leagues so conflict, influenza, and sportswear stay. Centrist feeds also drop partisan phrasing. The Mainland mixer does not filter sports or partisanship; ingest already did. Job `radio_news_update` timeout is 2400 seconds; At the Report Instructor's ~11:53 HST read, `RR_RADIO_NEWS=1` and the news job is on. See [voice desk](./2026-09-30-voice-desk.md).

2026-10-02 ~13:01 HST: the date is said once. `news_hour.py` on the Pacific desk opens with the month, day, and year and does not repeat a published-on line for each story. Cluster briefs in `pipeline.py` say Published once, on the opener. The ML2 vendor copy matches. The pacific worktree `news_hour.py` still dates every story. That copy is not what gets spoken. The builder the desk runs says the date once. No new audio was rendered and nothing was put on the air. Alexander’s later hour-long news block is an idea only. This cycle is still 30 minutes.

The send is `scp` of a temporary Opus file to a hidden partial name, an `ffprobe` check that the remote file has duration, then `mv` into the final name and mode `644`. After that move, the script deletes only that report's old `<report>_current.ogg`. Other reports' `.ogg` files stay until those reports are published as Opus.

Prune then runs on the remote reports directory. It keeps every `*_current.ogg` and every `*_current.opus`, keeps `.gitkeep`, and keeps `*.partial` files younger than 15 minutes. Anything else in that directory is removed.

`RR_RADIO_PUSH=0` turns the send off. The default is on. `RR_RADIO_SSH` defaults to `ml1` (`ml1.rootrecord.cloud`), so an IP change does not break the push. `RR_RADIO_REPORTS` stays `/home/ubuntu/rootrecord-radio/audio/reports`. Reports are not in the git checkout. A pull must not restore an older report.

Music is not pushed over SSH. The Opus bed, the chimes, and `library.json` are in the Mainland One repo. The host pull copies them into the runtime. `radio_push.py --music` remains a one-way rsync and is not the path that keeps the bed current.

The mainland process never fetches the WAV. A new file on disk is enough. The mixer scans the catalog about every 5 seconds. A changed report waits for the next half-hour cycle. It does not start when the file arrives. The node process stays up.

### Who is eligible

The scheduled pass plays every non-daypart `*_current.opus`, plus only the current daypart rollup, longest first. An older `*_current.ogg` beside a current Opus file is not played.

Dayparts are Pacific/Honolulu. Only one rollup is current:

| Id | Window |
| --- | --- |
| `morning_report` | 09:00 until 12:00 |
| `midday_report` | 12:00 until 21:00 |
| `late_report` | 21:00 until 09:00 |

At 09:00 the evening file is the previous day. Saving the current rollup removes the other two daypart wav, opus, and ogg files on the desk. `radio_push.py` returns `outside_daypart` and does not upload a rollup outside its window. After a successful upload, and again on the station scan as soon as the current daypart file is present, the runtime deletes the other two daypart `_current.opus` and `_current.ogg` files. Earthquake, weather, and the other desks are not daypart files.

Earthquake and hurricane reports stay in that set. Their jobs keep running on the Pacific desk whether or not the old globe process is up.

## How the mix works

`stream.js` is the mixer. `radio.js` is the catalog: it lists every `*_current.opus` in the reports directory and reads titles from `audio/library.json`. A missing library entry uses the file name with `.opus` removed. A leftover `*_current.ogg` for the same id is not a second copy.

Music stays open under the whole cycle. One encoder, one station process, and the public mix stays `/radio/live.mp3`. The music decoder reads the next file in a shuffled order and opens the following file when that one ends. The same track is not placed first again when the library has more than one file. If the music directory is empty, `music` in `now.json` stays empty and the encoder continues with silence under the voice.

Reports run twice an hour on Pacific/Honolulu. At `HH:59:59` the music bed ducks to `0.1`, one second before the chime, so the drop is already in place. At `HH:00:00` the hour chime plays (`hour-HH-00.opus`, about 11 seconds). Music stays at `0.1` through the chime. Then every current report plays, longest first, at full voice level in the current live mixer. Music stays at `0.1` under the reports and is not ducked again. When the last report ends, music returns to `1`.

Desk auto-sync `e101f21` briefly restored `DUCK = 0.25` because mainland mirror sync had rsynced Servers → worktree. Live mixer and desk were corrected to `0.1` ~01:38 HST (Mainland `1a4c1bb`; `rr-radio-station` restarted). From ~01:45 HST, `id=mainland` desk sync is worktree → Servers only (pacific `40e175e`).

At `HH:29:59` the same cycle starts for the half hour: duck, then `hour-HH-30.opus`, then every current report longest first, then restore. If a cycle is still running, that boundary cuts it. The voice stops, the new chime starts clean, and a second report pass is not stacked on one already playing. The slot key is the Hawaii date plus the chime `HH:MM`, so that half hour plays once and can play again the next day. A missing chime file is logged once for that slot, and the report pass still runs.

Order is duration, longest first. The mixer probes duration with `ffprobe` and keeps that value for the file identity. Until a duration is known, file size is the order. Samples are summed and clipped to 16-bit. The voice decoder is another ffmpeg reading that Opus file to 44.1 kHz stereo PCM.

Alexander's standing rule, recorded 2026-10-02 ~12:03 HST, is that each radio cycle is 30 minutes and all local reports play first, longest first among the locals; `news_update` gets whatever time remains, and a boundary cuts news before an unplayed local report. The live `/home/ubuntu/rootrecord-radio/active/stream.js` has locals first. Mainland reports `rr-radio-station` restarted at 12:02 HST, so this order is on the air as of that restart.

Root Monitor shows that same next cycle without touching the station. As of 2026-10-02 ~12:43 HST the Pacific desk panel has an ML1 playlist page (`Apps/Control-Panel/rr_radio_page.py`, order in `rr_radio_lineup.py`, sidebar id `radio`). It reads `*_current` files on `ml1` over SSH, orders locals longest first then news, prints each file's update time, marks a row cut when the running total would pass 30 minutes, and lists the other dayparts as not this cycle. The station is not restarted and nothing is written. Reopen the monitor to see the page. Desk only; no commit.

At ~12:46 HST Report Instructor read that page and left the station alone. The 12:29 solar file is already in the ML1 list, so the next cycle plays it, and it was not removed. Desk `hurricane_desk_current.wav` (09:42 HST, about 42 seconds) and `news_update_current.wav` (05:49, about 25 minutes) are newer than the queued copies (21:15 and 04:49) and were not pushed. Mainland ~12:48 HST confirmed the mismatch and is not copying the newer desk hurricane and news files onto ML1. The playlist is what the next cycle queues.

A new or replaced report does not start playback and does not restart the process. The file identity is device, inode, size, and modification time. The cycle list is the reports on disk at the boundary. A file that arrives or changes after that waits for the next cycle. A queued file whose identity changed before its turn is skipped.

Pacific renders the recurring desks at `:12` and `:42` so the files are on disk before `:29:59` and `:59:59`. How long that pass takes is on the [voice desk](./2026-09-30-voice-desk.md). A morning file written at 09:02 misses the 08:59:59 snapshot, so it first plays at 09:30. Midday first plays at 12:30. Late first plays at 21:30.

The chime does not pause or resume a report. `reportState` is `NONE` or `ACTIVE`. `phase` is `NORMAL`, `DUCK`, `CHIME`, or `REPORTS`. During a chime, `report` is `Time`.

Code activation waits until the cycle is idle (`phase` `NORMAL`). At that boundary, if `deploy-pending` names a different release, the process exits 75.

If ffmpeg disappears while a file is open, the process exits 127. `radio-run.sh` installs ffmpeg and starts the mix again. If `node` or `ffmpeg` is missing at start, `radio-run.sh` tries `apt-get install` and retries. The station watch script does the same for `python3` before it writes its status file.

## How the process stays up

One watchdog: `/home/ubuntu/radio-watchdog.sh`.

| Unit | Role |
| --- | --- |
| `rr-radio-watchdog.timer` | Every minute (`OnUnitActiveSec=60`, 30 seconds after boot) |
| `rr-radio-watchdog.service` | Oneshot. Runs the watchdog script |
| `rr-radio-station.service` | The mixer. `Restart=on-failure`, two seconds between starts |

`flock` on `/tmp/rr-radio-watchdog.lock` keeps a single watchdog run. A second copy exits immediately.

When `active` is missing, the watchdog reads `releases/staged` and, if that release contains `stream.js` and `radio.js`, points `active` at it and removes `deploy-pending`. It starts `rr-radio-station.service` when that unit is down. It restarts the unit only when `state/heartbeat` is older than 30 seconds. A healthy mixer is left alone. A second `radio-run.sh` for this runtime is killed.

`rr-radio-plays-purge.timer` is hourly. `radio-plays-purge.sh` truncates `plays.log` and deletes rotated names (`plays.log.*`, `plays.log-*`, `plays.log.gz`, `plays.log.old`) in the same directory. It keeps no archive.

A play, in the library handler, is a GET that starts at byte 0 and sends more than 1024 bytes. The line is UTC time, kind (`music`, `reports`, or `chimes`), file name, and byte count, tab-separated, appended to `plays.log` in the runtime. A one- or two-byte range probe is not a play. The public page does not request those library files. Listener count for the live mix is the `listeners` field in `now.json`.

Leave these masked. The old watch also started the status API and Caddy:

- `rr-radio-stream.service`
- `rr-radio-watch.timer`

`radio-watch.sh` in the tree is that older path. It is not the watchdog that should be enabled.

## How a code update lands

`aws-git-pull.timer` runs `/home/ubuntu/aws-git-pull.sh`. That script is on the host, outside the checkout, because the clean tree no longer has `references/aws-git-pull.sh`. It fast-forwards `/home/ubuntu/US-Mainland-Server`, copies the music bed and `library.json` with `status-api/install-music.sh`, copies the chimes, and copies `radio-run.sh` and `runtime-path.sh` into the runtime. If `stream.js` or `radio.js` changed, it copies them into `releases/local` and restarts `rr-radio-station.service`. A dirty tracked checkout makes the pull skip. Untracked files do not.

The running engine switches on exit 75 when `deploy-pending` names a release that exists and contains both `stream.js` and `radio.js`. `radio-run.sh` points `active` at `releases/<sha>`, deletes `deploy-pending`, and continues the loop. The listener port comes back inside that same script. Exit 75 with no such release is a failure (`deploy_missing`) and the script stops. Any other exit is a failure. systemd restarts the unit on failure. A clean quiet-boundary switch never leaves the `while` loop, so it is not a restart of the unit.

While a cycle is in progress (the pre-chime duck, a chime, or a report), the engine logs `deploy_deferred` and keeps the current release. The pending file stays on disk until the cycle is idle.

## How to test on the desk

The desk player was stopped. `station.sh` in the rebuild folder can start a local mix on `127.0.0.1:8092`. That is not the public host. Leave it stopped unless a desk test is the point.

That script uses the folder's own `rootrecord-radio` as the runtime. It links `status-api/stream.js` and `status-api/radio.js` into `releases/local`, points `active` at that release, and links `radio-run.sh` into the runtime. It binds `127.0.0.1:8092` unless `HOST` or `PORT` is set. Audio, the engine, and the logs stay in that folder.

Start it from that folder:

```text
./station.sh
```

Then open the local URLs at the end of this note. A desk process on port 8092 is not the Mainland One process. Do not treat a local `now.json` as the public station.

## What is on the host

Checked 2026-10-02 ~01:56–01:58 HST (Alexander read-only). Host `ip-172-31-10-115`. Uptime ~6h 33m; load 0.00/0.07/0.09; mem 555Mi/1.9Gi (~28%), no swap; disk `/` 67% (2.3G free). `rr-radio-station` up since 01:39 HST after one clean restart; `live.mp3` 200; air healthy; encoding + watchdog `watch_ok`; public stream OK. Checkout and GitHub `RootRecord-Software-Solutions/US-Mainland-One` were last noted at `9b7fccf`; host `aws-git-pull` is aborting on dirty `status-api/stream.js` (behind origin by 6), so the live mixer is not being replaced by pulls — left alone. `cloudflared` active with ~38 EOF/cancel from listener churn. Failed units also include `aws-readme-status`.

The desk folder `1 - Servers/2 - RootRecord-US-Mainland-One` and the host checkout contain only `mirror/`, `rootrecord-radio/`, `station.sh`, `status-api/`, and `.gitignore`. The globe, automations, communications, fallback, rebroadcast, scripts, system monitor, and `references/` are gone. Do not copy a new station on top of those old directories. They are not part of this tree.

The runtime has the 75-track Opus bed. `rr-radio-station.service` is the mixer. `https://radio.rootrecord.cloud/radio/now.json` returns a music title. `https://radio.rootrecord.cloud/radio/live.mp3` is `audio/mpeg` at 128 kbps. The music files were encoded from the old MP3 bed into 96 kbps Opus, and the mix encodes them again, so the bed is not a first-generation master.

The rebuild folder `1 - Servers/ML1 REBUILD/2 - RootRecord-US-Mainland-One <<< NEW` is the working copy that was moved into the live folder. It is not a second production checkout.

## What not to do

Leave `rr-radio-stream.service` and `rr-radio-watch.timer` masked. Enabling `radio-watch.sh` starts `rr-status-api` and Caddy again.

Keep Mainland Two routes off the Mainland-One tunnel. `api.rootrecord.cloud` belongs on tunnel `bd8e68a4-8a97-4b20-afd9-b058473a0a22`. `ml1.rootrecord.cloud` and `radio.rootrecord.cloud` belong on tunnel `939b16f7-7d13-4776-bd4d-80fe8021fc72`.

Leave `www.rootrecord.cloud` on Vercel.

Use `rr-aws-ip` before any change that restarts `cloudflared` on Mainland One. An `ml1` or `rr-aws` session dies with the tunnel.

## URLs

Public page: `https://www.rootrecord.cloud/radio`

Public stream: `https://radio.rootrecord.cloud/radio/live.mp3`

Public now-playing: `https://radio.rootrecord.cloud/radio/now.json`

Desk test stream: `http://127.0.0.1:8092/radio/live.mp3`

Desk test now-playing: `http://127.0.0.1:8092/radio/now.json`
