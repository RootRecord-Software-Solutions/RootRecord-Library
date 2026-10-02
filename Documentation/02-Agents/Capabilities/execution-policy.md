# Execution policy

The broker is a gate. It is not a shell.

## Who may decide

| Voice | May inspect | May verify | May restart, write, send, or push |
| --- | --- | --- | --- |
| Ava | yes | yes | no |
| Bruce | yes | yes | no |
| Carly | yes | yes | no |

Inspection is allowed because it only reads the snapshot or `verify.sh`. Carly's later job is to block unsafe writes. There are no writes to block yet.

## What already repairs the desk

`Automations/scripts/supervise-services.sh` runs from the poller job `service_supervisor` about every 300 seconds. It watches the weather poller and the council relay. If one is dead it runs that service's existing ensure script. At most 3 restarts in 30 minutes, then one BLOCKED line and no more retries until the process is seen alive. That loop is the automation engine. Agents do not get a second copy of it.

## Request shape

An agent request names a capability id and an agent id. The broker looks up the registry.

- Unknown id: refuse.
- Agent denied, or `agent_may_invoke` false: refuse, write an audit line, do not run the program.
- Read capability: return the fields listed in `returns`. No ensure script. No Bluetooth. No git push.
- Any non-empty `side_effects`: refuse even if a future edit sets `agent_may_invoke` true, until this policy file is changed to allow that effect.

## Not unlocked

`restart_known_service`, `run_known_diagnostic`, `generate_report`, `create_work_order`, `development.execute_work_order`, configuration edits, code edits, GitHub writes, deploys.

`development.execute_work_order` is the Cursor executor capability. Ava, Bruce, and Carly are denied. A Telegram username does not authorize it. The broker requires a numeric Telegram id on the authorization record, a request in `READY_FOR_BUILD`, and the `cursor_api` gate. That gate ships off. Commit, push, merge, and deploy stay off even when `cursor_api` is opened.

## Audit

Every request appends one JSON line under Database `Logs/Automations/execution-audit.jsonl`. The line has agent, capability, result, and time. It has no tokens and no chat text.
