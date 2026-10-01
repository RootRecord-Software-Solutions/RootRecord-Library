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

Inference is `run-infer.sh`. The council relay forces NPU `llama3.2:3b`, context 4096, on demand, no Ollama fallback. Other callers still default to `llama3.2:1b`. Personas are JSON files per voice. See Decisions/0002.

## Requests and the broker

A sandbox Telegram message can become an interaction request. The match key for a build is the numeric `from.id`, not the username. Schemas and the operator narrative are in `Documentation/02-agents/`. Decision 0006. The live request files stay in Database `System/status/requests/` and are not committed.

`Automations/execution/execution-broker.py` answers reads. It refuses agent restarts, writes, sends, and `development.execute_work_order`. Cursor runs only when a request is at `CURSOR_HANDOFF` and the `cursor_api` gate is on. That gate ships off. The poller job `service_supervisor` is the only automatic restart for the weather poller and the council relay. A persona file is not permission. Decision 0004 still holds.

## Verify

`bash verify.sh` at the ecosystem root. Read `Documentation/01-operations/HANDOFF.md` first.
