# Solar-Pacific-RootRecord-Server-Old — Full Top-Level Catalog (95)

| Field | Value |
| --- | --- |
| **Date** | 2026-09-28 (HST) |
| **Source** | `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server-Old` main |
| **Companion** | [Solar-Pacific-Old-Inventory-Map-2026-09-28.md](./Solar-Pacific-Old-Inventory-Map-2026-09-28.md) |
| **Rule** | Classification only — not an import authorization |

---

## Legend

| Tag | Meaning |
| --- | --- |
| **G3-core** | Candidate for Pacific server domain after G2 |
| **G3-optional** | Maybe G3 after review |
| **Product** | Product / website / android — not Pacific core |
| **Library** | Docs, persona, governance → Library or Master-Prompt |
| **Database** | Data layout / sync policy → Database tree |
| **Archive** | History / origin — external or Library archive only |
| **Retire** | Likely superseded by G3 Automations or dead |
| **Review** | Needs operator decision |

---

## Full list (alphabetical)

| Top-level | Tag | Notes |
| --- | --- | --- |
| account-import | Review | Business ops skill |
| advertising | Product | AdMob / AdSense EOD |
| api | Pacific `System/ApiPrices` | WO-MIG-35. Price catalog plus xAI and Cursor clients. Spend off. |
| boot | Library / Retire | boot-idle-origin, boot-prelims — historical |
| clients | Pacific `Products/scripts/Clients/` | Gig index only. nibble.love theme is in `Archive/Website-Themes/`. Public page paused. |
| cloudflare-workers | G3-optional | Edge workers ≠ poller cloudflared binary |
| code-review | Review | |
| communications | G3-core | discord, slack, telegram |
| companions | Pacific `Products/scripts/Companions/` | Source copy. Not a running path. |
| core-ops-install | Review | Install helpers |
| council | Library / G3-optional | council-telegram, health, quake, bruce-stats |
| database | Database | d1, data-layout — not G3 git dump |
| day-board-boot | Review | |
| desk-data-reader | G3-optional | |
| earthquakes | G3-optional / Geology | |
| ecosystem-history | Archive | WO-MIG-06: decisions in Library `Documentation/00-architecture/Governance/`. Full tree archived, then removed from -Old. Not in G3 runtime. |
| ecosystem-index | Library | |
| energy | G3-core | ecoflow-* packets; **after G2 energy** |
| ensure-ava-runtime | Review | Agent runtime |
| feature-toggles | Review | |
| fern-forest | Pacific `Products/scripts/FernForest/` | Public TMK facts only. Parcel PDFs stayed in the local archive. |
| finance-desk | Pacific `Products/scripts/FinanceDesk/` | Source copy. Not a running path. No Stripe call. |
| fs-index | Pacific `System/PathIndex/` | WO-MIG-42 scoped index. Job off |
| git-auto-push | G3-core | Compare to G2 github/scripts |
| goals | Product | |
| governance | Library | WO-MIG-06: decisions in `Documentation/00-architecture/Governance/`. Packet removed from -Old. Not a Pacific job. |
| heartbeat | Retire / Review | G3 engine has heartbeat builtin |
| history | Archive | |
| holding | Archive | |
| host-metrics | G3-core | Align with system-stats |
| hourly-clip-reports | Review | Media reports |
| hybrid-night-poller | Retire | Superseded by G3 Automations poller? |
| idle-stop | Review | |
| inbox | Review | |
| inbox-drain | Review | |
| kilauea | Product / Geology | alerts, cams, weather-kilauea |
| kokoro | Review | TTS? |
| launch | Review | |
| live-data-pages | Product / Website | |
| live-directories | Archive | Topic desk archived with fs-index. WO-MIG-42 |
| load-categories | Review | |
| local-data-globe | G3-core | Network globe cousin |
| log-cleanup | G3-optional / Logs | |
| look | Pacific `Products/scripts/Look/` | `look.py` source only. DVR grabber was not copied into Pacific. |
| merged-morning | Review | |
| minecraft | Product | |
| model-pick | Review | Inference routing |
| morning-boot-replay | Pacific `Media/MorningBootReplay` | Dry-run replay of `boot_brief`. Speakers off. Archived 2026-09-30 |
| mp4-converter | Review | Media |
| mysql | Database | |
| net-gate | G3-optional | Internet gate cousin |
| network-globe | G3-core | Communications/network |
| obs-studio | Review | Streaming |
| ollama-client | G3-optional | Plumbing cousin |
| ollama-env | G3-optional | Plumbing |
| ollama-lifecycle | G3-optional | Plumbing |
| ops-banner | Review | |
| origin | Archive | **~4342 paths — never bulk into G3** |
| origin-session | Archive | WO-MIG-06: decision in Library Governance. Helper not restored. `origin/` not imported. Removed from -Old. |
| overnight-relay | Review | |
| panels-cam | G3-optional / Security | |
| pantry | Pacific `Products/scripts/Pantry/` | CLI on an empty Database store. `stock.json` was not imported. |
| people | Review | |
| persona | Library | Agent persona material |
| player-economy | Product | RootMC |
| product-prices | Pacific `Products/scripts/ProductPrices/` | CLI on an empty Database store. Price history was not imported. |
| public-chat | Product | |
| public-edge | Product / Website | |
| public-finance | Product | |
| public-health | Product | |
| python-drop-runner | Pacific `System/PythonDrop` | Empty allowlist. Job `system_python_drop` gated off (`RR_PYTHON_DROP`). |
| rcon | Product | Minecraft |
| recycle-origin | Archive | |
| remaining-tasks | Archive | |
| reply-feedback | Review | |
| reports | G3-core | After G2 worklog |
| research-oa | Review | |
| root-record-registry | Library / Review | |
| rootmc-android | Product | |
| scheduler-clock | Retire | Likely superseded by Automations |
| site-backgrounds | Product / Website | |
| site-ops | Product / Website | |
| skill-creator | Library / Review | |
| state | Review | |
| stripe-poll | Product | Billing |
| subscribers | Product | |
| sunrise-restore | Review | |
| synth | Media / CloudTTS | Gated Ara route beside Kokoro (WO-MIG-33). Live xAI call still needs sign-off |
| system-perf | G3-optional / System | |
| topics | Library / Review | |
| uptime-log | G3-optional / Logs | |
| users | Database / Product | PII care |
| vercel-builds | Product / Website | |
| weather | G3-core | After G2 weather |
| websites | Product | |

---

## Priority recovery queue (after G2)

1. `energy/ecoflow-*` (diff only)  
2. `weather/*` (non-media first)  
3. `communications/*`, `network-globe`, `local-data-globe`  
4. `host-metrics`, `system-perf`, `log-cleanup`, `uptime-log`  
5. `git-auto-push`  
6. `reports`  
7. `ollama-*` (plumbing)  
8. Everything else only with explicit operator pick  

---

*Full catalog 2026-09-28 HST from G1 tree listing.*
