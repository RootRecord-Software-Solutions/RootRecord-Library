# Proposal — AWS US-Mainland node: stabilise, then make it a health + hazard continuity mirror

| Field | Value |
| --- | --- |
| **Date (HST)** | 2026-09-29 |
| **Proposed by** | Grok (executor, us-mainland-import pass), building on the US-MAINLAND-SERVER lane handoff (2026-09-22 functions/to-dos) |
| **State** | PROPOSED overall. **P0-1 LANDED/PASS** and **P0-4 LANDED/PASS** (cloudflared www) on 2026-09-29 14:07–14:15 HST, see the [test record](../07-testing/2026-09-29-aws-hawaii-trim-and-cloudflared.md). The rest is unchanged |
| **Grounding** | [US-Mainland-Server architecture](../00-architecture/US-Mainland-Server.md) (read-only SSH 13:49 HST); test record [2026-09-29-us-mainland-import-and-ssh](../07-testing/2026-09-29-us-mainland-import-and-ssh.md); G2 `handoff/emergency-2026-09-22/US-MAINLAND-SERVER-FUNCTIONS-TODOS-2026-09-22.md` |
| **Needs sign-off from** | Alexander (every AWS change), plus a working SSH path |
| **Related WO** | WO-SRV (Servers cutover) |

## Problem (measured)

- AWS is almost empty: only `rr-rootserver-poller` (1 s system monitor + comms polls + git pull), the Network Globe feed/history services and `github-poller` run. No cloudflared → `ssh.rootrecord.cloud` / `www.rootrecord.cloud` return Cloudflare **1033**; the 13 legacy `rr-*` hazard/radio/packer units are not running.
- `hawaii.ndjson` is **1.82 GB and growing ≈ 39 MB/h**; 1.6 GB free on a 6.7 GB root → **full in ≈ 40 h** because the trim script is missing on AWS.
- Public IP changed ([redacted public IP] → [redacted public IP]); `rr-aws-ip` is stale and `rr-aws` depends on the missing tunnel.
- t3.micro: 908 MB RAM, 514 MB available.

## Proposal (priority order)

### P0 — stop the disk from filling (urgent, small, reversible)

1. **LANDED / PASS (2026-09-29 14:07 HST)**. The script was deployed to `…/network-globe/network-globe/scripts/maintain-hawaii-feed.sh` and run once at `nice 10`: `hawaii.ndjson` 1,827,611,155 → 50,331,325 B (same inode), free disk 1.5G → 3.2G. Auto-trim now runs on AWS from the **`ubuntu` crontab `*/15`** (line mirrored in Mainland `network-globe/cron/maintain-hawaii-feed.crontab`, log `journalctl -t maintain-hawaii-feed`). Backup: AWS `~/rootrecord/bin.bak-hawaii-trim-20260929-140641/` (includes the last 64 MiB of the feed). [Test record](../07-testing/2026-09-29-aws-hawaii-trim-and-cloudflared.md). Original plan:
   Deploy the repo's own bounded-feed script where the desk collector already calls it, then run it once:
   ```bash
   H="-o BatchMode=yes -o ConnectTimeout=5 -o HostName=[redacted public IP] rr-aws-ip"
   ssh $H 'mkdir -p /home/ubuntu/network-globe/network-globe/scripts && df -h /'
   scp -o HostName=[redacted public IP] "/home/rootrecord/RootRecord-Ecosystem/1 - Servers/2 - RootRecord-US-Mainland-Server/network-globe/maintain-hawaii-feed.sh" rr-aws-ip:/home/ubuntu/network-globe/network-globe/scripts/
   ssh $H 'chmod 755 /home/ubuntu/network-globe/network-globe/scripts/maintain-hawaii-feed.sh && bash /home/ubuntu/network-globe/network-globe/scripts/maintain-hawaii-feed.sh && df -h /'
   ```
   Expected: `trimmed 18xxxxxxxx -> ~50331648 bytes; offset reset`, ~1.7 GB freed. The desk collector then keeps it ≤ 64 MB every 15 min. (Optional first: copy the last 48 MB aside if the history matters — the design says AWS is a live mirror, not a store.)
2. Add `logrotate` for `/home/ubuntu/**/*.log` and a disk alarm (P1-1 health reports `disk_free_pct`).

### P0 — stable, documented access

3. Allocate an **Elastic IP** (free while attached to a running instance) so the address stops changing; update local `~/.ssh/config` `rr-aws-ip` HostName and the collector `AWS_HOST` default together.
4. **LANDED / PASS for `www` (2026-09-29 14:12 HST)**. cloudflared 2026.9.3 (official .deb) now runs as `cloudflared-network-globe.service` (User=ubuntu, `--no-autoupdate`) on the existing tunnel `network-globe` **[redacted tunnel ID]** (credentials JSON from the desk's old aws-sync mirror, 0600; no tunnel created, no DNS change). The origin is `network-globe-web.service` (`server.js` :8090). `https://www.rootrecord.cloud/` went from 530/1033 to **200**. An `ssh.rootrecord.cloud → ssh://localhost:22` rule was added: the tunnel carries SSH and passes with the verified AWS host key, but the desk `known_hosts` still holds the old instance key for `ssh.rootrecord.cloud`, so `ssh rr-aws uptime` stays FAIL until that entry is replaced (needs OK). `rr-aws-ip` HostName is now [redacted public IP] (PASS). Backup: AWS `~/rootrecord/bin.bak-cloudflared-20260929-141048/`. Original plan:
   Restore **cloudflared** on AWS as a systemd unit with two ingress rules: `www.rootrecord.cloud → 127.0.0.1:8090` (existing `config-globe.yml`, tunnel `[redacted tunnel ID]…`) and `ssh.rootrecord.cloud → ssh://localhost:22`. Then `ssh rr-aws uptime` (desk ProxyCommand already fixed) becomes the primary path.

### P1 — health endpoint (what "continuity node" should expose first)

5. Tiny stdlib `health.py` on AWS (127.0.0.1:8091, behind the tunnel as `health.rootrecord.cloud` or `/health` on the globe host) returning JSON: `at`, uptime, load, mem/disk free %, `system-current.json` summary, unit states, `hawaii.ndjson` size, git HEAD vs origin, public IP. No secrets, read-only.
6. Desk side (gated, e.g. `RR_MAINLAND_HEALTH=1`, **only when Alexander asks for a jobs.py edit**): fetch it every 5 min → Database `System/Mainland/aws-last.json`; Root Monitor Network page can read that file (panel owner's lane).

### P1 — hazard collector mirror (continuity when the solar desk is offline)

7. Run the Pacific **Geology** collector (`geology_collect.py`, stdlib, 5 min, USGS/HVO) and the **current-only NWS weather** mirror (`weather/` in this repo) on AWS, writing `*-last.json` / `*_current.*` only (no history → fits 6.7 GB). The desk pulls them read-only when its own collectors were down (power / Starlink gaps). Honour the standing rule: AWS collects live; no desk→AWS seed.
8. Keep the legacy `rr-*` units (radio, packer, youtube, …) **parked** until each has an owner and a reason; revive one at a time.

### P2 — backup target

9. The host disk is too small for backups. If off-site backup is wanted, use an **S3 bucket** (versioned, lifecycle to Glacier) written by `restic` from the desk for non-git Database data (`RootRecord/` sqlite store, `Logs/`), with the restic password only in a gitignored desk file. AWS EC2 is not needed for this path. Git repos are already on GitHub.

### P3 — repo hygiene

10. Enable the `mainland` auto-sync row (exact line in the architecture doc) so desk edits reach GitHub → AWS.
11. Title-case layout (mapping in the repo README) — one coordinated move with the AWS paths, not before P0–P1.
12. Security: run the AWS git pull as `ubuntu` not root; branch protection on `main`; consider making the repo private or moving IDs out of `communications/.env.example`; untrack `scripts/__pycache__/jobs.cpython-314.pyc`.

## Scope and non-goals

- Out: LLM inference on AWS (stays on the desk NPU), EcoFlow/BLE, Stripe/memberships, public wording.
- Out: any change to AWS in this pass.

## Resource impact / safety

P0-1 frees ~1.7 GB with one short `tail`/`sed` pass on a 1.8 GB file (seconds of I/O on t3.micro; collector already closes its writer before maintenance — run it right after a desk maintenance cycle or accept one reconnect). P1 services are stdlib, < 30 MB RSS each, 5-min cadence. Dated backup before every AWS edit (lane standing rule).

## How it would be tested

- P0-1: `df -h /` before/after, `stat -c %s hawaii.ndjson` ≤ 64 MB, desk journal shows `trimmed …` (no exit 127) at the next 15-min cycle, globe still updates.
- P0-4: `ssh -o BatchMode=yes -o ConnectTimeout=5 rr-aws uptime` PASS; `curl -sI https://www.rootrecord.cloud` not 530.
- P1-5: `curl -s …/health | jq .disk_free_pct` from the desk.

## Open questions

- Is the Hawaii feed history on AWS worth keeping (copy the tail before trimming) or is live-only fine?
- Elastic IP vs. Cloudflare-only access?
- Which hazard sources should AWS mirror first (quakes/HVO, NWS alerts, hurricane)?
- Is `github-poller.service` / `ip-notify.sh` on AWS (not in the repo) still wanted? They should be committed to the repo or removed.
- Does `communications_telegram` on AWS share a bot token with the desk relay (409 risk)?
