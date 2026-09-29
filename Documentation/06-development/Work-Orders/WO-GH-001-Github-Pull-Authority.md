# WO-GH-001 — GitHub Pull Authority & Timer Policy

| Field | Value |
|-------|--------|
| **Priority** | P2 |
| **Status** | Draft |
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

## Acceptance criteria

1. Single written authority choice (A/B/C) with date and operator name
2. Non-authority path disabled or clearly marked inactive
3. Agent context / REPOS docs updated so agents do not suggest dual timers
4. No surprise pulls after the decision for at least one observed cycle window

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
- Open: pick the authority (options above) and mark the other path inactive. No script was changed.
