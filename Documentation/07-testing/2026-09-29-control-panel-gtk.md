# Test record — Control Panel (GTK4 + libadwaita) and Conky readout

| Field | Value |
| --- | --- |
| **Date / time (HST)** | 2026-09-29 11:53–12:16 HST |
| **Tester** | Grok Bot (executor agent) on Alexander Storey's desk |
| **Change under test** | New read-only panel at Pacific `Apps/Control-Panel/` ([architecture](../00-architecture/Control-Panel-GTK.md)), plus the Conky config, `.desktop` launcher and systemd --user unit (not enabled) |
| **State** | **PASS** (`--check` both modes, strace camera-off proof, real-window render of all pages). **VERIFY PENDING**: Conky (not installed) and the autostart unit (not enabled). Window RSS 85 MB is over the 80 MB target (flagged) |
| **Evidence** | `RootRecord-Ecosystem/test-reports/Control-Panel/` (check output, time -v, strace, screenshots) |
| **Commits** | auto-sync; see the worklog section (read-only `git log`) |
| **Backup** | `/home/rootrecord/Database/GITHUB/control-panel.bak-20260929-115632/` (07-testing README, worklog, copies + sha256 of every existing viewer file) |

## What was tested
1. The toolkit on system `python3` 3.14.4:
   - `gi` 3.56.2
   - Gtk 4.0 = 4.22.4, Adw 1 = 1.9
   - GdkPixbuf 2.44.5
   - conky: **not installed**
   - xvfb: not installed (not needed)
2. `--check`: builds all 9 pages, loads every data source once and exits without a window. Run with the camera viewer off and on.
3. With the viewer **off**, no camera file or stream is touched.
4. The real window opens, every page renders, and the window closes (Alexander was away; permitted by him).
5. The existing displays are unchanged.

## How
```bash
cd ".../1 - RootRecord-Pacific-Solar-Server/Apps/Control-Panel"
bash Tests/run-check.sh ~/RootRecord-Ecosystem/test-reports/Control-Panel/check-20260929-120905
#   -> nice 10; MemAvailable guard (>= 2 GB); /usr/bin/time -v; strace -f -e openat,open,getdents64,connect
nice -n 10 python3 rr_control_panel.py --run-for 30          # real window, 30 s, then quits
nice -n 10 python3 rr_control_panel.py --screenshot ~/RootRecord-Ecosystem/test-reports/Control-Panel
sha256sum -c control-panel.bak-20260929-115632/existing-viewers.sha256 (against the live files)
```

## Pass criteria (written before running)
1. `--check` exits 0 with `errors: 0` in both camera modes.
2. Viewer OFF: camera counters are all 0, strace shows 0 syscalls under `Media/Images` and 0 connects to `:8791`, and `store/CONNECTION.json` is never opened.
3. `--check` (default settings) peak RSS is under 80 MB.
4. Every page renders in a real window; the window closes and no panel process is left.
5. The sha256 of every existing viewer, dashboard and script is unchanged, and the poller PID 105444 is unchanged.

## Result
**`--check`, camera viewer off (12:09):**
- `errors: 0`, **RESULT: PASS**.
- Peak RSS **73.8 MB** (time -v 76,676 KB); CPU 0.35 s user + 0.05 s sys.
- Camera stats: dir scans 0, files opened 0, http fetches 0.
- strace: **Media/Images syscalls 0, connects to :8791 0, CONNECTION.json opens 0**.
- The only file read under `Security/Cameras` was `grab_all.sh` (camera discovery).

**`--check`, camera viewer on:**
- PASS: 4/4 stills loaded, 1 directory scan, 0 http fetches.
- Peak RSS 87.8 MB (time -v 89,880 KB).

**Data read at 12:03–12:09:**
- B1 river2pro 31.3 %, B2 delta2 31.3–31.8 %, B3 laptop 100 % → 94 % "Discharging".
- All 8 services PASS; NPU IDLE (on demand), lock IDLE, accel0 present.
- AI log: 10 requests, all npu-flm; 10 gated RR_* jobs listed (default OFF); 0 risky buttons clickable.

**Real window (cairo renderer):**
- 30 s run: peak RSS **85.0 MB**, CPU 0.50 + 0.08 s, camera stats all 0.
- For comparison: the default renderer took ~180 MB and GSK_RENDERER=gl 275 MB, which is why the panel defaults to cairo. An empty GTK4/Adw window alone is 66–68 MB on this desk.

**Screenshot run 12:09:24:**
- 10 PNGs saved, `pgrep rr_control_panel` = none afterwards.
- Screenshot mode peaks at 111.6 MB, because of render-to-texture captures.
- ch3 and ch4 stills were black frames (camera hardware work in progress; expected).

**Existing files:** sha256 unchanged for all 10 files, and the poller MainPID is still 105444 (see the worklog).

| Page | Screenshot (`RootRecord-Ecosystem/test-reports/Control-Panel/`) |
| --- | --- |
| Energy | `20260929-120924-01-energy.png` |
| Weather | `20260929-120924-02-weather.png` |
| System | `20260929-120924-03-system.png` |
| NPU | `20260929-120924-04-npu.png` |
| AI log | `20260929-120924-05-ai.png` |
| Poller / services | `20260929-120924-06-poller.png` |
| Controls | `20260929-120924-07-controls.png` |
| Settings | `20260929-120924-08-settings.png` |
| Cameras (viewer off) | `20260929-120924-09-cameras-viewer-off.png` |
| Cameras (viewer on) | `20260929-120924-10-cameras-viewer-on.png` |

The earlier pre-fix run (12:04:32) is in `Pre-Fix-Run-120432/`.

## Resource impact
| When | Load (1/5/15) | MemAvailable | Swap used | Peak RSS |
| --- | --- | --- | --- | --- |
| before (11:53) | 1.26 / 1.19 / 1.03 | 7596 MB | 550 MB | — |
| during (12:03–12:10) | ~2 | ≥ 7750 MB | 550 MB | 73.8 / 87.8 MB check; 85.0 MB window |
| after (12:11) | 2.34 / 2.10 / 1.68 | 7794 MB | 550 MB | — |

## Cleanup confirmation
- [x] No test process left (`pgrep -af rr_control_panel|conky_readout|strace` = none).
- [x] No port opened by the panel; lock IDLE.
- [x] No model loaded (`ollama ps` empty; no `flm serve`).
- [x] Poller not restarted (PID 105444, ActiveState active). No sudo, apt, sends, speaker playback or git writes.

## Open items / caveats
- The Conky config has not been run (conky not installed); it is **VERIFY PENDING** after `sudo apt install conky-all`.
- The systemd --user unit is written, not installed or enabled (sign-off).
- Window RSS of 85 MB is over the 80 MB target; the viewer-on `--check` is 88 MB.
- SUN is empty in both the dashboard and the panel: today's row is missing from `solar_calculation_table_current.md` (existing data issue).
