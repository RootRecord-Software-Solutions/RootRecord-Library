# Root Monitor — rename, Running / Network (+ Starlink) / SSH / Not-migrated pages, full Settings registry

| Field | Value |
| --- | --- |
| **Date** | 2026-09-29, 12:43–13:10 HST |
| **Tester** | Grok Bot (executor subagent) for Alexander Storey |
| **Changed** | Pacific `Apps/Control-Panel/` (new: `rr_pages.py`, `rr_ui.py`, `Lib/rr_registry.py`, `Lib/rr_config_io.py`, `Lib/rr_running.py`, `Lib/rr_netstat.py`, `Lib/rr_ssh.py`, `Lib/rr_migration.json`, `Starlink/starlink_status.py`, `Packaging/poller-dashboard-terminal.desktop`, `Packaging/root-monitor-autostart.desktop`, `Packaging/swap-default-viewer.sh`, `Tests/test_settings_io.py`; edited: `rr_control_panel.py`, `Lib/rr_settings.py`, `Lib/rr_sources.py` (docstring), `Packaging/*.desktop|.service|install-launcher.sh`, `Tests/run-check.sh`, `README.md`) |
| **State** | **PASS** functional (`--check` off/on, strace camera-off 0, leak tests 0, settings editor 103/103, real-window render). **FAIL** on the RSS target: `--check` 84.5 MB > 80 MB. **VERIFY PENDING**: viewer swap, autostart, Conky start (sign-off) |
| **Backup** | `/home/rootrecord/Database/GITHUB/control-panel-settings.bak-20260929-123505/` (+ `Control-Panel-before-root-monitor-1244.tgz`, installed launcher copy) |
| **Evidence** | `RootRecord-Ecosystem/test-reports/Control-Panel/check-root-monitor/` (check-off/on, time, strace, test-settings-io) and the PNGs below |

## Pass criteria (written before the result)

1. `--check` builds all 13 pages and all 10 Settings + 23 placeholder sub-pages, loads every source once, 0 errors.
2. Camera viewer off → 0 syscalls under `Media/Images` and 0 connects to :8791 (strace -f).
3. No secret value appears in any widget string, any Settings row string, the unit-test stdout, or any screenshot (checked in code; values never printed).
4. Editor on **temporary copies** of every editable file: one-line change, comments/line count/permissions kept, new inode (atomic rename), backup byte-identical with 0600 for secret files, revert byte-identical, stale plan refused, secret Replace/Clear diffs masked, git-tracked secrets refused, all 5 text formats covered, no `.tmp` left, temp dir removed, real backup dir untouched.
5. Starlink helper and panel processes gone after every run; the helper runs only while Network is visible.
6. Existing viewers byte-identical to the 11:56 backup; poller PID 105444 not restarted.
7. `--check` peak RSS < 80 MB.

## Results

| # | Result | Evidence |
| --- | --- | --- |
| 1 | **PASS** — 13 pages, 0 errors, `RESULT: PASS` both modes | `check-off.txt`, `check-on.txt` |
| 2 | **PASS** — off: `Media/Images`=0, `:8791`=0; on: 5 image syscalls, 4/4 stills | `strace-off.txt`, `strace-on.txt` |
| 3 | **PASS** — 34 known secret values vs ~422k chars of widget text → 0; unit-test stdout → 0; screenshot guard 0 matches on all 24 captures. First run found 9 matches (env-var names treated as secrets, a Cloudflare account id and EcoFlow serials repeated in non-secret files, a `gh` user name); fixed by skipping names/paths in the secret list, cross-file masking and a render-time redaction pass | `check-*.txt` |
| 4 | **PASS** — 103 checks, 0 failures (earlier runs: JSON edits re-serialised whole files → replaced by value-token edits; cloudflare snapshots showed a secret-equal value → masked) | `test-settings-io.txt` |
| 5 | **PASS** — `ps` after runs: no `starlink_status` / `rr_control_panel` process; screenshot run reports "starlink helper running at exit: False" | shell log |
| 6 | **PASS** — 10/10 unchanged (`poller-dashboard.py`, `poller-watch.py`, `open-poller-window.sh`, `npu-status.sh`, `rootserver_poller.py`, `run-poller.sh`, poller README, autostart entry, Desktop launcher + script); poller MainPID 105444 active | cmp vs `control-panel.bak-20260929-115632/existing-viewers/` |
| 7 | **FAIL** — 84.5 MB (was 73.8 MB before the new pages). Window (25 s): 85.7 MB | `check-off.txt`, `--run-for 25` |

**One-time live checks (read-only, allowed once each):**

- Starlink `192.168.100.1:9200` reachable at 12:45; `get_status` → CONNECTED, uptime ~12.4 h, PoP latency 50–58 ms, drop 0 %, obstruction 0.07 %, no alerts — **PASS**. The helper is also exercised once per `--check` (use `--no-starlink` to skip).
- `timeout 5 ssh -o BatchMode=yes -o ConnectTimeout=5 rr-aws uptime` (12:47) → **FAIL**: its ProxyCommand binary `~/.local/bin/cloudflared` does not exist.
- same for `rr-aws-ip` → **FAIL**: no answer within 5 s.
- Nothing else was run remotely.

**Screenshots** (`/home/rootrecord/RootRecord-Ecosystem/test-reports/Control-Panel/`): `20260929-130606-01-energy.png` … `-07-running.png`, `-09-ssh.png` … `-24-settings-panel.png` (23 files; the Network capture of that run returned no texture) and `20260929-130419-08-network.png` (Network with live Starlink). The earlier `20260929-130419-*` set is kept except its Running PNG, which was removed because a worklog `find` command line showed the excluded private paths; Running now shows them as `<excluded path>`.

## Resource impact

| When | MemAvailable | Peak RSS |
| --- | --- | --- |
| before (12:44) | 7159 MB | — |
| during (12:56–13:08) | ≥ 7212 MB | `--check` 84.5 / 98.9 MB; window 85.7 MB; screenshot 127.3 MB; Starlink helper 55.7 MB |
| after (13:08) | ≥ 7200 MB | no processes left |

## Caveats / open items

- RSS target missed by 4.5 MB (`--check`); Settings sub-pages are the main cost even with lighter rows and release-on-leave.
- The flags editor cannot save until `rr-flags.conf` exists (sign-off).
- `rr-aws` SSH is broken by a stale ProxyCommand path; `rr-aws-ip` unreachable; Mainland has no Host alias.
- The "Not migrated" list is a curated snapshot (`Lib/rr_migration.json`, 2026-09-29 12:50 HST); update it when items land.
- Conky is installed (1.22.2, dpkg 12:35 HST, not by this pass); config installed, not started.
