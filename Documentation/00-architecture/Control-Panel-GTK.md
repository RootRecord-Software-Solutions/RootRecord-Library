# Control Panel (GTK4) + Conky readout — architecture

*Added 2026-09-29 ~12:15 HST. Status: **LANDED**. `--check` PASS, real-window render PASS. Conky and autostart are **VERIFY PENDING** (not installed / not enabled).*

## 1. What it is

A native, read-only Linux desk app for the RootRecord Pacific Solar Server. It is Python + PyGObject with **GTK 4.22.4 + libadwaita 1.9** (system `python3`, no venv) and does not use a browser, Chromium or Electron. There is also a Conky config for an always-visible readout.

It is **added alongside** the existing displays and replaces none of them:

| Existing display (unchanged) | Where | What it shows | Reads / how often |
| --- | --- | --- | --- |
| `poller-dashboard.py` (default viewer, opened by `open-poller-window.sh`, autostart `~/.config/autostart/rootrecord-poller-watch.desktop`, Desktop `RootRecord-Poller-Window.desktop`) | Pacific `Automations/scripts/poller/` | header + HST clock, refresh countdown, 8 service rows (poller, relay, BLE, globe, cam, weather, ollama, tunnel) PASS/WARN/FAIL, **B1 river2pro / B2 delta2 / B3 System (laptop) battery bars** + SUMMARY lines, SYS line, SUN (solar state), recent poller log | `Energy/soc/{river2pro,delta2}-last.json`, `/sys/class/power_supply/BAT*`, last 64 KB of `Logs/Automations/automations_current.log`, `/proc/*/cmdline`, `systemctl is-active` ×4, NOAA `solar_calculation_table_current.md` — snapshot every **5 s** (`POLLER_DASH_REFRESH`), redraw every 1 s |
| `poller-watch.py` (Bruce's scrolling viewer, `POLLER_VIEWER=poller-watch.py`) | same | banner (public/local URL, systemd state), colour-formatted live log | tails `automations_current.log` (0.25 s poll), `systemctl --user is-active` once |
| Poller **status line** (ENERGY heartbeat) | `rootserver_poller.py` `_energy_log_line()`; served at `http://127.0.0.1:8799/` (`/health`) | `ENERGY status= B2= B1= [B3=] solar= ac= usbc= src= [LAP=]` | SQLite board + `Energy/soc|watts/*-last.json` + sysfs; heartbeat job every **60 s** |
| `npu-status.sh` | Pacific `System/scripts/plumbing/` | `/dev/accel`, xrt/npu dpkg packages, single-flight lock, FLM on-demand state | on demand |

The data the panel reads is produced by these poller jobs: `sys_stats_cycle` every 5 s, `ecoflow_read_cycle` every 15 s, `security_camera_frame_grab` every 1 s, and `heartbeat` every 60 s.

## 2. Pages and data sources

All sources are read-only. There are no writes, no sqlite and no network, except the optional localhost camera fallback.

| Page | Covers | Sources |
| --- | --- | --- |
| Header (always) | poller state, B1/B2/B3 SOC, log age, clock | soc JSON, sysfs, `/proc`, log mtime |
| Energy | the 3 dashboard bars (B1, B2, B3 laptop), watts per device (solar in, AC out/in, USB-C, charge source, source, time), the verbatim ENERGY status line, the Delta2 expansion B3 and `LAP=` when present, SUMMARY lines, SUN | `Energy/soc/*`, `Energy/watts/*`, sysfs, log tail, solar table (via `poller-watch.aeyes_solar_state`, import only) |
| Weather | sun state, ZFP Today/Tonight + advisories for a configurable zone | `zfp_zone_forecast_current.md` (cached by mtime), state report header |
| System | CPU / RAM bars, load 1/5/15, 5-min averages, SYSTEM line | `System/last/host-last.json`, `System/status/system-status.json` |
| NPU | accel, FLM on-demand state, lock; button runs `npu-status.sh` at nice 10 | `/dev/accel`, `/proc`, `/proc/net/tcp`, `Github/plumbing/state/holder.txt` |
| AI log | inference count/today/routes/models/callers/latency/fallbacks/exits, routing rows, report head | `Logs/AI/Inference/inference_current.jsonl` (cached by size+mtime), `Logs/AI/Routing/routing_current.jsonl`, `Logs/AI/Reports/ai-processing-report_current.md` |
| Poller / services | the dashboard's 8 service rows (same rule) + MainPID, log age, recent formatted log | `/proc`, `systemctl [--user] show` (2 calls), log tail |
| Cameras | latest still per enabled camera | `Database/Media/Images/chN-*.jpg` (listing + ≤1 JPEG per camera) |
| Controls | safe actions, risky actions (sign-off), gated `RR_*` jobs list | `jobs.py` text scan |
| Settings | every setting, Known URLs, camera toggles | `Apps/Control-Panel/settings.json` |

**Not covered, or covered differently:**

- The dashboard's 1 s "refresh in N s" countdown is replaced by one 5 s refresh.
- `poller-watch.py`'s Ctrl-C stack-stop is intentionally **not** reproduced (the panel never stops anything).
- `npu-status.sh`'s dpkg package list appears only when the script is run from the NPU page.
- The SUN value is currently empty in **both** the dashboard and the panel, because today's date row is not found in `solar_calculation_table_current.md` (the collected page looks like the NOAA HTML shell). That is an existing data issue and was not changed.

## 3. Runtime model

- **One GLib timeout** (`refresh_sec`, default 5 s). Each tick refreshes the header and **the visible page only**. There are no busy loops and no threads, except one short-lived fetch thread for the camera fallback.
- Pages are **built on first visit** in the window to save memory. `--check` builds them all.
- **Camera viewer:** `camera_viewer_enabled` is false by default.
  - **When off:** no timer, no directory scan, no image load, no stream. strace-verified: 0 syscalls under `Media/Images` and 0 connects to :8791.
  - **When on:** a separate 10 s timer, added only while the Cameras page is visible and removed on leave or turn-off. Textures are dropped when you leave.
  - Stills are decoded to at most 640×360. A still younger than 1.5 s is skipped, because it may still be being written.
  - The localhost still fallback runs only if a camera has no still on disk.
  - Missing or flapping stills (camera hardware work) are expected and shown as "no still on disk".
- **Renderer:** `GSK_RENDERER=cairo` by default (`gsk_renderer` in settings). The environment variable overrides it.
- **Single instance:** app id `cloud.rootrecord.ControlPanel`.

## 4. Launch

- **App menu:** "RootRecord Control Panel" (`~/.local/share/applications/rootrecord-control-panel.desktop`).
- **Terminal:** `python3 ".../1 - RootRecord-Pacific-Solar-Server/Apps/Control-Panel/rr_control_panel.py"`
- **Test:** `--check [--camera-viewer on|off]`, `Tests/run-check.sh <outdir>`, `--screenshot DIR`, `--run-for SEC`.

## 5. Measured resources (2026-09-29)

| Mode | Peak RSS |
| --- | --- |
| `--check`, viewer off | 73.8 MB — **PASS** (< 80 MB target) |
| `--check`, viewer on | 87.8 MB (opt-in) |
| Window 30 s (cairo) | 85.0 MB, 0.58 s CPU incl. startup (an empty GTK4/Adw window is 66–68 MB on this desk) |
| Window, default GL renderer | ~180 MB |
| Window, gl renderer | ~275 MB |

## 6. Sign-off items (Alexander)

1. `sudo apt install conky-all` (conky is not installed). Then run `Packaging/install-launcher.sh` to copy the config, and start it with `conky -c ~/.config/conky/rootrecord.conkyrc`. Autostarting conky is a separate yes/no.
2. Enable autostart: copy `Packaging/rootrecord-control-panel.service` to `~/.config/systemd/user/`, then run `systemctl --user daemon-reload && systemctl --user enable --now rootrecord-control-panel.service`.
3. Risky actions: setting `risky_actions_enabled: true` and marking individual actions `signed_off: true` (poller restart). Telegram send, voice send and `RR_*` flag enabling also need a signed-off command before they can be wired.
4. Accept or reject the window RSS of ~85 MB against the 80 MB target. If rejected, the options are fewer pages or a lighter toolkit.

## 7. Files

- **Pacific** `Apps/Control-Panel/`: `rr_control_panel.py`, `Lib/rr_sources.py`, `Lib/rr_settings.py`, `settings.json`, `Conky/rootrecord.conkyrc`, `Conky/conky_readout.py`, `Packaging/rootrecord-control-panel.desktop`, `Packaging/rootrecord-control-panel.service`, `Packaging/install-launcher.sh`, `Tests/run-check.sh`, `README.md`.
- **Test record:** [../07-testing/2026-09-29-control-panel-gtk.md](../07-testing/2026-09-29-control-panel-gtk.md)
