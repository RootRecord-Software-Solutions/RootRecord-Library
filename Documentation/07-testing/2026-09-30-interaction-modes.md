# Test record — interaction modes

| Field | Value |
| --- | --- |
| **Date / time (HST)** | 2026-09-30 14:46 HST |
| **Tester** | Cursor session on the Pacific desk |
| **Change under test** | Interaction modes, principal match, council loop, handoff package, gated Cursor call, recovery draft, broker denial |
| **State** | PASS for the script and `verify.sh`. Live relay seed VERIFY PENDING until that process is started again. Root Monitor gate clicks were not exercised in the window. |
| **Evidence** | Command output in the session. No Migration log was written. |
| **Commits** | not committed |
| **Backup** | none |

## What was tested

Temp-directory request lifecycle. No NPU call. No Cursor API call. The stub council returned JSON. The live principal registry was not given numeric ids.

## How

```bash
python3 "1 - Servers/1 - RootRecord-Pacific-Solar-Server/Automations/execution/test_interaction.py"
python3 "1 - Servers/1 - RootRecord-Pacific-Solar-Server/Automations/execution/verifier.py" WO-SRV-RELAY
python3 "1 - Servers/1 - RootRecord-Pacific-Solar-Server/System/scripts/verify.py"
```

## Pass criteria

1. A live-council chat id is refused.
2. Username `rootrecordadmin` with a different `from.id` stays `work_order`.
3. Three question rounds end at `NEEDS_DECISION` and the original sentence is unchanged.
4. A standard user stays `PENDING_AUTHORIZATION`. A later authorization by id 42 keeps `requested_by`.
5. Carly `reject` is `BLOCKED`.
6. Id 42 with the build gate on reaches `READY_FOR_BUILD`, then `CURSOR_HANDOFF` with the gate on, and does not call Cursor while `cursor_api` is off.
7. With `cursor_api` on, a fake executor writes an execution report and a verified verification report.
8. A BLOCKED supervisor file produces a draft and `executed` is false.
9. The broker refuses `development.execute_work_order` for Bruce and still allows `inspect_npu`.
10. `verify.sh` reports the restart lock, the agent build denial, closed seed gates, and `telegram_user_id` as the match key.
11. `WO-SRV-RELAY` still passes `process_alive` and `agent_may_invoke` false.

## Result

PASS on all of the above in that run. `WO-SRV-RELAY process_alive count=1`.

## Resource impact

| When | Load (1/5/15) | MemAvailable | Swap used | Peak RSS |
| --- | --- | --- | --- | --- |
| before | not recorded | not recorded | not recorded | not recorded |
| during | not recorded | not recorded | not recorded | not recorded |
| after | not recorded | not recorded | not recorded | not recorded |

The script did not start FLM or Cursor.

## Cleanup confirmation

- [x] no test process left (the script exits)
- [x] no port or model was opened by the script
- [x] temp directory under `/tmp/rr-interaction-*` only
