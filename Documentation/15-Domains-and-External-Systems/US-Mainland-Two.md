# US-Mainland-Two

Current as of 2026-10-02 ~02:57 HST. This page is the live host role. The 2026-10-01 SSH and rename sitting is [2026-10-01 mainland rename and SSH tunnels](../01-Operations/2026-10-01-mainland-rename-and-ssh-tunnels.md). Do not treat OLD FILES or continuity plans as live ML1/ML2 truth.

| Field | Value |
| --- | --- |
| **Role** | Tunnel + GitHub-ops scaffolding, with geology + US-states weather collectors, local API + analytics, and verified Pacific DB stream. **Not** a YouTube station. |
| **GitHub** | `RootRecord-Software-Solutions/US-Mainland-Two` |
| **Desk folder** | `1 - Servers/3 - RootRecord-US-Mainland-Two` (own `.git`; umbrella gitignores it) |
| **Host checkout** | `/home/ubuntu/US-Mainland-Server-2` |
| **Host** | `ip-172-31-15-254`, public `3.149.238.83` |
| **SSH** | `ssh ml2` → `ml2.rootrecord.cloud`. Direct fallback `ml2-ip` |
| **Tunnel** | `bd8e68a4-8a97-4b20-afd9-b058473a0a22`. Routes include `ml2.rootrecord.cloud` (SSH). `api.rootrecord.cloud` → ML2 `:8091` is live (`/health`, `/api/operations`, `/api/state`, analytics). |
| **Desk branch** | `main`, local `819f68e` (US-Mainland-Two; also `6c66bf1`; ahead, no push) |
| **Host SHA** | `087ee38` (US-Mainland-Server-2; rsync deploy; no push) |
| **Ecosystem SHA** | `00985524` (desk umbrella; context only) |
| **Library SHA** | `2fc7a47` (RootRecord-Library; context only) |
| **Test-mode toggle** | Host `docs/TOGGLE.md` test-mode § (Library does not edit that file) |

## Live host check (2026-10-02 ~02:50 HST) — supersedes ~02:10 / ~02:26 / ~02:29 / ~02:39

Mainland landed ML2 analytics + bank path; **schema parity PASS** (~02:39) still stands. Desk data-poll **flipped to ML2 LIVE** (~02:50). Desk ML2 `6425c8a`, host `087ee38`, Ecosystem `00985524`, Library `2fc7a47`.

- **API + analytics:** `ANALYTICS.md` in the ML2 tree; endpoints `/api/analytics/daily`, `/api/analytics/period`, `/api/analytics/current` on `:8091`. Desk sink: Pacific Database `Logs/Website/analytics/`. Pacific `Website/scripts/analytics_pull.py` (job `analytics_pull`, gate `RR_ANALYTICS_PULL=1`, off until armed) consumes `/api/analytics/daily` into that bank for voice `bandwidth_desk` / `current_report`.
- **Stream verified:** 7 handoffs reached Pacific `Geology/` + `Weather/US-States/`. `ml2-db-stream` runs via desk tunnel `rr-ml2-db-tunnel` on `:17022` (not the earlier “stream still off” state).
- **Collectors on:** `geology` and `weather_us_states` (other internet-facing collectors remain staged for review).
- **Pacific gate (LIVE ~02:50 HST):** Settings write mode, `data_poll_desired=ml2`; drop-in `~/.config/systemd/user/rr-rootserver-poller.service.d/rr-data-poll.conf` sets `Environment=RR_LOCAL_DATA_POLL=0`; intent `data_poll_mode.yaml` `mode=remote`; poller restarted. Verified `live_raw=0` / `live_label=ML2 offload`; `:8799` HTTP 200. **Clears** earlier “`RR_LOCAL_DATA_POLL` still not flipped” / default-local-ON-as-current-live notes. Code fail-safe default remains local ON when unset; live desk is now gated off. Toggle-not-replacement: home collectors stay installed; gate flipped only. No git commit.
- **Toggle plan:** toggle-not-replacement + later local-mirror plan already filed (~02:26); SHAs and live stream/analytics state attached here; GTK UI filed ~02:32; live flip applied ~02:50.

### Post-boot verification + globe /api/state (~02:52–02:57 HST)

Desk rebooted into ML2 mode; drop-in `RR_LOCAL_DATA_POLL=0` was already on disk — **flip LIVE notes above still stand**. Alexander observed: radio online; EcoFlow and cameras online; no network trackers on Vercel yet; API still needs work; globe initially showed no ping-line connectors.

**Globe arcs restored (~02:55–02:56 HST):** Empty arcs were an ML2 stub. `api.rootrecord.cloud/api/state` now carries **11 arcs / 7 points** fed from Pacific live LAN rebroadcast (`Communications/network/local-data-globe` → `hawaii-current.ndjson`) into ML2 `var/cache/api/state.json` — globe capture is **not** running on ML2. Ops seed / `status-current` refreshed ~02:55–02:56 HST. Recurring desk user timer `rr-ml2-globe-state-push` every 2m. Desk ML2 commits `6c66bf1` + `819f68e` (ahead, **no push**). LAN capture stays Pacific; EcoFlow stays Pacific (expected with the toggle).

Disk recovery and API enable from ~02:10 remain in force (`ml2-api`, `ml2-collectors`, `ml2-purge` installed). Sysmon remains staged/off.

### Stream path (now working) — schema parity PASS (~02:39 HST)

- Desk `rr-ml2-db-tunnel` → `:17022` carries `ml2-db-stream` NDJSON home.
- Verified landings: Pacific Geology + Weather/US-States (7 handoffs). Banks and paths: `Geology/*`, `Weather/US-States/us-last.json`; stream drains handoffs after ack.
- **Schema parity PASS vs Pacific** (Mainland fix ~02:39 HST; clears prior FAIL blocker): ML2 `geology` + `weather_us_states` now match Pacific last-file contracts — quakes enriched `events[]` with `nearest`/`time_hst`/`kilauea_150km_count`; volcanoes / `hvo-last` Pacific shape with top-level `alert_level`/`color_code`/`erupting`/`latest_notice`/`at`; `us-last` `{updated_at, location_count:77, rows}`; `collector-last` `sources{}`. Vendored `config/geology/global-locations.json` for nearest + US locations. SHAs: desk ML2 `6425c8a`, host `087ee38`, Ecosystem `00985524`, Library `2fc7a47`. Local commits desk+host; no push; ML1 radio untouched. **Data-poll flipped to ML2 LIVE ~02:50** (`RR_LOCAL_DATA_POLL=0`; schema PASS still stands).
- Earlier blockers (missing stream key / receiver / forced-command) remain cleared; keep purge as safety until acks stay healthy.

## What is in the tree

The desk tree and host checkout run a live path under the toggle plan:

- `collectors/` — geology, Kīlauea camera, weather (Hawaiʻi, US states, country locations, hurricanes), and radio-RSS scaffold modules plus the runner. **Live now:** `geology` and `weather_us_states` via `ml2-collectors.timer`. Other internet-facing collectors stay staged for review.
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

Pacific is the **only long-term data bank**. ML2 never accumulates a retention archive: `var/raw/` is processed into a handoff, raw is deleted when the handoff is written, and `var/handoff/` is streamed as clean SSH NDJSON and deleted after a successful receiver acknowledgement. Hourly **`ml2-purge`** remains as safety for leftovers without acks. API-circulated status and home metrics are overwritten locally under `var/cache/api/` and are not streamed.

EcoFlow and all energy data are Pacific-only. ML2 collectors must not collect or stage `Energy/`; `config/stream_deny.yaml` rejects `Energy/`, `RootRecord/`, status snapshots, the `energy`/`ecoflow` domains, and the `api_mirror` cache domain. Smart devices, security cameras, and Pacific LAN globe capture likewise stay on Pacific.

## Pacific data-poll toggle — not a replacement

Alexander (2026-10-02 ~02:26 HST; SHAs attached ~02:29; schema FAIL ~02:34 cleared PASS ~02:39; **live flip ~02:50**): this is a **toggle**, not a cutover that deletes home collectors. Pacific/home data polling **stays installed**. `RR_LOCAL_DATA_POLL` in Pacific `automation_control.py` (host `docs/TOGGLE.md` test-mode §) turns local polling **off** while ML2 is healthy; if AWS/ML2 dies, flip local polling **back on**. Never delete home collectors as the path to ML2. Code fail-safe default remains local ON when the env is unset. **Live desk (~02:50 HST):** gate flipped — Settings write / `desired=ml2`, drop-in `rr-data-poll.conf` `RR_LOCAL_DATA_POLL=0`, intent `data_poll_mode.yaml` `mode=remote`, poller restarted; verified `live_raw=0` / `live_label=ML2 offload`, `:8799` HTTP 200. No git commit. Schema parity PASS ~02:39 still stands. Current SHAs: desk ML2 `6425c8a`, host `087ee38`, Ecosystem `00985524`, Library `2fc7a47`.

**Near-term** (now live): collectors (geology + weather_us_states), stream (verified), and API/analytics are live with Pacific local data-poll gated **off** (`RR_LOCAL_DATA_POLL=0`) while ML2 is healthy. Pacific remains the **sole long-term bank**. EcoFlow/energy, LAN globe, voice, local devices, tunnel, and durable Database stay Pacific-owned.

**GTK Automations UI (desk, landed ~02:32; live flip ~02:50 HST):** Root Monitor Automations Local Pacific vs ML2 **data-poll** control under Pacific `Apps/Control-Panel/` (`Lib/rr_data_poll.py`). Panel code defaults remain dry-run / desired=local / apply_dropin=false; **current live** after write-mode apply: `desired=ml2`, drop-in applied, intent `mode=remote`, poller restarted and verified. Confirm before write; panel does not auto-restart the poller (human restarted). Operator detail: `Guides & Tutorials/Root-Monitor-Operators-Handbook/Root-Monitor-Operators-Handbook.md` · contract: [Desk-Automations-and-Service-Windows.md](../11-Runtime-Jobs-and-Control/Desk-Automations-and-Service-Windows.md). Do not treat that UI as a cutover that deletes collectors.

**Later** (document now, implement later — not building yet): move/mirror functions into the two mainland desk repos (`US-Mainland-One`, `US-Mainland-Two`) so work can run from those trees locally with no behavioral difference if mainland servers go down — local desk as failover parity.

## Recent ML2 commits

- `819f68e` / `6c66bf1` — Desk (US-Mainland-Two): globe `/api/state` feed from Pacific `local-data-globe` rebroadcast (`hawaii-current.ndjson` → `var/cache/api/state.json`); ops status-current refresh; desk timer `rr-ml2-globe-state-push` every 2m. Ahead of origin; **no push**. Host rsync path unchanged this note.

- `484abe1` — Desk (US-Mainland-Two): analytics + bank path; geology + weather_us_states; stream verified. Host deployed as `559f90e` via rsync (no push). Ecosystem context `bfa9ff2f`.
- `84c4a37` — Desk: earlier test-mode geology collectors + `:8091` API enable path (superseded live state above; host was `3274fb3`).
- `7065795` — **Stage ML2 system monitor + extend stream allowlist for metrics**: collect/send/purge scaffold, `enabled: false` stream config, and staged `ml2-sysmon` units.
- `737b583` — **Stage ML2 data collectors and SSH home-DB stream scaffold**: collectors, stream client/receiver, toggle example, inventory, and staged units.
- `abd4bd0` — **ML2 ephemeral handoff + purge (ML1 mirror); EcoFlow excluded**: raw/handoff purge, API-local overwrite cache, deny-list, and policy docs.
- `04142d5` — **Remove failed YouTube station experiment**: the desk wipe commit.

## YouTube experiment — ended 2026-10-02

Decision: the YouTube / rr-streaming station on ML2 is **scrapped**. Alexander owns any future process himself. ML2 is no longer a YouTube station. Geology + US-states weather collectors, local API/analytics, and Pacific DB stream are live; sysmon remains staged/off.

YouTube paths are gone: `youtube/`, `station/`, the experiment config and `requirements.txt`, `rr-youtube-station.service`, `/etc/rootrecord` YouTube env/oauth, `youtube-venv`, `chromium-profile`, and `/var/lib/rootrecord`. Disk recovery at ~02:10 also purged leftover YouTube-related packages (chromium/gnome/mesa/cups) after apt/snap cache clean.

Backup (mode 600), desk Downloads:

- `/home/rootrecord/Downloads/ml2-youtube-backup-20261002.tar.gz` (31M)
- stamped twin `…-20261002-002841` (same bytes)

Contents covered host secrets, unit file, full checkout, youtube-venv, chromium-profile, `/var/lib/rootrecord`, desk tree copy, and Downloads `client_secret_*.json` (those leftovers were removed from Downloads after the backup).

Local commits (authorized; **not pushed** from the wipe seat): desk `04142d5`, host `6c5070d`, message “Remove failed YouTube station experiment”. Two different remotes — desk automation covers the desk repo; the host remote updates only if that checkout’s publish path runs.

## What stays elsewhere

Mainland One is radio only ([US-Mainland-One](./US-Mainland-One.md), [2026-10-01 radio station](../01-Operations/2026-10-01-radio-station.md)). `www` stays on Vercel. Pacific keeps the poller and the durable Database. Do not restore the YouTube tree from the backup onto the live host without a new Alexander ask.
