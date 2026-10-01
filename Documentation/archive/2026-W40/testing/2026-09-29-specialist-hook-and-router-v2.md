# Test record — Specialist hook in `run-infer.sh` + router v2 (model-free diff, 2 live calls)

| Field | Value |
| --- | --- |
| **Date / time (HST)** | 2026-09-29 04:51–05:00 HST |
| **Tester** | agent pass g3-specialists (hook + router v2) |
| **Change under test** | `run-infer.sh` specialist hook (`RR_SPECIALIST_ROUTING`, default off); `route-specialist.py --force`; `specialist-routes.json` v2; `template_fill.py` passing `RR_SPECIALIST=rr-exec` ([design](../00-architecture/AI-Specialist-Models-and-Routing.md) §3.1, §4) |
| **State** | **PASS** (hook). Flag-off byte-identical 8/8; flag-on 7/7; both live calls routed correctly. Router v2: **no gain on the blind set** (17/22 → 17/22). Template free text still falls back (see below) |
| **Evidence** | `System/scripts/plumbing/test-run-infer-hook.sh`; `2 - RootRecord-Database/Logs/AI/Routing/router-test-2026-09-29-v2.md`; inference and routing JSONL lines at 04:58:52 and 04:59:57 |
| **Backup** | `/home/rootrecord/Database/GITHUB/g3-specialists.bak-20260929-041126/` (`*.pre-hook`, `*.pre-router-v2`) |

## Pass criteria (written before running)
1. Flag off: `run-infer.sh` output, FLM request body, JSONL line and Ollama model are byte-identical to the pre-hook file. Checked by a diff, not a model call.
2. Flag on: the Ollama path uses the routed model; the FLM path sends the specialist SYSTEM (plus its temperature and max tokens); JSONL has `specialist` and `route_confidence`.
3. A fresh held-out set of at least 20 prompts is written before tuning, and accuracy is reported before and after.
4. At most 2 live model calls, with the lock IDLE and MemAvailable > 2 GB. Afterwards `ollama ps` is empty and no flm is running.

## 1. Byte-identical check (no model)
`test-run-infer-hook.sh <pre-hook backup>`: a temp dir, a fake FLM server on 127.0.0.1:52999, a stub `run-ollama.sh`, and a private lock, state and JSONL.

| Group | Cases | Result |
| --- | --- | --- |
| Flag OFF vs pre-hook | FLM ok; FLM fail → Ollama; `RR_SPECIALIST` + injected `RR_SPEC_SYS`/`RR_SPEC_SYSTEM`/`RR_SPEC_TEMP` env; `RR_SPECIALIST_ROUTING=0`; TARGET `rr-exec` (FLM and Ollama); generic prompt; `DESK_LIVE_FILE` | **8/8 byte-identical** (7498 bytes compared) |
| Flag ON | routed energy (FLM: system "You are RootRecord Energy…", 0.2, 256; Ollama: `rr-energy`); generic (voice prompt, 0.3, 180, `specialist":"generic"`); forced by env and by TARGET `rr-exec` (0.1, 320); explicit non-rr model (not routed, no new fields); unknown forced name → generic | **7/7 PASS** |
| Sensitivity | reference mutated (`temperature` 0.31) | 8/8 OFF cases **FAIL**, as expected |

## 2. Router accuracy (no model)

| Set | v1 | v2 |
| --- | --- | --- |
| Original labelled (35) | 35/35 | 35/35 |
| Labelled + 18 tuning rows from domain-doc phrasing (53) | 43/53 | 53/53 |
| Old held-out (8) | 5/8 | 5/8 |
| Fresh held-out `specialist-heldout-2026-09-29b.json` (27; written 04:51, before tuning) | **11/27 = 40.7%** | 27/27 (optimistic: its failures were visible during tuning) |
| Blind `specialist-heldout-2026-09-29c-blind.json` (22; written 04:55 after tuning; scored once) | 17/22 = 77.3% | **17/22 = 77.3%** |

Honest reading: v2 fixes the phrasings it targets, but gives **no measurable gain on truly new prompts**. Blind misses: "percent … River pack", "kilowatt hours", "high temperature", "master key" (spaced), "better to buy a battery or panels" (→ energy instead of reason).

## 3. Live calls (2 total)

| # | Time (HST) | Request | Route | Result |
| --- | --- | --- | --- | --- |
| 1 | 04:58:44–04:58:52 | `template_fill.py --template workorder --draft model` (hook: `RR_SPECIALIST=rr-exec`) | npu-flm `llama3.2:1b` + `rr-exec` SYSTEM; JSONL `"specialist":"rr-exec","route_confidence":1.0` | 7364 ms, cold start, FLM peak 2005 MB, prompt 816 / reply 291 chars. Output valid (12 headings / 3 tables, 0 unsupported numbers). **Free text fell back again**: the reply opened "No data — I can't see the desk." (INTENT missing). SCOPE listed repo folders from the SYSTEM desk layout and was rejected for unsupported numbers `2`, `1`. The file was unchanged, so there was no rotation |
| 2 | 04:59:52–04:59:57 | `RR_SPECIALIST_ROUTING=1 run-infer.sh bruce "Is it going to rain in Hilo today?"` | router `rr-weather` 0.5 (`rain*`, `hilo`; model verified; router 31 ms) → npu-flm + `rr-weather` SYSTEM | Reply "No data — I can't see the desk." (correct DATA GATE, no invented forecast). 4687 ms, cold start, FLM peak 2007 MB. JSONL `"specialist":"rr-weather","route_confidence":0.5` |

**Resources:**
- Call 1: MemAvailable 9158 MB before → minimum 7643 → 9493 after.
- Call 2: 9568 → minimum 7685 → 9503.
- Afterwards: `ollama ps` empty, 0 flm processes, :52625 closed, single-flight IDLE.

## Findings
- The hook works on both backends and is invisible when off.
- `rr-exec`'s SYSTEM is a command persona with a desk layout and the DATA GATE, so it is a poor fit for facts-only drafting. The next option is a facts `DESK_LIVE_FILE` block or a small `rr-draft` specialist, with one re-test.
- Router generalization needs structural changes (hyphen/space normalization, unit words, a comparative-frame regex) and a new blind set, not more synonyms.

*Record 2026-09-29 HST.*
