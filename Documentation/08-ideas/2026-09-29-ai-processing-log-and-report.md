# Proposal — AI processing log and daily report

| Field | Value |
| --- | --- |
| **Date (HST)** | 2026-09-29 |
| **State** | PROPOSED |
| **Grounding** | [NPU on-demand test record](../07-testing/2026-09-29-npu-llama3.2-1b-on-demand.md) (latency and peak RSS measured by hand); NPU/FLM evidence finding that FLM logs record full request bodies (moved to git-ignored `Logs/AI/FLM/`) |
| **Needs sign-off from** | Alexander |

## Problem
Nothing records inference activity (backend, model, latency, memory, rc) in a structured way. Tonight's numbers were collected by hand, and the only FLM log holds full prompt text, which is private.

## Proposal
- `run-infer.sh` appends one metadata-only JSON line per request to `2 - RootRecord-Database/Logs/AI/inference.jsonl` (git-ignored): time HST, caller, backend (FLM/NPU or Ollama fallback), model, cold start yes/no, latency, peak FLM RSS, minimum MemAvailable, rc. **No prompt or reply text.**
- A Reports job rolls it up into a daily `AI processing` section: counts, p50/max latency, fallbacks, memory minimums.

## Resource impact / safety
Append-only small file. No resident process.

## How it would be tested
One approved on-demand request, then confirm exactly one metadata line with no text fields.
