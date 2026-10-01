# Root Monitor (GTK4 control panel) + Conky readout — architecture

*Added 2026-09-29 ~12:15 HST as "RootRecord Control Panel"; renamed **Root Monitor** and extended 2026-09-29 12:43–13:10 HST. File name and app paths are unchanged. Status: **LANDED**. Login autostart **applied** 2026-09-30 02:33 HST. `--check` that night: 0 secret leaks, peak RSS 89.8 MB (over the 80 MB target). Conky is still not started. The user systemd unit is still not installed.*

## 1. What it is

A native Linux desk app for the RootRecord Pacific Solar Server: Python + PyGObject with **GTK 4.22.4 + libadwaita 1.9** (system `python3`, no venv for the app). No browser, Chromium or Electron. Plus a Conky config for an always-visible readout.

It is **added alongside** the existing displays and replaces none of them. All 10 existing viewer/dashboard/launcher files were re-compared byte-for-byte with the 11:56 backup at 13:08 HST: **unchanged**.

| Existing display (unchanged) | Where | What it shows | Reads / how often |
| --- | --- | --- | --- |
| `poller-dashboard.py` (default viewer; opened by `open-poller-window.sh`; autostart `~/.config/autostart/rootrecord-poller-watch.desktop`; Desktop `RootRecord-Poller-Window.desktop`) | Pacific `Automations/scripts/poller/` | header + clock, 8 service rows PASS/WARN/FAIL, **B1 river2pro / B2 delta2 / B3 laptop bars**, SUMMARY, SYS, SUN, recent log | soc JSON, sysfs, log tail, `/proc`, `systemctl` — every 5 s |
| `poller-watch.py` (`POLLER_VIEWER=poller-watch.py`) | same | banner + colour live log | tails `automations_current.log` |
| Poller **status line** (ENERGY heartbeat, `http://127.0.0.1:8799/`) | `rootserver_poller.py` | `ENERGY status= B2= B1= …` | every 60 s |
| `npu-status.sh` | Pacific `System/scripts/plumbing/` | accel, packages, lock, FLM state | on demand |

## 2. Pages

Every page does **nothing unless it is visible**. One GLib timeout (`refresh_sec`, 5 s) refreshes the header and the visible page only.

| Page | Covers | Sources / cost |
| --- | --- | --- |
| Header | poller state, B1/B2/B3 SOC, log age, clock | soc JSON, sysfs, `/proc` |
| Energy, Weather, System, NPU, AI log, Poller/services, Cameras, Controls | unchanged from the 12:15 build (see §2 of the testing record `2026-09-29-control-panel-gtk.md`) | existing JSON / log files |
| **Running** (new) | poller PID + its child jobs (tree) with listening ports; RootRecord processes (masked command lines); all local TCP listeners; tunnels (cloudflared, ssh -L/-R/-D, wg/tun interfaces); Ollama (version + loaded models via `GET /api/version`, `/api/ps` on 127.0.0.1) and FLM (pids, :52625, lock); systemd **user** units (all 108 loaded; RootRecord ones as rows) and **system** units (52 running); user/system timers; user crontab (masked) + `/etc/cron.*` names. Read-only, no actions; every row has **Settings →** to the matching Settings sub-page | `/proc`, `/proc/net/tcp*`, fd→socket inodes, `systemctl list-units/list-timers` + `crontab -l` cached 15 s; ~20–30 ms CPU per refresh |
| **Network** (new) | per-interface rx/tx rate (delta between refreshes), totals + packets/errors/drops since boot, state/kind/speed; **Starlink**: state, uptime, PoP latency + drop, throughput, obstruction, alerts, software version | `/proc/net/dev` + sysfs; Starlink via `Starlink/starlink_status.py` (see §4) |
| **SSH** (new) | `rr-aws` (Cloudflare Access hostname) and `rr-aws-ip` (direct IP) from `~/.ssh/config`: alias, user@host:port, ProxyCommand present / binary present, identity configured (paths and keys never read). Buttons: **Open terminal** (ptyxis → `ssh <alias>`) and **Status (uptime)** = `timeout 5 ssh -o BatchMode=yes -o ConnectTimeout=5 <alias> uptime`, once per press. **Mainland** = placeholder (no Host alias exists; set `ssh_mainland_alias`) | `~/.ssh/config` read at page build |
| **AWS Fallback** (new 2026-09-29 15:05) | 18 AWS fallback functions (catalog `Lib/rr_aws_fallback.json`) with RAM/disk/network/fits/default and an `AWS: On/Off` button each; budget box vs floors (≥ 512 MB RAM, ≥ 1.5 GB disk) for t3.micro, 2 GB and measured; **Status** = one read-only SSH to `aws_fallback_alias`; toggle → confirm dialog; `aws_fallback_mode` `dry-run` (code default, writes nothing) / `write` (**desk `settings.json` = `write` since 2026-09-29 16:05 HST**, after the Phase 2 runtime deploy; round-trip [tested](../07-testing/2026-09-29-aws-fallback-phase2-runtime-deploy.md); dated `bin.bak-fallback-flags-*` backup, then atomic `flags/<id>`; refuses if the runtime isn't deployed). Built on visit, released on leave. [Proposal](../08-ideas/2026-09-29-aws-fallback-rebuild.md) · [test](../07-testing/2026-09-29-root-monitor-aws-fallback-page.md) | `rr_aws_page.py`, `Lib/rr_aws_fallback.py`; +4.4 MB RSS (`--check`) |
| **Not migrated** | 16 open placeholders (7 BLOCKED, 9 VERIFY PENDING) as of 2026-09-30 02:35 HST. Closed work orders were removed from this list. | `Apps/Control-Panel/Lib/rr_migration.json` |
| **Settings** (hub) | 10 sub-pages: Network, Messaging, Environment (.env), Feature Flags (RR_*), Services/Poller, Weather, Voice, AI/NPU, Cameras, Panel (the panel's own settings.json: refresh, paths, camera toggles, Known URLs, risky-action safety, Starlink poll, Mainland alias) | `Lib/rr_registry.py` + `Lib/rr_config_io.py` |

Not-migrated items: Telegram council replies (BLOCKED), Discord bot (BLOCKED, WO-COM-002), Slack/comms surface, Security timelapse, Energy actuating actions, FLM own-session fix, Reports roll-up, Weekly archive, Geology, Weather retention apply, Public status board, Public site + website sync (BLOCKED), US-Mainland-Server (BLOCKED), Cloudflare credential recovery (BLOCKED), G1 recovery packets (BLOCKED), G2 residual paths (all KEPT), Residual jobs rewire (BLOCKED), Poller observability, GitHub pull authority, Database boundary, Agent context home, Repo map, WO generator (BLOCKED).

### On/off buttons (2026-09-29 16:15 HST)

**On/off controls are buttons (2026-09-29 16:15 HST).** There are no switches. Each on/off setting is a labelled toggle button, for example `Camera viewer: Off` (red outline) or `Camera viewer: On` (green), from `rr_ui.state_toggle`. The **camera viewer button** is the first row of the **Cameras** page and the first row of **Settings → Panel** (Cameras group first). The two stay in sync. It is Off by default. A click changes the running panel only; **Save settings** keeps it. Risky actions still need the confirm dialog. AWS Fallback rows (`AWS: On/Off`) keep confirm, dry-run revert and failed-write revert. Test: `Tests/test_toggle_buttons.py` (30 checks, AWS ssh stubbed) · [record](../07-testing/2026-09-29-root-monitor-toggle-buttons.md).

Why the camera toggle couldn't be seen before: the Cameras page had no control, its hint pointed at Settings → *Cameras* (the camera config-file page), and the real `Adw.SwitchRow` sat in the third group of Settings → Panel, below the fold of a nested scroller.

## 3. Settings registry (every setting)

`Lib/rr_registry.py` lists 27 config sources. For each setting it records file, key, type, secret?, service, restart needed, editable? (+ reason). Counts on 2026-09-29 13:05 HST — **1,590 settings**:

| Page | Settings | Editable | Secret (masked) |
| --- | ---: | ---: | ---: |
| Network | 80 | 11 | 12 |
| Messaging | 41 | 30 | 11 |
| Environment (.env) | 38 | 23 | 26 |
| Feature Flags (RR_*) | 47 | 46* | 1 |
| Services / Poller | 170 | 95 | 2 |
| Weather | 551 | 93 | 0 |
| Voice | 139 | 0 | 1 |
| AI / NPU | 483 | 436 | 7 |
| Cameras | 16 | 7 | 7 |
| Panel | 25 | via Panel controls | 0 |

\* RR_* flags are written to the poller drop-in `~/.config/systemd/user/rr-rootserver-poller.service.d/rr-flags.conf`. That file does **not** exist yet, so the editor refuses and says creating it is a sign-off item.

**Editable files** (env / ini / json / yaml / tsv / raw): `~/.cloudflared/rootserver.token` (secret file), `Communications/telegram/config/relay.conf`, `voices.conf`, `~/master/master-key.env` (secret file), `Github/scripts/repos.conf`, user units `rr-rootserver-poller.service` (+ `logging.conf` drop-in), `ava-ecoflow-ble.service`, `network-globe-hawaii.service`, `Energy/config/devices.conf`, `Weather/config/{hosts,tiers,resources,counties,report_counties,text_cleaning}.yaml`, `System/config/specialist-routes.json`, `Security/Cameras/store/CONNECTION.json` (secret file).

**Read-only:** `cf-status.json` / `cf-blocker.json` (tooling snapshots), `~/.config/gh/hosts.yml` + `config.yml` (managed by `gh`), `/etc/systemd/system/ollama.service` (needs sudo), `jobs.py` (code; job table shown), `weather-retention.py` constants (code), Kokoro model `config.json`, env-var references from scripts (default + where set), NetworkManager connections (`nmcli`, secrets never read), listening ports, structural unit keys (ExecStart, …), duplicate keys, lists/objects, and every secret-looking key inside a git-tracked file.

**Secrets:** detected by key name (TOKEN, KEY, SECRET, PASS, PAT, WEBHOOK, AUTH, COOKIE, ACCESS) and by secret files (`CONNECTION.json`, `master-key.env`, the tunnel token). Values are shown only as `set (len N)` / `empty`. Replace uses a PasswordEntry; Clear sets empty; both go through the masked diff + confirm. Values that equal a secret held in another file are masked everywhere too (display, diffs, Running command lines), and a redaction pass runs over every rendered row. Command lines also mask `--token`-style arguments and long opaque strings. The private-archive and model-drafts paths are shown as `<excluded path>` if another tool names them.

**Each save:** masked unified diff → confirm dialog stating "takes effect after <service> restart" → backup to `/home/rootrecord/Database/GITHUB/control-panel-settings-backups/` (dir 0700; file 0600 for secrets, else the original mode) → atomic write (temp file in the same dir, fsync, chmod/chown to the original, `os.replace`). Refuses if the file changed since the diff. Comments, key order and formatting are kept (JSON edits replace only the value token). Validation: port 1–65535, bool01 0/1, int, float, URL (http/https/rtsp/ws), host. **Nothing is ever restarted.** No real setting was saved during testing.

**Security items** (secret-looking keys or secret-equal values in git-tracked files — names only, never written from the panel):

1. `Communications/network/cloudflare/config/cf-status.json` → `auth_source`
2. `…/cf-status.json` → `account_id` (equals an entry of `master-key.env`)
3. `…/cf-blocker.json` → `findings.CLOUDFLARE_API_TOKEN`
4. `…/cf-blocker.json` → `findings.global_key_account`
5. `…/cf-blocker.json` → `findings.origin_tunnel_account` (equals an entry of `master-key.env`)
6. `Communications/telegram/config/relay.conf` → `SECRETS_1` (file-path reference, not a credential)
7. `…/relay.conf` → `SECRETS_2` (file-path reference, not a credential)

## 4. Starlink

The dish answers gRPC at `192.168.100.1:9200` (reachable 12:45 HST). No Starlink tooling existed in the repos (only keyword mentions in specialist configs). Installed without sudo: `Apps/Control-Panel/Starlink/.venv` (uv, Python 3.12; `starlink-grpc-core` 1.2.5, grpcio 1.84.0, protobuf, yagrc; `.venv/` is gitignored). The PyPI name `starlink-grpc-tools` does not exist; `starlink-grpc-core` is its published module.

`Starlink/starlink_status.py` calls **only** `status_data` (get_status; never reboot/stow/config) and prints one JSON line per poll (dish id/serial are not forwarded). Root Monitor starts it with `--loop 10` (minimum 10 s, `starlink_poll_sec`) **only while the Network page is visible** and kills it on leave or window close. One-shot cost: 55.7 MB RSS in its own process, 0.43 s CPU, ~180–260 ms RPC.

## 5. Launch

- **Login (applied 2026-09-30 02:33 HST):** `~/.config/autostart/root-monitor.desktop`. The old terminal autostart is in `~/.config/autostart/.root-monitor-swap/`. `Packaging/swap-default-viewer.sh revert` puts it back.
- **App menu:** "Root Monitor". The terminal dashboard stays as "Poller Dashboard (terminal)".
- **Stack reload:** `do-stack-reload.sh` opens `Packaging/open-root-monitor.sh`. That script does not start the poller. `OPEN_POLLER_WINDOW=0` skips the window.
- **Terminal:** `python3 ".../Apps/Control-Panel/rr_control_panel.py"`.
- **Test:** `--check [--camera-viewer on|off] [--no-starlink]`, `Tests/run-check.sh <outdir>`, `Tests/test_settings_io.py`, `--screenshot DIR`, `--run-for SEC`.

## 6. Measured resources (2026-09-29 13:02–13:08 HST, nice 10, MemAvailable ≥ 7.2 GB)

| Mode | Peak RSS | CPU |
| --- | --- | --- |
| `--check`, viewer off (every page + every Settings / placeholder sub-page built once, all data loaded) | **84.5 MB — over the 80 MB target by 4.5 MB** (73.8 MB before this pass) | 1.1 s user + 0.1 s sys |
| `--check`, viewer on | 98.9 MB (opt-in) | 1.3 s |
| Window 25 s (Energy start page, cairo) | 85.7 MB | 0.52 + 0.07 s |
| Screenshot mode (24 pages rendered to textures) | 127.3 MB | 5.4 s |
| Starlink helper (own process, only while Network visible) | 55.7 MB | 0.43 s per poll incl. start |

2026-09-30 02:33 HST: every settings row is built (the 12-row cap is gone). Editable `bool01` rows are labelled toggles. `--check` peak RSS 89.8 MB. Sub-pages are still built on visit and released on leave.

## 7. Sign-off items (Alexander)

1. **Default viewer swap:** **done** 2026-09-30 02:33 HST. Revert with `Packaging/swap-default-viewer.sh revert`. Do not also enable the user unit.
2. **systemd --user unit:** still not installed. Leave it off while the autostart desktop is in place.
3. **Conky:** installed, config copied, **not started**.
4. **RSS:** `--check` 89.8 MB on 2026-09-30 02:33 HST, over the 80 MB target.
5. **RR_* flags:** a confirmed toggle creates `rr-flags.conf` if it is missing. Nothing is restarted. The new value is used the next time the poller starts.
6. **SSH:** `rr-aws` ProxyCommand points at `~/.local/bin/cloudflared`, which does not exist (the tunnel binary is Pacific `Communications/network/cloudflare/bin/cloudflared`); `rr-aws-ip` timed out after 5 s. Fix `~/.ssh/config` / the AWS side yourself. Mainland: add a Host block and set `ssh_mainland_alias`.
7. **Security items** in §3: review the cloudflare snapshot files (git-tracked) and decide whether those fields should leave git.
8. Risky actions: `risky_actions_enabled` + per-action `signed_off` (unchanged rule).
9. System-level settings (NetworkManager, `/etc/systemd/system/ollama.service`) stay read-only (need sudo).

## 8. Files

- **Pacific** `Apps/Control-Panel/`: `rr_control_panel.py`, `rr_pages.py` (new pages + Settings hub), `rr_ui.py` (shared widgets, redaction), `Lib/rr_sources.py`, `Lib/rr_settings.py`, `Lib/rr_registry.py`, `Lib/rr_config_io.py`, `Lib/rr_running.py`, `Lib/rr_netstat.py`, `Lib/rr_ssh.py`, `Lib/rr_migration.json`, `rr_aws_page.py`, `Lib/rr_aws_fallback.py`, `Lib/rr_aws_fallback.json`, `Starlink/starlink_status.py` (+ gitignored `.venv`), `settings.json`, `Conky/`, `Packaging/` (`rootrecord-control-panel.desktop` = Root Monitor, `poller-dashboard-terminal.desktop`, `root-monitor-autostart.desktop`, `swap-default-viewer.sh`, `rootrecord-control-panel.service`, `install-launcher.sh`), `Tests/run-check.sh`, `Tests/test_settings_io.py`, `README.md`.
- **Test records:** [../07-testing/2026-09-29-control-panel-gtk.md](../07-testing/2026-09-29-control-panel-gtk.md) · [../07-testing/2026-09-29-root-monitor-settings-running-network-ssh.md](../07-testing/2026-09-29-root-monitor-settings-running-network-ssh.md) · [../07-testing/2026-09-29-root-monitor-aws-fallback-page.md](../07-testing/2026-09-29-root-monitor-aws-fallback-page.md)
