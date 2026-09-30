# WORK ORDER — Morning boot replay

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-MIG-16-2026-09-29 |
| **Date** | 2026-09-29 (HST) |
| **Status** | OPEN — draft, not accepted for execution |
| **Owner** | RootRecord |
| **Related** | Agent 16. Depends on Report playback (agent 15) before any build. `voice_reports.py boot_brief` stays the text and WAV source. |

**Scope:** Add same-day morning replay onto the live `boot_brief` Kokoro WAV. This draft is the before-documentation only. Building, speaker playback, `jobs.py`, `master-key.env`, and Library corrections wait until Alexander accepts this draft and says to build. Sunrise restore, readiness audio, hurricane radio, and the shared player are out of scope.

---

## 1. Intent

The old job replayed today's morning-boot audio at :32 HST until noon, then disarmed. It did not synthesize speech. Source: `/home/rootrecord/old ollama/old skills/morning-boot-replay/scripts/job.py`.

The live system already writes the boot brief and must be kept: `voice_reports.py boot_brief` (Ava), morning edition before 12:00 HST and midday after, text plus a WAV from `voice-render.sh`. Speaker delivery stays off.

New code wins. Replay the Kokoro WAV `boot_brief_current.wav` (default `2 - RootRecord-Database/Media/Audio/Voice/`). Do not restore the old MP3 director.

---

## 2. Current reality

Folder: `MorningBootReplay`. It belongs in Media. `boot_brief` already lives in `Media/Voice`. Morning boot replay is not installed. One capitalized folder, same name in all three places. No lowercase twin, no symlink, no `Logs/` on the server, no `config/` (no secrets).

| Path | Role |
| --- | --- |
| Code | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Media/MorningBootReplay/scripts` (package `MorningBootReplay`) |
| Database | `2 - RootRecord-Database/Media/MorningBootReplay/` (state JSON only; created at runtime, not committed) |
| Logs | `2 - RootRecord-Database/Logs/Media/MorningBootReplay/` |
| Secrets | none. No `master-key.env` keys. |

### 2.1 What exists

| Item | Location / status |
| --- | --- |
| Folder `MorningBootReplay` | Not installed |
| `boot_brief` text and WAV path | `Media/Voice/scripts/voice_reports.py` (`b_boot_brief`). WAV default `2 - RootRecord-Database/Media/Audio/Voice/boot_brief_current.wav` |
| Speaker playback | Absent. `speakers.py` and `voice-render.sh` say no delivery |
| ON_BOOT `voice_boot_brief` (`RR_VOICE_BOOT`) | Proposed in documentation only. Not in `jobs.py` |
| Report playback (agent 15) | No Folder yet. Build pauses until that Folder exists |
| Midday board | `Reports/scripts/report_board.py`. `status == done` disarms replay |
| Old replay job | `/home/rootrecord/old ollama/old skills/morning-boot-replay/scripts/job.py` (read-only until phase 4) |

### 2.2 Completed so far

- [x] Draft work order written (this file). Status stays OPEN — draft, not accepted for execution
- [x] Build requested. Paused 2026-09-29: Report playback (agent 15) has no Folder. That function was not built.
- [ ] Report playback Folder is in place
- [ ] `MorningBootReplay` code, state, and dry-run test
- [ ] Phase 4 archive and old-repo deletion
- [ ] Phase 5 result note and Library corrections

### 2.3 Known friction

- Report playback (agent 15) has no Folder yet. Checked 2026-09-29 under Pacific `Media` (`Voice`, `Video` only) and the server top level. This function queues onto that player and does not build it. Build stays paused until that Folder exists.
- `jobs.py`, the Vercel app shell, and `master-key.env` are shared. Leave them alone. If one of them is already being edited when build starts, pause.
- `voice_reports.py` is shared by the other spoken reports. Prefer not to edit it.
- Speaker playback, sends, OBS, hardware switching, and cloud spend need Alexander's sign-off.

---

## 3. Tasks

Build later, in this order. Do not start these until Alexander accepts this draft and says to build.

1. Pause if Report playback has no Folder. Name that function. Do not build the player, Kokoro, OBS, sunrise restore, or readiness audio.
2. Add `Media/MorningBootReplay/scripts/replay.py` plus package init and a short README. State file `morning-boot-replay.json` under the Database path. Logs only under the Logs path. Do not put a `Logs/` directory on the server.
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
| `2 - RootRecord-Database/Media/MorningBootReplay/morning-boot-replay.json` | Runtime state. Not committed. Not imported from the old repo |
| `2 - RootRecord-Database/Logs/Media/MorningBootReplay/` | Logs only |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Media/Voice/scripts/voice_reports.py` | Read-only. `b_boot_brief` stays the text source |
| `2 - RootRecord-Database/Media/Audio/Voice/boot_brief_current.wav` | Read-only morning WAV to replay |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Reports/scripts/report_board.py` | Read-only midday `done` disarm |
| `/home/rootrecord/old ollama/old skills/morning-boot-replay/scripts/job.py` | Old source. Read-only until phase 4 |

---

## 6. Open items

**Additional requirements:**

- Build was requested. It is paused. Missing function: **Report playback** (agent 15). No Folder is in place. Do not build that player here.
- Report playback (agent 15) Folder must exist before the Morning boot replay build continues.
- Speaker playback stays off until Alexander signs off, even if `RR_MORNING_BOOT_REPLAY` is later set to `1`.
- Phase 4 and phase 5 below are not done. This file has no result note yet.

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

Not written. Phase 4 has not run.

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
