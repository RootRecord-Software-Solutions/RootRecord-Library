# WORK ORDER — River car DC drive

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-MIG-39-2026-09-29 |
| **Date** | 2026-09-30 (HST) |
| **Status** | OPEN — built, dry-run verified; hardware not switched |
| **Owner** | RootRecord |
| **Related** | Agent 39. Old home `energy/ecoflow-river-car`. Live BLE switch `Energy/scripts/actions/river2pro-dc-on.sh` and `river2pro-dc-off.sh`. |

**Scope:** Policy layer for the River 2 Pro car/12V port that powers external drives. Default off. Dry-run unless `--execute`, and `--execute` still refuses unless `RR_RIVER_CAR_EXECUTE=1`. Built 2026-09-30 HST. The car port was not switched. The 30-minute job is gated off.

---

## 1. Intent

Old `energy/ecoflow-river-car` powered external drives from the River 2 Pro car/12V port only. Default off. Dry-run unless `--execute`. If the port was already on, an off without force left it on. A 30-minute `drive-automation` tick did nothing until `auto` was true and an enabled copy job existed. Copy is still a stub (`copy_not_implemented`), so the tick never spun disks. It never switched AC. Starlink stays on Delta AC. River AC stays on for the laptop.

Keep the live BLE switch. `river2pro-dc-on.sh` and `river2pro-dc-off.sh` call `action_runner.py` method `enable_dc_12v_port`. Do not replace the BLE poller, `ecoflow_api.py`, or those scripts. The new code is the policy layer on top of them. Cloud `PUT mpptCar` from the old `river_car_dc.py` is not ported.

---

## 2. Current reality

Subfolder of Energy. Name in all three places: **River-Car**. No top-level domain, no lowercase twin, no symlink.

- Code: `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Energy/River-Car/scripts`
- Database: `2 - RootRecord-Database/Energy/River-Car/` (state and last files; not git)
- Logs: `2 - RootRecord-Database/Logs/Energy/River-Car/`

No new `master-key.env` keys. Actuation reuses the live BLE scripts, which already load `ECOFLOW_RIVER_2_PRO` through `Energy/lib/envload.py`. This function does not print values and does not add an env file. It does not call the EcoFlow cloud quota API.

### 2.1 What exists

| Item | Location / status |
| --- | --- |
| Folder name | `River-Car` under Energy |
| Code path | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Energy/River-Car/scripts` |
| Database path | `2 - RootRecord-Database/Energy/River-Car/` (runtime state; gitignored) |
| Logs path | `2 - RootRecord-Database/Logs/Energy/River-Car/` (runtime; gitignored) |
| Secrets | No new keys. Existing allowlist name used by the BLE scripts: `ECOFLOW_RIVER_2_PRO`. Do not print values. |
| Old source | Removed from `/home/rootrecord/old ollama/old skills` and from GitHub commit `e41510a8`. Archive: `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/energy/ecoflow-river-car/`. |
| Live atomic switch | `Energy/scripts/actions/river2pro-dc-on.sh` and `river2pro-dc-off.sh` via `enable_dc_12v_port`. Keep. |
| Automation policy | `Energy/River-Car/scripts/`. Job `energy_river_car_drive` gated off. |
| Car state for status | Existing Energy reads (`dc_12v_port` in `read_runner.py`). Not a new cloud poll. |
| Dependency Folders | Energy and `Energy/scripts/actions/` already exist. No pause for a missing Folder. |

### 2.2 Completed so far

- [x] Draft work order written.
- [x] `Energy/River-Car` scripts
- [x] Database state and logs directories (created at runtime by the dry-run; not committed)
- [x] Gated `jobs.py` block (`RR_RIVER_CAR_DRIVE` default off)
- [x] Dry-run proof test (spawn count 0)
- [x] Archive, old-repo deletion, GitHub file deletion (`e41510a8`)
- [x] Result note and Library row corrections

### 2.3 Known friction

- The live system already switches this port over BLE. The old skill used a cloud `PUT mpptCar`. New code calls the BLE scripts. It does not copy the cloud client over them.
- `jobs.py` was free at build time. The gated-off `energy_river_car_drive` block is in place. `RR_RIVER_CAR_DRIVE` is unset.
- Do not edit the Vercel app or `master-key.env` for this function.
- Hardware switching needs Alexander's sign-off. `--execute` stays refused until `RR_RIVER_CAR_EXECUTE=1`.

---

## 3. Tasks

Build only after Alexander accepts this draft and says to build. Until then, do not edit runtime files, restart services, send messages, actuate hardware, or spend cloud money.

1. Add `Energy/River-Car/scripts/river_car_dc.py`: `--status`, `--on`, `--off`. Default dry-run. `--execute` is the only path that runs `river2pro-dc-on.sh` or `river2pro-dc-off.sh`, and it still refuses unless `RR_RIVER_CAR_EXECUTE=1`. Off without force, when the last read says the port is already on, records `leave_on_manual` and does not call the off script.
2. Add `disk_session.py`: `lsblk` snapshot, `prepare` / `release`. Same dry-run and execute gate. No AC calls.
3. Add `drive_automation.py`: `--status`, `--on`, `--off`, `--session`, `--tick`, `--auto on|off`. `--tick` returns `auto_off` unless state `auto` is true, then `no_copy_jobs` or `copy_not_implemented`. `run_copy_jobs` stays a stub. No rsync.
4. State JSON (`river-car-dc.json`, `drive-automation.json`, lock) is written under Database `Energy/River-Car/` at runtime. Logs under Database `Logs/Energy/River-Car/`. Do not commit them. Do not copy old `~/.ollama` state in.
5. Propose this gated block. Add it to `jobs.py` only when that file is not being edited; otherwise stop and name `jobs.py`. Gate default off. The tick’s own skips stay in place even if the gate is later turned on.

```text
id: energy_river_car_drive
enabled: RR_RIVER_CAR_DRIVE == "1"   # default off
interval: 30 min
command: python3 Energy/River-Car/scripts/drive_automation.py --tick
```

6. Small test, no power change: `--tick` prints `skipped=auto_off` and does not spawn the DC scripts. `--on` without `--execute` records `dry_run_on` and does not spawn them. `--execute` without `RR_RIVER_CAR_EXECUTE=1` exits refused and does not spawn them.
7. After that test passes: archive, then delete, then update this work order and the stale Library rows. Do not start step 7 in the draft pass.

---

## 4. Non-goals

- Do not overwrite `river2pro-dc-on.sh`, `river2pro-dc-off.sh`, `action_runner.py`, `ble_client.py`, `ecoflow_api.py`, or the BLE poller.
- Do not PUT EcoFlow cloud quota, and do not switch Delta AC, River AC, USB, or the solar gate.
- Do not implement copy/rsync/unmount, panels-cam (agent 40), or any other agent’s function.
- Do not edit the website, Android apps, or `master-key.env`.
- Do not import logs, samples, last-state, `__pycache__`, or old Core Ops JSON into Pacific, Database git, or the website.
- Do not restore anything under `~/.ollama/skills/energy`.

---

## 5. Key file / path reference

| Path | Role |
|------|------|
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Energy/River-Car/scripts` | Code. Add at build: `README.md` beside `scripts/`, plus `scripts/river_car_dc.py`, `scripts/disk_session.py`, `scripts/drive_automation.py`. |
| `2 - RootRecord-Database/Energy/River-Car/` | Runtime state (`river-car-dc.json`, `drive-automation.json`, lock). Not git. |
| `2 - RootRecord-Database/Logs/Energy/River-Car/` | Logs only. |
| `Energy/scripts/actions/river2pro-dc-on.sh` | Live BLE on. Call. Do not edit. |
| `Energy/scripts/actions/river2pro-dc-off.sh` | Live BLE off. Call. Do not edit. |
| `Automations/scripts/jobs.py` | One gated-off `energy_river_car_drive` entry, only if the file is free at build time. Otherwise the block stays in this work order. |
| `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/energy/ecoflow-river-car/` | Phase 4 archive. Same relative path as the old repo. Include the untracked `__pycache__` beside those scripts. |
| `/home/rootrecord/old ollama/old skills` | Old git root. Delete the archived paths only after the copy is on disk. Commit and push `Solar-Pacific-RootRecord-Server`. No force-push. Do not delete the GitHub repository. If the archive copy fails, do not delete. |
| `Documentation/00-architecture/Old-Repo-Migration-Matrix.md` | Phase 5. Correct row 32 only. |
| `Documentation/00-architecture/Solar-Pacific-Old-Inventory-Map-2026-09-28.md` | Phase 5. Correct the `ecoflow-river-car` line only. |

---

## 6. Open items

**Additional requirements:**

- Hardware switching, cloud spend, sends, speaker playback, OBS, and deletion of live Ecosystem files need Alexander's sign-off. This draft does none of them. `--execute` stays refused until `RR_RIVER_CAR_EXECUTE=1` for a real run.
- `RR_RIVER_CAR_DRIVE` stays unset, so the 30-minute job cannot run even after the gated block is added.
- Proof test is task 6. It must not change the car port.
- After phase 4, add a short result note to this same work order: what landed, the archive path, and the GitHub file deletion. Correct only the two Library pages in section 5.

---

## 7. Notes & constraints

- No force-push.
- Secrets stay out of git. No new `master-key.env` keys. Never print secret values.
- Prefer small reversible steps. The first build step is the dry-run policy scripts. The DC scripts are not spawned by the proof test.
- Do not edit `jobs.py`, the Vercel app shell, or `master-key.env` while this file is still a draft. At build time, pause if `jobs.py` is already being edited.
- Starlink stays on Delta AC. River AC stays on for the laptop. This function never calls AC APIs.

---

*Work order prepared 2026-09-30 HST. Update status when closed.*

---

## Archive / location note

**Active / accepted WOs** — filename when saved:

```text
River_car_DC_drive_Work_Order_WO-MIG-39-2026-09-29.md
```

Location when accepted (do not promote this draft):

```text
Documentation/06-development/Work-Orders/
```

**Drafts (not on active index)** — this file:

```text
Documentation/06-development/Work-Orders/drafts/River_car_DC_drive_Work_Order_WO-MIG-39-2026-09-29.md
```

See `drafts/README.md` and WO-WOGEN-001. Do not auto-promote.

**Closed WOs:** set Status → COMPLETE/CLOSED → `git mv` into:

```text
Documentation/06-development/Work-Orders/Complete/
```

Human session logs archive under `Documentation/01-operations/archive/YYYY-Www/` (WO-ARCH) — separate from closed work orders.

---

## Result note

Built 2026-09-30 HST. Landed: `Energy/River-Car/README.md`, `scripts/river_car_dc.py`, `scripts/disk_session.py`, `scripts/drive_automation.py`. `jobs.py` gained gated-off `energy_river_car_drive` (1800 s, `RR_RIVER_CAR_DRIVE` default off). Proof: `--tick` printed `skipped=auto_off`, `--on` recorded `dry_run_on`, `--on --execute` without `RR_RIVER_CAR_EXECUTE=1` exited refused. Spawn count 0. The car port was not switched.

Archived to `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/energy/ecoflow-river-car/` (tracked sources plus `__pycache__`, and the untracked sibling bytecode). Removed from `/home/rootrecord/old ollama/old skills` and from GitHub `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server` branch `online-safe-20260920` commit `e41510a8`. The repository was not deleted. No force-push.

Library rows corrected: Old-Repo-Migration-Matrix row 32, and the `ecoflow-river-car` line in Solar-Pacific-Old-Inventory-Map-2026-09-28. This work order stays in `drafts/` and is not on the active index.
