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
Weather/              # weather ensure + sync helpers
Energy/               # shell; EcoFlow jobs still on G2 skills paths until import
Security/             # cameras / security domain shell
System/               # system domain shell
Logs/                 # log ownership by domain
Github/               # repo-ops shell (mirrors, metadata)
Geology/              # domain shell
```

Key operational paths (desk):
- Runtime root: `…/1 - Servers/1 - RootRecord-Pacific-Solar-Server`
- Poller engine: `Automations/scripts/rootserver_poller.py`
- Jobs catalog: `Automations/scripts/jobs.py`
- cloudflared binary: `Communications/network/cloudflare/bin/cloudflared`
- CF config: `Communications/network/cloudflare/config/`
- Desk live file: `/home/rootrecord/Database/intake/desk-live.txt`
- Backups: `/home/rootrecord/Database/GITHUB/`
- Master env: `/home/rootrecord/master/master-key.env` (never commit)
- Poller log (current): `~/.ollama/skills/logs/store/rootserver-poller.log`

## Migration generations (2026-09-28)

| Gen | Location |
| --- | --- |
| **G3** live | Pacific org repo + Ecosystem Servers path above |
| **G2** residual jobs | `~/.ollama/skills/…` (energy, a-eyes, github, plumbing, …) |
| **G1** archive | `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server-Old` |

**Entry point for all migration docs:**  
`Documentation/00-architecture/MIGRATION-DOCS-INDEX-2026-09-28.md`

Rule: G2→G3 domain imports before selective G1 recovery. Never bulk-merge G1 `origin/` into G3.

## US Mainland Server
Secondary node providing continuity, synchronization, and recovery when the Pacific root is unavailable.

Treat mirrored files as recovery sources; verify before assuming they are the live deployed state.

## Inference & Council
- Single-flight enforcement via plumbing scripts (Bruce’s operational responsibility)
- Ava participates in design and public voice; does not own the inference gate
