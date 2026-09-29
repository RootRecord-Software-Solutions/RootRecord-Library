# Proposal — Pacific copy of `npu-status.sh`

| Field | Value |
| --- | --- |
| **Date (HST)** | 2026-09-29 |
| **State** | PROPOSED |
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
