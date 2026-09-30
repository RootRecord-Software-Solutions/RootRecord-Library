# Test record — AWS Mainland: Hawaii feed trim + auto-trim cron, and the www.rootrecord.cloud tunnel restored

| Field | Value |
| --- | --- |
| **Date / time (HST)** | 2026-09-29 14:05–14:35 HST |
| **Tester** | Grok (executor) for Alexander Storey |
| **Change under test** | AWS plan [P0-1](../08-ideas/2026-09-29-aws-mainland-improvement-plan.md) (deploy + run `maintain-hawaii-feed.sh`, plus auto-trim on AWS) and P0-4 (cloudflared on AWS). Also the desk `~/.ssh/config` `rr-aws-ip` HostName. WO-SRV |
| **State** | **PASS** (trim, auto-trim, www tunnel, direct SSH) · `rr-aws` via tunnel **PASS with a verified key** / desk `known_hosts` stale (see open items) |
| **Evidence** | AWS `~/rootrecord/bin.bak-hawaii-trim-20260929-140641/first-run.log`; `journalctl -t maintain-hawaii-feed`; `journalctl -u cloudflared-network-globe` |
| **Commits** | Library: desk auto-sync (see the worklog). Mainland: **none**. The files are uncommitted in the checkout because `mainland` isn't in auto-sync yet |
| **Backup** | AWS `/home/ubuntu/rootrecord/bin.bak-hawaii-trim-20260929-140641/` and `/home/ubuntu/rootrecord/bin.bak-cloudflared-20260929-141048/`. Desk `/home/rootrecord/Database/GITHUB/aws-hawaii-trim-cloudflared.bak-20260929-141557/` and `~/.ssh/config.bak-20260929-140612` |

## What was tested

1. `hawaii.ndjson` (1.83 GB, about 40 MB/h) is trimmed back to the 48 MiB window by the repo script, at the path the desk collector calls (`/home/ubuntu/network-globe/network-globe/scripts/maintain-hawaii-feed.sh`, from `collector.js` `AWS_FEED_MAINTENANCE_SCRIPT`). Before this, the desk calls failed with exit 127 at 13:40 and 13:55.
2. Trimming now happens automatically on AWS itself (`ubuntu` crontab, `*/15`), so it doesn't depend on the desk.
3. `www.rootrecord.cloud` stops returning Cloudflare 1033/530.
4. `rr-aws-ip` points at the current IP.

## Safety review of the script (before running)

- It uses `flock -n` on `/tmp/rootrecord-hawaii-feed-maintenance.lock`, so the desk call and the cron call can't overlap. It does nothing when the file is ≤ 64 MiB.
- It runs `tail -c 48MiB | sed 1d` into a temp file (dropping the first partial record), then rewrites the file in place with `cat tmp > feed`. This is **truncate-in-place on the same inode, not a rename**. The live writer (desk `cat >>`, pid 222029, O_APPEND) keeps appending to the same file with no sparse gap. The inode stayed at 291042 before and after.
- Accepted caveat: during the sub-second rewrite, appended records can be lost, or one partial line can be left. `connection-history.py` and `server.js` `try/except` bad lines. Both reset their offset when `size < offset` and re-read the retained window, so the daily SQLite counters get one re-ingest of ≤ 48 MiB per trim. `hawaii-offset.json` didn't exist; the script created it with `{"offset":0}`. Nothing on AWS reads that file.

## How (exact commands / procedure)

```bash
# desk ~/.ssh/config: only rr-aws-ip HostName [redacted public IP] -> [redacted public IP] (backup config.bak-20260929-140612)
ssh -o BatchMode=yes -o ConnectTimeout=5 rr-aws-ip uptime
# AWS backup: existing maintain-hawaii-feed.sh (repo copy in network-globe/ root), feed/history units,
# crontab (none), timers, stat/df, last 64 MiB of hawaii.ndjson
scp .../network-globe/maintain-hawaii-feed.sh rr-aws-ip:/home/ubuntu/network-globe/network-globe/scripts/
ssh rr-aws-ip 'chmod +x …/scripts/maintain-hawaii-feed.sh && bash -n …/scripts/maintain-hawaii-feed.sh'
ssh rr-aws-ip 'nice -n 10 bash …/scripts/maintain-hawaii-feed.sh 67108864 50331648'   # via nohup, log in backup dir
ssh rr-aws-ip crontab -    # line = Mainland network-globe/cron/maintain-hawaii-feed.crontab
# cloudflared: official .deb 2026.9.3; tunnel [redacted tunnel ID] creds JSON from desk (old aws-sync mirror, sha prefix f62c19ac) -> ~ubuntu/.cloudflared/ 0600
# units network-globe-web.service (server.js :8090) + cloudflared-network-globe.service (--no-autoupdate, User=ubuntu)
curl -sI https://www.rootrecord.cloud/
```

## Pass criteria (written before running)

1. `bash -n` OK, and the script exits 0 with the file ≤ 64 MiB after the run.
2. Free disk space goes up by about 1.7 GB.
3. `network-globe-feed-server` and `network-globe-connection-history` are still active, and the writer keeps appending.
4. The crontab is installed, and at least one cron fire is logged under `maintain-hawaii-feed`.
5. `www.rootrecord.cloud` returns 200 or 3xx, not 530/1033. MemAvailable stays ≥ 300 MB.

## Result

| Check | Before | After |
| --- | --- | --- |
| `hawaii.ndjson` | 1,827,611,155 B (inode 291042) | 50,331,325 B (inode 291042); run time 0.53 s; `trimmed 1827611155 -> 50331325 bytes; offset reset`; rc 0 |
| `df -h /` | 5.2G used, **1.5G free** (78 %) | 3.5G used, **3.2G free** (53 %) |
| feed-server / connection-history | active / active | active / active; writer still appending (+≈ 42 MB/h) |
| Auto-trim | none (desk calls exit 127) | `ubuntu` crontab `*/15 … nice -n 10 … \| logger -t maintain-hawaii-feed`. 14:15:02 fire: `feed 55736202 bytes <= 67108864 -- no trim` **14:30:03 fire: `trimmed 67465261 -> 50343031 bytes; offset reset`**. This is the first automatic trim on AWS. The inode is unchanged, the writer (pid 222029) is still appending, and all services are active |
| `www.rootrecord.cloud` | HTTP/2 **530** (1033) | **200** (5346 B, globe `index.html`); `rootrecord.cloud` 301 → `www` |
| Tunnel `network-globe` [redacted tunnel ID] | 0 connections, cloudflared purged 2026-09-26 02:41 HST | 4 connections registered 14:12:13–15 HST |
| `rr-aws-ip uptime` (desk) | TCP timeout (stale IP) | **PASS** (up 3 days 9:23) |
| `rr-aws uptime` (tunnel) | 1033 / bad handshake | the tunnel carries SSH (the ingress rule `ssh.rootrecord.cloud → ssh://localhost:22` was added); host key `[redacted SSH host-key fingerprint]` = the AWS `/etc/ssh/ssh_host_ed25519_key.pub`. With that verified key: **PASS**. With the desk `known_hosts`: FAIL, because line 11 holds the old instance's key (`[redacted SSH host-key fingerprint]`, same as [redacted public IP]) |

## Resource impact

| When | Load (1/5/15) | MemAvailable | Swap used | Peak RSS |
| --- | --- | --- | --- | --- |
| before (14:10) | 0.27/0.31/0.28 | 512 MB | none (no swap) | — |
| during (trim) | not recorded | 508 MB | none | trim 0.53 s wall |
| after (14:15) | 1.39/1.17/0.74 | 446 MB | none | server.js 84.5 MB, cloudflared 39.5 MB, feed-server 32 MB, history 31.6 MB |

## Cleanup confirmation

- [x] No test process left. The nohup trim finished (rc 0), and the temp `.deb` and `/tmp` unit copies were removed.
- [x] New listeners are intended only: `:8090` (server.js) and cloudflared metrics on localhost.
- [x] No models are involved.

## Open items / caveats

- The desk `~/.ssh/known_hosts` line 11 (`ssh.rootrecord.cloud`) is the pre-rebuild host key. It was not changed. Fix, after Alexander OKs it: `ssh-keygen -R ssh.rootrecord.cloud`, then add the verified key (`[redacted SSH host-key fingerprint]`).
- Still untouched: the poller, the Elastic IP (P0-3), Cloudflare DNS/tunnels (none created, none re-routed), Vercel, the `rootserver` tunnel [redacted tunnel ID] (connectors are on the desk), and the leftover `cloudflared-update.{service,timer}` (disabled).
- The Mainland repo mirror files are uncommitted: `network-globe/cron/`, `network-globe/*.service`, `mirror/.cloudflared/config-globe.yml` (+ssh rule), and the README section.
- Double-count after each trim in `hawaii-connections.sqlite3` (see the safety review). A fix belongs in `connection-history.py` (track the inode and a post-trim resume point) and is proposed, not done.
