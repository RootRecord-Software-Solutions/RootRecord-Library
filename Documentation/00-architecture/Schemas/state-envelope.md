# State envelope

Live file, not committed: `2 - RootRecord-Database/System/status/rootrecord-state.json`. Written by `System/scripts/state-aggregate.py`. Schema version 2.

A fact should carry:

| Field | Meaning |
| --- | --- |
| `state` | `observed`, `stale`, `dead`, `running`, `gated`, `disabled`, `unknown`, `configuration_drift`, `not_built` |
| `source` | File or scan that produced it |
| `observed_at` | When this snapshot recorded it |
| `confidence` | `live`, `recent`, `configured`, `unknown` |
| `visibility` | `public`, `agent`, `operator`, `internal`, `private`, `secret` |

`configured` and `observed` are both kept when they disagree. The drift record is the disagreement. Do not collapse it in the writer.

`dead` on a pack means the last measurement is old. The collector is not automatically at fault.

`secret` values are never written. A credential object may say configured and must set `value` to null.

Visibility:

- `public` may later feed a website. Almost nothing is public yet. `projections/public.json` stays empty of telemetry until a field is marked.
- `agent` is the slice Ava, Bruce, and Carly may see.
- `private` (hostname) stays in the canonical file and out of agent and public views.

Context for council inference is 4096 tokens. The model receives a slice from `projections/slices.json`, not the whole snapshot.

Events are not a stream yet. `recent_changes` is the last few git subjects, and a commit is not a deploy.

`execution_broker` carries `read_broker`, `agent_launch`, `build_handoff`, and `cursor_api`. `interaction` may carry a request id, mode, and status for the agent slice. The original Telegram text stays on the request record, visibility `operator`, and out of this snapshot.
