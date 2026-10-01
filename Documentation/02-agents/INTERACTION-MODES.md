# Interaction modes

Read this with [HANDOFF.md](../01-operations/HANDOFF.md). The machine contracts are the JSON schemas next to this file. This page is how they fit together.

`interaction_mode` is a Telegram request mode. The 2026-09-28 note “Migrate mode → build mode” is a migration phase. Those words are not this mode.

## Two loops

Both use the execution broker. They do not share one state machine.

A human request:

```text
Telegram message
        │
        ▼
numeric from.id → principal registry
        │
        ▼
interaction mode
        │
        ▼
Ava, then Bruce, then Carly
        │
        ▼
work order draft
        │
        ├── standard user → PENDING_AUTHORIZATION
        └── build principal, gates on → READY_FOR_BUILD
                    │
                    ▼
              context package
                    │
                    ▼
              Cursor API, only if cursor_api is on
                    │
                    ▼
         execution report, then verification report
```

A known desk failure:

```text
measured state matches a machine work order
        │
        ▼
broker selects a registered capability
        │
        ▼
existing program, or a refusal
        │
        ▼
BLOCKED supervisor → a draft, not a second restarter
```

## Who may build

The match key is the numeric Telegram `from.id` in [principal-registry.json](identity/principal-registry.json). The username is a label.

The labels waiting for ids:

- `@rootrecordadmin`
- `@WildEcho94`
- `@Crazychickenlady12`

A matching name with a missing or different id is a standard user. Standard users can reach `PENDING_AUTHORIZATION`. They cannot reach `READY_FOR_BUILD`.

Ava, Bruce, and Carly have `can_build: false`. They are not in that set. `development.execute_work_order` is denied to all three.

Until Alexander records the three numeric ids, the live registry cannot authorize a build.

## What a mode means

| Mode | Who | What it may do |
| --- | --- | --- |
| conversation | both | Answer from the state slice. No work order. |
| diagnose | both | Read capabilities the broker already allows. |
| work_order | both | Inspect, ask, draft. Stop at `PENDING_AUTHORIZATION`. |
| build | a matched numeric id | Same clarification. May become `READY_FOR_BUILD` when the build gate is on. |
| recovery | later | Name an existing supervisor program. The run gate ships off. |
| deployment | a matched id | Separate gate. Ships off. |

Build mode is the pathway. It is not a shell, and it is not the first step. The council may ask up to three rounds. The fourth unresolved round is `NEEDS_DECISION`. Carly’s reject is `BLOCKED`.

The original human sentence stays on the request. Council text is a later version. A later authorization adds an event and keeps `requested_by`.

## Where the bytes go

| Thing | Where | Committed |
| --- | --- | --- |
| Schemas, registry, mode policy | Library `Documentation/02-agents/` | yes |
| Live request, handoff package, reports | Database `System/status/requests/` | no |
| Gate file the broker reads | Database `System/control-panel/execution-gates.json` | no |
| Gate seed | Pacific `Apps/Control-Panel/execution-gates.json` | yes |
| Audit line | Database `Logs/Automations/execution-audit.jsonl` | no |

The seed closes `cursor_api`, commit, push, merge, deploy, recovery run, and raising the attempt cap. Opening `build` does not open `deployment`. Opening `cursor_api` does not open commit.

Root Monitor → Settings → Panel lists the same gates. Turning one on asks for confirm. The broker still refuses the action if the gate file says off. The panel is not the permission.

## What the programs do

`Automations/execution/execution-broker.py`

- `request <ava|bruce|carly> <capability>` reads a snapshot field or refuses.
- `execute <request_id>` calls Cursor only from a `CURSOR_HANDOFF` package when `cursor_api` is on.
- `recover <agent> <service>` refuses `restart_known_service` and, when the supervisor is BLOCKED, writes a draft.

`Automations/execution/interaction.py` records a sandbox message, runs the three persona passes, writes the draft and the package. The live council chat is not seeded. Council passes on the relay run only when `RR_INTERACTION_COUNCIL=1`. That variable ships unset. The running relay process keeps its old code until that process is started again.

`Automations/execution/verifier.py` still checks `WO-SRV-RELAY` for one relay process and `agent_may_invoke: false`. `verifier.py report <execution-report>` writes the verification report. The executor does not grade itself.

## What stays locked

ADR [0004](../00-architecture/Decisions/0004-no-execution-broker-yet.md) still holds. ADR [0006](../00-architecture/Decisions/0006-interaction-modes.md) adds modes on top of it.

- `restart_known_service` stays agent-locked. `supervise-services.sh` is the only automatic restarter.
- One getUpdates owner. FLM on demand, context 4096, not resident.
- Agents do not toggle gates and do not receive a shell.
- Commit, push, merge, and deploy stay off after `cursor_api` exists.
