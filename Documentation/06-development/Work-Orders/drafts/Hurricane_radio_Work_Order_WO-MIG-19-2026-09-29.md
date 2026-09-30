# WORK ORDER — Hurricane radio

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-MIG-19-2026-09-29 |
| **Date** | 2026-09-30 (HST) |
| **Status** | OPEN — draft, not accepted for execution |
| **Owner** | RootRecord |
| **Related** | Agent 19, Wave C. Depends on 15, Report playback. No later function depends on this one. Old source: `old ollama/old skills/weather/hurricane-radio/scripts/job.py`. Live desk: `Media/Voice/scripts/voice_reports.py` `hurricane_desk`. Live player: `Media/Playback/scripts/play.py`. |

**Scope:** Add a radio output beside the existing hurricane desk. The output hands the desk's Kokoro WAV to the shared Report playback player as a dry-run. In scope is that script, its Database last-run file, its log path, and one gated job proposal that stays off. Out of scope is the player, the desk text, AWS radio, speaker playback, OBS, and any other agent's function. This draft is not accepted for execution. Do not promote it onto the active index.

---

## 1. Intent

The old `weather/hurricane-radio/scripts/job.py` called `hurricane_desk.play_on_radio()` at 06:35, 13:12, and 17:02. That method skipped when the AWS radio service was off air, when `hurricane_on_radio` was false, or when the desk WAV was missing, then pushed the WAV with `play_report_mp3`. The folder is marked offloaded to AWS radio. The old scheduler skipped the job during night sleep.

Storm data and the hurricane desk text already exist. Radio playback does not. The live desk stays `voice_reports.py` `hurricane_desk` (Carly), job `voice_hurricane_desk`, gated on `RR_VOICE_HURRICANE`. The shared player stays `Media/Playback/scripts/play.py`. Kokoro, the weather poller, EcoFlow BLE, Hawaiʻi weather, and `geology_collect.py` stay as they are. The new behavior is a dry-run handoff of `hurricane_desk` to that player. It does not restore AWS on-air, Icecast, or a website listen page, and it does not copy the old runner over the live desk.

---

## 2. Current reality

### 2.1 What exists

Folder name: **HurricaneRadio**, under the Media domain. One capitalized folder. No lowercase twin and no symlink.

| Item | Location / status |
| --- | --- |
| Folder | `HurricaneRadio` — not installed |
| Server code | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Media/HurricaneRadio/scripts` — to be created at build |
| Database data | `2 - RootRecord-Database/Media/HurricaneRadio/` — `last-radio.json`; not created yet; runtime only, not committed |
| Database logs | `2 - RootRecord-Database/Logs/Media/HurricaneRadio/` — `radio.log`; not created yet |
| master-key.env | No keys. This function reads no secrets |
| Package | `HurricaneRadio` |
| Report playback | Present: `Media/Playback/scripts/play.py`. Pause at build only if that Folder is gone. Do not build the player |
| Live desk | `Media/Voice/scripts/voice_reports.py` `hurricane_desk`. Job `voice_hurricane_desk` at 05:50, 09:50, 12:50, 16:55, 20:50, gated `RR_VOICE_HURRICANE`. Do not edit |
| Desk WAV | `2 - RootRecord-Database/Media/Audio/Voice/hurricane_desk_current.wav` — not on disk as of this draft |
| Storm data | `Weather/hurricanes/` and Database `Weather/Hawai'i/hurricanes/`. Read by the desk. Do not edit |
| Night sleep | `System/NightSleep`. Read `sleeping` only. Do not edit |
| Old radio job | `old ollama/old skills/weather/hurricane-radio/` on GitHub `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server`, branch `online-safe-20260920` |

### 2.2 Completed so far

- [x] Old `job.py` and `play_on_radio` read. AWS push is not ported
- [x] Live desk and `Media/Playback` confirmed. No newer hurricane-radio output exists to enhance
- [ ] Alexander accepts this draft and says to build
- [ ] `HurricaneRadio` script, last-run path, and log path
- [ ] Dry-run test (no speaker, no `aplay`)
- [ ] Phase 4 archive, then deletion from the old repo locally and on GitHub
- [ ] Result note and Library corrections

### 2.3 Known friction

- Report playback (agent 15) is the shared Kokoro player. This function pauses if that Folder is missing and does not build the player.
- `hurricane_desk_current.wav` is not on disk. A run with no WAV records `no_wav` or `audio_missing` and exits 0. This function does not render speech.
- `jobs.py` is shared. If it is already being edited when the build starts, do not edit it. Stage the gated block in `proposed-job-block.txt`. If it is free, insert that same block, still default off.
- Speaker playback and AWS radio need Alexander's sign-off. This folder never passes `--play` and never calls `aplay`.
- `play_on_radio` lives in old `hurricane-desk`. That file is shared with the already-migrated desk. Leave it.

---

## 3. Tasks

Build only after Alexander accepts this draft and says to build. Until then, do not edit runtime files, restart services, send messages, actuate hardware, or spend cloud money.

1. Pause if Report playback has no Folder yet. Name that function. Do not build the player. Do not build Morning boot replay, Sunrise restore, Report readiness audio, OBS, or Cloud TTS.
2. Add `Media/HurricaneRadio/__init__.py`, `Media/HurricaneRadio/README.md`, and `Media/HurricaneRadio/scripts/radio.py`. `radio.py run` reads NightSleep state and skips with `night_sleep` when `sleeping` is true. If `Media/Playback/scripts/play.py` is missing, log `player_missing` and stop. Otherwise hand `hurricane_desk` to `play.py --report hurricane_desk --dry-run`. A missing WAV is `no_wav` or `audio_missing`, exit 0. A player `busy` result is the overlap skip. Write `2 - RootRecord-Database/Media/HurricaneRadio/last-radio.json` and append `2 - RootRecord-Database/Logs/Media/HurricaneRadio/radio.log`. Do not call `aplay`. Do not load Kokoro. Do not pass `--play`.
3. Propose one gated `jobs.py` block, id `media_hurricane_radio`, times `06:35`, `13:12`, and `17:02`, enabled only when `RR_HURRICANE_RADIO=1`. Do not edit `jobs.py` in this draft. On build, if `jobs.py` is already being edited, write that block to `Media/HurricaneRadio/proposed-job-block.txt` and leave `jobs.py` alone. If `jobs.py` is free, insert that same block, still default off.
4. Leave `voice_reports.py`, `play.py`, `Weather/hurricanes/`, and `System/NightSleep` unchanged.
5. Prove it with `python3 scripts/radio.py run`. It prints one JSON line with `played: false` and does not spawn `aplay`. With no WAV, detail is `no_wav` or `audio_missing`. The last-run file and the log line stay out of git.
6. After the migration works, archive the tracked old-repo files into `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/weather/hurricane-radio/`, keeping the path inside that repo:
   - `weather/hurricane-radio/DAILY.md`
   - `weather/hurricane-radio/INDEX.md`
   - `weather/hurricane-radio/OFFLOADED`
   - `weather/hurricane-radio/SKILL.md`
   - `weather/hurricane-radio/references/migrate.md`
   - `weather/hurricane-radio/scripts/job.py`
   Leave `weather/hurricane-desk/` (`play_on_radio` stays with the desk). Do not restore anything under `~/.ollama/skills/energy`, automations, or `coms/ssh/local-data-globe`. Do not import logs, samples, last-state files, generated reports, images, radar frames, zip archives, dumps, caches, virtualenvs, `node_modules`, or `__pycache__` into Pacific, Database, the website, or git. Generated data that lived beside the old source goes into the archive only. If the archive copy fails, do not delete. After the archive copy is on disk, delete those six files from the old repo on this machine and on GitHub (`rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server`). Commit that deletion and push it. Do not force-push. Do not delete the GitHub repository.
7. Then update this work order with what landed, the archive path, the GitHub deletion, and the new status. Correct only the Library pages this function made stale: the radio half of row 41 in `Documentation/00-architecture/Old-Repo-Migration-Matrix.md`, and the hurricane-radio row in `Documentation/00-architecture/G1-Scheduler-To-G3-Jobs-Map-2026-09-29.md`. Leave the OBS half of row 41 untouched. Do not rewrite unrelated work orders.

---

## 4. Non-goals

- Do not overwrite Kokoro (`voice_generate.py`, `speakers.py`, `clip_catalog.py`, `voice_reports.py`), `play.py`, `geology_collect.py`, EcoFlow BLE, the poller, Hawaiʻi weather, the globe collector, or camera grabs.
- Do not restore AWS on-air, Icecast, or a website listen page.
- Do not render a new hurricane-desk WAV. The desk already owns that.
- Do not edit Morning boot replay, Sunrise restore, Report readiness audio, OBS, or Cloud TTS.
- Do not play speakers, send messages, switch hardware, delete live Ecosystem files, or spend cloud money without a separate sign-off.
- Do not enable `RR_HURRICANE_RADIO` or `RR_PLAYBACK` on the live poller in this draft.
- Do not import logs, samples, last-state files, generated reports, images, radar frames, zip archives, dumps, caches, virtualenvs, `node_modules`, or `__pycache__` into the live Folders.

---

## 5. Key file / path reference

| Path | Role |
|------|------|
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Media/HurricaneRadio/scripts` | Server code. Package `HurricaneRadio` |
| `2 - RootRecord-Database/Media/HurricaneRadio/` | Database data. `last-radio.json` created at runtime, not committed |
| `2 - RootRecord-Database/Logs/Media/HurricaneRadio/` | Database logs only. `radio.log` |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Media/HurricaneRadio/__init__.py` | Package marker, added at build |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Media/HurricaneRadio/scripts/radio.py` | Dry-run handoff. Never passes `--play`. Never calls `aplay` |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Media/HurricaneRadio/README.md` | Desk note, added at build |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Media/HurricaneRadio/proposed-job-block.txt` | Staged only if `jobs.py` is already being edited |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Media/Playback/scripts/play.py` | Shared player. Do not edit |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Media/Voice/scripts/voice_reports.py` | Existing `hurricane_desk`. Do not edit |
| `2 - RootRecord-Database/Media/Audio/Voice/hurricane_desk_current.wav` | Desk WAV the player reads. Not on disk yet. Do not synthesize it here |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/System/NightSleep/scripts/night_sleep.py` | Read `sleeping` only. Do not edit |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Automations/scripts/jobs.py` | One gated block at build, only if the file is free. Not edited in this draft |
| `old ollama/old skills/weather/hurricane-radio/` | Old function files to archive in phase 4, then remove from the old repo and GitHub |
| `old ollama/old skills/weather/hurricane-desk/` | Shared `play_on_radio`. Leave |
| `5 - RootRecord-Library/Documentation/00-architecture/Old-Repo-Migration-Matrix.md` | Correct the radio half of row 41 after phase 4 only |
| `5 - RootRecord-Library/Documentation/00-architecture/G1-Scheduler-To-G3-Jobs-Map-2026-09-29.md` | Correct the hurricane-radio row after phase 4 only |

---

## 6. Open items

**Additional requirements:**

- Alexander accepts this draft and says to build before any runtime edit.
- Report playback must have a Folder before this build continues. It is present now (`Media/Playback`). If it is gone at build time, pause and name Report playback.
- Speaker playback, AWS radio, sends, hardware switching, and cloud spend need a separate sign-off. This draft does none of those.
- `RR_HURRICANE_RADIO=1` on the live poller needs a separate sign-off. The default stays off.
- Phase 4 result note is written only after the archive copy is on disk and the old-repo deletion is committed.

---

## 7. Notes & constraints

- No force-push.
- Secrets stay out of git. No master-key.env keys for this function.
- Prefer small reversible steps.
- Sends, speaker playback, OBS, hardware switching, deletion of live Ecosystem files, and cloud spend need Alexander's sign-off. This draft does none of those.
- Sign-off gate: live `aplay` (`RR_PLAYBACK=1` and `--play` on the player), AWS radio, and turning `RR_HURRICANE_RADIO` on. This folder's dry-run sets `played: false`.
- Test, after a build accept only: `python3 scripts/radio.py run` prints one JSON line with `played: false` and does not spawn `aplay`. With no WAV, detail is `no_wav` or `audio_missing`.
- New periodic jobs stay gated off. The `jobs.py` block is proposed only, default off.
- After phase 4, add a short result note here: what landed, the archive path, and the GitHub deletion. Then correct only the two Library pages named in task 7.

---

*Work order prepared 2026-09-30 HST. Update status when closed.*

---

## Archive / location note

**Active / accepted WOs** — filename when saved:

```text
Hurricane_radio_Work_Order_WO-MIG-19-2026-09-29.md
```

Location after acceptance (do not move this file there yet):

```text
Documentation/06-development/Work-Orders/
```

**Drafts (not on active index)** — this file:

```text
Documentation/06-development/Work-Orders/drafts/Hurricane_radio_Work_Order_WO-MIG-19-2026-09-29.md
```

See `drafts/README.md` and WO-WOGEN-001. Do not auto-promote.

**Closed WOs:** set Status → COMPLETE/CLOSED → `git mv` into:

```text
Documentation/06-development/Work-Orders/Complete/
```

Human session logs archive under `Documentation/01-operations/archive/YYYY-Www/` (WO-ARCH) — separate from closed work orders.
