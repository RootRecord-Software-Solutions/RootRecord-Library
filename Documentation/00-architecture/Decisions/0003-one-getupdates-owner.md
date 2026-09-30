# 0003 — One getUpdates owner

Date: 2026-09-29. Still in force 2026-09-30.

## Decision

Only `council-relay.py` long-polls Telegram, using Ava's token. Bruce and Carly send and react. They do not poll.

## Reason

Two pollers on one token receive HTTP 409 and can double-post.

## Do not remove without reconsidering

- A verify check that fails when the relay count is not exactly one
- `ensure-relay.sh` refuses to start a second copy
- Process scans must match `python3` plus the script name. A shell command that merely mentions the path is not a second relay
