# Test record — OOM incident: resident FLM warmup (llama3.2:3b)

| Field | Value |
| --- | --- |
| **Date / time (HST)** | 2026-09-29 03:10–03:13 HST (incident); fix 03:13–03:15 HST |
| **Change under test** | `flm_npu_warmup` ON_BOOT job at poller start (surfaced during the Title-case rename restart) |
| **State** | **FAIL → fixed; fix PASS** |
| **Evidence** | `2 - RootRecord-Database/Logs/Migration/g3-titlecase-rename-evidence-20260929T130752Z.md` §4; WO-SRV entry "03:10–03:13 HST — OOM restart loop" |
| **Commits** | Pacific `ff298b2` (03:13, `flm-warmup.sh` non-resident by default; `FLM_WARMUP_RESIDENT=1` opt-in) · `3039c3f` (03:15, `run-infer.sh`/`run-ollama.sh` `ollama run --keepalive ${OLLAMA_KEEP_ALIVE:-0}`) |
| **Backup** | `/home/rootrecord/Database/GITHUB/g3-oom-flm.bak-20260929-031323/` |

## What happened (FAIL)
At every poller start, the warmup ran `flm serve llama3.2:3b`, which mapped about 10 GB (9.6 GB shmem). The kernel OOM-killed the whole poller unit **11 times** between 03:10 and 03:13 HST (NRestarts 11).

## Fix
- Warmup is non-resident by default and only loads a model with `FLM_WARMUP_RESIDENT=1`.
- Ollama CLI calls unload right after the reply (`--keepalive 0`).
- Later (03:29) the default model became `llama3.2:1b` on demand (see the [1b on-demand record](./2026-09-29-npu-llama3.2-1b-on-demand.md)).

## Pass criteria (fix)
The poller stays up with no further OOM restarts, and no model stays resident.

## Result (fix PASS)
- Poller stable since 03:13:28 HST (PID 105444).
- Read-only check at 03:38 HST: MainPID 105444, NRestarts 11 (unchanged since the fix).

## Resource impact
About 10 GB per warmup attempt on a ~14 GB desk, which exhausted memory. Recorded as the reason for the test-safety policy (no resident models).

## Open items
- `OLLAMA_KEEP_ALIVE=0` in `ollama.service`: **BLOCKED** (needs sudo). The server default is still 5m for non-CLI callers.
