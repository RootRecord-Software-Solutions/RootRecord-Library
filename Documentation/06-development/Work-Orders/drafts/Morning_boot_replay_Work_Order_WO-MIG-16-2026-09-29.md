# WORK ORDER — Morning boot replay

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-MIG-16-2026-09-29 |
| **Date** | 2026-09-29 (HST) |
| **Status** | BUILT — dry-run replay landed; speakers off; old files archived and removed locally and on GitHub. Not promoted to the active index. |
| **Owner** | RootRecord |
| **Related** | Agent 16. Depends on Report playback (agent 15) before any build. `voice_reports.py boot_brief` stays the text and WAV source. |

**Scope:** Same-day morning replay of the live `boot_brief` Kokoro WAV. That replay landed 2026-09-30 as a dry-run handoff to `Media/Playback`. Speaker playback and `jobs.py` stay off. Sunrise restore, readiness audio, and hurricane radio stay out of scope.

---

## 1. Intent

The old job replayed today's morning-boot audio at :32 HST until noon, then disarmed. It did not synthesize speech. Source archive: `Old repos deleted and merged/Solar-Pacific-RootRecord-Server-Old/morning-boot-replay/scripts/job.py`.

The live system already writes the boot brief and must be kept: `voice_reports.py boot_brief` (Ava), morning edition before 12:00 HST and midday after, text plus a WAV from `voice-render.sh`. Speaker delivery stays off.

New code wins. Replay the Kokoro WAV `boot_brief_current.wav` (default `2 - RootRecord-Database/Media/Audio/Voice/`). Do not restore the old MP3 director.

---

## 2. Current reality

Folder: `MorningBootReplay`, installed under Media. `boot_brief` stays in `Media/Voice`. One capitalized folder, same name in all three places. No lowercase twin, no symlink, no `Logs/` on the server, no `config/` (no secrets).

| Path | Role |
| --- | --- |
| Code | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Media/MorningBootReplay/scripts` (package `MorningBootReplay`) |
| Database | `2 - RootRecord-Database/Media/MorningBootReplay/replay-last.json` (active database, `at` field; not committed) |
| Logs | `2 - RootRecord-Database/Logs/Media/MorningBootReplay/` |
| Secrets | none. No `master-key.env` keys. |

### 2.1 What exists

| Item | Location / status |
| --- | --- |
| Folder `MorningBootReplay` | Installed. `scripts/replay.py` arms and runs. Speakers stay off |
| `boot_brief` text and WAV path | `Media/Voice/scripts/voice_reports.py` (`b_boot_brief`). WAV default `2 - RootRecord-Database/Media/Audio/Voice/boot_brief_current.wav` |
| Speaker playback | Off. Replay calls `Media/Playback/scripts/play.py --dry-run` only |
| ON_BOOT `voice_boot_brief` (`RR_VOICE_BOOT`) | Proposed in documentation only. Not in `jobs.py` |
| Report playback | `Media/Playback`. This function does not replace it |
| Midday board | `Reports/scripts/report_board.py`. `status == done` disarms replay |
| Old replay job | Archived. Removed locally (`fb3b6149`) and on GitHub (`9231029`) |

### 2.2 Completed so far

- [x] Draft work order written (this file). Status stays OPEN — draft, not accepted for execution
- [x] Build requested. Report playback is `Media/Playback`. This function was built. The player was not rebuilt here.
- [x] `MorningBootReplay` code and dry-run test (played + last_played; midday done disarms). Speakers stayed off.
- [x] Phase 4 archive copy, then local deletion and commit `fb3b6149` on `online-safe-20260920`
- [x] GitHub: `Solar-Pacific-RootRecord-Server-Old` `main` `9231029` removed the packet. Repository kept. No force-push.
- [x] Phase 5 result note and the Library pages this function made stale

### 2.3 Known friction

- Report playback is `Media/Playback`. This function calls `play.py --dry-run` only. It does not open a speaker.
- `jobs.py`, the Vercel app shell, and `master-key.env` are shared. Leave them alone. If one of them is already being edited when build starts, pause.
- `voice_reports.py` is shared by the other spoken reports. Prefer not to edit it.
- Speaker playback, sends, OBS, hardware switching, and cloud spend need Alexander's sign-off.

---

## 3. Tasks

Done, in this order. Speaker playback and `jobs.py` stayed off.

1. Pause if Report playback has no Folder. Name that function. Do not build the player, Kokoro, OBS, sunrise restore, or readiness audio.
2. Add `Media/MorningBootReplay/scripts/replay.py` plus package init and a short README. State file `replay-last.json` under the Database path, with an `at` time like the other active last files. Logs only under the Logs path. Do not put a `Logs/` directory on the server.
3. `arm`: only when today's `boot_brief` WAV is a morning file (name and mtime are today, HST, and the name is not midday, evening, or late). Set `enabled`, `day`, and `until` capped at noon HST.
4. `run`: skip if disabled, not :32 (unless `play_once`), past noon, wrong day, or midday board status is `done`. Refuse a stale or non-morning file and disarm. On success, clear `play_once` and record `last_played`.
5. Hand the WAV to Report playback's player. Do not call `aplay` or any speaker from this folder.
6. Leave `jobs.py` and the existing `voice_boot_brief` block alone. Gated proposal, written here only, not registered:

```python
{
    "id": "morning_boot_replay",
    "enabled": os.environ.get("RR_MORNING_BOOT_REPLAY", "0") == "1",
    "schedule": "minute 32, hours before noon HST",
    "description": "Replay today's morning boot_brief WAV until noon. No TTS. No speaker until sign-off.",
    "command": 'python3 "Media/MorningBootReplay/scripts/replay.py"',
}
```

`RR_MORNING_BOOT_REPLAY` defaults to `0`. The command does not synthesize speech.

7. Do not edit `voice_reports.py` unless it is idle and the only change is a comment that replay is a separate folder. Prefer not touching it.

---

## 4. Non-goals

- Do not replace Kokoro, `voice_generate.py`, `geology_collect.py`, the EcoFlow poller, Hawaiʻi weather, or the globe collector.
- Do not port sunrise-restore, readiness audio, hurricane radio, or the old play jobs. Those belong to other agents.
- Do not import logs, samples, last-state files, generated reports, `__pycache__`, or `DAILY.md` into Pacific, Database, the website, or git.
- Do not send messages, play speakers, switch OBS or other hardware, delete live Ecosystem files, or spend cloud money.
- Do not edit other agents' files. Do not promote this draft onto the active index.
- Do not delete a GitHub repository. Do not force-push. Do not restore `~/.ollama/skills/`.

---

## 5. Key file / path reference

| Path | Role |
|------|------|
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Media/MorningBootReplay/scripts` | Code to add at build time (package `MorningBootReplay`) |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Media/MorningBootReplay/scripts/replay.py` | `arm` and `run` |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Media/MorningBootReplay/scripts/__init__.py` | Package init |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Media/MorningBootReplay/README.md` | Short folder note |
| `2 - RootRecord-Database/Media/MorningBootReplay/replay-last.json` | Active-database state. `at` plus enabled, day, until, wav. Not committed |
| `2 - RootRecord-Database/Logs/Media/MorningBootReplay/` | Logs only |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Media/Voice/scripts/voice_reports.py` | Read-only. `b_boot_brief` stays the text source |
| `2 - RootRecord-Database/Media/Audio/Voice/boot_brief_current.wav` | Read-only morning WAV to replay |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Reports/scripts/report_board.py` | Read-only midday `done` disarm |
| `Old repos deleted and merged/Solar-Pacific-RootRecord-Server-Old/morning-boot-replay/scripts/job.py` | Archived old source. Removed from the local old repo |

---

## 6. Open items

**Additional requirements:**

- Speaker playback stays off until Alexander signs off. `RR_MORNING_BOOT_REPLAY` is not in `jobs.py`.

---

## 7. Notes & constraints

- No force-push.
- Secrets stay out of git. This function has no `master-key.env` keys.
- Prefer small reversible steps.
- Sends, speaker playback, OBS, hardware switching, deletion of live Ecosystem files, and cloud spend require Alexander's sign-off. Do not do those things in the draft pass.
- Proof test, after a later build, with `--dry-run` and a temp database root, no audio device: a today morning WAV plus `play_once` returns `played` and writes `last_played`; a midday `done` board returns `disarmed`.

### Phase 4 (after the migration works, not now)

Copy this function's old files into `/home/rootrecord/RootRecord-Ecosystem/Old repos deleted and merged/<old-repo-name>/`, keeping the path they had inside the old repo. Generated data that lived beside that source goes into the archive too, and still does not go into the live Folders. Then delete those same files from the old repo on this machine and on GitHub.

- GitHub: `Solar-Pacific-RootRecord-Server-Old` packet `morning-boot-replay` only. Do not delete the repository.
- Local skill tree: `/home/rootrecord/old ollama/old skills/morning-boot-replay`.
- Leave shared scheduler files. If a file is shared with another agent's function, leave it and name it here.
- If the archive copy fails, do not delete.
- Do not restore `~/.ollama/skills/`.

### Phase 5 (after phase 4, not now)

Add a short result note to this work order: what landed, what was archived, what was removed on GitHub, and the new status. Correct only the Library pages this function made stale:

- G1 scheduler map row for `morning-boot-replay`
- Old-repo migration matrix row 25, replay clause only
- `Voice-Reports-G3.md`
- `Media/Voice/README.md`
- Boot-brief row of the residual-path table

Do not rewrite unrelated work orders.

### Result note

Landed 2026-09-30: `Media/MorningBootReplay/scripts/replay.py`. It replays today's morning `boot_brief_current.wav` until noon HST and hands it to `Media/Playback/scripts/play.py --report boot_brief --dry-run`. `run` arms itself when today's state is not already disarmed. A same-day disarm stays off. This folder never calls `aplay`. Live build 01:02 HST: `voice_reports.py boot_brief` wrote `2 - RootRecord-Database/Media/Audio/Voice/boot_brief_current.wav` (32.9 s, QC PASS, no speaker). Replay armed and a `play_once` dry-run set `replay-last.json` to `detail: dry_run`. `jobs.py` was not edited. Gate `RR_MORNING_BOOT_REPLAY` stays off.

Archived to `Old repos deleted and merged/Solar-Pacific-RootRecord-Server-Old/morning-boot-replay/` and `.../origin/ns/apps/core/crons/since_last_fire/morning_boot_replay.py`. Removed those paths from the local old repo (`/home/rootrecord/old ollama/old skills`, commit `fb3b6149`). Shared files left in place: `scheduler-clock/scripts/scheduler.py`, `scheduler-clock/CURRENT.md`, `ecosystem-index/`, `companions/dev-desk/lib/deskState.mjs`, `ecosystem-history/scripts/one_shot_morning_boot_tts.py`, `origin/scripts/routes/desktop.py`.

GitHub: `Solar-Pacific-RootRecord-Server-Old` `main` moved `fd0a9c0..9231029`. That commit deletes `morning-boot-replay/` and `origin/ns/apps/core/crons/since_last_fire/morning_boot_replay.py` only. The repository was not deleted. No force-push.

---

*Work order prepared 2026-09-29 HST. Update status when closed.*

---

## Archive / location note

This file is a draft. Do not auto-promote it onto the active index.

**Active / accepted WOs** — filename when saved:

```text
Morning_boot_replay_Work_Order_WO-MIG-16-2026-09-29.md
```

Location after Alexander accepts it:

```text
Documentation/06-development/Work-Orders/
```

**Drafts (not on active index)** — this file lives here:

```text
Documentation/06-development/Work-Orders/drafts/
```

See `drafts/README.md` and WO-WOGEN-001. Do not auto-promote.

**Closed WOs:** set Status → COMPLETE/CLOSED → `git mv` into:

```text
Documentation/06-development/Work-Orders/Complete/
```

Human session logs archive under `Documentation/01-operations/archive/YYYY-Www/` (WO-ARCH) — separate from closed work orders.
