# Test record — Weather + relay supervisor (detection / backoff dry run)

| Field | Value |
| --- | --- |
| **Date / time (HST)** | 2026-09-29 03:59:54–04:00:10 HST |
| **Tester** | executor agent (g3-proposals-impl) |
| **Change under test** | Pacific `Automations/scripts/supervise-services.sh` + jobs.py EVERY_SECONDS `service_supervisor` (300 s). Proposal: [08-ideas auto-recovery](../08-ideas/2026-09-29-weather-relay-auto-recovery.md) |
| **State** | **PASS** (logic, dry run) · live effect **VERIFY PENDING (next poller start)** |
| **Evidence** | `2 - RootRecord-Database/Logs/Migration/g3-proposals-impl-evidence-20260929T140900Z.md` |
| **Commits** | Pacific `5353e1f` (script) · `52573e7` (jobs.py) |
| **Backup** | `/home/rootrecord/Database/GITHUB/g3-proposals-impl.bak-20260929-035910/` |

## What was tested
The alive/dead detection and the 3-per-30-min backoff. No process was killed and nothing was started.

## How (exact commands / procedure)

```bash
S=".../Automations/scripts/supervise-services.sh"
bash "$S" --dry-run                                      # live detection, no state written
T=$(mktemp -d /tmp/rr-supervisor-test.XXXX)
for i in 1 2 3 4 5; do bash "$S" --dry-run --pretend-dead weather --state-dir "$T"; done
bash "$S" --dry-run --pretend-dead relay --state-dir "$T"
bash "$S" --dry-run --state-dir "$T"                    # alive again -> block clears
bash "$S" --pretend-dead weather                        # guard: must refuse without --dry-run
rm -rf "$T"
```

## Pass criteria (written before running)
1. Live dry run reports both weather and relay **alive**, with their PIDs. Nothing is started, and no live state dir is created.
2. Simulated death gives WOULD-RESPAWN for attempts 1–3, then WOULD-BLOCK, then BLOCKED with no retry.
3. Once the service is seen alive again, the block clears. `--pretend-dead` without `--dry-run` is refused.

## Result
1. `weather alive pid=106159`, `relay alive pid=105964`, rc 0. `/run/user/1000/rootrecord-supervisor` was not created. **PASS**
2. Attempts 1/3, 2/3 and 3/3 gave WOULD-RESPAWN, then `WOULD-BLOCK (3 restarts in last 1800s >= 3)`, then `BLOCKED since 2026-09-29T03:59:54-10:00`. Relay attempt 1/3 was reported separately. **PASS**
3. `weather seen alive — BLOCKED cleared`. The guard exited rc 2. **PASS**
4. The poller's exact job command (`bash -lc 'bash ".../supervise-services.sh" --dry-run'`) gave both alive.

## Resource impact

| When | Load (1/5/15) | MemAvailable | Swap used | Peak RSS |
| --- | --- | --- | --- | --- |
| before | 1.87 / 1.51 / 1.41 | 7399 MB | not recorded | not recorded (a few pgrep calls, < 1 s) |
| after | not recorded | not recorded | not recorded | — |

## Cleanup confirmation
- [x] no test process left (the temp state dir `/tmp/rr-supervisor-test.*` was removed)
- [x] no ports or locks touched
- [x] no model involved

## Open items / caveats
- It runs live only from the next poller start (jobs.py is read at start). Expect one `job:service_supervisor` RUN line and two "alive" lines every 5 min in `automations_current.log`.
- A real respawn briefly holds the scheduler thread (≤ ~4 s: the ensure scripts sleep 1 s and 3 s).
- Kill-and-respawn test: still needs an approved window.
