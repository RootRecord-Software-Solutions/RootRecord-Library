# Proposal — Auto-recovery for weather and relay after a mid-session crash

| Field | Value |
| --- | --- |
| **Date (HST)** | 2026-09-29 |
| **State** | **LANDED / VERIFY PENDING (next poller start)** — approved by Alexander 2026-09-29 |
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

## Implementation (2026-09-29 ~04:00 HST)
- `Automations/scripts/supervise-services.sh` (new): for weather and the relay it uses the same `pgrep` patterns as `ensure-weather-poller.sh` / `ensure-relay.sh` and, if a service is dead, runs that same ensure script (a WARN line). Backoff: at most 3 respawns per 30 min per service, then one `BLOCKED` line and no more tries until the service is seen alive again. State is kept in `$XDG_RUNTIME_DIR/rootrecord-supervisor/` (tmpfs, not in git). `--dry-run` / `--check` only detects.
- `jobs.py`: new EVERY_SECONDS job `service_supervisor` (every 300 s, enabled). jobs.py is read at poller start, so this is active only from the **next poller start**.
- Commits: Pacific `5353e1f` (script, 04:02:54) · `52573e7` (jobs.py, 04:06:53). Backup `/home/rootrecord/Database/GITHUB/g3-proposals-impl.bak-20260929-035910/`.
- Test: [07-testing record](../07-testing/2026-09-29-service-supervisor-dry-run.md). Dry run: both alive, and a simulated death gave 3× WOULD-RESPAWN, then WOULD-BLOCK. No live process was killed. Evidence `2 - RootRecord-Database/Logs/Migration/g3-proposals-impl-evidence-20260929T140900Z.md`.
- Still to verify (approved window): after the next poller start, one `job:service_supervisor` line every 5 min reports both alive. The kill-and-respawn test stays as proposed.
