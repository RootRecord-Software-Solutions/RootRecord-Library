# 0006 — Interaction modes

Date: 2026-09-30.

## Decision

Telegram requests carry an `interaction_mode`. The match key for build eligibility is the numeric Telegram `from.id` in `Documentation/02-agents/identity/principal-registry.json`. Usernames are labels.

Authorized labels, once their numeric ids are recorded:

- `@rootrecordadmin`
- `@WildEcho94`
- `@Crazychickenlady12`

Ava, Bruce, and Carly stay `can_build: false`. `development.execute_work_order` is denied to them. The Cursor API is the development executor, and only when the `cursor_api` gate is on. That gate ships off.

A standard user can reach `PENDING_AUTHORIZATION`. They cannot reach `READY_FOR_BUILD`.

ADR 0004 still holds. `restart_known_service` stays agent-locked. The poller supervisor remains the only automatic restarter. Recovery selection may notice a BLOCKED supervisor and write a draft. It does not start a second restarter and it does not raise the attempt cap.

## Reason

The council needs a shared request, an immutable human sentence, and a broker that refuses writes from a username or from an agent. The context package is how Cursor eventually runs. Phase proof of that package is a closed gate, not a person who must launch the session forever.

## Do not remove without reconsidering

- Numeric id match, fail closed on unknown identity
- Original request kept apart from council interpretation, execution, and verification
- `cursor_api` independent from commit, push, merge, and deploy
- One getUpdates owner, on-demand FLM, context 4096, no resident 3B model
