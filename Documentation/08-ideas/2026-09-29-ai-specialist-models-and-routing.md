# Proposal — AI specialist models and keyword router

| Field | Value |
| --- | --- |
| **Date (HST)** | 2026-09-29 |
| **Proposed by** | Alexander (operator request); built by agent pass g3-specialists |
| **State** | **LANDED / gated.** Specialist models, router, config and tests landed. The `run-infer.sh` hook LANDED 2026-09-29 ~04:56 HST, OFF unless `RR_SPECIALIST_ROUTING=1` (flag-off byte-identical; see the design doc §4) |
| **Grounding** | Team constitution §3 ("specialists over generalists"); `run-infer.sh` / relay fall back to `*-telegram` models that were missing from `ollama list` (overnight worklog sign-off list); G2 lane catalog `old ollama/agents/lanes.conf` |
| **Needs sign-off from** | Alexander (to apply the hook to `run-infer.sh` and switch the gate on) |
| **Related WO** | none yet |
| **Design doc** | [AI-Specialist-Models-and-Routing.md](../00-architecture/AI-Specialist-Models-and-Routing.md) |

## Problem (measured)
Every request goes to one generic prompt: FLM `llama3.2:1b` with a two-line system prompt, or an Ollama `*-telegram` persona that did not exist on the desk (the models were missing from `ollama list` until this pass). Small models answer better with a focused, grounded prompt.

## Proposal
- 10 isolated specialists, one Modelfile each (`Database/AI/Ollama/Modelfiles/Specialists/`): `rr-exec`, `rr-reason`, `rr-energy`, `rr-weather`, `rr-system`, `rr-security`, `rr-cameras`, `rr-council-ava`, `rr-council-bruce`, `rr-council-carly`. All built on installed small models.
- The three `*-telegram` persona models restored from their G2 Modelfiles (`Modelfiles/Production/`).
- `System/scripts/plumbing/route-specialist.py` scores each request against `System/config/specialist-routes.json`. It outputs a specialist and a confidence score, falls back to the voice's persona model below the threshold, and logs metadata-only JSONL.
- FLM route: the specialist's SYSTEM block goes to the NPU base model as the system message.
- The hook into `run-infer.sh` is written in the design doc (§4). It is not applied.

## Scope and non-goals
In: models on disk, router, config, tests, docs. Out: editing `run-infer.sh` or the relay; enabling the gate; pulling models; rebuilding `ava`/`bruce`/`carly`.

## Resource impact / safety
Models are disk only (shared base blobs) and never resident: `keep_alive 0`, FLM stops after each reply. The router costs about 55 ms and loads no model. Live test peaks: about 1.8 GB MemAvailable drop (Ollama 1.5B) and about 2.0 GB FLM RSS. Both are well above the 2 GB floor.

## How it would be tested
Done: [router unit test](../07-testing/2026-09-29-specialist-router-unit-test.md) (35 labelled prompts plus 8 held-out, no models) and [2 live tiny requests](../07-testing/2026-09-29-specialist-live-tiny-requests.md). Once the hook is applied: one `RR_SPECIALIST_ROUTING=1 run-infer.sh bruce "<tiny prompt>"`, then check that the inference JSONL shows the specialist as `model` and `ollama ps` is empty.

## Open questions
- Should `prefer=ollama` routes (reason, security, council) skip the NPU (phase-2 hook), or stay NPU-first for power?
- Tune keywords against more real (held-out) traffic. The routing JSONL now records matched names to support that.
