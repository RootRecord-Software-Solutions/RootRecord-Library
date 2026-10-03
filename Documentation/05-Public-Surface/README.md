# 05 — Public surface

The public page is [Website/Home](../../../1%20-%20Servers/1%20-%20RootRecord-Pacific-Solar-Server/Website/Home/README.md) in the Pacific tree, published to [RootRecord-Website](https://github.com/RootRecord-Software-Solutions/RootRecord-Website). Production is `https://www.rootrecord.cloud/` on Vercel. `www` stays there. `ssh.rootrecord.cloud` is retired. Mainland One is the radio tree at `9b7fccf` and the Opus bed is on the air. The mix still playing is `https://radio.rootrecord.cloud/radio/live.mp3`. 2026-10-02 ~12:54 HST Alexander ordered listeners onto YouTube with no video (stills only, not built). This page was not changed. Superseded ~13:27 HST: Alexander reopened YouTube on ML1. Picture is `1 - Servers/ML1 REBUILD/youtube-thumb.png`, not the live website. Radio page is to embed the active livestream at https://www.youtube.com/@rootmcnews. ML1 renders the local mix and YouTube in parallel. Mainland is wiring it. Not live yet. The wiped ML2 tree stays wiped. ~12:56 HST: Report Instructor keeps reports as audio and will not make a video version or touch the station. Cove’s ~12:56 hold (keep the Radio page on the live mp3 and do not embed) is superseded by this ~13:27 order. Cove landed the embed ~13:31 HST in `Website/Home/radio/index.html` (channel UC6M7U4fXAWuVYhgm_veKecA, `https://www.youtube.com/embed/live_stream?channel=UC6M7U4fXAWuVYhgm_veKecA`). The page no longer plays `live.mp3` or loads `radio.js`. `Website/Home/assets/site.css` styles `.radio-frame`. The ML1 broadcast itself is not verified on the air. Superseded ~14:30 HST: the iframe is `https://www.youtube.com/embed/2STpx2YzOQA`. The channel-wide live_stream URL showed unavailable. This id does not follow the next broadcast. The sentence above the frame is: This page plays the Root Record livestream that is on now, from the Root Record channel. The meta description is: The Root Record livestream that is on now. No commit. Reports stay audio. After first Listen unlock, `/radio` and `/live` auto-resume (15-min / `/pro/radio` later, not built). The guide is [2026-10-01 radio station](../01-Operations/2026-10-01-radio-station.md). `api.rootrecord.cloud` is aimed at Mainland Two and is not live yet (route only). The ML2 video experiment stays wiped ([US-Mainland-Two](../15-Domains-and-External-Systems/US-Mainland-Two.md)). Do not restore it. The Radio and Live nav items are unchanged. `rootserver.rootrecord.cloud` stays the Pacific poller. Reports live at `https://www.rootrecord.cloud/reports/`. The homepage service banner reads `service-notice.json`. The contract is [HANDOFF-vercel-homepage-2026-09-30.md](../../../1%20-%20Servers/1%20-%20RootRecord-Pacific-Solar-Server/Website/HANDOFF-vercel-homepage-2026-09-30.md) plus [Desk automations and service windows](../11-Runtime-Jobs-and-Control/Desk-Automations-and-Service-Windows.md). The radio plan is [2026-10-01 mainland rename and SSH tunnels](../01-Operations/2026-10-01-mainland-rename-and-ssh-tunnels.md).

Primary nav (2026-10-02): Home, Products, Services, Solutions, About, Security, Status, Reports, Radio, Live; footer sitewide Account, Terms, Privacy, Data deletion; current page is a span not a link; report pages share that nav.

| Field | Value |
| --- | --- |
| **Public wording** | **Ava** writes |
| **Honesty / numbers seal** | **Carly** seals before ship |
| **Implementation** | **Bruce** where automation is required |

---

## Related work

| Doc | Topic |
| --- | --- |
| [WO-WEB-001](../06-Development/Work-Orders/WO-WEB-001-Public-Status-Solar-Board.md) | Public status / solar board |
| [WO-WEB-002](../06-Development/Work-Orders/WO-WEB-002-Public-Site-Foundation.md) | Public site foundation |
| [WO-COM-001](../06-Development/Work-Orders/WO-COM-001-Communications-Surface.md) | Messaging edges (not open bots without approval) |
| Notify policy draft | [Communications-Notify-Policy-Draft](../16-Communications/Communications-Notify-Policy-Draft-2026-09-28.md) |

## Rules

- Numbers are measured or marked Waiting / No data  
- No secrets in public copy  
- Billing language consistent with the wall  
- Do not treat draft notify policy as live until sealed and accepted  

This folder may stay thin until a public ship cycle needs durable copy here.

*README added 2026-09-28 HST — section pointer only.*
