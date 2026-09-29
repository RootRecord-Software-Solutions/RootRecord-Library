# Proposal — Relay quiet mode without losing messages

| Field | Value |
| --- | --- |
| **Date (HST)** | 2026-09-29 |
| **State** | **LANDED / VERIFY PENDING (next poller start)** — approved by Alexander 2026-09-29 (message text included) |
| **Grounding** | NPU/FLM evidence addendum 03:02 HST: quiet mode logs `[quiet] update N consumed — replies OFF` (Pacific `ebc32a7`) |
| **Needs sign-off from** | Alexander |

## Problem
In quiet mode (`RR_RELAY_REPLIES=0`, the default), updates are consumed (marked read), so those messages are never answered later.

## Proposal
While quiet, record the consumed update metadata (chat, time, message id; text only if Alexander approves) in the git-ignored relay state under `2 - RootRecord-Database/Intake/council-relay/`. When replies are opted in, offer a one-time "held messages" digest instead of silently dropping them.

## Resource impact / safety
Small state file. No inference while quiet. No token handling changes.

## Implementation (2026-09-29 ~04:01 HST)
- `council-relay.py`: when `RR_RELAY_REPLIES=0`, each consumed message is appended to `2 - RootRecord-Database/Logs/Communications/Relay-Inbox/relay-inbox_current.jsonl`. Fields: `ts`, `received_ts`, `update_id`, `chat_id`, `chat_type`, `from`, `persona_target`, `message_id`, `text`, `status: held`. Files are mode 0600. The relay rotates the file hourly into `Archive/YYYY-MM-DD/relay-inbox_YYYY-MM-DD_HH00.jsonl` (checked once a minute). A write failure is logged and never stops the relay. Nothing else changed: same single getUpdates, and no infer or post while quiet.
- Location: this uses the Database `Logs/Communications/Relay-Inbox/` folder that Alexander asked for, not `Intake/council-relay/`. Git-ignored (`/Logs/Communications/Relay-Inbox/*`, only its README is tracked), verified with `git check-ignore -v`.
- `Communications/telegram/scripts/relay-inbox-replay.py` (new) lists held items by default, read-only. It answers them as Telegram replies only with `--send` **and** `RR_RELAY_REPLIES=1`, and keeps a `replayed.jsonl` ledger.
- Commits: Pacific `5353e1f` (04:02:54) · `52573e7` (README) · Database `57172d0` (.gitignore + Relay-Inbox README, 04:03:03). Backup `/home/rootrecord/Database/GITHUB/g3-proposals-impl.bak-20260929-035910/`.
- Test: [07-testing record](../07-testing/2026-09-29-relay-quiet-inbox-parse.md). This was a parse-only test on synthetic data, with `api()` tripwired so a send would fail. `--send` without replies was refused (rc 3). Evidence `2 - RootRecord-Database/Logs/Migration/g3-proposals-impl-evidence-20260929T140900Z.md`.
- Active from the **next poller start**: the relay runs in the poller unit cgroup (`KillMode=control-group`), so it restarts with the stack. Sending held replies still needs Alexander's sign-off.
