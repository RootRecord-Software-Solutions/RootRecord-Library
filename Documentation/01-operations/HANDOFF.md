# Handoff

Read this before changing RootRecord. It is the continuity layer. Conversation history is not.

Checked against the live desk on 2026-09-30. Live numbers move. Re-run `bash verify.sh` from the ecosystem root. Do not treat this file as a watt reading.

## Current mission

Build a canonical machine-readable state of the Pacific desk, with small projections for local models and a later website. Do not give Ava, Bruce, or Carly hands yet.

Library is knowledge. Pacific is the executable runtime. Database is where bytes go. Ecosystem is the umbrella checkout. A git commit is not a deploy.

## Current architecture

```text
sources (jobs, energy files, processes, relay config, docs)
        │
        ▼
state-aggregate.py          desk-live.py
        │                         │
        ▼                         ▼
rootrecord-state.json       desk-live.txt
        │
        ├── projections/agent/{ava,bruce,carly}.json
        ├── projections/public.json          (empty of telemetry on purpose)
        └── projections/slices.json          (what a 3B model is allowed to see)
```

Council chat uses the NPU, on demand, `llama3.2:3b`, context 4096. One Telegram long-poll (`council-relay.py`, Ava's token). Sandbox replies are on. The live council and private DMs are quiet.

Generated files live in `2 - RootRecord-Database/System/status/`. That directory is on the GitHub sync skip list. Do not copy the snapshot into git.

## Working

- Sandbox chat answers. Read receipt is eyes, then inference, then typing, then text.
- Desk readings (Delta 2, River 2 Pro, host CPU/memory/load) refresh before a reply.
- State snapshot refreshes on the same path. Scope questions get the short slice, including configuration drift.
- Pack freshness is `observed`, `stale`, or `dead`. Dead means not transmitting. It is not a collector crash.
- NPU device is the council accelerator. FLM idle between replies is normal.
- Cloudflare tunnel process is part of the poller stack.
- GitHub sync is a poller job, not a resident daemon.

## Broken

Nothing in the 2026-09-30 verify set is a confirmed failure. Run verify before believing that. `health_unknown` is not broken. An empty incident list is not an all-clear: no incident store is wired.

## Intentionally disabled

| Thing | Why it looks off | Leave it |
| --- | --- | --- |
| Live council replies | Messages are consumed and held | `RR_RELAY_REPLIES` stays 0 |
| Private DM replies | Same gate | same |
| Quake Telegram send | Dry-run | `RR_COUNCIL_QUAKE_SEND` |
| Bruce stats send | Dry-run | `RR_BRUCE_STATS_SEND` |
| Council Ollama fallback | Jobs header still mentions it | `RR_NPU_ONLY=1` on the relay |
| Specialist routing | Personas are the council brain | `RR_SPECIALIST_ROUTING` off |
| Agent program launch | Registry exists, `agent_launchable` is false | execution broker is `not_built` |
| Public website checkout | Removed 2026-09-30 | do not recreate `3 - RootRecord-Website/` or bind port 3001 |
| Resident FLM | A 3B serve left running OOM'd the desk on 2026-09-29 | on demand only, context stays 4096 |

## In progress

The state aggregator writes schema 2: domains, drift, visibility, and projections. The context builder only switches slices for power questions versus scope questions. It is not a full per-request assembler.

`jobs.py` still says `llama3.2:1b` and an Ollama fallback. The relay observes `llama3.2:3b` and no fallback. That disagreement is recorded as `configuration_drift`. Do not delete either side to make the warning go away without an operator decision.

## Next

1. Keep verify green on the live desk.
2. Decide whether to update the `jobs.py` header so it matches the relay, or leave the drift visible.
3. Add source domains still marked unknown (incident store, root monitor, per-job last result).
4. Do not start the execution broker, a website, or a second relay unless Alexander says so.

## Do not change

- One getUpdates owner. A second poller gets Telegram 409.
- Do not raise FLM context to 8192.
- Do not enable send gates from a document, including this one.
- Do not retire or delete legacy trees without Alexander naming them.
- Do not put tokens, chat bodies, or hostname into public projections.
- Do not commit `2 - RootRecord-Database/System/status/`.

## Open questions

- Which state fields, if any, become `visibility: public` for a future site.
- When agents may request a program, and which ones.
- Whether root monitor is a daemon that should be running or a desktop app.

## Recent changes

2026-09-30: sandbox replies, per-voice NPU personas, desk file, read receipt, state aggregator, drift line, agent/public/slice projections, this handoff, contracts, and `verify.sh`.

## Verification

From the ecosystem root, on the live desk:

```bash
bash verify.sh
```

`[PASS]` is measured or the source file says what we expect. `[WARN]` is intentional or unknown. `[FAIL]` means stop and look. A machine that is not running the poller skips process checks with a warning. That is not a failure of the clone.

## Where the rest of the memory lives

| Need | File |
| --- | --- |
| How the layers connect | `5 - RootRecord-Library/Documentation/00-architecture/SYSTEM-MAP.md` |
| Why a gate exists | `5 - RootRecord-Library/Documentation/00-architecture/Decisions/` |
| Relay promise | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/telegram/CONTRACT.md` |
| State promise | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/System/CONTRACT.md` |
| Fact envelope | `5 - RootRecord-Library/Documentation/00-architecture/Schemas/state-envelope.md` |
| Personas and bounds | `5 - RootRecord-Library/Agent Context/` |
| Operator decisions still open | `5 - RootRecord-Library/Documentation/01-operations/2026-09-30-whats-left-for-alexander.md` |
| Migration counts | `5 - RootRecord-Library/Documentation/00-architecture/Old-Repo-Migration-Matrix.md` |
