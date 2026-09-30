# Test record: Root Monitor — switches replaced by labelled buttons; camera viewer button made visible

| Field | Value |
| --- | --- |
| **Date / time (HST)** | 2026-09-29 16:07–16:20 HST |
| **Tester** | Grok (executor) for Alexander Storey |
| **Request** | "make toggles buttons. I can't see the camera toggle." |
| **Change under test** | Pacific `Apps/Control-Panel`: `rr_ui.py` (new `state_toggle` + `TOGGLE_CSS`), `rr_control_panel.py` (Cameras page button, Settings → Panel camera group moved first, all switch rows → buttons, risky confirm kept), `rr_aws_page.py` (minimal: `Gtk.Switch` → `state_toggle`, same confirm / dry-run / revert logic), new `Tests/test_toggle_buttons.py`, `Tests/run-check.sh` runs it. `settings.json`, `Lib/rr_aws_fallback*` and `jobs.py` were **not** edited |
| **State** | **PASS** |
| **Evidence** | `/home/rootrecord/RootRecord-Ecosystem/test-reports/Control-Panel/toggle-buttons-20260929-161253/` (4 PNGs, `check/` logs, `screenshot-run.log`, `shot-driver.py`) |
| **Backup** | `/home/rootrecord/Database/GITHUB/2026-09-29_160737_control-panel-toggle-buttons-backup/` (whole Control-Panel dir + launcher + these docs before editing) |
| **Commits** | desk auto-sync (no manual git writes) |

## Cause of the missing camera toggle

1. The **Cameras page had no control at all**: only a dim label saying "Turn it on in Settings → Cameras".
2. That pointer was **wrong**: Settings → *Cameras* is the registry page for camera config files (CONNECTION.json, master-key.env). The real toggle was an `Adw.SwitchRow` in Settings → **Panel**.
3. On Settings → Panel it was in the **third group, below the fold** (after 9 General rows + Paths), inside an `Adw.PreferencesPage` that scrolls on its own inside two outer ScrolledWindows. At the default 1100×760 window it was off-screen (see the 13:06 screenshot `20260929-130606-24-settings-panel.png`, which ends at "Mainland SSH Host alias").

## Fix

- New `rr_ui.state_toggle(name, active, on_change)` → a `Gtk.ToggleButton` that reads "\<name\>: On" (green fill) or "\<name\>: Off" (red outline); `btn.rr_set(v)` changes state without firing the callback (used for reverts / status reads).
- **Cameras page**: big "Camera viewer: Off" button as the first row, plus a corrected hint. **Settings → Panel**: the Cameras group is now first, and its first row is the same button. Both stay in sync; `--camera-viewer` overrides repaint them. Default stays **Off**; clicks change memory only, **Save settings** persists (as before).
- Every other switch → button: Starlink, Still fallback, Show ch1–ch4, Risky actions (confirm dialog kept; cancel or no window = stays Off), AWS Fallback rows ("AWS: On/Off"; confirm, dry-run revert, failed-write revert, status repaint unchanged).
- No `Gtk.Switch` / `Adw.SwitchRow` remains (test walks 1,408 widgets).

## Results

| Check | Result |
| --- | --- |
| `Tests/run-check.sh` | `--check` viewer OFF and ON: **RESULT PASS, 0 errors, 0 leaks** (34 secret values vs ~450 k chars). strace viewer OFF: **0** Media/Images syscalls, **0** connects to :8791 |
| `test_settings_io.py` | **103/103** |
| `test_toggle_buttons.py` (new) | **30/30**. AWS `spawn` is stubbed for the whole run: **no ssh started, nothing written on AWS**; desk `settings.json` md5 unchanged |
| `rr_aws_fallback` unit checks | **12/12**, re-created inline (load, defaults, budget, 4 bad ids rejected, backup before write, exit 3 if not deployed, status read-only, parse_status). The original 13-check heredoc was not saved, so this is not the identical set |
| Memory (`--check`, before vs after, same session) | viewer OFF 85.5–85.8 → **85.2–85.4 MB**; viewer ON 100.2–100.8 → 100.7–100.8 MB. **No growth** |
| Screenshots (separate NON_UNIQUE instance, nice 10, secret guard PASS on all) | `20260929-161357-01-cameras-viewer-off.png`, `-02-cameras-viewer-on.png`, `-03-settings-panel-buttons.png`, `-04-aws-fallback-buttons.png` |
| Cleanup | Test instance exited by itself; Alexander's own instance (PID 3221324) was left running and untouched; `settings.json` unchanged |

## Verdict

**PASS.** Alexander's open window (started before 16:10) still runs the old code. **Close and reopen Root Monitor** to get the buttons.
