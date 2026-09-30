# WORK ORDER — Governance and origin session archive

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-MIG-06-2026-09-29 |
| **Date** | 2026-09-29 (HST) |
| **Status** | COMPLETE |
| **Owner** | RootRecord |
| **Related** | [Old-Repo-Migration-Matrix](../../../00-architecture/Old-Repo-Migration-Matrix.md) row 78; [G1-Scheduler-To-G3-Jobs-Map](../../../00-architecture/G1-Scheduler-To-G3-Jobs-Map-2026-09-29.md) (`governance-daily` OUT); [Solar-Pacific-Old-Full-TopLevel-Catalog](../../../00-architecture/Solar-Pacific-Old-Full-TopLevel-Catalog-2026-09-28.md); [Solar-Pacific-Old-Inventory-Map](../../../00-architecture/Solar-Pacific-Old-Inventory-Map-2026-09-28.md); [WO-OLD](../Old_Server_Selective_Recovery_Work_Order_WO-OLD-2026-09-28.md) |

**Scope:** Copy the decisions from the old `governance` packet, `origin-session`, and `ecosystem-history` into the Library. Do not install a Pacific package, do not schedule the old jobs, and do not bulk-import `origin/` or the ecosystem-history dump. Closed 2026-09-30. It is not on the active work-order index.

---

## 1. Intent

The old function recorded how RootRecord was governed and how the desk session started, plus a hand-written history of which hosts and paths are live.

`governance/` is three retired scheduler skills. `governance-daily` tallied community wishes and could queue a Cursor self-update. Defaults are off. `cursor_may_run` refuses unless community governance and self-update are both on, origin uptime is at least one hour, and free context is known and above 25%. Boot never self-updates. The migrate notes say do not restore the old body. The G1 jobs map already marks `governance-daily` **OUT (Library content)**.

`origin-session` wrote a pid and timestamp JSON so council could catch up when the desk started. Its migrate note says the body was moved and must not be restored. That packet is not the `origin/` app (~4342 paths). `origin/` stays untouched.

`ecosystem-history` holds the decisions in `NARRATIVE.md`: the OmniBook was the live host in that draft, the Dell OptiPlex is dead, Towny is not production, and the old Windows and OptiPlex paths are not live. `CURRENT.md` is generated. `references/` is a docs dump. `scripts/` includes destructive and playback helpers (`delete_archives_trees.sh`, archive and import shells, TTS proofs). Those do not become live code.

The live system already runs the poller, EcoFlow BLE, Hawaiʻi weather, the globe collector, camera grabs, Kokoro, and `geology_collect.py`. Those stay. Library work orders are the current governance of this migration. The old archive was not copied. This work copies the decisions into the Library and labels ecosystem-history facts **Historical**, because the live tree is now RootRecord-Ecosystem. It does not rebuild the `0-master-prompt` governance layer described in Claude Pass 3. That layer is a different subject.

---

## 2. Current reality

Folder name used in the Library: **Governance**. There is no Pacific, Database, or Logs folder for this function, and none will be created. This matches the catalog row for `governance` (Library) and matrix row 78 (archive-only).

### 2.1 What exists

| Item | Location / status |
| --- | --- |
| Code | None. Do not create `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Governance/`. Live Pacific has no `governance` or `origin_session` code. |
| Database | None. Do not create `2 - RootRecord-Database/Governance/`. |
| Logs | None. Do not create `2 - RootRecord-Database/Logs/Governance/`. |
| Docs (only live destination) | `5 - RootRecord-Library/Documentation/00-architecture/Governance/` — four decision pages |
| Old `governance/` | `/home/rootrecord/old ollama/old skills/governance` (132K). Three skills: `governance-daily`, `governance-boot`, `governance-self-update`. |
| Old `origin-session/` | `/home/rootrecord/old ollama/old skills/origin-session` (32K). `scripts/origin_session.py` plus skill notes. |
| Old `ecosystem-history/` | `/home/rootrecord/old ollama/old skills/ecosystem-history` (4.1M, 398 files). Decisions in `NARRATIVE.md`. |
| Old git remote | `git@github.com:rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server.git`, branch `online-safe-20260920` |
| Library name for that archive | `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server-Old` |
| Secrets | None. No `master-key.env` keys. Do not copy `.env` or sqlite dumps. |

### 2.2 Completed so far

- [x] Old source read. Decisions identified. Runtime dump and `origin/` excluded.
- [x] This draft written under `Work-Orders/drafts/`. Not promoted onto the active index.
- [x] Alexander said to complete the work.
- [x] Four Library decision pages written.
- [x] Phase 4 archive copy, then deletion from the old repo locally and on GitHub.
- [x] This work order updated with the result, and the stale Library rows corrected.

### 2.3 Known friction

- The local clone remote is `Solar-Pacific-RootRecord-Server`. Library docs call the archive `Solar-Pacific-RootRecord-Server-Old`. Phase 4 must confirm which GitHub repo still holds `governance/`, `origin-session/`, and `ecosystem-history/` before any deletion. If the copy fails, do not delete.
- `NARRATIVE.md` and `CURRENT.md` name paths (`~/.ollama/skills`, Ava-Core, OmniBook) that are not the live Ecosystem tree. Copied facts stay labeled Historical.
- `governance-daily/DAILY.md` is a telemetry snapshot (power, weather, camera age). It is generated output. It goes to the phase-4 archive only, not into the live Library pages.

---

## 3. Tasks

Build only after Alexander accepts this draft. No other function has to exist first. Nothing later in the migration list depends on this one. If a shared file (`jobs.py`, the Vercel app shell, or `master-key.env`) is already being edited when build starts, pause.

1. Add four Library files under `5 - RootRecord-Library/Documentation/00-architecture/Governance/`:
   - `README.md` — what was copied and what was refused (self-update gate, origin non-import, no Pacific Governance package).
   - `community-governance-decisions.md` — flags and the self-update gate, taken from the Python and the migrate notes. Not a port of the jobs.
   - `origin-session-decision.md` — the session-id helper, the do-not-restore note, and the exclusion of `origin/`.
   - `ecosystem-history-decisions.md` — condensed from `NARRATIVE.md` only. Each stale host or path marked Historical.
2. Do not edit `jobs.py`. Do not add `governance-daily`, `governance-boot`, or `governance-self-update`.
3. Phase 4, only after those Library pages exist and Alexander has signed off on the GitHub repo name: copy `governance/`, `origin-session/`, and `ecosystem-history/` — including generated notes, `__pycache__` excluded — into `/home/rootrecord/RootRecord-Ecosystem/Old repos deleted and merged/<confirmed-old-repo-name>/`, keeping the path each tree had inside the old repo. If that copy fails, stop. Do not delete. Then delete only those three trees from the old repo on this machine and on GitHub. Commit that deletion and push it. Do not force-push. Do not delete the GitHub repository.
4. Update this same work order with what landed, the archive path, and the GitHub deletion. Set the new status only then. Correct only the Library rows this function made stale: matrix row 78, the catalog lines for these three tops, and the inventory archive-only lines for `ecosystem-history/` (and the `origin/` line only to confirm it was not imported). Leave matrix row 69's other packets (goals, topics, skill-creator, and the rest) alone.

---

## 4. Non-goals

- Do not overwrite live Energy, Geology, Weather, Reports, Security, Communications, System, or Media.
- Do not create a Pacific `Governance` package, a Database folder, or a Logs folder.
- Do not import `origin/` (~4342 paths), `CURRENT.md`, `ecosystem-history/references/`, sqlite, `.env`, DAILY telemetry, or any ecosystem-history script into Pacific, Database, the website, or git as live source.
- Do not schedule `governance-daily`, `governance-boot`, or `governance-self-update`.
- Do not edit other agents' files. Shared `apps.core` is imported by the old scripts and is not owned by these three folders. Leave it.
- Do not restore files under `~/.ollama/skills/energy`, automations, or `coms/ssh/local-data-globe`.
- Do not replace the poller, EcoFlow BLE, Hawaiʻi weather, the globe collector, camera grabs, Kokoro, or `geology_collect.py`.
- Do not delete a whole GitHub repository. Do not force-push.
- Do not promote this draft onto the active work-order index until Alexander accepts it.

---

## 5. Key file / path reference

| Path | Role |
|------|------|
| `5 - RootRecord-Library/Documentation/06-development/Work-Orders/drafts/Governance_and_origin_session_archive_Work_Order_WO-MIG-06-2026-09-29.md` | This draft. Only file written before build. |
| `5 - RootRecord-Library/Documentation/00-architecture/Governance/README.md` | Decision index. Added at build. |
| `5 - RootRecord-Library/Documentation/00-architecture/Governance/community-governance-decisions.md` | Self-update gate and flags. Added at build. |
| `5 - RootRecord-Library/Documentation/00-architecture/Governance/origin-session-decision.md` | Session helper and origin non-import. Added at build. |
| `5 - RootRecord-Library/Documentation/00-architecture/Governance/ecosystem-history-decisions.md` | Historical decisions from `NARRATIVE.md`. Added at build. |
| `/home/rootrecord/old ollama/old skills/governance/` | Old packet. Phase 4 archive, then remove from the old repo. |
| `/home/rootrecord/old ollama/old skills/origin-session/` | Old packet. Phase 4 archive, then remove from the old repo. |
| `/home/rootrecord/old ollama/old skills/ecosystem-history/` | Old packet. Phase 4 archive, then remove from the old repo. |
| `/home/rootrecord/RootRecord-Ecosystem/Old repos deleted and merged/<confirmed-old-repo-name>/` | Phase 4 archive root. Relative paths kept. |
| `1 - Servers/.../Automations/scripts/jobs.py` | Do not edit. Must still have no governance job id after the test. |
| `/home/rootrecord/master/master-key.env` | No keys for this function. Do not edit. |

Code, database, and logs paths are intentionally empty. See section 2.

---

## 6. Open items

**Additional requirements:**

- Alexander accepts this draft and says to build before any Library decision pages are written.
- Confirm the GitHub repo that still contains the three trees (`Solar-Pacific-RootRecord-Server` vs `Solar-Pacific-RootRecord-Server-Old`) before phase 4 deletion.
- Phase 4 deletion of old-repo files is already ordered, and still waits on a successful archive copy plus that repo confirmation.
- Sends, speaker playback, OBS, hardware switching, deletion of live Ecosystem files, and cloud spend stay blocked until a separate sign-off. This function does not need any of those.

---

## 7. Notes & constraints

- No force-push.
- Secrets stay out of git. No second env file. No key values in this work order.
- Prefer small reversible steps.
- New periodic jobs stay gated off. This plan does not propose a `jobs.py` block.
- Small test, after the Library pages exist: `Documentation/00-architecture/Governance/README.md` states the self-update gate (off unless context is known and above 25%, and origin uptime is at least one hour), states that `origin/` was not imported, and states that Pacific has no Governance package. `jobs.py` still has no governance job id.
- After phase 4, add a short result note here: what landed, the archive path, and what was removed on GitHub. Then correct only the Library pages listed in task 4.

---

*Work order prepared 2026-09-29 HST. Update status when closed.*

---

## Archive / location note

This file is closed. It is not on the active index.

```text
Governance_and_origin_session_archive_Work_Order_WO-MIG-06-2026-09-29.md
```

Location:

```text
Documentation/06-development/Work-Orders/Complete/
```

See `drafts/README.md` and WO-WOGEN-001. Do not auto-promote.

**Closed WOs:** set Status → COMPLETE/CLOSED → `git mv` into:

```text
Documentation/06-development/Work-Orders/Complete/
```

Human session logs archive under `Documentation/01-operations/archive/YYYY-Www/` (WO-ARCH) — separate from closed work orders.

---

## Result note

Landed 2026-09-30 HST.

**Library.** `Documentation/00-architecture/Governance/` now has `README.md`, `community-governance-decisions.md`, `origin-session-decision.md`, and `ecosystem-history-decisions.md`. No Pacific package, no Database folder, no Logs folder, no `jobs.py` edit, no `master-key.env` keys. `jobs.py` has no governance job id. `origin/` was not imported (still HTTP 200 on -Old).

**Archive.** 419 files, `__pycache__` excluded, at `Old repos deleted and merged/Solar-Pacific-RootRecord-Server-Old/` under `governance/`, `origin-session/`, and `ecosystem-history/`. The copy matched the on-machine trees before deletion. `main` and `skills-rebuild` had no files beyond that archive.

**Removed.** The three trees are gone from the machine (`/home/rootrecord/old ollama/old skills`) and from `Solar-Pacific-RootRecord-Server-Old` (GitHub contents HTTP 404):

- `online-safe-20260920` `4fe7f7c4`
- `main` `fd0a9c0`
- `skills-rebuild` `c864821`

The repository was not deleted. No force-push. Nothing was pushed to `Solar-Pacific-RootRecord-Server` (that remote never had these paths). The `online-safe-20260920` push also published two commits already on the local branch and not yet on GitHub: radar-archive (`8c9437d0`) and RAMMB sources (`e8c37881`).

**Library rows corrected.** Matrix row 78, the catalog lines for `governance`, `ecosystem-history`, and `origin-session`, and the inventory archive-only lines. Matrix row 69 was left unchanged.
