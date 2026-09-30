# WORK ORDER — US all-states weather dataset

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-MIG-11-2026-09-29 |
| **Date** | 2026-09-29 (HST) |
| **Status** | OPEN — collector landed; `/us-states` mounted in the Vercel app; deploy not run |
| **Owner** | RootRecord |
| **Related** | Agent 11. Depends on 7. Public website checkout. Later: 13. Country location pollers. Matrix row 43. |

**Scope:** Port the old US all-states weather collector into Weather folder `US-States`, with data and logs under Database, and one public page in the single Vercel app once that checkout exists. Hawaiʻi weather, EcoFlow, the globe collector, cameras, Kokoro, and `geology_collect.py` stay as they are. This draft is before-documentation only. It is not on the active index and it is not permission to build.

---

## 1. Intent

The old function `operations/weather/fetch_us_weather.py` in GitHub repo `old`, plus the hourly wrapper `operations/cronologicals/since-last-fire/every-hour/fetch-us-weather.py`, collects Open-Meteo and NOAA/NWS observations for United States rows and writes them to sqlite `weather.db`. That 50-state dataset is not in the Ecosystem.

The live system already runs Hawaiʻi weather (`weather_poller` and Pacific `Weather/` fetch, reports, and radar). This dataset is additional website data. It does not replace the Hawaiʻi poller, EcoFlow BLE, the globe collector, camera grabs, Kokoro, or `geology_collect.py`.

How to add it: data only, into the one Vercel site. No old weather-page theme.

---

## 2. Current reality

Folder name in all three places: **US-States**. It sits inside the existing Weather domain. No lowercase twin, no symlink, no second top-level domain, and no `Logs/` directory on the server.

| Place | Path |
| --- | --- |
| Server code | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Weather/US-States/scripts` |
| Database data | `2 - RootRecord-Database/Weather/US-States` |
| Database logs | `2 - RootRecord-Database/Logs/Weather/US-States` |

`master-key.env` key name for this function: `NWS_USER_AGENT` only. It is not set today. No other weather key is required. Open-Meteo needs no key. Do not print values. Do not add a second env file.

### 2.1 What exists

| Item | Location / status |
| --- | --- |
| Old collector | Archived at `Old repos deleted and merged/old/operations/weather/`. Removed from GitHub repo `old` (`91b66eb`). |
| Old hourly wrapper | Archived at `Old repos deleted and merged/old/operations/cronologicals/since-last-fire/every-hour/fetch-us-weather.py`. Removed from GitHub with the collector. |
| US places (shared) | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Geology/config/global-locations.json`. 77 US rows, all 50 states, Hawaiʻi denser (28). Read it. Do not copy or edit it. |
| Hawaiʻi weather | Live under Pacific `Weather/` and Database `Weather/Hawai'i/`. `jobs.py` id `weather_poller` is enabled. Leave it. |
| Public website checkout | `3 - RootRecord-Website` is the one Vercel app. `/us-states` is mounted there. Deploy was not run. |
| Secrets | `/home/rootrecord/master/master-key.env` has no `NWS_USER_AGENT` and no other weather key for this function. |
| Database Weather tree | `2 - RootRecord-Database/.gitignore` ignores `/Weather/`, so a store written there stays out of git. |

### 2.2 Completed so far

- [x] Draft work order written (this file).
- [x] Alexander said to build.
- [x] Public website checkout is in folder 3. `/us-states` is mounted. Deploy was not run.
- [x] Collector, store, and gated job. `/us-states` is in the Vercel app. The earlier HTML file remains under `Weather/US-States/site/`.
- [x] One-state proof test (Wyoming, Open-Meteo, Cheyenne, 2026-09-29).
- [x] Phase 4 archive is on disk, and the three files are removed from repo `old` on GitHub (`cursor/radio-idle-obs-gates`, `91b66eb`). No force-push. The repository was not deleted.
- [x] Phase 5 result note below. Matrix row 43 set to partial.

### 2.3 Known friction

- Build pauses while `3 - RootRecord-Website` has no Vercel checkout. Name the missing function: Public website checkout. Do not create the site.
- `jobs.py`, the Vercel app shell, and `master-key.env` are shared. If one of them is already being edited, pause.
- NWS requires `NWS_USER_AGENT`. Until Alexander sets that key, NWS calls are skipped and Open-Meteo still stores.
- A full 77-location NWS pass is not the proof test. api.weather.gov is paced and easy to overload.
- Repo `old` may have no local checkout. Phase 4 still archives from GitHub first, then deletes only these files. If the archive copy fails, do not delete.

---

## 3. Tasks

Do not start these until Alexander accepts this draft and says to build.

1. If `3 - RootRecord-Website` still has no Vercel checkout, pause and name Public website checkout. Do not build that function.
2. Add `Weather/US-States/scripts/fetch_us_states.py`. Stdlib only (`urllib`), 10 second timeout, one attempt per call, 0.2 second spacing. Read US rows from Geology `config/global-locations.json`. Flags: `--force`, `--dry-run`, `--verbose`, `--state`.
3. Add `Weather/US-States/lib/envload.py` on the Energy `lib/envload.py` pattern. Allowlist is `NWS_USER_AGENT` only. Load `/home/rootrecord/master/master-key.env` only. Never print values. Do not edit `master-key.env`. If the key is unset, skip NWS and still store Open-Meteo.
4. Write runtime output only under Database `Weather/US-States/`: `weather.db` (tables `locations`, `weather`, `daily_sun`, `meta`) and `us-last.json`. Logs only under Database `Logs/Weather/US-States/`. Do not import an old `weather.db`, samples, or last-state files.
5. When the Vercel checkout exists, add one route in that one app. Dark glass cards in the globe overlay style (`rgba(8,10,28,.46)`, blur, 16 px radius). Show `us-last.json` when a read path exists; otherwise an empty state. Do not invent numbers. Do not commit dataset files into the website repo. Do not import an old weather theme, CSS skin, or avaivy background.
6. If `jobs.py` is not already being edited, add one gated block only: id `weather_us_states`, enabled only when `RR_US_STATES=1`, hourly, `nice -n 10`, default off. Do not restart the poller. If `jobs.py` is already being edited, pause.
7. Proof test, one state: `python3 "1 - Servers/1 - RootRecord-Pacific-Solar-Server/Weather/US-States/scripts/fetch_us_states.py" --state WY --force`. Pass means `us-last.json` has a Wyoming Open-Meteo row.
8. After that test passes, copy the three old files listed in section 5 into `/home/rootrecord/RootRecord-Ecosystem/Old repos deleted and merged/old/`, keeping each path from inside repo `old`. Generated data that lived beside that source goes into this archive too, and still does not go into the live Folders. If the archive copy fails, stop and do not delete.
9. After the archive copy is on disk, delete those same three files from repo `old` on this machine and on GitHub. Commit that deletion and push it. Do not force-push. Do not delete the GitHub repository.
10. Update this work order with what landed, the archive path, the GitHub deletion, and the new status. Correct matrix row 43 in `5 - RootRecord-Library/Documentation/00-architecture/Old-Repo-Migration-Matrix.md` only.

---

## 4. Non-goals

- Do not overwrite or replace Pacific `Weather/` Hawaiʻi fetch, reports, radar, hurricanes, or `jobs.py` id `weather_poller`.
- Do not replace EcoFlow BLE, the poller, the globe collector, camera grabs, Kokoro, or `geology_collect.py`.
- Do not build 13. Country location pollers, or any other agent's function.
- Do not edit Geology `config/global-locations.json`. It is shared. Leave `config/locations/global-locations.json` in repo `old`.
- Do not pull `web/sites/avaivy.cloud` themes, backgrounds, CSS skins, or `hawaii-locations.json`. The Geology locations file already has the Hawaiʻi rows.
- Do not open a second website, a second env file, or a `Logs/` directory on the server.
- Do not import logs, samples, last-state files, generated reports, images, radar frames, zip archives, database dumps, caches, virtualenvs, `node_modules`, or `__pycache__` into Pacific, Database, the website, or git.
- Do not restore files under `~/.ollama/skills/energy`, automations, or `coms/ssh/local-data-globe`.
- Do not send messages, play speaker audio, drive OBS, switch hardware, delete live Ecosystem files, or spend cloud money.

---

## 5. Key file / path reference

| Path | Role |
|------|------|
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Weather/US-States/scripts/fetch_us_states.py` | New collector. Add at build. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Weather/US-States/lib/envload.py` | New allowlist loader. Key name `NWS_USER_AGENT` only. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Geology/config/global-locations.json` | Shared US place list. Read only. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Energy/lib/envload.py` | Pattern for the allowlist loader. Do not edit. |
| `2 - RootRecord-Database/Weather/US-States/weather.db` | Runtime store. Gitignored with the rest of `/Weather/`. Do not import the old database. |
| `2 - RootRecord-Database/Weather/US-States/us-last.json` | Runtime snapshot for the public page. Stays out of git. |
| `2 - RootRecord-Database/Logs/Weather/US-States/` | Logs only. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Automations/scripts/jobs.py` | Shared. Proposed gated block `weather_us_states` / `RR_US_STATES=1` only, and only if this file is not already being edited. |
| `/home/rootrecord/master/master-key.env` | Shared secrets file. Do not edit. Allowlist name: `NWS_USER_AGENT`. |
| `3 - RootRecord-Website` | One Vercel app. One new route after checkout exists. UI only; data stays in Database. |
| `1 - Servers/2 - RootRecord-US-Mainland-Server/mirror/network-globe/network-globe/overlay/overlay.css` | Visual reference for glass cards. Do not copy the globe app into the site. |
| `5 - RootRecord-Library/Documentation/08-ideas/2026-09-29-globe-landing-overlay.md` | Visual direction. Read before any UI. |
| `operations/weather/fetch_us_weather.py` | Old source. Phase 4 archive, then remove from repo `old`. |
| `operations/weather/README.md` | Old source note for this function only. Phase 4 archive, then remove from repo `old`. |
| `operations/cronologicals/since-last-fire/every-hour/fetch-us-weather.py` | Old hourly wrapper. Phase 4 archive, then remove from repo `old`. |
| `config/locations/global-locations.json` (repo `old`) | Shared with Geology and later location pollers. Leave it. |
| `5 - RootRecord-Library/Documentation/00-architecture/Old-Repo-Migration-Matrix.md` | Phase 5: correct row 43 only. |
| `/home/rootrecord/RootRecord-Ecosystem/Old repos deleted and merged/old/` | Phase 4 archive root. Keep the old in-repo paths. |

---

## 6. Open items

**Additional requirements:**

- Alexander accepts this draft and says to build before any runtime edit.
- Public website checkout (function 7) must occupy `3 - RootRecord-Website` before the page or the dataset build continues. Until then, pause and name that function.
- Alexander sets `NWS_USER_AGENT` in `master-key.env` when NWS rows are wanted. This work order does not write that file.
- Phase 4 GitHub deletion is ordered only after the archive copy is on disk and the one-state test has passed.
- Phase 5 result note is empty until phase 4 finishes. Do not mark this work order COMPLETE from the draft.

---

## 7. Notes & constraints

- No force-push.
- Secrets stay out of git. List key names, never values.
- Prefer small reversible steps.
- Sign-off gates: sends, speaker playback, OBS, hardware switching, deletion of live Ecosystem files, and cloud spend. Do not do those. Phase 4 is the only ordered deletion, and it is this function's three old files after a good archive copy.
- Proof test: `python3 "1 - Servers/1 - RootRecord-Pacific-Solar-Server/Weather/US-States/scripts/fetch_us_states.py" --state WY --force`. Pass means Database `Weather/US-States/us-last.json` contains a Wyoming Open-Meteo row. Not the full 77-location NWS pass.
- New periodic job stays gated off (`RR_US_STATES` unset). Do not restart services to register it.
- Do not promote this file onto the active Work-Orders index.

### Result note (phase 5)

- Landed: `Weather/US-States/scripts/fetch_us_states.py`, `Weather/US-States/lib/envload.py` (allowlist `NWS_USER_AGENT` only), Database `Weather/US-States/weather.db` and `us-last.json`, log under `Logs/Weather/US-States/`. Job `weather_us_states` in `jobs.py`, enabled only when `RR_US_STATES=1`, default off. Poller was not restarted.
- Proof: `fetch_us_states.py --state WY --force` PASS. `us-last.json` has Cheyenne, provider `open-meteo`, temp 7.3°C, obs `2026-09-30T04:00`. NWS skipped because `NWS_USER_AGENT` is unset.
- Public page: mounted at `3 - RootRecord-Website/src/app/us-states/page.tsx` (glass card). It reads Database `Weather/US-States/us-last.json` on this host and shows an empty state when that file is absent. The snapshot is not committed into the website repo. Vercel deploy was not run.
- Archive path: `Old repos deleted and merged/old/operations/weather/fetch_us_weather.py`, `operations/weather/README.md`, and `operations/cronologicals/since-last-fire/every-hour/fetch-us-weather.py`.
- Removed on GitHub: yes. Repo `old`, branch `cursor/radio-idle-obs-gates`, push `c5b935a..91b66eb`. `operations/weather/fetch_us_weather.py` returns 404. No force-push. The repository was not deleted. Shared `config/locations/global-locations.json` was left in repo `old`.

---

*Work order prepared 2026-09-29 HST. Update status when closed.*

---

## Archive / location note

This file is a draft. It is not on the active index. Do not auto-promote.

```text
US_all_states_weather_dataset_Work_Order_WO-MIG-11-2026-09-29.md
```

Location:

```text
Documentation/06-development/Work-Orders/drafts/
```

See `drafts/README.md` and WO-WOGEN-001. Promotion is Alexander's decision: move into `Documentation/06-development/Work-Orders/`, set Status OPEN or IN PROGRESS, and add a row to the index.

**Closed WOs:** set Status → COMPLETE/CLOSED → `git mv` into:

```text
Documentation/06-development/Work-Orders/Complete/
```

Human session logs archive under `Documentation/01-operations/archive/YYYY-Www/` (WO-ARCH) — separate from closed work orders.
