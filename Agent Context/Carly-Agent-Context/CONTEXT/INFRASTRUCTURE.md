# Infrastructure Context

## RootRecord Pacific Solar Server
Primary operational environment (Hawaiʻi desk).

**Git root for this path:** `RootRecord-Software-Solutions/RootRecord-Ecosystem` (`/home/rootrecord/RootRecord-Ecosystem`). This directory is not its own clone.  
**Domain repository:** `RootRecord-Software-Solutions/RootRecord-Pacific-Solar-Server`  
**Live local path:**

```text
/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server
```

Key paths (on desk):
- Runtime root: Ecosystem `1 - Servers/1 - RootRecord-Pacific-Solar-Server`
- Public host: `https://rootserver.rootrecord.cloud/`
- Local poller HTTP: `http://127.0.0.1:8799/`
- Energy (measured only): `/home/rootrecord/RootRecord-Ecosystem/2 - RootRecord-Database/Energy/{soc,watts,samples}/`
- System samples: `/home/rootrecord/RootRecord-Ecosystem/2 - RootRecord-Database/System/`
- Worklog: `/home/rootrecord/RootRecord-Ecosystem/2 - RootRecord-Database/Worklog/`
- Backups: `/home/rootrecord/Database/GITHUB/`
- Master env: `/home/rootrecord/master/master-key.env` (never commit)

Communications domain (in Pacific repo):
- Cloudflare tunnel binary + config: `Communications/network/cloudflare/`
- Messaging shells: discord, email, slack, telegram, github (api/messaging/notifications/webhooks)

## US Mainland Server
Secondary node providing continuity, synchronization, and recovery when the Pacific root is unavailable.

Treat mirrored files as recovery sources; verify before assuming they are the live deployed state.

## Inference & Council
- Single-flight enforcement via plumbing scripts (Bruce’s operational responsibility)
- Carly participates in security review, billing, and honesty seal; does not own the inference gate
