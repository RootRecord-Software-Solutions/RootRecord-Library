# WORK ORDER — API prices and external AI fallback

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-MIG-35-2026-09-29 |
| **Date** | 2026-09-30 (HST) |
| **Status** | BUILT — spend off, jobs enabled False. Not on the active index. |
| **Owner** | RootRecord |
| **Related** | [Old-Repo-Migration-Matrix.md](../../../00-architecture/Old-Repo-Migration-Matrix.md) row 72; [Solar-Pacific-Old-Full-TopLevel-Catalog-2026-09-28.md](../../../00-architecture/Solar-Pacific-Old-Full-TopLevel-Catalog-2026-09-28.md) `api`; [G1-Scheduler-To-G3-Jobs-Map-2026-09-29.md](../../../00-architecture/G1-Scheduler-To-G3-Jobs-Map-2026-09-29.md) `api-prices` / `cursor-fallback` |

**Scope:** One function: a local public-price catalog and a fail-closed xAI / Cursor client under System `ApiPrices`. In scope after acceptance: source, an offline seed test, two disabled job blocks if `jobs.py` is free, then archive and delete only the old `api/` tree. Out of scope: BLE reads, Kokoro, template reports, model-pick, other vendors' clients, enabled jobs, secret values, sends, playback, and any cloud call before sign-off.

---

## 1. Intent

The old function kept a public price catalog (Cursor, xAI, OpenAI, Gemini, Anthropic) and a fail-closed external client. Daily work was an HTTP GET of vendor docs. It did not spend tokens unless the operator turned spend on. xAI chat and TTS refused when spend was off and opened a circuit on credit or auth errors. Cursor fallback ran at most one ask-mode job, capped at 2 per day and 6 hours apart. The old Cursor drain also wrote report drafts. That write is not ported.

The live system already has EcoFlow BLE reads, Kokoro voice, and template reports. Those stay. This function does not replace them. Cloud chat, TTS, the xAI prepaid balance probe, and `cursor agent` stay off until Alexander signs off spend.

No newer copy of this function is installed on Pacific. Matrix row 72 is **missing**. New code, when the build is accepted, is a client that reads key names from `master-key.env` and never stores secret values in the repo.

---

## 2. Current reality

### 2.1 What exists

| Item | Location / status |
| --- | --- |
| Folder | `ApiPrices` (package `ApiPrices`), subfolder of System. Not created yet. |
| Server code | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/System/ApiPrices/scripts` — absent |
| Database data | `2 - RootRecord-Database/System/ApiPrices/` — absent |
| Database logs | `2 - RootRecord-Database/Logs/System/ApiPrices/` — absent |
| Key names (allowlist only) | `XAI_API_KEY`, `XAI_MGMT_KEY`, `XAI_TEAM_ID`, `CURSOR_API_KEY`. Read like `Energy/lib/envload.py`: one allowlist, never print values, no second env file. |
| `master-key.env` | `/home/rootrecord/master/master-key.env`. Those four names are absent. This draft does not edit that file. |
| Gates | `RR_API_PRICES` and `RR_API_SPEND` stay unset. `spend_master` stays false. |
| Old source | Tracked tree `api/` in `/home/rootrecord/old ollama/old skills`. Remote `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server`, branch `online-safe-20260920`. Not under `~/.ollama/skills`. |
| Price catalog | `api/api-prices/scripts/api_ledger.py`, `api/api-prices/scripts/job.py`, `api/api-prices/api-prices-boot/scripts/job.py`. Public docs GET. Spend master defaults off. SQLite plus `api-ledger.json`. |
| xAI client | `api/ai-external-api/xai/scripts/xai.py`. Chat and TTS. TTS is not Kokoro. |
| Cursor fallback | `api/ai-external-api/cursor/scripts/cursor_fallback.py`, `api/ai-external-api/cursor/scripts/job.py`. Old drain wrote report drafts. That write is not ported. |
| Scheduler | `api-prices` 10:25 HST and `cursor-fallback` 10:22 and 16:22 HST. Both blocked. Not in the live poller as enabled jobs. |

### 2.2 Completed so far

- [x] Old `api/` tree read. Pacific has no `ApiPrices` package.
- [x] Key names checked. `XAI_*` and `CURSOR_API_KEY` are not in `master-key.env`. Values were not printed.
- [x] Draft accepted. Alexander said to build (2026-09-30).
- [x] Package `System/ApiPrices/scripts` created. Live Database and Logs directories were not created.
- [x] Offline seed test on `/tmp/rr-mig-35`.
- [x] Disabled job blocks in `jobs.py`: `api_prices` and `cursor_fallback`, both `"enabled": False`.
- [x] Archive copy, then deletion of `api/` from both old repos locally and on GitHub.
- [x] Result note and the Library lines this function made stale.

### 2.3 Known friction

- Old modules import `apps.core` and `model_pick`. Those are other functions. The new client does not import them. Omitted model defaults: `grok-4.6` for xAI, `composer-2.5` for Cursor. Model-pick stays unbuilt.
- `jobs.py` and `master-key.env` are shared. If either is already being edited at build time, pause and name that file. Do not wait on it by editing it.
- The price catalog mentions OpenAI, Gemini, and Anthropic prices from public docs. Their inference clients are not this function.
- Operator seed notes in the old ledger (Cursor used percent, xAI prepaid dollars, dated 2026-09-03) are not live meters and are not secrets. They may ship as seed constants. Runtime JSON and SQLite stay under the Database path and out of git.
- GitHub name in the migration matrix is `Solar-Pacific-RootRecord-Server-Old`. The checkout that still tracks `api/` is `Solar-Pacific-RootRecord-Server` on `online-safe-20260920`. Phase 4 checks both and deletes only the `api/` path where it still exists.

---

## 3. Tasks

Build only after Alexander accepts this draft and says to build. Until then, do not edit runtime files, restart services, send messages, actuate hardware, or spend cloud money.

1. If `jobs.py` or `master-key.env` is already being edited, pause and name that file. Do not build another agent's function. Model-pick is not a blocker: this client does not call it.
2. Add package `ApiPrices` under `1 - Servers/1 - RootRecord-Pacific-Solar-Server/System/ApiPrices/scripts`: `envload.py`, `api_ledger.py`, `xai.py`, `cursor_fallback.py`, `job.py`. Paths point at `2 - RootRecord-Database/System/ApiPrices/` and `2 - RootRecord-Database/Logs/System/ApiPrices/`. No `config/` directory. No `Logs/` directory on the server. No `apps.core` import.
3. Ledger: embedded seed table, SQLite under the Database path, `may_spend` false unless `spend_master` and that vendor's flag are on. Public-doc GET and the xAI billing probe run only when `RR_API_PRICES=1`. Chat, TTS, and `cursor agent` run only when `RR_API_SPEND=1`. Cursor text is stored under the Database path. It does not call report draft or playback code.
4. Propose two blocks in `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Automations/scripts/jobs.py`, both `"enabled": False`: `api_prices` (10:25 HST, public GET only) and `cursor_fallback` (10:22 and 16:22 HST). If `jobs.py` is busy, skip that edit and record the skip here.
5. Do not write secrets. Do not restart services, send, play audio, or call xAI, Cursor, or the billing API during the build.
6. Small test on a temp root. No live Database write and no network. Seed the catalog, assert `may_spend("xai")` and `may_spend("cursor")` are false, and assert the HTTP and spend entry points were not called.
7. After that works: copy `api/` into `/home/rootrecord/RootRecord-Ecosystem/Old repos deleted and merged/Solar-Pacific-RootRecord-Server/api/`, keeping the path it had inside the old repo, including `__pycache__` that sits beside that source. Generated data stays in the archive and out of Pacific, Database, the website, and git. If the archive copy fails, stop and do not delete. Then delete only `api/` from `/home/rootrecord/old ollama/old skills` and from GitHub `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server` branch `online-safe-20260920`. Commit that deletion and push it. No force-push. Do not delete the repository. If `Solar-Pacific-RootRecord-Server-Old` still contains `api/`, delete only that path there too. Leave every file outside `api/`. Do not restore `~/.ollama/skills`.
8. Update this same work order with what landed, the archive path, the GitHub deletion, and the new status. Correct only the Library lines this function makes stale: matrix row 72 and the matching clause in blocker 6, the `api` catalog row, and the `api-prices` / `cursor-fallback` rows in the G1 scheduler map.

---

## 4. Non-goals

- EcoFlow BLE, the poller, Hawaiʻi weather, the globe collector, camera grabs, Kokoro, and `geology_collect.py`.
- Template reports, the public draft queue, speaker playback, OBS, and hardware switching.
- Model-pick, Grok ecosystem report generation, AdMob/AdSense, Stripe, and OpenAI / Gemini / Anthropic inference clients.
- Other agents' files, and any old-repo file outside `api/`.
- A second env file, printed secret values, an enabled periodic job, a website page, and an Android import.
- Deleting either GitHub repository, force-push, or restoring files under `~/.ollama/skills`.

---

## 5. Key file / path reference

| Path | Role |
|------|------|
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/System/ApiPrices/scripts` | Server code. Package `ApiPrices`. Create on build. |
| `2 - RootRecord-Database/System/ApiPrices/` | Samples, last files, SQLite, ledger JSON, Cursor fallback text. |
| `2 - RootRecord-Database/Logs/System/ApiPrices/` | Logs only. |
| `/home/rootrecord/master/master-key.env` | Only secret file. Allowlist names: `XAI_API_KEY`, `XAI_MGMT_KEY`, `XAI_TEAM_ID`, `CURSOR_API_KEY`. Do not edit in this draft. Do not commit. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Energy/lib/envload.py` | Pattern for the allowlist loader. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Automations/scripts/jobs.py` | Shared. Two `"enabled": False` blocks only if the file is free. |
| `/home/rootrecord/old ollama/old skills/api/api-prices/scripts/api_ledger.py` | Old price catalog. Read until phase 4. |
| `/home/rootrecord/old ollama/old skills/api/api-prices/scripts/job.py` | Old daily price job. |
| `/home/rootrecord/old ollama/old skills/api/api-prices/api-prices-boot/scripts/job.py` | Old boot refresh. |
| `/home/rootrecord/old ollama/old skills/api/ai-external-api/xai/scripts/xai.py` | Old xAI chat and TTS. |
| `/home/rootrecord/old ollama/old skills/api/ai-external-api/cursor/scripts/cursor_fallback.py` | Old Cursor queue and ask. |
| `/home/rootrecord/old ollama/old skills/api/ai-external-api/cursor/scripts/job.py` | Old Cursor drain. Report-draft write is not ported. |
| `api/api-prices/` and `api/ai-external-api/` SKILL, INDEX, DAILY, and `references/migrate.md` | Old notes. Archive with the tree. Do not treat as live runtime. |
| `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/api/` | Phase 4 archive path. Not written by this draft. |
| `5 - RootRecord-Library/Documentation/00-architecture/Old-Repo-Migration-Matrix.md` | Row 72 and blocker 6. Correct only after phase 4. |
| `5 - RootRecord-Library/Documentation/00-architecture/Solar-Pacific-Old-Full-TopLevel-Catalog-2026-09-28.md` | `api` row. Correct only after phase 4. |
| `5 - RootRecord-Library/Documentation/00-architecture/G1-Scheduler-To-G3-Jobs-Map-2026-09-29.md` | `api-prices` and `cursor-fallback` rows. Correct only after phase 4. |

New files after acceptance, not before: `envload.py`, `api_ledger.py`, `xai.py`, `cursor_fallback.py`, and `job.py` under `System/ApiPrices/scripts`.

---

## 6. Open items

**Additional requirements:**

- Alexander accepts this draft and says to build before any runtime file changes.
- Alexander signs off before any xAI chat, xAI TTS, xAI prepaid balance GET, Cursor `agent`, speaker playback, report write, live Ecosystem file deletion, or turning a job on.
- Alexander adds key values to `master-key.env` if a later signed-off call needs them. This work order lists names only.
- If `jobs.py` or `master-key.env` is mid-edit at build time, pause and name that file.
- Phase 4 is done. See the result note below. Chat, TTS, the billing probe, and Cursor agent still need a separate spend sign-off.

---

## 7. Notes & constraints

- No force-push.
- Secrets stay out of git. Never print env values. Never add a second env file.
- Prefer small reversible steps.
- New periodic jobs stay gated off (`"enabled": False`). Scripts also fail closed unless `RR_API_PRICES` or `RR_API_SPEND` is set, and those stay unset.
- The proving test is an offline seed on a temp root: catalog rows exist, `may_spend("xai")` and `may_spend("cursor")` are false, and HTTP and spend entry points are not called.
- Phase 4 order is fixed: archive `api/` first. If that copy fails, do not delete. Then remove only `api/` from the old repo on this machine and on GitHub. Do not delete the repository.
- Do not import logs, samples, last-state files, generated reports, caches, virtualenvs, or `__pycache__` into Pacific, Database, the website, or git. `__pycache__` beside the old source goes to the archive only.
- Sends, speaker playback, OBS, hardware switching, deletion of live Ecosystem files, and cloud spend need Alexander's sign-off. This build did none of those.

---

## Result (2026-09-30)

Landed `System/ApiPrices/scripts/` (`envload.py`, `api_ledger.py`, `xai.py`, `cursor_fallback.py`, `job.py`). Jobs `api_prices` (10:25) and `cursor_fallback` (10:22, 16:22) are in `jobs.py` with `"enabled": False`. `master-key.env` was not edited.

Proof on `/tmp/rr-mig-35`: `seeded=25 prices=25 may_spend_xai=False (spend_master_off) may_spend_cursor=False (spend_master_off) http_attempts=0 spend_attempts=0`. The live Database path `System/ApiPrices` was not created. A proof pointed at the live Database exited 2.

Archive: `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/api/` (24 files, copy matched). Removed `api/` on GitHub `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server` commit `205f06e4` branch `online-safe-20260920`, and on `Solar-Pacific-RootRecord-Server-Old` commit `fa261cb` branch `main`. Neither repository was deleted. `apps.core` was left. `~/.ollama/skills` was not restored.

Library lines updated: matrix row 72 and blocker 6, the `api` catalog row, and the `api-prices` / `cursor-fallback` rows in the G1 scheduler map.

---

*Work order prepared 2026-09-30 HST. Update status when closed.*

---

## Archive / location note

This file is a draft. It is not on the active index. Do not promote it until Alexander accepts it.

**Active / accepted WOs** — filename when saved:

```text
API_prices_and_external_AI_fallback_Work_Order_WO-MIG-35-2026-09-29.md
```

Location after promotion:

```text
Documentation/06-development/Work-Orders/
```

**Drafts (not on active index)** — this file stays here until that decision:

```text
Documentation/06-development/Work-Orders/drafts/
```

See `drafts/README.md` and WO-WOGEN-001. Do not auto-promote.

**Closed WOs:** set Status → COMPLETE/CLOSED → `git mv` into:

```text
Documentation/06-development/Work-Orders/Complete/
```

Human session logs archive under `Documentation/01-operations/archive/YYYY-Www/` (WO-ARCH) — separate from closed work orders.

Phase 4 archive of the old function, after a successful build, is:

```text
Old repos deleted and merged/Solar-Pacific-RootRecord-Server/api/
```
