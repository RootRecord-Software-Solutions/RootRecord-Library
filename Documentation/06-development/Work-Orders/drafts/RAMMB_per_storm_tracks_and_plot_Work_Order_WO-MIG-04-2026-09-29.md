# WORK ORDER — RAMMB per-storm tracks and plot

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-MIG-04-2026-09-29 |
| **Date** | 2026-09-29 (HST) |
| **Status** | COMPLETE — migrated 2026-09-29. Not promoted to the active index. |
| **Owner** | RootRecord |
| **Related** | Agent 04. Later consumer: agent 20 OBS studio and overlays. Live board: `Weather/hurricanes/scripts/global_board.py`. |

**Scope:** Extend the live worldwide hurricane board with RAMMB per-storm pages (IR gif URL plus official track tables), persist those tracks, and write the Hawaiʻi text plot. Do not replace the board, do not build OBS, and do not turn the proposed global-board job on. This file stays in `drafts/` and is not on the active work-order index.

---

## 1. Intent

The old `weather/hurricane-tracker` processor listed storms from NHC, RAMMB, and JTWC, then for each merged storm (max 14) fetched `storm.asp?storm_identifier=…`. It resolved the 4 km IR gif URL, parsed the official Forecast Hour and Track History tables, and stored the last 24 history fixes plus the forecast. `weather/hurricane-desk/scripts/storm_plot.py` turned the nearest Hawaiʻi storm into an ASCII plot (islands as `+`, history endpoints, RAMMB forecast summary, 800 nmi threat line). Those fields were inputs for OBS slides. OBS itself is a later function.

The live system already merges NHC, RAMMB, and JTWC in `global_board.py` and writes `storms-last.json`. `parse_jtwc_moving` is already in that file. The Hawaiʻi-relevant NHC `track.json` poller in `sources.py` and the voice desk stay as they are. This work adds the missing per-storm page, track attach, and text plot onto that board.

---

## 2. Current reality

### 2.1 What exists

| Item | Location / status |
| --- | --- |
| Folder | Weather domain, existing `hurricanes` subfolder. No new top-level folder. |
| Server code | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Weather/hurricanes/scripts/` |
| Database data | `2 - RootRecord-Database/Weather/Hawai'i/hurricanes/global/` (`storms-last.json` today; `storm-tracks.json` and `storm-plot.txt` when this runs) |
| Database logs | `2 - RootRecord-Database/Logs/Weather/hurricanes/` |
| Secrets | None. Public NHC, RAMMB, and JTWC URLs. No `master-key.env` key names. |
| Live board | `global_board.py` four-source merge. Per-storm pages, track persist, and the plot were not in this file at draft time. |
| Old source | `old ollama/old skills/weather/hurricane-tracker/scripts/storm_track.py` and `old ollama/old skills/weather/hurricane-desk/scripts/storm_plot.py` |
| Proposed job | `weather_hurricane_global` / `RR_HURRICANE_GLOBAL` is not in `jobs.py` and stays off. |

### 2.2 Completed so far

- [x] Live four-source merge and `storms-last.json` write
- [x] RAMMB per-storm page, track tables, persist, and text plot
- [x] Archive of the two old source files, then removal from the old repo locally. GitHub push of that commit was rejected.

### 2.3 Known friction

- Extra HTTP: up to 14 storm-page GETs after the existing four source GETs. Each page times out at 14 s and a failure skips that storm.
- GitHub push of the deletion commit is blocked by push protection on an ancestor that is already the remote tip. See the result note. No force-push.
- `hurricane_tracker.py` is shared with the already-ported board and with the OBS kit. It stays in the old tree.

---

## 3. Tasks

1. Add `storm_track.py` beside `global_board.py`. Port region, motion versus Hawaiʻi, table parse, and `attach_track`. `TRACKS_PATH` is `Weather/Hawai'i/hurricanes/global/storm-tracks.json` under `RR_DATABASE_ROOT`. Do not write under `~/.ollama`.
2. Add `storm_plot.py`. Read `storms-last.json` in that same directory. Write `storm-plot.txt` beside it. Keep the text plot. Do not download IR gif bytes and do not draw a map.
3. Extend `refresh()` after `_merge` and before the JSON write. For each kept storm, GET the RAMMB storm page, set `ir_url`, `apply_rammb_page`, `_enrich` again, `attach_track(persist=True)`, then write the plot. Leave the four source fetches and `_merge` in place.
4. Do not edit `jobs.py`. No second job. `RR_HURRICANE_GLOBAL` stays unregistered.
5. One test on a temp database root: fixture HTML with a Forecast Hour row and a Track History row yields non-empty `forecast` and `history`, and `plot_text()` includes the history endpoint line.
6. After that works: archive only `weather/hurricane-tracker/scripts/storm_track.py` and `weather/hurricane-desk/scripts/storm_plot.py` into `Old repos deleted and merged/<old-repo-name>/`, keeping those in-repo paths. Then delete those two files from the old repo locally and on GitHub. Do not force-push. Do not delete the GitHub repository. If the archive copy fails, do not delete. If the Solar-Pacific checkout is missing, pause and name it before any GitHub delete.
7. Update this work order with what landed, the archive path, and the GitHub deletion. Correct only the Library lines that still say the track tables and plot were not ported.

No dependency Folder is missing. `global_board.py` is already in Weather/hurricanes.

---

## 4. Non-goals

- Do not replace `global_board.py`, `sources.py`, `voice_reports.py`, the EcoFlow poller, Hawaiʻi weather, the globe collector, camera grabs, Kokoro, or `geology_collect.py`.
- Do not build OBS scenes, browser sources, speaker playback, sends, or hardware switching (agent 20).
- Do not edit other agents' files. Shared old files stay: `hurricane_tracker.py` and the rest of `hurricane-desk` except `storm_plot.py`.
- Do not edit `jobs.py`.
- Do not import logs, samples, images, radar frames, caches, or dumps into Pacific, Database git, the website, or this work order's runtime.
- Do not open a second top-level domain or a `Weather/RAMMB` twin.

---

## 5. Key file / path reference

| Path | Role |
|------|------|
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Weather/hurricanes/scripts/global_board.py` | Extend `refresh()`; do not replace the merge |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Weather/hurricanes/scripts/storm_track.py` | Add. Parse, attach, persist tracks |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Weather/hurricanes/scripts/storm_plot.py` | Add. Text plot and `storm-plot.txt` |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Weather/tests/hurricanes/test_storm_track_plot.py` | Fixture test, no live network |
| `2 - RootRecord-Database/Weather/Hawai'i/hurricanes/global/storms-last.json` | Existing board output |
| `2 - RootRecord-Database/Weather/Hawai'i/hurricanes/global/storm-tracks.json` | Persisted history and forecast |
| `2 - RootRecord-Database/Weather/Hawai'i/hurricanes/global/storm-plot.txt` | Text plot |
| `2 - RootRecord-Database/Logs/Weather/hurricanes/global-board.log` | One line per run |
| `5 - RootRecord-Library/Documentation/07-testing/2026-09-29-old-repo-ports-breadth-batch5.md` | Correct the "not ported" check-later after the build |
| `5 - RootRecord-Library/Documentation/00-architecture/Old-Repo-Migration-Matrix.md` | Correct the row-40 track-table note after the build |

---

## 6. Open items

**Additional requirements:**

- Agent 20 may read `track_history`, `forecast_track`, `ir_url`, `track_summary`, and `storm-plot.txt`. This work order does not build those scenes.
- Label doubling ("Fay Fay") stays a separate check-later. Do not retune labels here.
- GitHub still has the two source files on `online-safe-20260920` because push protection rejected the deletion commit. Local commit is `e8c37881`.

---

## 7. Notes & constraints

- No force-push.
- Secrets stay out of git. This function has no `master-key.env` keys.
- Prefer small reversible steps.
- Sends, speaker playback, OBS, hardware switching, deletion of live Ecosystem files, and cloud spend stay off until a separate sign-off. Phase 4 deletion is limited to the two old source files, and only after the archive copy is on disk.
- One test that proves the new behavior: fixture HTML with one Forecast Hour row and one Track History row. `parse_rammb_tracks` returns non-empty `forecast` and `history`. `plot_text()` on that storm includes the history endpoint line (`16.5N 149.5E` to `16.8N 148.2E` in the fixture). Database writes for the test use a temp root, not the live `storms-last.json`.

---

*Work order prepared 2026-09-29 HST. Update status when closed.*

---

## Archive / location note

**Draft (not on active index):**

```text
Documentation/06-development/Work-Orders/drafts/RAMMB_per_storm_tracks_and_plot_Work_Order_WO-MIG-04-2026-09-29.md
```

Do not auto-promote.

---

## Result (2026-09-29 HST)

Landed in `Weather/hurricanes/scripts/`: `storm_track.py`, `storm_plot.py`, and an extension of `global_board.refresh()` (per-storm RAMMB page, `ir_url`, track attach, `storm-plot.txt`, log line under `Logs/Weather/hurricanes/`). `jobs.py` was not edited. Fixture test `Weather/tests/hurricanes/test_storm_track_plot.py` PASS. No live board fetch was run.

Archive (verified with `cmp` before delete):

```text
Old repos deleted and merged/Solar-Pacific-RootRecord-Server/weather/hurricane-tracker/scripts/storm_track.py
Old repos deleted and merged/Solar-Pacific-RootRecord-Server/weather/hurricane-desk/scripts/storm_plot.py
```

Bytecode that sat beside those sources was archived under each script's `__pycache__/` and removed locally. `hurricane_tracker.py` and the rest of `hurricane-desk` stayed. Test files that still name the old modules were left: `origin/tests/test_storm_track.py`, `origin/tests/council/test_storm_plot.py`, and `council/council-telegram/desk/src/tests/council/test_storm_plot.py`.

Local old repo `Solar-Pacific-RootRecord-Server` (`/home/rootrecord/old ollama/old skills`, branch `online-safe-20260920`) commit `e8c37881` deletes the two source files. Push to `origin/online-safe-20260920` was rejected by GitHub push protection. The blocked ancestor is `679fd86c`, already the remote tip, because `ecosystem-history/references/archives-pull-20260916/august-emergency-txt/chatgpt improvements.txt` contains an OpenAI API key. This pass did not force-push and did not use the secret-allow URL. The two files are not on `origin/main`.

Library lines corrected: breadth-batch-5 check-later, and Old-Repo-Migration-Matrix row 40 plus the next-candidates sentence.
