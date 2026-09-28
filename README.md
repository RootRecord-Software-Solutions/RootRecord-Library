# 🌺 RootRecord Library

> **The shared knowledge base for Root Record Software Solutions** — agent context, architecture records, operations logs, guides, and handoff material that keep the ecosystem coherent across desks, agents, and time.

[![Org](https://img.shields.io/badge/org-RootRecord--Software--Solutions-0B3D2E?style=flat-square)](https://github.com/RootRecord-Software-Solutions)
[![Runtime](https://img.shields.io/badge/runtime-Pacific--Solar--Server-2F6FED?style=flat-square)](https://github.com/RootRecord-Software-Solutions/RootRecord-Pacific-Solar-Server)
[![Locale](https://img.shields.io/badge/base-Hawai%CA%BBi-C8102E?style=flat-square)](https://rootrecord.cloud)

---

## What this repository is

**RootRecord Library** is the durable, versioned documentation and context layer for the RootRecord ecosystem. It is **not** application source code. It holds the material that agents, operators, and future sessions need in order to act with continuity:

| Layer | Purpose |
| --- | --- |
| **Agent Context** | Identity, principles, bounds, workflow, and product/infrastructure maps for Ava, Bruce, and Carly |
| **Documentation** | Architecture sessions, operations work logs, security notes, data notes, public surface, development work orders, ADRs |
| **Guides & Tutorials** | How-to material for turning messy AI output into clean plans and other standing practices |
| **Handoff-Context** | Structured transfer points between sessions and operators |

Desk path (Solar Pacific):

```text
/home/rootrecord/RootRecord-Ecosystem/5 - RootRecord-Library
```

GitHub org home:

```text
https://github.com/RootRecord-Software-Solutions/RootRecord-Library
```

---

## Repository map

```text
RootRecord-Library/
├─ Agent Context/
│   ├─ Ava-Agent-Context/      # Primary coordination / architecture persona
│   ├─ Bruce-Agent-Context/    # Monitoring & operational awareness
│   └─ Carly-Agent-Context/    # Communications & public surface
├─ Documentation/
│   ├─ 00-architecture/       # Restructuring sessions, system design notes
│   ├─ 01-operations/         # Human operator work logs & checkpoints
│   ├─ 02-agents/             # Agent-facing documentation index
│   ├─ 03-security/
│   ├─ 04-data/
│   ├─ 05-public-surface/
│   ├─ 06-development/        # Work orders and build notes
│   ├─ adr/                   # Architecture decision records
│   ├─ archive/
│   └─ schemas/
├─ Guides & Tutorials/
├─ Handoff-Context/
└─ README.md
```

---

## Agent Context

Each agent pack follows a consistent spine so handoffs stay predictable:

| File | Role |
| --- | --- |
| `IDENTITY.md` | Who the agent is |
| `PRINCIPLES.md` | Standing values and constraints |
| `ROLE-AND-BOUNDS.md` | What is in scope vs out of scope |
| `WORKFLOW.md` | How the agent is expected to operate |
| `HANDOFF-TEMPLATE.md` | Standard transfer format |
| `CONTEXT/` | Infrastructure, products, repos |
| `CHANGELOG.md` | Material changes to the pack |
| `README.md` | Pack entry point |

| Agent | Path |
| --- | --- |
| **Ava** | [`Agent Context/Ava-Agent-Context/`](./Agent%20Context/Ava-Agent-Context/) |
| **Bruce** | [`Agent Context/Bruce-Agent-Context/`](./Agent%20Context/Bruce-Agent-Context/) |
| **Carly** | [`Agent Context/Carly-Agent-Context/`](./Agent%20Context/Carly-Agent-Context/) |

---

## Documentation index

| Section | Contents |
| --- | --- |
| **00-architecture** | Multi-model restructuring sessions (ChatGPT, Copilot, Grok, Claude) and system design exploration |
| **01-operations** | Human operator work logs, checkpoints, reinstall / recovery notes |
| **02-agents** | Agent documentation mirrors and indexes |
| **03-security** | Security notes and posture records |
| **04-data** | Data layout and integrity notes |
| **05-public-surface** | Public-facing surface documentation |
| **06-development** | Work orders and development records |
| **adr** | Architecture decision records |
| **archive** | Historical material retained for audit |
| **schemas** | Shared schema definitions |

---

## Guides & Tutorials

Practical standing guides live under [`Guides & Tutorials/`](./Guides%20%26%20Tutorials/), including:

- **How to turn messy AI output into one clean plan** — intake, structure, and execution discipline for multi-model sessions.

---

## How this stays current

Library content is authored on the Solar Pacific desk and published through the RootRecord Git synchronization workflow:

1. Local edits under `RootRecord-Ecosystem/5 - RootRecord-Library`
2. Catalogued in `repos.conf` as id `library` (inplace mode)
3. Picked up by `github_sync_all` (≈300s) via `sync-all.sh` → `push-repo-once.sh`
4. Merged safely (no force-push); conflicts abort and preserve local history

Related infrastructure repos:

| Repository | Role |
| --- | --- |
| [RootRecord-Pacific-Solar-Server](https://github.com/RootRecord-Software-Solutions/RootRecord-Pacific-Solar-Server) | Primary desk runtime (Automations + domain layout) |
| [US-Mainland-Server](https://github.com/rootrecordsoftwaresolutions/US-Mainland-Server) | Secondary continuity node |
| [RootRecord-Website](https://github.com/rootrecordsoftwaresolutions/RootRecord-Website) | Public Next.js surface |
| [RootRecord-Weather-Database](https://github.com/rootrecordsoftwaresolutions/RootRecord-Weather-Database) | Hawaiʻi weather data & media |

Live Pacific runtime path:

```text
/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server
```

---

## Principles for contributors

- **Preserve source identity** — session notes and operator logs remain attributable.
- **Prefer structure over sprawl** — use the numbered Documentation sections and agent pack spine.
- **No force-push** — history is part of the operational record.
- **Desk is authoritative for live ops** — this repo is the published, shareable layer of that desk knowledge.
- **File layout is standing** — keep section banners and templates where they exist in sibling systems.

---

## Quick links

| Resource | URL |
| --- | --- |
| Organization | [github.com/RootRecord-Software-Solutions](https://github.com/RootRecord-Software-Solutions) |
| Pacific runtime | [RootRecord-Pacific-Solar-Server](https://github.com/RootRecord-Software-Solutions/RootRecord-Pacific-Solar-Server) |
| Cloud / status | [rootrecord.cloud](https://rootrecord.cloud) |
| Marketing & accounts | [rootrecord.info](https://rootrecord.info) |
| Contact | rootrecord@outlook.com |

---

<p align="center">
  <strong>Root Record Software Solutions</strong><br/>
  <em>Oriented from Hawaiʻi Island · Building software, infrastructure, automation, AI, and distributed systems</em>
</p>
