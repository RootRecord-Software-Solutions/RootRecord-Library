# US-Mainland-One

Current as of 2026-10-02 08:40 UTC. This page is the live host. The operator guide is [2026-10-01 radio station](../01-operations/2026-10-01-radio-station.md). The 2026-09-29 import, globe, and fallback notes are historical. They are in [the archive architecture page](../archive/2026-W40/architecture-pre-reorg/US-Mainland-Server.md) and the 2026-09-29 testing records. Do not treat that inventory as this machine.

| Field | Value |
| --- | --- |
| **Role** | Radio only |
| **GitHub** | `RootRecord-Software-Solutions/US-Mainland-One`, `main`, `9b7fccf` |
| **Desk folder** | `1 - Servers/2 - RootRecord-US-Mainland-One` |
| **Host checkout** | `/home/ubuntu/US-Mainland-Server` |
| **Host** | `ip-172-31-10-115`, public `3.140.195.32` |
| **Runtime** | `/home/ubuntu/rootrecord-radio` |
| **Stream** | `https://radio.rootrecord.cloud/radio/live.mp3` (`audio/mpeg`, 128 kbps) |
| **Now playing** | `https://radio.rootrecord.cloud/radio/now.json` |
| **Page** | `https://www.rootrecord.cloud/radio` |
| **SSH** | `ssh ml1` and `ssh rr-aws` use `ml1.rootrecord.cloud`. Direct fallback is `rr-aws-ip` |
| **Tunnel** | Mainland-One `939b16f7-7d13-4776-bd4d-80fe8021fc72`. Routes: `ml1.rootrecord.cloud` SSH, `radio.rootrecord.cloud` to `127.0.0.1:8092` |

## What is in the tree

The desk folder and the host checkout contain only:

- `mirror/`
- `rootrecord-radio/`
- `station.sh`
- `status-api/`
- `.gitignore`

The globe, automations, communications, fallback, rebroadcast, scripts, system monitor, and `references/` are not in this tree. Do not copy a station on top of those directories.

## What is playing

The library is Opus. Music is 75 tracks at 96 kbps. Reports are 24 kbps mono. Chimes are 48 kbps. The public mix is the 128 kbps MP3. Music is in git and lands with `/home/ubuntu/aws-git-pull.sh`. Reports stay off git and arrive over `ssh ml1` into `/home/ubuntu/rootrecord-radio/audio/reports`.

The mixer is `rr-radio-station.service`. The watchdog is `rr-radio-watchdog.timer`. Leave `rr-radio-stream.service` and `rr-radio-watch.timer` masked.

At Hawaii `HH:59:59` and `HH:29:59` the bed ducks to 25 percent, the chime plays, then every current report plays longest first, then the bed returns to full. Only the Hawaii daypart that contains now is kept: morning 09:00–12:00, midday 12:00–21:00, late 21:00–09:00. The other two daypart files are deleted when the current one is present.

## What stays elsewhere

`www.rootrecord.cloud` stays on Vercel. `ssh.rootrecord.cloud` is retired. `api.rootrecord.cloud` is aimed at Mainland Two and the API process is not there. `rootserver.rootrecord.cloud` stays the Pacific poller. Earthquake and hurricane voice reports stay Pacific poller jobs.

Do not restart cloudflared over `ssh ml1`. Use `rr-aws-ip` for a change that restarts the tunnel.
