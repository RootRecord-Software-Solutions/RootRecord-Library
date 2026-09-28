# Infrastructure Context

## Solar Pacific RootRecord Server
Primary operational environment.  
Contains live skills, agent packets, automations, energy monitoring, communications, and desk state.

Key paths (on desk):
- Skills root: `~/.ollama/skills` (synced from the Pacific repo)
- Desk live file: `/home/rootrecord/Database/intake/desk-live.txt`
- Backups: `/home/rootrecord/Database/GITHUB/`
- Master env: `/home/rootrecord/master/master-key.env` (never commit)

## US Mainland Server
Secondary node providing continuity, synchronization, and recovery when the Solar Pacific root is unavailable.

Treat mirrored files as recovery sources; verify before assuming they are the live deployed state.

## Inference & Council
- Single-flight enforcement via plumbing scripts
- Council mediation is Bruce’s operational responsibility
- Telegram poll ownership stays with the single council-relay process
