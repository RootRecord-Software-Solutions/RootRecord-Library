# WORK ORDER — Panels-cam power session

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-MIG-40-2026-09-29 |
| **Date** | 2026-09-30 (HST) |
| **Status** | OPEN — draft, not accepted for execution |
| **Owner** | RootRecord |
| **Related** | Agent 40, Wave F. Hardware. Old home `panels-cam` in `Solar-Pacific-RootRecord-Server-Old`. Live grab: Pacific `Security/Cameras/`. Live switch: Energy `river2pro-dc-on.sh` / `river2pro-dc-off.sh`. |

**Scope:** Add the River 2 Pro car/12V power session beside the existing Night Owl grab, as Pacific `Security/PanelsCamPower`. In scope after this draft is accepted: a dry-run-by-default session script that calls the existing BLE DC scripts only with `--execute`. Out of scope: camera grab changes, EcoFlow BLE or the poller, cloud `mpptCar`, AC switching, `jobs.py`, other agents’ functions, and any hardware or GitHub deletion before acceptance and a working build.

This file is the before-documentation. It is not on the active index.

---

## 1. Intent

The old function `panels-cam/scripts/cam_power_session.py` ran one River 2 Pro car/12V session for the Night Owl rear-shed camera. It turned the car port on, waited (default 8 seconds) only when this session was the one that turned it on, then turned it off unless this session did not own the power or a drive hold said to leave it on. The default was a dry-run. `--execute` was required to switch. It never toggled AC.

That old path called the cloud `mpptCar` client. The live system already switches the same bit over BLE: Energy `dc_12v_port` is `pb_mppt.car_state`, and `river2pro-dc-on.sh` / `river2pro-dc-off.sh` call `enable_dc_12v_port`. The build enhances that path. It does not port the cloud client and does not replace the BLE poller.

Camera grabs for channels 1–4 are live under Pacific `Security/Cameras/` (`grab_frame.py`, `grab_all.sh`, `cam_server.py`, and the camera entries in `jobs.py`). Those stay. The power session is the missing piece, added beside the grab.

---

## 2. Current reality

### 2.1 What exists

Folder name: `PanelsCamPower`. Same name in all three places. No lowercase twin and no symlink. No `Logs/` directory on the server.

| Item | Location / status |
| --- | --- |
| Server code | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Security/PanelsCamPower/scripts` — not installed |
| Database data | `2 - RootRecord-Database/Security/PanelsCamPower` — not installed; session JSON only, not imported into git |
| Database logs | `2 - RootRecord-Database/Logs/Security/PanelsCamPower` — not installed |
| master-key.env | No new key names. The session does not read secrets. Existing Energy scripts already load EcoFlow keys. |
| Live grab | Pacific `Security/Cameras/` channels 1–4. Keep. |
| Live River DC switch | `Energy/scripts/actions/river2pro-dc-on.sh` and `river2pro-dc-off.sh` (`enable_dc_12v_port`). Keep. |
| EcoFlow BLE and poller | Live. Do not replace. |
| Old source | `Solar-Pacific-RootRecord-Server-Old` `panels-cam/scripts/cam_power_session.py` |
| Dependency | `Energy` exists. No pause. |

### 2.2 Completed so far

- [x] Draft work order written (this file). Status stays OPEN — draft, not accepted for execution.
- [ ] Alexander accepts this draft and says to build.
- [ ] `PanelsCamPower` package and `scripts/cam_power_session.py` added.
- [ ] Dry-run test passed (`--on` without `--execute`).
- [ ] Phase 4 archive, old-repo deletion, and GitHub commit/push.
- [ ] Result note on this work order, and the two stale Library lines corrected.

### 2.3 Known friction

- Hardware switching needs Alexander’s sign-off. `--execute` stays gated until then.
- The old cloud `mpptCar` client is not the live switch. New code uses the existing BLE DC scripts.
- `panels_grab.py` in the old packet mixes grab and car power. It is shared with the live grab function and stays in the old repo.
- There is no G3 drive-hold file yet. Off skips when the port was already on (`not_our_power`). A hold file is honored if one is present later. This work does not build drive automation.

---

## 3. Tasks

Build only after Alexander accepts this draft and says to build. Until then, do not edit runtime files, restart services, send messages, actuate hardware, or spend cloud money.

1. Add the `PanelsCamPower` package under Pacific `Security/`, beside `Security/Cameras/`, with `scripts/cam_power_session.py` and a short README. Python package name `PanelsCamPower`.
2. `--status` (and the default with no `--on`/`--off`) reads the latest River 2 Pro sample `dc_12v_port` plus local session state. No BLE write.
3. `--on` / `--off` without `--execute` write a dry-run JSON report only. They do not call the DC scripts.
4. `--execute` is gated. It calls the existing `river2pro-dc-on.sh` or `river2pro-dc-off.sh`. It does not call AC scripts and does not use the cloud `mpptCar` client.
5. After a real on, wait the settle time (default 8 seconds) only when this session turned the port on. Off skips when the port was already on (`not_our_power`) or a hold file says to leave it on.
6. Write session JSON under `2 - RootRecord-Database/Security/PanelsCamPower`. Logs, if any, go under `2 - RootRecord-Database/Logs/Security/PanelsCamPower`. Do not put logs on the server. Do not import session JSON, samples, or logs into git.
7. Do not edit `jobs.py`. No new periodic job.
8. Small test, before any `--execute`: `python3 cam_power_session.py --on` prints a JSON dry-run and does not invoke `river2pro-dc-on.sh`.
9. After the migration works, phase 4: copy `panels-cam/scripts/cam_power_session.py` to `Old repos deleted and merged/Solar-Pacific-RootRecord-Server-Old/panels-cam/scripts/cam_power_session.py`, keeping that path inside the old repo. Generated data that belongs to this file goes with it and still does not go into the live Folders. If the archive copy fails, do not delete. After the archive copy is on disk, delete that same file from `Solar-Pacific-RootRecord-Server-Old` on this machine and on GitHub. Commit that deletion and push it. Do not force-push. Do not delete the GitHub repository.
10. Then add the result note to this work order and correct only the Library pages this function made stale.

---

## 4. Non-goals

- Do not overwrite or replace `Security/Cameras/` (`grab_frame.py`, `grab_all.sh`, `cam_server.py`, timelapse scripts, `references/CAMERAS.md`).
- Do not replace EcoFlow BLE, the poller, Hawaiʻi weather, the globe collector, Kokoro, or `geology_collect.py`.
- Do not edit `jobs.py` or the live camera job entries.
- Do not port the cloud `mpptCar` client. Do not add a second env file. Do not commit secrets.
- Do not call River or Delta AC scripts. Do not switch hardware without `--execute` and Alexander’s sign-off.
- Do not build drive automation, the AWS cam gateway, or the origin mux.
- Do not edit other agents’ files. Shared old-repo files stay and are named in Notes.
- Do not import logs, samples, last-state files, frames, or other generated data into Pacific, Database git, the website, or git.
- Do not restore files under `~/.ollama/skills/energy`, automations, or `coms/ssh/local-data-globe`.
- Do not delete the GitHub repository. Do not force-push.

---

## 5. Key file / path reference

| Path | Role |
|------|------|
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Security/PanelsCamPower/scripts/cam_power_session.py` | New session script (add at build) |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Security/PanelsCamPower/README.md` | Short README (add at build) |
| `2 - RootRecord-Database/Security/PanelsCamPower/` | Session JSON (runtime; not git) |
| `2 - RootRecord-Database/Logs/Security/PanelsCamPower/` | Logs only (runtime; not git) |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Energy/scripts/actions/river2pro-dc-on.sh` | Existing BLE DC on. Called only with `--execute`. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Energy/scripts/actions/river2pro-dc-off.sh` | Existing BLE DC off. Called only with `--execute`. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Energy/lib/vendor/eflib/devices/river2.py` | `dc_12v_port` is `pb_mppt.car_state`. Do not edit. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Security/Cameras/` | Live grab. Do not edit. |
| `panels-cam/scripts/cam_power_session.py` in `Solar-Pacific-RootRecord-Server-Old` | Old source. Archive, then delete, only in phase 4. |

---

## 6. Open items

**Additional requirements:**

- Alexander accepts this draft and says to build before any runtime edit.
- Alexander signs off before any `--execute` hardware switch.
- Phase 4 runs only after the migration works, and only for `cam_power_session.py`.

---

## 7. Notes & constraints

- No force-push.
- Secrets stay out of git. No new `master-key.env` key names.
- Prefer small reversible steps.
- Hardware switching (`--execute`), sends, speaker playback, OBS, deletion of live Ecosystem files, and cloud spend require Alexander’s sign-off. Do not do those things in the draft phase. Phase 4 is already ordered for the old function’s file only: archive first, then remove it from the old repo locally and on GitHub.
- Small test that proves the new behavior: from `Security/PanelsCamPower/scripts`, `python3 cam_power_session.py --on` with no `--execute` prints a JSON dry-run and does not invoke `river2pro-dc-on.sh`.
- Shared old-repo files to leave, and name here: `panels-cam/scripts/panels_grab.py`, `panels-cam/scripts/cam_gateway.py`, `panels-cam/scripts/solar_origin_mux.py`, `panels-cam/store/`, `panels-cam/SKILL.md`. Also leave `/home/rootrecord/old ollama/old skills` (different repo, `Solar-Pacific-RootRecord-Server`).
- If the archive copy fails, do not delete.
- After phase 4, add a short result note here (what landed, what was archived, what was removed on GitHub) and correct only the stale Library lines for this function: migration matrix row 64, and the panels-cam row on the scheduler map. `Security/Cameras/references/CAMERAS.md` still describes the grab, which still has no power control, so it stays unless that grab text is wrong.
- Do not rewrite unrelated work orders. Do not promote this draft onto the active index.

---

*Work order prepared 2026-09-30 HST. Update status when closed.*

---

## Archive / location note

**Active / accepted WOs** — filename when saved:

```text
Panels_cam_power_session_Work_Order_WO-MIG-40-2026-09-29.md
```

Location when accepted (not yet):

```text
Documentation/06-development/Work-Orders/
```

**Drafts (not on active index)** — this file:

```text
Documentation/06-development/Work-Orders/drafts/Panels_cam_power_session_Work_Order_WO-MIG-40-2026-09-29.md
```

See `drafts/README.md` and WO-WOGEN-001. Do not auto-promote.

**Closed WOs:** set Status → COMPLETE/CLOSED → `git mv` into:

```text
Documentation/06-development/Work-Orders/Complete/
```

Human session logs archive under `Documentation/01-operations/archive/YYYY-Www/` (WO-ARCH) — separate from closed work orders.

---

## Result note

Not written. Phase 4 has not run. Fill this after the archive and the GitHub deletion: what landed, the archive path, and what was removed on GitHub.
