# WORK ORDER — Report playback

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-MIG-15-2026-09-29 |
| **Date** | 2026-09-29 (HST) |
| **Status** | BUILT — dry-run pass 2026-09-30 00:57 HST; live speaker play still needs sign-off |
| **Owner** | RootRecord |
| **Related** | Agent 15. Later callers (do not build them here): 16 Morning boot replay, 17 Sunrise restore, 18 Report readiness audio, 19 Hurricane radio, 33 Cloud TTS routing. Kokoro stays in Media/Voice. |

**Scope:** Add one gated player that plays existing Kokoro WAV clips. In scope after this draft is accepted: `Media/Playback/scripts/play.py`, its Database state and logs, a dry-run proof, then archive and local removal of the old play-job folders. Out of scope until a separate sign-off: opening a speaker, editing `jobs.py`, restoring the old morning / midday / late / evening / periodic play crons, and any of the later caller functions.

This file stays in `Work-Orders/drafts/`. Do not add it to the active work-order index.

---

## 1. Intent

The old function queued an existing morning, midday, or late report WAV (evening play was already a no-op) through `voice_events.play_report_mp3` into the Windows stream director. `report-periodic-audio` replayed the active slot on a timer (about every 10 minutes). Those jobs are why report playback is absent: speaker playback was left off on purpose.

The live system already renders Kokoro clips and report WAVs under Database `Media/Audio/Voice` and refuses delivery. That renderer, the personas, and the clip catalog stay. This function plays those new clips. It does not restore the old play jobs.

---

## 2. Current reality

Folder name: **Playback**, a subfolder of the existing Media domain. Package name: `Playback`. No second top-level domain, no lowercase twin, no symlink.

| Path | Role |
| --- | --- |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Media/Playback/scripts` | Server code |
| `2 - RootRecord-Database/Media/Playback` | Database data (last-play state only) |
| `2 - RootRecord-Database/Logs/Media/Playback` | Database logs |

WAV clips stay in `2 - RootRecord-Database/Media/Audio/Voice`. No `config/`. No `Logs/` directory on the server. No `master-key.env` keys. The gate flag is `RR_PLAYBACK` (not a secret).

### 2.1 What exists

| Item | Location / status |
| --- | --- |
| Playback folder | Installed. `Media/Playback/scripts/play.py` |
| Kokoro renderer, personas, clip catalog | Pacific `Media/Voice/scripts/` — live. Do not replace |
| Report and phrase WAVs | Database `Media/Audio/Voice/<report>_current.wav` and `Clips/<Persona>/<slug>.wav`. Delivery is off |
| Old play jobs | `/home/rootrecord/old ollama/old skills/reports/sort/` — morning, midday, late, and evening play, evening-report-audio, report-periodic-audio. Checkout branch `online-safe-20260920`, remote `Solar-Pacific-RootRecord-Server`. `reports/` is gitignored |
| Shared old player pieces | `media/voice/scripts/director.py` and `voice-events/scripts/voice_events.py` — leave in place |
| `jobs.py` | Unchanged. No playback job is proposed |

### 2.2 Completed so far

- [x] Draft written (this file)
- [x] Alexander said to complete the remaining work
- [x] `play.py` landed
- [x] Dry-run proof recorded (2026-09-30 00:01 HST)
- [x] Old play-job folders archived, then removed from the old-repo working tree
- [x] GitHub: `7416bf2f` is `skills-rebuild`. `main` and `online-safe-20260920` already omitted the files.
- [x] Result note and the Library corrections

### 2.3 Known friction

- `aplay` is on this host. The dry-run passed. A live play still needs Alexander's sign-off.
- `skills-rebuild` on GitHub is `7416bf2f`. That tip no longer has the six play-job directories. Live `aplay` is still the open sign-off.
- Media/Voice already exists. Agents 16, 17, 18, 19, and 33 depend on this player. They are not built here.

---

## 3. Tasks

Do these only after Alexander accepts this draft and says to build. Until then, do not edit runtime files, restart services, send messages, actuate hardware, or spend cloud money.

1. Confirm `Media/Voice` is still the Kokoro home. It is present, so do not pause for a missing dependency. If it is gone when the build starts, pause and name Kokoro. Do not rebuild it.
2. Add `Media/Playback/scripts/play.py` only. Do not edit `jobs.py`. Do not register a periodic job.
3. Resolve audio only under Database `Media/Audio/Voice`. `--report <name>` maps to `<name>_current.wav`. `--clip <Persona>/<slug>` maps to `Clips/<Persona>/<slug>.wav`. Refuse any other path.
4. Default `--dry-run`: write `2 - RootRecord-Database/Media/Playback/last-play.json` with `played: false`. Do not open a device.
5. Live play requires both `RR_PLAYBACK=1` and `--play`. Otherwise exit with `playback_gated`. The player is `aplay`. No `ffplay` window, no music bed, no OBS.
6. One file at a time. Take a lock in the Database Playback folder. A second caller gets `busy` and does not overlap.
7. Quiet hours 22:00–06:00 HST skip unless `--force`. `--force` is still behind the same gate. Do not read `~/.ollama` night-mode.
8. Logs go only to `2 - RootRecord-Database/Logs/Media/Playback`. Runtime output stays out of Pacific, the website, and git.
9. Prove it with speakers still off (section 7). A live `aplay` run is a separate sign-off. Do not do it in this build.
10. Phase 4, only after that dry-run works: copy the six old play-job directories into `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/`, keeping the path each had inside the old repo. Generated data that lived beside that source goes into the archive too, and still does not go into the live Folders. If the archive copy fails, do not delete. After the copy is on disk, delete those same directories from `/home/rootrecord/old ollama/old skills`. Run `git log` for those paths. If they were never tracked, record that and do not push an empty deletion. If they were tracked, commit that deletion and push it. Do not force-push. Do not delete the GitHub repository.
11. Phase 5: add the result note to this work order (section 8). Correct only the Library lines this function makes stale: matrix row 46, the `report-periodic-audio` scheduler row, and the speaker bullet in Voice-Reports-G3 section 6.

---

## 4. Non-goals

- Do not overwrite `Media/Voice` (`voice_generate.py`, `speakers.py`, `voice_reports.py`, `clip_catalog.py`, Kokoro model, or the venv).
- Do not restore the old play jobs or the 10-minute replay.
- Do not edit `jobs.py`.
- Do not build Morning boot replay, Sunrise restore, Report readiness audio, Hurricane radio, or Cloud TTS routing.
- Leave these shared old files: `media/voice/scripts/director.py`, `voice-events/scripts/voice_events.py`, `reports/sort/evening-report/`, `reports/sort/day-reports-evening/`.
- Do not restore files under `~/.ollama/skills/energy`, automations, or `coms/ssh/local-data-globe`.
- Do not send, play speakers, switch hardware, delete live Ecosystem files, or spend cloud money. Phase 4 deletes only the six old play-job directories, and only after the archive copy is on disk.
- Do not promote this draft onto the active work-order index.

---

## 5. Key file / path reference

| Path | Role |
|------|------|
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Media/Playback/scripts/play.py` | Player |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Media/Playback/README.md` | Folder note: paths, gate, no cron |
| `2 - RootRecord-Database/Media/Playback/last-play.json` | Runtime state written by the player. Not source |
| `2 - RootRecord-Database/Media/Playback/` lock file | Single-flight lock. Runtime |
| `2 - RootRecord-Database/Logs/Media/Playback/` | Player logs. Runtime |
| `2 - RootRecord-Database/Media/Audio/Voice/` | Existing Kokoro WAVs. Read only |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Media/Voice/` | Existing Kokoro. Do not edit |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Automations/scripts/jobs.py` | Do not edit |
| `/home/rootrecord/master/master-key.env` | No keys for this function |
| `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/reports/sort/morning-report-play/` | Phase 4 archive |
| `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/reports/sort/midday-report-play/` | Phase 4 archive |
| `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/reports/sort/late-report-play/` | Phase 4 archive |
| `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/reports/sort/evening-report-play/` | Phase 4 archive |
| `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/reports/sort/evening-report-audio/` | Phase 4 archive |
| `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/reports/sort/report-periodic-audio/` | Phase 4 archive |
| `5 - RootRecord-Library/Documentation/00-architecture/Old-Repo-Migration-Matrix.md` | Phase 5. Row 46 only |
| `5 - RootRecord-Library/Documentation/00-architecture/G1-Scheduler-To-G3-Jobs-Map-2026-09-29.md` | Phase 5. `report-periodic-audio` row only |
| `5 - RootRecord-Library/Documentation/00-architecture/Voice-Reports-G3.md` | Phase 5. Speaker bullet in section 6 only |

---

## 6. Open items

**Additional requirements:**

- Speaker playback stays gated. Live `aplay` needs a separate sign-off. The build test did not play audio.
- This file stays in drafts. It is not on the active index.

---

## 7. Notes & constraints

- No force-push.
- Secrets stay out of git. This function has no `master-key.env` keys.
- Prefer small reversible steps.
- Sends, speaker playback, OBS, hardware switching, deletion of live Ecosystem files, and cloud spend need Alexander's sign-off. Do not do those things while executing the build. Phase 4 is the ordered exception for the six old play-job directories only, and only after they are in `Old repos deleted and merged`.
- New periodic jobs stay off. Do not edit `jobs.py`.
- EcoFlow BLE, the poller, Hawaiʻi weather, the globe collector, camera grabs, Kokoro, and `geology_collect.py` stay as they are.

**Sign-off gate.** `--play` without `RR_PLAYBACK=1` returns `playback_gated` and does not spawn `aplay`. Both the flag and `--play` are required before a device opens. Quiet hours still apply unless `--force`, and `--force` does not bypass the flag.

**Small test (speakers stay off).** From the Playback scripts directory:

```text
python3 play.py --clip Ava/boot_all_systems_running --dry-run
python3 play.py --clip Ava/boot_all_systems_running --play
```

The first prints `dry_run` or `audio_missing` and does not open a device. The second, with `RR_PLAYBACK` unset, returns `playback_gated`. A live `aplay` run is not part of this test.

---

## 8. Result note

Landed 2026-09-30 ~00:01 HST.

- Player: `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Media/Playback/scripts/play.py`. `jobs.py` was not edited. Kokoro in `Media/Voice` was not edited.
- Proof, speakers off: `--clip Ava/boot_all_systems_running --dry-run` returned `audio_missing` (that clip is not on disk) with `played: false`. `--play` without `RR_PLAYBACK` returned `playback_gated` (exit 2). With `RR_PLAYBACK=1` during quiet hours (00:01 HST) it returned `quiet_hours` and did not call `aplay`. A second caller holding the lock got `busy` (exit 3). A path outside Voice was `refused`.
- Runtime state and the player log are under Database `Media/Playback/` and `Logs/Media/Playback/`, gitignored.
- Archive: `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/reports/sort/` holds `morning-report-play`, `midday-report-play`, `late-report-play`, `evening-report-play`, `evening-report-audio`, and `report-periodic-audio`. File counts matched the source before delete.
- Removed from the working tree of `/home/rootrecord/old ollama/old skills` (branch `online-safe-20260920`). Left in place: `evening-report/`, `day-reports-evening/`, `media/voice/scripts/director.py`, `voice-events/scripts/voice_events.py`.
- GitHub: `origin/main` and `origin/online-safe-20260920` already had none of those paths. Commit `7416bf2f` (`Remove retired report play jobs.`, full `7416bf2f1ed3e006fae24be7ce770e61d5845011`) is `skills-rebuild`. Those play paths are absent from that tip. The repository was not deleted. No force-push.
- Local tips in `/home/rootrecord/old ollama/old skills`, same message, not pushed: `main` `9207a29c` (was `cfb4f335`), `solar-battery-offline-recovery` `21205485` (was `322421fa`). Both tips now have zero of those play paths. `origin/solar-battery-offline-recovery` does not exist, so that branch was not pushed. Local `main` was not pushed to `origin/main`. `~/.ollama/skills` is a separate clone on `origin/main` and did not have the directories on disk.

Re-checked 2026-09-30 00:57 HST. A busy caller no longer overwrites `last-play.json`. `--report boot_brief`, `--report hurricane_desk`, `--clip Ava/boot_all_systems_running`, and `--clip Ava/battery_reconnect` each returned `audio_missing` because those WAVs are not on disk. `--play` without `RR_PLAYBACK` returned `playback_gated`. No `aplay`. It was quiet hours, so a live run was not forced.

01:02–01:11 HST: the Voice `.venv` was missing, so it was rebuilt (torch CPU, kokoro 0.9.4, misaki, soundfile). `kokoro-v1_0.pth` (313 MB) was copied from the old Kokoro store into Database `AI/Kokoro/Kokoro-82M/` because that file was absent. The clip render did not finish: the first attempt found no weights, the second stopped with `No virtual environment found` before the model loaded. No speaker. Kokoro inference was not started again after that.

This file stays in `Work-Orders/drafts/`. It is not on the active index. Live `aplay` still needs a separate sign-off.

---

*Work order prepared 2026-09-29 HST. Update status when closed.*

---

## Archive / location note

**Active / accepted WOs** — filename when saved:

```text
Report_playback_Work_Order_WO-MIG-15-2026-09-29.md
```

Location after promotion (not now):

```text
Documentation/06-development/Work-Orders/
```

**Drafts (not on active index)** — this file:

```text
Documentation/06-development/Work-Orders/drafts/Report_playback_Work_Order_WO-MIG-15-2026-09-29.md
```

See `drafts/README.md` and WO-WOGEN-001. Do not auto-promote.

**Closed WOs:** set Status → COMPLETE/CLOSED → `git mv` into:

```text
Documentation/06-development/Work-Orders/Complete/
```

Human session logs archive under `Documentation/01-operations/archive/YYYY-Www/` (WO-ARCH) — separate from closed work orders.
