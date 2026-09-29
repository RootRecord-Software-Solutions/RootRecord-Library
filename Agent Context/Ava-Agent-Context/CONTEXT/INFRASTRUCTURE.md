# Infrastructure Context

## RootRecord Pacific Solar Server
Primary operational environment (Hawaiʻi desk).

**GitHub:** `RootRecord-Software-Solutions/RootRecord-Pacific-Solar-Server`  
**Live local path (authoritative runtime):**

```text
/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server
```

Domain layout (PascalCase top-level folders):

```text
Automations/          # poller engine, jobs catalog, stack lifecycle
Communications/       # network (cloudflare), discord, email, slack, telegram, github
Energy/               # EcoFlow reads/actions (LIVE per WO-SRV)
System/               # sys-sample + plumbing warmups / single-flight
Reports/              # worklog foundation (WO-RPT-001)
Weather/              # weather poller (job enabled 2026-09-29; Weather/.venv)
Github/               # setup-remotes + sync-all
Geology/              # domain shell; Kīlauea ownership note in Library architecture
Security/             # security domain shell
A-Eyes/               # cam / grab / timelapse (source on Pacific; runtime verify pending)
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
- Single-flight enforcement via `System/scripts/plumbing/` (Bruce’s operational responsibility)
- Ava participates in design and public voice; does not own the inference gate
