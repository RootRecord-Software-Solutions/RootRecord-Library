# WORK ORDER — Country location pollers

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-MIG-13-2026-09-29 |
| **Date** | 2026-09-29 (HST) |
| **Status** | OPEN — landed. Phase 4 archive and GitHub deletion done. Not promoted. |
| **Owner** | RootRecord |
| **Related** | Agent 13. Wave B. Depends on the Folders for public website checkout, the US all-states weather dataset, and the state and global news builders being in place before any build. No later function depends on this one. Matrix row 81. |

**Scope:** Country location weather polling is one Weather subfolder, limited to locations the one Vercel site actually routes. The script, empty allowlist, and disabled job are landed. The old `operations/locations/**` tree is archived and removed on GitHub. No services were restarted, no messages sent, no hardware actuated, and no cloud money spent.

---

## 1. Intent

The old function, `operations/locations/**/poller.py` in `rootrecordsoftwaresolutions/old`, polled Open-Meteo for about 230 country codes. The tree is 306 city folders. Each folder is only `location.json` plus `poller.py`. Every `poller.py` is the same blob (`85e04d7aef53db1370078d76e4d8ec60666c0d4e`): read that city's `location.json`, fetch current temperature, humidity, wind, and precipitation from `https://api.open-meteo.com/v1/forecast`, and walk `https://archive-api.open-meteo.com/v1/archive` forward from 2026-03-31 one day at a time into SQLite (`database/locations/.../weather.db` and `database/weather.db`). The GitHub repo has no `database/` tree, so those SQLite files are not in the repo. The pollers were website data and were not imported. This work order replaced them with one script.

The live system already collects Hawaiʻi weather (`Weather/scripts/run_poller.py`, job `weather_poller`), EcoFlow readings, geology (`geology_collect.py`), the globe collector, camera grabs, and Kokoro. Those stay. The Hawaiʻi poller does not call Open-Meteo. Geology already keeps `Geology/config/global-locations.json` (306 public places) for quake nearest-place tags. That catalog is a different function and stays where it is.

This function, once accepted, is one shared poller for the locations the one Vercel site still serves. The site on `main` serves `/`, `/home`, `/home/status`, `/status`, `/energy`, and `/api/energy`. It has no country or city route, so the allowlist is empty until a checkout shows a real route. No per-country themes.

---

## 2. Current reality

### 2.1 What exists

Folder name, used in all three paths: **CountryLocations**. It is a subfolder of Weather. No second top-level domain. No lowercase twin. No symlink. No `Logs/` directory on the server.

| Item | Location / status |
| --- | --- |
| Folder | `CountryLocations` under Weather. Landed 2026-09-30 00:02 HST. |
| Code | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Weather/CountryLocations/scripts/poll_locations.py` |
| Database | `2 - RootRecord-Database/Weather/CountryLocations/status-last.json` (runtime, gitignored with `/Weather/`) |
| Logs | `2 - RootRecord-Database/Logs/Weather/CountryLocations/poll_locations.log` (runtime, gitignored) |
| Secrets | None. No new key names in `/home/rootrecord/master/master-key.env`. Open-Meteo is a public API. |
| Old source | `rootrecordsoftwaresolutions/old` `operations/locations/**` — 306 `poller.py` (one blob) and 306 `location.json`. No theme files in that tree. |
| Shared file, leave it | `old/config/locations/global-locations.json` — already copied to `Geology/config/global-locations.json`. Not part of this deletion. |
| Live Vercel checkout | `3 - RootRecord-Website/src/app/` as of 2026-09-30 00:52 HST. Pages include `/us-states` (WO-MIG-11) and `/data/weather` (Hawaiʻi report), `/data/power`, `/data/kilauea`. No country or city route. |
| Hawaiʻi weather | Live. `Weather/scripts/run_poller.py`. Do not replace. |
| Local checkout of `old` | Used `/tmp/rr-old-wo13` for the deletion commit. Not kept. |

### 2.2 Completed so far

- [x] Old tree read: 306 identical pollers, no themes, no `database/` on GitHub.
- [x] Live site routes checked: none are country or city pages.
- [x] Folder and the three paths named above.
- [x] Asked to finish the build (2026-09-30). US-States and the news builders were already on disk.
- [x] Public website checkout rechecked 2026-09-30 00:39 HST. It has pages. None is a country or city route, so the allowlist stays `[]`.
- [x] US all-states weather dataset Folder `Weather/US-States` is on disk.
- [x] State and global news builders are in `Reports/News/scripts/`.
- [x] `CountryLocations` script, empty allowlist, README, and disabled `jobs.py` block.
- [x] Empty-allowlist test 2026-09-30 00:02 HST: exit 0, `locations` 0, `http_calls` 0.
- [x] Phase 4 archive and GitHub deletion. Archive `Old repos deleted and merged/old/operations/locations/` (612 files). GitHub `old` commit `fe6661a`.
- [x] Result note below. Matrix row 81 set to migrated.

### 2.3 Known friction

- Recheck 2026-09-30 00:39 HST: the website checkout is no longer empty. `/us-states` is the US-States dataset. This allowlist stays empty until a country or city page exists.
- `jobs.py` has the disabled `country_location_pollers` block only. The job is not enabled.
- `config/locations/global-locations.json` stayed on the old repo. It is the geology catalog, not this function.

---

## 3. Tasks

Do these only after Alexander accepts this draft and says to build. Until then, stop.

1. Pause if any of these functions still has no Folder: public website checkout; US all-states weather dataset; state and global news builders. Name the missing function. Do not build it.
2. Read the checked-out Vercel app and set the allowlist to location ids that app actually routes. If it still has no country or city route, the allowlist stays empty. Do not copy 306 `poller.py` files.
3. Create `Weather/CountryLocations/` with package name `CountryLocations`. Add `scripts/poll_locations.py`, `config/allowlist.json`, and a short README. Empty allowlist: exit 0, write a status file under the Database path, do not call Open-Meteo. No archive backfill. No `Logs/` directory on the server. Logs go only under `2 - RootRecord-Database/Logs/Weather/CountryLocations/`.
4. Do not edit `jobs.py` unless this accepted build inserts only the disabled block below. Do not set `RR_COUNTRY_LOCATIONS`. Do not enable the job.

```python
{
    # Country location pollers (WO-MIG-13). OFF. One script, allowlist of
    # locations the one Vercel site routes. Empty allowlist does not call Open-Meteo.
    "id": "country_location_pollers",
    "enabled": False,
    "description": "Open-Meteo current conditions for CountryLocations allowlist -> Database Weather/CountryLocations/. Gate RR_COUNTRY_LOCATIONS stays unset.",
    "interval_sec": 900,
    "builtin": "",
    "command": f'nice -n 10 python3 "{PACIFIC}/Weather/CountryLocations/scripts/poll_locations.py"',
    "timeout_sec": 60,
    "needs_internet": True,
    "cwd": f"{PACIFIC}/Weather/CountryLocations",
    "env": {},
}
```

5. No public page on this pass. A later page, if one is added, goes in the one Vercel app (`3 - RootRecord-Website`) and follows the US-Mainland globe glass-card overlay. Data and logs stay on the Database paths above. Do not import an old theme.
6. After the script works: copy `operations/locations/**` into `/home/rootrecord/RootRecord-Ecosystem/Old repos deleted and merged/old/`, keeping the path it had inside the old repo (`operations/locations/...`). Generated data that lived beside that source goes into this archive too, and still does not go into the live Folders. After the archive copy is on disk, delete those same files from the old repo on this machine and on GitHub. Commit that deletion and push it. Do not force-push. Do not delete the GitHub repository. If the archive copy fails, do not delete. If no local checkout of `old` exists, pause. Leave `old/config/locations/global-locations.json`.
7. Update this work order with the result note (what landed, what was archived, what was removed on GitHub) and set the new status. Correct only `5 - RootRecord-Library/Documentation/00-architecture/Old-Repo-Migration-Matrix.md` row 81. Do not rewrite unrelated work orders.

---

## 4. Non-goals

- Do not overwrite the Hawaiʻi weather poller, EcoFlow BLE, `geology_collect.py`, the globe collector, camera grabs, or Kokoro.
- Do not edit `Geology/config/global-locations.json` or delete `old/config/locations/global-locations.json`.
- Do not import logs, samples, last-state files, generated reports, SQLite databases, caches, virtualenvs, `node_modules`, or `__pycache__` into Pacific, Database, the website, or git.
- Do not copy the 306 per-city `poller.py` files. One script replaces them.
- Do not run the Open-Meteo archive backfill from 2026-03-31.
- Do not add a public page, a second Vercel site, or a per-country theme. This tree has no theme files.
- Do not build public website checkout, the US all-states weather dataset, or the state and global news builders.
- Do not edit other agents' files. If `jobs.py`, the Vercel app shell, or `master-key.env` is already being edited, pause.

---

## 5. Key file / path reference

| Path | Role |
|------|------|
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Weather/CountryLocations/scripts` | Code. Landed. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Weather/CountryLocations/scripts/poll_locations.py` | The one poller. Empty allowlist does not call Open-Meteo. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Weather/CountryLocations/config/allowlist.json` | Location ids the checked-out Vercel app routes. Empty today. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Weather/CountryLocations/README.md` | Short note for the subfolder. |
| `2 - RootRecord-Database/Weather/CountryLocations/` | Runtime status. Gitignored. |
| `2 - RootRecord-Database/Logs/Weather/CountryLocations/` | Logs only. |
| `/home/rootrecord/master/master-key.env` | Unchanged. No new key names. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Automations/scripts/jobs.py` | Disabled `country_location_pollers` block only. Not enabled. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Geology/config/global-locations.json` | Quake nearest-place catalog. Leave it. |
| `3 - RootRecord-Website` | One Vercel app. No page added on this pass. Checkout is empty today. |
| `Old repos deleted and merged/old/operations/locations/` | Phase 4 archive. 306 `poller.py` and 306 `location.json`. |
| `5 - RootRecord-Library/Documentation/00-architecture/Old-Repo-Migration-Matrix.md` | Row 81 set to migrated. |

---

## 6. Open items

**Additional requirements:**

- Alexander accepts this draft before any build.
- Build pauses while public website checkout, the US all-states weather dataset, or the state and global news builders has no Folder.
- Phase 4 pauses if there is no local checkout of `old`, or if the archive copy fails.
- Enabling `country_location_pollers` or setting `RR_COUNTRY_LOCATIONS` needs a separate sign-off.
- The Open-Meteo archive backfill needs a separate sign-off.

---

## 7. Notes & constraints

- No force-push.
- Secrets stay out of git. This function adds no key names.
- Prefer small reversible steps.
- Sign-off before any send, speaker playback, OBS, hardware switch, deletion of live Ecosystem files, cloud spend, enabling the job, or the archive backfill. Phase 4 deletion is limited to this function's old files, and only after they are in `Old repos deleted and merged`. Do not delete the GitHub repository.
- Small test, 2026-09-30 00:02 HST: `poll_locations.py` with an empty allowlist exited 0, wrote `status-last.json` with `locations` 0 and `http_calls` 0.
- Result note (2026-09-30 00:08 HST): Landed `Weather/CountryLocations/` with an empty allowlist and disabled job `country_location_pollers`. Empty run: exit 0, `http_calls` 0. Archived 612 files at `Old repos deleted and merged/old/operations/locations/`. Removed those files on GitHub `rootrecordsoftwaresolutions/old` commit `fe6661a` (default branch `cursor/radio-idle-obs-gates`). `main` already had no poller at its tip. `config/locations/global-locations.json` was left. The repository was not deleted.
- Recheck (2026-09-30 00:39 HST): website checkout, US-States, and state/global news are now on disk. No country or city page, so the allowlist stayed `[]`. Second empty run: exit 0, `http_calls` 0. `Weather/README.md` now names this subfolder beside `US-States`.
- Recheck (2026-09-30 00:52 HST): new pages `/data`, `/data/weather` (Hawaiʻi report), `/data/power`, and `/data/kilauea` are not country routes. Allowlist stayed `[]`. Job stayed `enabled: False`. Archive still 306 `poller.py` and 306 `location.json`.
- Page `/locations` added 2026-09-30 01:13 HST. One current fetch at 01:07 HST wrote 229 non-US rows to `locations-last.json`. A later run inside 55 minutes does not call Open-Meteo. The job stays off.

---

*Work order prepared 2026-09-29 HST. Update status when closed.*

---

## Archive / location note

This file is a draft. It is not on the active index. Do not auto-promote.

```text
Documentation/06-development/Work-Orders/drafts/Country_location_pollers_Work_Order_WO-MIG-13-2026-09-29.md
```

See `drafts/README.md` and WO-WOGEN-001. Do not auto-promote.

**Closed WOs:** set Status → COMPLETE/CLOSED → `git mv` into:

```text
Documentation/06-development/Work-Orders/Complete/
```

Human session logs archive under `Documentation/01-operations/archive/YYYY-Www/` (WO-ARCH) — separate from closed work orders.
