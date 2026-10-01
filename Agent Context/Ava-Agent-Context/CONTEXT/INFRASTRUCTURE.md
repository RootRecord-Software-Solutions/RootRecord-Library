# Infrastructure Context

## RootRecord Pacific Solar Server
Primary operational environment (Hawaiʻi desk).

**Git root for this path:** `RootRecord-Software-Solutions/RootRecord-Ecosystem` (`/home/rootrecord/RootRecord-Ecosystem`). This directory is not its own clone.  
**Domain repository:** `RootRecord-Software-Solutions/RootRecord-Pacific-Solar-Server`  
**Live local path (authoritative runtime):**

```text
/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server
```

Domain layout (PascalCase top-level folders):

```text
Automations/          # poller engine, jobs catalog, stack lifecycle
Communications/       # network (cloudflare), discord, email, slack, telegram, github
Energy/               # EcoFlow reads PASS (Energy/.venv, BLE); actuating actions VERIFY PENDING (WO-SRV)
System/               # sys-sample + plumbing warmups / single-flight
Reports/              # worklog foundation (WO-RPT-001)
Weather/              # weather poller (job enabled 2026-09-29; Weather/.venv)
Github/               # setup-remotes + sync-all
Geology/              # domain shell; Kīlauea ownership note in Library architecture
Security/             # Cameras/ = canonical cam / grab / timelapse (jobs.py); cam+grab PASS, timelapse VERIFY PENDING
A-Eyes/               # legacy leftover (stale __pycache__ only, untracked) — KEPT; not used by jobs.py
```

**Not a Pacific code domain:** `Logs/` — log **bytes** live under Database only.

Key operational paths (desk):
- Runtime root: `\u2026/1 - Servers/1 - RootRecord-Pacific-Solar-Server`
- Poller engine: `Automations/scripts/rootserver_poller.py`
- Jobs catalog: `Automations/scripts/jobs.py`
- cloudflared binary: `Communications/network/cloudflare/bin/cloudflared`
- CF config: `Communications/network/cloudflare/config/`
- Plumbing / single-flight: `System/scripts/plumbing/`
- Desk live file: `/home/rootrecord/RootRecord-Ecosystem/2 - RootRecord-Database/Intake/desk-live.txt`
- Logs: `/home/rootrecord/RootRecord-Ecosystem/2 - RootRecord-Database/Logs/` (e.g. Automations/automations_current.log)
- Backups: `/home/rootrecord/Database/GITHUB/`
- Master env: `/home/rootrecord/master/master-key.env` (never commit)

## Migration generations (2026-09-28)

| Gen | Location |
| --- | --- |
| **G3** live | Pacific org repo + Ecosystem Servers path above |
| **G2** residual | Historical skills paths; production poller must not host here |
| **G1** archive | `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server-Old` |

**Entry point for all migration docs:**  
`Documentation/00-architecture/MIGRATION-DOCS-INDEX-2026-09-28.md`

**Authoritative cutover status:** Work order WO-SRV-2026-09-27 (runtime verification still required before legacy retirement).

Rule: G2→G3 domain imports before selective G1 recovery. Never bulk-merge G1 `origin/` into G3.

## US Mainland Server
Secondary node providing continuity, synchronization, and recovery when the Pacific root is unavailable.

Treat mirrored files as recovery sources; verify before assuming they are the live deployed state.

## Inference & Council
- Council replies use the NPU, `llama3.2:3b`, context 4096, on demand, no Ollama fallback. Personas: Database `AI/FLM/Personas/`.
- Sandbox chat answers. Live council and private DMs stay quiet.
- One getUpdates owner: `council-relay.py`.
- Desk file and state snapshot refresh before a reply. Generated state is not committed.
- Reads go through `Automations/execution/execution-broker.py`. Restarts stay with `supervise-services.sh`. Agents do not restart services.
- Ava may inspect, diagnose, and help draft a work order. `can_build` is false. A build principal is a numeric Telegram id, not Ava and not a username. See Library `Documentation/02-agents/INTERACTION-MODES.md`.
- Single-flight enforcement via `System/scripts/plumbing/`.
- Start here if this chat is new: Library `Documentation/01-operations/HANDOFF.md`.
