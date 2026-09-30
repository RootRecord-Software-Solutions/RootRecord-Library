# WORK ORDER — Bruce stats posts

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-MIG-26-2026-09-29 |
| **Date** | 2026-09-30 (HST) |
| **Status** | OPEN — built (dry-run); send not signed off |
| **Owner** | RootRecord |
| **Related** | Agent 26, wave D. Depends on Folder 25, Council quake Telegram posts (`Communications/CouncilQuake`). No later function waits on this one. Matrix row 60, Bruce clause only. |

**Scope:** Build Bruce’s measured desk sample from the live host and EcoFlow last files, three times a day, and keep the Telegram send off until a separate sign-off. Keep the host sampler, the EcoFlow poller, and `council-relay.py`. This draft does not authorize a live send, a poller restart, speaker playback, hardware changes, or cloud spend.

---

## 1. Intent

Old `council/council-bruce-stats/scripts/job.py` calls `tick()`. The body is `council/council-telegram/scripts/bruce_stats.py`. At 07:18, 15:18, and 21:18 HST it posts once per hour slot as Bruce:

```text
Desk sample (measured)
<host line>
<ecoflow line>

Bruce Monitor
```

It skips when council discussion is off, and it never invents watts. `origin/ns/apps/council/bruce_stats.py` only loads that script. The function was absent because the Telegram send was not signed off.

Live readers stay. Host samples stay in `2 - RootRecord-Database/System/last/host-last.json` from `System/lib/sample.py`. EcoFlow stays in `2 - RootRecord-Database/Energy/soc/` and `Energy/watts/`. Do not replace the BLE poller, `council-relay.py` (one `getUpdates` owner), or live jobs.

Text uses only those last files: host CPU, RAM, and load, plus Delta 2 and River 2 Pro state of charge and watts, with the sample time. A missing file is `DOWN`. No watts are filled in.

---

## 2. Current reality

### 2.1 What exists

Folder name, used in all three places: `BruceStats` (inside Communications). No lowercase twin. No second top-level domain.

| Item | Location / status |
| --- | --- |
| Server code | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/BruceStats/scripts` — package name `BruceStats`. No `Logs/` directory on the server. |
| Database data | `2 - RootRecord-Database/Communications/BruceStats/` — slot file and last text only. |
| Database logs | `2 - RootRecord-Database/Logs/Communications/BruceStats/` — one JSON line per tick. |
| Host samples (keep) | `2 - RootRecord-Database/System/last/host-last.json`, written by `System/lib/sample.py`. |
| EcoFlow samples (keep) | `2 - RootRecord-Database/Energy/soc/{delta2,river2pro}-last.json` and `Energy/watts/{delta2,river2pro}-last.json`. |
| Quake posts folder (dependency) | `Communications/CouncilQuake/` is on disk. Chat id helper: `quake_posts.council_chat_id`. `maybe_send` in that file posts as Carly under `RR_COUNCIL_QUAKE_SEND`. This function does not call `maybe_send`. |
| Live relay (keep) | `Communications/telegram/scripts/council-relay.py`. Chat id key: `COUNCIL_CHAT_ID` in `Communications/telegram/config/relay.conf`. |
| Secrets | `/home/rootrecord/master/master-key.env` only. Allowlist key name: `TELEGRAM_BRUCE_TOKEN`. Loaded only when `RR_BRUCE_STATS_SEND=1`. Never print the value. |

### 2.2 Completed so far

- [x] Old source read (`council-bruce-stats`, `bruce_stats.py`, the origin shim).
- [x] Council quake Telegram posts folder is in place, so the build does not pause.
- [x] Dry-run proof passed. Phase 4 archive and GitHub deletion are in the result note below.

### 2.3 Known friction

- `Communications/CouncilQuake/scripts/quake_posts.py` `maybe_send` uses `TELEGRAM_CARLY_TOKEN`. Bruce cannot post through that function and still be voice Bruce.
- This function calls `council_chat_id` from that folder when the Bruce send flag is on, then `sendMessage` with `TELEGRAM_BRUCE_TOKEN`. The default run does not import that helper, does not load the token, and does not make an HTTP call.
- The old discussion-off holdoff has no live state file under `2 - RootRecord-Database/Intake/council-relay/`. This function does not add a second holdoff store.
- `jobs.py` is shared. This work order adds one gated block only. If that file is already being edited, pause.

---

## 3. Tasks

1. Confirm `Communications/CouncilQuake/` exists. If it does not, stop and name Council quake Telegram posts. Do not build that function.
2. Add `Communications/BruceStats/scripts/bruce_stats.py`. Read the live last files. Print the desk sample. Write the slot and last text under Database `Communications/BruceStats/`. Append one log line. Default is dry-run.
3. Add `Communications/BruceStats/scripts/envload.py` with allowlist `TELEGRAM_BRUCE_TOKEN` only. Dry-run does not load it.
4. Add `Communications/BruceStats/__init__.py` and `README.md` naming the Folder and the three paths.
5. Add one `ON_AT` block in `Automations/scripts/jobs.py`: id `bruce_stats_posts`, times `07:18`, `15:18`, `21:18` HST, enabled only when `RR_BRUCE_STATS=1`. `RR_BRUCE_STATS_SEND=1` is required before any Telegram call. Do not restart the poller.
6. Prove the dry-run: the text contains `Desk sample (measured)`, a host line, and an EcoFlow line; the slot file is under Database `Communications/BruceStats/`; nothing is posted.
7. After that proof, archive the old paths, delete them from the old repo locally and on GitHub, then fill the result note and correct only the Bruce lines named in section 5.

---

## 4. Non-goals

- Do not overwrite Energy BLE, the poller, Hawaiʻi weather, the globe collector, camera grabs, Kokoro, or `geology_collect.py`.
- Do not edit other agents’ functions. Do not build Council quake Telegram posts, Council health, Discord, or Slack.
- Do not import logs, samples, last-state files, generated reports, or `__pycache__` into live Pacific, the website, or git. Runtime slot and log files stay under Database and out of git.
- Leave shared old sources: the rest of `council/council-telegram/`, `notify.py`, `origin/ns/apps/council/` except `bruce_stats.py`, `db_facts.py`, and `scheduler.py`.
- Do not replace `council-relay.py`. Do not add a second `getUpdates` poller.
- Do not post to Discord or Slack.
- Do not delete the GitHub repository. Do not force-push.

---

## 5. Key file / path reference

| Path | Role |
|------|------|
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/BruceStats/scripts` | New code. Package `BruceStats`. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/BruceStats/scripts/bruce_stats.py` | Build the measured text, slot once per hour, dry-run by default. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/BruceStats/scripts/envload.py` | Allowlist `TELEGRAM_BRUCE_TOKEN` only. Never print the value. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/BruceStats/README.md` | Folder name and the three paths. |
| `2 - RootRecord-Database/Communications/BruceStats/` | `slot.json` and `last-text.txt`. |
| `2 - RootRecord-Database/Logs/Communications/BruceStats/` | `bruce-stats.jsonl`, one JSON line per tick. |
| `2 - RootRecord-Database/System/last/host-last.json` | Read only. |
| `2 - RootRecord-Database/Energy/soc/` and `Energy/watts/` | Read only. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/CouncilQuake/scripts/quake_posts.py` | Call `council_chat_id` only when the send flag is on. Do not call `maybe_send`. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/telegram/config/relay.conf` | Existing `COUNCIL_CHAT_ID`. Do not add a second chat config. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/telegram/scripts/council-relay.py` | Keep. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Automations/scripts/jobs.py` | One gated `bruce_stats_posts` block, default off. |
| `/home/rootrecord/master/master-key.env` | `TELEGRAM_BRUCE_TOKEN` only. Do not commit. Do not print. |
| `/home/rootrecord/old ollama/old skills/council/council-bruce-stats/` | Old function. Archive, then delete. |
| `/home/rootrecord/old ollama/old skills/council/council-telegram/scripts/bruce_stats.py` | This function’s processor. Archive, then delete. Leave the rest of `council-telegram`. |
| `/home/rootrecord/old ollama/old skills/origin/ns/apps/council/bruce_stats.py` | Shim. Archive, then delete. Leave the rest of `apps/council`. |
| `5 - RootRecord-Library/Documentation/00-architecture/G1-Scheduler-To-G3-Jobs-Map-2026-09-29.md` | Phase 5: correct the `council-bruce-stats` line only. |
| `5 - RootRecord-Library/Documentation/00-architecture/Old-Repo-Migration-Matrix.md` | Phase 5: Bruce clause of row 60 and item 12 only. |
| `5 - RootRecord-Library/Documentation/07-testing/2026-09-29-old-repo-ports-breadth-batch4.md` | Phase 5: Bruce clause of the blocked bullet only. |

---

## 6. Open items

**Additional requirements:**

- Alexander accepts this draft and says to build before any file outside this draft is written.
- If `Communications/CouncilQuake/` is missing at build time, pause and name Council quake Telegram posts. Do not build it.
- If `jobs.py` or `master-key.env` is already being edited at build time, pause and name the file.
- `RR_BRUCE_STATS_SEND=1` stays off until a separate sign-off. Enabling the dry-run job is not a send.
- Phase 4 deletes only the three old paths after the archive copy is on disk. Shared files stay. If the archive copy fails, do not delete.
- Phase 5 result note is filled below. This draft stays in `drafts/` and is not on the active index.

---

## 7. Notes & constraints

- No force-push. Do not delete the GitHub repository `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server`.
- Secrets stay out of git. The plan lists `TELEGRAM_BRUCE_TOKEN` by name only. Never print the value. Never add a second env file.
- Prefer small reversible steps.
- Sign-off gate: do not call Telegram `sendMessage` unless `RR_BRUCE_STATS_SEND=1`, do not set that flag, do not play speakers, do not switch hardware, do not restart the poller, and do not spend cloud money. The proposed job runs the dry-run script only, and only when `RR_BRUCE_STATS=1` at the next poller start Alexander chooses.
- Proof test: a dry run prints `Desk sample (measured)`, a `Host:` line, and an `EcoFlow:` line; `slot.json` lands under Database `Communications/BruceStats/`; `sent` is false and no HTTP call is made.
- Phase 4 archive root: `/home/rootrecord/RootRecord-Ecosystem/Old repos deleted and merged/Solar-Pacific-RootRecord-Server-Old/`. Keep each file’s path from inside the old repo, including `__pycache__` that sat beside the source. Generated data stays in that archive and out of the live Folders. If the archive copy fails, do not delete.
- After phase 4, add a short result note here (what landed, archive path, what was removed on GitHub) and correct only the Library lines named in section 5.

---

*Work order prepared 2026-09-30 HST. Update status when closed.*

---

## Archive / location note

This file is a draft. It is not on the active index. Do not auto-promote.

```text
Documentation/06-development/Work-Orders/drafts/Bruce_stats_posts_Work_Order_WO-MIG-26-2026-09-29.md
```

See `drafts/README.md` and WO-WOGEN-001. Promotion is Alexander's decision: move into `Documentation/06-development/Work-Orders/`, set Status, and add an index row.

**Closed WOs:** set Status → COMPLETE/CLOSED → `git mv` into `Documentation/06-development/Work-Orders/Complete/`.

Human session logs archive under `Documentation/01-operations/archive/YYYY-Www/` (WO-ARCH) — separate from closed work orders.

### Phase 4 / phase 5 result

**Landed.** `Communications/BruceStats/` reads the live host and EcoFlow last files and writes `slot.json` plus `last-text.txt` under Database `Communications/BruceStats/`. The dry-run printed `Desk sample (measured)`, a host line, and an EcoFlow line. `sent` was false. Job `bruce_stats_posts` is in `jobs.py`, off unless `RR_BRUCE_STATS=1`. `RR_BRUCE_STATS_SEND` was not set. No poller restart.

**Archived.** `Old repos deleted and merged/Solar-Pacific-RootRecord-Server-Old/` keeping the old paths: `council/council-bruce-stats/` (including `scripts/__pycache__/job.cpython-314.pyc`), `council/council-telegram/scripts/bruce_stats.py`, `origin/ns/apps/council/bruce_stats.py`, and `origin/ns/apps/council/__pycache__/bruce_stats.cpython-314.pyc`.

**Removed on GitHub.** `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server`, branch `online-safe-20260920`, commit `7feb8e5f`. The repository was not deleted. `origin/main` did not contain these files. Shared files left in the old repo: the rest of `council/council-telegram/`, the rest of `origin/ns/apps/council/`, `notify.py`, and `scheduler.py`.

**Library.** Bruce lines only: `G1-Scheduler-To-G3-Jobs-Map-2026-09-29.md`, matrix row 60 and item 12, and the batch-4 blocked bullet. Council health text in those pages was left as the health work order wrote it.
