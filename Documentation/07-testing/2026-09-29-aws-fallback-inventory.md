# Test record: AWS fallback rebuild, Phase 1 read-only inventory

| Field | Value |
| --- | --- |
| **Date / time (HST)** | 2026-09-29 14:57–15:05 HST |
| **Tester** | Grok (executor) for Alexander Storey |
| **Change under test** | None. This was a read-only inventory of AWS `rr-aws` ([redacted public IP]) for the [AWS fallback rebuild proposal](../08-ideas/2026-09-29-aws-fallback-rebuild.md). WO-SRV |
| **State** | **PASS**: all reads done and **0 changes on AWS**. **Findings:** the instance has **908 MB RAM, not 2 GB**, and only ~445 MB is available; there is 28–44 % iowait; two legacy pollers waste CPU; `:8787` is still public (listed, not changed) |
| **Evidence** | the command outputs summarised below; the catalog `Pacific Apps/Control-Panel/Lib/rr_aws_fallback.json` carries the per-function measurements |
| **Commits** | Library: desk auto-sync (see the worklog) |
| **Backup** | not needed on AWS (read-only). Desk backup of the docs and Control-Panel files: `/home/rootrecord/Database/GITHUB/aws-fallback-phase1.bak-20260929-150225/` |

## How (exact commands / procedure)

All commands went through `ssh -o BatchMode=yes rr-aws-ip` and were read-only:

```bash
curl -s http://169.254.169.254/latest/meta-data/instance-type  # (IMDSv2 token) -> t3.micro
free -m; swapon --show; nproc; uptime; df -h /; uname -r; lsb_release -ds
sudo du -xsh /usr /snap /var/lib/apt /var/cache/apt /var/log ~/rootrecord ~/network-globe
journalctl --disk-usage
systemctl list-units --type=service --state=running --no-pager
systemctl list-unit-files --state=enabled --no-pager; systemctl list-timers --no-pager
ps -eo pid,user,rss,cputimes,cmd --sort=-rss | head -30
crontab -l; sudo crontab -l; ls /etc/cron.d
sudo ss -ltnup
vmstat 1 5; sudo iotop -b -o -n 3 (or /proc/<pid>/io deltas)
awk -F= '{print $1}' ~/.env        # key NAMES only, values never printed
git -C ~/US-Mainland-Server log -1 --oneline; git -C ~/US-Mainland-Server status --short
```

## Results

| Area | Result |
| --- | --- |
| Instance | t3.micro, 2 vCPU, **908 MB RAM**, no swap, Ubuntu 26.04, kernel 7.0.0-1006-aws, load ~1.1–1.3 |
| RAM | ~463 MB used, **~445 MB available** |
| Disk | 6.7 GB root: 3.5 GB used, **3.1 GB free**. `/usr` 2.7 GB, `/snap` 889 MB, `/var/lib/apt` 152 MB, `/var/cache/apt` 105 MB, `/var/log` 33 MB, journal 24 MB, `~/rootrecord` backups 65 MB, feed 55 MB, history SQLite 332 KB |
| Services (custom) | `cloudflared-network-globe` 29–40 MB · `network-globe-web` 80–85 MB on 127.0.0.1:8090 · `network-globe-feed-server` 35–37 MB on **0.0.0.0:8787** · `network-globe-connection-history` 28–47 MB, 2,501 CPU-s, commits once per record (8–12 MB/s writes) · `rr-rootserver-poller` (root, 10.7 MB, 701 CPU-s; its 4 jobs every 1 s point at missing scripts) · `github-poller` (`git fetch` every 1 s, **14,318 CPU-s** in ~3.4 days) · `ip-notify` oneshot · `cloudflared-update.{service,timer}` leftovers (disabled) |
| Services (OS) | fwupd, ModemManager, udisks2, multipathd, snapd, unattended-upgrades, amazon-ssm-agent (snap) |
| Cron | `ubuntu`: `*/15` feed trim only. root: none. `/etc/cron.d`: `e2scrub_all` |
| Ports | 22 public · **8787 public (feed-server; Alexander's decision still pending, left open)** · 8090 / 20241 / 53 on localhost only · cloudflared UDP out |
| Secrets | `~/.env` 0600 with 23 key names (EcoFlow ×6, A-EYES ×2, GitHub, Cloudflare ×3, Telegram/Discord/Slack bots). Recommendation: cut this down to the relay keys only |
| Repo | `~/US-Mainland-Server` at `b61d63c`, `network-globe/server.js` modified; live `~/network-globe` differs from the repo |

## Verdict

**PASS** (read-only; AWS unchanged). The inventory is the grounding for the budget tables in the proposal. At 908 MB, the default-ON set leaves only ~279 MB free, below the 512 MB floor, so the proposal's first sign-off step is to resize to t3.small (or accept a trimmed micro profile).
