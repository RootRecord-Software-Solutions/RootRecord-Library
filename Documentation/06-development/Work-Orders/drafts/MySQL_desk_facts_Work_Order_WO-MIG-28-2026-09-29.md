# WORK ORDER — MySQL desk facts

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-MIG-28-2026-09-29 |
| **Date** | 2026-09-30 (HST) |
| **Status** | BUILT — missing-credentials proof passed 2026-09-30 00:32 HST. Live Shockbyte read not run. Not on the active index. |
| **Owner** | RootRecord |
| **Related** | Agent 28, Wave D. Later function that depends on this Folder: 29, Economy brief. Old home: `mysql`, `database/db-facts` in `old ollama/old skills` (git remote `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server`). |

**Scope:** One read-only MySQL desk-facts client under System. In scope is the Folder, the allowlisted key names, an on-demand facts command, and the missing-credentials proof. Out of scope is the old MySQL app (pool, writes, cron inserts), EcoFlow and host fact lines, the economy brief, Discord, and any other agent's function. This file stays in drafts. Do not promote it onto the active index.

---

## 1. Intent

Old `mysql/scripts/mysql.py` is an aiomysql app: a local pool (`AVA_MYSQL_*` toward `ava_core` on port 3306), a Shockbyte ping (`ROOTMC_CORE_MYSQL_*`), `query`, `execute`, and inserts into `ava_cron.cron_runs`. Old `database/db-facts/scripts/db_facts.py` speaks EcoFlow, host, and identity counts from SQLite and jsonl. It never inserts, and it never prints emails, Discord ids, UUIDs, or Solana pubs.

The live system already covers the parts that must stay: EcoFlow BLE, `System/scripts/host_desks.py`, the poller, and Ava-Ops in `6 - Android Development`. This function does not replace those. It does not recreate the MySQL app: no pool, no `execute`, no `log_cron_run`, no aiomysql. It does not re-read EcoFlow jsonl or host history.

What it adds is one on-demand read-only facts call the economy brief can use later. The shape follows the aggregates `rootmc_economy.snapshot()` already returned. That RootMC module is not copied.

- `ok`, `local_3306`, `shockbyte`, `source`, `error` (exception class or a short reason only)
- `wallets`, `total_gold`, `positive_gold`, `avg_gold`, `max_gold` from `root_economy_balances`
- `bonds_count`, `bonds_principal` from `root_bonds` (unredeemed principal)
- pool totals from `root_list_totals` where `scope='claims'` and `group_key='pools'`
- top 5 in-game names and balances

No `SELECT *`. Gold stays an in-game number.

---

## 2. Current reality

### 2.1 What exists

Folder name: **MysqlDesk**, under the System domain. One capitalized folder. No lowercase twin and no symlink.

| Item | Location / status |
| --- | --- |
| Server code | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/System/MysqlDesk/scripts` — not created yet. Package name `MysqlDesk`. No `Logs/` directory on the server. |
| Database data | `2 - RootRecord-Database/System/MysqlDesk/` — not created yet. Runtime last file only. |
| Database logs | `2 - RootRecord-Database/Logs/System/MysqlDesk/` — not created yet. |
| Secrets | `/home/rootrecord/master/master-key.env` only. No `MYSQL` key names are present today. |
| Old mysql skill | `/home/rootrecord/old ollama/old skills/mysql/` |
| Old db-facts skill | `/home/rootrecord/old ollama/old skills/database/db-facts/` |
| Live host desks | `System/scripts/host_desks.py` — keep |
| Live EcoFlow | Energy BLE poller — keep |

Allowlist, same pattern as `Energy/lib/envload.py`. Names only:

- `ROOTMC_CORE_MYSQL_HOST`
- `ROOTMC_CORE_MYSQL_PORT`
- `ROOTMC_CORE_MYSQL_USER`
- `ROOTMC_CORE_MYSQL_PASSWORD`
- `ROOTMC_CORE_MYSQL_DATABASE`
- `AVA_MYSQL_HOST`
- `AVA_MYSQL_PORT`
- `AVA_MYSQL_USER`
- `AVA_MYSQL_PASSWORD`
- `AVA_MYSQL_DATABASE`

Shockbyte is preferred when all five `ROOTMC_CORE_MYSQL_*` names are set (port may default to 3306). Local `AVA_MYSQL_*` is the fallback. An incomplete set is skipped. Never print values. Never add a second env file.

No `mysql` client and no PyMySQL are installed. The live path may import PyMySQL lazily. The missing-credentials path returns before that import and before any socket.

### 2.2 Completed so far

- [x] Old source read (`mysql.py`, `db_facts.py`) and live System / Energy layout checked
- [x] `MysqlDesk` client built
- [x] Missing-credentials proof (2026-09-30 00:32 HST)
- [x] Old files archived, then removed from the old repo and GitHub where unshared
- [x] Library row 68 corrected for this function only

### 2.3 Known friction

- `master-key.env` has none of the allowlisted names, so a live Shockbyte read cannot run.
- `live-data-pages/scripts/live_data_pages.py` in the old repo imports `apps.core.services.db_facts`. If that import still points at this function's file, leave the file and name it.
- Row 68 of the migration matrix also covers d1, data-layout, state, and desk-data-reader. Those stay with their own functions.

---

## 3. Tasks

1. This draft stays OPEN until Alexander accepts it and says to build.
2. Add `System/MysqlDesk/lib/envload.py` and `System/MysqlDesk/scripts/mysql_desk.py`.
3. `python3 mysql_desk.py facts` writes `2 - RootRecord-Database/System/MysqlDesk/facts-last.json` and appends one log line (ok, source, error — no DSN, no balances) under `Logs/System/MysqlDesk/`. Those runtime files stay out of git.
4. Missing credentials: `ok` false, `error` `missing-credentials`, `local_3306` false, `shockbyte` false. No network.
5. Do not edit `jobs.py`. No periodic job. No other function has to exist before this build.
6. Proof: run `facts` with the allowlist empty. Confirm the JSON above and that PyMySQL is not imported. Do not run a live Shockbyte `SELECT` until Alexander confirms the key names are in `master-key.env`.
7. After that proof: copy `mysql/` and `database/db-facts/` into `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/`, keeping those paths. Then delete them from the old repo on this machine and on GitHub only when nothing else in that repo still imports them. Do not delete the GitHub repository. Do not force-push. If the archive copy fails, do not delete.
8. Update this work order with what landed, the archive path, and the GitHub deletion. Correct only row 68 of `Documentation/00-architecture/Old-Repo-Migration-Matrix.md` for `mysql` / `db-facts`.

---

## 4. Non-goals

- Do not overwrite Energy BLE, `host_desks.py`, `jobs.py`, `master-key.env`, the website, or Android apps.
- Do not port `execute`, cron inserts, identity counts, or EcoFlow/host fact lines.
- Do not copy `rootmc_economy.py`. Do not build the economy brief, a Discord post, or desk-data-reader.
- Do not open a second top-level domain. Other agents' files stay untouched.
- Sends, speaker playback, OBS, hardware switching, deletion of live Ecosystem files, and cloud spend stay off.

---

## 5. Key file / path reference

| Path | Role |
|------|------|
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/System/MysqlDesk/scripts` | Server code. Package name `MysqlDesk`. |
| `2 - RootRecord-Database/System/MysqlDesk/` | Last facts file. Runtime. Not imported from the old repo. |
| `2 - RootRecord-Database/Logs/System/MysqlDesk/` | Log line only. |
| `System/MysqlDesk/lib/envload.py` | Allowlist loader for the key names in §2.1. |
| `System/MysqlDesk/scripts/mysql_desk.py` | Read-only facts CLI. |
| `/home/rootrecord/master/master-key.env` | Only secret file. Not edited by this work order. |
| `old ollama/old skills/mysql/` | Old mysql skill. Archive, then delete if unshared. |
| `old ollama/old skills/database/db-facts/` | Old db-facts skill. Archive, then delete if unshared. |
| `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/` | Archive root for those two paths. |
| `Documentation/00-architecture/Old-Repo-Migration-Matrix.md` | Row 68, mysql / db-facts note only, after phase 4. |

---

## 6. Open items

**Additional requirements:**

- Alexander puts the allowlisted key names into `master-key.env` before any live Shockbyte read. This work order does not write those values.
- Shared file left: `mysql/scripts/mysql.py`. `desk-data-reader/desk/live/mysql.py` symlinks to it.

---

## 7. Notes & constraints

- No force-push. Do not delete the GitHub repository `Solar-Pacific-RootRecord-Server`.
- Secrets stay out of git. The plan and this file list key names, not values.
- Prefer small reversible steps. New periodic jobs stay off. Do not edit `jobs.py`.
- Sign-off gates: live Shockbyte read, sends, speaker playback, OBS, hardware switching, deletion of live Ecosystem files, and cloud spend. Phase 4 archive-then-delete of this function's old files is already ordered, with the shared-file pause in §6.
- Proof, and the only test to run before a live read: `python3 mysql_desk.py facts` with the allowlist empty. Expect `{"ok": false, "error": "missing-credentials", "local_3306": false, "shockbyte": false}` and no PyMySQL import.

---

*Work order prepared 2026-09-30 HST. Update status when closed.*

---

## Archive / location note

This draft stays here:

```text
Documentation/06-development/Work-Orders/drafts/MySQL_desk_facts_Work_Order_WO-MIG-28-2026-09-29.md
```

Do not promote it onto the active index.

---

## Result

Landed 2026-09-30. Read-only client at `System/MysqlDesk/scripts/mysql_desk.py` with `System/MysqlDesk/lib/envload.py`. `python3 mysql_desk.py facts` with the allowlist empty wrote `facts-last.json` and one log line: `ok=False`, `error=missing-credentials`, both targets false. PyMySQL was not imported. No Shockbyte socket. No `jobs.py` edit.

Archive (checksums matched the old tree before deletion):

- `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/mysql/`
- `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/database/db-facts/`

Removed on GitHub `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server` branch `online-safe-20260920` commit `0e3ebe2b`: all of `database/db-facts/`, plus `mysql/DAILY.md`, `mysql/INDEX.md`, `mysql/SKILL.md`, and `mysql/references/migrate.md`. `origin/main` (`1dcee662`) does not contain those paths. The repository was not deleted.

Left in the old repo: `mysql/scripts/mysql.py`. `desk-data-reader/desk/live/mysql.py` is a symlink to it. `live-data-pages` is already gone from this branch (`577ad693`), so it does not import `db_facts` here. The `origin/ns/apps/core/services` shims still point at `~/.ollama/skills/mysql` and `~/.ollama/skills/db-facts`, which are not this tree and were already absent.
