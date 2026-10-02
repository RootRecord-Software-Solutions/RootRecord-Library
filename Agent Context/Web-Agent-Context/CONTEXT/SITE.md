# The public page

Checked against the desk on 2026-10-02. If a file named here has moved, follow the file.

## Where it lives

| Fact | Value |
| --- | --- |
| Desk source | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Website/Home/` |
| Production | `https://www.rootrecord.cloud/` on Vercel, project `rootrecord`, team `rrc-ore` |
| Apex | CNAME to the same Vercel target. It answers 308 to `www` |
| Also | `https://rootrecord.vercel.app/` |
| Publish | `github_sync_all` rows `website` and `website-personal`. `Website/Home/` has no `.git` of its own |
| Shape | Static HTML, CSS, and JS. `Home/vercel.json` sets `framework` to null. This is not a Next app |
| Contract | `Website/HANDOFF-vercel-homepage-2026-09-30.md`. The block marked locked 2026-10-01 is current. The DNS table under "Evening of 2026-09-30" is not |

Do not recreate `3 - RootRecord-Website/`. Do not bind port 3001. Do not start a local Next server.

## Pages

Primary navigation (Alexander 2026-10-02): Home, Products, Services, Solutions, About, Security, Status, Reports, Radio, Live. Current page is a span, not a link (omit the self-link). Footer sitewide: Account, Terms, Privacy, Data deletion. Report pages use the same primary nav. Ecosystem / Systems (`/operations` as nav label) / Intelligence / Knowledge stay off primary nav. The page list is `Website/Home/README.md`.

| Path | What it is |
| --- | --- |
| `/` | Entrance. `assets/home.js` draws the globe from the state feed |
| `/live` | Same globe, with the solar-desk overlay |
| `/radio` | Plays `https://radio.rootrecord.cloud/radio/live.mp3` and reads `now.json`. The page does not mix audio. Listen unlocks once; then auto-resume/reconnect (no TAP LISTEN on stall). 15-min / `/pro/radio` later, not built |
| `/reports` and `/reports/<slug>` | Written by `Website/scripts/publish_report_pages.py` from the measured voice files. Spoken transcripts and persona names stay off the page |
| `/operations` | Public readings. `assets/charts.js` draws charge, solar, and AC when the feed has them |
| `/status` | Public system status |

`assets/shell.js` is the small-screen menu. `assets/site.css` is the skin.

## Pending API

`assets/telemetry.js` sets `API` to `https://api.rootrecord.cloud`.

| Request | Used for | Ready when |
| --- | --- | --- |
| `GET /api/state` | Globe: flows, Hawaii, Mainland, endpoints. Needs `stats` and `ok` not false | The process exists |
| `GET /api/operations` | Power, weather, Kīlauea, moon. Needs `ok: true` | The process exists |
| `GET /service-notice.json` | Homepage banner and the planned-down label. This file ships with the site. It does not use the API host | Now |

The hostname is aimed at Mainland Two, tunnel `bd8e68a4-8a97-4b20-afd9-b058473a0a22`, toward `127.0.0.1:8091`. The API process is not running there. A missing reading stays missing. Do not point the page at port 8787. Do not point it at `www`. Do not treat the old AWS host `18.118.30.226` as the live API. That address was the 2026-09-30 evening record.

`rootserver.rootrecord.cloud` is the Pacific poller on `127.0.0.1:8799`. It is not this API. Pollers have not moved to Mainland Two.

The operations bundle the future API is meant to serve is written on the desk by `Website/scripts/live_data_pages.py` to `2 - RootRecord-Database/Website/operations.json`. The page does not read that file directly.

`Website/Cloudflare-Workers/` is not deployed. Its default origin is still the deleted `root-record-cloud.vercel.app` project. Leave it.

## Power on the page

`assets/live.js` marks a pack **POWERED OFF** when the last state of charge is 5 percent or less and the reading is older than 30 minutes. A quiet pack above 5 percent is **STALE** after 20 minutes, not powered off. Charts skip a powered-off pack. Do not draw its last watts as live.

## Radio on the page

One mix. `https://radio.rootrecord.cloud/radio/live.mp3` is `audio/mpeg` at 128 kbps. Now-playing is `https://radio.rootrecord.cloud/radio/now.json`. The station library is Opus and is not what the browser plays. `www` stays on Vercel. `radio.rootrecord.cloud` is the Mainland One tunnel to `127.0.0.1:8092`. Do not put the radio on the API tunnel, and do not put the API on the radio tunnel.

## Service windows

`Home/service-notice.json` is the public list. An empty `windows` array means there is no window. `assets/service-banner.js` shows a window that is active, or one that starts inside 24 hours. Dismiss is for that browser session only.

## What stays off the public page

A cloud provider name. A finer server location. A private path. A token. Persona names on a report page. The 2026-09-29 Mainland continuity inventory.
