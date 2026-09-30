# WORK ORDER — A-EYES Capture Rate & Timelapse Optimization

| Field            | Value                          |
|------------------|--------------------------------|
| **Work Order ID**| WO-AEYES-2026-09-27            |
| **Date**         | 2026-09-27                     |
| **Status**       | OPEN — Ready for additions     |
| **Owner**        | RootRecord                     |
| **Updated**      | 2026-09-30 02:35 HST — grabs still pass (ch1–ch4; ch4 is a small night frame). Interval still 1s. Timelapse still waits on 05:00–19:00 HST. Alexander's call is in `Documentation/01-operations/2026-09-30-whats-left-for-alexander.md`. |

**Scope:** Reduce A-EYES archive load while producing a clean, human-viewable 1-minute daily timelapse. This document captures the current system, the math, the recommended changes, and leaves room for additional requirements.

**Migration note (2026-09-28, superseded):** The import is done. Do not look for a live grab under `~/.ollama/skills/a-eyes/`.

**Current paths (read-only desk check 2026-09-29 ~03:52 HST; supersedes the 2026-09-28 note above):** Pacific `Security/Cameras/` is canonical and there is no A-Eyes compatibility layer.
- `jobs.py` runs all camera jobs from there (`cwd` = `Security/Cameras`): `ensure_cam_server.sh`, `timelapse_catchup.sh`, `grab_all.sh` (job `security_camera_frame_grab`), `timelapse_hourly.sh`, `timelapse_daily.sh`. The running `cam_server.py` has cwd `…/Security/Cameras`.
- Frames go to `2 - RootRecord-Database/Media/Images/`; timelapses go to `2 - RootRecord-Database/Media/Timelapses/`.
- Pacific `A-Eyes/` still exists but holds only a stale, git-ignored `scripts/__pycache__/grab_frame.cpython-314.pyc` (dated 09-28 21:06). It has no source, no tracked files and no job references: **legacy, KEPT**.
- G2 `~/.ollama/skills/a-eyes/` is **KEPT** (retire only with Alexander sign-off).
- State: cam server + frame grab **PASS**. At 22:21 HST, `cam_server.py` cwd is Pacific `Security/Cameras` and ch1–ch4 wrote stills. ch4 is a dark night frame. Timelapse compile **VERIFY PENDING**: `video_chunks` and `final_output` are empty because the current frames are outside 05:00–19:00 HST. `interval_sec` is still 1.

---

## 1. Current System Snapshot

### 1.1 Capture Path

- Scheduler: `Automations/scripts/jobs.py` → `EVERY_SECONDS` → `security_camera_frame_grab` (was `a_eyes_frame_grab`)
  - **Historical:** `automations/scripts/jobs.py` (pre-domain layout)
- `interval_sec = 1` (1 frame per second per camera)
- Command: `bash "{PACIFIC}/Security/Cameras/grab_all.sh"` (cwd `Security/Cameras`)
- `grab_all.sh` loops channels 1–4 and calls `grab_frame.py` for each
- `grab_frame.py`: RTSP → single JPEG → `/home/rootrecord/RootRecord-Ecosystem/2 - RootRecord-Database/Media/Images/`
- Crop applied at grab time (right edge % + 20 px). Left side (timestamp OSD) preserved.
- Cross-process flock (`/tmp/security-camera-frames.lock`). Grabs are non-blocking (skip if busy).

### 1.2 Timelapse Path

- Engine: `Security/Cameras/timelapse_engine.py` (output under `2 - RootRecord-Database/Media/Timelapses/`)
- Window: **05:00–19:00 HST** (14 hours)
- `TARGET_TOTAL_SECONDS = 180` (3-minute master)
- `MASTER_FPS = 68`
- Only **channel 1** is used for the master stitch
- Hourly (top of hour): compile previous hour → `video_chunks/hour_HH.mp4`
- Daily at **19:01**: concat 14 hourly MP4s → `final_output/master_stitched_timelapse.mp4`
- Frames archived (or deleted) after successful hourly compile

### 1.3 Live UI

- `cam_server.py` binds `127.0.0.1:8791`
- Public path: `https://rootserver.rootrecord.cloud/aeyes` (password-protected)
- On-demand stills, ~2 s refresh — independent of the archive grab rate

---

## 2. Current Load Math

| Metric                        | Per Camera     | All 4 Cameras   |
|-------------------------------|----------------|-----------------|
| Frames / hour                 | 3,600          | 14,400          |
| Frames / day (14 h)           | 50,400         | **201,600**     |
| Source frames in 180 s master | ~50,400 (stretched) | N/A (ch1 only) |

**Problem:** 50,400 real frames are forced into a 180-second / 68 FPS container. The output is mostly frame duplication/stretching, not true 68 captured FPS. Archive grows unnecessarily large for intermediate stills that are never viewed at full temporal resolution.

---

## 3. Recommended Changes

### 3.1 Capture Interval (primary lever)

**File:** `Automations/scripts/jobs.py`  
**Job:** `security_camera_frame_grab` (EVERY_SECONDS section)

```python
# Change:
"interval_sec": 1   →   "interval_sec": 5
```

### 3.2 Timelapse Output Length & FPS

**File:** `Security/Cameras/timelapse_engine.py` (or env overrides; the `A_EYES_TIMELAPSE_*` env names are unchanged)

```bash
A_EYES_TIMELAPSE_TOTAL_SEC = 60     # was 180
A_EYES_TIMELAPSE_FPS       = 20     # was 68  (15–24 acceptable)
```

### 3.3 Resulting Numbers

| Metric                     | After Change      | vs Current                  |
|----------------------------|-------------------|-----------------------------|
| JPEGs / day (4 cams)       | ~40,320           | ≈ 1/5 of current            |
| Daily master length        | 60 seconds        | 1/3 of current              |
| Master FPS                 | 20                | Matches real capture density|
| Frame use                  | Near 1:1          | No heavy duplication        |

---

## 4. Implementation Tasks

1. Change `interval_sec` from `1` → `5` in `Automations/scripts/jobs.py` (`security_camera_frame_grab`; still `1` on 2026-09-29, PROPOSED).
2. Set `TARGET_TOTAL_SECONDS = 60` and `MASTER_FPS = 20` (env vars preferred).
3. Push → auto-reload (`schedule-stack-reload`).
4. Verify after next daily window.
5. ~~Optional: import A-EYES into Pacific `Security/`~~ **LANDED**: code is in Pacific `Security/Cameras/` and the jobs are rewired. Cam server + grab PASS; timelapse VERIFY PENDING.

---

## 5. Key File Reference

| Path                                      | Role                                              |
|-------------------------------------------|---------------------------------------------------|
| `Automations/scripts/jobs.py`             | Canonical scheduler — capture interval            |
| `Security/Cameras/grab_all.sh`            | Loops ch1–4                                       |
| `Security/Cameras/grab_frame.py`          | Single RTSP grab + crop → `Media/Images/`         |
| `Security/Cameras/timelapse_engine.py`    | Hourly compile + daily stitch → `Media/Timelapses/` |
| `Security/Cameras/timelapse_{hourly,daily,catchup}.sh`, `ensure_cam_server.sh` | Job wrappers |
| `Security/Cameras/cam_server.py`          | Live stills server (`127.0.0.1:8791`)             |
| `Security/Cameras/store/CONNECTION.json`  | RTSP + crop config (secrets stay local; `store/` git-ignored) |
| Pacific `A-Eyes/`                         | Legacy leftover (stale `__pycache__` only) — **KEPT**, not used |
| G2 `~/.ollama/skills/a-eyes/`             | Legacy — **KEPT** (sign-off). G2 still tracks `a-eyes/store/CONNECTION.json`: security item BLOCKED pending Alexander |
| **Historical:** `automations/scripts/jobs.py` | Pre-domain-layout scheduler path                |

---

## 6. Open Items / Room for Additions

**Additional requirements:**

- 
- 
- 

---

## 7. Notes & Constraints

- Changing only `TARGET_TOTAL_SECONDS` does **not** reduce capture rate or archive load.
- The capture-rate lever is exclusively `interval_sec` in `jobs.py`.
- Deploy path is GitHub push → `github_sync_all` → `schedule-stack-reload`.
- Never invent frames. No stream = error, not a placeholder image.
- Secrets (RTSP password, public password) never go in git.

---

*Document prepared from live repo inspection of `a-eyes/` and `automations/` on 2026-09-27. Path annotations added 2026-09-28.*
