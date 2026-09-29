# Proposal — Auto-recovery for weather and relay after a mid-session crash

| Field | Value |
| --- | --- |
| **Date (HST)** | 2026-09-29 |
| **State** | PROPOSED |
| **Grounding** | `2 - RootRecord-Database/Logs/Migration/g3-followups-evidence-20260929T124741Z.md` item 2; relay crashes at 01:39:21 and 02:08:38 HST (`g3-weather-archive-evidence-20260929T115429Z.md`, `g3-poller-viewer-evidence-20260929T121959Z.md`) |
| **Needs sign-off from** | Alexander (`jobs.py` change + poller restart to take effect) |

## Problem (measured)
`weather_poller` and `council_relay` are ON_BOOT jobs, so a crash mid-session is not re-ensured until the next poller start. The relay was down from 01:39 until the 01:50 boot job.

## Proposal
Add low-frequency periodic ensure jobs (for example every 5 min) that call the existing single-instance-safe `Weather/scripts/ensure-weather-poller.sh` and `Communications/telegram/scripts/ensure-relay.sh`. Both already match their process first, so a live instance is left alone. Log each respawn as a WARN line.

## Scope and non-goals
- Docs/proposal only. `jobs.py` is not touched without approval.
- No change to relay quiet mode (`RR_RELAY_REPLIES=0` stays the default).

## Resource impact / safety
Each ensure call is a `pgrep`. A respawn costs one process start. Add a backoff cap (e.g. 3 respawns per hour) so a crash loop cannot storm.

## How it would be tested
Once, on an approved window: kill the test weather process, then confirm exactly one respawn within one interval and no duplicates.
