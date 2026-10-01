# What's left for Alexander — 2026-09-30

**For:** Alexander (operator)  
**Checked:** 2026-09-30 02:35 HST on `rootrecord-software-solutions`  
**Status:** Draft for you. Agents do not promote, enable, send, spend, or delete from this list.

The 40-agent pass across ecosystem, pacific, database, and library held. The desk came up at 01:09 HST and the Pacific stack started from this Ecosystem tree. This file is the remaining work that still needs you. Historical work orders stay the record of how it got here.

---

## Already running (leave it)

| Surface | State |
| --- | --- |
| Poller | `rr-rootserver-poller.service` active, Pacific `Automations/` |
| Tunnel | `https://rootserver.rootrecord.cloud` HTTP 200. That hostname is the poller on `:8799`, not a website |
| River 2 Pro | BLE live. About 35% SOC at 01:22, discharging, solar 0 W (night) |
| Delta 2 | Dead. It does not transmit. `WAITING` and the 00:53 snapshot at 1% SOC are normal |
| Cameras | ch1–ch4 grabbing. ch4 is a small night frame |
| Weather | Poller recycled 02:24:58 HST so it loads the resource edits. County reports regenerated 02:34. `noaa_homepage` still failed a bot-check at 02:33. Geology stays off |
| Desk window | Root Monitor autostarts at the next login (applied 02:33). The terminal dashboard stays in the menu. Conky is not started |
| Globe, Ollama, GitHub sync | Up. Sync publishes ecosystem, pacific, database, library. `skills` matched |
| Telegram relay | Process up, replies off on purpose |

Later the same day (afternoon): the sandbox answers. The live council and private DMs stay quiet. Council inference is NPU `llama3.2:3b`. Delta 2 freshness is whatever the latest BLE file says (`observed`, `stale`, or `dead`), not the 02:35 "dead" label. See `HANDOFF.md` in this folder.
| FLM | On demand. Resident warmup is off |
| Geology and the other gated jobs | Off until you say otherwise |

Laptop was 100%, on AC. Disk about 60% (264 / 468 GB).

---

## Your calls

These are the decisions. Nothing below should be flipped by an agent from this document alone.

### 1. Legacy code stays until you name it

Standing rule from 2026-09-29: do not retire or delete G2 or G1 code without your explicit sign-off. "No live references" is not enough.

Still on disk at the 02:35 check:

- `~/.ollama/skills` — still the enabled `skills` sync row. Byte-identical copies of Pacific files were removed tonight. Unique and diverged files stayed. Dangerous leftover scripts exit immediately and do not run the old target. Latest skills commit at 02:16 HST was `6483586`.
- `/home/rootrecord/old ollama/old skills` — 27 GB, not part of that removal
- `Old repos deleted and merged/` — partial copy, still being filled

**Your call:** leave all of it, or name a specific tree you want retired. Until you name one, agents keep it.

### 2. No local website

Alexander removed the local site on 2026-09-30. `3 - RootRecord-Website` is gone, and port 3001 is closed. Do not run `next dev`, `npm run dev`, or any other local website on this desk.

The `website` catalog row stays disabled. `https://rootserver.rootrecord.cloud/` is the poller, not a site. The mainland desk copy is `1 - Servers/2 - RootRecord-US-Mainland-Server`, and that sync row stays disabled until Alexander says otherwise.

### 3. Daylight cameras

Grabs pass. Timelapse folders stay empty until the 05:00–19:00 HST window. Capture interval is still 1 second. WO-AEYES proposed 5 seconds and did not apply it.

**Your call:** after sunrise, look at one hourly compile. Say whether the interval stays 1 second or becomes 5.

### 4. River hardware actions

Reads on River 2 Pro pass. Actuating actions (solar-gate arm/disarm, AC always-on) are still unverified. Delta 2 action tests from 2026-09-23 are historical. That pack is dead, so do not schedule a Delta 2 actuation test.

**Your call:** when you want a hardware PASS, name the River action and the moment to run it.

### 5. Telegram replies

Morning check: replies were off. Afternoon the same day: the sandbox answers. Live council and private DMs stay quiet (`RR_RELAY_REPLIES` default 0). Council model is NPU `llama3.2:3b`. `getUpdates` timeouts after the reboot were a network retry, not a missing model.

**Your call:** leave the live council quiet, or opt in with `RR_RELAY_REPLIES=1`.

### 6. Turn-on batch (data only, no send)

These exist in `jobs.py` and stay off. One sentence from you can enable a named subset.

| Gate | Job |
| --- | --- |
| `RR_GEOLOGY=1` | Earthquake and volcano collect |
| `RR_KILAUEA_CAMS=1` | Kilauea cam stills |
| `RR_SUN_TIMES=1` | Sunrise and sunset file |
| `RR_UPTIME_LOG=1` | Desk up/down log |
| `RR_US_STATES=1` | US states weather dataset |
| `RR_SMART_DEVICES=1` | Smart-device collect |
| `RR_TEMPLATE_REPORTS=1` | Daily template reports |
| `RR_AI_REPORT=1` / `RR_AI_USAGE=1` | AI processing and usage reports |

Separate from that batch, because they move files or fill disk:

| Item | What you would be allowing |
| --- | --- |
| `weather_retention` | Dry run around 02:02 HST would have moved 0 files. Apply is still your call |
| `log_retention` | Dry-run job first. Live `--apply` needs its own yes (`RR_LOG_RETENTION_APPLY=1`) |
| `RR_RADAR_ZIP=1` | All-time radar zip growth |
| `path_index` | Full-disk path index. Job stays `enabled: False` until a separate yes |

### 7. Send, spend, and speaker batch

Built, gated, and staying off until you name the one you want.

- Council quake Telegram send (`RR_COUNCIL_QUAKE_SEND=1`)
- Earthquake Discord live post, Discord poller, Slack poller
- Kilauea public draft send
- Council health send
- Bruce stats posts
- Inbox drain and overnight relay
- Voice reports and live speaker play (`aplay`)
- Hurricane radio
- AdSense / AdMob live Google calls
- xAI chat, TTS, billing probe, Cursor fallback spend
- Cloud narrative live spend
- Stripe poll and Vercel build poll
- River-car DC drive (`RR_RIVER_CAR_DRIVE=1`)
- Discord bot credential rotation (WO-COM-002): issue a fresh token before any enable. Do not load a token from archive history

### 8. What gets published

WO-DATA is still open for this, not for the path. The canonical Database path is already in use.

**Your call:**

- Geology `*-last.json` and `Daily/*.jsonl` are still tracked. Say if they stay public or become local-only.
- Users / PII retention: do not copy people, users, or account-import into a repo.
- Timelapse masters: say whether those files stay local.
- The Pacific `cloudflared` binary is untracked. Say if it stays off git (recommended) or gets a published home.

### 9. Draft work orders

46 `WO-MIG-*` files sit in `Work-Orders/drafts/`. They are not a queue. Promote one only when you want that function accepted for execution.

### 10. Interaction modes need your ids, not a username

The build path is documented in `Documentation/02-agents/INTERACTION-MODES.md`. The registry already names `@rootrecordadmin`, `@WildEcho94`, and `@Crazychickenlady12`. Each `telegram_user_id` is null. Until you record the numeric Telegram ids, nobody can reach `READY_FOR_BUILD`, including a message that uses one of those names.

`cursor_api`, commit, push, merge, deploy, and recovery run ship off. Root Monitor can open a gate after a confirm. Opening one from this file does not turn it on.

**Your call:** paste the three numeric ids when you want the build ceiling to exist. Leave `cursor_api` off until you want a `READY_FOR_BUILD` request to call Cursor without a person starting the session. Do not unlock `restart_known_service` from this note.

---

## Suggested order, when you want to pick

1. Leave Delta 2 and the live stack alone. Root Monitor is the login window as of 02:33 HST. Conky is still off.
2. Local website stays off. Mainland sync row stays disabled unless you say otherwise.
3. After sunrise, accept or reject the timelapse hour and the 5-second camera interval.
4. Name a River action test only if you want actuation marked PASS.
5. Enable any data-only gates from section 6 in one list.
6. Name any send, spend, or speaker from section 7 one at a time.
7. Decide publication for geology files, timelapse masters, and the cloudflared binary.
8. Name a legacy tree only when you actually want it retired.
9. Record the three Telegram numeric ids before expecting a build to pass the principal check. Leave `cursor_api` off until you want that call.

---

## Work orders this list sits on

| ID | Still open because |
| --- | --- |
| WO-ECO-2026-09-27 | Out-of-scope imports and a few ownership checkboxes. Runtime path is done |
| WO-SRV-2026-09-27 | Your sign-off on actuation, timelapse, relay replies, and G2 retirement |
| WO-OLD-2026-09-28 | Next G1 packet, and no retirement without you |
| WO-GH-2026-09-27 | Website and mainland rows |
| WO-DATA-2026-09-27 | Publication and retention choices above |
| WO-AEYES-2026-09-27 | Interval and daylight timelapse |

Closed recently and not reopened by this list: WO-RPT-001, WO-ARCH, WO-SYS-001, WO-AGENT, WO-GH-001.
