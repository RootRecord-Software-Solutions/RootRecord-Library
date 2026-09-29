# Proposal — Pacific copy of `npu-status.sh`

| Field | Value |
| --- | --- |
| **Date (HST)** | 2026-09-29 |
| **State** | **LANDED / VERIFY PENDING** — idle run PASS; lock-held run pending (not poller-dependent) |
| **Grounding** | `2 - RootRecord-Database/Logs/Migration/g3-npu-flm-evidence-20260929T125429Z.md`: "G2 `~/.ollama/skills/plumbing/scripts/npu-status.sh` (read-only; there is no Pacific copy)" |
| **Needs sign-off from** | Alexander |

## Problem
The only NPU status helper lives in G2. It also keeps the G2 `single-flight.sh` in use.

## Proposal
Copy it to Pacific `System/scripts/plumbing/npu-status.sh` (the G2 original stays **KEPT**). Point it at the Pacific `single-flight.sh` and the canonical `Github/plumbing/state`. Report the on-demand FLM model correctly: when idle, "no `flm serve`, :52625 closed" is the normal state.

## Resource impact / safety
Read-only (accel0, packages, lock state). No model load.

## How it would be tested
Run it once while idle (expect IDLE, no server), then once during an approved on-demand request (expect lock held).

## Implementation (2026-09-29 ~04:00 HST)
- Copied to Pacific `System/scripts/plumbing/npu-status.sh`. The G2 original is **KEPT** and unchanged. The copy calls the Pacific `single-flight.sh` (same folder) with `RR_PLUMBING_STATE` = `2 - RootRecord-Database/Github/plumbing/state`, and adds an FLM line: `IDLE (on demand): no flm serve, :52625 closed — normal`.
- Commit: Pacific `5353e1f` (04:02:54). No jobs.py change.
- Test: [07-testing record](../07-testing/2026-09-29-npu-status-pacific-copy.md). The idle run at 04:00:26 gave accel0 present, XRT 2.25.0 packages, lock IDLE, and FLM idle (normal). **PASS.** Evidence `2 - RootRecord-Database/Logs/Migration/g3-proposals-impl-evidence-20260929T140900Z.md`.
- Pending: one run during an approved on-demand request (expect BUSY + flm serve).
