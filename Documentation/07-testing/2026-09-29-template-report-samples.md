# Test record — Template reports: one sample per Library template (3 light model calls)

| Field | Value |
| --- | --- |
| **Date / time (HST)** | 2026-09-29 04:31:25–04:34:05 HST |
| **Tester** | agent pass g3-template-reports |
| **Change under test** | `Reports/template_fill.py` + `Reports/template_validate.py` ([design](../00-architecture/Template-Report-Generation.md)); gated job `template_reports_daily` |
| **State** | **PASS** (4/4 outputs pass the structure validator; 0 unsupported numbers; model free text used for 1 of 2 templates, fallback for the other) |
| **Evidence** | Database `Reports/Generated/*_current.md`, `Archive/`, `template-fill-validation_current.json`; `Logs/AI/Inference/inference_current.jsonl` (caller `template_fill`) |
| **Backup** | `/home/rootrecord/Database/GITHUB/g3-specialists.bak-20260929-041126/` (`*.pre-template-reports`) |

## Pass criteria (written before running)
1. One output per template (4). Each passes `template_validate.py` with the same headings, table columns, field order and vocabulary as its template.
2. No number in any output is missing from the source data (`unsupported_numbers` empty).
3. The model is called for at most 3 light requests in total. The lock is IDLE before each call, and MemAvailable stays above 2 GB.
4. Afterwards: `ollama ps` is empty and no flm is running. Nothing is written into the Library.
5. The validator rejects deliberately broken copies.

## Result

| Step | Time (HST) | What | Result |
| --- | --- | --- | --- |
| Dry run | 04:30 | `--all --draft none --dry-run` | 4/4 ok (headings 11/12/7/12, tables 2/3/1/3) |
| Negative tests | 04:30 | Renamed heading, renamed table column, wrong status vocabulary, invented numbers | All 3 structural mutations **rejected**; `73.4`, `417`, `9137` **flagged** |
| Library guard | 04:30 | `write_rotating()` aimed at the Library | Refused (`[fail] refusing to write into the Library`), no file created |
| Run 1 | 04:31:25–04:31:39 | `--all --draft model --model-templates worklog,workorder` (13.96 s wall) | 4/4 ok; model calls 1 and 2 |
| Call 1 (worklog) | 04:31:33 | npu-flm `llama3.2:1b`, cold start, 7655 ms, prompt 870 / reply 572 chars, FLM peak RSS 2006 MB | PURPOSE / NEXT / STATUS accepted |
| Call 2 (work order) | 04:31:39 | npu-flm, cold start, 5969 ms, 727 / 438 chars, peak 2006 MB | INTENT / SCOPE **fallback**: reply not in `KEY:` form |
| Call 3 (work order only) | 04:32:56 | npu-flm, cold start, 9217 ms, 816 / 786 chars, peak 2006 MB | **fallback** again. Reply opened "I am RootRecord, and I cannot see the desk…" (generic voice system prompt on the NPU path) and added the unsupported claim "require restarts", which was rejected. Old `Work-Order_current.md` → `Archive/Work-Order_2026-09-29T0431.md` |
| Fix + rerun | 04:34:05 | Cloudflared detection bug fixed (path with spaces; now `/proc/*/comm`); `--template checkpoint --draft none` | ok; tunnel `ok` (1 process, last tunnel line 03:46 connected). Old copy → `Archive/RootRecord-Checkpoint_2026-09-29T0431.md` |

**Resources:** MemAvailable was 11977 MB before run 1, dropped to a minimum of 9942 MB (04:31:37) and returned to 11993 MB after.
Around call 3 it went 11941 → 9879 min → 11794 MB. The largest single process was about 2.0 GB (FLM). There were no Ollama loads (no fallback).
Afterwards `ollama ps` was empty, there were 0 `flm` processes, and single-flight was IDLE.

**Sample of accepted model text (worklog, as written at 04:31):** Purpose "This digest covers testing of the system."; Next "Restart the poller.";
Status "Sign-off needed: Poller restart." The bare "Restart the poller." dropped the sign-off context. So **after** this run, `NEXT` must name a
real sign-off item and is written as `Alexander sign-off: <item>` (not re-run, to stay within the 3-call budget; the sample file still shows the 04:31 text).

## Findings
- The structure is exact for all 4 templates. The deterministic fallback keeps every report complete when the 1B model ignores the format.
- NPU drafts are weak because `run-infer.sh`'s FLM path uses the generic voice system prompt, not the `rr-exec` SYSTEM.
  The gated specialist hook (`RR_SPEC_SYSTEM`, needs approval) is the fix. `run-infer.sh` was not edited in this pass.
- Job `template_reports_daily` imports with `enabled=False` by default and `True` with `RR_TEMPLATE_REPORTS=1` (checked by importing `jobs.py`; the poller was not restarted).

*Record 2026-09-29 HST.*
