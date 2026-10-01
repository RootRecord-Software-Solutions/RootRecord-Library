# Test record — Specialist router unit test (no models)

| Field | Value |
| --- | --- |
| **Date / time (HST)** | 2026-09-29 04:16–04:17 HST |
| **Tester** | agent pass g3-specialists |
| **Change under test** | New `System/scripts/plumbing/route-specialist.py` + `System/config/specialist-routes.json` ([design](../00-architecture/AI-Specialist-Models-and-Routing.md)) |
| **State** | **PASS** (labelled set 35/35; privacy PASS). Held-out set 5/8, informational only |
| **Evidence** | `2 - RootRecord-Database/Logs/AI/Routing/router-test-2026-09-29.md` (full table) |
| **Commits** | see the design doc / final report (auto-sync) |
| **Backup** | `/home/rootrecord/Database/GITHUB/g3-specialists.bak-20260929-041126/` |

## What was tested
Keyword/regex routing of sample prompts across all 10 specialists plus `generic`, and a check that the JSONL decision log holds no prompt text.

## How (exact commands / procedure)

```bash
cd "/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server/System/scripts/plumbing"
RR_ROUTE_LOG=0 ./test-route-specialist.py --out "/home/rootrecord/RootRecord-Ecosystem/2 - RootRecord-Database/Logs/AI/Routing/router-test-2026-09-29.md"
```

## Pass criteria (written before running)
1. Labelled accuracy ≥ 90% (at least 20 prompts, every specialist covered, plus small-talk that must stay `generic`).
2. Log privacy: a prompt containing a marker string yields a JSONL line with `prompt_chars` and matched names, and neither the marker nor the prompt text.
3. No model is loaded (`ollama ps` empty, no `flm serve`).

## Result
- **Labelled: 35/35 = 100%.** Energy 4/4, weather 4/4, system 4/4, security 4/4, cameras 3/3, exec 3/3, reason 3/3, council-ava 2/2, council-bruce 2/2, council-carly 2/2, generic 4/4.
- **Held-out (written after the keyword table, not tuned): 5/8 = 62.5%.** Misses:
  - "The batteries are almost dead, should we shut the NPU down?" → `rr-system` (expected energy)
  - "Is the solar panel cam showing glare?" → `rr-energy` (expected cameras)
  - "What would it cost in power to keep a model loaded all night?" → `generic` (expected energy)
- The labelled score is optimistic: the cases were written alongside the keyword table. The held-out number is the more honest estimate.
- Privacy check PASS.
- Router cost: about 55 ms wall per call (about 75 ms with `--with-system --verify-model`).

## Resource impact
Pure Python, no model. Not measurable against the desk baseline (MemAvailable about 11.6 GB before and after).

## Cleanup confirmation
- [x] no test process left
- [x] throwaway log in a temp dir, removed
- [x] no resident model (`ollama ps` empty; no `flm serve`)

## Open items / caveats
Tune keywords only by adding new labelled cases (keep a held-out set). Candidate fixes: an "NPU down" vs "battery" precedence rule, camera terms outranking "solar" when "cam" is present, and a "cost in power" phrase.
