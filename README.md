# 🌺 RootRecord Library

> **The durable knowledge layer for RootRecord Software Solutions.**
>
> Architecture • agent context • operations • security • data notes • work orders

<p align="center">
  <a href="https://github.com/RootRecord-Software-Solutions"><strong>Organization</strong></a>
  ·
  <a href="https://github.com/RootRecord-Software-Solutions/RootRecord-Pacific-Solar-Server"><strong>Runtime</strong></a>
  ·
  <a href="https://github.com/RootRecord-Software-Solutions/RootRecord-Database"><strong>Database</strong></a>
  ·
  <a href="https://rootrecord.cloud"><strong>rootrecord.cloud</strong></a>
</p>

---

## 🧭 What this is

**RootRecord Library** is the versioned context and documentation layer for the RootRecord ecosystem.

It gives operators and agents a durable place to find the same architecture, constraints, work orders, operational records, and handoff context across sessions.

**This repository is documentation and context — not application runtime code.**

| Layer | Purpose |
| --- | --- |
| 🧠 **Agent Context** | Identity, principles, bounds, workflow, infrastructure maps, handoffs |
| 🏗️ **Architecture** | System design, migration records, decisions, canonical paths |
| 🛠️ **Operations** | Operator logs, recovery notes, runtime verification, security records. Current remaining-work list: `Documentation/01-operations/2026-09-30-whats-left-for-alexander.md` |
| 📋 **Work Orders** | Active migration and development work with explicit acceptance criteria |
| 📚 **Guides** | Standing practices and reusable how-to material |

---

## 🗺️ Canonical ecosystem

| Repository | Role |
| --- | --- |
| **[RootRecord-Ecosystem](https://github.com/RootRecord-Software-Solutions/RootRecord-Ecosystem)** | Public umbrella and this desk's git root |
| **[RootRecord-Library](https://github.com/RootRecord-Software-Solutions/RootRecord-Library)** | Durable docs, agent context & work orders |
| **[RootRecord-Pacific-Solar-Server](https://github.com/RootRecord-Software-Solutions/RootRecord-Pacific-Solar-Server)** | Primary Pacific runtime |
| **[RootRecord-Database](https://github.com/RootRecord-Software-Solutions/RootRecord-Database)** | Data, media & log layout |
| **[US-Mainland-Server](https://github.com/rootrecordsoftwaresolutions/US-Mainland-Server)** | Continuity node |
| **[RootRecord-Website](https://github.com/rootrecordsoftwaresolutions/RootRecord-Website)** | Public web surface |
| **[RootRecord-Weather-Database](https://github.com/rootrecordsoftwaresolutions/RootRecord-Weather-Database)** | Hawaiʻi weather data & media |

Historical and mirror repositories remain useful for lineage and inventory; active canonical org work belongs in the appropriate current repository.

---

## 📁 Repository map

```text
RootRecord-Library/
├─ Agent Context/
│  ├─ Ava-Agent-Context/
│  ├─ Bruce-Agent-Context/
│  └─ Carly-Agent-Context/
├─ Documentation/
│  ├─ 00-architecture/
│  ├─ 01-operations/
│  ├─ 02-agents/
│  ├─ 03-security/
│  ├─ 04-data/
│  ├─ 05-public-surface/
│  ├─ 06-development/
│  │  └─ Work-Orders/
│  ├─ 07-testing/
│  ├─ 08-ideas/
│  ├─ adr/
│  ├─ archive/
│  └─ schemas/
├─ Guides & Tutorials/
└─ README.md
```

### 📋 Work orders

**Single work-order home:**
[Documentation/06-development/Work-Orders/](./Documentation/06-development/Work-Orders/)

Work orders are the execution spine for active migrations and development. They carry scope, acceptance criteria, verification requirements, and retirement conditions.

### 🧠 Agent packs

Each agent pack follows the same basic spine:

`IDENTITY.md` · `PRINCIPLES.md` · `ROLE-AND-BOUNDS.md` · `WORKFLOW.md` · `HANDOFF-TEMPLATE.md` · `CONTEXT/` · `CHANGELOG.md`

- [Ava](./Agent%20Context/Ava-Agent-Context/)
- [Bruce](./Agent%20Context/Bruce-Agent-Context/)
- [Carly](./Agent%20Context/Carly-Agent-Context/)

---

## Current status — 2026-09-30 afternoon

Council chat on this desk uses NPU `llama3.2:3b`, on demand, context 4096, with no Ollama fallback. The sandbox answers. The live council and private DMs stay quiet. Generated state stays in Database `System/status/` and is not committed. The execution broker can read state and refuses restarts and agent builds. Interaction modes, the principal registry, and the Cursor handoff contract are in [INTERACTION-MODES.md](./Documentation/02-agents/INTERACTION-MODES.md). `cursor_api` ships off. Start at [HANDOFF.md](./Documentation/01-operations/HANDOFF.md). The 2026-09-29 section below is the record of that day, not the council model in use now.

## Current status — 2026-09-29 (HST)

G2 → G3 migration: the Pacific runtime is on the new Database root (`2 - RootRecord-Database`, Title-case folders). Post-reboot checks, Weather, NPU/FastFlowLM (`llama3.2:1b` on demand) and the Title-case rename are **PASS**. G2 legacy files are **KEPT** until Alexander signs off. Open items are tracked as BLOCKED / PROPOSED / VERIFY PENDING in WO-SRV.

- 🧪 **Testing thread:** [Documentation/07-testing/](./Documentation/07-testing/README.md) — one record per test run, plus the test-safety policy
- 💡 **Ideas & proposals:** [Documentation/08-ideas/](./Documentation/08-ideas/README.md) — every item PROPOSED until Alexander signs off
- 📝 **Overnight worklog:** [2026-09-29 System Operator Worklog — Overnight](./Documentation/01-operations/0%20-%20Human%20Operator%20Work%20Logs/2026-09-29%20System%20Operator%20Worklog%20%E2%80%94%20Overnight.md) (includes the "Needs Alexander sign-off" list)
- 🗂️ **Migration index:** [MIGRATION-DOCS-INDEX](./Documentation/00-architecture/MIGRATION-DOCS-INDEX-2026-09-28.md)

### Where things stand — 16:25 HST (paused)

- **LANDED / PASS today:** AWS feed trim + auto-trim cron; `www.rootrecord.cloud` back (200) with the P0 static-allowlist fix; globe overlay v2 on AWS (spin, click info, AWS Ohio node); AWS fallback Phase 2 on the trimmed t3.micro profile (908 MB RAM) with Root Monitor write mode; Root Monitor toggle buttons + camera button; 9 Android apps imported (80.7 MB); old-repo matrix 35 / 22 / 33.
- **VERIFY PENDING:** the globe in a real browser, a real fallback on AWS, a relay send.
- **Waiting on Alexander:** the consolidated list in the worklog's [State at pause, 16:25 HST](./Documentation/01-operations/0%20-%20Human%20Operator%20Work%20Logs/2026-09-29%20System%20Operator%20Worklog%20%E2%80%94%20Overnight.md#state-at-pause-1625-hst-2026-09-29) section.
- **New docs:** [Android-Apps-Inventory](./Documentation/00-architecture/Android-Apps-Inventory.md), [US-Mainland-Server](./Documentation/00-architecture/US-Mainland-Server.md), [Control-Panel-GTK (Root Monitor)](./Documentation/00-architecture/Control-Panel-GTK.md); all linked from the migration index.

---

## 🔄 How the ecosystem stays in sync

The Library is authored on the Solar Pacific desk. This desk publishes it through the `library` mirror row and through the umbrella `ecosystem` row. The Library directory in this checkout is not its own git repository.

```text
Desk edit
   │
   ▼
Git repository
   │
   ▼
Automated GitHub sync
   │
   ▼
GitHub — durable shared context
   │
   ▼
Other agents / desks can inspect current commits
```

GitHub commits therefore act as durable checkpoints between sessions. **A pushed path is not, by itself, proof that a runtime is deployed or verified.** Runtime state remains subject to the documented verification gates.

---

## 🧱 Operating principles

- **Preserve source identity** — records remain attributable.
- **Prefer structure over sprawl** — use the numbered documentation layout.
- **No force-push** — history is part of the operational record.
- **Separate code from context** — runtime belongs in runtime repositories; durable knowledge belongs here.
- **Verify before declaring** — landed, running, verified, and retired are distinct states.
- **Docs-only hygiene is safe** — README and documentation improvements do not imply runtime migration.

---

## 🔗 Quick links

| Resource | Link |
| --- | --- |
| GitHub organization | https://github.com/RootRecord-Software-Solutions |
| Public umbrella | https://github.com/RootRecord-Software-Solutions/RootRecord-Ecosystem |
| Pacific runtime | https://github.com/RootRecord-Software-Solutions/RootRecord-Pacific-Solar-Server |
| Database | https://github.com/RootRecord-Software-Solutions/RootRecord-Database |
| Work orders | [Documentation/06-development/Work-Orders/](./Documentation/06-development/Work-Orders/) |
| Public site | https://rootrecord.cloud |
| Contact | rootrecord@outlook.com |

<p align="center">
  <strong>Root Record Software Solutions</strong><br/>
  <em>Oriented from Hawaiʻi Island · software · infrastructure · automation · AI · distributed systems</em>
</p>
