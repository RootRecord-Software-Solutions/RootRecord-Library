# US-Mainland-Server (AWS continuity node) — desk import + current state

| Field | Value |
| --- | --- |
| **Date (HST)** | 2026-09-29 13:45–14:05 HST |
| **Author** | Grok (executor, us-mainland-import pass) for Alexander; context from teammate lane **US-MAINLAND-SERVER** (G2 handoff 2026-09-22) |
| **State** | Import **PASS** (clone at `b61d63c`) · layout README + `.env.example` **LANDED** (uncommitted — repo not in auto-sync) · auto-sync **BLOCKED on sign-off** · `rr-aws` SSH **FAIL** (tunnel down on AWS) · direct SSH to current IP **PASS** (read-only) · AWS changes **PROPOSED** |
| **Repo** | `rootrecordsoftwaresolutions/US-Mainland-Server` (PUBLIC, user account — not the org; `main`, HEAD `b61d63c` 2026-09-28 18:40 HST) |
| **Desk checkout** | `/home/rootrecord/RootRecord-Ecosystem/1 - Servers/2 - RootRecord-US-Mainland-Server/` |
| **AWS checkout** | `/home/ubuntu/US-Mainland-Server/` (same HEAD `b61d63c`) |
| **Test record** | [07-testing/2026-09-29-us-mainland-import-and-ssh.md](../07-testing/2026-09-29-us-mainland-import-and-ssh.md) |
| **Plan** | [08-ideas/2026-09-29-aws-mainland-improvement-plan.md](../08-ideas/2026-09-29-aws-mainland-improvement-plan.md) |
| **Backup** | `/home/rootrecord/Database/GITHUB/us-mainland-import.bak-20260929-134629/` |

> **At pause (16:25 HST):** the State row above describes 13:45–14:05. For the current state see [Current AWS state](#current-aws-state-at-pause-2026-09-29-1625-hst).

## What the repo is

"Secondary infrastructure node providing service continuity, synchronization, and recovery … when the Solar Pacific Root Server is unavailable." 112 tracked files (~0.85 MB working tree; GitHub reports 195 KB packed). README banner (2026-09-28): continuity node; the **org** `RootRecord-Software-Solutions` is authority (the repo itself still lives on the `rootrecordsoftwaresolutions` user account; no org copy exists).

| Path | Contents | Where it runs |
| --- | --- | --- |
| `automations/` | `rr-rootserver-poller.service` (**User=root**, `EnvironmentFile=-/home/ubuntu/.env`), `scripts/rootserver_poller.py` (1 s loop), `scripts/jobs.py`: `system_monitor` 1 s, `communications_{telegram,discord,slack}` 1 s, `public_ip_notify` + `github_pull` (`git fetch && merge --ff-only`) every minute, `globe_feed` on boot | AWS (`/home/ubuntu/automations/` copy) |
| `communications/` | Telegram `getUpdates` poll (token from `/home/ubuntu/.env`), Discord/Slack stubs, `.env.example` with destination chat/channel **IDs** | AWS |
| `system-monitor/` | `sys-sample.sh` → `system-current.json` + SQLite rolling averages (1 s … 1 y) | AWS |
| `network-globe/` | Hawaii collector (`collector.js`, `telegram-relay.js`), `maintain-hawaii-feed.sh`, `connection-history.py`, `feed-server.js`, units, `health-check.sh` | collector: desk (Pacific `Communications/network/local-data-globe/` is the live copy); feed + history: AWS |
| `mirror/network-globe/` | AWS globe web server (`server.js`, `index.html`, port 8090), nested duplicate `network-globe/network-globe/` | AWS (`/home/ubuntu/network-globe/network-globe/`) |
| `mirror/.cloudflared/config-globe.yml` | tunnel `[redacted tunnel ID]…` → `www.rootrecord.cloud` → `127.0.0.1:8090` (credentials file gitignored) | AWS |
| `mirror/rootrecord/systemd/` | 13 legacy units: `rr-{audio-recv,chat,cloudflared,dropins,earthquake,hurricane,icecast,noaa,packer,radar,radio,weather,youtube}` | **not running** (bins/venv not in repo) |
| `weather/` | current-only NWS mirror (config/core/fetch/scheduler) | not running |
| `scripts/` | desk helpers `aws-sysmon-pull.sh`, `ssh-datapack-pull.sh` (target old `Database/NETWORK/…`), G2 `jobs.py` template (cwd `~/.ollama/skills/us-mainland-server`), a **tracked** `__pycache__/jobs.cpython-314.pyc` | desk (G2 paths — stale) |
| `references/`, `notes/`, `docs/`, `.github/` | `aws-git-pull.{service,timer}`, `GITHUB-IDENTITY.md` (commit as US-MAINLAND-SERVER), packer notes, 2026-09-22 stopping point, avatar | — |

Env vars used by the code (names only) are in the new root `.env.example`.

## Measured AWS state (one read-only SSH, 13:49 HST)

| Item | Value |
| --- | --- |
| Host | `[redacted internal hostname]`, up 3 d 9 h, load 0.32; RAM 908 MB (514 MB available) — t3.micro class, us-east-2 |
| Public IP | **[redacted public IP]** (from the desk collector's `AWS_HOST` default). `rr-aws-ip` still points at the old **[redacted public IP]** → TCP 22 timeout (no Elastic IP; IP changed on a stop/start) |
| Disk `/` | 6.7 G, 5.1 G used, **1.6 G free (77 %)** |
| Running | `rr-rootserver-poller`, `network-globe-feed-server`, `network-globe-connection-history`, `github-poller` (not in repo). **No cloudflared, no rr-* collectors, no radio** — "basically empty" confirmed |
| Timers | none matching `aws-git-pull` / `rr-*` (the pull is the poller's `github_pull` job) |
| `/home/ubuntu` | `US-Mainland-Server` 7.1 M, `automations`, `network-globe` **1.7 G**, `github-poller.sh`, `ip-notify.sh`, `ip-state.json`, stray `index.html`/`server.js`/`package.json` |
| **Hawaii feed** | `network-globe/network-globe/data/hawaii.ndjson` = **1,815,325,001 B** and growing ≈ 11 KB/s (≈ 39 MB/h, ≈ 0.95 GB/day: 1,809,246,044 B at 13:40:34 → 1,815,325,001 B at 13:49:49 HST). Intended cap 64 MB. The desk collector runs maintenance every 15 min but the AWS script path `…/network-globe/scripts/maintain-hawaii-feed.sh` **does not exist** (exit 127 in desk journal) |
| **Projection** | at this rate `/` fills in roughly **40 h (around 2026-10-01 morning HST)** → ENOSPC for the poller, git pull and globe. **Urgent sign-off item** (fix = deploy the repo's `network-globe/maintain-hawaii-feed.sh` to that path; see plan P0-1) |

## SSH paths

| Alias | Before | After this pass | Result |
| --- | --- | --- | --- |
| `rr-aws` (`ssh.rootrecord.cloud` via Cloudflare Access) | ProxyCommand `~/.local/bin/cloudflared` (missing) | ProxyCommand → Pacific `Communications/network/cloudflare/bin/cloudflared` (quoted; only that path changed; backup in `ssh/config`) | cloudflared now starts; **`websocket: bad handshake`**, exit 255. `https://ssh.rootrecord.cloud` and `https://www.rootrecord.cloud` both return **HTTP 530 / Cloudflare error 1033** = no tunnel connector → cloudflared is not running on AWS. **FAIL (remote side)** |
| `rr-aws-ip` (`[redacted public IP]`) | unchanged | unchanged | TCP 22 timeout — stale IP. **FAIL** |
| `rr-aws-ip` **after 14:06 HST** | [redacted public IP] | `HostName [redacted public IP]`: only that line changed; backup `~/.ssh/config.bak-20260929-140612` | `ssh -o BatchMode=yes -o ConnectTimeout=5 rr-aws-ip uptime` **PASS** |
| `rr-aws` **after 14:12 HST** | 1033 | tunnel [redacted tunnel ID] running on AWS with an `ssh.rootrecord.cloud → ssh://localhost:22` rule | the tunnel works: **PASS** with the AWS host key pinned (`[redacted SSH host-key fingerprint]`). Plain `ssh rr-aws` FAILs with *host key changed*: the desk `known_hosts` line for `ssh.rootrecord.cloud` holds the pre-rebuild key (same as [redacted public IP]). Not edited; waiting on OK |
| `rr-aws-ip` with `-o HostName=[redacted public IP]` | — | (command-line override only; config not changed) | **PASS**, read-only commands only |

## Desk auto-sync coverage

- Auto-sync = Pacific poller job `github_sync_all` (every 5 s) → `Github/scripts/sync-all.sh` → `push-repo-once.sh <id>` for each **enabled** row of `Github/scripts/repos.conf`. No systemd user timer; `~/agent-tools` is unrelated.
- `repos.conf` row today: `mainland 0 inplace /home/rootrecord/.ollama/skills/us-mainland-server rootrecordsoftwaresolutions/US-Mainland-Server origin` → **disabled** and pointing at an **empty G2 folder**. The new checkout is **not covered**; nothing was committed or pushed.
- Exact change needed (sign-off; Pacific `Github/scripts/repos.conf`, tab-separated):

  ```text
  mainland	1	inplace	/home/rootrecord/RootRecord-Ecosystem/1 - Servers/2 - RootRecord-US-Mainland-Server	rootrecordsoftwaresolutions/US-Mainland-Server	origin
  ```

  Effects once enabled: `push-repo-once.sh` rewrites `origin` to `git@github.com:rootrecordsoftwaresolutions/US-Mainland-Server.git` (SSH; desk key already pushes to that account for `skills`), `git add -A` commits the 3 pending files (`README.md` layout section, `.gitignore` bytecode rule, root `.env.example`) as `auto: … desk sync`, pushes, and **AWS fast-forwards them within ~60 s** (docs/ignore only — no runtime effect). `is_runtime_code_tree` is false for this path → **no Pacific stack reload**. Commits will use the desk git identity, not `US-MAINLAND-SERVER` as `references/GITHUB-IDENTITY.md` asks.

**Correction, 2026-09-29 evening:** do not enable that `mainland` row as written. `/home/rootrecord/RootRecord-Ecosystem` is now one git repository. `1 - Servers/2 - RootRecord-US-Mainland-Server` has no `.git` of its own, and nested git directories must not be added back into the umbrella. `mainland` stays disabled. The desk publishes the umbrella through the `ecosystem` row. A separate Mainland checkout, outside this snapshot, is required before that repository can sync on its own again.

## Title-case / G3 layout

Not restructured: AWS pulls this repo every minute and its units/docs reference lowercase paths (`/home/ubuntu/automations`, `mirror/network-globe/network-globe`, `RECOVERY.md`). A rename is only safe together with an AWS path change. Proposed mapping is in the repo README (*Desk checkout layout*) — e.g. `automations/`→`Automations/`, `communications/`→`Communications/`, `system-monitor/`→`System/Monitor/`, `network-globe/`→`Network/Globe-Collector/`, `mirror/network-globe/`→`Network/Globe-Server/`, `mirror/rootrecord/`→`Collectors/Legacy-Units/`. The pre-existing empty desk folder `Communications/` (2026-09-27) is untracked and left in place (future merge target for `communications/`).

## Security observations (no change made)

1. Repo is **PUBLIC** and contains the globe tunnel ID, Telegram chat IDs / Discord channel IDs (`communications/.env.example`), and (desk collector) the AWS IP + key path. Not secrets, but reconnaissance data.
2. AWS `rr-rootserver-poller` runs **as root** and fast-forwards a public repo every minute; anyone with push access effectively schedules code on the host once a deploy step runs it. Prefer the pull as `ubuntu`, branch protection / signed commits.
3. `communications_telegram` calls `getUpdates` every 1 s; if its token is shared with the desk relay bot this causes Telegram 409 conflicts (the G2 notes used two tokens for this reason) — confirm.

*US-Mainland import, 2026-09-29 HST.*

## Change log — 2026-09-29 14:05–14:35 HST (approved AWS changes)

[Test record](../07-testing/2026-09-29-aws-hawaii-trim-and-cloudflared.md) · plan [P0-1 / P0-4](../08-ideas/2026-09-29-aws-mainland-improvement-plan.md). AWS backups: `/home/ubuntu/rootrecord/bin.bak-hawaii-trim-20260929-140641/` and `/home/ubuntu/rootrecord/bin.bak-cloudflared-20260929-141048/`. Desk backups: `~/.ssh/config.bak-20260929-140612` and `/home/rootrecord/Database/GITHUB/aws-hawaii-trim-cloudflared.bak-20260929-141557/`.

| Area | Now on AWS | Mirror in the Mainland checkout (uncommitted) |
| --- | --- | --- |
| Feed trim script | `/home/ubuntu/network-globe/network-globe/scripts/maintain-hawaii-feed.sh` (= repo, sha256 `d9447d84…`) | `network-globe/maintain-hawaii-feed.sh` |
| Auto-trim | `ubuntu` crontab `*/15`, `nice -n 10`, 64 MiB cap / 48 MiB window, syslog tag `maintain-hawaii-feed` | `network-globe/cron/maintain-hawaii-feed.crontab` |
| Feed size | 1.83 GB → 50.3 MB at 14:07:38 HST; free disk 1.5G → 3.2G | — |
| Web origin | `network-globe-web.service` (`server.js`, User=ubuntu, :8090) | `network-globe/network-globe-web.service` |
| Tunnel | cloudflared 2026.9.3 (official .deb), `cloudflared-network-globe.service`, existing tunnel **`network-globe` [redacted tunnel ID]** (no new tunnel), config `~ubuntu/.cloudflared/config-globe.yml` 0600, creds JSON 0600 (copied from the desk's old aws-sync mirror, never printed) | `network-globe/cloudflared-network-globe.service`, `mirror/.cloudflared/config-globe.yml` (+`ssh.rootrecord.cloud` rule) |
| DNS | **No DNS record changed.** `www` was already routed to [redacted tunnel ID], and `rootrecord.cloud` 301 → `www` is unchanged. Vercel is untouched. Other tunnels on the account: `rootserver` [redacted tunnel ID] (its connectors are on the desk; untouched) and `avaivy-local-truth` [redacted tunnel ID] (untouched) | — |
| Result | `https://www.rootrecord.cloud/` 530/1033 → **200**. MemAvailable 446 MB after (512 MB before) | — |

Why the tunnel was down: cloudflared and its unit were purged on AWS on 2026-09-26 at 02:41 HST (`apt remove --purge`, `rm -rf /etc/cloudflared`). Before that it ran only the token tunnel `rootserver`. The globe tunnel's creds had never been placed on this instance, and the globe web server had no unit.

### Change log: 2026-09-29 14:43 HST, globe `server.js` static allowlist

- **Problem:** with the tunnel back up (14:12), AWS `server.js`'s `express.static(__dirname)` made the whole globe folder public on `www`. That included source, scripts, `data/hawaii.ndjson`, the sqlite history, `geo-cache.json` and `node_modules`, and unknown paths returned `index.html` with a 200.
- **Fix:** an explicit allowlist: `/`, `/index.html`, `/overlay/{overlay.js,overlay.css,overlay-config.json}` (from `./overlay/` when present), `/health`, `/api/state`. Everything else returns 404, and the server binds to `127.0.0.1:8090`. AWS sha256 is now `4ba42236…e0e9fc`. Backup: AWS `~/rootrecord/bin.bak-globe-static-allowlist-20260929-144149/`. Mirror: `mirror/network-globe/network-globe/server.aws-live-2026-09-29-allowlist.js` + `AWS-LIVE-SERVER.md` (the repo `server.js` is untouched). [Test record](../07-testing/2026-09-29-aws-globe-static-allowlist.md).
- **Outside access:** there are no per-request logs. The tunnel counted 55 requests in total during the exposure, mostly desk checks. The web socket-write total was 4.6 MB, so there was no full feed download.
- **Open finding:** `network-globe-feed-server` listens on `0.0.0.0:8787` and is **publicly reachable** at the EC2 IP (`/hawaii.ndjson`). It has been up since 09-26 and has served only 5.5 KB. Decide between binding it to localhost and closing it in the security group.


### Change log: 2026-09-29 15:00 HST, fallback rebuild Phase 1 (plan only, **no AWS changes**)

- Alexander's direction: the desk is canonical, and AWS is rebuilt as a **small fallback** (comms hold, status, globe, current-only hazards, buffer-to-Data-Relay while the desk is offline, desk catch-up with dedupe), with per-function toggles in Root Monitor. Plan: [08-ideas AWS fallback rebuild](../08-ideas/2026-09-29-aws-fallback-rebuild.md). Read-only inventory: [test record](../07-testing/2026-09-29-aws-fallback-inventory.md).
- **Correction to the sizing assumption:** the instance is **t3.micro, 908 MB RAM** (not 2 GB). ~445 MB is available now, and the default fallback set would leave ~279 MB, below the 512 MB floor, so a resize to t3.small is proposed (sign-off). `:8787` is still public (unchanged, listed).

### Change log: 2026-09-29 15:45–16:16 HST, fallback Phase 2 (trimmed-micro, approved)

- **Instance kept:** t3.micro (908 MB) with the trimmed profile. Floors: 485 MB RAM and 1.5 GB disk.
- **Disabled, reversible:** `github-poller` and `rr-rootserver-poller` (files and units kept). ModemManager, fwupd and udisks2 masked; multipathd, fwupd-refresh.timer, networkd-dispatcher and the unattended-upgrades shutdown helper disabled.
- **History:** `connection-history.py` batches its commits.
- **New:** `~/rootrecord/fallback/` (tick timer, root `rr-fallback-apply` + path unit, flags, spool), from the desk `fallback/deploy-aws-fallback.sh`; journald and logrotate caps.
- **Result:** MemAvailable ≥ 497 MB, iowait 7.4 % → 0.1 %.
- **Unchanged:** `:8787` is still public. Records: [reclaim](../07-testing/2026-09-29-aws-fallback-phase2-reclaim-retention.md) · [history](../07-testing/2026-09-29-aws-globe-history-batched-commits.md) · [deploy](../07-testing/2026-09-29-aws-fallback-phase2-runtime-deploy.md).

## Current AWS state (at pause, 2026-09-29 16:25 HST)

Rolled up from the change logs above and the Phase 2 records. Measured values are from the 16:13–16:16 HST verify unless noted.

| Item | State |
| --- | --- |
| Instance | t3.micro, **908 MB RAM**, no swap; kept (no resize). Profile: **trimmed-micro** (7 functions) |
| Memory / I/O / disk | MemAvailable min **497 MB** (floor 485), iowait **0.1 %**, disk free **3,278 MB** (floor 1.5 GB): **PASS** |
| Hawaii feed | trimmed and capped (64 MiB cap, `*/15` cron as `ubuntu`); the cron ran at 16:00 and 16:15: **PASS** |
| Tunnel + `www` | cloudflared 2026.9.3 on the existing globe tunnel; `www` `/`, `/health`, `/api/state` **200**: **PASS** |
| Globe web server | static allowlist, bound to localhost :8090: **PASS** |
| Globe overlay | v2 + AWS Ohio node LANDED 16:10 / 16:16; real-browser check **VERIFY PENDING** |
| Connection history | batched commits + persisted cursor: **PASS** |
| `github-poller`, `rr-rootserver-poller` | disabled, files and units kept (reversible): **KEPT** |
| Fallback runtime | `~/rootrecord/fallback/`, release `20260929-160245-5ee01b1e`, rollback proven: **PASS**. A real fallback is **VERIFY PENDING** |
| Root Monitor AWS Fallback page | write mode, alias `rr-aws-ip`; `system_monitor` 0→1→0 round-trip: **PASS** |
| `telegram_hold`, `basic_replies`, `relay_send` | OFF (sign-off); relay send **VERIFY PENDING** |
| Feed server `:8787` | still public: open finding (sign-off) |
| AWS `.env` | 23 keys; trim pending (sign-off) |
| Desk jobs `aws_heartbeat_push`, `aws_catchup` | not registered; `aws_catchup.py` not written (sign-off) |
| SSH | `rr-aws-ip` **PASS**; `rr-aws` PASS with the pinned host key, FAIL with the stale desk `known_hosts` (sign-off) |
| Mainland checkout | uncommitted; the `mainland` auto-sync row is disabled (sign-off) |

Sign-offs: worklog section "State at pause, 16:25 HST".
