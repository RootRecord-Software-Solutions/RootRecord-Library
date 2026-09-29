# Infrastructure Context

## RootRecord Pacific Solar Server
Primary operational environment (Hawaiʻi desk).

**GitHub:** `RootRecord-Software-Solutions/RootRecord-Pacific-Solar-Server`  
**Live local path:**

```text
/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server
```

### Stack Bruce must monitor
| Unit / process | Role |
|----------------|------|
| `rr-rootserver-poller.service` | User systemd unit for the poller engine |
| `rootserver_poller.py` | HTTP :8799, job scheduler, tunnel ownership |
| `poller-dashboard.py` | Default status viewer (read-only; never starts/stops anything), opened via the single-window launcher `Automations/scripts/poller/open-poller-window.sh` (Pacific `884c832`, `89a8d6d`, `4a4107a`) |
| `poller-watch.py` | Older status viewer — still exists; Ctrl-C in it stops the entire stack, and stack reloads kill it |
| `cloudflared` | Tunnel binary under `Communications/network/cloudflare/bin/` |
| `network-globe-hawaii.service` | Hawaii Network Globe SSH collector (stopped with stack) |

### Key paths
- Jobs catalog: `Automations/scripts/jobs.py`
- Stack stop/reload: `Automations/scripts/stack/`
- cloudflared: `Communications/network/cloudflare/bin/cloudflared`
- Token (local only): `/home/rootrecord/.cloudflared/rootserver.token`
- Poller log: `/home/rootrecord/RootRecord-Ecosystem/2 - RootRecord-Database/Logs/Automations/automations_current.log` (since 2026-09-29)
- Desk live: `/home/rootrecord/RootRecord-Ecosystem/2 - RootRecord-Database/Intake/desk-live.txt`
- Backups: `/home/rootrecord/Database/GITHUB/`
- Master env: `/home/rootrecord/master/master-key.env` (never commit)

## US Mainland Server
Secondary node providing continuity, synchronization, and recovery when the Pacific root is unavailable.

Treat mirrored files as recovery sources; verify before assuming they are the live deployed state.

## Inference & Council
- Single-flight enforcement via plumbing scripts
- Council mediation is Bruce’s operational responsibility
- Telegram poll ownership stays with the single council-relay process
