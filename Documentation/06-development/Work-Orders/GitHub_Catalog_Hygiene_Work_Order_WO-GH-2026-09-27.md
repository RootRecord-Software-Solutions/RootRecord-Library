# WORK ORDER — GitHub Catalog Hygiene & Non-Canonical Cleanup

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-GH-2026-09-27 |
| **Status** | **IN PROGRESS** — desk publishes `ecosystem` (inplace) and `pacific`, `database`, `library` (mirror). `skills` stays on. `website` and `mainland` stay disabled |
| **Updated** | 2026-09-30 02:35 HST — the five enabled rows stay on. Skills HEAD at 02:16 was `6483586`. Website and mainland stay disabled. See `Documentation/01-operations/2026-09-30-whats-left-for-alexander.md`. |

**Scope:** Catalog + auto-sync under Pacific; org remotes for canonical three; retire non-canonical clutter when convenient.

**Desk correction, 2026-09-30 00:05 HST:** `/home/rootrecord/RootRecord-Ecosystem` is still one git repository. Do not put a nested `.git` in Pacific, Database, or Library. Those three publish as `mirror` rows from `/home/rootrecord/Database/GITHUB/worktrees/`. Do not retire the `skills` row without Alexander's sign-off. `Pull.sh` stays as the manual pull path.

---

## Done

- [x] Github scripts imported to `…/Pacific/Github/scripts/`
- [x] `repos.conf` tab-separated. As of 23:45 HST the enabled rows are `ecosystem` (inplace) plus `pacific`, `database`, and `library` (mirror publishes of the live subfolders) and `skills`. `website` and `mainland` stay disabled.
- [x] jobs.py → Pacific `setup-all-remotes` + `sync-all`
- [x] Poller cycle publishes `ecosystem`, `pacific`, `database`, `library`, and `skills`. Evidence 2026-09-29 ~23:49–23:52 HST: Pacific `9d2ce23` (23 files), Library `fa93b0c` (3 files), Database `b8e904d` (16 files), Ecosystem `b4b9739` (4 files).

## Operator pull workflow clarification — 2026-09-29

- **Resolved:** the human/operator `/home/rootrecord/RootRecord-Ecosystem/Pull.sh` workflow is intentional and remains available for Bruce/operator use.
- It is **not** a migration failure or an automation conflict. The 5-second `github_sync_all` job and the human `Pull.sh` workflow serve different operator/automation use cases and are allowed to coexist.
- No change was made to remove, disable, or supersede `Pull.sh`.

## Documentation sweep refresh — 2026-09-29 ~01:11 HST

- The human `Pull.sh` workflow remains explicitly resolved and retained.
- The Pacific poller source now uses the canonical Database root; this does not alter the operator pull workflow.
- `Github/scripts/common.sh` still carries an old default Database root and remains a small cleanup item; it is not a reason to remove or disable `Pull.sh`.

## Refresh — 2026-09-29 ~01:37 HST

- `Github/scripts/common.sh` DATABASE_ROOT default → canonical — **LANDED** (Pacific `75d86f2`). `BAK_ROOT` intentionally stays `/home/rootrecord/Database/GITHUB` (flags/worktrees/backups outside the auto-synced Database tree; matches the stack-reload scripts).
- Live logs untracked in the Database repo (`eabe62e`) to stop per-sync churn; hourly archives remain synced.
- G2 retirements reverted (skills `1dcee66`); the `skills` catalog entry stays. **Standing rule (Alexander, 2026-09-29):** never retire or delete G2/legacy code. "No live references" is not grounds — unimported automations (e.g. the older repo `rootrecordsoftwaresolutions/old`) may need it. Retirement happens only with Alexander's explicit sign-off.
- Needs decision: `push-repo-once.sh` `is_runtime_code_tree` still arms a poller stack reload on `~/.ollama/skills` pulls. Survey: `2 - RootRecord-Database/Logs/Migration/g3-residual-path-survey-20260929T113523Z.md`.
- *~02:08 HST:* `push-repo-once.sh` no longer treats `~/.ollama/skills` pulls as runtime code (Pacific `abc78b2`) — G2 syncs never restart the poller. Note: the weather daemon rewrites tracked `Pacific/Weather/reports/README.md` each report cycle (sync churn; decision pending).
- *02:23 HST (Alexander-approved):* `push-repo-once.sh` `pull_is_docs_only` — a pull whose changed files are all `*.md`/`*.markdown`/`README*` no longer arms a poller stack reload; any code/config file (or empty/unknown diff) reloads exactly as before (Pacific `31fd21e`; tested on eb8f465 docs range = skip, 884c832/89a8d6d/mixed = reload).

## Remaining

- [ ] Enable website when a mirror worktree exists outside this umbrella. `repos.conf` still points the disabled row at `~/.ollama/skills/website/site`. Do not enable that path inside the snapshot.
- [ ] Enable mainland when path is a real git clone
- [ ] Delete non-canonical user-account Library repo if still present — 2026-09-29 ~00:28 HST desk check: `git ls-remote git@github.com:rootrecordsoftwaresolutions/RootRecord-Library.git` → `ERROR: Repository not found` (control: org Library returned `main` = `e28b1da`); the public URL also returns 404. Likely already deleted, but a private repo the desk key cannot read looks the same — confirm in the GitHub account before ticking.
- [ ] Optional: stop publishing skills to the historical Solar-Pacific remote when G2 is fully retired — **not yet.** Live processes at 22:13 HST are already Pacific (poller, BLE owner, relay, globe, weather). The `skills` row stays enabled because Alexander has not signed off G2 retirement. Do not set `skills` to 0 from this order alone.

## Catalog home

```text
/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server/Github/scripts/repos.conf
```

Token: `master-key.env` — never commit.


## Static Catalog Audit — 2026-09-28

- Direct Pacific inspection of `Github/scripts/repos.conf` confirms the enabled catalog entries are Pacific, Database, Library, and the historical skills repository; Website and mainland remain explicitly disabled.
- The two `.ollama/skills` references in `repos.conf` are the intentional `skills` catalog path and disabled Website/Mainland paths, not active Pacific runtime executable references.
- Direct inspection of `Github/scripts/setup-all-remotes.sh` and `Github/scripts/sync-all.sh` found no embedded `/home/rootrecord/.ollama/skills/` or `~/.ollama/skills/` executable references.
- Representative current source SHAs: `repos.conf` `d3a24a3133c51117084c7440473b58e030436424`; `setup-all-remotes.sh` `22253d003c01488f618f195d7a3a983dbfd51f46`; `sync-all.sh` `57e2c7b2a570ba6340cfcb29c578e765727ec001`.
- Desk re-read at Pacific HEAD `f70cc27`: `sync-all.sh` blob `8f125ed361b4f4f5d3581803f59266a9c31d7f2c` (last changed in commit `9d0d059`, "Prevent database sync from reloading poller stack"); the post-pull stack reload now lives in `push-repo-once.sh` `mark_code_pulled`. `jobs.py` `github_sync_all` `interval_sec` changed from 300 to 5 in commit `494bf8b`. A later comment/unused-variable cleanup of `sync-all.sh` header supersedes that blob.
- This is a static catalog audit only. It does not enable Website/Mainland or authorize removal of the historical skills catalog before the remaining WO-GH prerequisites are satisfied.

## Refresh — 2026-09-29 ~03:45 HST (truth-gated)

- Pacific `Github/` auto-sync **PASS** after the 02:28 HST reboot (Database commits since boot; Pacific/Library/skills clean, no `index.lock` — `g3-post-reboot-evidence-20260929T123313Z.md`), and it is still committing after the 03:09 HST Title-case restart.
- Docs-only pulls no longer reload the stack — **PASS** (`31fd21e`; [test record](../../07-testing/2026-09-29-poller-dashboard-single-window.md)).
- Database `.gitignore` follows the Title-case names (`/Github/logs/`, `/Github/plumbing/state/`, `/Weather/`, `/RootRecord/`, `/Energy/state/`, `/Energy/ports/`; Database `92bd69c`). `BAK_ROOT` stays `/home/rootrecord/Database/GITHUB` (**KEPT**, outside the auto-synced tree).
- `skills` catalog row: **KEPT** (G2 legacy files are retired only with Alexander sign-off).
- Website/mainland: still disabled (**BLOCKED** on worktree/clone prerequisites above).
- Security items **BLOCKED** (unremediated, need Alexander): camera stills in the public Database repo; `CONNECTION.json` in Pacific history (`6328af6`); G2 still tracks `a-eyes/store/CONNECTION.json`. History rewrite or untracking needs explicit approval.
- Test records: [`Documentation/07-testing/`](../../07-testing/README.md).

## Migration pass — 2026-09-29 ~13:40 HST

- Database `.gitignore`: added `/Geology/Earthquakes/*.db`, `*.db-wal`, `*.db-shm` (quake backfill SQLite stays local) and the cam stills `Geology/Volcanoes/Cams/*.jpg` stay untracked. `Geology/*-last.json` + `Daily/*.jsonl` are tracked (small text); once `RR_GEOLOGY=1` they change every ~5 min → auto-sync commit churn (**sign-off** item).
- New tracked Pacific paths: `Geology/scripts/*.py`, `Energy/scripts/sun_times.py`, `System/scripts/uptime_log.py`, `Media/Video/{README.md,scripts/mp4_converter.py}`. Commits made by desk auto-sync only (no manual git writes).
- Old repos (`Solar-Pacific-RootRecord-Server-Old`, `old`): read via shallow `/tmp` clones, deleted afterwards; **no commits/pushes**. The G1 README status list was not edited — the [Old-Repo-Migration-Matrix](../../00-architecture/Old-Repo-Migration-Matrix.md) is the current comparison.
- Addendum ~14:10 HST: Database `.gitignore` += `/Reports/News/**/*.db`, `/Reports/News/**/*.db-wal`, `/Reports/News/**/*.db-shm` (Hawaiʻi news SQLite stays local) and `/System/network/Daily/` (net byte-counter JSONL, ~290 lines/day). Tracked when written: `Reports/News/hawaii/hawaii-news-last.json`, `System/network/net-last.json`, `System/security/security-last.json` (counts only; no IPs / usernames) — tracking vs ignore is a sign-off item. New tracked Pacific paths: `Communications/web-facts/`, `Reports/News/`, `System/scripts/host_desks.py`.
- Addendum ~14:40 HST (breadth batch 5): Database `.gitignore` is **unchanged**. New outputs `Weather/Hawai'i/official/*` and `Weather/Hawai'i/hurricanes/global/*` fall under the existing `/Weather/` ignore. `Reports/board/daily-reports-due.json` (report_board) and `Reports/News/hawaii/hawaii-news-last.json` would be **tracked** once written for real. So far only temp roots were used (sign-off: keep tracked or ignore). No git writes by the agent (auto-sync commits).

## State at pause — 2026-09-29 16:25 HST

- **Mainland:** the desk path `1 - Servers/2 - RootRecord-US-Mainland-Server/` is now a real git clone, so the desk side of "Enable mainland when path is a real git clone" is met. The `repos.conf` row still points at the empty G2 folder and stays disabled: **BLOCKED on sign-off** (exact row in [US-Mainland-Server](../../00-architecture/US-Mainland-Server.md)). The uncommitted Mainland changes (units, crontab, overlay, `fallback/`) wait on that.
- **`6 - Android Development`:** not a repo and not in `repos.conf`, `Push.sh` or `Pull.sh`. Its `.gitignore` covers keystores and secrets (24/24 checked). [Inventory](../../00-architecture/Android-Apps-Inventory.md).
- **Security (sign-off):** Android signing material sits in GitHub repos that aren't private (details kept out of this public page); PAT rotation; the earlier camera-stills and `CONNECTION.json` items.
- **Tracking decisions (sign-off):** `Reports/board/daily-reports-due.json` tracked vs ignored; `git rm --cached` of generated reports.
- Library desk auto-sync kept committing through the afternoon (auto commits only, no manual git writes).
