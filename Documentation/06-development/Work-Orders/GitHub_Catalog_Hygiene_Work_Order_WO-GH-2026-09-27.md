# WORK ORDER — GitHub Catalog Hygiene & Non-Canonical Cleanup

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-GH-2026-09-27 |
| **Status** | **IN PROGRESS** — Pacific `Github/` sync **LIVE**; website/mainland still disabled |
| **Updated** | 2026-09-29 ~01:37 HST |

**Scope:** Catalog + auto-sync under Pacific; org remotes for canonical three; retire non-canonical clutter when convenient.

---

## Done

- [x] Github scripts imported to `…/Pacific/Github/scripts/`
- [x] `repos.conf` tab-separated: pacific, database, library, skills (enabled); website, mainland (disabled)
- [x] jobs.py → Pacific `setup-all-remotes` + `sync-all`
- [x] Poller cycle fetches org pacific / database / library + legacy skills without fail storms

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

## Remaining

- [ ] Enable website when mirror worktree exists under `Database/GITHUB/worktrees/website`
- [ ] Enable mainland when path is a real git clone
- [ ] Delete non-canonical user-account Library repo if still present — 2026-09-29 ~00:28 HST desk check: `git ls-remote git@github.com:rootrecordsoftwaresolutions/RootRecord-Library.git` → `ERROR: Repository not found` (control: org Library returned `main` = `e28b1da`); the public URL also returns 404. Likely already deleted, but a private repo the desk key cannot read looks the same — confirm in the GitHub account before ticking.
- [ ] Optional: stop publishing skills to historical Solar-Pacific remote when G2 is fully retired — 2026-09-29 assessment: **not yet.** *Update ~00:52 HST:* both units were repointed to Pacific and PASS (00:33 / 00:35 HST), and no process now runs from `~/.ollama/skills`. Still pending G3: the residual G2 executables — `a-eyes` `grab_frame.py` and timelapse, the Telegram relay, plumbing `single-flight.sh` / `run-*.sh` / `*-warmup.sh`, and Energy actions. Until they are retired, the `skills` row must keep publishing. The `skills` row (enabled=1) is also what publishes the retirement `MIGRATED.md` markers (last push `83e10bd`). Prerequisites: both unit repoints done, remaining G2 executables retired, then set `skills` enabled=0 in Pacific `Github/scripts/repos.conf`.

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
