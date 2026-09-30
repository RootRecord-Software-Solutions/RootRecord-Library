# WORK ORDER — Cloud narrative reports

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-MIG-32-2026-09-29 |
| **Date** | 2026-09-29 (HST) |
| **Status** | BUILT — dry-run landed; spend off; old engine archived and removed on GitHub. Not promoted to the active index. |
| **Owner** | RootRecord |
| **Related** | Agent 32. Wave E. Optional cloud pass on the existing templates. No other function has to exist first. No later function depends on this one. |

**Scope:** Optional cloud prose for morning, midday, late, merged-morning, and Kīlauea, read from the live template reports. The templates, Kokoro, and local BLE reads stay. This draft does not build, spend, send, or schedule anything.

---

## 1. Intent

The old `report_generation.py` engine could write morning, midday, late, and Kīlauea text through a cloud model when that type's toggle was `cloud` and spend was open. NWS product bodies were stripped before a cloud package. Thin or rejected cloud text was not published. Merged morning did not call the model a second time; it reused the morning text. Kīlauea called `generate("kilauea")` and then wrote a Discord draft.

Old engine: `/home/rootrecord/old ollama/old skills/reports/sort/report-generation/scripts/report_generation.py` (`generate`, `_generate_grok`). Merged morning: `merged-morning/scripts/job.py` → `morning-report` `run_merged`. Kīlauea hook: `kilauea/rr-kilauea/scripts/kilauea.py`.

The live system already has the reports this pass must keep:

- `Media/Voice/scripts/voice_reports.py` templates `morning_report`, `midday_report`, `late_report`, and `kilauea_report`, plus Kokoro.
- `Reports/template_fill.py`, `Reports/scripts/report_board.py`, and `Reports/Late-Final`.
- EcoFlow BLE, the poller, Hawaiʻi weather, the globe collector, camera grabs, and `geology_collect.py`.

New code wins. Add an optional cloud pass that reads those template texts. Do not replace them, do not re-fetch the old `avaivy.cloud` context URLs, and do not rewrite the measured lines.

---

## 2. Current reality

Folder: `CloudNarrative`, installed under Reports. One capitalized folder, same name in all three places. No lowercase twin, no symlink, no `Logs/` on the server.

| Path | Role |
| --- | --- |
| Code | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Reports/CloudNarrative/scripts` (package `CloudNarrative`) |
| Database | `2 - RootRecord-Database/Reports/CloudNarrative/` (last file and narrative store; gitignored runtime) |
| Logs | `2 - RootRecord-Database/Logs/Reports/CloudNarrative/` |
| Secrets | `XAI_API_KEY` in `/home/rootrecord/master/master-key.env` only. That name is not in the file today. Allowlist that one name. Never print the value. No second env file. |

### 2.1 What exists

| Item | Location / status |
| --- | --- |
| Folder `CloudNarrative` | Installed. `scripts/cloud_narrative.py` dry-run. Spend stays off |
| Morning / midday / late templates | `voice_reports.py` roll-ups. Text under `RR_VOICE_REPORT_OUT` (default `test-reports/Voice/<report>_current.md`). Jobs gated `RR_VOICE_ROLLUPS=1` |
| Kīlauea template | `voice_reports.py kilauea_report`. Job gated `RR_VOICE_KILAUEA=1`. `geology_collect.py` stays the data source |
| Optional local one-line summary | `RR_VOICE_ROLLUP_LLM=1` via `run-infer.sh`. Stays. This function does not replace it |
| Old cloud engine | Archived. Removed from the local skills tree and from GitHub `main` `85add20` |
| `XAI_API_KEY` | Not in `master-key.env`. A live call cannot run until Alexander adds that name there |
| GitHub `Solar-Pacific-RootRecord-Server-Old` | `reports/sort/report-generation/` removed on `main` `85add20`. Repository kept |

### 2.2 Completed so far

- [x] Draft work order written (this file)
- [x] Alexander said to build
- [x] `CloudNarrative` code and dry-run test (no socket, template unchanged)
- [x] Phase 4 archive, then local deletion and GitHub `main` `85add20`
- [x] Phase 5 result note and the Library pages this function made stale
- [ ] `jobs.py` block. The file was already modified when build started, so it was left alone. The gated proposal stays in section 3.

### 2.3 Known friction

- `jobs.py`, the Vercel app shell, and `master-key.env` are shared. If one of them is already being edited when build starts, pause.
- `voice_reports.py` is shared by the other spoken reports. Read it. Do not edit it.
- `XAI_API_KEY` is absent. Dry-run does not need it. A live call does, and still needs a separate spend sign-off.
- Cloud spend, sends, speaker playback, OBS, and hardware switching need Alexander's sign-off. This draft does none of those.

---

## 3. Tasks

Build later, in this order. Do not start these until Alexander accepts this draft and says to build.

1. No dependency Folder is missing. Template roll-ups and `kilauea_report` already exist. Do not build Kokoro, playback, Discord, the xAI spend ledger, or geology collect.
2. Add `Reports/CloudNarrative/scripts/cloud_narrative.py`, `scripts/envload.py` (allowlist `XAI_API_KEY` only, never print values), `scripts/__init__.py`, and a short README. State file `last.json` under the Database path. Narrative markdown in that same Database folder. Logs only under the Logs path. Gitignore the runtime files (same idea as `Reports/Economy-Brief`). Do not put a `Logs/` directory on the server. Do not commit narrative text or `last.json`.
3. Kinds: `morning`, `midday`, `late`, `merged`, `kilauea`. Input is the current template markdown (measured section). `merged` copies today's morning cloud text when one exists. It does not make a second model call.
4. Default `--dry-run`: write the prompt package and `last.json` with `dry_run: true`. No HTTP. Strip NWS product bodies before a package is eligible for cloud. Scrub vendor names with the existing speech scrub. Reject thin output. Leave the template file untouched.
5. A live call is a separate manual invocation. It requires `XAI_API_KEY` in `master-key.env` and `RR_CLOUD_NARRATIVE_SPEND=1` on that process, and only after Alexander has signed off for that run. No blog, Discord, Telegram, Kokoro, or speaker.
6. `jobs.py`: one gated block only, and only if that file is idle. If it is already being edited, pause and name it. The command is `--dry-run`. The schedule never spends. Proposal, registered only when the file is idle:

```python
{
    "id": "cloud_narrative_dry_run",
    "enabled": os.environ.get("RR_CLOUD_NARRATIVE", "0") == "1",
    "description": "Optional cloud-narrative package for morning/midday/late/kilauea. Dry-run only. No spend.",
    "at_times": ["10:20"],
    "command": 'python3 "Reports/CloudNarrative/scripts/cloud_narrative.py" morning --dry-run',
}
```

`RR_CLOUD_NARRATIVE` defaults to `0`. `RR_CLOUD_NARRATIVE_SPEND` is not used by the job.

7. Proof test: `python3 cloud_narrative.py morning --dry-run` exits 0, writes `2 - RootRecord-Database/Reports/CloudNarrative/last.json` with `dry_run: true`, does not change the morning template, and does not open a socket.

---

## 4. Non-goals

- Do not replace Kokoro, `voice_reports.py`, `template_fill.py`, `report_board.py`, Late-Final, `geology_collect.py`, the EcoFlow poller, Hawaiʻi weather, the globe collector, or camera grabs.
- Do not port Ara TTS, the public draft queue, Discord or Telegram posts, the xAI spend ledger, or crawling of the old context URLs. Those belong to other agents.
- Do not import logs, samples, last-state files, generated reports, `__pycache__`, or `DAILY.md` into Pacific, Database, the website, or git. New runtime output uses the Database paths above and stays gitignored.
- Do not send messages, play speakers, switch OBS or other hardware, delete live Ecosystem files, or spend cloud money.
- Do not edit other agents' files. Do not promote this draft onto the active index.
- Do not delete a GitHub repository. Do not force-push. Do not restore `~/.ollama/skills/energy`, `automations`, or `coms/ssh/local-data-globe`.

---

## 5. Key file / path reference

| Path | Role |
|------|------|
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Reports/CloudNarrative/scripts` | Code to add at build time (package `CloudNarrative`) |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Reports/CloudNarrative/scripts/cloud_narrative.py` | Dry-run package and optional spend call |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Reports/CloudNarrative/scripts/envload.py` | Allowlist `XAI_API_KEY` only |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Reports/CloudNarrative/scripts/__init__.py` | Package init |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Reports/CloudNarrative/README.md` | Short folder note |
| `2 - RootRecord-Database/Reports/CloudNarrative/last.json` | Last run. Not committed |
| `2 - RootRecord-Database/Reports/CloudNarrative/` | Narrative markdown store. Not committed |
| `2 - RootRecord-Database/Logs/Reports/CloudNarrative/` | Logs only |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Media/Voice/scripts/voice_reports.py` | Read-only template source |
| `test-reports/Voice/morning_report_current.md` (and midday, late, kilauea) | Read-only measured text. Default `RR_VOICE_REPORT_OUT` |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Media/Voice/scripts/speech_scrub.py` | Read-only vendor scrub |
| `/home/rootrecord/master/master-key.env` | `XAI_API_KEY` only, when Alexander adds it. Never commit |
| `/home/rootrecord/old ollama/old skills/reports/sort/report-generation/` | Old source to archive in phase 4 |

Shared files to leave (name them; do not archive or delete):

- `old skills/reports/sort/morning-report/`, `midday-report/`, `late-report/` (`job.py` also queues drafts and touches playback)
- `old skills/merged-morning/scripts/job.py`
- `old skills/kilauea/rr-kilauea/scripts/kilauea.py`
- `old skills/api/ai-external-api/xai/scripts/xai.py` and `api_ledger.py`

---

## 6. Open items

**Additional requirements:**

- Cloud spend stays off until Alexander signs off for a specific run and adds `XAI_API_KEY` to `master-key.env`.
- `RR_CLOUD_NARRATIVE` stays `0`. The proposed `jobs.py` block is dry-run only.
- If `jobs.py` is already being edited at build time, pause. Do not take the file.

---

## 7. Notes & constraints

- No force-push.
- Secrets stay out of git. The plan lists the key name `XAI_API_KEY` only. Never print the value.
- Prefer small reversible steps.
- Sends, speaker playback, OBS, hardware switching, deletion of live Ecosystem files, and cloud spend require Alexander's sign-off. Do not do those things in the draft pass.
- Proof test, after a later build: `python3 cloud_narrative.py morning --dry-run` exits 0, writes `last.json` with `dry_run: true`, leaves the morning template unchanged, and opens no socket.

### Phase 4 (after the migration works, not now)

Copy this function's old files into `/home/rootrecord/RootRecord-Ecosystem/Old repos deleted and merged/<old-repo-name>/`, keeping the path they had inside the old repo. Generated data that lived beside that source goes into the archive too, and still does not go into the live Folders. Then delete those same files from the old repo on this machine and on GitHub.

- Archive only `reports/sort/report-generation/` (scripts, prompts, skill notes). Drop `__pycache__` from the live copy; it may sit in the archive and still must not enter Pacific, Database, the website, or git.
- Local tree: `/home/rootrecord/old ollama/old skills/reports/sort/report-generation/`.
- Leave the shared files named in section 5.
- GitHub: confirm the path is absent on Library, Database, Pacific, Ecosystem, and `.github`. `Solar-Pacific-RootRecord-Server-Old` was already 404 on 2026-09-30. If it is still absent, record "nothing to delete on GitHub". Do not delete a repository.
- If the archive copy fails, do not delete.
- Do not restore `~/.ollama/skills/`.

### Phase 5 (after phase 4, not now)

Add a short result note to this work order: what landed, what was archived, what was removed on GitHub, and the new status. Correct only the Library pages this function made stale:

- `Documentation/00-architecture/Voice-Reports-G3.md` (Kīlauea Grok line, and the morning/midday/late cloud clause)
- `Documentation/00-architecture/Old-Repo-Migration-Matrix.md` (Kīlauea Grok clause, row 45 cloud generation, row 50 merged-morning Grok clause)
- `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Geology/README.md` ("Grok report generation" line only)

Do not rewrite unrelated work orders.

### Result note

Landed 2026-09-30: `Reports/CloudNarrative/scripts/cloud_narrative.py`. It reads the template markdown, strips NWS product bodies, and writes a prompt package plus `last.json`. Default and `--dry-run` set `http: false`. `merged` copies today's `morning-current.md` only when `--spend` is allowed, and it never calls the model. A live call needs both `--spend` and `RR_CLOUD_NARRATIVE_SPEND=1`, plus `XAI_API_KEY`. That call was not made.

Proof: `morning --dry-run` exited 0 with `dry_run: true` and `http: false`. A socket guard saw no sockets. The morning template file was absent before and after. A fixture template with a long NWS product line stayed byte-identical, the product line was dropped from the package, and the measured battery line was kept.

`jobs.py` was already modified (hurricane radio and Bruce stats), so the gated `cloud_narrative_dry_run` block was not registered. `RR_CLOUD_NARRATIVE` stays off.

Archived to `Old repos deleted and merged/Solar-Pacific-RootRecord-Server-Old/reports/sort/report-generation/` (scripts, skill notes, migrate note; no `__pycache__`). Removed that tree from `/home/rootrecord/old ollama/old skills/reports/sort/report-generation/`. Shared files left in place: `morning-report/`, `midday-report/`, `late-report/`, `merged-morning/scripts/job.py`, `kilauea/rr-kilauea/scripts/kilauea.py`, `xai.py`, `api_ledger.py`, and the origin `report_generation.py` shim.

GitHub: `Solar-Pacific-RootRecord-Server-Old` `main` moved `55e9c84..85add20`. That commit deletes `reports/sort/report-generation/` only. The repository was not deleted. No force-push. The skills checkout ignores `reports/`, so there was no commit there.

---

*Work order prepared 2026-09-30 HST. Update status when closed.*

---

## Archive / location note

This file is a draft. Do not auto-promote it onto the active index.

**Active / accepted WOs** — filename when saved:

```text
Cloud_narrative_reports_Work_Order_WO-MIG-32-2026-09-29.md
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
