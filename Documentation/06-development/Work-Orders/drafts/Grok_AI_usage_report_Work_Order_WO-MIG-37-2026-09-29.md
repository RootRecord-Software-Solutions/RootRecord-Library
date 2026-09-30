# WORK ORDER — Grok AI-usage report

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-MIG-37-2026-09-29 |
| **Date** | 2026-09-29 (HST) |
| **Status** | OPEN — ledger landed; spend section on the local report; job gated off; old files removed from GitHub |
| **Owner** | RootRecord |
| **Related** | Agent 37. Wave E. No earlier function has to exist first. No later function depends on this one. Matrix row 84. |

**Scope:** Extend the live local AI processing report with a Grok spend ledger under Reports folder `AI-Usage`. The ledger records estimated token cost. It does not call xAI. The existing JSONL report, EcoFlow BLE, Kokoro, and template reports stay as they are. This file stays in `drafts/` and is not on the active index.

---

## 1. Intent

The old function is two pieces in GitHub repo `old` (`rootrecordsoftwaresolutions/old`). There is no local checkout of that repo on this machine.

`operations/system-tools/ai_usage.py` is a SQLite ledger. `record_usage()` stores provider, model, token counts, and an estimated USD cost from a price table. xAI rates in that table are `grok-3`, `grok-2`, and `default`. The file stores no API keys. `operations/system-tools/ai_usage_report.py` writes a 30-day `last-summary.json` from that ledger.

`operations/api-ai-tasks/ecosystem_report.py` is the spend path. It reads `ECOSYSTEM_REPORT_API` and POSTs to `https://api.x.ai/v1/chat/completions` or `https://grok-api.com/v1/chat/completions`, then asks Grok to write an energy narrative, a spoken script, and YouTube chapters from `avaivy.cloud`. That script is not the report this work order keeps.

The live system already has `Reports/ai_processing_report.py`. It reads inference JSONL (route, model, latency, memory) and writes a metadata report. Prompt text is never stored. Hourly job `ai_processing_report_hourly` stays gated off unless `RR_AI_REPORT=1`. That local report must be kept. The Grok spend path is what is absent.

How to add it: extend the local report with a Grok spend section read from the new ledger. Do not replace `ai_processing_report.py` with the Grok script.

---

## 2. Current reality

Folder name in all three places: **AI-Usage**. It sits inside the existing Reports domain. No lowercase twin, no symlink, no second top-level domain, and no `Logs/` directory on the server.

| Place | Path |
| --- | --- |
| Server code | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Reports/AI-Usage/scripts` |
| Database data | `2 - RootRecord-Database/Reports/AI-Usage` |
| Database logs | `2 - RootRecord-Database/Logs/Reports/AI-Usage` |

`master-key.env` key names for a later signed-off caller only: `ECOSYSTEM_REPORT_API`, `ECOSYSTEM_REPORT_API_BASE`, `ECOSYSTEM_REPORT_MODEL`. The ledger and the default report do not read them. Do not print values. Do not add a second env file. Do not edit `master-key.env`. A name-only check of that file was not done.

### 2.1 What exists

| Item | Location / status |
| --- | --- |
| Local AI report | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Reports/ai_processing_report.py`. Stdlib. Reads `Logs/AI/Inference/inference_current.jsonl`. Default output `RR_AI_REPORT_OUT`, else `test-reports/AI-Processing/ai-processing-report_current.md`. Enhance this file. Do not replace it. |
| Hourly job | `jobs.py` id `ai_processing_report_hourly`. Enabled only when `RR_AI_REPORT=1` at poller start. Leave that gate off. |
| Inference log | `2 - RootRecord-Database/Logs/AI/Inference/`. Metadata only. Leave it. |
| Library page | `5 - RootRecord-Library/Documentation/00-architecture/AI-Processing-Logs-and-Reports.md`. Describes the JSONL report. Phase 5 corrects section 3 only, after the spend section exists. |
| Matrix | Row 84 is **partial**. Grok key path is a secret. Cloud spend is not ported. |
| Old ledger | Archived at `Old repos deleted and merged/old/operations/system-tools/ai_usage.py` and `ai_usage_report.py`. Removed from GitHub repo `old` (`aea8b73`). |
| Old Grok caller | Archived at `Old repos deleted and merged/old/operations/api-ai-tasks/ecosystem_report.py`. Removed from GitHub (`aea8b73`). Not copied into Pacific. |
| Secrets loader pattern | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Energy/lib/envload.py`. Allowlist, never print values. Do not edit that file. |

### 2.2 Completed so far

- [x] Draft work order written (this file).
- [x] Alexander said to keep working. Build started 2026-09-30 HST.
- [x] Ledger, summary writer, pricing file, allowlist loader, and Grok spend section on the local report.
- [x] Gated `jobs.py` block `ai_usage_report` / `RR_AI_USAGE=1`, default off. `RR_AI_REPORT` left off.
- [x] Fixture proof test, no network. `grok-3`, 1,000,000 input tokens, 0 output: Estimated USD 3.00. Empty summary: `no ledger rows`. Temp trees deleted.
- [x] Phase 4 archive is on disk. The three files are removed from repo `old` on GitHub (`cursor/radio-idle-obs-gates`, `aea8b73`). No force-push. The repository was not deleted.
- [x] Phase 5 result note below. Matrix row 84 stays partial. Section 3 of `AI-Processing-Logs-and-Reports.md` names the spend section.

### 2.3 Known friction

- No dependency Folder is missing. Nothing else in this wave has to exist before the build.
- `jobs.py` and `master-key.env` are shared. If either is already being edited, pause. Do not edit `master-key.env` in any case.
- `operations/system-tools/` in repo `old` is shared with other functions. Phase 4 removes only `ai_usage.py` and `ai_usage_report.py` from that directory.
- Repo `old` may have no local checkout. Phase 4 archives from GitHub first, then deletes only these files. If the archive copy fails, do not delete.
- The price table is an estimate from the old file. It is not an xAI invoice.
- `ai_processing_report.py` comment says the report lands in `Logs/AI/Reports/`. The code default is `test-reports/AI-Processing/`. Leave that output path as it is.

---

## 3. Tasks

Do not start these until Alexander accepts this draft and says to build.

1. No dependency Folder is missing. Do not pause for another function.
2. Add `Reports/AI-Usage/scripts/ai_usage.py`. Port the ledger. Paths resolve under `RR_DATABASE_ROOT`, defaulting to Database `Reports/AI-Usage/` (`ai_usage.db`). Keep the xAI price table. Stdlib only. No network.
3. Add `Reports/AI-Usage/scripts/ai_usage_report.py`. Write `2 - RootRecord-Database/Reports/AI-Usage/last-summary.json` for the last 30 days. Runtime output stays out of git.
4. Add `Reports/AI-Usage/config/pricing.json`. The old rate table as source. No secrets.
5. Add `Reports/AI-Usage/lib/envload.py` on the Energy pattern. Allowlist is `ECOSYSTEM_REPORT_API`, `ECOSYSTEM_REPORT_API_BASE`, `ECOSYSTEM_REPORT_MODEL` only. Load `/home/rootrecord/master/master-key.env` only. Never print values. The ledger and the default report do not call this loader.
6. Extend `Reports/ai_processing_report.py` with one Grok spend section read from `last-summary.json`: xAI calls, tokens, estimated USD, and the line `no ledger rows` when the summary is missing or has no xAI rows. Leave the existing JSONL sections and `RR_AI_REPORT_OUT` unchanged.
7. Logs for this function, if any, go only under `2 - RootRecord-Database/Logs/Reports/AI-Usage/`. Do not put a `Logs/` directory on the server. Do not import an old `ai_usage.db`, samples, or last-summary files.
8. If `jobs.py` is not already being edited, add one gated block only: id `ai_usage_report`, enabled only when `RR_AI_USAGE=1`, command runs `ai_usage_report.py` with `nice -n 10`, default off. Do not turn on `ai_processing_report_hourly`. Do not restart the poller. If `jobs.py` is already being edited, pause.
9. Do not add an HTTP client. Do not copy `ecosystem_report.py`. A POST to xAI or grok-api.com needs a separate sign-off.
10. Proof test, temp tree only. Record one fixture xAI row (`grok-3`, known token counts) into a temp `RR_DATABASE_ROOT`, write the summary, then run `ai_processing_report.py` with `RR_DATABASE_ROOT` and `RR_AI_REPORT_OUT` pointed at that temp tree. Pass means the markdown still has the local JSONL sections and a Grok spend line whose USD matches the fixture rate (`grok-3`: input $3.00 and output $15.00 per 1M tokens). No network. No `master-key.env`.
11. After that test passes, copy the three old files listed in section 5 into `/home/rootrecord/RootRecord-Ecosystem/Old repos deleted and merged/old/`, keeping each path from inside repo `old`. Generated data that lived beside that source goes into this archive too, and still does not go into the live Folders. If the archive copy fails, stop and do not delete.
12. After the archive copy is on disk, delete those same three files from repo `old` on this machine and on GitHub. Commit that deletion and push it. Do not force-push. Do not delete the GitHub repository.
13. Update this work order with what landed, the archive path, the GitHub deletion, and the new status. Correct only matrix row 84 and section 3 of `AI-Processing-Logs-and-Reports.md`.

---

## 4. Non-goals

- Do not overwrite `Reports/ai_processing_report.py` with `ecosystem_report.py`, and do not replace its JSONL sections.
- Do not call xAI, grok-api.com, or avaivy.cloud. Do not send messages, play speaker audio, drive OBS, switch hardware, delete live Ecosystem files, or spend cloud money.
- Do not replace EcoFlow BLE, the poller, Hawaiʻi weather, the globe collector, camera grabs, Kokoro, template reports, or `geology_collect.py`.
- Do not build any other agent's function.
- Do not edit `Energy/lib/envload.py`, `run-infer.sh`, `ai-log-rotate.sh`, or `master-key.env`.
- Do not import logs, samples, last-state files, generated reports, images, radar frames, zip archives, database dumps, caches, virtualenvs, `node_modules`, or `__pycache__` into Pacific, Database, the website, or git.
- Do not restore files under `~/.ollama/skills/energy`, automations, or `coms/ssh/local-data-globe`.
- Do not open a second top-level domain, a second env file, a website page, or a `Logs/` directory on the server.
- Shared leftovers in repo `old` `operations/system-tools/` stay: `AGENTS.md`, `GITHUB-AUTO-PUSH.txt`, `database-root-migrate.py`, `desk-backup-20260823-193454.tar.gz`, `desk/`, `directory-printer/`, `directory-sync/`, `github-auto-push.py`, `new 1.txt`, `screenshot.sh.disabled`, `sync-ava-directory.sh`. Name them here and leave them.

---

## 5. Key file / path reference

| Path | Role |
|------|------|
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Reports/AI-Usage/scripts` | Server code. New at build. |
| `2 - RootRecord-Database/Reports/AI-Usage` | Database data. Ledger sqlite and `last-summary.json`. Runtime. Out of git. |
| `2 - RootRecord-Database/Logs/Reports/AI-Usage` | Database logs. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Reports/AI-Usage/scripts/ai_usage.py` | New ledger. Add at build. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Reports/AI-Usage/scripts/ai_usage_report.py` | New summary writer. Add at build. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Reports/AI-Usage/config/pricing.json` | Source rate table. No secrets. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Reports/AI-Usage/lib/envload.py` | Allowlist loader. Not used by the default report. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Reports/ai_processing_report.py` | Existing local report. Extend with one Grok spend section. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Energy/lib/envload.py` | Pattern for the allowlist loader. Do not edit. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Automations/scripts/jobs.py` | Shared. Proposed gated block `ai_usage_report` / `RR_AI_USAGE=1` only, and only if this file is not already being edited. |
| `/home/rootrecord/master/master-key.env` | Shared secrets file. Do not edit. Allowlist names: `ECOSYSTEM_REPORT_API`, `ECOSYSTEM_REPORT_API_BASE`, `ECOSYSTEM_REPORT_MODEL`. |
| `operations/system-tools/ai_usage.py` | Old source. Phase 4 archive, then remove from repo `old`. |
| `operations/system-tools/ai_usage_report.py` | Old source. Phase 4 archive, then remove from repo `old`. |
| `operations/api-ai-tasks/ecosystem_report.py` | Old spend script. Phase 4 archive, then remove from repo `old`. Not copied into Pacific. |
| `5 - RootRecord-Library/Documentation/00-architecture/Old-Repo-Migration-Matrix.md` | Phase 5: correct row 84 only. |
| `5 - RootRecord-Library/Documentation/00-architecture/AI-Processing-Logs-and-Reports.md` | Phase 5: correct section 3 only, after the spend section exists. |

---

## 6. Open items

**Additional requirements:**

- Sign-off before any Grok POST, send, speaker playback, OBS, hardware switch, live Ecosystem deletion, or cloud spend. This build does none of those.
- Phase 4 is already ordered: archive the three old files, then remove them from repo `old` locally and on GitHub. No force-push. Do not delete the repository.
- Result note is in the section below. This file stays in `drafts/`. It is not on the active index.
- `operations/system-tools/` files listed in section 4 are shared. Leave them.

---

## 7. Notes & constraints

- No force-push.
- Secrets stay out of git. Never print key values.
- Prefer small reversible steps.
- New periodic jobs stay gated off. `RR_AI_USAGE` defaults to off. Do not enable `RR_AI_REPORT`.
- Cloud spend stays behind Alexander's sign-off. The proof test uses one fixture row in a temp database.
- Fixture rate check: `grok-3` input $3.00 per 1M tokens, output $15.00 per 1M tokens. Example: 1,000,000 input and 0 output estimates $3.00.
- Do not promote this file onto the active index.

---

*Work order prepared 2026-09-30 HST. Update status when closed.*

---

## Result (2026-09-30 HST)

Landed: `Reports/AI-Usage/scripts/ai_usage.py`, `ai_usage_report.py`, `config/pricing.json`, `lib/envload.py`, and a Grok spend section on `Reports/ai_processing_report.py`. `jobs.py` id `ai_usage_report` is off unless `RR_AI_USAGE=1`. No HTTP client. No call to xAI.

Archive: `/home/rootrecord/RootRecord-Ecosystem/Old repos deleted and merged/old/operations/system-tools/ai_usage.py`, `ai_usage_report.py`, and `operations/api-ai-tasks/ecosystem_report.py`.

GitHub: those three paths removed from `rootrecordsoftwaresolutions/old` branch `cursor/radio-idle-obs-gates`, commit `aea8b73`. Shared files in `operations/system-tools/` were left. The repository was not deleted.

Proof: temp database only. Fixture `grok-3` at 1,000,000 input tokens and 0 output wrote `Estimated USD: 3.00` and kept the JSONL sections. A second run with no summary wrote `no ledger rows`.

---

## Archive / location note

**Active / accepted WOs** — filename when saved:

```text
Grok_AI_usage_report_Work_Order_WO-MIG-37-2026-09-29.md
```

Location when accepted:

```text
Documentation/06-development/Work-Orders/
```

**Drafts (not on active index)** — this file stays here until Alexander accepts it:

```text
Documentation/06-development/Work-Orders/drafts/
```

See `drafts/README.md` and WO-WOGEN-001. Do not auto-promote.

**Closed WOs:** set Status → COMPLETE/CLOSED → `git mv` into:

```text
Documentation/06-development/Work-Orders/Complete/
```

Human session logs archive under `Documentation/01-operations/archive/YYYY-Www/` (WO-ARCH) — separate from closed work orders.
