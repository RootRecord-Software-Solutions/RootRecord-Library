# 0004 — No execution broker yet

Date: 2026-09-30.

## Decision

`System/config/program-registry.json` lists programs, side effects, and gates. Every entry has `agent_launchable: false`. The snapshot field `execution_broker` is `not_built`.

## Reason

The agents need to know what exists and what they must not touch before they can start anything. A persona instruction is not permission.

## Do not remove without reconsidering

- Confirmation, audit, and the difference between gated, disabled, and not built
- BLE, git push, and Telegram send are side effects even when a human runs them from the poller
- Alexander has not authorized agent execution
