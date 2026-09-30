# WORK ORDER — State and global news builders

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-MIG-12-2026-09-29 |
| **Date** | 2026-09-29 (HST) |
| **Status** | BUILT — result recorded in this draft; not promoted to the active index |
| **Owner** | RootRecord |
| **Related** | Agent 12. Depends on agent 07 (Public website checkout) for the public page only. Agent 13 (Country location pollers) depends on this function later. Matrix row 80. Live Hawaiʻi collector: Pacific `Reports/News/`. |

**Scope:** Extend the live Hawaiʻi news collector so the other 49 states and a global index can be built from official state portals, with data under Database `Reports/News/` and a later page on the one Vercel site. This draft does not authorize runtime edits, a `jobs.py` change, a deploy, or deletion from the old repo. Those wait until this draft is accepted and Alexander says to build.

---

## 1. Intent

G0 `rootrecordsoftwaresolutions/old` (default branch `cursor/radio-idle-obs-gates`) collected official state-government news for all 50 states and folded those databases into one public index.

Each `operations/news/<state>/news.py` only set a slug, a portal URL, and a SQLite path, then called `_collector.run`. `state_portals.json` holds the 50 portal URLs. `build_state_news.py` was the hourly orchestrator: skip a state checked within 55 minutes, `--backfill` when the database is empty, 8 workers, 120s per state, paths hard-coded under `/home/ava-core`. `build_global_news.py` read `database/states/*/*_news.db` (and an optional `database/global/global_news.db`) and wrote `web/sites/avaivy.cloud/data/global-news.json` (top 5000 posts, 1000 events, collection health). It attached `config/locations/global-locations.json` when that file existed. Cronologicals launchers called those scripts (`every-hour/build-state-news.py`, `every-5-minutes/global-news.py`, `every-10-minutes/global-news.py`, `every-10-minutes/all-states-news.py`, and `on-time/*/<state>-news.py`).

The live system already has the shared collector and the Hawaiʻi wrapper. That behavior stays. This work adds the other states and the global index on top of it. Hawaiʻi keeps its 16 seed feeds. The 49 duplicate wrappers are not copied in as 49 scripts.

---

## 2. Current reality

Folder name: **News**, under the existing **Reports** domain. No new top-level folder.

| Place | Path |
| --- | --- |
| Server code | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Reports/News/scripts` (portal list in `Reports/News/config/`) |
| Database data | `2 - RootRecord-Database/Reports/News/` |
| Database logs | `2 - RootRecord-Database/Logs/Reports/News/` |
| Public page (after agent 07) | `3 - RootRecord-Website` — UI only; data and logs stay on the Database paths |

Secrets: none. Public official pages only. No `master-key.env` keys.

### 2.1 What exists

| Item | Location / status |
| --- | --- |
| Shared collector | Pacific `Reports/News/scripts/_collector.py`. Live. Official `.gov` host check, seed feeds, `RR_NEWS_SEEDS_ONLY`, crawl caps. |
| Hawaiʻi wrapper | Pacific `Reports/News/scripts/hawaii_news.py`. 16 seed feeds. Writes `Reports/News/hawaii/hawaii_news.db` and `hawaii-news-last.json`. |
| Hawaiʻi job | `reports_hawaii_news` (`RR_HAWAII_NEWS`, 10:00, `RR_NEWS_SEEDS_ONLY=1`) is proposed. It is not in `jobs.py`. |
| Live Database store | `2 - RootRecord-Database/Reports/News/` has no store yet. The 278-post pass used a temp root. |
| SQLite gitignore | `2 - RootRecord-Database/.gitignore` already ignores `/Reports/News/**/*.db`, `*.db-wal`, `*.db-shm`. |
| Website | `3 - RootRecord-Website` is empty. Agent 07 checks out the one Vercel app. |
| G0 builders | `operations/news/build_state_news.py`, `build_global_news.py`, `state_portals.json`, 50 `news.py` wrappers. Not ported. |
| Globe visual language | Mainland `mirror/network-globe/network-globe/overlay/overlay.css` class `.ov-glass`: `rgba(8,10,28,.46)`, 1px light border, 16px radius, `blur(14px)`. |

### 2.2 Completed so far

- [x] Hawaiʻi collector and shared `_collector.py` ported (2026-09-29). Seed-feed retest: 278 posts, temp root.
- [x] This draft work order written. Not promoted to the active index.
- [x] `state_portals.json`, `state_event_sources.json`, `state_news.py`, `build_state_news.py`, `build_global_news.py` in Pacific `Reports/News/`.
- [x] Temp-root smoke test (Wyoming, then the global index). PASS.
- [ ] Public news page on the Vercel app. Paused: `3 - RootRecord-Website` is empty. Named dependency: Public website checkout (agent 07).
- [x] Phase 4 archive and old-repo deletion (`ec11eca`).
- [x] Phase 5 result note and Library corrections (matrix row 80, News README).

### 2.3 Known friction

- Portal discovery alone returned 0 Hawaiʻi posts (25 × HTTP 404). Seeds fixed Hawaiʻi. The other 49 states have no seed lists in G0. A first run can legally record empty source health. An empty state must show up in collection health.
- Eight parallel collectors is the G0 default. This desk uses 2 workers.
- `build_state_news.py` on G0 points at `/home/ava-core`. The port uses `RR_DATABASE_ROOT`.
- `jobs.py`, `master-key.env`, and the Vercel app shell are shared. If another agent is editing one of them, pause and do not take the file.
- The public page needs agent 07. If `3 - RootRecord-Website` is still empty when the build starts, pause that page and name Public website checkout. Do not check the site out here.

---

## 3. Tasks

Build only after Alexander accepts this draft and says to build. Until then, do not edit runtime files, restart services, send messages, actuate hardware, or spend cloud money.

1. Add `Reports/News/config/state_portals.json` from the G0 portal list, including Hawaiʻi.
2. Add `Reports/News/scripts/state_news.py`: `--state <slug>`, portal from that JSON, database and last-file at Database `Reports/News/<slug>/`. Same summary shape as Hawaiʻi. If the slug is `hawaii`, exit with a message to use `hawaii_news.py`.
3. Add `Reports/News/scripts/build_state_news.py`: freshness window 55 minutes, empty database means `--backfill`, default 2 workers, 120s per state. Hawaiʻi goes through `hawaii_news.py` so the 16 seeds stay. Paths use `RR_DATABASE_ROOT` (default `2 - RootRecord-Database`), not `/home/ava-core`.
4. Add `Reports/News/scripts/build_global_news.py`: read those state databases, write Database `Reports/News/global/global-news-last.json` (bounded index plus collection health, empty states visible). Leave `locations` empty. Agent 13 owns `global-locations.json`. Do not build country pollers.
5. Copy `state_event_sources.json` into `Reports/News/config/` as config only. It records that weather and earthquakes stay out. Do not fetch the NWS calendar.
6. Git-ignore new `*-news-last.json` files and `global-news-last.json` under Database `Reports/News/`. The already-tracked Hawaiʻi summary, if it is tracked later, stays tracked; this ignore is for new runtime output.
7. Logs, if any file is written, only under `2 - RootRecord-Database/Logs/Reports/News/`. No `Logs/` directory on the server.
8. Propose the gated `jobs.py` block in this work order (section 6). During the build, also record it in `Reports/News/README.md`. Do not edit `Automations/scripts/jobs.py` while another agent may be in it. Flags default off: `RR_STATE_NEWS`, `RR_GLOBAL_NEWS`.
9. Public page: pause if `3 - RootRecord-Website` is still empty and name Public website checkout (agent 07). When that shell exists, add one news route that reads the Database JSON. Match the globe overlay glass card (dark glass, 16px radius, blur). Do not import `avaivy.cloud/css/news.css`, geography news HTML, or any old skin. Do not deploy. A Vercel deploy is cloud spend and needs a separate sign-off.
10. Smoke test, temp root only, one state, crawl caps lowered. Pass rule is in section 7. Nothing written under the live Database root.

---

## 4. Non-goals

- Do not replace `_collector.py`, `hawaii_news.py`, EcoFlow BLE, the poller, Hawaiʻi weather, the globe collector, camera grabs, Kokoro, or `geology_collect.py`.
- Do not build agent 13 country location pollers, and do not copy `config/locations/`.
- Do not import old news-page CSS, static geography news HTML, or the avaivy site. Those stay for the website checkout agent. Name them as shared and leave them in the old repo.
- Do not import generated SQLite, `global-news.json`, feed dumps, logs, samples, caches, virtualenvs, `node_modules`, or `__pycache__` into Pacific, Database, the website, or git. Bring source and config only.
- Do not edit `jobs.py`, `master-key.env`, or the Vercel shell if another agent is already in that file.
- No sends, speaker playback, OBS, hardware switching, deletion of live Ecosystem files, or cloud spend.
- Do not open a second top-level domain, a second Vercel site, or a lowercase twin of `News`.
- Do not delete the GitHub repository `rootrecordsoftwaresolutions/old`. Phase 4 removes only this function's old files, and only after the archive copy is on disk.

---

## 5. Key file / path reference

| Path | Role |
|------|------|
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Reports/News/scripts/_collector.py` | Live shared collector. Keep. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Reports/News/scripts/hawaii_news.py` | Live Hawaiʻi wrapper. Keep. Called by the orchestrator for slug `hawaii`. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Reports/News/config/state_portals.json` | Add. 50 portal URLs. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Reports/News/config/state_event_sources.json` | Add. Config only. Weather and earthquakes excluded. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Reports/News/scripts/state_news.py` | Add. One wrapper for the other 49 slugs. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Reports/News/scripts/build_state_news.py` | Add. Freshness orchestrator. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Reports/News/scripts/build_global_news.py` | Add. Index builder. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Reports/News/README.md` | Extend during the build with the gated job proposal. |
| `2 - RootRecord-Database/Reports/News/<slug>/` | Runtime SQLite and `<slug>-news-last.json`. Git-ignored output. |
| `2 - RootRecord-Database/Reports/News/global/global-news-last.json` | Runtime global index. Git-ignored. |
| `2 - RootRecord-Database/Logs/Reports/News/` | Logs only. |
| `2 - RootRecord-Database/.gitignore` | Extend so new last-JSON files stay out of git. |
| `3 - RootRecord-Website` | News route, only after agent 07. Pause and name that function if the folder is empty. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Automations/scripts/jobs.py` | Shared. Proposed block is below. Do not edit during a collision. |
| `5 - RootRecord-Library/Documentation/00-architecture/Old-Repo-Migration-Matrix.md` | Phase 5: correct row 80 only. |
| `Old repos deleted and merged/old/` | Phase 4 archive. Preserve the path each file had inside the old repo. |

G0 sources read for this draft (not copied yet): `operations/news/build_state_news.py`, `build_global_news.py`, `state_portals.json`, `state_event_sources.json`, and the thin `operations/news/<state>/news.py` wrappers.

---

## 6. Open items

**Additional requirements:**

- Alexander accepts this draft and says to build before any of section 3 runs.
- Public page waits on agent 07 (Public website checkout) if folder 3 is empty.
- `locations` in the global index stays empty until agent 13 lands. This work order does not build that function.
- Gated job registration is proposed here. It is not applied.

Proposed blocks for Pacific `Automations/scripts/jobs.py`. Both stay off unless the flag is `1` in the poller's environment at process start. Do not paste them until this work order is accepted and `jobs.py` is free.

`EVERY_HOUR`:

```python
    {
        "id": "reports_state_news",
        "enabled": os.environ.get("RR_STATE_NEWS", "0") == "1",
        "description": "49 state portals via state_news.py; Hawaiʻi via hawaii_news.py. Skip fresh DBs. Default off.",
        "only_at_hours": [],
        "builtin": "",
        "command": f'nice -n 10 python3 "{PACIFIC}/Reports/News/scripts/build_state_news.py"',
        "timeout_sec": 3600,
        "needs_internet": True,
        "cwd": f"{PACIFIC}/Reports/News/scripts",
        "env": {},
    },
    {
        "id": "reports_global_news",
        "enabled": os.environ.get("RR_GLOBAL_NEWS", "0") == "1",
        "description": "Aggregate Reports/News state DBs into global/global-news-last.json. Default off.",
        "only_at_hours": [],
        "builtin": "",
        "command": f'nice -n 10 python3 "{PACIFIC}/Reports/News/scripts/build_global_news.py"',
        "timeout_sec": 120,
        "needs_internet": False,
        "cwd": f"{PACIFIC}/Reports/News/scripts",
        "env": {},
    },
```

`RR_HAWAII_NEWS` stays the separate proposed daily job. This hourly orchestrator also calls `hawaii_news.py` when that state's database is stale, so the two gates can both be off.

---

## 7. Notes & constraints

- No force-push.
- Secrets stay out of git. This function has no secret keys.
- Prefer small reversible steps.
- Sign-off gates: sends, speaker playback, OBS, hardware switching, deletion of live Ecosystem files, and cloud spend (including a Vercel deploy) need Alexander's sign-off. Do not do those things under this draft.
- Phase 4 is already ordered for later, and only after the migration works: archive this function's old files, then remove them from `rootrecordsoftwaresolutions/old` locally and on GitHub. Commit that deletion and push it. If the archive copy fails, do not delete. Do not delete the repository.
- New periodic jobs stay gated off (`RR_STATE_NEWS` and `RR_GLOBAL_NEWS` default `0`).

**Smoke test** (temp root, one state, lowered caps). Run from Pacific `Reports/News/scripts` after the scripts exist:

```text
RR_DATABASE_ROOT=/tmp/rr-mig-12 \
RR_NEWS_MAX_FEEDS=3 RR_NEWS_MAX_PAGES=2 RR_NEWS_MAX_SITEMAPS=1 RR_NEWS_MAX_ARTICLES=5 \
python3 state_news.py --state wyoming
RR_DATABASE_ROOT=/tmp/rr-mig-12 python3 build_global_news.py
```

Pass: both return rc 0, `/tmp/rr-mig-12/Reports/News/wyoming/wyoming_news.db` exists, a Wyoming last JSON exists, and `global-news-last.json` has a collection-health row for Wyoming. The live Database root is unchanged.

### Phase 4 archive list (after the build works)

Archive root: `/home/rootrecord/RootRecord-Ecosystem/Old repos deleted and merged/old/`, keeping each file's path inside the old repo. Generated data that lived beside that source goes into this archive too, and still does not go into the live Folders.

Archive, then delete from the old repo on this machine and on GitHub:

- `operations/news/build_state_news.py`
- `operations/news/build_global_news.py`
- `operations/news/state_portals.json`
- `operations/news/state_event_sources.json`
- `operations/news/news.txt`
- `operations/news/news_tree.txt`
- `operations/news/<state>/news.py` for the 49 states other than Hawaiʻi
- `operations/cronologicals/since-last-fire/every-hour/build-state-news.py`
- `operations/cronologicals/since-last-fire/every-10-minutes/all-states-news.py`
- `operations/cronologicals/since-last-fire/every-10-minutes/global-news.py`
- `operations/cronologicals/since-last-fire/every-5-minutes/global-news.py`
- `operations/cronologicals/on-time/*/<state>-news.py` except `on-time/10:00/hawaii-news.py`

Leave, and keep named here:

- `operations/news/_collector.py`, `operations/news/hawaii/news.py`, `operations/news/collect_hawaii_news.py`, `operations/news/README.md` (shared with the live Hawaiʻi collector)
- `operations/cronologicals/on-time/10:00/hawaii-news.py` and `operations/cronologicals/archive/legacy-news/`
- `web/sites/avaivy.cloud/` including `css/news.css`, and `origin/.../geography/news/` (website checkout and country pages)
- `config/locations/` (agent 13)

### Phase 4 result

Built 2026-09-29. Landed in Pacific `Reports/News/`: `config/state_portals.json`, `config/state_event_sources.json`, `scripts/state_news.py`, `scripts/build_state_news.py`, `scripts/build_global_news.py`. Hawaiʻi collector unchanged. `jobs.py` not edited. Public page not built: folder 3 is empty (Public website checkout).

Smoke PASS, temp root `/tmp/rr-mig-12`, caps 3/2/1/5: `state_news.py --state wyoming` rc 0 (0 posts, source health 2 empty / 3 error), `build_global_news.py` rc 0 (50 health rows, Wyoming `empty`, `locations` []). Live Database `Reports/News/` was not created.

Archive: `/home/rootrecord/RootRecord-Ecosystem/Old repos deleted and merged/old/` (109 files, old-repo paths kept). That set includes `operations/cronologicals/since-last-fire/every-10-minutes/README.md` because it only documented these news launchers. No generated SQLite lived in the old repo.

GitHub deletion: `rootrecordsoftwaresolutions/old` branch `cursor/radio-idle-obs-gates`, commit `ec11ecadaae83b67a33638f653879f6353712a4b` (`0c2bfdb..ec11eca`). Repository not deleted. No force-push. Confirmed `build_state_news.py` is 404 and `operations/news/hawaii/news.py` plus `_collector.py` remain.

Left in the old repo: `operations/news/_collector.py`, `hawaii/news.py`, `collect_hawaii_news.py`, `README.md`; `operations/cronologicals/on-time/10:00/hawaii-news.py`; `operations/cronologicals/archive/legacy-news/`; `web/sites/avaivy.cloud/` (including `css/news.css`); `origin/.../geography/news/`; `config/locations/`.

Library: matrix row 80 set to migrated, and the product/missing counts on that page adjusted by one. Pacific `Reports/News/README.md` check-later item 3 now records the port.

---

*Work order prepared 2026-09-29 HST. Update status when closed.*

---

## Archive / location note

This file is a draft. It is not on the active index. Do not promote it until Alexander accepts it.

```text
Documentation/06-development/Work-Orders/drafts/State_and_global_news_builders_Work_Order_WO-MIG-12-2026-09-29.md
```

See `drafts/README.md` and WO-WOGEN-001. Do not auto-promote.

**Closed WOs:** set Status → COMPLETE/CLOSED → `git mv` into:

```text
Documentation/06-development/Work-Orders/Complete/
```

Human session logs archive under `Documentation/01-operations/archive/YYYY-Www/` (WO-ARCH) — separate from closed work orders.
