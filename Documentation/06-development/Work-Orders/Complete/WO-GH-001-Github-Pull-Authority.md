# WO-GH-001 — GitHub Pull Authority & Timer Policy

| Field | Value |
|-------|--------|
| **Priority** | P2 |
| **Status** | **COMPLETE** — Option B, Alexander, 2026-09-29 ~22:00 HST. Pacific `github_sync_all` is the only automatic pull. |
| **Target** | Policy between Core-Processor auto-pull and Pacific `Github/` |
| **Depends on** | Private-Repos-Feature-Map § Core-Processor; operator preference |
| **Related** | Migration priority P2 System/Github pull timer |

## Goal

Decide and document **one authority** for automatic repository pulls so Pacific and Core-Processor do not race, double-pull, or leave operators unsure which timer is live.

## Options (pick one with operator)

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A — Core-Processor owns** | Systemd timer + auto-pull-server remains sole puller | Already private & tested | Pacific `Github/` stays thin/docs-only |
| **B — Pacific owns** | Jobs under `Github/` + poller schedule | Everything under G3 domain layout | Must retire or disable Core-Processor timer |
| **C — Split by repo** | Critical ecosystem repos via Core-Processor; experimental via Pacific | Flexible | Harder to remember; dual ops |

## Scope (in)

- Written decision record in Library
- Inventory of which repos are auto-pulled today
- Disable or document the non-authority path so it cannot silently re-enable
- Optional: Pacific `Github/README.md` states “pulls deferred to Core-Processor” (if A)

## Scope (out)

- Changing git credentials or deploy keys in this WO
- Force-push / rewrite history automation
- CI/CD beyond pull-to-disk

## Decision

**Option B — Pacific owns automatic pull.** Operator: Alexander. Date: 2026-09-29.

| Path | Role |
| --- | --- |
| `github_sync_all` every 5 s | Automatic authority. Enabled rows: `ecosystem`, `skills`. |
| Core-Processor timer | Not present. User timers on this desk at 21:58 HST were firmware-notifier, launchpadlib-cache-clean, and ubuntu-insights only. |
| `Pull.sh` / `Push.sh` | Manual scripts. Headers say they are not timers. They are not scheduled. |

## Acceptance criteria

1. [x] Single written authority choice (B) with date and operator name
2. [x] Non-authority path marked inactive as a timer (`Pull.sh`, `Push.sh` headers). No Core-Processor unit to disable.
3. [x] Ava, Bruce, and Carly `CONTEXT/REPOS.md` say not to suggest a second pull timer. Pacific `Github/README.md` states the same.
4. [x] One observed cycle after this decision: 2026-09-29 22:01:03 HST. `github_sync_all` committed and pushed `ecosystem`, fetched `skills`, and no new file appeared under `Logs/Github/Manual/`.

## Risks

- Disabling the wrong timer leaves servers stale
- Pull storms if both remain on
- Private repo tokens assumed present without verification

## Notes

Default recommendation if operator is undecided: **Option A** until Pacific Energy/Weather imports stabilize — reduce moving parts on the solar node.

## Open conflict — second pull authority (recorded 2026-09-29)

- **Automated:** Pacific `github_sync_all` (`Github/scripts/sync-all.sh` → `push-repo-once.sh`, `interval_sec=5`) fetches, merges and pushes pacific, database, library and skills.
- **Manual:** `/home/rootrecord/RootRecord-Ecosystem/Pull.sh` ("RootRecord Ecosystem Smart Pull") fetches and merges Pacific, Database and Library, logging to `2 - RootRecord-Database/Logs/Github/Manual/` (latest `pull-20260928-232443.log`). A matching manual `Push.sh` logs `push-*.log` there too.
- Both act on the same three checkouts, so the manual run is a second pull authority competing with the 5 s auto-sync. No Core-Processor pull timer or unit was found on the desk (2026-09-29 check of systemd user and system unit files and timers), so today the conflict is Pacific auto-sync vs manual Smart Pull, not Core-Processor.
- Resolved 2026-09-29: Option B. The 21:57:31 HST cycle fetched and pushed `ecosystem` and fetched `skills` with no second puller in that window.
