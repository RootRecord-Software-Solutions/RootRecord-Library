# WORK ORDER — RootRecord Ecosystem Migration & Repository Foundation

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-ECO-2026-09-27 |
| **Date** | 2026-09-27 (HST) |
| **Status** | OPEN — Active migration night |
| **Owner** | RootRecord |
| **Related** | Library online; github_sync_all catalog includes `library` |

**Scope:** Establish clean ownership boundaries between the local `RootRecord-Ecosystem` tree and independent GitHub repositories; migrate durable knowledge and runtime artifacts out of the legacy single-tree model; leave temporary READMEs alone until each new repo is intentionally filled.

---

## 1. Intent

Tonight’s priority is **maximum migration from the old system** with **documentation that matches reality**, not perfect final content in every folder.

The long-term shape is already agreed in principle:

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
| Always-on agent bootstrap (“where does this go?”) | `0 - Master-Prompt` |

Do **not** treat temporary README placeholders as finished product. Do **not** rewrite them until the corresponding repo is intentionally populated.

---

## 2. Current GitHub Reality (as of 2026-09-27)

### 2.1 Online and in use

| Repository | Owner | Role |
| --- | --- | --- |
| **RootRecord-Library** | `RootRecord-Software-Solutions` | Durable knowledge, agent context, architecture sessions, ops logs, work orders |
| **Solar-Pacific-RootRecord-Server** | `rootrecordsoftwaresolutions` | Primary desk skills / poller / automations (legacy tree still the live runtime source) |
| **US-Mainland-Server** | `rootrecordsoftwaresolutions` | Continuity node |
| **RootRecord-Website** | `rootrecordsoftwaresolutions` | Public Next.js surface |
| **RootRecord-Weather-Database** | `rootrecordsoftwaresolutions` | Generated weather data & media |

### 2.2 Completed this session (Library + sync)

- [x] Org repo created / confirmed: `RootRecord-Software-Solutions/RootRecord-Library`
- [x] Local tree initialized and committed under `5 - RootRecord-Library`
- [x] `repos.conf` entry: id `library`, mode `inplace`, path `…/5 - RootRecord-Library`, slug org Library
- [x] `setup-remote.sh library` + first successful sync path (unrelated-histories merge handled)
- [x] Professional Library README published (do not churn further tonight unless requested)
- [x] `jobs.py` descriptions updated so `github_sync_all` / setup-remotes language includes library

### 2.3 Known transitional friction

- Live runtime still largely lives under `~/.ollama/skills` (Solar-Pacific skills tree), not yet a clean `1 - Servers/1 - RootRecord-Pacific-Solar-Server` layout on disk as the sole source of truth.
- Org placement differs: **Library** under `RootRecord-Software-Solutions`; operational repos under `rootrecordsoftwaresolutions`. Document that deliberately when Master-Prompt map is written.
- Mistaken user-account repo `rootrecordsoftwaresolutions/RootRecord-Library` may still exist; safe to delete in UI when convenient (org Library is canonical).
- Master-Prompt path `0 - Master-Prompt/prompts/08-repository-and-file-links.md` is the intended home for the short ownership contract; **not authored yet** (wait until new-repo foundations are clearer).

---

## 3. Ownership Contract (working draft — for agents and operators)

Use this until the Master-Prompt section is formalized.

### RootRecord-Library

- **GitHub:** https://github.com/RootRecord-Software-Solutions/RootRecord-Library
- **Contains:** agent contexts, architecture notes, human operator logs, work orders, ADRs, guides, handoffs, historical decisions
- **Does not contain:** runtime services, live telemetry, secrets, generated databases

### Solar-Pacific / Pacific Solar Server (runtime)

- **GitHub (current):** https://github.com/rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server
- **Local (target shape):** `1 - Servers/1 - RootRecord-Pacific-Solar-Server`
- **Contains:** automations, energy, cameras, weather services, system scripts, server configuration
- **Does not contain:** long-term documentation archives, library agent packs, bulk generated data

### US Mainland Server

- **GitHub:** https://github.com/rootrecordsoftwaresolutions/US-Mainland-Server
- **Local (target shape):** `1 - Servers/2 - RootRecord-US-Mainland-Server`
- **Contains:** continuity / secondary node logic and communications

### RootRecord-Website

- **GitHub:** https://github.com/rootrecordsoftwaresolutions/RootRecord-Website
- **Local:** `3 - RootRecord-Website`
- **Contains:** public site code and public assets

### RootRecord-Database (local) + Weather Database (GitHub)

- **Local:** `2 - RootRecord-Database` — energy, system, media, users, logs, geology, weather staging, etc.
- **GitHub weather publication:** https://github.com/rootrecordsoftwaresolutions/RootRecord-Weather-Database
- **Contains:** generated operational data and media; **not** source code or agent identity

### RootRecord-Node

- **Local:** `4 - RootRecord-Node` (placeholder / future)
- **Contains:** future distributed node deployment material only

### Master-Prompt

- **Local:** `0 - Master-Prompt`
- **Role:** first load for agents — core rules, architecture, agents, development, operations, energy, handoff, current state, **repository links**, file-layout style
- **Does not replace** Library deep history; answers *where does this go?* not *why did we choose this over five sessions?*

**Boundary rule:** When ownership is ambiguous, prefer Library for decisions/history and Server for runnable code. Do not invent a new home without updating the ownership map.

---

## 4. Migration checklist (tonight-oriented)

### 4.1 Protect and publish knowledge (high priority)

- [x] Library repo online and auto-synced
- [ ] Confirm desk `push-repo-once.sh library` stays clean after further local edits
- [ ] Continue moving architecture / ops / agent material into Library sections already present
- [ ] Add further work orders under `Documentation/06-development/Work Orders/` as streams open
- [ ] Optionally add `Documentation/00-architecture/Repository Ownership Model.md` once repo set stabilizes (deep *why*; not blocking)

### 4.2 Runtime (do not break the desk)

- [ ] Keep Solar-Pacific skills poller / `github_sync_all` healthy during moves
- [ ] Treat `1 - Servers/…` as the **target** layout; only cut over when paths in `jobs.py`, scripts, and `repos.conf` are updated together
- [ ] Mainland remains optional until its local `.git` / path is intentional

### 4.3 Data

- [ ] Keep generated content out of Library and out of runtime git trees
- [ ] Weather publication continues via existing weather sync path + Weather-Database repo
- [ ] Document which Database subtrees are local-only vs published

### 4.4 Website & Node

- [ ] Website continues via existing mirror worktree + `RootRecord-Website`
- [ ] Node: leave placeholder; no forced content

### 4.5 Master-Prompt (foundation, not tonight’s essay)

- [ ] When ready: expand `prompts/08-repository-and-file-links.md` with short canonical map + boundary rule only
- [ ] Keep `MASTER-PROMPT.md` / `prompts.yaml` load path intact
- [ ] Do not paste full ecosystem tree into boot prompts

### 4.6 Explicit non-goals tonight

- Rewriting temporary READMEs across new/empty repos
- Force-push or history rewrite on any canonical remote
- Moving secrets into git
- Finalizing every new repo name before the physical cutover is designed

---

## 5. Sync system (standing)

Catalog: `github/scripts/repos.conf` (tab-separated)

| id | mode | local (desk) | github_slug |
| --- | --- | --- | --- |
| skills | inplace | `~/.ollama/skills` | `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server` |
| website | mirror | `~/.ollama/skills/website/site` | `rootrecordsoftwaresolutions/RootRecord-Website` |
| mainland | inplace | `~/.ollama/skills/us-mainland-server` | `rootrecordsoftwaresolutions/US-Mainland-Server` |
| library | inplace | `…/RootRecord-Ecosystem/5 - RootRecord-Library` | `RootRecord-Software-Solutions/RootRecord-Library` |

- Cycle: `github_sync_all` ~300s → `sync-all.sh` → `push-repo-once.sh <id>`
- Rules: no force-push; merge conflicts abort and preserve local history; oversized files blocked by `MAX_FILE_MB`

When a **new** runtime or knowledge repo is ready: add a `repos.conf` row, create the remote under the correct org, `setup-remote.sh <id>`, then first push.

---

## 6. Suggested order of operations (when you resume this thread)

1. Finish tonight’s content moves into Library and Database without breaking the poller.
2. List the **new** repos you intend to create (exact names + org + local path under Ecosystem).
3. For each: empty remote (prefer **no** auto-README if local history already exists), `repos.conf` row, setup-remote, first push.
4. Only then expand Master-Prompt `08-repository-and-file-links.md` to match the final set.
5. Only then replace temporary READMEs with real product docs.

---

## 7. Open items / room for additions

**Additional requirements:**

- Exact final names for Pacific Solar Server cutover under `1 - Servers/`
- Whether Master-Prompt itself becomes its own GitHub repo or stays desk-only / skills-linked
- Database publication policy beyond weather
- Node architecture first milestone
- Cleanup of `rootrecordsoftwaresolutions/RootRecord-Library` (non-canonical)
- 
- 

---

## 8. Notes & constraints

- Library README is already professional; **leave it** unless content structure changes require an update.
- Agent context packs under Library are the durable identity layer; keep Master-Prompt as the boot contract, not a second full copy of every pack.
- Deploy standing rule for desk code: push → `github_sync_all` merge → `schedule-stack-reload` when skills code is pulled.
- Prefer structure over sprawl: numbered Documentation sections and the agent-pack spine already exist—use them.

---

*Work order prepared 2026-09-27 HST from live Library tree, github_sync catalog, and migration discussion. Temporary READMEs intentionally not modified.*
