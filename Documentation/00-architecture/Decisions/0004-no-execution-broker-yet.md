# 0004 — Broker refuses side effects

Date: 2026-09-30.

## Decision

`System/config/program-registry.json` lists programs, side effects, and gates. Every entry has `agent_launchable: false`.

On 2026-09-30 a refuse-by-default broker was added at `Automations/execution/execution-broker.py`. It may answer read capabilities from the snapshot. It refuses `restart_known_service`. The poller job `service_supervisor` remains the only automatic restart for the weather poller and the council relay.

## Reason

The agents need to know what exists and what they must not touch before they can start anything. A persona instruction is not permission. The supervisor already implements observe, restart, cap, and BLOCK. A second restarter in the model is the bug.

## Do not remove without reconsidering

- Confirmation, audit, and the difference between gated, disabled, and not built
- BLE, git push, and Telegram send are side effects even when a human runs them from the poller
- Alexander has not authorized agent execution

Decision 0006 adds interaction modes and a Cursor handoff. It does not unlock `restart_known_service`, and it does not put Ava, Bruce, or Carly in the build-operator set.
