# Residual Path Retirement Table

| Field | Value |
| --- | --- |
| **Date** | 2026-09-28 (HST) |
| **Supports** | WO-SRV-2026-09-27 |
| **Rule** | Pre-filled from existing static audits. Bruce fills Verified / Retired after G3 checklist. Docs only. |

---

## Operator runbook

Use the companion [G3 Runtime Verification Runbook](./G3-Runtime-Verification-Runbook-2026-09-28.md) for exact desk commands and evidence requirements. This table remains the retirement record.

## How to use

1. Run [G3 Runtime Verification Checklist](./G3-Runtime-Verification-Checklist-2026-09-28.md)  
2. Mark **Verified** only with evidence (cycle OK + path on Pacific)  
3. Mark **Retired** only after legacy **executable** removed or `MIGRATED.md` placed  
4. Keep legacy `SKILL.md` files  

Pacific root (desk):  
`/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server`

---

## Residuals (from WO-SRV audit 2026-09-28)

| Surface | Legacy pattern (historical) | Pacific target | Static source OK | Verified (runtime) | Retired |
| --- | --- | --- | --- | --- | --- |
| Telegram / council_relay | `…/skills/coms/telegram/…` | `Communications/telegram/` (+ plumbing under `System/scripts/plumbing/`) | Yes (paths rewired in source) | | |
| Security/Cameras cam / grab / timelapse | `…/.ollama/skills/a-eyes/scripts/…` | `Security/Cameras/` (hourly wrapper on Pacific) | Yes | PASS (cam server + frame grab; timelapse compile VERIFY PENDING) 2026-09-29T10:12–10:16Z (00:12–00:16 HST) — `2 - RootRecord-Database/Logs/Migration/g3-runtime-evidence-20260929T101550Z.md` |Partial 2026-09-29: `~/.ollama/skills/a-eyes/scripts/grab_all.sh` → `Security/Cameras/grab_all.sh` (MIGRATED.md placed). Still open: `cam_server.py`, `ensure_cam_server.sh`, `grab_frame.py` (referenced by G2 `install_aeyes_web.sh` / `timelapse_engine.py`) and the timelapse part |
| Energy actions | `…/skills/energy/scripts/actions` | `Energy/scripts/actions` | Yes — source LANDED / runtime VERIFY PENDING | | confirm only |
| Plumbing warmups / single-flight | `…/skills/plumbing/…` | `System/scripts/plumbing/` | Yes — source LANDED / runtime VERIFY PENDING | | confirm only |
| System sampling | `…/.ollama/skills/system-stats/scripts/sys-sample.sh` | `System/scripts/sys-sample.sh` | Present on Pacific; `jobs.py` points here | PASS 2026-09-29T10:12–10:16Z (00:12–00:16 HST) — `2 - RootRecord-Database/Logs/Migration/g3-runtime-evidence-20260929T101550Z.md` |2026-09-29: `~/.ollama/skills/system-stats/scripts/sys-sample.sh` → `System/scripts/sys-sample.sh` (MIGRATED.md placed) |
| Reports worklog | `…/.ollama/skills/reports/scripts/worklog_once.sh` | `Reports/scripts/worklog_once.sh` | Present on Pacific; `jobs.py` points here | PASS 2026-09-29T10:12–10:16Z (00:12–00:16 HST) — `2 - RootRecord-Database/Logs/Migration/g3-runtime-evidence-20260929T101550Z.md` |2026-09-29: `~/.ollama/skills/reports/scripts/worklog_once.sh` → `Reports/scripts/worklog_once.sh` (MIGRATED.md placed) |
| Weather poller | `…/skills/Weather/…` | `Weather/` (when imported) | N/A — **disabled** | leave disabled | leave until Weather WO |
| Network globe cwd | legacy `coms/ssh/…` | Pacific `Communications/network/` | Yes — cwd source LANDED / runtime VERIFY PENDING | | |

### G3 runtime evidence — 2026-09-29

Read-only desk capture 2026-09-29T10:12–10:16Z (00:12–00:16 HST); evidence file `2 - RootRecord-Database/Logs/Migration/g3-runtime-evidence-20260929T101550Z.md` (RootRecord-Database repo). Scored against the G3 Runtime Verification Runbook. No retirement performed.

| Row | State | Evidence / note |
| --- | --- | --- |
| Security/Cameras — cam server | PASS | `:8791` listener is `python3 cam_server.py` with cwd Pacific `Security/Cameras`; `/health` 200; no cam process under `.ollama/skills` |
| Security/Cameras — frame grab | PASS | `security_camera_frame_grab` wrote ch1–ch4 frames to `2 - RootRecord-Database/Media/Images/`; Pacific tree clean; `store/` git-ignored |
| Security/Cameras — timelapse | VERIFY PENDING | hourly/catchup ran from Pacific but only skipped (outside window / no frames); no compile observed |
| Telegram council relay | FAIL | No `council-relay.py` process; relay exits at start with `No data: poll token` (74× in relay log). `TELEGRAM_AVA_TOKEN` is not supplied: `SECRETS_1` (`~/.config/ava-council/secrets.env`) is missing and `SECRETS_2` has no Telegram key. `ensure-relay.sh` still logs `[ok] started` without checking the process survived. |
| Energy actions | VERIFY PENDING | Pacific `Energy/scripts/actions/` present and executable; no `solar-gate-status` run in the log |
| Energy BLE owner | FAIL | `ava-ecoflow-ble.service` runs G2 `~/.ollama/skills/energy/scripts/ble/ble-owner.py`; Pacific `Energy/config/devices.conf` `owner_script` points there; no Pacific counterpart |
| System sampling | PASS | `sys_stats_cycle` runs Pacific `System/scripts/sys-sample.sh` → `OK wrote /home/rootrecord/Database/SYSTEM/samples/…json` |
| Reports worklog | PASS | `worklog_scan` runs Pacific `Reports/scripts/worklog_once.sh` → `OK wrote/updated /home/rootrecord/Database/WORKLOG/worklog_current.md` |
| Plumbing (non-NPU) | VERIFY PENDING | `ollama_warmup` from Pacific `System/scripts/plumbing/` → `[ok] ollama up`; no inference through the Pacific single-flight gate (state dir `/home/rootrecord/Database/GITHUB/plumbing/state` absent) |
| Plumbing (NPU / FLM) | BLOCKED | no `flm` binary, no `ava-flm.service`, `:52625` unreachable |
| Network globe | FAIL | `network-globe-hawaii.service` ExecStart/WorkingDirectory = G2 `~/.ollama/skills/coms/ssh/local-data-globe/collector.js` (running); Pacific has no collector |
| systemd ExecStart | PASS | `rr-rootserver-poller.service` (user) ExecStart = Pacific `Automations/scripts/poller/run-poller.sh`; MainPID = Pacific `rootserver_poller.py` (imports `jobs` from its own dir) |
| Pacific poller (§5) | FAIL | poller, `jobs.py` and log are Pacific; log fresh; no `.ollama/skills` refs in the last 3000 lines; no FAIL storm. Fails only because Network Globe resolves to the legacy runtime and the relay is not running |
| Preconditions: single poller / relay / cloudflared | PASS | 1 Pacific `rootserver_poller.py`, no G2 poller; 0 relays (no second getUpdates owner); 1 `cloudflared` (Pacific binary) |

---

## Source LANDED / runtime VERIFY PENDING (no residual action required for path)

Energy reads + leapfrog · System · Reports foundation · Github sync · Cloudflare tunnel · Network globe command  

Record any post-check confirmation in WO-SRV notes if useful; do not re-open closed path work.

---

## Retirement note

- Prefer `MIGRATED.md` on old packet: status, date, canonical Pacific path, “do not run”  
- Do not bulk-delete G1/G2 trees  
- Do not remove legacy `SKILL.md` solely because runtime moved  

*Pre-filled for Bruce. Empty columns are intentional. 2026-09-28 HST.*
