# 2026-10-01 — Radio station

| Field | Value |
| --- | --- |
| **When** | 2026-10-01 evening HST |
| **Operator** | Alexander |
| **State** | One station process is up on Mainland One. The public host is not yet playing the Opus music bed |
| **Secrets** | None in this file. No tunnel credential JSON, API tokens, or private keys |

This is how the station works. Listeners join one live mix. They do not pick tracks.

## What listeners hit

There is one station, one mix, and one encoder. The public page is `https://www.rootrecord.cloud/radio`. That page plays `https://radio.rootrecord.cloud/radio/live.mp3` and reads `https://radio.rootrecord.cloud/radio/now.json`.

The listener stream is always `audio/mpeg`, 128 kbps, 44.1 kHz, stereo PCM encoded by ffmpeg `libmp3lame`. Library files are not what the browser plays. The engine decodes each library file to raw samples, mixes them, and encodes one continuous MP3. A new listener receives the bytes the encoder is producing now, plus a short preroll of recent MP3 frames, and stays on that socket. The page does not start a track from the beginning, and it does not offer a skip.

`now.json` is `Cache-Control: no-store`. The body is:

| Field | Meaning |
| --- | --- |
| `music` | Title of the open music file. Empty when no music file is open |
| `description` | Description from `audio/library.json` for that file, or empty |
| `report` | Spoken title of the report on air. The string `Time` while a chime is playing |
| `chime` | True while a Hawaii chime is the voice |
| `duck` | `0.25` while a report or a chime is the voice. `1` when music is full level |
| `phase` | `NORMAL` or `CHIME` |
| `reportState` | `NONE`, `ACTIVE`, or `HELD` |
| `musicPid` | Process id of the open music decoder. `0` when none is open |
| `listeners` | Open `live.mp3` sockets |

`GET /health` on the same port reports whether the encoder process is still up, plus `phase` and `reportState`. That path is for the host. The public page uses the two URLs above.

The encoder listens on `127.0.0.1:8092`. Cloudflare publishes that port as `radio.rootrecord.cloud`. The browser does not open the AWS address.

## Where the files live

Mainland One is radio only.

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

Mainland Two is a different machine and a different tunnel.

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

The send is `scp` of a temporary Opus file to a hidden partial name, an `ffprobe` check that the remote file has duration, then `mv` into the final name and mode `644`. After that move, the script deletes only that report's old `<report>_current.ogg`. Other reports' `.ogg` files stay until those reports are published as Opus.

Prune then runs on the remote reports directory. It keeps every `*_current.ogg` and every `*_current.opus`, keeps `.gitkeep`, and keeps `*.partial` files younger than 15 minutes. Anything else in that directory is removed.

`RR_RADIO_PUSH=0` turns the send off. The default is on. `RR_RADIO_SSH` defaults to `rr-aws-ip`. `RR_RADIO_REPORTS` overrides the remote reports directory.

Music push is a separate one-way `rsync`. It is `radio_push.py --music`. It is not part of each report. It does not delete remote files and it does not download. The default music source is the desk path in `RR_RADIO_MUSIC`. A report push does not wait for that copy.

The mainland process never fetches the WAV. A new file on disk is enough. The mixer scans the catalog about every 5 seconds. A changed report is queued. The node process stays up.

### Who is eligible

Windows are Pacific/Honolulu. The end of a window is the start of the next one, so 12:00 is midday and 21:00 is late. 09:00 belongs to the morning.

| File id | On air |
| --- | --- |
| `morning_report` | 09:00–12:00 |
| `midday_report` | 12:00–21:00 |
| `late_report` | 21:00–09:00, across midnight |

The file can sit on disk outside its window. The catalog omits it until the window opens, and drops it from the queue when the window closes. Every other `*_current.opus` is eligible whenever it is present. Earthquake and hurricane reports are in that second group. Their jobs keep running on the Pacific desk whether or not the old globe process is up.

## How the mix works

`stream.js` is the mixer. `radio.js` is the catalog: it lists Opus files, applies the Hawaii windows, and reads titles from `audio/library.json`. A missing library entry uses the file name with `.opus` removed.

Music stays open under reports and chimes. The music decoder reads the next file in a shuffled order and opens the following file when that one ends. The same track is not placed first again when the library has more than one file. If the music directory is empty, `music` in `now.json` stays empty and the encoder continues with silence under the voice.

A report ducks music to `0.25`. Samples are summed and clipped to 16-bit. The report decoder is a second ffmpeg reading that Opus file to 44.1 kHz stereo PCM. When the report ends, music returns to full level.

A Hawaii `:00` or `:30` chime holds the report decoder and then resumes the same samples. `reportState` goes from `ACTIVE` to `HELD` for the length of the chime, then back to `ACTIVE`. The chime slot key is the Hawaii date plus `HH:MM`, so the same half-hour plays once that day and can play again the next day. A missing chime file is logged once for that slot and the report is left running.

A new report file does not restart the process. The file identity is device, inode, size, and modification time. A new identity for a report that is already on air is stored as pending. The current decode finishes, then the new file starts. A new identity for a report that is waiting replaces that queue entry. The first quiet moment after the process opens waits about 12 seconds, then plays the next eligible report. After that, reports already on disk rotate about every 10 minutes. A newly written or replaced file skips that wait.

Code activation waits for a quiet boundary: no report in progress and no chime in progress. `HELD` still counts as in progress, because the same report samples have to resume. At that boundary, if `deploy-pending` names a different release, the process exits 75.

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

`aws-git-pull.timer` fast-forwards the checkout at `/home/ubuntu/US-Mainland-Server`. A dirty tracked checkout makes the pull skip. Untracked files do not. The script stages a radio release into `/home/ubuntu/rootrecord-radio/releases/<git-sha>/` when `stream.js` or `radio.js` differs from the staged release, writes that sha to `releases/staged` and to `deploy-pending`, and checks both files with `node --check` before it publishes the sha. It does not start the station and it does not restart the player.

The running engine switches on exit 75 when `deploy-pending` names a release that exists and contains both `stream.js` and `radio.js`. `radio-run.sh` points `active` at `releases/<sha>`, deletes `deploy-pending`, and continues the loop. The listener port comes back inside that same script. Exit 75 with no such release is a failure (`deploy_missing`) and the script stops. Any other exit is a failure. systemd restarts the unit on failure. A clean quiet-boundary switch never leaves the `while` loop, so it is not a restart of the unit.

While a report or a chime is in progress, the engine logs `deploy_deferred` and keeps the current release. The pending file stays on disk until the boundary.

## How to test on the desk

The local player is `station.sh` in `1 - Servers/ML1 REBUILD/2 - RootRecord-US-Mainland-One <<< NEW/`. It is the desk player, not the public host.

That script uses the folder's own `rootrecord-radio` as the runtime. It links `status-api/stream.js` and `status-api/radio.js` into `releases/local`, points `active` at that release, and links `radio-run.sh` into the runtime. It binds `127.0.0.1:8092` unless `HOST` or `PORT` is set. Audio, the engine, and the logs stay in that folder.

Start it from that folder:

```text
./station.sh
```

Then open the local URLs at the end of this note. A desk process on port 8092 is not the Mainland One process. Do not treat a local `now.json` as the public station.

## The current gap

There is no music on the live Mainland host. The new build folder, `1 - Servers/ML1 REBUILD/2 - RootRecord-US-Mainland-One <<< NEW`, is the local copy being converted to Opus. The public station is not playing a music bed. A report's old `*_current.ogg` stays until that report is replaced. The replace then deletes only that report's old ogg.

The watchdog on that host has one station process up. `now.json` can show an empty music title until the library arrives. Reports already published as `*_current.opus` can still be eligible. `*_current.ogg` files are kept by prune and are not what the current catalog selects.

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
