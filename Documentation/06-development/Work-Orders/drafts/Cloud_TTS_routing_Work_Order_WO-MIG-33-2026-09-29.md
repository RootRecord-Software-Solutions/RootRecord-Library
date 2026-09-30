# WORK ORDER — Cloud TTS routing

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-MIG-33-2026-09-29 |
| **Date** | 2026-09-30 (HST) |
| **Status** | BUILT — gated dry-run pass; live xAI call still needs sign-off |
| **Owner** | RootRecord |
| **Related** | Agent 33. Depends on agent 15 Report playback (`Media/Playback`), which is already installed. Kokoro stays in `Media/Voice`. |

**Scope:** Add one gated router that can record a cloud Ara voice request beside Kokoro. In scope after this draft is accepted: `Media/CloudTTS`, its Database state and logs, a dry-run proof that does not call xAI, and a note that no exclusive old file was archived. Out of scope: a live xAI call, speaker playback, editing `jobs.py`, replacing Kokoro, and deleting shared old files (`synth.py`, `xai.py`, Kokoro scripts).

This file stays in `Work-Orders/drafts/`. Do not add it to the active work-order index.

---

## 1. Intent

The old synth desk is labeled Ara / Grok / Cursor TTS routing. The script at `old ollama/old skills/synth/scripts/synth.py` routes text: Grok chat, then local Ollama, then a factual stub, with Cursor as a text queue. Cloud speech is a separate call, `xai.tts` to `https://api.x.ai/v1/tts`, voice id `ara`, metered as `grok-voice-tts`. Kokoro is the live voice. Its generator maps the names `ara` and `cloud` onto local `af_heart` and does not call xAI.

This function adds an optional cloud route beside that local voice. It does not replace Kokoro, the template reports, or the EcoFlow BLE reads.

---

## 2. Current reality

Folder name: **CloudTTS**, a subfolder of the existing Media domain. Package name: `CloudTTS`. No second top-level domain, no lowercase twin, no symlink.

| Path | Role |
| --- | --- |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Media/CloudTTS/scripts` | Server code |
| `2 - RootRecord-Database/Media/CloudTTS` | Database data (last-route state only) |
| `2 - RootRecord-Database/Logs/Media/CloudTTS` | Database logs |

No `config/` directory. No `Logs/` directory on the server. No website page.

`master-key.env` allowlist, names only: `XAI_API_KEY`. Loaded the same way as Energy `lib/envload.py`. Values are never printed. `RR_CLOUD_TTS` is a gate flag, not a secret. `TTS_VOICE` is not on this allowlist. The cloud voice id on the signed-off path is the constant `ara`.

### 2.1 What exists

| Item | Location / status |
| --- | --- |
| CloudTTS folder | Installed. `Media/CloudTTS/scripts/route.py` |
| Kokoro renderer, personas, clip catalog | Pacific `Media/Voice/scripts/` — live. Do not replace |
| Report playback | Pacific `Media/Playback/` — present. If it is missing when the build starts, pause and name Report playback. Do not rebuild it |
| Old text router | `/home/rootrecord/old ollama/old skills/synth/scripts/synth.py` — shared with cloud narrative routing. Leave it |
| Old xAI client | `/home/rootrecord/old ollama/old skills/api/ai-external-api/xai/scripts/xai.py` — shared with the API client function. Leave it |
| Kokoro scripts | Already ported to `Media/Voice`. Leave the old skill scripts |
| `jobs.py` | Do not edit. No CloudTTS job is proposed |

### 2.2 Completed so far

- [x] Draft written (this file)
- [x] Alexander said to build
- [x] `CloudTTS` router landed
- [x] Gated proof recorded (no HTTP, no speaker)
- [x] Phase 4 recorded: no exclusive old file to archive or delete
- [x] Result note and the Library corrections

### 2.3 Known friction

- A live xAI call spends money. The build proof must not set `RR_CLOUD_TTS` and must not pass `--speak` together with that flag.
- Cursor in the old synth script enqueues text. This router does not send audio to Cursor.
- `jobs.py` is already dirty in the working tree from other work. This function does not touch it.

---

## 3. Tasks

Do these only after Alexander accepts this draft and says to build. Until then, do not edit runtime files, restart services, send messages, actuate hardware, or spend cloud money.

1. Confirm `Media/Playback` is still on disk. It is present, so do not pause. If it is gone when the build starts, pause and name Report playback. Do not rebuild it.
2. Add `Media/CloudTTS` (`__init__.py`, `__main__.py`, `scripts/route.py`, `scripts/envload.py`, `README.md`). Do not edit `jobs.py`. Do not register a periodic job.
3. Default engine is `kokoro`. Write a route record and do not render, do not HTTP, and do not call `Media/Voice`.
4. `--engine ara` without both `RR_CLOUD_TTS=1` and `--speak` writes `called: false` and `detail: gated`. No request leaves the machine.
5. `--engine cursor` writes `cursor_is_text_queue` and does not call an API. Any other engine is `refused`.
6. The live Ara path, when both gates are on, loads only `XAI_API_KEY`, posts to `https://api.x.ai/v1/tts` with voice id `ara`, and writes `ara-last.mp3` under the Database CloudTTS folder. Cap the spoken text at 2000 characters. Do not run this path in the build proof.
7. Do not call `aplay` and do not call `Media/Playback/scripts/play.py`. Speaker playback stays a separate sign-off.
8. Logs go only to `2 - RootRecord-Database/Logs/Media/CloudTTS`. Runtime output stays out of Pacific, the website, and git. Ignore those Database paths.
9. Prove the gate (section 7). A live xAI call is a separate sign-off. Do not do it in this build.
10. Phase 4: no file belongs only to this function. Leave `synth/scripts/synth.py`, `xai/scripts/xai.py`, and the Kokoro scripts. Do not archive them, do not delete them, and do not push.
11. Phase 5: add the result note to this work order (section 8). Correct only the Library lines this function makes stale: matrix row 54, the Grok voice bullet in Voice-Reports-G3, and the synth row in the 2026-09-28 top-level catalog.

---

## 4. Non-goals

- Do not overwrite `Media/Voice` (`voice_generate.py`, `speakers.py`, `voice_reports.py`, `clip_catalog.py`, Kokoro model, or the venv).
- Do not edit `Media/Playback` or call the speaker.
- Do not edit `jobs.py`.
- Do not build cloud narrative reports, the xAI chat client, API price ledger, or Cursor text fallback.
- Leave these shared old files: `synth/scripts/synth.py`, `api/ai-external-api/xai/scripts/xai.py`, `kokoro/scripts/`.
- Do not restore files under `~/.ollama/skills/energy`, automations, or `coms/ssh/local-data-globe`.
- Do not send, play speakers, switch hardware, delete live Ecosystem files, or spend cloud money. Phase 4 deletes nothing, because nothing here is exclusive.
- Do not promote this draft onto the active work-order index.

---

## 5. Key file / path reference

| Path | Role |
|------|------|
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Media/CloudTTS/scripts/route.py` | Router |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Media/CloudTTS/scripts/envload.py` | Allowlist loader for `XAI_API_KEY` |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Media/CloudTTS/README.md` | Folder note: paths, gate, no cron |
| `2 - RootRecord-Database/Media/CloudTTS/last-route.json` | Runtime state. Not source |
| `2 - RootRecord-Database/Logs/Media/CloudTTS/` | Router log. Runtime |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Media/Voice/` | Existing Kokoro. Do not edit |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Media/Playback/` | Dependency. Present. Do not edit |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Automations/scripts/jobs.py` | Do not edit |
| `/home/rootrecord/master/master-key.env` | Allowlist name `XAI_API_KEY` only. Never commit values |
| `/home/rootrecord/old ollama/old skills/synth/scripts/synth.py` | Shared text router. Leave it |
| `/home/rootrecord/old ollama/old skills/api/ai-external-api/xai/scripts/xai.py` | Shared API client. Leave it |
| `5 - RootRecord-Library/Documentation/00-architecture/Old-Repo-Migration-Matrix.md` | Phase 5. Row 54 only |
| `5 - RootRecord-Library/Documentation/00-architecture/Voice-Reports-G3.md` | Phase 5. Grok voice bullet only |
| `5 - RootRecord-Library/Documentation/00-architecture/Solar-Pacific-Old-Full-TopLevel-Catalog-2026-09-28.md` | Phase 5. synth row only |

---

## 6. Open items

**Additional requirements:**

- A live xAI call stays gated. It needs `RR_CLOUD_TTS=1` and `--speak`, and a separate sign-off. The build test does not make that call.
- This file stays in drafts. It is not on the active index.

---

## 7. Notes & constraints

- No force-push.
- Secrets stay out of git. The allowlist is the name `XAI_API_KEY` only. Never print the value.
- Prefer small reversible steps.
- Sends, speaker playback, OBS, hardware switching, deletion of live Ecosystem files, and cloud spend need Alexander's sign-off. Do not do those things while executing the build. Phase 4 has no exclusive files, so it deletes nothing.
- New periodic jobs stay off. Do not edit `jobs.py`.
- EcoFlow BLE, the poller, Hawaiʻi weather, the globe collector, camera grabs, Kokoro, and `geology_collect.py` stay as they are.

**Sign-off gate.** `--engine ara` without both `RR_CLOUD_TTS=1` and `--speak` returns `gated` and does not open a socket. `--speak` without the flag returns exit 2. The flag without `--speak` still stays gated.

**Small test (no cloud spend, speakers stay off).** From the Media directory, with `RR_CLOUD_TTS` unset:

```text
python3 -m CloudTTS --engine ara
python3 -m CloudTTS --engine ara --speak
python3 -m CloudTTS --engine kokoro
```

The first prints `called: false` and `detail: gated`. The second does the same with exit 2. The third prints `detail: kokoro_local` and does not render a WAV. A live xAI call is not part of this test.

---

## 8. Result note

Landed 2026-09-30 ~01:07 HST.

- Router: `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Media/CloudTTS/scripts/route.py`. `jobs.py` was not edited. Kokoro in `Media/Voice` was not edited. `Media/Playback` was present and was not called.
- Proof, no cloud spend, speakers off, `RR_CLOUD_TTS` unset: `--engine ara` returned `called: false`, `detail: gated` (exit 0). `--engine ara --speak` returned the same with exit 2. `--engine kokoro` returned `kokoro_local` (exit 0) and did not render a WAV. `--engine cursor` returned `cursor_is_text_queue`. `--engine grok` returned `refused` (exit 1). `RR_CLOUD_TTS=1` without `--speak` stayed `gated`. No `ara-last.mp3`. An in-process tripwire on `urlopen` was not hit.
- Runtime state is `2 - RootRecord-Database/Media/CloudTTS/last-route.json`. The log is `2 - RootRecord-Database/Logs/Media/CloudTTS/route.log`. Both paths are gitignored.
- Archive: none. No file belongs only to this function. Left in place: `/home/rootrecord/old ollama/old skills/synth/scripts/synth.py`, `/home/rootrecord/old ollama/old skills/api/ai-external-api/xai/scripts/xai.py`, and the Kokoro scripts. Nothing was deleted from the old repo or from GitHub. No push.
- Library corrections: matrix row 54, the Grok voice bullet in `Voice-Reports-G3.md`, and the synth row in the 2026-09-28 top-level catalog.

This file stays in `Work-Orders/drafts/`. It is not on the active index. A live xAI call still needs a separate sign-off.

---

*Work order prepared 2026-09-30 HST. Update status when closed.*

---

## Archive / location note

**Active / accepted WOs** — filename when saved:

```text
Cloud_TTS_routing_Work_Order_WO-MIG-33-2026-09-29.md
```

Location after promotion (not now):

```text
Documentation/06-development/Work-Orders/
```

**Drafts (not on active index)** — this file:

```text
Documentation/06-development/Work-Orders/drafts/Cloud_TTS_routing_Work_Order_WO-MIG-33-2026-09-29.md
```

See `drafts/README.md` and WO-WOGEN-001. Do not auto-promote.

**Closed WOs:** set Status → COMPLETE/CLOSED → `git mv` into:

```text
Documentation/06-development/Work-Orders/Complete/
```

Human session logs archive under `Documentation/01-operations/archive/YYYY-Www/` (WO-ARCH) — separate from closed work orders.
