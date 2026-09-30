# WORK ORDER — EcoFlow cloud quota poll

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-MIG-36-2026-09-29 |
| **Date** | 2026-09-30 (HST) |
| **Status** | BUILT — gate in place, job not inserted, archive copied, GitHub deletion pushed. Not on the active index. |
| **Owner** | RootRecord |
| **Related** | Agent 36. Wave E. Cloud and keys, after the local path. No earlier function has to exist before the build. No later function in this list depends on this one. Matrix row 31. |

**Scope:** EcoFlow cloud quota poll is one Energy subfolder. BLE stays the live read. The cloud path is a labeled fallback and does not call the EcoFlow Open Platform unless `RR_ECOFLOW_CLOUD=1`. That flag stays unset. The job was not inserted because `jobs.py` already had other edits. Exclusive old files are archived, and that deletion is on GitHub.

---

## 1. Intent

The old cron at `/home/rootrecord/old ollama/old skills/energy/ecoflow-quota/scripts/ecoflow_quota.py` refreshed a snapshot about every 2 minutes, then called a voice “EcoFlow down” announce and the AC solar gate. That file is not the cloud client. The announce and the gate belong to other functions. Do not port them.

The live system already has the newer client. `Energy/lib/ecoflow_api.py` signs `GET /iot-open/sign/device/quota/all` and maps quota keys into the same field shape as a BLE read. Leap-frog (`ecoflow_read_cycle`, every 15s) and the boot read stay the live poll. `read_runner.py` still tries BLE first. A cloud call now happens only when `RR_ECOFLOW_CLOUD=1`, and that snapshot is labeled `source: cloud` under `Energy/Cloud-Quota/`. The flag is unset.

---

## 2. Current reality

### 2.1 What exists

Folder name, used in all three paths: **Cloud-Quota**. It is a subfolder of Energy. No second top-level domain. No lowercase twin. No symlink. No `Logs/` directory on the server. Python is invoked by script path, same as `Geology/Earthquake-Discord/scripts/`.

| Item | Location / status |
| --- | --- |
| Folder | `Cloud-Quota` under Energy. Created. |
| Code | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Energy/Cloud-Quota/scripts` |
| Database | `2 - RootRecord-Database/Energy/Cloud-Quota/` |
| Logs | `2 - RootRecord-Database/Logs/Energy/Cloud-Quota/` |
| Secrets | `/home/rootrecord/master/master-key.env` only, through `Energy/lib/envload.py`. Allowlist names already present: `ECOFLOW_ACCESS`, `ECOFLOW_SECRET`, `ECOFLOW_REGION`, `ECOFLOW_DELTA_2`, `ECOFLOW_RIVER_2_PRO`, `ECOFLOW_DELTA_2_SECONDARY`. `ECOFLOW_ACCESS` and `ECOFLOW_SECRET` are set. `ECOFLOW_REGION` is absent, so the client defaults to `us`. No second env file. Values are never printed. |
| Spend gate | Process env `RR_ECOFLOW_CLOUD`. Not a secret. Unset. Not a new key in `master-key.env`. |
| Client, keep and enhance | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Energy/lib/ecoflow_api.py`. Newer than the old skill. Do not copy the old skill over it. |
| BLE read, keep | `Energy/lib/read_runner.py`, `Energy/scripts/read/leapfrog-read.sh`, `delta2-read.sh`, `river2pro-read.sh`. Delta 2 and River 2 Pro have `prefer_api=0`. Security / B3 has `prefer_api=1` and uses the same client, so the flag covers all three. |
| Live samples, do not replace | `2 - RootRecord-Database/Energy/samples/`. BLE files stay there. Cloud JSON, when the flag is on, goes under `Energy/Cloud-Quota/`. |
| Scheduler | `ecoflow_read_cycle` and `ecoflow_read_boot` in `Automations/scripts/jobs.py` stay enabled. `jobs.py` is already modified in the working tree. This draft does not edit it. |
| Old source | Exclusive files removed from the old skill folder after the archive copy. See the result note. |
| Shared old files, left | `scripts/energy.py`, `scripts/ecoflow_public.py`, and `desk/scheduler.py` (symlink). Still in the old skill folder. |
| GitHub | Deletion `50d3b0a6` is on `Solar-Pacific-RootRecord-Server` branch `online-safe-20260920`. Repository was not deleted. |

### 2.2 Completed so far

- [x] Old cron read. It is not the Open Platform client. Voice announce and AC solar gate left with their own functions.
- [x] Newer client confirmed in `Energy/lib/ecoflow_api.py`. BLE leap-frog confirmed as the live poll.
- [x] Folder `Cloud-Quota` and the three paths named above.
- [x] `master-key.env` checked for key names only. Access and secret names are set. Region name is absent.
- [x] Alexander accepted this draft and said to build.
- [x] `Energy/Cloud-Quota/scripts/quota_poll.py` and a short README. Default run prints `cloud=off` and does not HTTP.
- [x] `read_runner._read_api` skips the Open Platform unless `RR_ECOFLOW_CLOUD=1`, then labels `source: cloud`.
- [ ] Proposed gated `jobs.py` block. Paused: `jobs.py` already had other edits. The block stays in section 3.
- [x] Phase 4 archive of this function’s exclusive old files, then delete only after the copy was on disk.
- [x] Result note and the Library lines that still said the cloud poll was not ported or was blocked.

### 2.3 Known friction

- Build waits until Alexander accepts this draft. Until then, do not edit runtime files, restart services, send messages, actuate hardware, or spend cloud money.
- `jobs.py` is already modified. Do not edit it for this draft. At build time, insert the gated block only if this accepted build is the only edit. If other edits are still there, pause and leave the block in this work order.
- The same client serves Delta 2, River 2 Pro, and security / B3. Gating `_read_api` stops cloud HTTP for all three when the flag is unset. BLE success is unchanged. A BLE miss with the flag unset keeps the existing WAITING exit.
- Tonight’s Delta 2 sample can already be `source: api`. After the build, that fallback does not HTTP unless the flag is on. That is the sign-off. It is not done in this draft.
- `energy.py` and `ecoflow_public.py` stay in the old skill folder. Do not restore anything under `~/.ollama/skills/energy` into Pacific.

---

## 3. Tasks

Do these only after Alexander accepts this draft and says to build. Until then, stop.

1. No dependency folder is missing. Energy and `ecoflow_api.py` already exist. Do not build another agent’s function.
2. Pause if `jobs.py`, the Vercel app shell, or `master-key.env` is already being edited.
3. Add `Energy/Cloud-Quota/scripts/quota_poll.py` and a short README. Default run prints `cloud=off`, the device aliases, and whether the key names are set. It does not HTTP, does not write samples, and does not print secret values.
4. Enhance `read_runner._read_api`. If `RR_ECOFLOW_CLOUD` is not `1`, skip the Open Platform call. BLE success stays as it is. If BLE has no fields and the flag is unset, keep the existing WAITING exit. Delta 2, River 2 Pro, and security / B3 share this client.
5. When the flag is `1`, label the snapshot `source: cloud`, write that JSON under `2 - RootRecord-Database/Energy/Cloud-Quota/`, and append a line under `Logs/Energy/Cloud-Quota/`. Do not replace `Energy/samples` BLE files. Last SOC/watts files may record `source: cloud` so a fallback is visible.
6. Do not edit `jobs.py` unless this accepted build inserts only the gated block below, and only when `jobs.py` has no other edits. Do not enable the job. `RR_ECOFLOW_CLOUD` stays unset, so `enabled` is false at poller start. Leap-frog stays as it is.

```python
{
    # EcoFlow cloud quota (WO-MIG-36). OFF unless RR_ECOFLOW_CLOUD=1
    # is in the poller's environment at poller start. No HTTP until that gate.
    "id": "ecoflow_cloud_quota",
    "enabled": os.environ.get("RR_ECOFLOW_CLOUD", "0") == "1",
    "description": "Labeled EcoFlow Open Platform quota fallback. BLE stays primary. No HTTP unless RR_ECOFLOW_CLOUD=1.",
    "interval_sec": 120,
    "builtin": "",
    "command": f'nice -n 10 python3 "{PACIFIC}/Energy/Cloud-Quota/scripts/quota_poll.py"',
    "timeout_sec": 30,
    "needs_internet": True,
    "cwd": f"{PACIFIC}/Energy/Cloud-Quota",
    "env": {},
}
```

7. One test, no cloud spend: run `quota_poll.py` with the flag unset. Expect exit 0, text `cloud=off`, no new file under `Energy/Cloud-Quota/`, and no request to `api.ecoflow.com`. A fixture map of `pd.soc` through `map_quota_to_fields` proves the field shape without HTTP.
8. After the migration works, and before the Library update: copy this function’s exclusive old files into `Old repos deleted and merged/ecoflow-quota/`, keeping their old relative paths: `scripts/ecoflow_quota.py`, `SKILL.md`, `INDEX.md`, `DAILY.md`, `references/migrate.md`. Leave `scripts/energy.py` and `scripts/ecoflow_public.py`. Do not restore those files into Pacific. After the archive copy is on disk, delete those same exclusive files from the old location on this machine and, if a remote still has them, from GitHub. Commit that deletion and push it. Do not force-push. Do not delete the GitHub repository. `Solar-Pacific-RootRecord-Server-Old/energy/ecoflow-quota` is not in the checkout here. If no remote still has these files, record that and stop. If the archive copy fails, do not delete.
9. Update this work order with the result note (what landed, what was archived, what was removed on GitHub) and set the new status. Correct only the Library lines this function made stale: the ecoflow-quota row in `5 - RootRecord-Library/Documentation/00-architecture/G1-Scheduler-To-G3-Jobs-Map-2026-09-29.md`, and row 31 in `5 - RootRecord-Library/Documentation/00-architecture/Old-Repo-Migration-Matrix.md`. Do not rewrite unrelated work orders.

---

## 4. Non-goals

- Do not replace EcoFlow BLE, `leapfrog-read.sh`, the boot read, `geology_collect.py`, the Hawaiʻi weather poller, the globe collector, camera grabs, or Kokoro.
- Do not port the USB solar gate, the voice “EcoFlow down” announce, or `ecoflow_public.py` / `energy.py` bank math.
- Do not copy the old skill over `Energy/lib/ecoflow_api.py`.
- Do not import logs, samples, last-state files, generated reports, collected images, radar frames, zip archives, database dumps, caches, virtualenvs, `node_modules`, or `__pycache__` into Pacific, Database, the website, or git. Cloud JSON under `Energy/Cloud-Quota/` is runtime output and stays out of git.
- Do not edit the Vercel app, `master-key.env`, or live `Energy/samples` files.
- Do not send, play audio, touch OBS, switch hardware, delete live Ecosystem files, or call EcoFlow during this draft. A live cloud call waits for `RR_ECOFLOW_CLOUD=1` after this draft is accepted.
- Do not enable `ecoflow_cloud_quota`. Do not set `RR_ECOFLOW_CLOUD`.
- Do not add a public page or a second Vercel app.
- Do not edit other agents' files. If `jobs.py`, the Vercel app shell, or `master-key.env` is already being edited, pause.
- Do not put a secret value in this file or in git.
- Do not restore files under `~/.ollama/skills/energy`, automations, or `coms/ssh/local-data-globe`.

---

## 5. Key file / path reference

| Path | Role |
|------|------|
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Energy/Cloud-Quota/scripts` | Code. Created. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Energy/Cloud-Quota/scripts/quota_poll.py` | Default run prints `cloud=off` and does not HTTP. Dry run passed. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Energy/Cloud-Quota/README.md` | Short note for the subfolder. Created. |
| `2 - RootRecord-Database/Energy/Cloud-Quota/` | Cloud snapshots only, and only when `RR_ECOFLOW_CLOUD=1`. Not written in this draft. |
| `2 - RootRecord-Database/Logs/Energy/Cloud-Quota/` | Logs only. |
| `2 - RootRecord-Database/Energy/samples/` | BLE samples. Do not replace. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Energy/lib/ecoflow_api.py` | Live client. Enhance only. Do not overwrite with the old skill. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Energy/lib/read_runner.py` | BLE first. `_read_api` gains the flag and the `cloud` label. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Energy/lib/envload.py` | Allowlist. Do not add a second env file. Do not print values. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Energy/scripts/read/leapfrog-read.sh` | Live poll. Do not replace. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Energy/config/devices.conf` | `prefer_api=0` on Delta 2 and River 2 Pro. `prefer_api=1` on security / B3. |
| `/home/rootrecord/master/master-key.env` | Unchanged. Key names listed in section 2.1. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Automations/scripts/jobs.py` | Proposed gated `ecoflow_cloud_quota` block only. Not edited in this draft. Already modified by other work. |
| `/home/rootrecord/old ollama/old skills/energy/ecoflow-quota/scripts/ecoflow_quota.py` | Exclusive old cron. Archive in phase 4. Do not restore into Pacific. |
| `/home/rootrecord/old ollama/old skills/energy/ecoflow-quota/scripts/energy.py` | Shared bank math. Leave it. |
| `/home/rootrecord/old ollama/old skills/energy/ecoflow-quota/scripts/ecoflow_public.py` | Shared sanitized live file. Leave it. |
| `5 - RootRecord-Library/Documentation/00-architecture/G1-Scheduler-To-G3-Jobs-Map-2026-09-29.md` | ecoflow-quota row, after phase 4 only. |
| `5 - RootRecord-Library/Documentation/00-architecture/Old-Repo-Migration-Matrix.md` | Row 31, after phase 4 only. |

---

## 6. Open items

**Additional requirements:**

- Alexander accepts this draft before any build.
- A live EcoFlow Open Platform call needs a separate sign-off: `RR_ECOFLOW_CLOUD=1`. The flag stays unset.
- Enabling `ecoflow_cloud_quota` needs that same sign-off. The proposed block stays out of `jobs.py` until `jobs.py` has no other edits.
- If `jobs.py`, the Vercel app shell, or `master-key.env` is already being edited at build time, pause.
- Phase 4 leaves `energy.py` and `ecoflow_public.py`. Exclusive files are archived before any delete. If no GitHub remote still has them, record that and do not delete a repository.

---

## 7. Notes & constraints

- No force-push.
- Secrets stay out of git. Allowlist names: `ECOFLOW_ACCESS`, `ECOFLOW_SECRET`, `ECOFLOW_REGION`, `ECOFLOW_DELTA_2`, `ECOFLOW_RIVER_2_PRO`, `ECOFLOW_DELTA_2_SECONDARY`. Do not print the values. Follow `Energy/lib/envload.py`: an allowlist of key names, never a second env file.
- Prefer small reversible steps.
- Sign-off before any send, speaker playback, OBS, hardware switch, deletion of live Ecosystem files, or cloud spend. The cloud spend gate is `RR_ECOFLOW_CLOUD=1`. It stays unset for this draft and for the build’s default test. Phase 4 deletion is limited to this function’s exclusive old files, and only after they are in `Old repos deleted and merged/ecoflow-quota/`. Do not delete the GitHub repository.
- Small test, at build time: run `quota_poll.py` with `RR_ECOFLOW_CLOUD` unset. Expect exit 0, text `cloud=off`, no new file under `Energy/Cloud-Quota/`, and no request to `api.ecoflow.com`. A fixture map of `pd.soc` through `map_quota_to_fields` proves the field shape without HTTP. Not run for this draft.
- Result note (2026-09-30 HST): Landed `Energy/Cloud-Quota/scripts/quota_poll.py`, `store.py`, and `README.md`. `read_runner._read_api` returns `cloud=off` unless `RR_ECOFLOW_CLOUD=1`, and a signed-off read is labeled `source: cloud` under Database `Energy/Cloud-Quota/`. BLE samples stay in `Energy/samples`. Dry run: exit 0, text `cloud=off`, fixture `pd.soc=55.0`, no file written, no EcoFlow request. `jobs.py` was not edited. Archive path: `Old repos deleted and merged/ecoflow-quota/` (`scripts/ecoflow_quota.py`, `SKILL.md`, `INDEX.md`, `DAILY.md`, `references/migrate.md`, plus the old `__pycache__` bytecode). Left in the old skill folder: `scripts/energy.py`, `scripts/ecoflow_public.py`, and `desk/scheduler.py` (symlink). GitHub deletion: commit `50d3b0a6` on `Solar-Pacific-RootRecord-Server` branch `online-safe-20260920` (remote at `c1ea1dd5`, which contains that commit). Repository was not deleted. No force-push.

---

*Work order prepared 2026-09-30 HST. Update status when closed.*

---

## Archive / location note

This file is a draft. It is not on the active index. Do not auto-promote.

```text
Documentation/06-development/Work-Orders/drafts/EcoFlow_cloud_quota_poll_Work_Order_WO-MIG-36-2026-09-29.md
```

See `drafts/README.md` and WO-WOGEN-001. Do not auto-promote.

**Closed WOs:** set Status → COMPLETE/CLOSED → `git mv` into:

```text
Documentation/06-development/Work-Orders/Complete/
```

Human session logs archive under `Documentation/01-operations/archive/YYYY-Www/` (WO-ARCH) — separate from closed work orders.
