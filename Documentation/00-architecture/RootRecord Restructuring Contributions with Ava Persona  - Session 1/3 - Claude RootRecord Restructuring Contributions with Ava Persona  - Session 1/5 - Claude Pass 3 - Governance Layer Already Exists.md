# Claude — Pass 3: The Governance Layer Grok/Copilot Recommended Already Exists

**Document Status:** Collaborative Architectural Draft — Claude Contribution, Pass 3
**Contributor:** Claude
**Builds on:** Pass 1 (weather/comms duplication, human-scale recoverability), Pass 2 (agent identity migration in progress)
**Responds to:** Grok Phase 1 ("Clarity & Contracts" — repository map, status schema versioning, ADRs) and Copilot's equivalent recommendations (repository manifests, CI validation, ADRs, health/status contracts).

---

## 1. The finding

Grok and Copilot both recommended, as near-term work, building: a repository map, per-repository manifests, CI validation that catches invalid state before it looks deployable, a versioned status schema, and lightweight ADRs for major decisions. Having opened `0-master-prompt/` in the actual repo, essentially all of this already exists, already works, and is already partway wired up:

| Recommended (Grok/Copilot) | Already present in `0-master-prompt/` |
|---|---|
| Repository map document | `prompts/08-repository-and-file-links.md` — explicit rule: *"these are links to the real source files. Do not copy those files into the Master Prompt repository."* |
| Per-repository manifest / schema | `manifest/prompts.yaml` — versioned (`version: "1.3"`), each prompt file marked `required: true/false` |
| CI validation that fails on invalid state | `.github/workflows/build-bundle.yml` — checks required files exist, validates `state.json` and `state-history.json` are well-formed, confirms the repo-link index isn't empty, before building anything |
| Versioned status/state schema | `state/state.json` — has `schema_version`, `generated_at`, per-subsystem status blocks (`repository`, `connections`, `power`, `work`, `evidence`) |
| Evidence labeling discipline | `state.json`'s `evidence.overall: "Confirmed"` field, and `prompts/00-core.md` / `04-operations.md` both formalize **Confirmed / Hypothesis / Unknown / Historical** as required labels |
| ADR-style decision record | Not yet present as a dedicated `ADR-000x` series, but `prompts/01-architecture.md`'s explicit source hierarchy (live verification > repo docs > master-prompt rules > historical handoffs > unverified assumptions) already does the job an ADR index is meant to do: telling a future reader what outranks what when sources disagree. |
| File-layout convention so config doesn't become unreadable | `prompts/09-file-layout-style.md` — already codifies the sectioned banner / TEMPLATE-block style Section 29 of the baseline document describes, with `automations/scripts/jobs.py` as the canonical worked example. |

This isn't "close to" what was recommended — the manifest schema, the CI gate, the evidence-labeling convention, and the file-layout rule are functionally the same artifacts Grok and Copilot proposed inventing, already in daily use.

---

## 2. What this changes about the recommendation

Both prior passes' Phase 1 recommendations should be re-scoped from **"create"** to **"declare canonical and extend."** Concretely:

* Don't create a new `REPOSITORY-MAP.md` — `prompts/08-repository-and-file-links.md` is that document. Section 38 of the baseline ("Canonical Source Links") duplicates part of its content; Section 38 should point at the master-prompt file rather than maintaining a second copy that can drift out of sync with it — the same duplication pattern Pass 1 flagged for weather and comms, just at the documentation layer instead of the code layer.
* Don't invent a new status schema — `state/state.json`'s existing shape (`repository` / `connections` / `power` / `work` / `evidence`) is the schema. What Grok specifically asked for that's genuinely missing is a `schema_url`, and a documented public-vs-detailed split for anything this feeds into the website's status page (`website/site/src/app/status/page.tsx` / `home/status/page.tsx` already exist as consumers, per the repo).
* Don't invent an ADR series from nothing — `prompts/01-architecture.md`'s source-precedence rule already substitutes for most of what ADRs are for at this scale. A dedicated ADR series is only worth adding if there start to be genuine multi-option decisions (e.g., the weather/comms canonicalization calls from Pass 1) that need a permanent record of *why* one option was picked over another — the precedence rule alone doesn't capture that.

---

## 3. What's genuinely missing (the real gap)

The system's own `state.json` already says what's incomplete, in its own words: `connections.rootrecord_server` and `connections.mainland_server` are both `"status": "unknown"`, and `work.next_action` states the five-minute updater still needs to be connected to real connection, power, and worklog collectors. So the actual open work is not "design a state/status contract" — that's done — it's:

1. Wire the five-minute updater to live Solar-Pacific and Mainland connection checks (currently `unknown`, not `false` — meaning no check has run yet, not that the check failed).
2. Wire the `power` block to the actual EcoFlow/energy telemetry that already exists under `energy/` (190 files — clearly a substantial existing subsystem) rather than leaving it `null` in the schema.
3. Decide whether `logs/state-history.json` is meant to be the durable record referenced elsewhere (it's currently 34 lines — a very short history for a "five-minute recorder," suggesting it was recently reset or isn't yet running on its full cadence) or a rolling short window with a separate durable archive.

---

## 4. Recommendation

* Add one line to `prompts/07-current-state.md` or `README.md` explicitly declaring `0-master-prompt/` the canonical governance layer for repository maps, manifests, state schema, and evidence discipline — closing the door on Grok/Copilot's (reasonable, evidence-free-at-the-time) recommendation to build these from scratch.
* Retire the duplicate link list in Section 38 of the baseline document in favor of a pointer to `prompts/08-repository-and-file-links.md`.
* Treat "wire the collectors" (item 1–2 above) as the actual next unit of work, not "design the schema" — the schema is done and already has a CI gate protecting it.
* If a dedicated ADR series is added later, reserve it for genuinely contested calls — starting with the weather-canonicalization and comms-pattern decisions raised in Pass 1 — rather than duplicating what `01-architecture.md` already covers.

---

*End of Pass 3. Next candidate for Pass 4: a closer look at the `energy/` subsystem (190 files, the largest single directory in Solar-Pacific) — worth checking whether it already follows the operations/skills split cleanly, given how central power state is to this system's actual recoverability story.*
