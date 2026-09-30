# WORK ORDER — OBS studio and overlays

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-MIG-20-2026-09-29 |
| **Date** | 2026-09-29 (HST) |
| **Status** | OPEN — draft, not accepted for execution |
| **Owner** | RootRecord |
| **Related** | Agent 20. Reads agent 04 RAMMB tracks and plot, and agent 05 all-time radar zip. Live still catalog: `Geology/scripts/kilauea_cams.py`. |

**Scope:** Add one on-demand overlay file sender under the existing Media domain. It writes a JSON overlay and a static HTML page from storm, radar, and Kīlauea catalog files already on disk. It does not start OBS, open a socket, or replace the still catalog. This file stays in `drafts/` and is not on the active work-order index.

---

## 1. Intent

The old kit in `/home/rootrecord/old ollama/old skills/obs-studio` (git `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server`) drove OBS WebSocket 5: scene collections, browser sources, rotation, and `apply_obs_scenes`. `weather/hurricane-obs/scripts/job.py` called `apply_hurricane_kit` only when OBS work was allowed. `weather/official-weather-media` pushed official graphics into scenes the same way. Kīlauea YouTube ids were scraped and pushed into browser sources (`obs_cam_url`, `push_embeds_to_current_collection`). A separate helper, `solar_obs_server.py`, listened on port 8765.

The live system keeps the USGS V1/V2/V3 still catalog and catalog embed ids in `Geology/scripts/kilauea_cams.py`. RAMMB per-storm tracks and the text plot are in `Weather/hurricanes/scripts/storm_track.py` and `storm_plot.py`. The all-time radar zip writer is `Weather/RadarZip/scripts/radar_zip.py`. There is no OBS process and no overlay sender in Pacific. This work adds a file sender. It does not copy the WebSocket driver over the live catalog.

---

## 2. Current reality

### 2.1 What exists

| Item | Location / status |
| --- | --- |
| Folder | `Overlays`, a subfolder of the existing Media domain. No new top-level folder. No lowercase twin. No symlink. |
| Server code | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Media/Overlays/scripts` (package `Overlays`). Not created yet. |
| Database data | `2 - RootRecord-Database/Media/Overlays/` (`overlay-last.json` and the static HTML page when this runs). Not created yet. |
| Database logs | `2 - RootRecord-Database/Logs/Media/Overlays/` only. No `Logs/` directory on the server. |
| Secrets | None for the file sender. A later WebSocket sign-off would allowlist only `OBS_WS_URL` and `OBS_WS_PASSWORD` from `/home/rootrecord/master/master-key.env`, following `Energy/lib/envload.py` (allowlist of key names, never print values, no second env file). This draft does not read those values and does not add them. |
| Live catalog | `Geology/scripts/kilauea_cams.py` stills and catalog embed ids. Keep. |
| Dependency folders | `Weather/hurricanes/scripts/storm_track.py`, `storm_plot.py`, and `Weather/RadarZip/scripts/radar_zip.py` are on disk as of this draft. |
| Old source | `old ollama/old skills/obs-studio/` and `old ollama/old skills/weather/hurricane-obs/`. |
| Proposed job | `media_obs_overlay` / `RR_OBS_OVERLAY` is not in `jobs.py` and stays off. On demand only. |

### 2.2 Completed so far

- [x] Live Kīlauea still catalog and catalog embed ids
- [x] RAMMB track and plot scripts on disk
- [x] All-time radar zip script on disk
- [ ] Overlay file sender
- [ ] Archive of this function's old files, then removal from the old repo locally and on GitHub

### 2.3 Known friction

- The old WebSocket helper, the port 8765 server, and YouTube live-id scraping are the same historical function as the slides this sender replaces. They stay behind sign-off. This draft does not port them.
- `kilauea_cams.py`, `weather/hurricane-tracker` (`apply_hurricane_kit`), and `weather/official-weather-media` (HLS fetch mixed with `apply_obs_scenes`) are shared with other functions. They stay in the old tree.
- GitHub deletion of the old files waits until the sender works and the archive copy is on disk. No force-push.

---

## 3. Tasks

1. Pause if `Weather/hurricanes/scripts/storm_track.py` or `storm_plot.py` is missing. Name RAMMB per-storm tracks and plot. Do not build that function.
2. Pause if `Weather/RadarZip/scripts/radar_zip.py` is missing. Name all-time radar zip. Do not build that function.
3. Pause if `jobs.py`, the Vercel app shell, or `master-key.env` is already being edited.
4. Add `Media/Overlays/` with package `Overlays` and `scripts/overlay_sender.py`. On demand, read files already on disk and write `overlay-last.json` plus a static HTML browser page under `2 - RootRecord-Database/Media/Overlays/`. Inputs: `storm-plot.txt` and `storm-tracks.json` from the hurricane board output, the radar zip path from RadarZip (path only; do not unzip and do not fetch), and the three catalog still URLs and embed URLs from the live cam catalog. Do not bind a port, connect to `ws://localhost:4455`, start OBS or a stream, scrape YouTube, or download graphics. Do not write under `~/.ollama`.
5. Do not edit `jobs.py`. Record this proposed block here only. It stays unregistered and off:

```text
# PROPOSED — do not register until a separate sign-off
# id: media_obs_overlay
# env: RR_OBS_OVERLAY=1
# schedule: on demand
# enabled: False
```

6. One test on a temp database root: a fixture plot line plus the three catalog still URLs produces JSON with storm, radar, and cam fields. The run opens no socket. Do not write the live Database path.
7. After that works: archive `obs-studio/` source and `weather/hurricane-obs/` into `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/`, keeping the paths they had inside the old repo. Generated `store/obs-quake-feed.json` goes to that archive and does not go into Database git. Then delete those same paths from the old repo on this machine and on GitHub. Commit that deletion and push it. Do not force-push. Do not delete the GitHub repository. If the archive copy fails, do not delete.
8. Update this work order with what landed, the archive path, and the GitHub deletion. Correct only the Library lines that still say OBS overlays are absent: Old-Repo-Migration-Matrix rows 41 and 56 and blocker 3, and the OBS half of the blocked line in Pacific `Weather/README.md`. Leave the storm-radio half of that line.

Both dependency folders are on disk as of this draft. The pause in tasks 1 and 2 still applies at build time.

---

## 4. Non-goals

- Do not replace the EcoFlow BLE poller, Hawaiʻi weather, the globe collector, camera grabs, Kokoro, `geology_collect.py`, or `Geology/scripts/kilauea_cams.py`.
- Do not build OBS WebSocket, a listening overlay server (`solar_obs_server.py` on port 8765), scene changes, streaming, speaker playback, sends, or hardware switching.
- Do not edit other agents' files. Hurricane radio, report playback, morning boot replay, and sunrise restore are other functions.
- Shared old files stay: `kilauea/kilauea-cams/scripts/kilauea_cams.py`, `weather/hurricane-tracker`, and `weather/official-weather-media`.
- Do not edit `jobs.py`.
- Do not import logs, samples, images, radar frames, zip archives of collected data, caches, or dumps into Pacific, Database git, the website, or this work order's runtime.
- Do not open a second top-level domain. Do not add a public website page. Do not re-import Android apps. Do not touch `/snap/obs-studio`.

---

## 5. Key file / path reference

| Path | Role |
|------|------|
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Media/Overlays/scripts/overlay_sender.py` | Add. File sender. Package `Overlays`. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Media/Overlays/__init__.py` | Add. Package name matches the folder. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Geology/scripts/kilauea_cams.py` | Read the still catalog. Do not overwrite. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Weather/hurricanes/scripts/storm_track.py` | Dependency. Pause if missing. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Weather/hurricanes/scripts/storm_plot.py` | Dependency. Pause if missing. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Weather/RadarZip/scripts/radar_zip.py` | Dependency. Pause if missing. Read the zip path only. |
| `2 - RootRecord-Database/Media/Overlays/overlay-last.json` | Sender output |
| `2 - RootRecord-Database/Media/Overlays/` static HTML page | Browser-source page. No listening server. |
| `2 - RootRecord-Database/Logs/Media/Overlays/` | Run log only |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Automations/scripts/jobs.py` | Do not edit. Proposed gate stays in this draft. |
| `5 - RootRecord-Library/Documentation/00-architecture/Old-Repo-Migration-Matrix.md` | After phase 4, correct rows 41 and 56 and blocker 3 |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Weather/README.md` | After phase 4, correct the OBS half of the blocked line. Leave storm radio. |

---

## 6. Open items

**Additional requirements:**

- Build waits until Alexander accepts this draft and says to build.
- OBS WebSocket, the port 8765 server, scene changes, and streaming need a separate sign-off. Key names for that later gate, not used by the file sender: `OBS_WS_URL`, `OBS_WS_PASSWORD`.
- Shared old files named in section 4 stay even after phase 4.

---

## 7. Notes & constraints

- No force-push.
- Secrets stay out of git. The file sender has no `master-key.env` keys. Do not print env values.
- Prefer small reversible steps.
- Sends, speaker playback, OBS, hardware switching, deletion of live Ecosystem files, and cloud spend need Alexander's sign-off. This draft does none of those. Phase 4 deletes only `obs-studio/` and `weather/hurricane-obs/` in the old repo, and only after the archive copy is on disk.
- One test that proves the new behavior: temp database root, fixture plot line, three catalog still URLs. The written JSON has storm, radar, and cam fields. The process opens no socket.

---

*Work order prepared 2026-09-30 HST. Update status when closed.*

---

## Archive / location note

**Draft (not on active index):**

```text
Documentation/06-development/Work-Orders/drafts/OBS_studio_and_overlays_Work_Order_WO-MIG-20-2026-09-29.md
```

Do not auto-promote. The result note (what landed, archive path, GitHub deletion) is added to this file after phase 4.
