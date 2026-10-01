# Decisions

Short records of choices a later agent will want to undo because the code looks unused. Read the matching file before removing a gate.

| ID | Choice |
| --- | --- |
| [0001](0001-council-replies-gated.md) | Live council and private DMs stay quiet |
| [0002](0002-npu-council-inference.md) | Council inference is NPU `llama3.2:3b`, on demand, context 4096 |
| [0003](0003-one-getupdates-owner.md) | One Telegram long-poll |
| [0004](0004-no-execution-broker-yet.md) | Broker answers reads and refuses restarts |
| [0005](0005-generated-state-not-in-git.md) | The live snapshot stays in Database status and is not auto-committed |
| [0006](0006-interaction-modes.md) | Build match is a numeric Telegram id. Cursor stays behind `cursor_api`. Agents cannot build. |
