# 02 — Agents

Documentation about RootRecord agents. **Canonical identity packs do not live here.**

| Field | Value |
| --- | --- |
| **Canonical packs** | [`Agent Context/`](../../Agent%20Context/) at Library repo root |
| **Not a pack** | [CouncilPersona-shell.md](CouncilPersona-shell.md) — Pacific loader only. It reads these packs. It does not store them. |
| **Team constitution** | [Local Multi-Agent Team & Migration → Build](../10-AI-and-Agent-Runtime/Local-Multi-Agent-Team-and-Migration-to-Build-2026-09-28.md) |
| **Related WO** | [WO-AGENT-2026-09-27](../06-Development/Work-Orders/Complete/AgentContext_CanonicalHome_Work_Order_WO-AGENT-2026-09-27.md) |

---

## Agent map

| Agent | Role | Pack |
| --- | --- | --- |
| **Ava Ivy** | Architect + public voice. Minecraft / RootMC personality | [Ava-Agent-Context](../../Agent%20Context/Ava-Agent-Context/) |
| **Carly Mal** | Security, billing, honesty seal, WO structure | [Carly-Agent-Context](../../Agent%20Context/Carly-Agent-Context/) |
| **Bruce** | Implement & operate | [Bruce-Agent-Context](../../Agent%20Context/Bruce-Agent-Context/) |
| **Root Record Global Updater** | Factual data, observations, operational information, professional help desk | [Global-Updater-Agent-Context](../../Agent%20Context/Global-Updater-Agent-Context/) |
| **Wren** | Root Record Documenter. Writes the current fact into the existing Library page and the master prompt | [Documenter-Agent-Context](../../Agent%20Context/Documenter-Agent-Context/) |
| **Cove** | Root Record Web. Keeps the public page in Pacific `Website/Home/` | [Web-Agent-Context](../../Agent%20Context/Web-Agent-Context/) |

Council pipeline: **Ava → Carly → Bruce**. That pipeline is not the Global Updater, not Wren, and not Cove.

Fleet rule (Alexander via Master, 2026-10-02): any agent that finishes work that produced changes sends Wren a change summary so the Documenter can update the Library. Ecosystem work stays on the local desk checkout only.

```text
Ava Ivy
→ Minecraft / RootMC
→ personality-driven gamer/community agent

Global Updater
→ professional RootRecord Discord
→ factual operational/data/help-desk agent

Wren (Documenter)
→ Library and master prompt
→ writes the current fact into the existing page

Cove (Web)
→ Pacific Website/Home/
→ the public page Vercel publishes
```

## Boundary

Library `Agent Context/` is the only editable home for who Ava, Bruce, Carly, the Global Updater, Wren, and Cove are: identity, principles, bounds, durable workflow, and `CONTEXT/`.

Pacific may hold server implementation. It must not hold a second copy of that identity. `Communications/CouncilPersona/scripts/personas.py` reads `IDENTITY.md`, `ROLE-AND-BOUNDS.md`, `PRINCIPLES.md`, and `WORKFLOW.md` from this tree, including `Global-Updater-Agent-Context`. It does not load `Documenter-Agent-Context` or `Web-Agent-Context`. There is no sync job. Telegram does not request the Global Updater, Wren, or Cove.

`CONTEXT/`, changelogs, and the handoff template stay here and are not injected into every Telegram turn (NPU context 4096).

Database `AI/FLM/Personas/*.json` and the `*-telegram` Modelfiles are old runtime text plus sampling settings. They are not a place to edit identity. `agents/{ava-ivy,bruce-monitor,carly-mal}/` is not on the live Pacific tree. Leftover packets under old skills checkouts are historical.

## Interaction contracts

These files are the mode, identity, and handoff layer. They do not replace the capability registry or the machine work orders.

| Contract | Path |
| --- | --- |
| Principals | [Identity/principal-registry.json](Identity/principal-registry.json) |
| Modes | [Modes/mode-policy.md](Modes/mode-policy.md) |
| Requests | [Requests/request-lifecycle.md](Requests/request-lifecycle.md) |
| Cursor handoff | [Handoff/cursor-handoff-schema.json](Handoff/cursor-handoff-schema.json) |
| Reports | [Reports/execution-report-schema.json](Reports/execution-report-schema.json), [Reports/verification-report-schema.json](Reports/verification-report-schema.json) |
| Decision | [0006](../00-Architecture/Decisions/0006-interaction-modes.md) |
| How to read it | [INTERACTION-MODES.md](INTERACTION-MODES.md) |

`interaction_mode` is a request mode. The 2026-09-28 “Migrate mode → build mode” section is a migration phase. The names are not the same thing.

Standing strategy: same roles on small local NPU models or future larger capacity; **migrate & stabilize first**, then **build**. Truth gate: path landed ≠ runtime verified ≠ legacy retired.

## Empty subfolders under this path

Any `Ava-Agent-Context/`, `Bruce-Agent-Context/`, `Carly-Agent-Context/`, `Documenter-Agent-Context/`, or `Web-Agent-Context/` directories **under** `Documentation/02-Agents/` are placeholders only. Do **not** maintain a second copy of IDENTITY/ROLE files here — edit the root `Agent Context/` packs.

## Personal mirrors

- `AvaIvy/AvaIvy-Agent-Context` — personal mirror; Library pack is authority for org work  
- `CarlyMal/Carly-Agent-Context` — personal pack; sync toward Library when bounds change  

## Decision (2026-09-29)

Diff of `Agent Context/` (34 files) against `Documentation/02-Agents/` (5 files): the only shared names are four identical `.gitkeep` placeholders. `02-Agents/README.md` is the index and is not a second pack. Placeholder folders stay. Nothing was deleted.

Personal remotes `AvaIvy/Agent-Context` and `CarlyMal/Carly-Agent-Context` stay separate. This desk does not sync them. The Library pack is the org authority.

*README updated 2026-09-29 HST — canonical-home decision recorded.*
