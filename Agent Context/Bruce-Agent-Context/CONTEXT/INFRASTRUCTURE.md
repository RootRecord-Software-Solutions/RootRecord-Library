# Infrastructure Context

## RootRecord Pacific Solar Server
Primary operational environment (Hawaiʻi desk).

**Git root for this path:** `RootRecord-Software-Solutions/RootRecord-Ecosystem` (`/home/rootrecord/RootRecord-Ecosystem`). This directory is not its own clone.  
**Domain repository:** `RootRecord-Software-Solutions/RootRecord-Pacific-Solar-Server`  
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
- Council replies use the NPU, `llama3.2:3b`, context 4096, on demand, no Ollama fallback.
- Sandbox chat answers. Live council and private DMs stay quiet.
- Single-flight and the poller supervisor are Bruce's operational surface. The supervisor may restart a dead relay or weather poller (3 times per 30 minutes, then BLOCKED). Bruce does not get a second restart through the broker. A BLOCKED service may produce a draft. Bruce does not raise the attempt cap and does not build. `can_build` is false. See Library `Documentation/02-agents/INTERACTION-MODES.md`.
- Telegram poll ownership stays with the single council-relay process.
- Start here if this chat is new: Library `Documentation/01-operations/HANDOFF.md`.
