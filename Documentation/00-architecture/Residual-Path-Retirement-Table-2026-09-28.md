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
| Energy actions | `…/skills/energy/scripts/actions` | `Energy/scripts/actions` | Yes — source LANDED / runtime VERIFY PENDING | Partial — `solar-gate-status` PASS 2026-09-29T10:43:09Z (00:43 HST; read-only, returns the honest `WAITING` / no data answer); actuating actions (arm/disarm, AC always-on) VERIFY PENDING (they change hardware; not approved) — `2 - RootRecord-Database/Logs/Migration/g3-energy-plumbing-evidence-20260929T104618Z.md` | Partial 2026-09-29: `~/.ollama/skills/energy/scripts/actions/solar-gate-status.sh` → `Energy/scripts/actions/solar-gate-status.sh` (MIGRATED.md placed). Actuating wrappers stay in G2 |
| Energy BLE owner | `…/.ollama/skills/energy/scripts/ble/ble-owner.py` | `Energy/scripts/ble/ble-owner.py` | Yes — `ava-ecoflow-ble.service` + `devices.conf` repointed 2026-09-29 | PASS 2026-09-29T10:35:14Z (00:35 HST) — `2 - RootRecord-Database/Logs/Migration/g3-cutover-evidence-20260929T103720Z.md` | 2026-09-29: `~/.ollama/skills/energy/scripts/ble/ble-owner.py` → `Energy/scripts/ble/ble-owner.py` (MIGRATED.md placed) |
| Plumbing warmups / single-flight | `…/skills/plumbing/…` | `System/scripts/plumbing/` | Yes — source LANDED / runtime VERIFY PENDING | Non-NPU PASS 2026-09-29T10:45:00Z (00:45 HST), after restoring the exec bit on `run-infer.sh` / `run-ollama.sh` / `single-flight.sh` (first try: exit 126): one inference through the Pacific gate, a parallel run refused (exit 75), state under `/home/rootrecord/Database/GITHUB/plumbing/state`. NPU/FLM BLOCKED (no FLM) — `2 - RootRecord-Database/Logs/Migration/g3-energy-plumbing-evidence-20260929T104618Z.md` | Partial 2026-09-29: `~/.ollama/skills/plumbing/scripts/ollama-warmup.sh` → `System/scripts/plumbing/ollama-warmup.sh` (MIGRATED.md placed). Still open: `single-flight.sh`, `run-ollama.sh`, `run-infer.sh` (the retained G2 Telegram relay and `relay.conf` point at them) and `flm-warmup.sh` (NPU BLOCKED) |
| System sampling | `…/.ollama/skills/system-stats/scripts/sys-sample.sh` | `System/scripts/sys-sample.sh` | Present on Pacific; `jobs.py` points here | PASS 2026-09-29T10:12–10:16Z (00:12–00:16 HST) — `2 - RootRecord-Database/Logs/Migration/g3-runtime-evidence-20260929T101550Z.md` |2026-09-29: `~/.ollama/skills/system-stats/scripts/sys-sample.sh` → `System/scripts/sys-sample.sh` (MIGRATED.md placed) |
| Reports worklog | `…/.ollama/skills/reports/scripts/worklog_once.sh` | `Reports/scripts/worklog_once.sh` | Present on Pacific; `jobs.py` points here | PASS 2026-09-29T10:12–10:16Z (00:12–00:16 HST) — `2 - RootRecord-Database/Logs/Migration/g3-runtime-evidence-20260929T101550Z.md` |2026-09-29: `~/.ollama/skills/reports/scripts/worklog_once.sh` → `Reports/scripts/worklog_once.sh` (MIGRATED.md placed) |
| Weather poller | `…/skills/Weather/…` | `Weather/` (when imported) | N/A — **disabled** | leave disabled | leave until Weather WO |
| Network globe cwd | legacy `coms/ssh/…` | Pacific `Communications/network/` | Yes — collector moved to `Communications/network/local-data-globe/`; `network-globe-hawaii.service` repointed 2026-09-29 | PASS 2026-09-29T10:33:44Z (00:33 HST) — `2 - RootRecord-Database/Logs/Migration/g3-cutover-evidence-20260929T103720Z.md` | 2026-09-29: `~/.ollama/skills/coms/ssh/local-data-globe/collector.js` + `telegram-relay.js` → `Communications/network/local-data-globe/` (MIGRATED.md placed) |

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

### Staged migrations — 2026-09-29

- **Network globe — STAGED (awaiting unit repoint).** G2 `~/.ollama/skills/coms/ssh/local-data-globe/collector.js` plus its required `telegram-relay.js` and `package.json` copied to Pacific `Communications/network/local-data-globe/` (no `node_modules`, no secrets; the copies contain no `.ollama/skills` paths; `node --check` OK). Proposed unit: `Communications/network/local-data-globe/network-globe-hawaii.service.proposed` (WorkingDirectory + ExecStart → Pacific). Not installed; the live `network-globe-hawaii.service` still runs the G2 collector.
- **Energy BLE owner — STAGED (awaiting unit repoint + `devices.conf`).** G2 `~/.ollama/skills/energy/scripts/ble/ble-owner.py` (stdlib only) copied to Pacific `Energy/scripts/ble/ble-owner.py`; log/pid moved to `/home/rootrecord/Database/Logs/Energy/ava-ecoflow-ble.log` and `/home/rootrecord/Database/ENERGY/state/ava-ecoflow-ble.pid` (env-overridable); `py_compile` OK. Proposed unit: `Energy/scripts/ble/ava-ecoflow-ble.service.proposed`, which also lists the `devices.conf` `ble_log` (line 24) and `owner_script` (line 98) changes. Not installed; the live `ava-ecoflow-ble.service` still runs the G2 owner.
- **Telegram relay — code fix landed.** Pacific `Communications/telegram/scripts/ensure-relay.sh` now checks the relay is alive 3 s after launch and prints `[FAIL] … last log: …` (token-redacted) with exit 1 instead of a false `[ok]`. `bash -n` OK. Takes effect the next time the poller runs `council_relay`; nothing was restarted. The relay itself still needs `TELEGRAM_AVA_TOKEN` provisioned.
- **Update 2026-09-29 ~00:35 HST:** both staged units were installed after operator approval and PASSed; see `2 - RootRecord-Database/Logs/Migration/g3-cutover-evidence-20260929T103720Z.md`.
- **Update 2026-09-29 ~00:46 HST:** Energy `solar-gate-status` PASS (read-only, no data yet); Plumbing non-NPU PASS after an exec-bit fix; B1 (River 2 Pro) = 0% recorded as a cloud-API/device reading, not a migration fault. See `2 - RootRecord-Database/Logs/Migration/g3-energy-plumbing-evidence-20260929T104618Z.md`.

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
