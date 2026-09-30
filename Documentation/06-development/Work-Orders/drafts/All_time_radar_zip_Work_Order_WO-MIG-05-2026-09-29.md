# WORK ORDER — All-time radar zip

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-MIG-05-2026-09-29 |
| **Date** | 2026-09-29 (HST) |
| **Status** | COMPLETE — RadarZip built 2026-09-29; `weather_radar_zip` stays off until `RR_RADAR_ZIP=1` |
| **Owner** | RootRecord |
| **Related** | Agent 05. Old source `weather/radar-archive/scripts/radar_archive.py`. Live poller `Weather/fetch/radar.py`. Later consumer: Agent 20 OBS studio and overlays (do not build it). |

**Scope:** Longer retention for Hawaii radar: frames the live poller already saved are appended into one all-time zip under `Weather/RadarZip`. The poller, the 14-day loose imagery window, and `weather_poller` stay. The scheduled job is in `jobs.py` and stays off.

---

## 1. Intent

The old `radar-archive` job downloaded `https://radar.weather.gov/ridge/standard/HAWAII_loop.gif` every 10 minutes, wrote a timestamped GIF and `radar_archive-current.gif`, and rebuilt `radar_archive.zip` by reading every member into memory. That all-time zip was not copied.

The live weather poller already fetches the same GIF and keeps dated frames for 14 days, then `weather-retention.py` moves them. That fetch and that 14-day rule must be kept. The missing behavior is one append-only zip of those frames, stored outside the 14-day imagery walk, so the loose dated folders can still age out while the zip is kept.

Night-sleep skip on the old job belongs to another agent. Do not rebuild it here. This zip does not fetch, so it only sees frames the poller already wrote.

---

## 2. Current reality

### 2.1 What exists

Folder name: `RadarZip` (capitalized, one name in all three places). No lowercase twin and no symlink. No `Logs/` directory on the server. No `master-key.env` keys.

| Item | Location / status |
| --- | --- |
| Code | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Weather/RadarZip/scripts/radar_zip.py` — package `RadarZip` |
| Database | `2 - RootRecord-Database/Weather/RadarZip/radar_archive.zip` and `radar-archive.json`. Not inside `Weather/Hawai'i` |
| Logs | `2 - RootRecord-Database/Logs/Weather/RadarZip/radar_zip.log` |
| Live fetch | `Weather/fetch/radar.py` writes `HAWAII_loop_current.gif` and dated frames under `2 - RootRecord-Database/Weather/Hawai'i/hfo/radar.weather.gov/ridge/standard/HAWAII_loop/`. Job `weather_poller` is live. Do not replace it |
| 14-day imagery rule | `Weather/scripts/weather-retention.py` keeps GOES / radar / IR-loop / wwamap dated folders 14 days, then moves them. Job `weather_retention` is gated (`enabled: False`, `--dry-run`). Do not change the window and do not turn on `--apply` |
| Old source | `/home/rootrecord/old ollama/old skills/weather/radar-archive/` — git remote `git@github.com:rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server.git`, branch `online-safe-20260920` |
| Old state file | `/home/rootrecord/old ollama/old skills/state/store/radar-archive.json` |
| Frame already on disk | `HAWAII_loop_20260929T220442-1000.gif` (about 213 KB) plus `HAWAII_loop_current.gif` |
| Secrets | None. No key names in `master-key.env` |

### 2.2 Completed so far

- [x] Old source read. Live poller and 14-day retention identified. Folder and three paths named.
- [x] `RadarZip` script, Database zip, state file, and log written.
- [x] Gated `weather_radar_zip` block in `jobs.py`. Off unless `RR_RADAR_ZIP=1` at poller start. Poller was not restarted.
- [x] Local test 2026-09-29 23:58 HST: first run added `HAWAII_loop_20260929T220442-1000.gif` (member count 1); second run added 0. `HAWAII_loop_current.gif` hash and mtime unchanged. Weather poller pid 5264 start time unchanged.
- [x] Phase 4 archive copy and GitHub file deletion. See the result note in section 7.
- [x] Library rows corrected (matrix row 42 and the scheduler `radar-archive` row).

### 2.3 Known friction

- The old zip rewrite loaded every GIF into memory. The new script appends missing members and must not do that rewrite.
- The zip is unbounded. A changed frame is about 200 KB today. Enabling `RR_RADAR_ZIP` is a separate disk sign-off.
- If `weather_retention --apply` moves dated radar folders before those frames are in the zip, the script must also scan `2 - RootRecord-Database/Archive/Previous-Datasets/Weather-*/` for the same GIFs. Do not enable retention apply as part of this function.
- Phase 4 deletes files only from `weather/radar-archive/` and `state/store/radar-archive.json` in the old repo named above. Confirm that remote and branch still hold those paths before the push. Copies under `reports/Stale Root Reports/` are a shared dump — leave them.

---

## 3. Tasks

Build only after this draft is accepted and a build is ordered. Until then, do not edit runtime files, restart services, send messages, actuate hardware, or spend cloud money.

1. Add `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Weather/RadarZip/scripts/radar_zip.py`. It does not HTTP-fetch. It scans the live `HAWAII_loop/archive/` tree and, if present, `Archive/Previous-Datasets/Weather-*/` copies of those same GIFs. It appends missing members to `2 - RootRecord-Database/Weather/RadarZip/radar_archive.zip` (append mode). A second run does not duplicate a name. It writes `radar-archive.json` with counts and paths only. Logs go to `2 - RootRecord-Database/Logs/Weather/RadarZip/`. No `config/` unless a later need appears. No server `Logs/` directory.
2. Propose one gated block in `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Automations/scripts/jobs.py`: id `weather_radar_zip`, `enabled` only when `RR_RADAR_ZIP=1`, default off. Do not enable it in this migration. Do not edit any other job.
3. One local test, no restart: run the script once against the frame already on disk (`HAWAII_loop_20260929T220442-1000.gif`), confirm the zip lists it, run again and confirm the member count stays the same, and confirm `HAWAII_loop_current.gif` and the poller are unchanged.
4. This function does not depend on another migration Folder. Do not pause for Agent 20. Agent 20 (OBS studio and overlays) depends on this Folder later. Do not build OBS.
5. After the migration works, and before Library updates: copy `weather/radar-archive/` (tracked source plus `OFFLOADED`) into `/home/rootrecord/RootRecord-Ecosystem/Old repos deleted and merged/Solar-Pacific-RootRecord-Server/weather/radar-archive/`, keeping the path it had inside the old repo. Also copy `state/store/radar-archive.json` the same way. Generated data that lived beside that source goes into this archive and still does not go into Pacific, Database, the website, or git. After the archive copy is on disk, delete those same files from the old repo on this machine and on GitHub. Commit that deletion and push it. Do not force-push. Do not delete the GitHub repository. If the archive copy fails, do not delete. Leave `reports/Stale Root Reports/` copies and name them here (shared). Do not import the old zip, GIFs, samples, or state into the live Folders.
6. Then update this same work order with what landed, the archive path, the GitHub deletion, and the new status. Correct only the Library pages this function made stale: row 42 of `5 - RootRecord-Library/Documentation/00-architecture/Old-Repo-Migration-Matrix.md` and the `radar-archive` row of `5 - RootRecord-Library/Documentation/00-architecture/G1-Scheduler-To-G3-Jobs-Map-2026-09-29.md`. Do not rewrite unrelated work orders.

---

## 4. Non-goals

- Do not replace the poller, `Weather/fetch/radar.py`, `Weather/core/daily_zip.py`, EcoFlow BLE, the globe collector, camera grabs, Kokoro, or `geology_collect.py`.
- Do not turn on `weather_retention --apply` or change the 14-day imagery window. `weather-retention.py` stays unchanged. The all-time zip lives outside `Weather/Hawai'i`, so that walk does not prune it.
- Do not add a night-sleep gate (another agent's function).
- Do not build OBS, overlays, or any other migration function.
- Do not send messages, play audio, switch hardware, delete live Ecosystem files, or spend cloud money.
- Do not import logs, samples, last-state files, generated reports, collected images, radar frames, zip archives of collected data, database dumps, caches, virtualenvs, `node_modules`, or `__pycache__` into Pacific, Database, the website, or git.
- Do not restore files under `~/.ollama/skills/energy`, automations, or `coms/ssh/local-data-globe`.
- Do not edit other agents' files. Shared live file touched only at build time, and only as a gated-off block: `Automations/scripts/jobs.py`. Shared old dump left in place: `reports/Stale Root Reports/` copies of `radar_archive.zip`, `radar_archive-current.gif`, and `radar-archive.json`.

---

## 5. Key file / path reference

| Path | Role |
|------|------|
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Weather/RadarZip/scripts/radar_zip.py` | New script. Append-only zip. No HTTP fetch. Add at build time |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Weather/RadarZip/` | Package `RadarZip`. Add `__init__.py` only if the script needs the package import |
| `2 - RootRecord-Database/Weather/RadarZip/radar_archive.zip` | All-time zip. Runtime output. Not committed |
| `2 - RootRecord-Database/Weather/RadarZip/radar-archive.json` | Last state: counts and paths only. Runtime output. Not committed |
| `2 - RootRecord-Database/Logs/Weather/RadarZip/` | Logs only |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Weather/fetch/radar.py` | Live fetch. Do not replace |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Weather/scripts/weather-retention.py` | 14-day imagery rule. Do not edit |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Automations/scripts/jobs.py` | At build time, one gated block `weather_radar_zip` (`RR_RADAR_ZIP=1`, default off). No other edit |
| `2 - RootRecord-Database/Weather/Hawai'i/hfo/radar.weather.gov/ridge/standard/HAWAII_loop/` | Live frames the script reads |
| `2 - RootRecord-Database/Archive/Previous-Datasets/` | Read-only scan for radar GIFs retention has already moved |
| `/home/rootrecord/old ollama/old skills/weather/radar-archive/` | Old source to archive in phase 4, then delete from that repo |
| `/home/rootrecord/old ollama/old skills/state/store/radar-archive.json` | Old state. Archive with the source. Do not import it |
| `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/weather/radar-archive/` | Phase 4 archive path (after the copy succeeds) |
| `5 - RootRecord-Library/Documentation/00-architecture/Old-Repo-Migration-Matrix.md` | Correct row 42 only after phase 4 |
| `5 - RootRecord-Library/Documentation/00-architecture/G1-Scheduler-To-G3-Jobs-Map-2026-09-29.md` | Correct the `radar-archive` row only after phase 4 |

---

## 6. Open items

**Additional requirements:**

- Accept this draft before any build.
- Separate sign-off before `RR_RADAR_ZIP=1`. The zip grows without a cap.
- Phase 4 GitHub deletion waits until the archive copy is on disk, and only for this function's old files on `Solar-Pacific-RootRecord-Server` branch `online-safe-20260920`.

---

## 7. Notes & constraints

- No force-push.
- Secrets stay out of git. This function has no `master-key.env` keys. Never print secret values. Never add a second env file.
- Prefer small reversible steps.
- Sign-off gates: no sends, speaker playback, OBS, hardware switching, deletion of live Ecosystem files, or cloud spend. Phase 4 deletion is limited to the old function's files after the archive copy succeeds. `RR_RADAR_ZIP` stays off until disk growth is accepted.
- Small test that proves the new behavior: run `radar_zip.py` once, confirm `radar_archive.zip` contains `HAWAII_loop_20260929T220442-1000.gif`, run it again and confirm the member count is unchanged, and confirm `HAWAII_loop_current.gif` and the poller process are unchanged. No service restart.
- New code wins. Enhance the live archive. Do not copy the old in-memory zip rewrite over the poller.
- Result note (2026-09-29 23:58 HST):
  - Landed: `Weather/RadarZip/scripts/radar_zip.py` and `Weather/RadarZip/__init__.py`. Zip and `radar-archive.json` under `2 - RootRecord-Database/Weather/RadarZip/`. Log under `2 - RootRecord-Database/Logs/Weather/RadarZip/`. `jobs.py` id `weather_radar_zip`, enabled only when `RR_RADAR_ZIP=1` (still off).
  - Archived: `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/weather/radar-archive/` (source plus `OFFLOADED` and `__pycache__`) and `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/state/store/radar-archive.json`.
  - Removed on this machine: `/home/rootrecord/old ollama/old skills/weather/radar-archive/` and `state/store/radar-archive.json`. Local commit `8c9437d0` on branch `online-safe-20260920` of `Solar-Pacific-RootRecord-Server`. That branch has no upstream and no merge-base with GitHub `main`, and `main` does not contain this folder, so that commit was not pushed.
  - Removed on GitHub: `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server-Old` `main`, commit `92d4f66` (`fac2b0e..92d4f66`). `weather/radar-archive` returns 404 on `main`. The repository was not deleted.
  - Left in place (shared): `reports/Stale Root Reports/` copies of the old zip, current GIF, and state JSON; on Server-Old, `origin/ns/apps/core/services/radar_archive.py`, `kilauea/weather-kilauea/desk/live/radar_archive.py`, and ecosystem-index mentions.

---

*Work order prepared 2026-09-29 HST. Update status when closed.*

---

## Archive / location note

**Active / accepted WOs** — filename when saved:

```text
All_time_radar_zip_Work_Order_WO-MIG-05-2026-09-29.md
```

Location when accepted (do not move this file there now):

```text
Documentation/06-development/Work-Orders/
```

**Drafts (not on active index)** — this file stays here until Alexander promotes it:

```text
Documentation/06-development/Work-Orders/drafts/
```

See `drafts/README.md` and WO-WOGEN-001. Do not auto-promote.

**Closed WOs:** set Status → COMPLETE/CLOSED → `git mv` into:

```text
Documentation/06-development/Work-Orders/Complete/
```

Human session logs archive under `Documentation/01-operations/archive/YYYY-Www/` (WO-ARCH) — separate from closed work orders.
