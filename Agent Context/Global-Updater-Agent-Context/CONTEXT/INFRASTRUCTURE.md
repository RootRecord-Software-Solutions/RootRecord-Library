# Infrastructure Context

## RootRecord Pacific Solar Server
Primary operational environment (Hawaiʻi desk).

**Git root:** `RootRecord-Software-Solutions/RootRecord-Ecosystem` (`/home/rootrecord/RootRecord-Ecosystem`). This directory is not its own clone.  
**Domain repository:** `RootRecord-Software-Solutions/RootRecord-Pacific-Solar-Server`  
**Live local path:**

```text
/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server
```

The Pacific server is the primary operational desk for RootRecord's Hawaiʻi runtime: communications, system sampling, weather, geology, and the poller. This paragraph is a description of that role. It is not a live measurement and it does not say whether a process is running.

### Recorded host sample
`2 - RootRecord-Database/System/last/host-last.json` is written by `System/scripts/sys-sample.sh` (job `sys_stats_cycle`). Discord only reads that file. It does not sample the host.

A figure from that file is a recorded sample with a timestamp. It is not a new measurement taken for the reply. If the file is missing or too old to cite, the measurement is unavailable.

### Professional Discord
Transport: `Communications/Discord/`. Channel allowlist: `Communications/Discord/config/channels.json`. Guild allowlist: `Communications/Discord/config/guilds.json`. Both lists stay empty until an id is accepted.

Token name: `DISCORD_BOT_TOKEN`. Ava Ivy's Discord token is a different name and is not read.

### Inference
`System/scripts/plumbing/run-infer.sh`, then `single-flight.sh`. The Global Updater does not start a second model server.

## US Mainland Server
Secondary node. A file there is not automatically the live Pacific state.

## Not this agent's job
Telegram council routing stays in `Communications/telegram/`. Minecraft community chat stays with Ava Ivy.
