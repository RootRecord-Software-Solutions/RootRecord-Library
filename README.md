# 🎺 RootRecord Library

> **The shared knowledge base for Root Record Software Solutions** — agent context, architecture records, operations logs, and guides that keep the ecosystem coherent across desks, agents, and time.

[![Org](https://img.shields.io/badge/org-RootRecord--Software--Solutions-0B3D2E?style=flat-square)](https://github.com/RootRecord-Software-Solutions)
[![Runtime](https://img.shields.io/badge/runtime-Pacific--Solar--Server-2F6FED?style=flat-square)](https://github.com/RootRecord-Software-Solutions/RootRecord-Pacific-Solar-Server)
[![Locale](https://img.shields.io/badge/base-Hawai%CA%BBi-C8102E?style=flat-square)](https://rootrecord.cloud)

---

## Canonical homes (as of 2026-09-28)

| Role | Owner | Repository |
| --- | --- | --- |
| **Durable docs & agent context** | Org | [RootRecord-Library](https://github.com/RootRecord-Software-Solutions/RootRecord-Library) (this repo) |
| **Primary Pacific runtime** | Org | [RootRecord-Pacific-Solar-Server](https://github.com/RootRecord-Software-Solutions/RootRecord-Pacific-Solar-Server) |
| **Data / log layout (source of truth)** | Org | [RootRecord-Database](https://github.com/RootRecord-Software-Solutions/RootRecord-Database) |
| Continuity node | User account | [US-Mainland-Server](https://github.com/rootrecordsoftwaresolutions/US-Mainland-Server) |
| Public website | User account | [RootRecord-Website](https://github.com/rootrecordsoftwaresolutions/RootRecord-Website) |
| Weather data & media | User account | [RootRecord-Weather-Database](https://github.com/rootrecordsoftwaresolutions/RootRecord-Weather-Database) |

**Historical / read-only:** personal accounts `RootRecord` and `RootMC`, inventory mirrors under `rootrecordsoftwaresolutions/mirror-*`, and legacy `Solar-Pacific-RootRecord-Server` / `-Old`.

**Migration posture:** inventory and mirrors are done; active feature work lands in the org (canonical public) or primary non-mirror repos under `rootrecordsoftwaresolutions` (ops / solar / Ava). No code is changed by documentation-only updates in this repo.

---

## What this repository is

**RootRecord Library** is the durable, versioned documentation and context layer for the RootRecord ecosystem. It is **not** application source code. It holds the material that agents, operators, and future sessions need in order to act with continuity:

| Layer | Purpose |
| --- | --- |
| **Agent Context** | Identity, principles, bounds, workflow, handoff templates, and product/infrastructure maps for Ava, Bruce, and Carly |
| **Documentation** | Architecture sessions, operations work logs, security notes, data notes, public surface, development work orders, ADRs |
| **Guides & Tutorials** | How-to material for turning messy AI output into clean plans and other standing practices |

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
│   ├─ Ava-Agent-Context/
│   ├─ Bruce-Agent-Context/
│   └─ Carly-Agent-Context/
├─ Documentation/
│   ├─ 00-architecture/
│   ├─ 01-operations/
│   ├─ 02-agents/
│   ├─ 03-security/
│   ├─ 04-data/
│   ├─ 05-public-surface/
│   ├─ 06-development/
│   │   └─ Work-Orders/     # single work-order home
│   ├─ adr/
│   ├─ archive/
│   └─ schemas/
├─ Guides & Tutorials/
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

Session handoffs use each pack’s `HANDOFF-TEMPLATE.md` — no separate top-level Handoff-Context folder.

---

## Documentation index

| Section | Contents |
| --- | --- |
| **00-architecture** | Multi-model restructuring sessions and system design exploration |
| **01-operations** | Human operator work logs, checkpoints, reinstall / recovery notes |
| **02-agents** | Agent documentation mirrors and indexes |
| **03-security** | Security notes and posture records |
| **04-data** | Data layout and integrity notes |
| **05-public-surface** | Public-facing surface documentation |
| **06-development** | Work orders and development records |
| **adr** | Architecture decision records |
| **archive** | Historical material retained for audit |
| **schemas** | Shared schema definitions |

### Work orders

**One folder only:** [`Documentation/06-development/Work-Orders/`](./Documentation/06-development/Work-Orders/)

Unified index of active ops backlog + domain/feature proposals. (The old space-named `Work Orders/` duplicate was removed 2026-09-28.)

---

## Guides & Tutorials

Practical standing guides live under [`Guides & Tutorials/`](./Guides%20%26%20Tutorials/), including:

- **How to turn messy AI output into one clean plan** — intake, structure, and execution discipline for multi-model sessions.

---

## How this stays current

Library content is authored on the Solar Pacific desk and published through the RootRecord Git synchronization workflow:

1. Local edits under `RootRecord-Ecosystem/5 - RootRecord-Library`
2. Catalogued in `repos.conf` as id `library` (EXISTS mode)
3. Picked up by `github_sync_all` (≈300s) via `sync-all.sh` → `push-repo-once.sh`
4. Merged safely (no force-push); conflicts abort and preserve local history

Related infrastructure repos:

| Repository | Role |
| --- | --- |
| [RootRecord-Pacific-Solar-Server](https://github.com/RootRecord-Software-Solutions/RootRecord-Pacific-Solar-Server) | Primary desk runtime |
| [RootRecord-Database](https://github.com/RootRecord-Software-Solutions/RootRecord-Database) | Official data & log layout |
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
- **Docs-only hygiene is allowed anytime** — README and work-order index updates do not imply code migration.

---

## Quick links

| Resource | URL |
| --- | --- |
| Organization | [github.com/RootRecord-Software-Solutions](https://github.com/RootRecord-Software-Solutions) |
| Pacific runtime | [RootRecord-Pacific-Solar-Server](https://github.com/RootRecord-Software-Solutions/RootRecord-Pacific-Solar-Server) |
| Database | [RootRecord-Database](https://github.com/RootRecord-Software-Solutions/RootRecord-Database) |
| Work orders | [Work-Orders/](./Documentation/06-development/Work-Orders/) |
| Cloud / status | [rootrecord.cloud](https://rootrecord.cloud) |
| Marketing & accounts | [rootrecord.info](https://rootrecord.info) |
| Contact | rootrecord@outlook.com |

---

<p align="center">
  <strong>Root Record Software Solutions</strong><br/>
  <em>Oriented from Hawaiʻi Island · Building software, infrastructure, automation, AI, and distributed systems</em>
</p>
