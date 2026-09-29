# WO-COM-002 — Discord Bot Credential Rotation (Migration Gate)

| Field | Value |
|-------|--------|
| **Priority** | P1 |
| **Status** | OPEN |
| **Target** | Pacific `Communications/discord/`; any Ava / Discord bot cutover |
| **Depends on** | Operator decides Discord is in scope for a given migration phase |
| **Related** | WO-COM-001; Ava-Ivy-Cloud / ava-core primaries; Communications domain import |
| **Security review** | Carly PASS — credential provenance tightened 2026-09-28 HST |

## Goal

Make **fresh Discord bot token issuance** a required step of any Discord migration or first-time Discord enablement under the org — not an afterthought.

When Discord is brought online (or re-homed from personal/archive inventory), operators must obtain a **new** bot token from the authoritative Discord Developer Portal, store it only in local secrets (never git), and wire the live path under Pacific Communications.

## Scope (in)

- Checklist for Discord enablement / migration phases
- Token storage rule: env file or host secret path only (same class as Cloudflare tunnel token)
- Application ownership: confirm bot app lives under the intended Discord account/team before cutover
- Post-rotation: update local runtime config only; restart the process that loads the token
- Docs pointer: `Communications/discord/README.md` on org Pacific

## Scope (out)

- Implementing Discord bot feature code in this WO (docs + process only until accepted for execution)
- Public disclosure of prior credential history
- Rotating unrelated secrets (Telegram, Slack, GitHub) except by their own WOs

## Credential provenance gate

The token used for enablement must originate from a **fresh issuance or reset in the authoritative Discord Developer Portal**.

No credential value may be copied, restored, reconstructed, or loaded from:

- repository history
- archives or mirrors
- transcripts
- documentation
- backups
- other historical artifacts

If fresh authoritative issuance cannot be completed, stop the enablement gate rather than attempting historical recovery.

## Acceptance criteria

1. Before any Discord-facing job is marked LIVE on Pacific, a **new** bot token has been issued from the authoritative Developer Portal for that application.
2. Token is present only in approved local secret locations (documented path or env name — **no values in git**).
3. `Communications/discord/README.md` lists the rotation gate and secret placement.
4. Work-order index links this WO under Communications proposals.
5. Any archive/mirror inventory is treated as **non-authoritative** for credentials; never copy tokens from history.
6. Acceptance verifies successful runtime authentication without recording, displaying, or transmitting the credential value.

## Suggested steps (when Discord migration is scheduled)

1. Open Discord Developer Portal → Applications → target bot → **Reset Token** / generate new token.
2. Store token in the designated host secret location (operator path; not committed).
3. Point Pacific Discord shell / future job at that secret via env or config that is gitignored.
4. Smoke-test connectivity (login / ready event) offline from production traffic if possible.
5. Mark Discord sub-domain READY only after smoke test; leave bot offline until then if not required.

## Risks

- Old tokens in git history remain invalid once rotated at Discord — do not re-use historical values.
- Running two processes with different tokens causes confusing partial outages.
- Accidental commit of `.env` or transcript dumps — enforce secret scanners and gitignore on agent worktrees.

## Notes

- Bot offline is an acceptable interim state; do not rush enablement without this gate.
- Ava Ivy / Ava stack Discord identity is in scope when those products are migrated under org authority.
- Pair with WO-COM-001 policy on which events may notify (Discord vs log-only).

*Opened 2026-09-28 HST — credential hygiene for Discord migrations. Security review tightened 2026-09-28 HST by Carly Mal.*
