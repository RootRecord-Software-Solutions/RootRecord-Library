# 02 — Agents

Documentation about RootRecord agents. **Canonical identity packs do not live here.**

| Field | Value |
| --- | --- |
| **Canonical packs** | [`Agent Context/`](../../Agent%20Context/) at Library repo root |
| **Team constitution** | [Local Multi-Agent Team & Migration → Build](../00-architecture/Local-Multi-Agent-Team-and-Migration-to-Build-2026-09-28.md) |
| **Related WO** | [WO-AGENT-2026-09-27](../06-development/Work-Orders/Complete/AgentContext_CanonicalHome_Work_Order_WO-AGENT-2026-09-27.md) |

---

## Agent map

| Agent | Role | Pack |
| --- | --- | --- |
| **Ava Ivy** | Architect + public voice | [Ava-Agent-Context](../../Agent%20Context/Ava-Agent-Context/) |
| **Carly Mal** | Security, billing, honesty seal, WO structure | [Carly-Agent-Context](../../Agent%20Context/Carly-Agent-Context/) |
| **Bruce** | Implement & operate | [Bruce-Agent-Context](../../Agent%20Context/Bruce-Agent-Context/) |

Pipeline: **Ava → Carly → Bruce**.

## Interaction contracts

These files are the mode, identity, and handoff layer. They do not replace the capability registry or the machine work orders.

| Contract | Path |
| --- | --- |
| Principals | [identity/principal-registry.json](identity/principal-registry.json) |
| Modes | [modes/mode-policy.md](modes/mode-policy.md) |
| Requests | [requests/request-lifecycle.md](requests/request-lifecycle.md) |
| Cursor handoff | [handoff/cursor-handoff-schema.json](handoff/cursor-handoff-schema.json) |
| Reports | [reports/execution-report-schema.json](reports/execution-report-schema.json), [reports/verification-report-schema.json](reports/verification-report-schema.json) |
| Decision | [0006](../00-architecture/Decisions/0006-interaction-modes.md) |
| How to read it | [INTERACTION-MODES.md](INTERACTION-MODES.md) |

`interaction_mode` is a request mode. The 2026-09-28 “Migrate mode → build mode” section is a migration phase. The names are not the same thing.

Standing strategy: same roles on small local NPU models or future larger capacity; **migrate & stabilize first**, then **build**. Truth gate: path landed ≠ runtime verified ≠ legacy retired.

## Empty subfolders under this path

Any `Ava-Agent-Context/`, `Bruce-Agent-Context/`, or `Carly-Agent-Context/` directories **under** `Documentation/02-agents/` are placeholders only. Do **not** maintain a second copy of IDENTITY/ROLE files here — edit the root `Agent Context/` packs.

## Personal mirrors

- `AvaIvy/AvaIvy-Agent-Context` — personal mirror; Library pack is authority for org work  
- `CarlyMal/Carly-Agent-Context` — personal pack; sync toward Library when bounds change  

## Decision (2026-09-29)

Diff of `Agent Context/` (34 files) against `Documentation/02-agents/` (5 files): the only shared names are four identical `.gitkeep` placeholders. `02-agents/README.md` is the index and is not a second pack. Placeholder folders stay. Nothing was deleted.

Personal remotes `AvaIvy/Agent-Context` and `CarlyMal/Carly-Agent-Context` stay separate. This desk does not sync them. The Library pack is the org authority.

*README updated 2026-09-29 HST — canonical-home decision recorded.*
