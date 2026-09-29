# WORK ORDER — RootRecord Ecosystem Migration & Repository Foundation

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-ECO-2026-09-27 |
| **Date** | 2026-09-27 (HST) |
| **Status** | IN PROGRESS — Pacific runtime cut over to Ecosystem Servers path |
| **Owner** | RootRecord |
| **Related** | Library online; WO-SRV; domain wiring 2026-09-28 |
| **Updated** | 2026-09-28 (HST) |

**Scope:** Establish clean ownership boundaries between the local `RootRecord-Ecosystem` tree and independent GitHub repositories; migrate durable knowledge and runtime artifacts out of the legacy single-tree model.

---

## 1. Intent

The long-term shape:

```text
RootRecord-Ecosystem
├─ 0 - Master-Prompt          # governance / identity / architecture (boot path)
├─ 1 - Servers                # deployed runtime systems
├─ 2 - RootRecord-Database    # generated data + telemetry + media
├─ 3 - RootRecord-Website     # public surface
├─ 4 - RootRecord-Node        # future distributed nodes
└─ 5 - RootRecord-Library     # durable knowledge / docs / agent context
```

**Rule of thumb:**

| Kind of material | Home |
| --- | --- |
| Runnable code / services | `1 - Servers` → matching GitHub runtime repo |
| Generated data, logs, media | `2 - RootRecord-Database` (and weather DB repo where applicable) |
| Public presentation | `3 - RootRecord-Website` |
| Future node deployments | `4 - RootRecord-Node` |
| Decisions, history, agent context, work orders | `5 - RootRecord-Library` |
| Always-on agent bootstrap | `0 - Master-Prompt` |

---

## 2. Current GitHub Reality (as of 2026-09-28)

### 2.1 Online and in use

| Repository | Owner | Role |
| --- | --- | --- |
| **RootRecord-Library** | `RootRecord-Software-Solutions` | Durable knowledge, agent context, architecture sessions, ops logs, work orders |
| **RootRecord-Pacific-Solar-Server** | `RootRecord-Software-Solutions` | **Primary desk runtime** (Automations domain live; other domains importing) |
| **US-Mainland-Server** | `rootrecordsoftwaresolutions` | Continuity node |
| **RootRecord-Website** | `rootrecordsoftwaresolutions` | Public Next.js surface |
| **RootRecord-Weather-Database** | `rootrecordsoftwaresolutions` | Generated weather data & media |

### 2.2 Completed

- [x] Org repo Library online and synced
- [x] Org repo **RootRecord-Pacific-Solar-Server** online
- [x] Live runtime path: `…/1 - Servers/1 - RootRecord-Pacific-Solar-Server`
- [x] Domain folders + Automations core wired (poller, jobs, stack, Communications/network)
- [x] Poller confirmed active from Ecosystem path (2026-09-28)
- [ ] Full domain import (energy, a-eyes, github, plumbing, telegram)
- [ ] `repos.conf` row(s) aligned to Ecosystem path
- [ ] Master-Prompt `08-repository-and-file-links.md` authored

### 2.3 Transitional friction

- Some `jobs.py` entries still call legacy `~/.ollama/skills/…` absolute paths for domains not yet imported
- Org placement: **Library + Pacific Server** under `RootRecord-Software-Solutions`; other operational repos under `rootrecordsoftwaresolutions`
- Prior remote `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server` is legacy for Pacific runtime

---

## 3. Ownership Contract (working draft)

### RootRecord-Library

- **GitHub:** https://github.com/RootRecord-Software-Solutions/RootRecord-Library
- **Contains:** agent contexts, architecture notes, human operator logs, work orders, ADRs, guides, handoffs
- **Does not contain:** runtime services, live telemetry, secrets, generated databases

### RootRecord Pacific Solar Server (runtime)

- **GitHub:** https://github.com/RootRecord-Software-Solutions/RootRecord-Pacific-Solar-Server
- **Local (live):** `/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server`
- **Contains:** Automations (poller/jobs/stack), Communications (network/cloudflare + messaging shells), Weather helpers, domain shells (Energy, Security, System, Logs, Github, Geology)
- **Does not contain:** long-term documentation archives, library agent packs, bulk generated data

### US Mainland Server

- **GitHub:** https://github.com/rootrecordsoftwaresolutions/US-Mainland-Server
- **Local (target):** `1 - Servers/2 - RootRecord-US-Mainland-Server`

### RootRecord-Website

- **GitHub:** https://github.com/rootrecordsoftwaresolutions/RootRecord-Website
- **Local:** `3 - RootRecord-Website`

### RootRecord-Database (local) + Weather Database (GitHub)

- **Local:** `2 - RootRecord-Database` / `/home/rootrecord/Database/`
- **GitHub weather publication:** https://github.com/rootrecordsoftwaresolutions/RootRecord-Weather-Database

### Master-Prompt

- **Local:** `0 - Master-Prompt`
- **Role:** first load for agents — answers *where does this go?*

**Boundary rule:** When ownership is ambiguous, prefer Library for decisions/history and Server for runnable code.

---

## 4. Migration checklist

### 4.1 Knowledge

- [x] Library repo online and auto-synced
- [x] Agent CONTEXT maps updated for Pacific path (2026-09-28)
- [x] WO-SRV / WO-CF updated for domain layout
- [ ] Master-Prompt repository links section

### 4.2 Runtime

- [x] Pacific server live under `1 - Servers/…`
- [x] Automations core path-wired and operator-verified
- [ ] Import remaining domains one at a time
- [ ] `repos.conf` path alignment

### 4.3 Data / Website / Node

- [ ] Keep generated content out of Library and runtime git trees
- [ ] Website continues via existing mirror
- [ ] Node: leave placeholder

---

## 5. Sync system (standing)

Catalog: `github/scripts/repos.conf` (may still list legacy skills path until updated)

| id | mode | local (desk) | github_slug |
| --- | --- | --- | --- |
| pacific / skills | inplace | **target** `…/1 - Servers/1 - RootRecord-Pacific-Solar-Server` | `RootRecord-Software-Solutions/RootRecord-Pacific-Solar-Server` |
| website | mirror | website worktree | `rootrecordsoftwaresolutions/RootRecord-Website` |
| mainland | inplace | mainland path | `rootrecordsoftwaresolutions/US-Mainland-Server` |
| library | inplace | `…/5 - RootRecord-Library` | `RootRecord-Software-Solutions/RootRecord-Library` |

Deploy standing rule: push → sync merge → `schedule-stack-reload` when runtime code is pulled.

---

## 6. Notes & constraints

- No force-push.
- Secrets stay out of git.
- Prefer structure over sprawl.
- Residual legacy runtime paths are retained only where the corresponding Pacific implementation has not yet passed required runtime verification and retirement criteria. For migrated functions, static source presence alone does not authorize legacy removal.

---

*Work order prepared 2026-09-27 HST. Updated 2026-09-28 HST after Pacific Automations domain wiring and live poller confirmation.*
