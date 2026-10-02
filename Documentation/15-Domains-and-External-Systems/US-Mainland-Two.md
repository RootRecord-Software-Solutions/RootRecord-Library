# US-Mainland-Two

Current as of 2026-10-02 ~01:20 HST. This page is the live host role. The 2026-10-01 SSH and rename sitting is [2026-10-01 mainland rename and SSH tunnels](../01-Operations/2026-10-01-mainland-rename-and-ssh-tunnels.md). Do not treat OLD FILES or continuity plans as live ML1/ML2 truth.

| Field | Value |
| --- | --- |
| **Role** | Tunnel + GitHub-ops scaffolding, with staged ephemeral collectors and SSH handoff scaffold. **Not** a YouTube station. Collector, stream, and purge units are not live. |
| **GitHub** | `RootRecord-Software-Solutions/US-Mainland-Two` |
| **Desk folder** | `1 - Servers/3 - RootRecord-US-Mainland-Two` (own `.git`; umbrella gitignores it) |
| **Host checkout** | `/home/ubuntu/US-Mainland-Server-2` |
| **Host** | `ip-172-31-15-254`, public `3.149.238.83` |
| **SSH** | `ssh ml2` → `ml2.rootrecord.cloud`. Direct fallback `ml2-ip` |
| **Tunnel** | `bd8e68a4-8a97-4b20-afd9-b058473a0a22`. Routes include `ml2.rootrecord.cloud` (SSH). `api.rootrecord.cloud` → ML2 `:8091` is **route only** (no API process). |
| **Desk branch** | `main`, local `abd4bd0`; three commits ahead of `origin/main` at this check |

## What is in the tree

The desk has a staged, not-live data path:

- `collectors/` — geology, Kīlauea camera, weather (Hawaiʻi, US states, country locations, hurricanes), and radio-RSS scaffold modules plus the runner. `config/collectors.yaml` currently enables only `geology`; the other internet-facing collectors are staged for review.
- `stream/` — clean SSH NDJSON client/protocol and the staged `home_receiver.py` for the Pacific Database.
- `api_local/` — local API status-cache sync; it overwrites `var/cache/api/` and does not stream API-circulated metrics home.
- `config/` — collector, purge, toggle-example, stream, and deny-list policy. `config/stream.yaml` is present but remains `enabled: false`.
- `scripts/` — `run-collectors.sh`, `run-stream.sh`, `ml2-purge.sh`, `run-api-local-sync.sh`, and the kept `aws-git-pull.sh`.
- `systemd/` — `ml2-collectors`, `ml2-db-stream`, and `ml2-purge` units are staged files, not installed by this work; the `aws-git-pull` scaffolding remains kept and its timer is not installed on the host.

The network-globe module is intentionally a refusal: LAN capture stays Pacific-local. The existing cloudflared tunnel and API route-only facts remain unchanged.

## Ephemeral handoff policy — locked

Pacific is the **only long-term data bank**. ML2 never accumulates a retention archive: `var/raw/` is processed into a handoff, raw is deleted when the handoff is written, and `var/handoff/` is streamed as clean SSH NDJSON and deleted after a successful receiver acknowledgement. The staged hourly `ml2-purge` mirrors the ML1 truncate-style purge for leftovers, temporary files, and rotated logs; it is not installed. API-circulated status and home metrics are overwritten locally under `var/cache/api/` and are not streamed.

EcoFlow and all energy data are Pacific-only. ML2 collectors must not collect or stage `Energy/`; `config/stream_deny.yaml` rejects `Energy/`, `RootRecord/`, status snapshots, the `energy`/`ecoflow` domains, and the `api_mirror` cache domain. Smart devices, security cameras, and Pacific LAN globe capture likewise stay on Pacific.

## Pacific kill-switch — design only

The Pacific stack is not replaced. The proposed `RR_LOCAL_DATA_POLL=0` flag, or `Automations/config/data_poll_mode.yaml` with `mode: remote`, would turn off the selected Pacific internet-data poll jobs so ML2 could collect and stream their processed handoffs. Pacific would continue to own EcoFlow/energy, LAN globe, voice, local devices, tunnel, and the durable Database. No Pacific kill-switch edit or cutover was made from this ML2 documentation seat; receiver/key setup, dry run, timer installation, and sign-off remain prerequisites.

## Recent ML2 commits

- `737b583` — **Stage ML2 data collectors and SSH home-DB stream scaffold**: collectors, stream client/receiver, toggle example, inventory, and staged units.
- `abd4bd0` — **ML2 ephemeral handoff + purge (ML1 mirror); EcoFlow excluded**: raw/handoff purge, API-local overwrite cache, deny-list, and policy docs.
- `04142d5` — **Remove failed YouTube station experiment**: the desk wipe commit; the local desk branch is three commits ahead of `origin/main` at this check.

## YouTube experiment — ended 2026-10-02

Decision: the YouTube / rr-streaming station on ML2 is **scrapped**. Alexander owns any future process himself. ML2 is no longer a YouTube station. Polling-on-ML2 is staged as a later, docs-only cutover, not live.

YouTube paths are gone: `youtube/`, `station/`, the experiment config and `requirements.txt`, `rr-youtube-station.service`, `/etc/rootrecord` YouTube env/oauth, `youtube-venv`, `chromium-profile`, and `/var/lib/rootrecord`.

Backup (mode 600), desk Downloads:

- `/home/rootrecord/Downloads/ml2-youtube-backup-20261002.tar.gz` (31M)
- stamped twin `…-20261002-002841` (same bytes)

Contents covered host secrets, unit file, full checkout, youtube-venv, chromium-profile, `/var/lib/rootrecord`, desk tree copy, and Downloads `client_secret_*.json` (those leftovers were removed from Downloads after the backup).

Local commits (authorized; **not pushed** from the wipe seat): desk `04142d5`, host `6c5070d`, message “Remove failed YouTube station experiment”. Two different remotes — desk automation covers the desk repo; the host remote updates only if that checkout’s publish path runs.

## What stays elsewhere

Mainland One is radio only ([US-Mainland-One](./US-Mainland-One.md), [2026-10-01 radio station](../01-Operations/2026-10-01-radio-station.md)). `www` stays on Vercel. Pacific keeps the poller and the durable Database. Do not restore the YouTube tree from the backup onto the live host without a new Alexander ask.
