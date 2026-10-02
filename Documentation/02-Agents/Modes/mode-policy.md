# Interaction mode policy

`interaction_mode` is how a Telegram request is handled. The migration document’s “build mode” is a different phrase. It names a project phase. It does not select this mode.

## Ceiling

The numeric Telegram `from.id` is the match key. A username is stored as a label.

- A matching id in the principal registry has ceiling `build`.
- Any other sender, including a matching username with a missing or different id, has ceiling `work_order`.
- Unknown identity fails closed for `BUILD`, `MODIFY_FILES`, `COMMIT`, `PUSH`, `CREATE_PR`, `MERGE`, `DEPLOY`, and `RECOVER`.

The classifier may place an authorized principal in `conversation` or `diagnose`. It may not place a standard user in `build`. The word “build” in a standard user’s text stays `work_order`.

## Modes

| Mode | Who | Execution |
| --- | --- | --- |
| conversation | both | no |
| work_order | both | no. Terminal status `PENDING_AUTHORIZATION` |
| build | authorized principals | pathway only. Council, then a work order, then Cursor when gates allow |
| diagnose | both | read capabilities already unlocked |
| recovery | later | existing supervisor programs. Gate default off |
| deployment | authorized principals | separate gate, default off |

Build mode is not the first step and is not a shell. `execution.permitted: true` means the pathway exists.

## Question cap

Three question rounds, then `NEEDS_DECISION`. The original human text is not rewritten.

## Agents

Ava, Bruce, and Carly stay `can_build: false`. Cursor is the development executor.
