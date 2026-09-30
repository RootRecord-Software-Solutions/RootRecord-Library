# System map

RootRecord is four roles. They are not four copies of the same tree.

| Role | Where | What it is |
| --- | --- | --- |
| Knowledge | `5 - RootRecord-Library/` | Architecture, decisions, work orders, agent identity. Not runtime. |
| Runtime | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/` | Programs, jobs, the relay, the state aggregator. |
| Persistence | `2 - RootRecord-Database/` | Measurements, logs, generated state. Not the place to edit behavior. |
| Umbrella | this ecosystem checkout | One git root on the desk. A commit here is not a deploy. |

GitHub still has separate remotes. This checkout is one repository. Do not add a nested `.git`.

## How a fact moves

```text
measured file or process
        │
        ▼
aggregator (state-aggregate.py) or desk writer (desk-live.py)
        │
        ▼
Database/System/status/     ← generated, skipped by github auto-commit
        │
        ├── agent slice  → Ava / Bruce / Carly (small; 4096 context)
        ├── public view  → empty until a field is marked public
        └── operator     → this desk, including paths and pids
```

Local models are the readers that matter today. A later website would read the public projection of the same snapshot. It would not get a second copy of reality.

## Council path

One process, `council-relay.py`, long-polls with Ava's token. Bruce and Carly post and react. Replies in the sandbox are on. Replies in the live council and in private DMs stay off. See Decisions/0001 and the telegram contract.

Inference is `run-infer.sh`: NPU, on demand, persona JSON per voice. The jobs header still names `llama3.2:1b` and an Ollama fallback. The relay does not. The snapshot records both. See Decisions/0002.

## What is not built

An execution broker. Agents cannot launch the programs listed in `System/config/program-registry.json`. Permissions in a persona file do not grant a side effect. The runtime does not enforce a broker yet because there is nothing to call.

## Verify

`bash verify.sh` at the ecosystem root. Read `Documentation/01-operations/HANDOFF.md` first.
