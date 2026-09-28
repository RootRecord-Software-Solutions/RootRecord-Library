# Claude — Pass 2: Agent Identity Currently Lives in Three Places

**Document Status:** Collaborative Architectural Draft — Claude Contribution, Pass 2
**Contributor:** Claude
**Builds on:** Pass 1 (weather duplication, comms duplication, human-scale recoverability)
**Follows up on:** Baseline Section 15 ("Agent identity and repository ownership are separate concepts") and the Copilot exchange where the per-agent `Agent-Context` repos and the planned local `RootRecord Library/Agent Context` cache were first described.

---

## 1. The finding

Section 15 of the baseline document treats "agent identity vs. repository ownership" as a principle to establish. Having opened `agents/ava-ivy/` inside the actual `Solar-Pacific-RootRecord-Server` repo, it's clear this isn't a principle waiting to be established — it's a live migration that is already in progress and currently sitting in an unresolved middle state. Right now, material that answers "who is Ava" exists in three separate physical locations:

```text
1. Solar-Pacific-RootRecord-Server/agents/ava-ivy/
   ├── SKILL.md                        (agent packet: models, inference routing, poll ownership)
   ├── docs/IDENTITY.md                (self-description, operator, host, "character" framing)
   ├── docs/ROLE-AND-BOUNDS.md
   ├── docs/PUBLIC-VOICE.md
   ├── docs/avatar.png / .github/profile-avatar.png
   └── references/GITHUB-IDENTITY.md   (explicitly marked "working")

2. AvaIvy/Agent-Context   (and BruceMonitor/Agent-Context, CarlyMal/Carly-Agent-Context)
   — per-agent personal GitHub repos, referenced in the Copilot conversation as the
     intended canonical home for each agent's own identity/context.

3. /home/rootrecord/Documents/RootRecord Library/Agent Context/
   ├── Ava-Agent-Context
   ├── Bruce-Agent-Context
   └── Carly-Agent-Context
   — the planned local working-copy cache of location 2, described in the Copilot
     conversation but not present in the repo archives reviewed here.
```

This is not a hypothetical overlap. `agents/ava-ivy/references/GITHUB-IDENTITY.md`, inside the org-owned Solar-Pacific repo, says plainly that Ava's own dedicated GitHub identity is still something to be provisioned in the future, and that until then commits on the shared tree should not carry a permanent git identity. That note was written before the `AvaIvy/Agent-Context` repo existed. The repo now exists. The note in Solar-Pacific hasn't been updated to reflect that, and the identity material it was guarding (`IDENTITY.md`, `ROLE-AND-BOUNDS.md`, `PUBLIC-VOICE.md`, avatar assets) is still sitting in the org repo rather than the agent's own repo.

In short: the cutover Section 15 describes as a target state has been started, not finished, and nothing currently marks which of the three locations is authoritative for which kind of content today.

---

## 2. Why this matters more than a tidiness issue

Two concrete risks follow directly from the current three-location state:

* **Drift.** If `IDENTITY.md` or `PUBLIC-VOICE.md` gets edited in Solar-Pacific (because that's the tree an agent or the operator has open at the time) after `AvaIvy/Agent-Context` is supposed to be canonical, the two copies silently diverge and nothing detects it. This is the same class of problem as the weather/comms duplication from Pass 1, just in the identity layer instead of the operational layer.
* **Recovery ambiguity.** Pass 1 noted that the handoff-context material already answers "what happens if the operator is unavailable." It does not yet answer "what happens if `AvaIvy/Agent-Context` is unreachable but Solar-Pacific's copy of `agents/ava-ivy/` is stale." Without an explicit statement of which copy wins, a coverage AI picking up mid-incident (exactly the scenario the emergency handoff pack exists for) has no way to know which `IDENTITY.md` to trust.

---

## 3. What actually belongs where

Not everything currently under `agents/ava-ivy/` is the same kind of thing, and it doesn't all belong in the same destination. Splitting it by function:

| Content | Current location | Best home | Why |
|---|---|---|---|
| `SKILL.md` (model bindings, poll ownership, inference routing) | `Solar-Pacific/agents/ava-ivy/` | **Stays in Solar-Pacific** | This is operational wiring specific to the OmniBook runtime, not portable identity. It matches the doc's own "operations vs. skills" boundary — it's a skill in the agent-capability sense, tied to this machine's Ollama/FastFlowLM setup. |
| `docs/IDENTITY.md`, `docs/ROLE-AND-BOUNDS.md`, `docs/PUBLIC-VOICE.md`, avatar assets | `Solar-Pacific/agents/ava-ivy/` | **Moves to `AvaIvy/Agent-Context`** | This is exactly the portable, agent-owned identity material Section 15 and the per-agent-repo model describe. It should be able to survive Solar-Pacific being rebuilt, replaced, or migrated. |
| `references/GITHUB-IDENTITY.md` | `Solar-Pacific/agents/ava-ivy/` | **Retired once the cutover completes** | Its entire content is "here's the plan for when the dedicated GitHub identity exists." The dedicated identity now exists. This file's job is done; keeping it risks someone reading stale provisioning instructions as current state. |
| `notes/2026-09-22-STOPPING-POINT.md` | `Solar-Pacific/agents/ava-ivy/` | **Belongs with the handoff-context material from Pass 1**, not with identity | It's a point-in-time operational snapshot, not who-Ava-is. Filing it next to `IDENTITY.md` conflates "durable identity" with "today's status," which is the same category error Section 34's contribution rules warn against (confirmed fact vs. observed problem vs. proposal). |

The same split applies to `bruce-monitor/`, `carly-mal/`, and `advisor/` — all four follow the identical internal shape (`SKILL.md` + `docs/` + `references/GITHUB-IDENTITY.md` + `notes/`), so whatever rule is adopted for Ava should apply uniformly to all four rather than being decided agent-by-agent.

---

## 4. What needs an explicit decision (not yet visible in the repos)

* **Sync direction and cutover trigger.** Once `AvaIvy/Agent-Context` holds the canonical identity docs, does Solar-Pacific stop containing copies entirely, or does it keep a read-only pulled cache for local operations that need identity context without a network round-trip? Either is defensible; right now neither is written down anywhere in the reviewed material.
* **Who is allowed to write to which copy.** `GITHUB-IDENTITY.md` already flags that the shared Solar-Pacific tree has multiple committers and deliberately avoids a permanent git identity for that reason. The same discipline needs a stated rule for the Agent-Context repos: is only the agent (via its own GitHub identity) allowed to write there, with the operator reviewing, or is it open to any panel agent?
* **What "the local cache" actually contains.** The Copilot conversation describes `RootRecord Library/Agent Context/` as a working-copy cache of the three Agent-Context repos, plus a parent "handoff context as structural context" layer above it. That parent layer's contents aren't enumerated anywhere in the material reviewed so far — worth resolving alongside the Handoff-Context structure Grok proposed in Phase 1, since they're clearly meant to be the same or adjacent thing.

---

## 5. Recommendation

Treat this as a **finish-the-migration task**, not a **new-design task** — the direction was already chosen when the Agent-Context repos were created. Concretely, per agent:

1. Move `docs/IDENTITY.md`, `docs/ROLE-AND-BOUNDS.md`, `docs/PUBLIC-VOICE.md`, and avatar assets from `Solar-Pacific/agents/<agent>/` into that agent's own `Agent-Context` repo.
2. Delete `references/GITHUB-IDENTITY.md` from Solar-Pacific once the corresponding dedicated GitHub identity is confirmed live and the move in step 1 is complete.
3. Leave `SKILL.md` in place in Solar-Pacific — it's operational, not identity.
4. Relocate `notes/*-STOPPING-POINT.md` into the handoff-context structure identified in Pass 1, rather than under the agent's identity folder.
5. Write the sync-direction and write-permission rules down once, in `0-master-prompt`, so the next coverage AI doesn't have to reverse-engineer them from file contents the way this pass did.

---

*End of Pass 2. Next candidate for Pass 3: the `0-master-prompt/prompts/` numbered file structure already in the repo (`00-core` through `09-file-layout-style`) is a close, working match for the ADR-style contract Grok and Copilot both proposed inventing from scratch — worth confirming whether that structure should simply be declared canonical rather than superseded by a new one.*
