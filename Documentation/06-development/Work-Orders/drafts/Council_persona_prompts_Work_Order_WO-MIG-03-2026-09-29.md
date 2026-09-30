# WORK ORDER — Council persona prompts

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-MIG-03-2026-09-29 |
| **Date** | 2026-09-29 (HST) |
| **Status** | OPEN — draft, not accepted for execution |
| **Owner** | RootRecord |
| **Related** | Agent 03, wave A. Later functions that wait on this Folder: 24 Kilauea public draft queue; 25 Council quake Telegram posts; 27 Council health alerts; 29 Economy brief. Matrix row 57. |

**Scope:** Add the Ava, Bruce, and Carly chat system prompts to the live council relay so an opted-in reply uses those prompts. Keep `speakers.py`, `speech_scrub.py`, quiet relay behavior, the `*-telegram` Modelfiles, and the generic infer default for every other caller. This draft does not authorize runtime edits, a relay restart, a Telegram send, a model load, or a GitHub deletion.

---

## 1. Intent

Old council replies spoke as Ava Ivy, Bruce Monitor, and Carly Mal. `council/council-telegram/scripts/personas.py` loaded `agents/{ava-ivy,bruce-monitor,carly-mal}/prompt.md` and prefixed `SPEAK_LOCK`. Those three chat prompts were not copied. Kokoro voice map and speech scrub already run and must stay: `Media/Voice/scripts/speakers.py` and `Media/Voice/scripts/speech_scrub.py`. The live relay still calls `run-infer.sh`. On the NPU path the system text is the short generic block (`You are RootRecord {voice}. Be brief.`). `RR_SPEC_SYS` replaces that block only when specialist routing is on. Quiet mode (`RR_RELAY_REPLIES=0`) never infers. Ollama fallback already has its own `*-telegram` Modelfiles; those stay as they are.

This function adds the three prompts to the current relay. It does not replace `speakers.py`.

---

## 2. Current reality

### 2.1 What exists

Folder name, used in all three places: `CouncilPersona` (inside Communications). No lowercase twin. No second top-level domain.

| Item | Location / status |
| --- | --- |
| Server code | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/CouncilPersona/scripts` — not created yet |
| Database data | `2 - RootRecord-Database/Communications/CouncilPersona/` — not created yet. Load stamps only (voice, path, sha256, char count). No prompt body. |
| Database logs | `2 - RootRecord-Database/Logs/Communications/CouncilPersona/` — not created yet. One JSON line per load. No prompt body. No `Logs/` directory on the server. |
| Prompt source (kept as source, not Database) | Planned: `Communications/CouncilPersona/prompts/{ava,bruce,carly}.md` |
| Old loader | `/home/rootrecord/old ollama/old skills/council/council-telegram/scripts/personas.py` (tracked in old-skills checkout `679fd86`) |
| Old prompts | `/home/rootrecord/old ollama/old skills/agents/{ava-ivy,bruce-monitor,carly-mal}/prompt.md` — on disk, gitignored (`agents/`), not on GitHub |
| Live relay | `Communications/telegram/scripts/council-relay.py` — quiet by default; `run_infer` does not load a persona prompt |
| Live infer | `System/scripts/plumbing/run-infer.sh` — FLM generic system unless `RR_SPEC_SYS` is set; Ollama fallback uses Modelfiles |
| Voice map (keep) | `Media/Voice/scripts/speakers.py` |
| Speech scrub (keep) | `Media/Voice/scripts/speech_scrub.py` (`SPEAK_LOCK` already here) |
| `master-key.env` keys | None. This function adds no key names. |

### 2.2 Completed so far

- [x] Old prompts and `personas.py` located. Live relay and infer path read. `speakers.py` and `speech_scrub.py` confirmed present.
- [x] This draft written. Not on the active work-order index.
- [ ] Alexander has not accepted this draft for execution.
- [ ] `CouncilPersona` code, prompts, Database stamp, and Logs line not created.
- [ ] `council-relay.py` and `run-infer.sh` not extended.
- [ ] Offline `system_for` test not run.
- [ ] Phase 4 archive not done. Phase 5 result note not written. Matrix row 57 not corrected.

### 2.3 Known friction

- `system_for()` in the old loader also pulls feelings, self-repair, desk wrap, and brainstorm. Those are not this function.
- `run-infer.sh` overwrites `RR_SPEC_SYS` inside `do_flm`, so a parent export of that variable does not carry a persona through. The build passes a separate `RR_PERSONA_SYSTEM` and reads it only when `RR_SPEC_SYS` is empty.
- `worker.py`, `pipeline.py`, `classify.py`, and `moderation.py` in old `council-telegram` still import `personas.py`. The three `prompt.md` files are gitignored. Phase 4 archives copies and leaves the old files in place.
- Old-skills checkout `679fd86` and `~/.ollama/skills` `1dcee66` are different commits of `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server`. Do not push from the old checkout.
- If `run-infer.sh` or `council-relay.py` is already being edited when the build starts, pause.

---

## 3. Tasks

Do not start these until Alexander accepts this draft and says to build. No other function has to exist first. There is no missing dependency Folder.

1. Add `Communications/CouncilPersona/scripts/personas.py`. Load `prompts/{ava,bruce,carly}.md`. Prefix `SPEAK_LOCK` from the existing `Media/Voice/scripts/speech_scrub.py`. Return `system_for(voice)`. Do not port `CLASSIFIER_SYSTEM`, feelings, self-repair, desk wrap, or brainstorm.
2. Copy the three old `prompt.md` files into `Communications/CouncilPersona/prompts/{ava,bruce,carly}.md`.
3. Add `Communications/CouncilPersona/README.md` naming the Folder and the three paths.
4. In `council-relay.py` `run_infer` only, export `RR_PERSONA_SYSTEM` from `system_for`. Quiet mode never calls `run_infer`, so held inbox behavior stays the same. `relay-inbox-replay.py` already calls `run_infer`, so a later `--send` uses the same prompts. Do not add a second send path.
5. In `run-infer.sh` `do_flm` only: if `RR_SPEC_SYS` is empty and `RR_PERSONA_SYSTEM` is set, use the persona text. An unset variable keeps today's generic system. Leave the Ollama fallback unchanged. If `run-infer.sh` or `council-relay.py` is already being edited, pause.
6. On a successful load, write a stamp (voice, path, sha256, char count; no prompt body) under `2 - RootRecord-Database/Communications/CouncilPersona/` and one JSON line under `2 - RootRecord-Database/Logs/Communications/CouncilPersona/`.
7. Run the offline test in Notes. Do not set `RR_RELAY_REPLIES=1`, restart the relay, call Telegram, or load FLM or Ollama.
8. After that test passes: archive copies of old `personas.py` and the three `prompt.md` files under `/home/rootrecord/RootRecord-Ecosystem/Old repos deleted and merged/Solar-Pacific-RootRecord-Server/`, keeping the path each file had inside the old repo. Do not delete those files from the old repo or from GitHub. Name the shared importers in the result note. Do not push from the old-skills checkout. Do not force-push. Do not delete the GitHub repository.
9. Then add the phase 5 result note to this work order and correct only Library matrix row 57.

---

## 4. Non-goals

- Do not replace or rewrite `speakers.py` or `speech_scrub.py`.
- Do not edit the `*-telegram` Modelfiles, `jobs.py`, `voices.conf`, `relay.conf`, or `master-key.env`.
- Do not port `CLASSIFIER_SYSTEM` or the rest of `council-telegram` (worker, pipeline, classify, moderation, feelings, repair, desk wrap, brainstorm).
- Do not build agent 24 (Kilauea public draft queue), 25 (Council quake Telegram posts), 27 (Council health alerts), or 29 (Economy brief).
- Do not open a second top-level domain. Do not add a `Logs/` directory on the server.
- Do not import logs, samples, last-state files, or other generated runtime output into Pacific, Database source, the website, or git. The load stamp and the log line are the only runtime records, and they omit prompt text.
- Do not turn replies on, restart the relay, send Telegram, play audio, switch hardware, or spend cloud money.
- Do not delete old `personas.py` or the three `prompt.md` files. They stay because other old council scripts still import the loader, and the prompts were never on GitHub.

---

## 5. Key file / path reference

| Path | Role |
|------|------|
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/CouncilPersona/scripts/personas.py` | New loader. `system_for(voice)` = `SPEAK_LOCK` + that voice's prompt. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/CouncilPersona/prompts/ava.md` | Ava Ivy chat prompt, copied from `agents/ava-ivy/prompt.md`. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/CouncilPersona/prompts/bruce.md` | Bruce Monitor chat prompt, copied from `agents/bruce-monitor/prompt.md`. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/CouncilPersona/prompts/carly.md` | Carly Mal chat prompt, copied from `agents/carly-mal/prompt.md`. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/CouncilPersona/README.md` | Folder name and the three paths. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/telegram/scripts/council-relay.py` | Extend `run_infer` only: export `RR_PERSONA_SYSTEM`. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/System/scripts/plumbing/run-infer.sh` | Extend `do_flm` only: persona text when `RR_SPEC_SYS` is empty and `RR_PERSONA_SYSTEM` is set. |
| `2 - RootRecord-Database/Communications/CouncilPersona/` | Load stamp. No prompt body. |
| `2 - RootRecord-Database/Logs/Communications/CouncilPersona/` | One JSON line per load. No prompt body. |
| `Media/Voice/scripts/speakers.py` | Keep. Do not replace. |
| `Media/Voice/scripts/speech_scrub.py` | Keep. Source of `SPEAK_LOCK`. |
| `/home/rootrecord/old ollama/old skills/council/council-telegram/scripts/personas.py` | Old loader. Archive a copy in phase 4. Leave in place (shared with `worker.py`, `pipeline.py`, `classify.py`, `moderation.py`). |
| `/home/rootrecord/old ollama/old skills/agents/{ava-ivy,bruce-monitor,carly-mal}/prompt.md` | Old prompts. Archive copies in phase 4. Leave in place (gitignored; not on GitHub). |
| `5 - RootRecord-Library/Documentation/00-architecture/Old-Repo-Migration-Matrix.md` | Phase 5 only: correct row 57. |

---

## 6. Open items

**Additional requirements:**

- Alexander accepts this draft and says to build before any file outside this draft is written.
- If `run-infer.sh` or `council-relay.py` is already being edited at build time, pause and name the file.
- Phase 4 does not delete shared files and does not push the old-skills checkout.
- Phase 5 result note is empty until the build and the archive copy exist. It will record what landed, the archive path, and that GitHub was not changed because the prompts are gitignored and `personas.py` stays for the other council scripts.

---

## 7. Notes & constraints

- No force-push.
- Secrets stay out of git. This function has no `master-key.env` keys.
- Prefer small reversible steps.
- Sign-off gate: do not set `RR_RELAY_REPLIES=1`, restart the relay, call Telegram `sendMessage`, load FLM or Ollama, play speakers, switch hardware, or spend cloud money. `relay-inbox-replay.py --send` stays refused unless Alexander later opts in with both `--send` and `RR_RELAY_REPLIES=1`.
- Proof test, offline only: `system_for("ava")`, `system_for("bruce")`, and `system_for("carly")` each contain that person's name (`Ava Ivy`, `Bruce Monitor`, `Carly Mal`) and the speak-lock line `Speak the answer only.` The three texts differ. `speakers.py` is byte-for-byte unchanged.
- Phase 4 archive root: `/home/rootrecord/RootRecord-Ecosystem/Old repos deleted and merged/Solar-Pacific-RootRecord-Server/`. Keep each file's path from inside the old repo. If the archive copy fails, do not delete. Planned result: copies only; nothing removed on GitHub.
- After phase 4, add a short result note here (what landed, archive path, GitHub unchanged) and correct matrix row 57 only.

---

*Work order prepared 2026-09-29 HST. Update status when closed.*

---

## Archive / location note

This file is a draft. It is not on the active index. Do not auto-promote.

```text
Documentation/06-development/Work-Orders/drafts/Council_persona_prompts_Work_Order_WO-MIG-03-2026-09-29.md
```

See `drafts/README.md` and WO-WOGEN-001. Promotion is Alexander's decision: move into `Documentation/06-development/Work-Orders/`, set Status, and add an index row.

**Closed WOs:** set Status → COMPLETE/CLOSED → `git mv` into `Documentation/06-development/Work-Orders/Complete/`.

Human session logs archive under `Documentation/01-operations/archive/YYYY-Www/` (WO-ARCH) — separate from closed work orders.

### Phase 4 / phase 5 result

Not written. Fill this subsection after the build works and the archive copies are on disk.
