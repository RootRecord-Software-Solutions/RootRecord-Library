# 0001 — Council replies stay gated

Date: 2026-09-29. Still in force 2026-09-30.

## Decision

`RR_RELAY_REPLIES` defaults to 0. The live council chat is consumed and held. Private DMs are held. The sandbox answers when `SANDBOX_REPLIES=1`.

## Reason

The sandbox is the test room. The live council stays quiet while routing and inference are exercised.

## Do not remove without reconsidering

- Telegram rate limits and duplicate posts
- Operator gating of a shared room
- Private message boundaries
- The inbox hold is the record of what was not answered

Turning the flag on is an operator action, not a bugfix.
