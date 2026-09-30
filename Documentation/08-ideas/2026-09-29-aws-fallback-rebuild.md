# Proposal — AWS as a small fallback node: rebuild plan, per-function toggles, buffer-to-relay catch-up

| Field | Value |
| --- | --- |
| **Date (HST)** | 2026-09-29 (Phase 1: plan + read-only inventory, 14:57–15:20 HST) |
| **Proposed by** | Grok (executor) for Alexander Storey |
| **State** | **Phase 2 LANDED (trimmed-micro profile, 16:03 HST)**: Alexander kept the t3.micro and chose the trimmed 7-function profile at 15:40 HST, and AWS changes are approved. Phase 1 inventory PASS. Root Monitor page in **write mode**. Items still pending sign-off are listed in [Phase 2](#phase-2-trimmed-micro-deployed-2026-09-29-15401625-hst) |
| **Grounding** | [Phase 2 reclaim + retention](../07-testing/2026-09-29-aws-fallback-phase2-reclaim-retention.md) · [Phase 2 history batching](../07-testing/2026-09-29-aws-globe-history-batched-commits.md) · [Phase 2 runtime deploy + Root Monitor write](../07-testing/2026-09-29-aws-fallback-phase2-runtime-deploy.md) · [inventory test record](../07-testing/2026-09-29-aws-fallback-inventory.md) · [Root Monitor page test record](../07-testing/2026-09-29-root-monitor-aws-fallback-page.md) · [US-Mainland-Server](../00-architecture/US-Mainland-Server.md) · [AWS plan](./2026-09-29-aws-mainland-improvement-plan.md) · catalog `Pacific Apps/Control-Panel/Lib/rr_aws_fallback.json` |
| **Needs sign-off from** | Alexander (instance size, each AWS change, desk jobs, Telegram ownership, write mode) |
| **Related WO** | WO-SRV (Servers cutover) |

## Intent (from Alexander, 2026-09-29 14:57 HST)

- The desk (Pacific) is the **main copy**. AWS was reset a few days ago and needs a full rebuild. The repo and AWS drifted because nothing was ever pulled back from AWS.
- AWS is a **simple fallback** that keeps basic operations alive while the desk is offline. It is **not** a full offload.
- Candidates:
  - the smallest polling jobs (communications, basic replies)
  - website telemetry/status
  - the globe, which the Vercel site will use as its background.
- If the desk↔AWS link fails, AWS buffers data packets to the **Data Relay**, so the desk can catch up and ingest them later.
- Each AWS function gets its own toggle in Root Monitor. The frequently useful small ones default to ON.

## Problem (measured, read-only, 2026-09-29 15:00 HST)

| Item | Measured |
| --- | --- |
| Instance | **t3.micro, 2 vCPU, 908 MB RAM** (IMDS instance-type), no swap. **Not 2 GB**: the 2 GB assumption needs a resize to t3.small (sign-off 1) |
| Disk | `/` 6.7 GB, 3.5 GB used, **3.1 GB free**. `/usr` 2.7 GB, `/snap` 0.9 GB, `/var/lib/apt` 152 MB, `/var/cache/apt` 105 MB (reclaimable), journald 24 MB, `/var/log` 33 MB |
| RAM | 463 MB used, **445 MB available** (already below a 512 MB floor). The globe stack is 172 MB of it: web 80–85, feed-server 35–37, cloudflared 29–40, history 28–47. The OS baseline is ~300 MB (fwupd 27, journald 26, snapd 24, networkd-dispatcher 19, unattended-upgrades 17, ssm-agent 15, …) |
| CPU / IO | load ~1.1–1.3 with **28–44 % iowait** and 8–12 MB/s writes. Causes: `connection-history.py` commits SQLite once per record (2,501 CPU-s since 09-26); `github-poller.sh` runs `git fetch` every 1 s (**14,318 CPU-s** in 3.4 days); the legacy 1 s poller spawns 4 failing `bash -lc` per second (701 CPU-s) |
| Services (custom) | `cloudflared-network-globe` · `network-globe-web` (127.0.0.1:8090) · `network-globe-feed-server` (**0.0.0.0:8787, public**, decision pending) · `network-globe-connection-history` · `github-poller` (1 s fetch loop) · `rr-rootserver-poller` (root; jobs point at `/home/ubuntu/system-monitor`, `/home/ubuntu/communications/*`, which **don't exist**) · `ip-notify` (oneshot at boot) · leftover `cloudflared-update.{service,timer}` (disabled) |
| Cron | `ubuntu`: `*/15` `maintain-hawaii-feed.sh` (added today). root: none |
| Ports | 22 (sshd, public), **8787 (public)**, 8090 / 20241 / 53 on localhost only, cloudflared QUIC out |
| Secrets on AWS | `~/.env` (0600) holds 23 keys, including ones AWS doesn't need (EcoFlow login, A-EYES passwords, GitHub token, Cloudflare tokens). Names only were read |
| Drift | `~/US-Mainland-Server` at `b61d63c` has local edits (`network-globe/server.js`) and is pulled every second. `~/network-globe/network-globe/` (live) differs from the repo |

## Proposal

### 1. Candidate functions (the same catalog drives the Root Monitor page)

"RAM" is the peak estimate per function: resident, or the transient peak of a one-shot. "Measured" values come from the AWS or desk process RSS today.

| id | Function | RAM (MB) | Disk cap | Network | Fits | Default |
| --- | --- | --- | --- | --- | --- | --- |
| `tunnel` | Cloudflare tunnel (www + ssh) | 40 res (29–40 measured) | 0 | control plane + globe traffic | yes | **ON (locked)** |
| `globe_ingest` | desk → AWS feed over SSH + 15-min trim cron | 12 res (sshd) | 64 MB | ~40 MB/h in | yes | **ON (locked)** |
| `globe_web` | globe for www / Vercel background | 85 res (80–85) | 1 MB | 40 KB per `/api/state` poll per viewer at 1 s → **reduce to 5 s + gzip** before the Vercel launch | yes | **ON** |
| `globe_history` | daily SQLite + datapack to the Data Relay | 30 res (28–47) | 50 MB | 1 zip/day | yes, after a batching fix | **ON** |
| `globe_feed_8787` | raw NDJSON on public :8787 | 37 res | 0 | 5.5 KB served since 09-26 | yes, but exposed | ON (unchanged, **decision pending**) |
| `desk_watch` | desk online/offline watch → mode | 0 (inside runner) | 1 MB | none | yes | **ON** |
| `status_health` | status JSON for the website `/status` | 20 transient | 1 MB | ~2 KB per request | yes | **ON** |
| `system_monitor` | 60 s sample (replaces the broken 1 s job) | 5 transient | 5 MB | none | yes | **ON** |
| `relay_buffer` | pack spooled records → Data Relay while the desk is offline | 20 transient | 256 MB spool | ≤ 1 MB / 15 min while offline | yes | **ON** |
| `telegram_hold` | quiet inbox hold; owns `getUpdates` **only while the desk is offline** | 16 res while offline (desk council-relay 15.9) | 20 MB | long-poll ~0.2 MB/h | yes | **ON** |
| `basic_replies` | canned replies (status, battery last-known, weather) with no LLM | +5 | 1 MB | sendMessage per reply | yes | OFF (**sign-off**; matches desk `RR_RELAY_REPLIES=0`) |
| `geology_current` | USGS / HVO, 5 min, current-only | 28 transient (desk 28 MB, 2.6 s) | 2 MB | ~1–2 MB/h | yes | **ON** (while offline) |
| `nws_current` | NWS current-only, 10 min | 31 transient (desk 20–31) | 2 MB | ~0.6 MB/h | yes | **ON** (while offline) |
| `public_ip_notify` | public IP change notice | 5 transient | 0 | 1 GET / 15 min | yes | **ON** |
| `hawaii_news` | news / web facts | 31 transient, 12 s | 5 MB | 25 feeds/run | yes, low value (25×404 today) | OFF |
| `github_poller` | legacy `git fetch` every 1 s | 24 res | 0 | 1 fetch/s | **no** (CPU) | OFF → retire |
| `legacy_poller` | legacy 1 s poller with 4 dead jobs | 11 res | 0 | none | **no** | OFF → retire |
| `weather_scheduler` | full Weather scheduler | 420 res | 2.9 GB | — | **NO** | locked OFF |

Not candidates (hardware- or desk-bound): LLM / NPU inference, voice TTS and playback, cameras and timelapse, EcoFlow BLE, Starlink, smart devices. The desk `discord`/`slack` folders are README shells only, so there is nothing to port yet.

**Proposed default-ON list:** `tunnel`, `globe_ingest`, `globe_web`, `globe_history`, `desk_watch`, `status_health`, `system_monitor`, `relay_buffer`, `telegram_hold`, `geology_current`, `nws_current`, `public_ip_notify`. `globe_feed_8787` stays as it is until you decide. Default OFF: `basic_replies` (sign-off), `hawaii_news`, and the two legacy services (retire).

### 2. Budget (floors: ≥ 512 MB RAM free, ≥ 1.5 GB disk free)

| Profile | Total RAM | OS baseline | Default-ON functions (sum of peaks) | Est. free | Floor 512 MB |
| --- | --- | --- | --- | --- | --- |
| **t3.micro now** | 908 | ~300 | 329 | **~279** | **FAIL** |
| t3.micro, OS trimmed (fwupd, ModemManager, udisks2, multipathd off; snapd kept for ssm-agent) | 908 | ~220 | 203 (tunnel, ingest, web, history, desk_watch, telegram_hold, relay_buffer only) | ~485 | borderline FAIL |
| **t3.small (2 GB), recommended** | 2048 | ~300 | 329 | **~1,419** | **PASS** |

Disk (6.7 GB root; target ≤ 4.2 GB used so ≥ 2.5 GB stays free, well above the 1.5 GB floor):

| Item | Cap |
| --- | --- |
| OS + packages + snaps (measured) | ~3.3 GB (`apt clean` −105 MB; `snap set system refresh.retain=2`) |
| `hawaii.ndjson` | 64 MB (cron trim, landed) |
| history SQLite | 50 MB (daily send + delete, existing) |
| spool (relay packets) | **256 MB hard cap**, oldest dropped first and logged |
| current-only data (`*-last.json`) | 10 MB |
| app code (+ node_modules) | 60 MB; deploy backups keep the last 5 (~25 MB) |
| journald | `SystemMaxUse=100M` (24 MB today) |
| `/var/log` + app logs | logrotate daily, 7 kept, compressed, ≤ 50 MB + 35 MB |
| dated `~/rootrecord/bin.bak-*` | pruned after 14 days, except the newest per kind (65 MB today, mostly the feed tail) |
| **Total** | **≈ 4.0 GB used → ≈ 2.7 GB free** |

### 3. Runtime layout on AWS (desk-built, deployed; nothing edited on AWS by hand)

```text
/home/ubuntu/rootrecord/fallback/
  app/                 deployed code (read-only, from the desk; app.prev kept for rollback)
  flags/<id>           "1" | "0", one file per function (written only by Root Monitor / deploy, backed up first)
  budget.json          {"ram_floor_mb":512,"disk_floor_mb":1536}
  state/mode           NORMAL | SUSPECT | FALLBACK   state/desk-heartbeat   state/desk-ack   state/<id>.last
  spool/<source>/      NDJSON segments -> packets (256 MB cap)
  data/current/        *-last.json (current-only mirrors)
  logs/                logrotate 7 x 5 MB
units: rr-fallback-runner.service (ubuntu, stdlib python, ~15 MB, MemoryMax=300M incl. children, Nice=10)
       rr-fallback-apply.path + .service (root): watches flags/ -> start/stop the service-type functions
       existing network-globe-* + cloudflared-network-globe units (unchanged; their flags map to start/stop)
```

- **Runner**: one scheduler reads `flags/` and `state/mode` every cycle. It starts each enabled job as a short-lived `nice -n 10` child with a timeout. A `fallback_only` job runs only in FALLBACK mode.
- **Budget guard**: before each start, the runner checks `MemAvailable − ram_mb ≥ 512` and `disk free ≥ 1.5 GB`. Otherwise it records `BUDGET_SKIP` in `state/<id>.last` and doesn't start the job. The status JSON shows it.
- **Toggles**: writing a flag file is the only control. The path unit applies service-type flags, and the runner reads the rest on its next cycle. No SSH session ever runs `systemctl` itself.

### 4. Offline detection, buffer-to-relay, desk catch-up and dedupe

- **Signals:**
  1. **Desk heartbeat push**: a new desk job (sign-off, `jobs.py` registration only) writes `state/desk-heartbeat` over SSH every 60 s.
  2. **Passive**: the `hawaii.ndjson` mtime. The desk collector streams about 11 KB/s.
  3. Optional: `https://rootserver.rootrecord.cloud/` (the desk tunnel).
- **State machine (`desk_watch`, every 30 s)**:
  - NORMAL → SUSPECT when no signal for 120 s.
  - SUSPECT → FALLBACK when no signal for 300 s.
  - Back to NORMAL only after 3 fresh heartbeats (≥ 3 min of hysteresis).
- **Telegram, one owner**:
  - The desk relay always owns `getUpdates`. `telegram_hold` polls only in FALLBACK and stops within one long-poll (≤ 30 s) of NORMAL. The desk may see `409 Conflict` for ≤ 30 s and already retries.
  - Updates that AWS consumes are acknowledged to Telegram, so AWS spools them in the desk quiet-inbox format (ts, chat id, from, persona target, message_id, text). They then land in `Logs/Communications/Relay-Inbox/`, where `relay-inbox-replay.py` already lists and answers them.
  - No replies unless `basic_replies` is ON.
- **Spool envelope**: `{id, source, observed_at, collected_by:"aws", seq, payload}`.
  - `id = sha256(source + natural key)`, for example a USGS event id + `updated`, an NWS product id + issued time, a Telegram `update_id`, or the minute for status.
  - Segments live at `spool/<source>/<YYYYMMDD-HHMM>-<seq>.ndjson`.
- **`relay_buffer`** (every 15 min while FALLBACK, or while the link fails):
  - Packs closed segments into `rr-aws-YYYYMMDD-HHMM-<seq>.zip` with `manifest.json` (seq range, counts, sha256 per file).
  - Sends it with `sendDocument` to **Root Record Data Relay** (`RR_DATAPACK_CHAT_ID`, the same channel convention as `telegram-relay.js`).
  - Keeps the local copy until the desk acks it.
- **Desk catch-up** (new desk job `aws_catchup`, sign-off; on reconnect and every 10 min):
  1. `rsync` the spool packets from AWS over SSH. This is the primary path.
  2. Verify each manifest sha256.
  3. Ingest through per-source adapters:
     - Geology: dedupe by event id.
     - Weather current: skipped if older than the desk's own copy.
     - Telegram: → Relay-Inbox.
     - Status: → `Logs/Mainland/`.
  4. Record every id in `Database/Logs/Mainland/aws-ingest-ledger.jsonl` (plus a SQLite id set).
  5. Write `state/desk-ack = <max seq>`. AWS then prunes the packets up to that seq.
  - Re-running the ingest must add 0 records (idempotent).
  - If AWS itself was lost, the desk can fetch the same zips from the Data Relay channel. Dedupe is identical.
- **Direction rule**: this is AWS→desk catch-up of data that AWS collected itself. The globe rule "AWS never gets a desk backfill" is unchanged.

### 5. Code push: the desk is canonical, with a one-way deploy and a backup

- Source: a new Mainland checkout folder `fallback/` (runner, jobs, units, `functions.json` = the Root Monitor catalog), plus the already-mirrored `network-globe/` files. The AWS-live `server.js` is kept as `mirror/network-globe/network-globe/server.aws-live-2026-09-29-allowlist.js`.
- `deploy-aws-fallback.sh [--dry-run (default) | --apply] [--only <component>]`:
  1. Preflight: `rr-aws-ip` is reachable, the floors are OK, and a flock is held.
  2. Build a sha256 manifest.
  3. Show the `rsync -n` diff.
  4. `--apply`:
     - Take a dated remote backup `~/rootrecord/bin.bak-fallback-deploy-<HST ts>/` (app, units, crontab, flags).
     - `rsync --checksum` into `app.new/`, then verify the manifest on AWS.
     - Swap atomically `app.new → app`, keeping `app.prev`.
     - Install changed units (sudo on EC2 is approved per change), then `daemon-reload`.
     - Restart only the changed components, then run a health check.
     - **Roll back automatically** to `app.prev` if the check fails.
  5. Log the deploy.
- **AWS stops pulling from GitHub**: retire `github-poller.service` and `rr-rootserver-poller.service` (back up the units; stop and disable). Remove `GITHUB_TOKEN` and the other unused keys from AWS `~/.env`, leaving only the Data Relay sender and the relay bot. The deploy never copies secrets; the secrets file is managed on its own (0600, backup first).
- The Mainland repo gets the result through desk auto-sync (the `mainland` row, still sign-off). AWS never commits.

### 6. Root Monitor page "AWS Fallback" (landed, dry-run)

- `Apps/Control-Panel/rr_aws_page.py` + `Lib/rr_aws_fallback.py` + `Lib/rr_aws_fallback.json`, in the sidebar after SSH.
- Each of the 18 functions is one row: RAM, disk, network, fits, default. There is a switch per toggleable function.
- A budget box compares the enabled set with the floors, for t3.micro, for 2 GB, and against the measured AWS values once read.
- **Status** runs one read-only SSH to `rr-aws-ip`: the flags, MemAvailable, disk free, and whether the runtime is deployed.
- A **toggle** opens a confirm dialog with the exact change and the budget afterwards:
  - `dry-run` (default) writes nothing.
  - `write` (sign-off) runs one SSH call that validates the id → takes a dated backup of `flags/` → does an atomic write of `flags/<id>`. The remote script refuses with exit 3 while the runtime isn't deployed.
- The page is built on visit and released on leave, with no timer. `--check` +4.4 MB when every page is built. No `jobs.py` edit.

## Scope and non-goals

- Out of scope: running LLM, voice, cameras or EcoFlow on AWS, full Weather, any history store on AWS beyond the caps above, and moving the Vercel site (it only uses the globe as a background).
- Phase 1 changed **nothing on AWS**.

## Sign-off steps (in order)

1. **Instance**: resize t3.micro → **t3.small (2 GB)**, or accept the trimmed-micro profile with a lower floor. Do the Elastic IP (plan P0-3) first, because stop/start changes the public IP.
2. **:8787**: bind it to 127.0.0.1, or close it in the security group.
3. **Retire** `github-poller.service` and `rr-rootserver-poller.service` (backup, stop, disable).
4. **Fix** `connection-history.py`: batch commits every 5 s and resume after a trim. This removes the iowait.
5. **Phase 2 deploy**: the fallback dir, flags (default list above), runner + path units, logrotate/journald caps, and `deploy-aws-fallback.sh`.
6. **Desk jobs** (`jobs.py` registration via Pending-Job-Registrations): `aws_heartbeat_push` (60 s) and `aws_catchup`.
7. **Telegram**: which bot `telegram_hold` uses (the council bot, with the one-owner rule enforced by mode). `basic_replies` stays OFF until you sign off separately.
8. **Root Monitor**: set `aws_fallback_mode` to `write`.
9. **Secrets**: minimise AWS `~/.env`.
10. **Globe**: poll every 5 s + gzip `/api/state` before the Vercel background launch.

## How it would be tested (Phase 2)

1. Stop the desk heartbeat for 6 min. Expected: mode goes SUSPECT → FALLBACK; geology and NWS run; packets are spooled and one is sent to the Data Relay.
2. Resume the heartbeat. Expected: NORMAL after 3 min; the desk pulls, verifies and ingests; a second ingest adds 0 records; the ack prunes the spool.
3. Throughout, the budget guard never lets MemAvailable drop below 512 MB (on 2 GB), and `telegram_hold` has stopped polling before the desk relay polls again.

## Open questions

- Resize to t3.small (~+US$7.6/month on-demand), or stay on micro with the trimmed profile?
- Should the `status_health` JSON be public (through the tunnel as `/api/status`), or only reachable through Access?
- Which bot and chat should AWS basic replies use, and what's the canned set?
- Keep `globe_history`'s daily datapack on AWS, or move it to the desk?

## Phase 2: trimmed-micro deployed (2026-09-29 15:40–16:25 HST)

**Decision (Alexander, 15:40 HST):** keep the t3.micro and use the trimmed 7-function profile. AWS changes are approved. Everything was reversible, with a backup first on AWS (`~/rootrecord/bin.bak-fallback-phase2-20260929-154333/`, plus one per deploy and one per flag write) and on the desk (`/home/rootrecord/Database/GITHUB/aws-fallback-phase2.bak-20260929-154400/`).

| Step | Landed | Record |
| --- | --- | --- |
| Reclaim | `github-poller` + `rr-rootserver-poller` **stopped and disabled** (files and units kept). OS trims: ModemManager (masked), fwupd (masked) + `fwupd-refresh.timer`, udisks2 (masked), multipathd (+ socket; no dm maps, root is plain NVMe), networkd-dispatcher (only the chrony on/off hooks), the unattended-upgrades **shutdown helper** (daily `apt-daily-upgrade.timer` security upgrades still run); `apt-get clean` (−105 MB). snapd and ssm-agent kept | [reclaim + retention](../07-testing/2026-09-29-aws-fallback-phase2-reclaim-retention.md) |
| History fix | `connection-history.py`: commit every 5 s, only whole lines, cursor persisted (inode + offset). An in-place trim no longer re-counts the retained window, and a restart no longer re-ingests the feed. Writes went from 43.9 MB/min to 1.6 MB/min | [history batching](../07-testing/2026-09-29-aws-globe-history-batched-commits.md) |
| Runtime | `~/rootrecord/fallback/` from the desk `deploy-aws-fallback.sh` (Mainland checkout `fallback/`): 30 s oneshot tick (0 MB resident), root `rr-fallback-apply` (hard-coded map, path unit + 15-min reconcile), flags, RAM/disk guard (floor **485 MB** / 1536 MB). Rollback was tested three times (see the record) | [runtime deploy](../07-testing/2026-09-29-aws-fallback-phase2-runtime-deploy.md) |
| Retention | journald drop-in `SystemMaxUse=100M`, `SystemKeepFree=1G`, `SystemMaxFileSize=16M`, `MaxRetentionSec=14day`. logrotate `fallback/logs/*.log` 5 MB × 7. Daily tick retention: `bin.bak-*` older than 14 days are deleted, except the newest per kind; releases keep 5. The spool is capped at 256 MB. The feed trim cron is unchanged | reclaim + retention |
| Root Monitor | desk `settings.json` `aws_fallback_mode` = `write`; catalog updated to trimmed-micro (+ `relay_send` row). A `system_monitor` 0 → 1 → 0 round-trip passed, with a dated backup per write | runtime deploy |

**Flags on AWS now.**
- ON: `tunnel` (locked), `globe_ingest` (locked, cron), `globe_web`, `globe_history`, `desk_watch`, `relay_buffer`, and `globe_feed_8787` (unchanged, **unmanaged**, public :8787).
- OFF: `telegram_hold` (the 7th trimmed function, kept OFF as instructed), `relay_send`, `basic_replies`, `status_health`, `system_monitor`, `geology_current`, `nws_current`, `public_ip_notify` (the boot-time `ip-notify.service` is unchanged), `hawaii_news`, `github_poller`, `legacy_poller`, `weather_scheduler`.

**Still pending sign-off (unchanged):**
1. `:8787` feed server (public)
2. `telegram_hold` + `basic_replies` (OFF)
3. `relay_send` (the first real Data Relay send needs one approved test send)
4. AWS `.env` trim (23 keys)
5. The desk jobs `aws_heartbeat_push` + `aws_catchup`: proposed blocks only, in [Pending-Job-Registrations §C](../00-architecture/Pending-Job-Registrations-2026-09-29.md)
6. Globe `/api/state` poll at 5 s + gzip
