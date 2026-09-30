# WORK ORDER — Sunrise restore

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-MIG-17-2026-09-29 |
| **Date** | 2026-09-29 (HST) |
| **Status** | BUILT — playback request landed, speakers off. Not promoted. |
| **Owner** | RootRecord |
| **Related** | Agent 17, Wave C. Depends on 15, Report playback. No later function depends on this one. Old source: `old ollama/old skills/sunrise-restore/scripts/sunrise_restore.py`. Live sun times: `Energy/scripts/sun_times.py`. Live Kokoro: `Media/Voice`. |

**Scope:** Add a sunrise-restore playback request under Media. When a pending flag is set, ask the shared Report playback player for two reconnect clips and then clear the flag. In scope is that script, its Database pending file, and its log path. Out of scope is the player itself, speaker playback, the old burst collectors, night-sleep flag writing, and any other agent's function. This draft is not accepted for execution. Do not promote it onto the active index.

---

## 1. Intent

The old `sunrise-restore/scripts/sunrise_restore.py` ran only when `pending` was true. It announced `battery_reconnect` and `phrase_all_systems_running`, then called solar, NOAA, Kīlauea, hybrid, overnight, and morning collectors, and cleared the flag. Origin started that about four seconds after process start. The EcoFlow poller set `pending` at the end of the sunrise sequence once the internet was up.

The burst-collect stays out. Live pieces that stay as they are: `Energy/scripts/sun_times.py` and gated job `energy_sun_times`, `Media/Voice` Kokoro (`voice_generate.py`, `speakers.py`, `clip_catalog.py`), EcoFlow BLE, the poller, Hawaiʻi weather, and `geology_collect.py`. The new behavior is a playback request only. It does not copy the old script over the live voice desk.

---

## 2. Current reality

### 2.1 What exists

Folder name: **SunriseRestore**, under the Media domain. One capitalized folder. No lowercase twin and no symlink.

| Item | Location / status |
| --- | --- |
| Folder | `SunriseRestore` — not installed |
| Server code | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Media/SunriseRestore/scripts` — to be created at build |
| Database data | `2 - RootRecord-Database/Media/SunriseRestore/` — `pending.json`; not created yet |
| Database logs | `2 - RootRecord-Database/Logs/Media/SunriseRestore/` — not created yet. `Logs/Media/` does not exist yet |
| master-key.env | No keys. This function reads no secrets. |
| Package | `SunriseRestore` |
| Live neighbors | `Media/Voice` and `Media/Video` exist. Report playback has no Folder yet |
| Spoken line on disk | Ava `boot_all_systems_running` in `clip_catalog.py`: "All systems running." |
| Missing clip text | `battery_reconnect` has no spoken line in the old source. Do not invent one |
| Sunrise clock | `2 - RootRecord-Database/Energy/sun/sun-times-last.json`, written by `sun_times.py`. Read only. Do not refresh Open-Meteo here |
| Old flag | EcoFlow poller store `sunrise-restore.json`. Not imported |
| Flag writer | Night sleep (agent 01), inside the old sunrise sequence. Not this function |

### 2.2 Completed so far

- [x] Old `maybe_run` read from `sunrise-restore/scripts/sunrise_restore.py` only
- [x] Live Kokoro and sun-times desks confirmed; no newer sunrise-restore playback exists to enhance
- [x] Alexander said to build
- [x] Report playback Folder present at build (`Media/Playback/scripts/play.py`)
- [x] `SunriseRestore` script, Database pending path, and log path
- [x] Dry-run test (no speaker, no model load) — 2026-09-30 00:04 HST, temp database root
- [x] Phase 4 archive copy, and local deletion commit `e4045fed`
- [ ] GitHub push of that deletion (rejected: older commit on the branch trips push protection)
- [x] Library pages corrected for the playback request

### 2.3 Known friction

- Report playback (agent 15) is the shared Kokoro player. This function pauses if that Folder is missing and does not build the player.
- `battery_reconnect` has no text. The request still names that id. A missing clip is skipped, the same way the old `try/except` skipped a failed announce.
- Night sleep is the intended writer of `pending`. This function does not edit the live EcoFlow poller. With no flag, the script skips.
- `jobs.py` is shared. If it is already being edited when the build starts, pause. The only proposed edit is one gated block, default off.
- Speaker playback needs Alexander's sign-off. The dry-run does not play audio.

---

## 3. Tasks

Build only after Alexander accepts this draft and says to build. Until then, do not edit runtime files, restart services, send messages, actuate hardware, or spend cloud money.

1. Pause if Report playback has no Folder yet. Name that function. Do not build the player. Do not build Morning boot replay, Report readiness audio, Hurricane radio, OBS, or Cloud TTS.
2. Add `Media/SunriseRestore/__init__.py`, `Media/SunriseRestore/README.md`, and `Media/SunriseRestore/scripts/sunrise_restore.py`. If `2 - RootRecord-Database/Media/SunriseRestore/pending.json` is missing or `pending` is not true, exit skipped. If pending, ask the Report playback player for `battery_reconnect` then `boot_all_systems_running`, skip a missing clip, clear `pending`, and append a line under `Logs/Media/SunriseRestore/`. Read sunrise time from `2 - RootRecord-Database/Energy/sun/sun-times-last.json` only. Do not refresh Open-Meteo. Do not call `aplay`. Do not load Kokoro.
3. Propose one gated `jobs.py` block, id `media_sunrise_restore`, enabled only when `RR_SUNRISE_RESTORE=1`. Do not edit `jobs.py` in this draft. On build, add only that block, and only if `jobs.py` is not already being edited. Default stays off.
4. Leave Night sleep as the writer of `pending`. Do not edit the live poller, `sun_times.py`, or `Media/Voice` to set the flag or to play the clips.
5. Prove it with `python3 sunrise_restore.py --dry-run` and a temporary pending file. First run prints `ran: true`, clip ids `battery_reconnect` and `boot_all_systems_running`, and `played: false`, then clears pending. Second run prints `skipped: true`. No model load and no speaker. The pending file and the log line stay out of git.
6. After the migration works, archive only the files that belong to this function from `/home/rootrecord/old ollama/old skills` (GitHub `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server`, branch `online-safe-20260920`) into `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/`, keeping the path inside that repo:
   - `sunrise-restore/DAILY.md`
   - `sunrise-restore/INDEX.md`
   - `sunrise-restore/SKILL.md`
   - `sunrise-restore/references/migrate.md`
   - `sunrise-restore/scripts/sunrise_restore.py`
   Leave and name: `origin/ns/apps/core/services/sunrise_restore.py` (shim still imported by shared `origin/scripts/main.py`), `energy/ecoflow-automations/desk/live/sunrise_restore.py`, and the EcoFlow poller. Do not restore anything under `~/.ollama/skills/energy`. Do not import `DAILY.md` inserts, the old flag JSON, logs, samples, or generated audio into Pacific, Database, the website, or git. If the archive copy fails, do not delete. After the archive copy is on disk, delete those five files from the old repo on this machine and on GitHub. Commit that deletion and push it. Do not force-push. Do not delete the GitHub repository.
7. Then update this work order with what landed, the archive path, the GitHub deletion, and the new status. Correct only the Library pages this function made stale: `Documentation/00-architecture/Old-Repo-Migration-Matrix.md` (row 25) and `Documentation/00-architecture/Voice-Reports-G3.md`. Do not rewrite unrelated work orders.

---

## 4. Non-goals

- Do not overwrite Kokoro (`voice_generate.py`, `speakers.py`, `clip_catalog.py`), `geology_collect.py`, EcoFlow BLE, the poller, Hawaiʻi weather, the globe collector, or camera grabs.
- Do not port the solar, NOAA, Kīlauea, hybrid, overnight, or morning burst collectors.
- Do not change power profiles, wait on the internet, or write the pending flag from the poller.
- Do not invent spoken text for `battery_reconnect`.
- Do not edit `origin/scripts/main.py` or build another agent's function.
- Do not play speakers, send messages, switch hardware, delete live Ecosystem files, or spend cloud money without a separate sign-off.
- Do not enable `RR_SUNRISE_RESTORE` on the live poller in this draft.
- Do not import logs, samples, last-state files, generated reports, images, radar frames, zip archives, dumps, caches, virtualenvs, `node_modules`, or `__pycache__` into the live Folders.

---

## 5. Key file / path reference

| Path | Role |
|------|------|
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Media/SunriseRestore/scripts` | Server code. Package `SunriseRestore` |
| `2 - RootRecord-Database/Media/SunriseRestore/` | Database data. `pending.json` created at runtime, not committed |
| `2 - RootRecord-Database/Logs/Media/SunriseRestore/` | Database logs only |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Media/SunriseRestore/__init__.py` | Package marker, added at build |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Media/SunriseRestore/scripts/sunrise_restore.py` | Playback request. Dry-run does not play |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Media/SunriseRestore/README.md` | Desk note, added at build |
| `2 - RootRecord-Database/Energy/sun/sun-times-last.json` | Read-only sunrise clock. Do not refresh it here |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Media/Voice/scripts/clip_catalog.py` | Existing Ava line `boot_all_systems_running`. Do not edit |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Automations/scripts/jobs.py` | One gated block at build, only if the file is free. Not edited in this draft |
| `old ollama/old skills/sunrise-restore/` | Old function files to archive in phase 4, then remove from the old repo and GitHub |
| `old ollama/old skills/origin/ns/apps/core/services/sunrise_restore.py` | Shared shim. Leave |
| `old ollama/old skills/origin/scripts/main.py` | Shared caller. Leave |
| `old ollama/old skills/energy/ecoflow-automations/desk/live/sunrise_restore.py` | Under energy. Leave |
| `5 - RootRecord-Library/Documentation/00-architecture/Old-Repo-Migration-Matrix.md` | Correct row 25 after phase 4 only |
| `5 - RootRecord-Library/Documentation/00-architecture/Voice-Reports-G3.md` | Correct the sunrise-restore playback note after phase 4 only |

---

## 6. Open items

**Additional requirements:**

- Alexander accepts this draft and says to build before any runtime edit.
- Report playback must have a Folder before this build continues. If it does not, pause and name Report playback.
- Speaker playback, sends, hardware switching, and cloud spend need a separate sign-off. This draft does none of those.
- `RR_SUNRISE_RESTORE=1` on the live poller needs a separate sign-off. The default stays off.
- GitHub push of `e4045fed` was rejected. The block is an OpenAI API key in older commit `679fd86c` (`ecosystem-history/references/archives-pull-20260916/august-emergency-txt/chatgpt improvements.txt`). This function did not add that secret and did not rewrite history.

---

## 7. Notes & constraints

- No force-push.
- Secrets stay out of git. No master-key.env keys for this function.
- Prefer small reversible steps.
- Sends, speaker playback, OBS, hardware switching, deletion of live Ecosystem files, and cloud spend need Alexander's sign-off. This draft does none of those.
- Sign-off gate: playing the clips on a speaker, and turning `RR_SUNRISE_RESTORE` on. The dry-run requests the clip ids and sets `played: false`.
- Test, after a build accept only: `python3 sunrise_restore.py --dry-run` with a temporary pending file prints `ran: true`, the two clip ids, and `played: false`, then clears pending. A second run prints `skipped: true`. No model load and no speaker.
- New periodic jobs stay gated off. The `jobs.py` block is proposed only, default off.
- Phase 4 result: see section 8. Archive copy is on disk. Local deletion commit is `e4045fed`. GitHub still has the five files because push protection rejected the branch.

---

## 8. Result note

Landed 2026-09-30: `Media/SunriseRestore` (`__init__.py`, `README.md`, `scripts/sunrise_restore.py`). `--dry-run` with a temporary pending file printed `ran: true`, clips `battery_reconnect` and `boot_all_systems_running`, and `played: false`, then cleared pending. A second run printed `skipped: true`. A non-dry run called `Media/Playback/scripts/play.py --clip Ava/<slug> --dry-run` and got `audio_missing` for both clips. No `aplay`, no Kokoro load.

`jobs.py` was already being edited, so the gated `media_sunrise_restore` / `RR_SUNRISE_RESTORE` block was not inserted. It is staged in `Media/SunriseRestore/proposed-job-block.txt`.

Archive path: `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/sunrise-restore/` (the five old files, copy matched the source). Left in place: `origin/ns/apps/core/services/sunrise_restore.py`, `origin/scripts/main.py`, `energy/ecoflow-automations/desk/live/sunrise_restore.py`, and the EcoFlow poller.

Local deletion: commit `e4045fed` on `online-safe-20260920` in `/home/rootrecord/old ollama/old skills`. GitHub push was rejected by push protection on older commit `679fd86c` (OpenAI API key in `ecosystem-history/references/archives-pull-20260916/august-emergency-txt/chatgpt improvements.txt`). The repository was not deleted. History was not rewritten.

Library: matrix row 25 and the boot_brief row in `Voice-Reports-G3.md` now say the playback request landed and the speaker stays off.

---

*Work order prepared 2026-09-29 HST. Build recorded 2026-09-30 HST. Not promoted.*

---

## Archive / location note

**Active / accepted WOs** — filename when saved:

```text
Sunrise_restore_Work_Order_WO-MIG-17-2026-09-29.md
```

Location after acceptance (do not move this file there yet):

```text
Documentation/06-development/Work-Orders/
```

**Drafts (not on active index)** — this file:

```text
Documentation/06-development/Work-Orders/drafts/Sunrise_restore_Work_Order_WO-MIG-17-2026-09-29.md
```

See `drafts/README.md` and WO-WOGEN-001. Do not auto-promote.

**Closed WOs:** set Status → COMPLETE/CLOSED → `git mv` into:

```text
Documentation/06-development/Work-Orders/Complete/
```

Human session logs archive under `Documentation/01-operations/archive/YYYY-Www/` (WO-ARCH) — separate from closed work orders.
