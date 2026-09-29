# AI Specialist Models and Routing

| Field | Value |
| --- | --- |
| **Date (HST)** | 2026-09-29 (~04:10–04:25 HST) |
| **Requested by** | Alexander (operator): isolated modelfiles, one per function (execution, reasoning, topic, specialty), with a keyword/topic router that sends each request to the right specialist, loaded on demand only |
| **State** | **LANDED / gated.** Models built, router and tests landed. `run-infer.sh` hook **PROPOSED** (not applied; `RR_SPECIALIST_ROUTING` is off by default) |
| **Proposal record** | [08-ideas/2026-09-29-ai-specialist-models-and-routing.md](../08-ideas/2026-09-29-ai-specialist-models-and-routing.md) |
| **Test records** | [Router unit test](../07-testing/2026-09-29-specialist-router-unit-test.md) · [Live tiny requests](../07-testing/2026-09-29-specialist-live-tiny-requests.md) |
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

## 4. Gate — proposed `run-infer.sh` hook (NOT applied)

`run-infer.sh` is owned by another agent's pass (JSONL logging), so this pass did **not** edit it. For a later pass, back it up first, re-read it, then add:

**Hook 1 (one line, right after the `case "$TARGET" in … esac` block):**

```bash
[[ "${RR_SPECIALIST_ROUTING:-0}" == "1" && "$TARGET" =~ ^(ava|bruce|carly)$ && -x "$HERE/route-specialist.py" ]] && eval "$(printf '%s' "$PROMPT" | RR_CALLER="${RR_CALLER:-run-infer}" "$HERE/route-specialist.py" --voice "$TARGET" --shell --with-system --verify-model 2>/dev/null)" && [[ "${RR_SPEC_DEFAULT:-1}" == "0" ]] && { OM="$RR_SPEC_OLLAMA_MODEL"; export RR_SPEC_SYSTEM RR_SPEC_TEMPERATURE RR_SPEC_MAX_TOKENS; }
```

**Hook 2 (FLM system message; one line inside `do_flm`'s Python, directly after the `system = (…)` assignment):**

```python
system = os.environ.get("RR_SPEC_SYSTEM") or system
```

(Optional, same place: `"temperature": float(os.environ.get("RR_SPEC_TEMPERATURE") or 0.3)`, `"max_tokens": int(os.environ.get("RR_SPEC_MAX_TOKENS") or 180)`.)

Behaviour:

- Off by default (`RR_SPECIALIST_ROUTING` unset, or anything other than `1`). With it off, `run-infer.sh` behaves exactly as it does today.
- It applies only when TARGET is a voice. Explicit model targets are never overridden.
- `generic` leaves `OM` unchanged. A missing specialist model swaps to its `fallback` (`--verify-model`).
- The existing `ailog` line then records the specialist as `model`, so the inference JSONL and the routing JSONL can be joined on time.
- **Phase 2 (later, separate approval):** honour `RR_SPEC_PREFER=ollama` by skipping the FLM branch (`if [[ "${RR_SPEC_PREFER:-flm}" != ollama ]] && flm_up; then` and the same guard on the on-demand start). Until then every route still tries the NPU first with the specialist system message, which is the cheaper path.

The relay needs no change. It already calls `run-infer.sh <voice> <prompt>`.

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

- Held-out routing accuracy is lower than on the tuned set: 5/8 (see the unit-test record). Known confusions: "batteries … NPU down" → system; "solar panel cam" → energy; power-cost phrasing without energy keywords → generic. Tune only with new labelled cases.
- The hook is not wired. It needs a later pass on `run-infer.sh` once the JSONL-logging edits settle, plus Alexander's go.
- Replies are only as good as 1.5B/3B models allow. The live FLM weather test answered the DATA GATE correctly but did not name the official source it was asked to name.
- `ava` / `bruce` / `carly` (voices.conf `fallback_model`) are still not built.

*Created 2026-09-29 ~04:25 HST (g3-specialists pass).*
