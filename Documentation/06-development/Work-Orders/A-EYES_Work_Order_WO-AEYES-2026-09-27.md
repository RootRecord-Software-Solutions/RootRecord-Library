# WORK ORDER — A-EYES Capture Rate & Timelapse Optimization

| Field            | Value                          |
|------------------|--------------------------------|
| **Work Order ID**| WO-AEYES-2026-09-27            |
| **Date**         | 2026-09-27                     |
| **Status**       | OPEN — Ready for additions     |
| **Owner**        | RootRecord                     |
| **Updated**      | 2026-09-28 (HST) — path notes only |

**Scope:** Reduce A-EYES archive load while producing a clean, human-viewable 1-minute daily timelapse. This document captures the current system, the math, the recommended changes, and leaves room for additional requirements.

**Migration note (2026-09-28):** Job catalog path is now `Automations/scripts/jobs.py` on the Pacific server. A-EYES skill code is **not yet imported** into the Pacific domain tree; runtime commands may still resolve under legacy `~/.ollama/skills/a-eyes/` until the Security/A-EYES domain is brought in.

---

## 1. Current System Snapshot

### 1.1 Capture Path

- Scheduler: `Automations/scripts/jobs.py` → `EVERY_SECONDS` → `a_eyes_frame_grab`
  - **Historical:** `automations/scripts/jobs.py` (pre-domain layout)
- `interval_sec = 1` (1 frame per second per camera)
- Command: `bash …/a-eyes/scripts/grab_all.sh` (legacy skills path until import)
- `grab_all.sh` loops channels 1–4 and calls `grab_frame.py` for each
- `grab_frame.py`: RTSP → single JPEG → `/home/rootrecord/Database/A-EYES/frames/`
- Crop applied at grab time (right edge % + 20 px). Left side (timestamp OSD) preserved.
- Cross-process flock (`/tmp/a-eyes-frames.lock`). Grabs are non-blocking (skip if busy).

### 1.2 Timelapse Path

- Engine: `a-eyes/scripts/timelapse_engine.py` (legacy location until import)
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
**Job:** `a_eyes_frame_grab` (EVERY_SECONDS section)

```python
# Change:
"interval_sec": 1   →   "interval_sec": 5
```

### 3.2 Timelapse Output Length & FPS

**File:** `a-eyes/scripts/timelapse_engine.py` (or env overrides; path may still be legacy until domain import)

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

1. Change `interval_sec` from `1` → `5` in `Automations/scripts/jobs.py` (`a_eyes_frame_grab`).
2. Set `TARGET_TOTAL_SECONDS = 60` and `MASTER_FPS = 20` (env vars preferred).
3. Push → auto-reload (`schedule-stack-reload`).
4. Verify after next daily window.
5. Optional: import A-EYES into Pacific `Security/` (or dedicated domain) and rewire job commands.

---

## 5. Key File Reference

| Path                                      | Role                                              |
|-------------------------------------------|---------------------------------------------------|
| `Automations/scripts/jobs.py`             | Canonical scheduler — capture interval            |
| `a-eyes/scripts/grab_all.sh`              | Loops ch1–4 (legacy path until import)            |
| `a-eyes/scripts/grab_frame.py`            | Single RTSP grab + crop                           |
| `a-eyes/scripts/timelapse_engine.py`      | Hourly compile + daily stitch                     |
| `a-eyes/scripts/cam_server.py`            | Live stills server (`127.0.0.1:8791`)             |
| `a-eyes/store/CONNECTION.json`            | RTSP + crop config (secrets stay local)           |
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
