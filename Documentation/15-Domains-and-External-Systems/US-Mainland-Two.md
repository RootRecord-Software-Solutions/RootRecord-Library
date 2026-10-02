# US-Mainland-Two

Current as of 2026-10-02 ~02:32 HST. This page is the live host role. The 2026-10-01 SSH and rename sitting is [2026-10-01 mainland rename and SSH tunnels](../01-Operations/2026-10-01-mainland-rename-and-ssh-tunnels.md). Do not treat OLD FILES or continuity plans as live ML1/ML2 truth.

| Field | Value |
| --- | --- |
| **Role** | Tunnel + GitHub-ops scaffolding, with geology + US-states weather collectors, local API + analytics, and verified Pacific DB stream. **Not** a YouTube station. |
| **GitHub** | `RootRecord-Software-Solutions/US-Mainland-Two` |
| **Desk folder** | `1 - Servers/3 - RootRecord-US-Mainland-Two` (own `.git`; umbrella gitignores it) |
| **Host checkout** | `/home/ubuntu/US-Mainland-Server-2` |
| **Host** | `ip-172-31-15-254`, public `3.149.238.83` |
| **SSH** | `ssh ml2` → `ml2.rootrecord.cloud`. Direct fallback `ml2-ip` |
| **Tunnel** | `bd8e68a4-8a97-4b20-afd9-b058473a0a22`. Routes include `ml2.rootrecord.cloud` (SSH). `api.rootrecord.cloud` → ML2 `:8091` is live (`/health`, `/api/operations`, `/api/state`, analytics). |
| **Desk branch** | `main`, local `484abe1` (US-Mainland-Two) |
| **Host SHA** | `559f90e` (US-Mainland-Server-2; rsync deploy; no push) |
| **Ecosystem SHA** | `bfa9ff2f` (desk umbrella; context only) |
| **Test-mode toggle** | Host `docs/TOGGLE.md` test-mode § (Library does not edit that file) |

## Live host check (2026-10-02 ~02:29 HST) — supersedes ~02:10 / ~02:26

Mainland landed ML2 analytics + bank path. Desk ML2 `484abe1`, host `559f90e`, Ecosystem `bfa9ff2f`.

- **API + analytics:** `ANALYTICS.md` in the ML2 tree; endpoints `/api/analytics/daily`, `/api/analytics/period`, `/api/analytics/current` on `:8091`. Desk sink: Pacific Database `Logs/Website/analytics/`.
- **Stream verified:** 7 handoffs reached Pacific `Geology/` + `Weather/US-States/`. `ml2-db-stream` runs via desk tunnel `rr-ml2-db-tunnel` on `:17022` (not the earlier “stream still off” state).
- **Collectors on:** `geology` and `weather_us_states` (other internet-facing collectors remain staged for review).
- **Pacific gate:** `RR_LOCAL_DATA_POLL` lives in Pacific `automation_control.py`; default local **ON**; **not flipped** this sitting. Desk Root Monitor Automations now exposes the GTK data-poll toggle (dry-run default); restart Root Monitor to load it.
- **Toggle plan:** toggle-not-replacement + later local-mirror plan already filed (~02:26); SHAs and live stream/analytics state attached here; GTK UI filed ~02:32.

Disk recovery and API enable from ~02:10 remain in force (`ml2-api`, `ml2-collectors`, `ml2-purge` installed). Sysmon remains staged/off.

### Stream path (now working)

- Desk `rr-ml2-db-tunnel` → `:17022` carries `ml2-db-stream` NDJSON home.
- Verified landings: Pacific Geology + Weather/US-States (7 handoffs this check).
- Earlier blockers (missing stream key / receiver / forced-command) are cleared for this verified path; keep purge as safety until acks stay healthy.

## What is in the tree

The desk tree and host checkout run a live path under the toggle plan:

- `collectors/` — geology, Kīlauea camera, weather (Hawaiʻi, US states, country locations, hurricanes), and radio-RSS scaffold modules plus the runner. **Live now:** `geology` and `weather_us_states` via `ml2-collectors.timer`. Other internet-facing collectors stay staged for review.
- `stream/` — clean SSH NDJSON client/protocol and `home_receiver.py` for the Pacific Database. **`ml2-db-stream` verified** through desk `rr-ml2-db-tunnel` `:17022`.
- `api_local/` — local API status-cache sync; it overwrites `var/cache/api/` and does not stream API-circulated metrics home. **`ml2-api.service` is enabled** on `:8091`, including analytics routes.
- Analytics — `ANALYTICS.md`; `/api/analytics/daily|period|current`; aggregates land under desk `Logs/Website/analytics/`.
- `config/` — collector, purge, toggle-example, stream, and deny-list policy. Operator toggle: host `docs/TOGGLE.md` test-mode §.
- `scripts/` — `run-collectors.sh`, `run-stream.sh`, `ml2-purge.sh`, `run-api-local-sync.sh`, and the kept `aws-git-pull.sh`.
- `systemd/` — **`ml2-api`**, **`ml2-collectors`**, **`ml2-purge`**, and **`ml2-db-stream`** are in the live path for this sitting. **`ml2-sysmon`** remains staged files only. The `aws-git-pull` scaffolding remains kept and its timer is not installed on the host.

The network-globe module is intentionally a refusal: LAN capture stays Pacific-local. The existing cloudflared tunnel serves the live API on `:8091`.

## 2026-10-02 staged system monitor (not installed)

Commit `7065795` stages ML2 collect → send → self-purge alongside the existing collector and ephemeral-handoff policy; it is not installed on the live host. `system-monitor/` sends primary SSH NDJSON to the Pacific `System/scripts/rr_db_stream_receive.py` and purges the local handoff after receiver acknowledgement. `config/sysmon-stream.yaml` remains `enabled: false`; `systemd/ml2-sysmon.{service,timer}` are staged files only. If SSH fails or remains disabled, `telegram_datapack.py` sends a zip through the separate datapack bot, then purges after `sendDocument` acceptance; Pacific `datapack-pickup.py` drains it into Database. The verified Database scaffold is commit `65dea848`, reserving `System/metrics/ml2/`, `Intake/ml2/`, `Logs/ML2/sysmon/`, and `Network/datapacks/{inbox,processed,state}/`. Geology + US-states weather collectors, API/analytics, purge, and DB stream are live; **sysmon remains staged/off**. YouTube remains wiped; EcoFlow/Energy stays denied and Pacific-only. Operator detail lives in Pacific `System/docs/MAINLAND-SYSMON-INTAKE.md`.

## Ephemeral handoff policy — locked

Pacific is the **only long-term data bank**. ML2 never accumulates a retention archive: `var/raw/` is processed into a handoff, raw is deleted when the handoff is written, and `var/handoff/` is streamed as clean SSH NDJSON and deleted after a successful receiver acknowledgement. Hourly **`ml2-purge`** remains as safety for leftovers without acks. API-circulated status and home metrics are overwritten locally under `var/cache/api/` and are not streamed.

EcoFlow and all energy data are Pacific-only. ML2 collectors must not collect or stage `Energy/`; `config/stream_deny.yaml` rejects `Energy/`, `RootRecord/`, status snapshots, the `energy`/`ecoflow` domains, and the `api_mirror` cache domain. Smart devices, security cameras, and Pacific LAN globe capture likewise stay on Pacific.

## Pacific data-poll toggle — not a replacement

Alexander (2026-10-02 ~02:26 HST; SHAs attached ~02:29): this is a **toggle**, not a cutover that deletes home collectors. Pacific/home data polling **stays installed**. `RR_LOCAL_DATA_POLL` in Pacific `automation_control.py` (host `docs/TOGGLE.md` test-mode §) turns local polling **off** while ML2 is healthy; if AWS/ML2 dies, flip local polling **back on**. Never delete home collectors as the path to ML2. **Default remains local ON; gate was not flipped** this sitting.

**Near-term** (Mainland bringing ML2 online): collectors (geology + weather_us_states), stream (verified), and API/analytics are live with that toggle still at default ON. Pacific remains the **sole long-term bank**. EcoFlow/energy, LAN globe, voice, local devices, tunnel, and durable Database stay Pacific-owned.

**GTK Automations UI (desk, 2026-10-02 ~02:32 HST):** Root Monitor Automations now has a Local Pacific vs ML2 **data-poll** control under Pacific `Apps/Control-Panel/` (`Lib/rr_data_poll.py`; defaults dry-run / desired=local / apply_dropin=false). Confirm before write; no auto poller restart; live collectors not flipped this session. Alexander must restart Root Monitor to see the GTK. Operator detail: [Root-Monitor-Operators-Handbook](../../Guides%20%26%20Tutorials/Root-Monitor-Operators-Handbook/Root-Monitor-Operators-Handbook.md) · contract: [Desk-Automations-and-Service-Windows.md](../11-Runtime-Jobs-and-Control/Desk-Automations-and-Service-Windows.md). Do not treat that UI as a cutover.

**Later** (document now, implement later — not building yet): move/mirror functions into the two mainland desk repos (`US-Mainland-One`, `US-Mainland-Two`) so work can run from those trees locally with no behavioral difference if mainland servers go down — local desk as failover parity.

## Recent ML2 commits

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
