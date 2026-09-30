# WORK ORDER — D1 sync

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-MIG-30-2026-09-29 |
| **Date** | 2026-09-30 (HST) |
| **Status** | OPEN — draft, not accepted for execution |
| **Owner** | RootRecord |
| **Related** | Agent 30. Wave D. Later function: 31. Inbox, drain, overnight relay, reply feedback. No earlier function has to exist before the build. |

**Scope:** Port the old D1 sync into the Ecosystem layout as one Folder, `D1`. In scope: a dry-run CLI that records `not_configured` when the D1 id is absent, the RootMC `rootmc-live` schema template, an allowlisted env loader, and one gated-off job proposal. Out of scope until Alexander accepts this draft and signs off a push: Cloudflare writes, MySQL reads, poller restart, and old-repo deletion. Inbox, the site worker, and the rest of matrix row 68 stay with their own functions.

---

## 1. Intent

The old function pushes a RootMC edge cache from host MySQL into Cloudflare D1 database `rootmc-live`. The host does the joins and the math. D1 keeps `player_balances` and `server_status` so workers still have balances and online flags when the origin is down. The job skips when `CF_D1_ROOTMC_DB_ID` is unset. Wallet rewrites are rare because they burn the D1 free-tier `rows_written` quota. A pause flag can skip balances and still write status.

What must be kept: that same edge-copy behavior for **live** `play.rootmc.net:25565` and **test** `127.0.0.1:24945` only. The live site worker stays without a D1 binding. EcoFlow BLE, the poller, Hawaiʻi weather, the globe collector, camera grabs, Kokoro, and `geology_collect.py` stay as they are.

The expired hard-coded pause through 2026-09-05 UTC is not carried forward. An operator pause stays, via `AVA_D1_SYNC_PAUSE_UNTIL` and `2 - RootRecord-Database/D1/d1-sync.json`.

---

## 2. Current reality

Folder name, used in all three places: **D1**. One capitalized top-level Folder. It is not a subfolder of Communications. No lowercase twin, no symlink, no `Logs/` directory on the server. Python package name: `D1`.

### 2.1 What exists

| Item | Location / status |
| --- | --- |
| Server code | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/D1/scripts` — not created. This draft does not create it. |
| Database data | `2 - RootRecord-Database/D1/` — not created. Last file and pause state land here at build time. No samples imported. |
| Database logs | `2 - RootRecord-Database/Logs/D1/` — not created. |
| Secret key names | `/home/rootrecord/master/master-key.env` only. Follow `Energy/lib/envload.py`: an allowlist, never print values, never add a second env file, never commit secrets. Present today: `CLOUDFLARE_ACCOUNT_ID`. Absent: the D1 database id, the API token, and the MySQL keys listed in section 6. |
| Live worker (keep) | `Communications/Cloudflare-Workers/config/wrangler.toml` — no route, no account id, no D1 id. Do not edit it. |
| Old source | `Solar-Pacific-RootRecord-Server` branch `online-safe-20260920`, checkout `/home/rootrecord/old ollama/old skills`. Function files: `database/d1-sync/scripts/job.py` and shim `origin/ns/apps/core/crons/always_on/d1_sync.py`. Schema template: `cloudflare-workers/workers/sql/rootmc-live.sql` (shared; leave the workers copy). `~/.ollama/skills` is `main` and does not have these files. Do not restore anything there. |
| Scheduler map | `d1-sync` every 6 h, blocked on D1 credentials (`G1-Scheduler-To-G3-Jobs-Map-2026-09-29.md`). |
| Matrix | `Old-Repo-Migration-Matrix.md` row 68 is still partial: D1/MySQL need credentials; policy docs only. |

### 2.2 Completed so far

- [x] Old source read. The job upserts `server_status` (live and test) and `player_balances`. Schema also defines `player_playtime`, `economy_snapshot`, and `sync_meta`. The job writes `sync_meta` and does not write playtime or economy snapshots.
- [x] Folder name and the three paths are fixed above.
- [ ] Runtime files. Not started. This draft is not acceptance.
- [ ] Dry-run proof.
- [ ] Phase 4 archive and GitHub deletion.
- [ ] Phase 5 result note and the two Library corrections.

### 2.3 Known friction

- `CLOUDFLARE_ACCOUNT_ID` is present. `CF_D1_ROOTMC_DB_ID` / `D1_ROOTMC_LIVE_ID` and an API token are not. A run without the database id must not POST to Cloudflare.
- MySQL keys are not in `master-key.env`. Balance sync has nothing to read until those names are added. Status-only is the path when MySQL is unset.
- `database/d1/scripts/d1.py` is shared with account-import, user-qrcodes, and public-edge. Leave it in the old repo.
- The cron shim execs `~/.ollama/skills/d1-sync/scripts/job.py`. That path is not restored. The new CLI is the Pacific script.
- `jobs.py` is shared. The only proposed edit is one gated-off block, and only after this draft is accepted.

---

## 3. Tasks

1. Stop after this draft. Wait until Alexander accepts it and says to build. Until then, do not edit runtime files, restart services, send messages, actuate hardware, or spend cloud money.
2. At build time, no earlier Folder is required. Inbox (31) waits on this Folder. Do not build inbox. If `jobs.py` or `master-key.env` is already being edited, pause.
3. Create `D1/` with `scripts/`, `lib/`, and `config/` only. Mirror `D1/` under Database and under `Logs/`. Do not put logs on the server. Do not import logs, samples, last-state files, or `__pycache__` into the live Folders.
4. Add `D1/lib/envload.py` (allowlist in section 6, never print values), `D1/lib/d1.py` (REST query; missing database id or account id returns not configured and does not POST), `D1/scripts/d1_sync.py`, `D1/config/rootmc-live.sql` (copy of the old schema template), and a short `D1/README.md`.
5. Default CLI is dry-run: no TCP, no MySQL, no Cloudflare. It writes `2 - RootRecord-Database/D1/d1-sync-last.json` with `not_configured` when the D1 id is absent.
6. `--push` is the signed-off path. It upserts `server_status` for live and test (TCP ping only those two hosts), then wallet rows from the first MySQL table that returns rows (`root_economy_balances`, `rootstat_player_balances`, `player_balances`, limit 5000). Missing keys skip that part and do not call the API. Do not run `--push` in this draft, and do not run it at build time unless Alexander signs off the push.
7. After acceptance, add one gated block to `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Automations/scripts/jobs.py`: id `d1_sync`, interval 21600 seconds (6 h), `enabled` only when `RR_D1_SYNC=1`. That is the only `jobs.py` edit. Do not start the poller. Do not set the flag.
8. Proof, before any Library correction: `python3 "1 - Servers/1 - RootRecord-Pacific-Solar-Server/D1/scripts/d1_sync.py" --dry-run` exits 0, writes the last file, and does not contact `api.cloudflare.com`.
9. After that check passes, phase 4: copy `database/d1-sync/**` and `origin/ns/apps/core/crons/always_on/d1_sync.py` into `/home/rootrecord/RootRecord-Ecosystem/Old repos deleted and merged/Solar-Pacific-RootRecord-Server/`, keeping the path each file had inside the old repo. Generated data that lived beside that source (`database/d1-sync/scripts/__pycache__/`) goes into the archive too, and still does not go into the live Folders. After the archive copy is on disk, delete those same paths from branch `online-safe-20260920` on this machine and on GitHub. Commit that deletion and push it. Do not force-push. Do not delete the GitHub repository. If the archive copy fails, do not delete. Do not commit from `~/.ollama/skills`.
10. Phase 5: add the result note in section 7 of this file (what landed, what was archived, what was removed on GitHub) and set the new status. Correct only the Library pages this function made stale: `Old-Repo-Migration-Matrix.md` row 68 (the D1 sync portion; leave mysql, db-facts, data-layout, state, and desk-data-reader), and the `d1-sync` row in `G1-Scheduler-To-G3-Jobs-Map-2026-09-29.md`. Do not rewrite unrelated work orders. Do not promote this file onto the active index until Alexander accepts it.

---

## 4. Non-goals

- Do not build 31. Inbox, drain, overnight relay, or reply feedback.
- Do not build Discord, Slack, Telegram, or the economy brief.
- Do not edit `Communications/Cloudflare-Workers/config/wrangler.toml` or attach a D1 binding to the site worker.
- Do not port RCON, Paper log tails, systemd unit control, or Hyperdrive.
- Do not add writers for `player_playtime` or `economy_snapshot`. The tables may remain in the schema template as `CREATE TABLE IF NOT EXISTS`.
- Do not replace EcoFlow BLE, the poller, Hawaiʻi weather, the globe collector, camera grabs, Kokoro, or `geology_collect.py`.
- Do not edit `jobs.py` except the one gated `d1_sync` block after acceptance. Do not enable it.
- Do not take the rest of matrix row 68: `mysql`, `db-facts`, `data-layout`, `state`, `desk-data-reader`.
- Do not restore files under `~/.ollama/skills`, including `energy`, `automations`, and `coms/ssh/local-data-globe`.
- Do not import system-generated data into Pacific, Database, the website, or git. Runtime output stays in the Database paths above.
- Do not add a public page. Android apps in `6 - Android Development` stay there.
- Shared old-repo files to leave, and not delete: `database/d1/**` (also used by account-import, user-qrcodes, and public-edge), `origin/ns/apps/core/services/d1.py`, `origin/scripts/config.py`, and `cloudflare-workers/workers/sql/rootmc-live.sql`.

---

## 5. Key file / path reference

| Path | Role |
|------|------|
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/D1/scripts/d1_sync.py` | CLI. Dry-run by default. `--push` only after sign-off. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/D1/lib/d1.py` | D1 REST helper. Missing id or account does not POST. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/D1/lib/envload.py` | Allowlist loader. Never prints values. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/D1/config/rootmc-live.sql` | Schema template copied from the old workers SQL. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/D1/README.md` | Short folder note. |
| `2 - RootRecord-Database/D1/d1-sync-last.json` | Last dry-run or push result. Not created by this draft. |
| `2 - RootRecord-Database/D1/d1-sync.json` | Pause state. Not created by this draft. |
| `2 - RootRecord-Database/Logs/D1/` | Logs only. Not created by this draft. |
| `/home/rootrecord/master/master-key.env` | Only secret file. Names in section 6. No values in this work order. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Automations/scripts/jobs.py` | One gated block after acceptance: `d1_sync`, `RR_D1_SYNC`, 21600 s. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Energy/lib/envload.py` | Pattern for the allowlist loader. Do not edit. |
| `/home/rootrecord/old ollama/old skills/database/d1-sync/scripts/job.py` | Old job. Archive in phase 4, then delete from `online-safe-20260920`. |
| `/home/rootrecord/old ollama/old skills/origin/ns/apps/core/crons/always_on/d1_sync.py` | Old shim. Archive in phase 4, then delete from that branch. |
| `5 - RootRecord-Library/Documentation/00-architecture/Old-Repo-Migration-Matrix.md` | Correct row 68 only after phase 4. |
| `5 - RootRecord-Library/Documentation/00-architecture/G1-Scheduler-To-G3-Jobs-Map-2026-09-29.md` | Correct the `d1-sync` row only after phase 4. |

---

## 6. Open items

**Additional requirements:**

- Accept this draft before any runtime edit.
- Sign off `--push` separately. A dry-run proof is not a push.
- Sign off `RR_D1_SYNC=1` separately. The job stays off. Do not restart the poller as part of adding the gated block.
- Add D1 and MySQL values to `master-key.env` only when a push is wanted. This work order does not write that file. Key names, not values:
  - D1: `CF_D1_ROOTMC_DB_ID`, `D1_ROOTMC_LIVE_ID`, `ROOTMC_CLOUDFLARE_ACCOUNT_ID`, `CLOUDFLARE_ACCOUNT_ID` (present), `CF_API_TOKEN`, `CLOUDFLARE_API_TOKEN`, `CF_EMAIL`, `CLOUDFLARE_EMAIL`, `CF_GLOBAL_API_KEY`, `CLOUDFLARE_API_KEY`, `CLOUDFLARE_GLOBAL_API_KEY`, `CF_WORKERS_EMAIL`, `CF_WORKERS_API_KEY`
  - MySQL, used only on an accepted push: `ROOTMC_CORE_MYSQL_HOST`, `ROOTMC_CORE_MYSQL_PORT`, `ROOTMC_CORE_MYSQL_USER`, `ROOTMC_CORE_MYSQL_PASSWORD`, `ROOTMC_CORE_MYSQL_DATABASE`, `ROOTMC_LOCAL_MYSQL_HOST`, `ROOTMC_LOCAL_MYSQL_PORT`, `ROOTMC_LOCAL_MYSQL_USER`, `ROOTMC_LOCAL_MYSQL_PASSWORD`, `ROOTMC_LOCAL_MYSQL_DATABASE`
  - Pause and hosts: `AVA_D1_SYNC_PAUSE_UNTIL`, `ROOTMC_PLAY_HOST`, `ROOTMC_PLAY_PORT`, `ROOTMC_TEST_HOST`, `ROOTMC_TEST_PORT`
- Phase 4 deletion is on branch `online-safe-20260920` of `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server` only, and only after the archive copy is on disk.

---

## 7. Notes & constraints

- No force-push.
- Secrets stay out of git. Do not print env values.
- Prefer small reversible steps.
- No `--push`, no `RR_D1_SYNC=1`, no Cloudflare call, no MySQL call, no poller restart, and no old-repo deletion until Alexander accepts this draft and then signs off the push.
- Hosts stay live production `play.rootmc.net` and test on this machine (`127.0.0.1:24945`). Do not add another production target.
- The small test that proves the new behavior: dry-run exits 0, writes `d1-sync-last.json` with `not_configured` while the D1 id is absent, and does not contact `api.cloudflare.com`.
- Phase 4 and phase 5 result notes are not written yet. This file stays a draft and is not on the active index.

**Result note (phase 4 / phase 5):** not started.

---

*Work order prepared 2026-09-30 HST. Update status when closed.*

---

## Archive / location note

**Active / accepted WOs** — filename when saved:

```text
D1_sync_Work_Order_WO-MIG-30-2026-09-29.md
```

Location when accepted:

```text
Documentation/06-development/Work-Orders/
```

**Drafts (not on active index)** — this file:

```text
Documentation/06-development/Work-Orders/drafts/D1_sync_Work_Order_WO-MIG-30-2026-09-29.md
```

See `drafts/README.md` and WO-WOGEN-001. Do not auto-promote.

**Closed WOs:** set Status → COMPLETE/CLOSED → `git mv` into:

```text
Documentation/06-development/Work-Orders/Complete/
```

Human session logs archive under `Documentation/01-operations/archive/YYYY-Www/` (WO-ARCH) — separate from closed work orders.
