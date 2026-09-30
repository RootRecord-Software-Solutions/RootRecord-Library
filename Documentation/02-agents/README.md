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
