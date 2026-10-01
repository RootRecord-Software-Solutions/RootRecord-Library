# Test record — Router v3 structural fixes + template drafting through a desk file (2 live NPU calls)

| Field | Value |
| --- | --- |
| **Date / time (HST)** | 2026-09-29 05:08–05:12 HST |
| **Tester** | agent pass g3-router-v3 |
| **Change under test** | `route-specialist.py` 3.0 (separator-insensitive keywords); `specialist-routes.json` v3 (energy units, `comparison_frame`); `Reports/template_fill.py` passing the facts as a temporary `DESK_LIVE_FILE` ([design](../00-architecture/AI-Specialist-Models-and-Routing.md) §3.1, [templates](../00-architecture/Template-Report-Generation.md) §3) |
| **State** | **PASS (router)**: labelled 35/35 kept; new blind 14/21 → 20/21. **PARTIAL (drafting)**: 1 of 2 free-text fields accepted on the second call, and that field contains a claim the facts don't support |
| **Evidence** | `2 - RootRecord-Database/Logs/AI/Routing/router-test-2026-09-29-v3.md`; inference JSONL 05:11:08 and 05:12:00 (caller `template_fill`); `test-reports/Templates/template-fill-validation_current.json` |
| **Backup** | `/home/rootrecord/Database/GITHUB/g3-specialists.bak-20260929-041126/` (`*.pre-v3`, `template_fill.py.pre-deskfile`, `template_fill.py.pre-deskfile-2`) |

## Pass criteria (written before running)
1. New blind set (about 20 prompts) written before any v3 change or result. It is scored once after the change and not tuned against.
2. Original 35 labelled cases stay 35/35. Before/after numbers are reported on every set, including the 04:55 blind set.
3. Drafting: at most 2 live NPU calls (on demand, keep nothing loaded). The number check passes or falls back safely. The temp desk file is deleted.
4. Afterwards: `ollama ps` empty, no flm, lock IDLE, MemAvailable never below 2 GB.

## 1. Router (no model)
Blind set `specialist-heldout-2026-09-29d-blind.json` (21 prompts) was written at 05:08:05, before any v3 change. It was scored once, in one run together with v2, using the pre-v3 router and config from the backup.

| Set | v2 | v3 |
| --- | --- | --- |
| Original labelled (35) | 35/35 | **35/35** |
| Labelled + v2 tuning rows (53) | 53/53 | 53/53 |
| Old held-out (8) | 5/8 (62.5%) | 5/8 (62.5%) |
| Held-out 29b (27, 04:51) | 27/27 | 27/27 |
| Blind 29c (22, 04:55) | 17/22 (77.3%) | 21/22 (95.5%). Optimistic: its misses shaped the fixes |
| **New blind 29d (21, 05:08)** | 14/21 (66.7%) | **20/21 (95.2%)** |

- **Fixed by v3:** pack voltage, 3 "better … or …" questions, "api-key" (just at the 0.30 threshold), "a eyes"; and in 29c: percent, kilowatt hours, master key, "better to buy a battery or panels".
- **Still wrong:** "high temperature" (29c); "rollback if the new poller build breaks" (29d, → rr-system instead of rr-council-bruce); old H2 / H4 / H5.
- **Caveat:** 29d was written knowing the three planned fixes, so it tests them. It is not a random sample.

## 2. Drafting through a desk file

Model-free check first (stubbed `run-infer.sh`):
- With the hook on, the desk file exists during the call with mode 0600, holds 9 fact lines, and is deleted afterwards. `RR_SPECIALIST_ROUTING=1` and `RR_SPECIALIST=rr-exec` are passed.
- With `RR_TEMPLATE_SPECIALIST_HOOK=0`: no desk file and no hook, as before.

| Call | Time (HST) | Route | Latency | FLM peak RSS | MemAvailable before → min → after | Result |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 05:10:58 | npu-flm `llama3.2:1b` + `rr-exec` SYSTEM + desk block, cold start | 9580 ms | 2006 MB | 9465 → 7604 → 9479 MB | Reply replaced by `run-infer.sh` `sanitize()` ("No live desk data attached."; the raw output was 20 lines, most likely echoing the DATA GATE's `DESK_LIVE:`). INTENT and SCOPE fell back |
| 2 | 05:11:52 | same, plus the end-of-prompt reminder "Answer now with only the INTENT: and SCOPE: lines" | 7028 ms | 2006 MB | 9466 → 7603 → 9470 MB | **INTENT accepted by the checks**: "The measured desk lines indicate a need for a restart to ensure accurate data." **SCOPE fell back** (desk-layout path; unsupported numbers `1`, `1`). Output valid: 12 headings / 3 tables, 0 unsupported numbers |

Afterwards: 0 `rr-template-desk-*` files, `ollama ps` empty, 0 flm processes, :52625 closed, single-flight IDLE.

## Findings
- The desk file got the model past "No data". The number check and structure validator caught the path leak in SCOPE and fell back safely.
- **The accepted INTENT is not fully supported by the facts** ("to ensure accurate data" is invented; the facts only list "Poller restart" as a sign-off item). The number check only guards numbers. Model free text must stay a draft for human review.
- A stronger guard would be a word-overlap or claim check, or restricting free text to paraphrases of the fact lines. Not done.
- The 1B model on the NPU often echoes its system text. `sanitize()` in `run-infer.sh` is what blocked call 1; `template_fill` now records that as `sanitized_by_run_infer`.

*Record 2026-09-29 HST.*
