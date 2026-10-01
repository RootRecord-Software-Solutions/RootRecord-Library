# AI Specialist Models and Routing

| Field | Value |
| --- | --- |
| **Date (HST)** | 2026-09-29 (~04:10–04:25 HST) |
| **Requested by** | Alexander (operator): isolated modelfiles, one per function (execution, reasoning, topic, specialty), with a keyword/topic router that sends each request to the right specialist, loaded on demand only |
| **State** | **LANDED / gated.** Models, router (v2 keywords), tests and the `run-infer.sh` hook landed. The hook is **OFF** unless `RR_SPECIALIST_ROUTING=1` (flag-off behaviour verified byte-identical, §4) |
| **Proposal record** | [08-ideas/2026-09-29-ai-specialist-models-and-routing.md](../08-ideas/2026-09-29-ai-specialist-models-and-routing.md) |
| **Test records** | [Router unit test](../07-testing/2026-09-29-specialist-router-unit-test.md) · [Live tiny requests](../07-testing/2026-09-29-specialist-live-tiny-requests.md) · [Hook + router v2](../07-testing/2026-09-29-specialist-hook-and-router-v2.md) |
| **Backup** | `/home/rootrecord/Database/GITHUB/g3-specialists.bak-20260929-041126/` |

---

## 1. Design

This follows the team constitution ([Local-Multi-Agent-Team-and-Migration-to-Build](./Local-Multi-Agent-Team-and-Migration-to-Build-2026-09-28.md) §3): *thin models + thick context, specialists over generalists, deterministic outer loop, fail closed.*

```text
request ──► route-specialist.py  (stdlib, ~50 ms, no model)
              │  keyword + regex scoring from System/config/specialist-routes.json
              │  confidence < threshold ──► "generic" = caller voice's persona model (today's behaviour)
              ▼
         specialist  ──► prefer=flm    : NPU llama3.2:1b, specialist SYSTEM block sent as the system message
                         prefer=ollama : built specialist model (rr-*) on CPU, keep_alive 0
              ▼
         loaded for this one request only, unloaded after (no resident models, no warmups)
```

- **Deterministic router.** Scoring is plain keyword/regex weights, so every decision can be explained (`--explain`) and tested without running a model.
- **One Modelfile per specialist**, grounded in Library agent packs and Pacific domain READMEs. Each one repeats the same DATA GATE (numbers only from `DESK_LIVE:` / `[desk: measured …]`, otherwise "No data — I can't see the desk"), which matches the blocks `run-ollama.sh` already injects.
- **On demand only.** Nothing is kept loaded. Ollama calls use `keep_alive 0`; FLM is started for the request and stopped afterwards (the existing `run-infer.sh` pattern).
- **FLM cannot load Ollama Modelfiles.** For `prefer=flm` routes, the router reads the specialist's `SYSTEM """…"""` block (plus `temperature` and `num_predict`) from the Modelfile and hands it over as the chat **system message** for the FLM base model (`llama3.2:1b`). The Modelfile stays the single source of truth for both backends. `route-specialist.py --system <name>` prints the exact text.
- **Reused from G1/G2:** the three persona prompts (`/home/rootrecord/old ollama/agents/{ava,bruce,carly}/*-telegram.Modelfile`, lanes catalog `lanes.conf`); the shared DATA GATE (`agents/shared/DATA_GATE.txt`); and the old council classifier's heuristics (`old skills/council/council-telegram/scripts/classify.py`: voice aliases / `@bot` mentions, moderation words, "what do you think / weigh in" council cues), which became keyword entries.

## 2. Specialists

Modelfiles: `2 - RootRecord-Database/AI/Ollama/Modelfiles/Specialists/<name>.Modelfile` (tracked in the Database repo; `~/.ollama/modelfiles` links there). Built with `ollama create <name> -f <file>` (disk only). The size shown by `ollama list` is the **shared base weights**. A specialist adds only a small system/params layer, not a new copy of the weights.

| Model | Function | Base (installed) | `ollama list` size | Prefer | temp | num_ctx | num_predict | Grounding |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `rr-exec` | execution | `qwen2.5:1.5b-instruct-q8_0` | 1.6 GB | flm | **0.1** | 2048 | 320 | Bruce ROLE/PRINCIPLES, 07-testing safety policy |
| `rr-reason` | reasoning | `llama3.2:3b-instruct-q4_K_M` | 2.0 GB | ollama | 0.4 | 4096 | 512 | team constitution, PRINCIPLES |
| `rr-energy` | topic | `qwen2.5:1.5b-instruct-q8_0` | 1.6 GB | flm | 0.2 | 3072 | 256 | Pacific `Energy/README.md`, `devices.conf` sections, jobs `ecoflow_read_*` |
| `rr-weather` | topic (weather + hazards) | `qwen2.5:1.5b-instruct-q8_0` | 1.6 GB | flm | 0.2 | 3072 | 256 | Pacific `Weather/README.md`, `Geology/README.md`, PRODUCTS |
| `rr-system` | topic (host/ops) | `qwen2.5:1.5b-instruct-q8_0` | 1.6 GB | flm | 0.2 | 4096 | 320 | Bruce INFRASTRUCTURE, `System/README.md`, `run-infer.sh` header |
| `rr-security` | specialty (AppSec) | `llama3.2:3b-instruct-q4_K_M` | 2.0 GB | ollama | 0.2 | 4096 | 384 | Carly packs, Pacific `.gitignore`, `Security/README.md` |
| `rr-cameras` | topic | `qwen2.5:1.5b-instruct-q8_0` | 1.6 GB | flm | 0.2 | 3072 | 256 | `Security/Cameras/references/CAMERAS.md`, jobs `security_*` |
| `rr-council-ava` | specialty (persona) | `llama3.2:3b-instruct-q4_K_M` | 2.0 GB | ollama | 0.5 | 4096 | 320 | Ava IDENTITY / ROLE-AND-BOUNDS / PRINCIPLES / PRODUCTS |
| `rr-council-bruce` | specialty (persona) | `llama3.2:3b-instruct-q4_K_M` | 2.0 GB | ollama | 0.3 | 4096 | 320 | Bruce IDENTITY / ROLE-AND-BOUNDS / PRINCIPLES |
| `rr-council-carly` | specialty (persona) | `llama3.2:3b-instruct-q4_K_M` | 2.0 GB | ollama | 0.3 | 4096 | 320 | Carly IDENTITY / ROLE-AND-BOUNDS / PRINCIPLES |

**Restored persona models** (`Modelfiles/Production/`). `run-infer.sh` and the relay fall back to these, and they had been missing from `ollama list`:

| Model | Source | Changes |
| --- | --- | --- |
| `ava-telegram` | `old ollama/agents/ava/ava-telegram.Modelfile` | `FROM dolphin-mistral:latest` (not installed; not pulled) → `llama3.2:3b-instruct-q4_K_M`; `num_ctx` 8192 → 4096; the long "RootRecord ideologies" block (Foundation v0.03) was dropped so the prompt fits 4096; persona, DATA GATE, HARD RULES, NPU and LANE text kept verbatim (one line that was truncated mid-word in the source was dropped) |
| `bruce-telegram` | `old ollama/agents/bruce/bruce-telegram.Modelfile` | same |
| `carly-telegram` | `old ollama/agents/carly/carly-telegram.Modelfile` | same |

The `ava` / `bruce` / `carly` models (voices.conf `fallback_model`) were **not** rebuilt. They are still missing.

Base choice: only installed small models (`qwen2.5:1.5b-instruct-q8_0`, `llama3.2:3b-instruct-q4_K_M`). Nothing was pulled. The NPU default `llama3.2:1b` exists only in FLM (`flm list`), not in Ollama. So the NPU route uses it as the base model plus the system message.

## 3. Routing config

`1 - Servers/1 - RootRecord-Pacific-Solar-Server/System/config/specialist-routes.json` (tracked):

| Key | Meaning |
| --- | --- |
| `threshold` (0.30) | Minimum confidence; below it the router returns `generic` |
| `saturation` (6.0) | Score at which strength reaches 1.0 |
| `priority` | Tie-break order (security first, so ties fail toward the safer lane) |
| `default` | `generic`: `voice_models` maps ava/bruce/carly → `*-telegram` (unchanged behaviour) |
| `specialists.<name>.keywords` | `{term: weight}`; word-boundary match after lowercasing and stripping diacritics / ʻokina (Kīlauea → kilauea); trailing `*` = prefix |
| `specialists.<name>.regex` | `[{name, pattern, weight}]`; only the **name** is ever logged |
| `ollama_model`, `modelfile`, `prefer` (`flm`/`ollama`), `fallback` | Target, prompt source, backend preference, and the model used when `--verify-model` finds the target missing |

Confidence = `min(1, top/saturation) × (0.6 + 0.4 × (top − second)/top)`. A single weight-3 keyword gives 0.5. A lone weight-1 word (e.g. "ava") gives 0.17, so it stays `generic` and the persona chat model answers.

Router CLI (`System/scripts/plumbing/route-specialist.py`, stdlib, never runs a model):

```bash
route-specialist.py --voice bruce "Why is the poller down?"          # -> rr-system 0.7
route-specialist.py --explain "Is Kīlauea erupting?"                  # per-specialist scores + matched terms
route-specialist.py --shell --with-system --verify-model --voice ava  # KEY=VALUE for eval (prompt on stdin)
route-specialist.py --json … | --list | --system rr-energy
```

Log: one JSON line per decision → `2 - RootRecord-Database/Logs/AI/Routing/routing_current.jsonl` (git-ignored, high churn). It records ts (HST offset), caller, voice, specialist, confidence, score, runner-up, **matched keyword/rule names**, prefer, model, model_verified, `prompt_chars` and elapsed µs. **It never stores prompt or reply text.** Matched keyword names are config terms, so they can hint at the topic. `RR_ROUTE_LOG=0` or `--no-log` disables it. Any router error falls back to `generic` with exit 0, so the hook can't break inference.

### 3.1 Router v2 (2026-09-29 ~04:51–04:55 HST)

`specialist-routes.json` `version: 2`. Keywords were expanded from the Library domain docs (not from `~/Desktop/old txt`): WO-ECO-001 / WO-WEB-001 (energy), WO-WXG-001 / Geology / weather-retention (weather), WO-SYS-001 / G3 runbook / WO-GH / WO-CF (system), WO-AEYES (cameras), `03-security` / WO-COM-002 (security), and `05-public-surface` / WO-WEB-002 (Ava). A term was added only if it appears in those docs or is a plain-English synonym of a doc term.

| Specialist | Added (weight) |
| --- | --- |
| rr-energy | `panel*` 3, `pv` 3, `power bank` 3, `charge level` 3, `delta2` 3, `river2pro` 3, `charged` 2, `energy-status` 2, `producing` 1, `plugged in` 1 |
| rr-weather | `swell*` 3, `shower*` / `downpour*` / `pour*` / `waves` / `cloudy` / `overcast` / `lightning` / `thunder*` 2; place names (county reports) `hilo`, `kona`, `maui`, `kauai`, `oahu`, `molokai`, `lanai`, `big island`, `north shore`, `summit` 1 |
| rr-system | `github` / `sync` / `internet` / `network` / `wifi` / `starlink` / `disconnect*` / `sluggish` 2, `relay` 1→2, `push*` / `online` / `offline` / `loaded` 1; regex `keeps_failing` 2; `liveness_question` tightened (at most 2 words between *is/are* and the state word; `up` only at the end), which fixed "What **are** the downsides of **running** …" |
| rr-cameras | `security feed` / `camera feed` 3, `stills` / `feed` / `recording` 2, `grab` 1; regex `a_still` 2 |
| rr-security | `expose*` / `bot key` / `unknown ip` 3, `is it safe` / `log in` / `login*` / `discord bot` 2, `ip address*` 1; regex `secret_in_git` 3 (commit/push/post … key/token/secret) and `login_attempts` 3 |
| rr-exec | `exact command` / `one-line` 3, `tail` / `markdown` 2, `table` 1; regex `transform_into` 3 ("turn/convert … into") |
| rr-reason | `downside*` / `walk me through` 4, `pros and cons` / `trade-off*` / `tradeoff*` 3→4, `upside*` 3, `worth it` 2 (strong reasoning cues outweigh a single topic word) |
| rr-council-ava | `announcement` 2→3, `public site` 3, `website` 2, `launch` 1 |

**Accuracy (no models run; `test-route-specialist.py`, report `2 - RootRecord-Database/Logs/AI/Routing/router-test-2026-09-29-v2.md`):**

| Set | v1 | v2 | Notes |
| --- | --- | --- | --- |
| Labelled `CASES` (35 original) | 35/35 | 35/35 | no regressions |
| Labelled `CASES` + 18 v2 tuning rows (53) | 43/53 | 53/53 | tuned on these rows (phrasing from the domain docs) |
| Old held-out (8) | 5/8 | 5/8 | same 3 misses as before, now H2 / H4 / H5 |
| **Fresh held-out `specialist-heldout-2026-09-29b.json` (27)**, written 04:51 before tuning | **11/27 (40.7%)** | 27/27 (100%) | **Optimistic.** The v1 baseline had to be scored first, so its failures were visible during tuning. Noted in the file's `_info` |
| **Blind `specialist-heldout-2026-09-29c-blind.json` (22)**, written 04:55 after tuning ended, scored once | 17/22 (77.3%) | **17/22 (77.3%)** | **The unbiased number: no gain on truly new prompts.** Misses: "What percent is the River pack at?", "kilowatt hours", "high temperature", "master key" (spaced, vs `master-key`), "better to buy a battery or panels" (→ energy, not reason) |

Conclusion: the keyword additions fix the phrasings they target, but they don't generalize by themselves. The blind misses are vocabulary gaps and structure (topic word vs reasoning frame). Proposed next steps, not done: normalize hyphen and space (`master key` = `master-key`); add unit words (`kilowatt*`, `percent`) to energy; give "better to X or Y" a comparative-frame regex that goes to rr-reason. Then score against a **new** blind set.

**v3 update (2026-09-29 ~05:08–05:10 HST, router `3.0`, config `version: 3`).** These were the structural fixes above, done as proposed:

- **Separator normalization.** Keyword matching now treats a space, hyphen or underscore the same (`kw_normalize`), so "master key" = `master-key` = `master_key`, and "a eyes" = `a-eyes`. Duplicate terms that now collide (`time-lapse` / `time lapse`, `single-flight` / `single flight`) count once, at the higher weight. Regex rules still see separators (`wo-[a-z]+`, token shapes).
- **Energy unit words:** `kilowatt*` 3, `kwh` 3, `watts` 3, `amps` 3, `amp` 2, `ampere*` 3, `amperage` 3, `volt*` 3, `percent*` 2.
- **Comparison rule:** rr-reason regex `comparison_frame` (weight 6). "is it / would it be / which is … better/best/cheaper/safer … or …" and "better to/than/for … or …" now beat one or two topic words.
- A **new blind set, `specialist-heldout-2026-09-29d-blind.json`** (21 prompts), was written at 05:08:05, before any v3 change or result, and scored once after the change.

| Set | v2 | v3 |
| --- | --- | --- |
| Original labelled (35) | 35/35 | **35/35** |
| Labelled + v2 tuning rows (53) | 53/53 | 53/53 |
| Old held-out (8) | 5/8 | 5/8 |
| Held-out 29b (27, 04:51) | 27/27 | 27/27 |
| Blind 29c (22, 04:55) | 17/22 (77.3%) | 21/22 (95.5%). Optimistic: its misses motivated the v3 fixes |
| **New blind 29d (21, 05:08)** | 14/21 (66.7%) | **20/21 (95.2%)** |

Caveat: set 29d was written knowing which three fixes were planned, and it deliberately includes unit, comparison and separator prompts. So it tests the fixes rather than being a random sample.

v3 misses:
- 29c: "What's the high temperature going to be tomorrow?" → generic (`temperature` weight 1).
- 29d: "What's the rollback if the new poller build breaks?" → rr-system instead of rr-council-bruce.
- Old held-out: H2 / H4 / H5, unchanged.
- "Where is the api-key for the weather feed stored?" is correct but only just reaches the threshold (0.30).

Report: `2 - RootRecord-Database/Logs/AI/Routing/router-test-2026-09-29-v3.md`.

## 4. Gate — `run-infer.sh` hook (LANDED 2026-09-29 ~04:56 HST, OFF by default)

`System/scripts/plumbing/run-infer.sh` (backup `run-infer.sh.pre-hook`). The file was re-read first; the JSONL-logging and single-flight changes were already in it.

- **Off** (`RR_SPECIALIST_ROUTING` unset or anything other than `1`): the hook block is skipped. `do_flm` gets empty `RR_SPEC_SYS` / `RR_SPEC_TEMP` / `RR_SPEC_MAXTOK`, so it keeps the generic voice prompt, `temperature` 0.3 and `max_tokens` 180. The JSONL line gets no new fields. A caller's own `RR_SPEC_*` variables are overridden to empty, so they can't leak in.
- **On**, with TARGET `ava|bruce|carly` (routed by prompt), or `RR_SPECIALIST=<rr-name>`, or TARGET `rr-*` (forced; new `route-specialist.py --force`, confidence 1.0, unknown name → generic):
  - **Ollama path:** `OM` = the routed specialist model (after `--verify-model`; a missing model falls back to its `fallback`).
  - **FLM / NPU path:** the specialist's Modelfile `SYSTEM """…"""` block is sent as the system message, with its `temperature` and `num_predict` (as `max_tokens`). The Modelfile stays the one source (`route-specialist.py` reads it).
  - **JSONL:** adds `"specialist":"<name|generic>","route_confidence":<0–1>` at the end of the line. The routing JSONL records the decision (names only).
  - `generic` (low confidence) leaves `OM` and the generic prompt unchanged. Explicit non-`rr-*` model targets are never routed.
  - Router errors → generic. Overhead is about 0.11 s wall per request (python start plus `/api/tags` for `--verify-model`).
- **Verification without a model:** `System/scripts/plumbing/test-run-infer-hook.sh <reference run-infer.sh>` runs the reference (pre-hook backup) and the current script against a fake FLM server and a stub `run-ollama.sh`, with a private lock and log.
  - Flag OFF: 8/8 cases **byte-identical**: stdout+stderr, the FLM request body, the normalised JSONL line and the Ollama model, including the injected-env, FLM-fail → Ollama and `DESK_LIVE_FILE` cases.
  - Flag ON: 7/7 routing checks pass.
  - A mutated reference (temperature 0.31) makes all 8 OFF cases FAIL, so the test is sensitive.
- **Callers:** `Reports/template_fill.py` sets `RR_SPECIALIST_ROUTING=1 RR_SPECIALIST=rr-exec` for its own drafting calls only (`RR_TEMPLATE_SPECIALIST_HOOK=0` disables this). The relay and voice callers are unchanged, so they stay off until the flag is set in their environment.
- **Phase 2 (not done, separate approval):** honour `RR_SPEC_PREFER=ollama` by skipping the FLM branch for reason / security / council.

## 5. Resource policy

- **No resident models.** Ollama uses `keep_alive 0`; FLM uses start → reply → stop. No warmups. `ollama create` only writes to disk.
- **Single-flight.** All inference still runs under `single-flight.sh`. The router adds about 55 ms of CPU and no model load (about 75 ms with `--with-system --verify-model`, measured 2026-09-29).
- **Light tests only**: at most 2–3 tiny prompts per change, `nice -n 10`, MemAvailable watched, stop below 2 GB. Measured 2026-09-29: Ollama `rr-energy` dropped MemAvailable by about 1.8 GB; FLM `llama3.2:1b` peak RSS was about 2.0 GB (see the live test record).
- **Small bases.** 1.5B for lookups and execution, 3B for judgement (reason, security, council). No 7B+ specialists.
- Per 07-testing policy: no secrets in prompts or logs, and hardware-actuating actions stay approval-only (each prompt says so).

## 6. How to add a specialist

1. Write `2 - RootRecord-Database/AI/Ollama/Modelfiles/Specialists/<name>.Modelfile`: the header comment with grounding, `FROM <installed small model>`, a focused `SYSTEM """…"""` that ends with the shared DATA GATE paragraph, and `PARAMETER`s (`num_ctx` ≤ 4096).
2. `ollama create <name> -f <file>` (disk only). Confirm with `ollama list` and check that `ollama ps` stays empty.
3. Add an entry under `specialists` in `System/config/specialist-routes.json` (`keywords`, optional `regex`, `ollama_model`, `modelfile`, `prefer`, `fallback`), and add it to `priority`.
4. Add at least 3 labelled prompts (plus 1 "should stay generic") to `CASES` in `System/scripts/plumbing/test-route-specialist.py`. Run it. It must stay ≥ 90% with privacy PASS. Save the table with `--out 2 - RootRecord-Database/Logs/AI/Routing/router-test-YYYY-MM-DD.md`.
5. At most one live tiny request (`keep_alive 0`, `nice -n 10`), with a record in `07-testing/`.
6. Update the table in §2.

## 7. Open items

- Router generalization: v2 gave no blind gain (17/22). v3's structural fixes gave blind 29c 21/22 and new blind 29d 14/21 → 20/21 (§3.1). The remaining misses are "temperature" (weight 1) and rollback phrasing going to system instead of Bruce.
- The hook is landed but OFF for the relay and voices. Turning it on for them (`RR_SPECIALIST_ROUTING=1` in their environment) is Alexander's call.
- With the hook, the NPU gets the specialist SYSTEM (live: `rr-weather` answered "No data — I can't see the desk." for a rain question). But `rr-exec`'s SYSTEM (desk layout plus DATA GATE) does not suit facts-only drafting: its reply printed the desk layout and "No data" ([template record](../07-testing/2026-09-29-specialist-hook-and-router-v2.md)).
- Replies are only as good as 1B/1.5B/3B models allow.
- `ava` / `bruce` / `carly` (voices.conf `fallback_model`) are still not built.

*Created 2026-09-29 ~04:25 HST (g3-specialists pass).*
*Updated 2026-09-29 ~05:02 HST (hook + router v2 pass).*
*Updated 2026-09-29 ~05:14 HST (router v3 pass).*
