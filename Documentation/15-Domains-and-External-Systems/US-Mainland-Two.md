# US-Mainland-Two

2026-10-02 ~21:52 HST: Pacific removed hourly `geology_collect` and `energy_sun_times`. ML2 `geology` already owns that fetch. Sun times is a catalog row with no clock and no collector script. The ML2 schedule was not armed. EcoFlow stays Pacific.

Current as of 2026-10-02 ~11:49 HST. This page is the live host role. The 2026-10-01 SSH and rename sitting is [2026-10-01 mainland rename and SSH tunnels](../01-Operations/2026-10-01-mainland-rename-and-ssh-tunnels.md). Do not treat OLD FILES or continuity plans as live ML1/ML2 truth. Mainland local commits only — **no push**.

| Field | Value |
| --- | --- |
| **Role** | Tunnel + GitHub-ops scaffolding, with **geology + weather_us_states + weather_hawaii + radio_rss** collectors (hurricanes via weather_hawaii), local API + analytics, and **verified** Pacific DB stream (SSH primary → same Database `path_rel` tree LLMs read; Telegram datapack fallback). **Not** a YouTube station. |
| **GitHub** | `RootRecord-Software-Solutions/US-Mainland-Two` |
| **Desk folder** | `1 - Servers/3 - RootRecord-US-Mainland-Two` (own `.git`; umbrella gitignores it) |
| **Host checkout** | `/home/ubuntu/US-Mainland-Server-2` |
| **Host** | `ip-172-31-15-254`, public `3.149.238.83` |
| **SSH** | `ssh ml2` → `ml2.rootrecord.cloud`. Direct fallback `ml2-ip` |
| **Tunnel** | `bd8e68a4-8a97-4b20-afd9-b058473a0a22`. Routes include `ml2.rootrecord.cloud` (SSH). `api.rootrecord.cloud` → ML2 `:8091` is live (`/health`, `/api/operations`, `/api/state`, analytics). |
| **Desk branch** | `main`, local tip `6560b75` (also `67e675c5078698b9cd2f0b577eed50d91a42ff9b`, `8cb0456`, `ca39035`, `6a6ebd8`, `08f6e05`; ahead, **no push**) |
| **Host SHA** | rsync deploy path (no push); Mainland desk-only sitting |
| **Ecosystem SHA** | desk umbrella; context only |
| **Library SHA** | RootRecord-Library; Wren desk-only this sitting |
| **Test-mode toggle** | Host `docs/TOGGLE.md` test-mode § (Library does not edit that file) |

**Current return (~11:45–11:49 HST):** Desk Cursor was offline from about 05:44–05:51 HST through about 11:45 HST. While down, `rootserver.rootrecord.cloud` returned HTTP 530 / Cloudflare 1033 (origin unreachable), ML2 `status_held` / Live `as_of` stayed frozen at about 05:44 HST, ML1 `live.mp3` stayed up, and the soft gate stayed ML2-on (`RR_LOCAL_DATA_POLL=0`); nobody flipped it. `:17022` was unmeasurable from Master during that window. On return, `rr-ml2-db-tunnel` has been active since about 11:45, rootserver is HTTP 200, ML2 `status_held` is about 11:47, handoffs are 0/0/0 (weather/media/geology), and `RR_LOCAL_DATA_POLL` is still 0. That tunnel and those handoffs are not an open attention item. The finite `overnight-station-check-till-7am` routine was deleted about 07:08 HST; its last fire still saw the desk offline, so Master has no final gate / `:17022` / River metrics from that pass. Morning checks took over from about 10:13 HST through noon. River and Delta readings for this window are on the EcoFlow pages. The ~04:58 paragraphs below, including River ~7.5% SOC and “overnight checks remain armed,” are that earlier sitting.

**Baseline post-reboot verification (~03:51 HST) — PASS:** Master Pacific remains live with the ML2-on gate (`RR_LOCAL_DATA_POLL=0`, intent `remote`), poller + `:8799` returning 200, Pacific `rr-ml2-db-tunnel` active on `:17022`, and Internet OK. The overnight ML2 stream stall and `:17022` tunnel conflict are cleared (~04:58 HST): `ml2-db-stream` now waits only on `network-online`, `scripts/run-stream.sh` uses `flock`, and handoffs drained 856→0. The desk `rr-aws-fetch-tunnel` unit is stopped/disabled; its remote-listen template is `:17023` if revived, leaving `:17022` to `ml2-db`. Collectors are OK; ML1 radio is OK; River is ~7.5% SOC with AC on; overnight checks remain armed. This is not a desk/net outage. If ML2 dies, the temporary Pacific poller remains the soft `RR_LOCAL_DATA_POLL=1` flip. AC-on if River dies remains a Master/EcoFlow decision.

## Public API origin (ML2) — not the AWS Fallback panel

Alexander (~03:00–03:02 HST; fallback restore ~03:04): **ML2 is the API.** Public hostname `api.rootrecord.cloud` → this host `:8091` (`/health`, `/api/state` arcs, `/api/operations`, analytics). That origin is **separate** from Root Monitor’s **AWS Fallback** page, which still aims at ML1 alias `rr-aws-ip` and `/home/ubuntu/rootrecord/fallback` (**restored** ~03:01–03:04; Status bindable again — see [US-Mainland-One](./US-Mainland-One.md)). Do **not** retarget the panel to ML2 without Alexander ask. Live flip already `RR_LOCAL_DATA_POLL=0` (survived reboot); banks keep landing. Automations data-poll remains the gate for Local Pacific vs ML2.

## Live inventory — authoritative (~04:58 HST)

**Bottom line:** Configured/live inventory is **geology + geology_kilauea_cams + weather_us_states + weather_hawaii + radio_rss** (hurricanes covered by `weather_hawaii`). SSH bank stream **PASS** is verified into the same Pacific Database `path_rel` tree desks/LLMs read. `radio_rss` is **LIVE again** after the `fetch` shadow fix; the later stream fix drained handoffs 856→0. Pacific `rr-ml2-db-tunnel` is active on `:17022`; the desk `rr-aws-fetch-tunnel` is stopped/disabled with `:17023` reserved as its revive template. Fix SHA: `6560b75` (local only, no push). **Not** a full poller move. Discord/Telegram *pollers* still scaffold. EcoFlow/cams/globe stay Pacific. Pacific remains the **only** LLM-readable long-term bank.

| State | What |
| --- | --- |
| **Working / status** | Radio on ML1; public API on ML2 (`/health`, `/api/state` arcs, `/api/operations`, analytics); collectors themselves OK; Pacific `rr-ml2-db-tunnel` active on `:17022` since about 11:45 HST (unmeasurable during the ~05:44–11:45 desk outage); `rr-aws-fetch-tunnel` stopped/disabled with `:17023` as the revive template; `RR_LOCAL_DATA_POLL=0` ML2-on intent, not flipped while the desk was blind; EcoFlow / cams / LAN globe **capture** Pacific; ML1 AWS Fallback restored. Handoffs at the ~11:47 `status_held` are 0/0/0 (weather/media/geology). Not an open attention item. The earlier ML2 stream stall and `:17022` conflict stay cleared. |
| **Not working / incomplete** | Full Home pageviews (Vercel, no client trackers — option C / ML2 logs only); Discord poller **blocked on token**; Telegram/Discord poller scaffolds not live (council-relay stays Pacific) |
| **ML2 LIVE collectors** | `geology` + `geology_kilauea_cams` (USGS still intake only; no vision) + `weather_us_states` + `weather_hawaii` (600s oneshot) + `radio_rss` — runner exclusive `RR_LOCAL_DATA_POLL=0` only; `radio_rss` is live again after the `fetch` shadow fix (SHA `67e675c`) |
| **Hurricanes** | Covered by `weather_hawaii` (not a separate live collector) |
| **Pacific gated off** while `RR_LOCAL_DATA_POLL=0` | `geology_collect`, `geology_kilauea_cams`, `weather_poller` (Hawaiʻi), `weather_us_states`, `weather_radar_zip`, `weather_retention`, `country_location_pollers`, `radio_rss_poll` |
| **Still Pacific forever** | EcoFlow / Energy; smart cams; `network_globe` LAN tap; Telegram **council-relay** — **not** in the ML2 exclusive gate and **not** moving |
| **Stream** | SSH primary into same Database `path_rel` tree LLMs read; Telegram datapack fallback; Pacific datapack-pickup allowlist expanded + `ml2_datapack_pickup` job (timer+boot) |
| **Scaffold / not live** | Discord poller (no token); Telegram poller scaffold (council-relay stays Pacific); country locations |
| **Verified Kīlauea Cams bank** | ML2 `geology_kilauea_cams` takes USGS stills only (no vision), remains in `LOCAL_DATA_POLL_JOBS` as a soft toggle, streams the handoff under exclusive `RR_LOCAL_DATA_POLL=0`, and wipes scratch after stream; Pacific Cams bank is durable/LLM-readable |
| **Purge / no-stack** | `ml2-purge` extended (`8cb0456`) wipes weather-bank archive/imagery scratch (+ radio-bank); handoff stays ~0 after stream. Weather-bank scratch was ~295M before scrub — ML2 must never accumulate |

**Cleared (~04:58 HST):** The ML2 bank-stream stall and `:17022` tunnel conflict are closed. `systemd/ml2-db-stream.service` now waits only on `network-online`; `scripts/run-stream.sh` uses `flock`, including on the host; handoffs drained 856→0. Pacific `rr-ml2-db-tunnel` is active on `:17022`. The desk user unit for `rr-aws-fetch-tunnel` is stopped/disabled, with a `:17023` remote-listen template if revived. SHA `6560b75` is local only; Pacific `RR_LOCAL_DATA_POLL=0` is untouched and the weather daemon remains down. ML1 radio and the desk/network remain OK.

**Cleared weather soft-gate finding (~04:56 HST):** Master left ML2-on intent and `RR_LOCAL_DATA_POLL=0` unchanged. `Weather/scripts/ensure-weather-poller.sh` refuses starts when the gate is off, using the environment or `rr-data-poll.conf`; `Automations/scripts/supervise-services.sh` soft-stops weather when gated off and does not respawn it. The live daemon (pid 197847) was soft-stopped and verified down. Relay untouched. Backups `*.bak-20261002-weather-gate` sit beside both scripts.

### Sample paths (room confirm ~03:23 HST) — Pacific Database

- `Weather/Hawai'i/ml2-collector-status.json` — ok
- `Weather/Hawai'i/reports/` hurricane tracks — fresh
- `Media/RadioRss/` health/queue — ok


## Verified — Kīlauea `*_current` bank + archive-on-replace (~03:31 HST)

The first `*_current` bank is **LIVE and verified**. ML2 `geology_kilauea_cams` performs USGS still intake only (no vision on the mainland host), is enabled under the exclusive `RR_LOCAL_DATA_POLL=0` gate and remains in `LOCAL_DATA_POLL_JOBS` as a soft toggle, streams the handoff to Pacific, and wipes scratch after stream. Pacific is the only durable/LLM-readable bank and the only side that looks at the images.

- Live paths: `Geology/Volcanoes/Hawaii/Cams/v1cam_current.jpg`, `v2cam_current.jpg`, `v3cam_current.jpg`, and `Geology/Volcanoes/Hawaii/Cams/cams_current.json`.
- `cams_current.json` records `photo_viewed` and per-camera `fetched_at`, `bytes`, `sha`, `ok`, and `error`.
- Pacific `rr_db_stream_receive` (and datapack twin when used) archives any filename containing `_current` on replacement as `archive/YYYYMMDD/<stem>_<HHMMSS><ext>`. The live `_current` is always newest for LLM reads; archive is history only. Verified example: `Geology/Volcanoes/Hawaii/Cams/archive/20261002/v3cam_current_033046.jpg`.
- `kilauea_look` prefers `*_current` over `*-last`; `v3cam_current.jpg` was verified with `source_kind=current`.
- EcoFlow stays Pacific forever. ML2 never runs vision; Pacific LLMs look.

Local SHAs (no push): ML2 `5f3d5c841a10145a33cb1723ee17e1097637f4a2`; Pacific `5bc07464631aa429c0d5813c55fe5db9455315bf`; Ecosystem `0bd1ecbd292863f8e39dea1696959a8bcf31ba70`.

### Verified — report blend (~03:33 HST)

Report Instructor confirmed the look/report blend. The report states whether a still was viewed (**Y/N**) and, when viewed, what conditions looked like. The bank, paths, archive-on-replace, Pacific-only looking, and report blend are verified.


### Room confirms (~03:02–03:04; stream-verify + scrub ~03:23 HST)

- **Master:** AWS Fallback Status should bind ON/OFF after recreate; leave panel on ML1; don’t confuse with ML2 API; globe units stay masked / flags forced off; classic activate expecting `:8090` won’t pass by design.
- **Report Instructor:** earthquake / Kīlauea / NWS Hawaiʻi / hurricane / radio news hour banks refresh from ML2→Pacific path_rel (SSH verified ~03:23). Stale-desk notes **cleared**. Analytics pull still hits ML2 API fine.
- **Cove:** Vercel up, no client trackers; Home/Live pull `api.rootrecord.cloud` (ML2) for arcs/ops; Radio page listens to ML1 only — no poller dependency on the Website tree.
- **Mainland (~03:23):** weather_hawaii + radio_rss live; SSH stream verified; Discord/Telegram pollers scaffold only; `8cb0456` purge no-stack scrub.

## Live host check (2026-10-02 ~02:50 HST) — supersedes ~02:10 / ~02:26 / ~02:29 / ~02:39

Mainland landed ML2 analytics + bank path; **schema parity PASS** (~02:39) still stands. Desk data-poll **flipped to ML2 LIVE** (~02:50). Desk ML2 `6425c8a`, host `087ee38`, Ecosystem `00985524`, Library `2fc7a47`.

- **API + analytics:** `ANALYTICS.md` in the ML2 tree; endpoints `/api/analytics/daily`, `/api/analytics/period`, `/api/analytics/current` on `:8091`. Desk sink: Pacific Database `Logs/Website/analytics/`. Pacific `Website/scripts/analytics_pull.py` (job `analytics_pull`, gate `RR_ANALYTICS_PULL=1`, off until armed) consumes `/api/analytics/daily` into that bank for voice `bandwidth_desk` / `current_report`.
- **Stream verified:** 7 handoffs reached Pacific `Geology/` + `Weather/US-States/`; the later drain reached 856→0. `ml2-db-stream` runs via active desk tunnel `rr-ml2-db-tunnel` on `:17022`; `systemd/ml2-db-stream.service` waits only on `network-online` and `scripts/run-stream.sh` serializes with `flock`.
- **Collectors on (first-test only):** `geology` and `weather_us_states` **only**. Other internet-facing modules stay scaffold/staged — not a full poller move (see First-test scope §).
- **Pacific gate (LIVE ~02:50 HST):** Settings write mode, `data_poll_desired=ml2`; drop-in `~/.config/systemd/user/rr-rootserver-poller.service.d/rr-data-poll.conf` sets `Environment=RR_LOCAL_DATA_POLL=0`; intent `data_poll_mode.yaml` `mode=remote`; poller restarted. Verified `live_raw=0` / `live_label=ML2 offload`; `:8799` HTTP 200. **Clears** earlier “`RR_LOCAL_DATA_POLL` still not flipped” / default-local-ON-as-current-live notes. Code fail-safe default remains local ON when unset; live desk is now gated off. Toggle-not-replacement: home collectors stay installed; gate flipped only. No git commit.
- **Toggle plan:** toggle-not-replacement + later local-mirror plan already filed (~02:26); SHAs and live stream/analytics state attached here; GTK UI filed ~02:32; live flip applied ~02:50.

### Post-boot verification + globe /api/state (~02:52–02:57 HST)

Desk rebooted into ML2 mode; drop-in `RR_LOCAL_DATA_POLL=0` was already on disk — **flip LIVE notes above still stand**. Alexander observed: radio online; EcoFlow and cameras online; no network trackers on Vercel yet; API still needs work; globe initially showed no ping-line connectors.

**Room confirms (same sitting):** Master — poller still `RR_LOCAL_DATA_POLL=0` through reboot; `:8799` HTTP 200; EcoFlow/cams Pacific matches toggle; radio up. Cove — `www` Vercel stays without client trackers (option C / ML2 logs only); Home ping lines are `/api/state`; if hard refresh still blanks after feed push, Cove will check `home.js` on desk. Report Instructor measured (~02:58) — poller active / `RR_LOCAL_DATA_POLL=0`; WAVs nws 02:24 / solar_desk 02:28 / bandwidth 02:31 / current_report md 02:33 all pre-reboot (no new voice cycle yet); analytics as_of 02:28:35 daily present; automations log fresh 02:58 no recent voice_/report_ failures; next stack expected at live `:22`/`:52` (see voice-desk).

**Globe arcs restored (~02:55–02:56 HST):** Empty arcs were an ML2 stub. `api.rootrecord.cloud/api/state` now carries **11 arcs / 7 points** fed from Pacific live LAN rebroadcast (`Communications/network/local-data-globe` → `hawaii-current.ndjson`) into ML2 `var/cache/api/state.json` — globe capture is **not** running on ML2. Ops seed / `status-current` refreshed ~02:55–02:56 HST. Recurring desk user timer `rr-ml2-globe-state-push` every 2m. Desk ML2 commits `6c66bf1` + `819f68e` (ahead, **no push**). LAN capture stays Pacific; EcoFlow stays Pacific (expected with the toggle).

Disk recovery and API enable from ~02:10 remain in force (`ml2-api`, `ml2-collectors`, `ml2-purge` installed). Sysmon remains staged/off.

### Stream path (now working) — schema parity PASS (~02:39 HST)

- Active desk `rr-ml2-db-tunnel` → `:17022` carries `ml2-db-stream` NDJSON home; the separate desk `rr-aws-fetch-tunnel` unit is stopped/disabled and reserves `:17023` if revived.
- Verified landings: Pacific Geology + Weather/US-States (7 handoffs). Banks and paths: `Geology/*`, `Weather/US-States/us-last.json`; stream drains handoffs after ack.
- **Schema parity PASS vs Pacific** (Mainland fix ~02:39 HST; clears prior FAIL blocker): ML2 `geology` + `weather_us_states` now match Pacific last-file contracts — quakes enriched `events[]` with `nearest`/`time_hst`/`kilauea_150km_count`; volcanoes / `hvo-last` Pacific shape with top-level `alert_level`/`color_code`/`erupting`/`latest_notice`/`at`; `us-last` `{updated_at, location_count:77, rows}`; `collector-last` `sources{}`. Vendored `config/geology/global-locations.json` for nearest + US locations. SHAs: desk ML2 `6425c8a`, host `087ee38`, Ecosystem `00985524`, Library `2fc7a47`. Local commits desk+host; no push; ML1 radio untouched. **Data-poll flipped to ML2 LIVE ~02:50** (`RR_LOCAL_DATA_POLL=0`; schema PASS still stands).
- Earlier blockers (missing stream key / receiver / forced-command) remain cleared; keep purge as safety until acks stay healthy.

## What is in the tree

The desk tree and host checkout run a live path under the toggle plan:

- `collectors/` — geology, Kīlauea camera, weather (Hawaiʻi, US states, country locations, hurricanes), and radio-RSS modules plus the runner. **LIVE / stream-verified (~03:51):** `geology` + `geology_kilauea_cams` (USGS still intake only; no vision) + `weather_us_states` + `weather_hawaii` (600s oneshot; hurricanes via this module) + `radio_rss`, live again after the `fetch` shadow fix (SHA `67e675c`). Collectors were still finishing the weather_hawaii cycle (~9m); `radio_rss` will log on that pass. The soft `RR_LOCAL_DATA_POLL=0` gate is unchanged. Runner exclusive gate is `RR_LOCAL_DATA_POLL=0` only. Still scaffold / not enabled: country locations, Discord/Telegram pollers. Kīlauea cam scratch is wiped after stream. Not a full poller move.
- `stream/` — clean SSH NDJSON client/protocol and `home_receiver.py` for the Pacific Database. **`ml2-db-stream` verified** through desk `rr-ml2-db-tunnel` `:17022`.
- `api_local/` — local API status-cache sync; it overwrites `var/cache/api/` and does not stream API-circulated metrics home. **`ml2-api.service` is enabled** on `:8091`, including analytics routes.
- Analytics — `ANALYTICS.md`; `/api/analytics/daily|period|current`; aggregates land under desk `Logs/Website/analytics/`. Pacific pull consumes daily for voice reports (gate `RR_ANALYTICS_PULL`).
- `config/` — collector, purge, toggle-example, stream, and deny-list policy. Operator toggle: host `docs/TOGGLE.md` test-mode §.
- `scripts/` — `run-collectors.sh`, `run-stream.sh`, `ml2-purge.sh`, `run-api-local-sync.sh`, and the kept `aws-git-pull.sh`.
- `systemd/` — **`ml2-api`**, **`ml2-collectors`**, **`ml2-purge`**, and **`ml2-db-stream`** are in the live path for this sitting. **`ml2-sysmon`** remains staged files only. The `aws-git-pull` scaffolding remains kept and its timer is not installed on the host.

LAN globe **capture** stays Pacific-local (network-globe module refused on ML2). Pacific rebroadcast feeds ML2 `var/cache/api/state.json` for public arcs (see post-boot §). The existing cloudflared tunnel serves the live API on `:8091`.

## 2026-10-02 staged system monitor (not installed)

Commit `7065795` stages ML2 collect → send → self-purge alongside the existing collector and ephemeral-handoff policy; it is not installed on the live host. `system-monitor/` sends primary SSH NDJSON to the Pacific `System/scripts/rr_db_stream_receive.py` and purges the local handoff after receiver acknowledgement. `config/sysmon-stream.yaml` remains `enabled: false`; `systemd/ml2-sysmon.{service,timer}` are staged files only. If SSH fails or remains disabled, `telegram_datapack.py` sends a zip through the separate datapack bot, then purges after `sendDocument` acceptance; Pacific `datapack-pickup.py` drains it into Database. The verified Database scaffold is commit `65dea848`, reserving `System/metrics/ml2/`, `Intake/ml2/`, `Logs/ML2/sysmon/`, and `Network/datapacks/{inbox,processed,state}/`. Geology + US-states weather collectors, API/analytics, purge, and DB stream are live; **sysmon remains staged/off**. YouTube remains wiped; EcoFlow/Energy stays denied and Pacific-only. Operator detail lives in Pacific `System/docs/MAINLAND-SYSMON-INTAKE.md`.

## Ephemeral handoff policy — locked

Pacific is the **only long-term / LLM-readable data bank**. ML2 never accumulates a retention archive: `var/raw/` is processed into a handoff, raw is deleted when the handoff is written, and `var/handoff/` is streamed as clean SSH NDJSON and deleted after a successful receiver acknowledgement (handoff≈0 after stream). Hourly **`ml2-purge`** remains as safety for leftovers without acks — extended (`8cb0456`) to wipe **weather-bank archive/imagery** (and radio-bank) scratch so ML2 never stacks (~295M weather-bank scratch observed before scrub). API-circulated status and home metrics are overwritten locally under `var/cache/api/` and are not streamed.

EcoFlow and all energy data are Pacific-only. ML2 collectors must not collect or stage `Energy/`; `config/stream_deny.yaml` rejects `Energy/`, `RootRecord/`, status snapshots, the `energy`/`ecoflow` domains, and the `api_mirror` cache domain. Smart devices, security cameras, and Pacific LAN globe capture likewise stay on Pacific.

## Pacific data-poll toggle — not a replacement

Alexander (2026-10-02 ~02:26 HST; SHAs attached ~02:29; schema FAIL ~02:34 cleared PASS ~02:39; **live flip ~02:50**; exclusive-gate rule ~03:08–03:09): this is a **toggle**, not a cutover that deletes home collectors. Pacific/home data polling **stays installed**. `RR_LOCAL_DATA_POLL` in Pacific `automation_control.py` (host `docs/TOGGLE.md` test-mode §) turns local polling **off** while ML2 is healthy; if AWS/ML2 dies, flip local polling **back on**. Never delete home collectors as the path to ML2. Code fail-safe default remains local ON when the env is unset. **Live desk (~02:50 HST):** gate flipped — Settings write / `desired=ml2`, drop-in `rr-data-poll.conf` `RR_LOCAL_DATA_POLL=0`, intent `data_poll_mode.yaml` `mode=remote`, poller restarted; verified `live_raw=0` / `live_label=ML2 offload`, `:8799` HTTP 200. No git commit. Schema parity PASS ~02:39 still stands. Current SHAs: desk ML2 `6425c8a`, host `087ee38`, Ecosystem `00985524`, Library `2fc7a47`.

### Exclusive gate (Alexander standing rule ~03:08–03:09 HST)

**Exclusive:** if AWS/ML2 data-poll is **on**, solar (Pacific local) data-poll is **off**; if solar/local is **on**, AWS/ML2 pollers are **off**. Soft kill-switch only — do **not** delete or hardcode collectors; Pacific collectors stay installed; `RR_LOCAL_DATA_POLL` flips them. Pacific already gates on `RR_LOCAL_DATA_POLL`; Mainland runner honors the same exclusive gate (`RR_LOCAL_DATA_POLL=0` only). **PASS (~03:51 HST):** `weather_hawaii` + `radio_rss` are live again after the `fetch` shadow fix; handoff drained ~656→1 and Cams/RadioRss banks freshened ~03:44. Reboot Working attention is clear. Discord/Telegram *pollers* remain scaffold (Discord blocked on token; council-relay stays Pacific). Clean bounce if needed when enabling more. **EcoFlow / Energy and smart cams stay Pacific forever** — they are **not** part of this exclusive gate and are **not** moving to ML2.

**Near-term** (now live): collectors (geology + weather_us_states + weather_hawaii + radio_rss), SSH stream (verified into Database path_rel; Telegram datapack fallback), and API/analytics are live with Pacific local data-poll gated **off** (`RR_LOCAL_DATA_POLL=0`) while ML2 is healthy under the exclusive gate. Pacific remains the **sole long-term / LLM-readable bank**. EcoFlow/energy, smart cams, LAN globe, voice, local devices, tunnel, council-relay, and durable Database stay Pacific-owned forever (outside the exclusive gate).

**GTK Automations UI (desk, landed ~02:32; live flip ~02:50; kill-switch fix ~03:14 HST):** Root Monitor Automations Local Pacific vs ML2 **data-poll** control under Pacific `Apps/Control-Panel/` (`Lib/rr_data_poll.py`, `rr_settings.py`, `rr_automations_page.py`, `rr_control_panel.py`) + `Automations/scripts/automation_control.py` (`job_enabled` Live-binds). Panel code defaults remain dry-run / desired=local / apply_dropin=false. **Overnight left ML2-on (~03:14):** `desired=ml2`, drop-in `RR_LOCAL_DATA_POLL=0`, intent `mode=remote`, ML2 timers active, poller `:8799` live; **kill-switch verified both ways** (drop-in + restart + sync-ml2; Live=ML2 offload; gated jobs Off + “ML2 owns”). Soft only — EcoFlow/cams ungated. Intent YAML: no inline `#` on `mode:` line. Settings keys `data_poll_restart_poller` + `data_poll_sync_ml2` enabled on desk (Alexander can confirm later). Operator detail: `Guides & Tutorials/Root-Monitor-Operators-Handbook/Root-Monitor-Operators-Handbook.md` · contract: [Desk-Automations-and-Service-Windows.md](../11-Runtime-Jobs-and-Control/Desk-Automations-and-Service-Windows.md). Do not treat that UI as a cutover that deletes collectors.

**Later** (document now, implement later — not building yet): move/mirror functions into the two mainland desk repos (`US-Mainland-One`, `US-Mainland-Two`) so work can run from those trees locally with no behavioral difference if mainland servers go down — local desk as failover parity.

## Recent ML2 commits

- `6560b75` — **Clear ML2 stream stall and tunnel conflict**: decouple `ml2-db-stream` from `ml2-collectors` (`After=network-online` only), serialize `scripts/run-stream.sh` with `flock`, drain 856→0, and keep `ml2-db` on `:17022` while the stopped/disabled `rr-aws-fetch-tunnel` uses `:17023` if revived. Local only; **no push**.
- `67e675c5078698b9cd2f0b577eed50d91a42ff9b` — **Fix RadioRss fetch-module shadowing**: evict foreign Weather `fetch`, prefer `vendor/RadioRss/scripts`, and return `radio_rss` to live service. Host shadow repro `ok=True` with 80 stories; handoff drained ~656→1; Cams/RadioRss banks freshened ~03:44. Local only; **no push**.
- `8cb0456` — Desk (US-Mainland-Two): **no-stack scrub** — `ml2-purge` wipes weather-bank archive/imagery scratch (radio-bank too); handoff stays ~0 after stream. Pacific remains only LLM-readable bank. Local; **no push**.
- `08f6e05` — Desk: `OFFLINE-TELEGRAM-BUFFER.md` + clearer systemd Descriptions (labels). Local; **no push**.
- `6a6ebd8` — Desk: Discord/Telegram poller scaffolds + stream Telegram datapack fallback. Pollers not live (Discord blocked on token; council-relay stays Pacific). Local; **no push**.
- `ca39035` — Desk: live `weather_hawaii` + `radio_rss` via vendor Weather/RadioRss; runner exclusive `RR_LOCAL_DATA_POLL=0`. Local; **no push**.
- `819f68e` / `6c66bf1` — Desk (US-Mainland-Two): globe `/api/state` feed from Pacific `local-data-globe` rebroadcast (`hawaii-current.ndjson` → `var/cache/api/state.json`); ops status-current refresh; desk timer `rr-ml2-globe-state-push` every 2m. Ahead of origin; **no push**. Host rsync path unchanged this note.

- `484abe1` — Desk (US-Mainland-Two): analytics + bank path; geology + weather_us_states; stream verified. Host deployed as `559f90e` via rsync (no push). Ecosystem context `bfa9ff2f`.
- `84c4a37` — Desk: earlier test-mode geology collectors + `:8091` API enable path (superseded live state above; host was `3274fb3`).
- `7065795` — **Stage ML2 system monitor + extend stream allowlist for metrics**: collect/send/purge scaffold, `enabled: false` stream config, and staged `ml2-sysmon` units.
- `737b583` — **Stage ML2 data collectors and SSH home-DB stream scaffold**: collectors, stream client/receiver, toggle example, inventory, and staged units.
- `abd4bd0` — **ML2 ephemeral handoff + purge (ML1 mirror); EcoFlow excluded**: raw/handoff purge, API-local overwrite cache, deny-list, and policy docs.
- `04142d5` — **Remove failed YouTube station experiment**: the desk wipe commit.

## Listeners — YouTube stills (2026-10-02 ~12:54 HST)

Alexander: the radio mix is causing trouble for other users, so listeners move to YouTube, and video is not allowed. Mainland: stills only, the live ML1 station is not being touched, and the wiped video stack below is not coming back. This is an order, not a running encoder. No stills path is built. `live.mp3` is still on the air. Superseded ~13:27 HST: Alexander reopened YouTube on ML1. Picture is `1 - Servers/ML1 REBUILD/youtube-thumb.png`, not the live website. Radio page is to embed the active livestream at https://www.youtube.com/@rootmcnews. ML1 renders the local mix and YouTube in parallel. Mainland is wiring it. Not live yet. The wiped ML2 tree stays wiped. ~12:56 HST: Report Instructor keeps reports as audio and will not make a video version or touch the station. Cove’s ~12:56 hold (keep the Radio page on the live mp3 and do not embed) is superseded by this ~13:27 order. Cove landed the embed ~13:31 HST in `Website/Home/radio/index.html` (channel UC6M7U4fXAWuVYhgm_veKecA, `https://www.youtube.com/embed/live_stream?channel=UC6M7U4fXAWuVYhgm_veKecA`). The page no longer plays `live.mp3` or loads `radio.js`. `Website/Home/assets/site.css` styles `.radio-frame`. The ML1 broadcast itself is not verified on the air. Reports stay audio.

## YouTube experiment — ended 2026-10-02

Decision: the YouTube / rr-streaming station on ML2 is **scrapped**. Alexander owns any future process himself. That video station stays scrapped. The ~12:54 HST listen order is a new stills path, not a restore of this one. Geology + US-states weather collectors, local API/analytics, and Pacific DB stream are live; sysmon remains staged/off.

YouTube paths are gone: `youtube/`, `station/`, the experiment config and `requirements.txt`, `rr-youtube-station.service`, `/etc/rootrecord` YouTube env/oauth, `youtube-venv`, `chromium-profile`, and `/var/lib/rootrecord`. Disk recovery at ~02:10 also purged leftover YouTube-related packages (chromium/gnome/mesa/cups) after apt/snap cache clean.

Backup (mode 600), desk Downloads:

- `/home/rootrecord/Downloads/ml2-youtube-backup-20261002.tar.gz` (31M)
- stamped twin `…-20261002-002841` (same bytes)

Contents covered host secrets, unit file, full checkout, youtube-venv, chromium-profile, `/var/lib/rootrecord`, desk tree copy, and Downloads `client_secret_*.json` (those leftovers were removed from Downloads after the backup).

Local commits (authorized; **not pushed** from the wipe seat): desk `04142d5`, host `6c5070d`, message “Remove failed YouTube station experiment”. Two different remotes — desk automation covers the desk repo; the host remote updates only if that checkout’s publish path runs.

## What stays elsewhere

Mainland One is the radio tree and, as of ~13:27 HST, the ordered YouTube broadcaster (public page embed landed ~13:31 HST; the broadcast is not verified on the air). See [US-Mainland-One](./US-Mainland-One.md) and [2026-10-01 radio station](../01-Operations/2026-10-01-radio-station.md). `www` stays on Vercel. Pacific keeps the poller and the durable Database. Do not restore the YouTube tree from the backup onto the live host. Alexander’s ~12:54 HST ask is a new stills path, not permission to put this tree back.
