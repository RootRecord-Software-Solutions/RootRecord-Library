# WO-COM-001 — Communications Surface (Tunnel, Telegram, Discord, Network)

| Field | Value |
|-------|--------|
| **Priority** | P1 |
| **Status** | Draft — sandbox replies on as of 2026-09-30 afternoon. Live council and private DMs stay quiet. Discord and the notify-policy seal are still open, so this draft is not promoted. |
| **Target** | Pacific `Communications/` (incl. `network/cloudflare`, `discord/`, `telegram/`) |
| **Depends on** | Live tunnel already working; operator policy on Telegram/Discord/alerts |
| **Related** | WO-WEB-001; WO-COM-002; poller stack lifecycle scripts; [Communications-Notify-Policy-Draft-2026-09-28.md](../../00-architecture/Communications-Notify-Policy-Draft-2026-09-28.md) (Ava draft — pending Carly seal) |

## Goal

Treat Communications as the single home for outbound/inbound edges: Cloudflare tunnel binaries/config references, network helpers, and messaging shells (Telegram, Discord, Slack) — without scattering secrets or second tunnels.

## Scope (in)

- Document current tunnel path: `Communications/network/cloudflare/` (bin + config expectations)
- Clarify what the poller stack starts/stops (cloudflared + unit) vs what stays systemd-only
- Inventory residual Telegram / Discord / notify scripts from G2 or private repos
- Policy: which events may notify (Energy critical, Geology alert, poller FAIL storm) vs log-only — see **Communications-Notify-Policy-Draft** (seal before treating as accepted policy)
- Lowercase `network` layout already established — preserve it
- **Discord:** any enablement or migration must follow **WO-COM-002** (fresh bot token; secrets outside git)

## Scope (out)

- Spinning a second cloudflared connector
- Public chatbots or open Telegram/Discord groups without operator approval
- Storing bot tokens in git (env or local-only secrets only)

## Acceptance criteria

1. `Communications/README.md` describes tunnel, network helpers, and notify policy
2. No second public hostname added without operator approval
3. Any Telegram or Discord job is either wired under Communications or explicitly deferred
4. Secrets remain outside the repo; docs only describe *where* to put them
5. Discord cutovers satisfy WO-COM-002 acceptance criteria before LIVE
6. Notify policy draft sealed (or explicitly revised) by Carly / operator before notify jobs expand

## Suggested steps

1. Snapshot current cloudflared invoke path from poller lifecycle scripts
2. Write Communications README + secret placement note
3. Operator / Carly seals or returns [Communications-Notify-Policy-Draft](../../00-architecture/Communications-Notify-Policy-Draft-2026-09-28.md)
4. Operator decides Telegram / Discord: enable / defer / disable residuals
5. If Discord enable: complete **WO-COM-002** token rotation gate first
6. If enable: one job template + rate limit note; then WO-SRV-001 wire

## Risks

- Token leak via accidental commit
- Notification spam from ecoflow_read_cycle FAIL codes (seen in live logs)
- Tunnel config drift between Pacific and older desk copies
- Stale Discord bot tokens after inventory mirrors or archive copies

## Notes

Live poller already shows tunnel + public URL healthy. This WO is organization and policy, not a rebuild of Cloudflare.

Discord credential rotation is **WO-COM-002** — required gate for any Discord migration phase.

*Related policy draft linked 2026-09-28 ~21:40 HST.*
