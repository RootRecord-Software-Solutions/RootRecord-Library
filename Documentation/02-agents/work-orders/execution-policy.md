# Work order execution policy

A work order is a trigger plus an allowed sequence. It is not permission for an agent to invent a repair.

## Two different flags

| Flag | Meaning |
| --- | --- |
| `executor` | The poller job or script that already owns the work |
| `agent_may_invoke` | Whether Ava, Bruce, or Carly may start it through the broker |
| `requires_operator` | Whether a human must approve the executor |

`requires_operator: false` on WO-SRV-RELAY means the poller supervisor may restart a dead relay without asking. It does not mean Bruce may restart it.

## When an agent sees a match

The agent may say: the measured state matches this order's trigger. The executor is the poller. I am not allowed to run the recovery. I may call `inspect_relay` and `run_verification`.

If the supervisor has BLOCKED the service, the agent reports that and stops. It does not raise the retry cap.

## File

The relay order is `WO-SRV-RELAY.json` in this directory. It describes `supervise-services.sh`. It does not replace it.
