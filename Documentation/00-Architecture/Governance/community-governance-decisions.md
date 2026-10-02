# Community governance decisions

Source: G1 `governance/governance-daily/scripts/governance.py`, plus the migrate notes under `governance-daily`, `governance-boot`, and `governance-self-update`. The jobs were not ported. `governance-daily` stays **OUT** of the Pacific scheduler.

Evidence label: **Historical** for the old scheduler. The gate below is the decision that was kept.

## Flags

Defaults, written only if a flags file was missing:

| Flag | Default |
| --- | --- |
| `community_governance` | off |
| `self_update` | off |
| `cursor_min_free_pct` | 25 (clamped 1–90) |
| `cursor_context_free_pct` | unknown (`null`) |
| `program_name` | RootRecord governance |

If `community_governance` is off, the daily run records `community_governance_off` and returns. It does not write proposal pages and it does not queue Cursor.

## What a passing wish was

Over a 26-hour window, a slug passed when at least two people asked for it and they were a strict majority of the people who spoke (`support * 2 > people`). A pass wrote a proposal page and a conclusion page. Those pages were drafts. They did not change the live host until a conclusion was filed and self-update was on.

## Self-update gate

`cursor_may_run` refuses unless every check passes:

1. `community_governance` is on, else `governance_off`.
2. `self_update` is on, else `self_update_off`.
3. Origin uptime is at least 3600 seconds, else `boot_grace`.
4. Free context is a known number, else `context_unknown`. Unknown context is queued, never auto-run.
5. Free context is greater than `cursor_min_free_pct` (default 25), else `low_context`.

Boot calls the daily tally with self-update forced off. The hourly self-update drain is a no-op when the gate fails.

When the gate did pass, the old hook still did not spawn Cursor. The job status was `held_for_sdk` ("do not spawn Cursor from origin"). That shutoff stays. This migration does not turn the program on and does not add a scheduler job.

## Migrate notes

Each skill was marked **moved** out of `apps/core` crons (`governance_daily.py`, `governance_boot.py`, `governance_self_update.py`, and the `governance.py` service). The notes say do not restore the old body. Shared `apps.core` was left in place. It is not part of this packet.
