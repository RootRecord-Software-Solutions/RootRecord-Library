# US-Mainland-Two

Current as of 2026-10-02 ~02:10 HST. This page is the live host role. The 2026-10-01 SSH and rename sitting is [2026-10-01 mainland rename and SSH tunnels](../01-Operations/2026-10-01-mainland-rename-and-ssh-tunnels.md). Do not treat OLD FILES or continuity plans as live ML1/ML2 truth.

| Field | Value |
| --- | --- |
| **Role** | Tunnel + GitHub-ops scaffolding, with **test-mode** geology collectors and local API live. Stream and sysmon remain staged/off. **Not** a YouTube station. |
| **GitHub** | `RootRecord-Software-Solutions/US-Mainland-Two` |
| **Desk folder** | `1 - Servers/3 - RootRecord-US-Mainland-Two` (own `.git`; umbrella gitignores it) |
| **Host checkout** | `/home/ubuntu/US-Mainland-Server-2` |
| **Host** | `ip-172-31-15-254`, public `3.149.238.83` |
| **SSH** | `ssh ml2` → `ml2.rootrecord.cloud`. Direct fallback `ml2-ip` |
| **Tunnel** | `bd8e68a4-8a97-4b20-afd9-b058473a0a22`. Routes include `ml2.rootrecord.cloud` (SSH). `api.rootrecord.cloud` → ML2 `:8091` is live (`/health`, `/api/operations`, `/api/state` → 200). |
| **Desk branch** | `main`, local `84c4a37` (US-Mainland-Two) |
| **Host SHA** | `3274fb3` (US-Mainland-Server-2; rsync deploy; no push) |
| **Test-mode toggle** | Host `docs/TOGGLE.md` test-mode § |

## Live host check (2026-10-02 ~02:10 HST) — supersedes ~01:58

Alexander test-mode enable on ML2 after the earlier disk-risk check. Disk `/` recovered **96% → ~66%** (~**2.3G free**) via apt clean, snap cache clear, and purge of YouTube leftovers (chromium/gnome/mesa/cups). Enabled **`ml2-api.service`** (`:8091`), **`ml2-collectors.timer`** (geology every 5m, **ok=6/6**), and **`ml2-purge.timer`** (hourly). **`ml2-db-stream`** and **sysmon** remain staged only (not installed). cloudflared `api.rootrecord.cloud` `/health`, `/api/operations`, `/api/state` → **200**; prior connection-refused to `:8091` cleared. Pacific **`RR_LOCAL_DATA_POLL` untouched** (parallel test). `config/stream.yaml` still **`enabled: false`**.

### Stream blockers (Pacific path still off)

- Missing `~/.ssh/ml2-db-stream` on the stream path.
- Pacific-db SSH/Access and Pacific `home_receiver` + forced-command key still needed.
- Handoffs purge hourly until the stream acks.
- `/api/operations` needs a Pacific→ML2 refresh or desk re-seed for current ops content.

## What is in the tree

The desk tree and host checkout now run a partial live path under test-mode:

- `collectors/` — geology, Kīlauea camera, weather (Hawaiʻi, US states, country locations, hurricanes), and radio-RSS scaffold modules plus the runner. `config/collectors.yaml` currently enables only `geology`; the other internet-facing collectors are staged for review. **Geology collectors are live** via `ml2-collectors.timer` (every 5m; last check ok=6/6).
- `stream/` — clean SSH NDJSON client/protocol and the staged `home_receiver.py` for the Pacific Database. **Not installed / not streaming.**
- `api_local/` — local API status-cache sync; it overwrites `var/cache/api/` and does not stream API-circulated metrics home. **`ml2-api.service` is enabled** on `:8091`.
- `config/` — collector, purge, toggle-example, stream, and deny-list policy. `config/stream.yaml` is present but remains `enabled: false`. Operator toggle: host `docs/TOGGLE.md` test-mode §.
- `scripts/` — `run-collectors.sh`, `run-stream.sh`, `ml2-purge.sh`, `run-api-local-sync.sh`, and the kept `aws-git-pull.sh`.
- `systemd/` — **`ml2-api`**, **`ml2-collectors`**, and **`ml2-purge`** are installed/enabled on the host for this test. **`ml2-db-stream`** and **`ml2-sysmon`** remain staged files only. The `aws-git-pull` scaffolding remains kept and its timer is not installed on the host.

The network-globe module is intentionally a refusal: LAN capture stays Pacific-local. The existing cloudflared tunnel now serves the live API on `:8091`.

## 2026-10-02 staged system monitor (not installed)

Commit `7065795` stages ML2 collect → send → self-purge alongside the existing collector and ephemeral-handoff policy; it is not installed on the live host. `system-monitor/` sends primary SSH NDJSON to the Pacific `System/scripts/rr_db_stream_receive.py` and purges the local handoff after receiver acknowledgement. `config/sysmon-stream.yaml` remains `enabled: false`; `systemd/ml2-sysmon.{service,timer}` are staged files only. If SSH fails or remains disabled, `telegram_datapack.py` sends a zip through the separate datapack bot, then purges after `sendDocument` acceptance; Pacific `datapack-pickup.py` drains it into Database. The verified Database scaffold is commit `65dea848`, reserving `System/metrics/ml2/`, `Intake/ml2/`, `Logs/ML2/sysmon/`, and `Network/datapacks/{inbox,processed,state}/`. Geology collectors + API + purge are live in test-mode; **stream and sysmon remain staged/off**. YouTube remains wiped; EcoFlow/Energy stays denied and Pacific-only. Operator detail lives in Pacific `System/docs/MAINLAND-SYSMON-INTAKE.md`.

## Ephemeral handoff policy — locked

Pacific is the **only long-term data bank**. ML2 never accumulates a retention archive: `var/raw/` is processed into a handoff, raw is deleted when the handoff is written, and `var/handoff/` is streamed as clean SSH NDJSON and deleted after a successful receiver acknowledgement. With stream still off, the hourly **`ml2-purge`** (now installed) clears leftovers until stream acks exist. API-circulated status and home metrics are overwritten locally under `var/cache/api/` and are not streamed.

EcoFlow and all energy data are Pacific-only. ML2 collectors must not collect or stage `Energy/`; `config/stream_deny.yaml` rejects `Energy/`, `RootRecord/`, status snapshots, the `energy`/`ecoflow` domains, and the `api_mirror` cache domain. Smart devices, security cameras, and Pacific LAN globe capture likewise stay on Pacific.

## Pacific kill-switch — design only

The Pacific stack is not replaced. The proposed `RR_LOCAL_DATA_POLL=0` flag, or `Automations/config/data_poll_mode.yaml` with `mode: remote`, would turn off the selected Pacific internet-data poll jobs so ML2 could collect and stream their processed handoffs. **`RR_LOCAL_DATA_POLL` remains untouched** for this parallel ML2 test. Pacific would continue to own EcoFlow/energy, LAN globe, voice, local devices, tunnel, and the durable Database. Receiver/key setup, dry run, stream enable, and sign-off remain prerequisites (see Stream blockers above).

## Recent ML2 commits

- `84c4a37` — Desk (US-Mainland-Two): test-mode geology collectors + `:8091` API enable path; stream still off. Host deployed as `3274fb3` via rsync (no push).
- `7065795` — **Stage ML2 system monitor + extend stream allowlist for metrics**: collect/send/purge scaffold, `enabled: false` stream config, and staged `ml2-sysmon` units.
- `737b583` — **Stage ML2 data collectors and SSH home-DB stream scaffold**: collectors, stream client/receiver, toggle example, inventory, and staged units.
- `abd4bd0` — **ML2 ephemeral handoff + purge (ML1 mirror); EcoFlow excluded**: raw/handoff purge, API-local overwrite cache, deny-list, and policy docs.
- `04142d5` — **Remove failed YouTube station experiment**: the desk wipe commit.

## YouTube experiment — ended 2026-10-02

Decision: the YouTube / rr-streaming station on ML2 is **scrapped**. Alexander owns any future process himself. ML2 is no longer a YouTube station. Geology collectors + local API are live under test-mode; the Pacific stream cutover remains blocked (keys/receiver).

YouTube paths are gone: `youtube/`, `station/`, the experiment config and `requirements.txt`, `rr-youtube-station.service`, `/etc/rootrecord` YouTube env/oauth, `youtube-venv`, `chromium-profile`, and `/var/lib/rootrecord`. Disk recovery at ~02:10 also purged leftover YouTube-related packages (chromium/gnome/mesa/cups) after apt/snap cache clean.

Backup (mode 600), desk Downloads:

- `/home/rootrecord/Downloads/ml2-youtube-backup-20261002.tar.gz` (31M)
- stamped twin `…-20261002-002841` (same bytes)

Contents covered host secrets, unit file, full checkout, youtube-venv, chromium-profile, `/var/lib/rootrecord`, desk tree copy, and Downloads `client_secret_*.json` (those leftovers were removed from Downloads after the backup).

Local commits (authorized; **not pushed** from the wipe seat): desk `04142d5`, host `6c5070d`, message “Remove failed YouTube station experiment”. Two different remotes — desk automation covers the desk repo; the host remote updates only if that checkout’s publish path runs.

## What stays elsewhere

Mainland One is radio only ([US-Mainland-One](./US-Mainland-One.md), [2026-10-01 radio station](../01-Operations/2026-10-01-radio-station.md)). `www` stays on Vercel. Pacific keeps the poller and the durable Database. Do not restore the YouTube tree from the backup onto the live host without a new Alexander ask.
