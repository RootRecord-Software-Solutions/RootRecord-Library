# Desk automations and public service windows

Written 1 October 2026, 01:40 HST, from the Pacific files named below. Clocks are Hawaii time (`Pacific/Honolulu`, HST, UTC−10, no DST).

Nothing in this page starts the poller, sends a message, spends money, or turns a job on.

The Root Monitor **Automations** page and **Telemetry** page write job overrides, power schedules, optional data-poll intent, and service-window files. The poller reads the first three families. The public site reads the service-window file.

## 1. Who writes, who runs

| Piece | Path | Writes | Runs |
| --- | --- | --- | --- |
| Job on/off | `Automations/scripts/automation_control.py` | `2 - RootRecord-Database/System/control-panel/automation-overrides.json` | The poller, on its next cycle after the file mtime changes |
| Power schedules | same module | `2 - RootRecord-Database/System/control-panel/power-automations.json` | The poller, on the minute the clock is due |
| Automations page | `Apps/Control-Panel/rr_automations_page.py` (+ `Lib/rr_data_poll.py`) | Those two JSON files, and (write mode) panel intent / optional `data_poll_mode.yaml`, after confirm | The page does not run a radio command and does not restart the poller |
| Data-poll toggle | `Apps/Control-Panel/Lib/rr_data_poll.py` (+ `rr_settings.py`, `rr_automations_page.py`) | Panel settings keys + optional Database `System/control-panel/data_poll_mode.yaml`; optional drop-in `rr-data-poll.conf` if `data_poll_apply_dropin`; optional poller restart / ML2 sync if `data_poll_restart_poller` / `data_poll_sync_ml2` | Poller honors env `RR_LOCAL_DATA_POLL`; Live label binds to poller env (not panel env) after ~03:14; defaults dry-run / desired=local / apply_dropin=false |
| Service windows | `Automations/scripts/service_notice.py` | `Website/Home/service-notice.json` | The poller takes one network snapshot when a window becomes active |
| Telemetry page | `Apps/Control-Panel/rr_telemetry_page.py` | That website file, after confirm | The page does not restart the poller |
| Public banner | `Website/Home/assets/service-banner.js` | Session dismiss only (`sessionStorage` key `rr-service-dismissed`) | Reads `/service-notice.json` |
| Live network panel | `Website/Home/assets/live.js` plus `telemetry.js` | Nothing | Same file. During an active window it shows the stored counts |

Database `.gitignore` ignores the whole `/System/control-panel/` directory. Those two JSON files stay on the desk. `Website/Home/service-notice.json` is in the site folder the website mirror publishes. An empty `"windows": []` is the idle file.

Tests point at copies with `RR_AUTOMATION_OVERRIDES`, `RR_POWER_AUTOMATIONS`, `RR_ECOFLOW_ACTIONS`, `RR_SERVICE_NOTICE`, `RR_DATABASE_ROOT`, and `RR_PACIFIC_ROOT`. The test files are `Automations/scripts/test_automation_control.py` and `Automations/scripts/test_service_notice.py`.

## 2. Data poll — Local Pacific vs ML2 (GTK, 2026-10-02)

Toggle, not replacement. Home collectors stay in `jobs.py`. Pacific env `RR_LOCAL_DATA_POLL` (in `automation_control.py`) gates the internet data-poll job set: unset/`1` = Local Pacific ON (fail-safe default when unset); `0` = gate those jobs off while ML2 collectors + stream are healthy. **Exclusive (~03:08 HST):** ML2 on ⇒ Pacific local off; Pacific local on ⇒ ML2 pollers off. Soft kill-switch only (`RR_LOCAL_DATA_POLL`); never delete collectors. Mainland wiring ML2 side of the gate. EcoFlow/cams stay Pacific forever (outside this gate). Policy essay: [US-Mainland-Two.md](../15-Domains-and-External-Systems/US-Mainland-Two.md).

Root Monitor **Automations** (desk `Apps/Control-Panel/`) shows Local Pacific vs ML2 at the top of the page. Behavior mirrors AWS Fallback safety:

| Setting (Panel `settings.json`) | Code default | Meaning |
| --- | --- | --- |
| `data_poll_toggle_mode` | `dry-run` | Confirm shows the change; writes nothing that affects the live poller |
| `data_poll_desired` | `local` | Panel intent (`local` → env 1, `ml2` → 0). Intent YAML must not use inline `#` comments on the `mode:` line (broke `mode: remote` parse before ~03:14) |
| `data_poll_apply_dropin` | `false` | When true *and* mode is `write`, also writes `~/.config/systemd/user/rr-rootserver-poller.service.d/rr-data-poll.conf` |
| `data_poll_restart_poller` | (desk On after ~03:14) | When true *and* write mode, apply restarts the poller so DESIRED=LIVE |
| `data_poll_sync_ml2` | (desk On after ~03:14) | When true *and* write mode, sync ML2 side of the exclusive gate both ways |

Confirm before any write. Example config: Pacific `Automations/config/data_poll_mode.example.yaml`.

**Kill-switch fix (2026-10-02 ~03:14 HST):** `job_enabled()` in `Automations/scripts/automation_control.py` was reading panel env, so gated jobs looked On while poller already had `RR_LOCAL_DATA_POLL=0` (`live_raw=0`); apply without restart left DESIRED≠LIVE; intent YAML inline `#` comments broke `mode: remote`. Fixed in `automation_control.py`, `Apps/Control-Panel/Lib/rr_data_poll.py`, `rr_settings.py`, `rr_automations_page.py`, `rr_control_panel.py`, and Database `System/control-panel/settings.json`. UI: Automations → Data poll **Live=ML2 offload**; gated jobs Off with “ML2 owns”. Drop-in + restart + sync-ml2 apply **both directions**. Soft only — EcoFlow/cams ungated. Backups `/tmp/root-monitor-toggle-fix-bak/`; report `/tmp/root-monitor-toggle-fix/REPORT.md`. Optional later: Alexander confirm Settings keep `data_poll_restart_poller` + `data_poll_sync_ml2` On.

**Current overnight (2026-10-02 ~03:14 HST; left ML2-on):** `data_poll_desired=ml2`; drop-in `RR_LOCAL_DATA_POLL=0`; intent `mode=remote`; ML2 timers active; poller `:8799` live; verified both ways. Collectors remain installed; gate flipped only. First test real for geology + US weather + API only — not a full poller move ([US-Mainland-Two](../15-Domains-and-External-Systems/US-Mainland-Two.md)). Prior live flip ~02:50 / reboot-survived still the base.

**AWS Fallback page vs Automations data-poll (~03:04 / ~03:14 HST):** AWS Fallback stays on ML1 (`rr-aws-ip`); `/home/ubuntu/rootrecord/fallback` **restored**, Status bindable (`deployed=1`; press Status once). Earlier “unavailable” was secondary (tree restored earlier). Do not confuse with ML2 public API. Automations Local Pacific vs ML2 is the data-poll gate. Globe units on ML1 stay masked / flags forced off.

## 3. Job on/off


`jobs.py` still holds the code default (`enabled` true or false). A boolean under `automation-overrides.json` → `jobs` → `<job id>` wins over that default. `set_job_override` drops the key when the saved value matches the code default, so the file only stores differences.

The poller function `_job_on` calls `job_enabled`. If that call throws, the poller uses the `jobs.py` flag. `scheduler_loop` reloads the four repeating lists when `overrides_mtime()` changes. It does not restart itself to pick up a toggle.

The Automations page shows one button per job, grouped as on boot, once at start, every few seconds, every minute, every hour, and at a clock time. A click confirms, then writes. These job ids add an extra sentence in that confirm, because turning them off changes the next poller start or the status line:

| Job id | Extra sentence |
| --- | --- |
| `self_terminal` | Next poller start skips its own process record. |
| `cloudflare_tunnel` | Next poller start skips the Cloudflare tunnel. |
| `heartbeat` | The ENERGY status line stops after the poller reloads this flag. |
| `ecoflow_read_cycle` | Off in `jobs.py`. Repeating EcoFlow reads are user timer `rr-ecoflow-read.timer`, not this job. See `Documentation/01-Operations/2026-10-01-ecoflow-ble-reads.md`. |
| `service_supervisor` | Service checks stop after the poller reloads this flag. |

The page status line is `poller_control_state()`:

| State | Meaning on the page |
| --- | --- |
| `live` | This poller process started after `automation_control.py` and `rootserver_poller.py`. Toggles apply on the next cycle. A due power schedule runs in that minute. |
| `restart` | The process is older than those files. The JSON is saved. It takes effect after the poller process starts again. |
| `down` | No `rootserver_poller.py` process. The JSON is saved. Nothing fires until a poller starts. |

Root Monitor does not restart the poller from this page.

## 4. Power schedules

A schedule is one catalog function at one clock time, HST. Repeat is `daily` or `once`. A once-row needs a date `YYYY-MM-DD` that is still in the future. Names are at most 80 characters. A blank name becomes the device, the function, and the clock time.

The page can store a second step in the same confirm (for example AC off, then AC on later). Both rows share a `group` id `pg-…`. Each row still has its own clock.

The catalog is the only set of scripts `run_due` will start. `script_for` resolves the file under `Energy/scripts/actions/` and refuses any path whose parent is not that directory or whose name is not the catalog name. The script also has to already be a file.

| Device | Functions |
| --- | --- |
| Delta 2 | AC output, DC output, USB output, AC charging, energy backup, grid bypass — each off and on |
| River 2 Pro | AC output, DC 12V, X-Boost, energy backup, AC always-on — each off and on |

`run_due` is called from the poller (`_kick_power`) on a daemon thread named `power-automations`. A second kick in the same minute is skipped while that thread holds `_power_busy`, and the poller logs `power schedules still running`.

Due means all of these:

- The master switch `master_enabled` is true, and the row `enabled` is true.
- The clock is valid (hour 0–23, minute 0–59).
- Wall time is at or after that clock, and less than 15 minutes past it (`RETRY_MINUTES`).
- A `once` row's date is today.
- `last_status` is not already `ok` for today.
- `last_attempt` is not already this minute (`YYYY-MM-DDTHH:MM`).

The attempt stamp is written before the script runs, so the same minute cannot start twice. The script runs as `flock -w 90 /tmp/ecoflow-ble.lock bash <script>`, timeout 120 seconds. Exit 0 stores `last_status` `ok` and `last_fired`. A `once` row is then set `enabled` false. Any other exit stores `fail` and the last output line (300 characters). Failures stay eligible until the 15-minute window ends.

The master button pauses every schedule. It does not delete them and it does not run one now. Deleting a row removes it. It does not run it.

Log lines look like `power:delta2.ac-off OK …` or `power:… FAIL …`, prefixed with the poller timestamp.

## 5. Public service windows

`service-notice.json` is `{ "windows": [ … ] }`. Each window:

| Field | Meaning |
| --- | --- |
| `id` | `tw-` plus 8 hex characters |
| `enabled` | false is phase `off` and is not shown |
| `down_at`, `up_at` | ISO timestamps with seconds, Hawaii time |
| `note` | One public sentence, at most 160 characters. Empty is allowed |
| `frozen` | True after the outage snapshot has been taken |
| `last_known` | `at`, `hawaii`, `mainland`, `flows`, `endpoints` from `https://api.rootrecord.cloud/api/state` → `stats` (`hawaiiActiveFlows`, `localActiveFlows`, `activeFlows`, `endpoints`) |

`validate_window` requires the return time after the down time, and the return time still in the future. `add_window` also stores a last-known snapshot at the moment the window is saved. If that read fails, the time is kept and the four counts stay empty.

Phase, in both Python (`phase`) and the site (`telemetry.js` `noticePhase`):

| Phase | When |
| --- | --- |
| `upcoming` | Now is before `down_at`. The public page shows it only when the down time is inside 24 hours |
| `down` | Now is at or after `down_at` and before `up_at` |
| `ended` | Now is at or after `up_at`. The public page hides it |
| `off` | Disabled, or the timestamps do not parse |

An active window wins over an upcoming one. If two windows share a phase, the one with the earlier return time is shown.

When a window is already `down` and `frozen` is still false, the poller (`_kick_service` → `freeze_due`) reads the public state once and stores it, then sets `frozen` so it does not keep retrying. A failed count read still sets `frozen`. The poller logs `service notice frozen <ids>`.

The homepage banner (`index.html` + `service-banner.js`) says "Planned service window" or "Service window in progress", the note, and the expected return. Dismiss hides that window id for the browser session.

During phase `down`, `live.js` labels the network panel planned-down and shows the stored counts. It does not invent a live reading.

The Telemetry page in Root Monitor lists the windows, adds one after confirm, deletes one after confirm, and can refresh one window's last-known snapshot. Refresh does not change the clock times.

## 6. What the public reports page does in the same pass

`Website/scripts/publish_report_pages.py` writes `Website/Home/reports/` from `test-reports/Voice/<key>_current.md` and the Discord route list `Communications/Discord/config/report-channels.json`. The address is `https://www.rootrecord.cloud/reports/<slug>`.

The page keeps measured sections. It drops the `## Spoken` block, persona names, and internal source paths. A file is left untouched when the bytes already match.

`Communications/Discord/scripts/report_relay.py` calls that script before it posts. `lib/public_report.py` posts the report title, the measured lines, and the page link. Spoken transcripts stay out of the Discord message. The 8-hour and 24-hour consolidations use the same measured text and the same link.

## 7. What this does not change

- Controls-page risky actions stay unwired until a command is signed off.
- The Not migrated row "Energy actuating actions" stays VERIFY PENDING. The scheduled catalog above is the path that exists. Immediate arm or disarm from Controls is still unwired.
- Delta 2 transmit behavior is unchanged. A quiet Delta 2 read is still normal.
- These modules do not send mail, spend money, or push git by themselves. The website mirror publishes `service-notice.json` when that folder syncs.
- The Automations **data-poll** control does not delete home collectors and does not auto-restart the poller. Live flip (~02:50 HST) applied env + human poller restart after ML2 banks/schema were verified; gate only — collectors stay installed. Exclusive (~03:08): only one side on at a time; EcoFlow/cams forever Pacific. Distinct from AWS Fallback (ML1; Status bindable again after ~03:04 restore).
