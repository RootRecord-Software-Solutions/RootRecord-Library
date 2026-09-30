# Test record: AWS fallback Phase 2, runtime deploy (desk one-way script) and Root Monitor write mode

| Field | Value |
| --- | --- |
| **Date / time (HST)** | 2026-09-29 15:55–16:16 HST |
| **Tester** | Grok (executor) for Alexander Storey (AWS changes approved 15:40 HST) |
| **Change under test** | New desk-canonical runtime (US-Mainland-Server checkout `fallback/`: `deploy-aws-fallback.sh`, `deploy/remote-activate.sh`, `app/rr_fallback_tick.py`, `app/rr-fallback-apply`, `system/*`, `profile/*`, `README.md`), deployed to AWS `~/rootrecord/fallback/`. Pacific `Apps/Control-Panel`: `settings.json` `aws_fallback_mode` = `write`, catalog `Lib/rr_aws_fallback.json` (trimmed-micro + `relay_send`), `Lib/rr_aws_fallback.py` (status reports the release), `rr_aws_page.py` (floors from the catalog). [Proposal Phase 2](../08-ideas/2026-09-29-aws-fallback-rebuild.md) |
| **State** | **PASS**. Live release `20260929-160245-5ee01b1e`, health OK, mode NORMAL. Rollback proven. Write round-trip passed |
| **Evidence** | AWS `~/rootrecord/fallback/logs/deploy.log`, `logs/events.log`, `state/mem_history.json`, `data/current/status.json`; desk `Database/Logs/Mainland/aws-fallback-deploy.log`; screenshot `test-reports/Control-Panel/aws-fallback-20260929/20260929-160715-aws-fallback-phase2-01-write-mode-status.png` |
| **Commits** | Library + Pacific: desk auto-sync (see the worklog). Mainland: none (checkout not in auto-sync) |
| **Backup** | AWS `~/rootrecord/bin.bak-fallback-deploy-<ts>/` for each deploy (155746, 155836, 155947, 160152, 160245, 160310) and `bin.bak-fallback-flags-20260929-160759/`, `-160844/` for each flag write. Desk `/home/rootrecord/Database/GITHUB/aws-fallback-phase2.bak-20260929-154400/` |

## Deploy runs (in order)

| Time (HST) | Run | Outcome |
| --- | --- | --- |
| 15:56:59 | `--dry-run` | 13 files; 8 system files to INSTALL; 19 flags to create; nothing changed |
| 15:57:46 | `--apply` | manifest OK → backup → flags created → system files installed → **tick failed** (the `app` symlink pointed at the release root, not `app/`) → **automatic rollback**: units removed, fallback timers disabled, release marked `.failed` (**rollback path 1: first install**) |
| 15:58:36 | `--apply` (fixed: `app -> releases/<REL>/app`) | **HEALTH OK**: tick success, `status.json` fresh with the right release, `127.0.0.1:8090/health` 200, tunnel active, apply plan "in sync" |
| 15:59:47 | `--apply --test-rollback` | forced health failure → rolled back to the previous release (**rollback path 2: with prev**). **Bug found:** the restore used `cp -p` from the ubuntu-owned backup, which left the 8 system files **owned by ubuntu** (including root-run `/usr/local/sbin/rr-fallback-apply`), and `app.prev` pointed at `app` |
| 16:02:07 | `--apply` | stopped by the new `logrotate -d` check ("file owner is wrong"), then rolled back. I fixed ownership by hand at once (`chown root:root`, 0644/0755; `find ! -user root` = none). The window was about 2 min, and the next dry-run showed all system files "unchanged" against the release sha256, so they hadn't been altered. `app.prev` removed |
| 16:02:45 | `--apply` (restore now uses `install -o root -g root -m …`; `app.prev` restored or removed) | **HEALTH OK** → live `20260929-160245-5ee01b1e` |
| 16:03:10 | `--apply --test-rollback` | forced failure → rolled back to `160245`, `app.prev` → `155836`, **all system files root-owned** (rollback path 2 re-proven) |

## Runtime behaviour tests

- **Desk, temp root:** NORMAL → SUSPECT (feed 200 s old) → FALLBACK (400 s) → `aws_status` + `aws_mode` spooled. The pack gave `rr-aws-…-000001.zip` (manifest sha256 per file). Back in NORMAL after 3 fresh ticks, with a final pack `000002`. `desk-ack.json {"pack_seq":1}` pruned `000001` only. Retention removed the old backup of kind x and kept the newest per kind. The budget guard gave `BUDGET_SKIP` with a huge floor. Tick peak RSS 13.1 MB, 0.03 s.
- **AWS:** the `rr-fallback-runner.timer` tick runs every 30 s. `rr-fallback-apply.path` fires on each flag write (journal: "in sync: no changes"). The reconcile timer runs every 15 min. The guard's `BUDGET_SKIP` (avail 469 MB at 15:58) was fixed so a skip is retried on the next tick and logged once; after that, `relay_buffer` reported "nothing to pack" and retention reported "ok".
- **Not exercised:** a real FALLBACK on AWS (it would need the desk feed to stop) and any Telegram send (`relay_send` = 0, sign-off).

## Root Monitor write mode: harmless toggle round-trip (`system_monitor`, a runner-only sample)

This used the exact calls the page makes (`rr_aws_fallback.status_argv` / `write_argv`, desk settings `mode=write`, alias `rr-aws-ip`):

```text
16:07:58 before        deployed=1 release=20260929-160245-5ee01b1e mode=NORMAL system_monitor=False avail=494
16:07:59 write 1       ok system_monitor=1 backup=~/rootrecord/bin.bak-fallback-flags-20260929-160759
16:08:01 status        system_monitor=True
16:08:29 AWS tick      data/current/system_monitor.json written (mem_avail 512, disk 3281) · functions.system_monitor "ok avail 512 MB"
16:08:45 write 0       ok system_monitor=0 backup=~/rootrecord/bin.bak-fallback-flags-20260929-160844 (contains 1 = the pre-write state)
16:08:46 status        system_monitor=False · apply journal "in sync: no changes" (x2)
bad id "x;rm -rf /"    rejected (ValueError) before any SSH
```

**GUI:** the driver opened the page in write mode, read the status and saved `…-phase2-01-write-mode-status.png` (secret guard PASS). The label still said "reading…" at capture. The test window then got a `close-request` from outside the process, about 3 s after each of 4 starts (Root Monitor itself was relaunched on the desk at 16:04:44, so someone is probably at the desk). I stopped opening windows and ran the round-trip above instead. `--check`: 0 errors, peak RSS 85.1 MB; settings 103/103. The running Root Monitor (started 16:04:44) loaded `write` mode.

## Verification after the deploy (steady: last change 16:08:46)

| Check | Result |
| --- | --- |
| MemAvailable | 23 tick samples 16:03–16:14 HST: **min 497 MB**, avg 506, max 516, **0 below 485**; 501 MB at 16:15:52 |
| Disk | 3,278 MB free (floor 1,536) |
| iowait | **0.1 %** (before: 7.4 %; Phase 1 peak: 28–44 %) |
| www | `/` 200, `/health` 200 (`flows` 57), `/api/state` 200 (arcs 71, points 57); `/server.js` and `/data/hawaii.ndjson` still 404 |
| Feed / trim cron | the feed grows ~9.8 KB/s; cron logged at 16:00 and 16:15 HST |
| Services | tunnel, web, feed-server (:8787 unchanged), history, fallback timers + path: active. `github-poller`, `rr-rootserver-poller`: inactive. `systemctl --failed`: none |

## Verdict

**PASS.** Stable at the end of Phase 2. The deploy script is proven for dry-run, first install, update, and both rollback paths.
