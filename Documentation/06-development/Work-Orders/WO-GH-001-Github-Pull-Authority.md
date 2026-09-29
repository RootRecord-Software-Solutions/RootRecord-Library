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
