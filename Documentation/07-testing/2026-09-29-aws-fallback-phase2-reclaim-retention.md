# Test record: AWS fallback Phase 2, reclaim resources (reversible) and retention caps

| Field | Value |
| --- | --- |
| **Date / time (HST)** | 2026-09-29 15:41–16:16 HST |
| **Tester** | Grok (executor) for Alexander Storey (AWS changes approved 15:40 HST; t3.micro kept; trimmed profile) |
| **Change under test** | AWS `rr-aws` ([redacted public IP]): legacy pollers stopped, OS services trimmed, apt cache cleaned, journald and logrotate caps, daily backup/release retention. [Proposal Phase 2](../08-ideas/2026-09-29-aws-fallback-rebuild.md) |
| **State** | **PASS**: every change is reversible (units and files kept). RAM stayed ≥ 485 MB (min 497 over 16:03–16:14 HST). **iowait went from 7.4 % to 0.1 %** (Phase 1 peak: 28–44 %) |
| **Evidence** | AWS `~/rootrecord/bin.bak-fallback-phase2-20260929-154333/`: `unit-states.before.txt`, `unit-states.after-reclaim.txt`, `metrics.before.txt`, `vmstat.before.txt`, `metrics.after.txt`, unit files, scripts, crontab, `journald.conf`, sha256 |
| **Commits** | Library: desk auto-sync (see the worklog) |
| **Backup** | AWS `~/rootrecord/bin.bak-fallback-phase2-20260929-154333/` (taken before any change). Desk `/home/rootrecord/Database/GITHUB/aws-fallback-phase2.bak-20260929-154400/` |

## Changes (all `sudo systemctl`, one at a time, state recorded)

| Unit | Before | After | Why it's safe | Re-enable |
| --- | --- | --- | --- | --- |
| `github-poller.service` | enabled, active (`git fetch` every 1 s, 14,318 CPU-s in 3.4 d) | **disabled, inactive**; unit + `~/github-poller.sh` kept | the desk is canonical; AWS no longer pulls | Root Monitor flag `github_poller` = 1, or `sudo systemctl enable --now github-poller.service` |
| `rr-rootserver-poller.service` | enabled, active (root; 4 jobs every 1 s, all script paths missing) | **disabled, inactive**; unit + `~/automations/scripts/*` kept | it did nothing useful | flag `legacy_poller` = 1, or `sudo systemctl enable --now rr-rootserver-poller.service` |
| `ModemManager.service` | enabled, active | disabled + **masked** | no modem on EC2 | `sudo systemctl unmask ModemManager && sudo systemctl enable --now ModemManager` |
| `fwupd.service` + `fwupd-refresh.timer` | static (D-Bus) active; timer enabled | stopped + **masked**; timer disabled | no firmware updates on a VM | `sudo systemctl unmask fwupd && sudo systemctl enable --now fwupd-refresh.timer` |
| `udisks2.service` | enabled, active | disabled + **masked** | no removable disks | `sudo systemctl unmask udisks2 && sudo systemctl enable --now udisks2` |
| `multipathd.service` (+ `.socket`) | enabled, active | disabled, inactive | `dmsetup ls` = no devices; root is plain `nvme0n1p1` | `sudo systemctl enable --now multipathd.service` |
| `networkd-dispatcher.service` | enabled, active | disabled, inactive | the only hooks are `chrony-onoffline`; chrony still tracks 169.254.169.123 | `sudo systemctl enable --now networkd-dispatcher` |
| `unattended-upgrades.service` | enabled, active | disabled, inactive | this is only the **shutdown helper** (`unattended-upgrade-shutdown --wait-for-signal`); `InstallOnShutdown` is unset; daily security upgrades still run from `apt-daily-upgrade.timer` (active) | `sudo systemctl enable --now unattended-upgrades` |
| `apt-get clean` | `/var/cache/apt` 105 MB | 48 KB | the cache re-downloads when needed | none needed |
| kept on purpose | snapd (amazon-ssm-agent snap refreshes), ssm-agent, journald, cron, chrony, sshd | | | |

**Retention caps**, installed by `deploy-aws-fallback.sh` and root-owned:
- `/etc/systemd/journald.conf.d/60-rootrecord-caps.conf`: `SystemMaxUse=100M`, `SystemKeepFree=1G`, `SystemMaxFileSize=16M`, `RuntimeMaxUse=16M`, `MaxRetentionSec=14day`. The journal is 24 MB now.
- `/etc/logrotate.d/rootrecord-fallback`: `fallback/logs/*.log` 5 MB × 7, compressed, copytruncate. `logrotate -d` gives rc 0.
- Tick daily retention: `~/rootrecord/bin.bak-*` older than 14 days are deleted, except the newest per kind; releases keep 5. The first run removed only the failed release `20260929-155746-fdf34b08.failed-…`.
- Spool: hard cap 256 MB, oldest dropped first.
- The feed trim cron is unchanged and still runs: 02:00 and 02:15 UTC (16:00 and 16:15 HST) logged "no trim" (65.1 MB ≤ 64 MiB).
- `snap refresh.retain` is already at the default of 2 (unset), so it wasn't changed.

## Before / after (same method: `vmstat 10 7` + a 60 s `/proc/stat` delta, AWS side)

| Metric | Before (15:41–15:44 HST) | After (16:13–16:15 HST) |
| --- | --- | --- |
| MemAvailable | 447–464 MB | **493–516 MB** (23 tick samples 16:03–16:14: min 497, avg 506, **0 below 485**) |
| RAM used (`free -m`) | 460 MB | 415 MB |
| Disk used / free | 3,588 / 3,166 MB | **3,476 / 3,278 MB** |
| CPU (60 s) | user 2.8 %, sys 2.0 %, idle 87.5 %, **iowait 7.4 %**, steal 0.4 % | user 0.3 %, sys 0.2 %, idle 99.2 %, **iowait 0.1 %**, steal 0.2 % |
| Block writes (`vmstat bo`) | 1.9–2.6 MB/s | **0.03–0.12 MB/s** |
| Load (1/5/15) | 0.45 / 1.07 / 1.02 | 0.01 / 0.03 / 0.16 |
| History writes | 43.9 MB/min | 1.6 MB/min ([record](./2026-09-29-aws-globe-history-batched-commits.md)) |

## Verdict

**PASS.** The globe, tunnel and history services stayed up throughout. The feed still streams (~9.8 KB/s), and `systemctl --failed` is empty.
