# 02 — Agents

Documentation about RootRecord agents. **Canonical identity packs do not live here.**

| Field | Value |
| --- | --- |
| **Canonical packs** | [`Agent Context/`](../../Agent%20Context/) at Library repo root |
| **Not a pack** | [CouncilPersona-shell.md](CouncilPersona-shell.md) — Pacific loader only. It reads these packs. It does not store them. |
| **Team constitution** | [Local Multi-Agent Team & Migration → Build](../10-AI-and-Agent-Runtime/Local-Multi-Agent-Team-and-Migration-to-Build-2026-09-28.md) |
| **Related WO** | [WO-AGENT-2026-09-27](../06-development/Work-Orders/Complete/AgentContext_CanonicalHome_Work_Order_WO-AGENT-2026-09-27.md) |

---

## Agent map

| Agent | Role | Pack |
| --- | --- | --- |
| **Ava Ivy** | Architect + public voice. Minecraft / RootMC personality | [Ava-Agent-Context](../../Agent%20Context/Ava-Agent-Context/) |
| **Carly Mal** | Security, billing, honesty seal, WO structure | [Carly-Agent-Context](../../Agent%20Context/Carly-Agent-Context/) |
| **Bruce** | Implement & operate | [Bruce-Agent-Context](../../Agent%20Context/Bruce-Agent-Context/) |
| **Root Record Global Updater** | Factual data, observations, operational information, professional help desk | [Global-Updater-Agent-Context](../../Agent%20Context/Global-Updater-Agent-Context/) |

Council pipeline: **Ava → Carly → Bruce**. That pipeline is not the Global Updater.

```text
Ava Ivy
→ Minecraft / RootMC
→ personality-driven gamer/community agent

Global Updater
→ professional RootRecord Discord
→ factual operational/data/help-desk agent
```

## Boundary

Library `Agent Context/` is the only editable home for who Ava, Bruce, Carly, and the Global Updater are: identity, principles, bounds, durable workflow, and `CONTEXT/`.

Pacific may hold server implementation. It must not hold a second copy of that identity. `Communications/CouncilPersona/scripts/personas.py` reads `IDENTITY.md`, `ROLE-AND-BOUNDS.md`, `PRINCIPLES.md`, and `WORKFLOW.md` from this tree, including `Global-Updater-Agent-Context`. There is no sync job. Telegram does not request the Global Updater voice.

`CONTEXT/`, changelogs, and the handoff template stay here and are not injected into every Telegram turn (NPU context 4096).

Database `AI/FLM/Personas/*.json` and the `*-telegram` Modelfiles are old runtime text plus sampling settings. They are not a place to edit identity. `agents/{ava-ivy,bruce-monitor,carly-mal}/` is not on the live Pacific tree. Leftover packets under old skills checkouts are historical.

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
