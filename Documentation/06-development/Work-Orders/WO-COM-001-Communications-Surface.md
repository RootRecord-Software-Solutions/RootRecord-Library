# WO-COM-001 — Communications Surface (Tunnel, Telegram, Network)

| Field | Value |
|-------|--------|
| **Priority** | P1 |
| **Status** | Draft |
| **Target** | Pacific `Communications/` (incl. `network/cloudflare`) |
| **Depends on** | Live tunnel already working; operator policy on Telegram/alerts |
| **Related** | WO-WEB-001; poller stack lifecycle scripts |

## Goal

Treat Communications as the single home for outbound/inbound edges: Cloudflare tunnel binaries/config references, network helpers, and any Telegram/notify jobs — without scattering secrets or second tunnels.

## Scope (in)

- Document current tunnel path: `Communications/network/cloudflare/` (bin + config expectations)
- Clarify what the poller stack starts/stops (cloudflared + unit) vs what stays systemd-only
- Inventory residual Telegram / notify scripts from G2 or private repos
- Policy: which events may notify (Energy critical, Geology alert, poller FAIL storm) vs log-only
- Lowercase `network` layout already established — preserve it

## Scope (out)

- Spinning a second cloudflared connector
- Public chatbots or open Telegram groups
- Storing bot tokens in git (env or local-only secrets only)

## Acceptance criteria

1. `Communications/README.md` describes tunnel, network helpers, and notify policy
2. No second public hostname added without operator approval
3. Any Telegram job is either wired under Communications or explicitly deferred
4. Secrets remain outside the repo; docs only describe *where* to put them

## Suggested steps

1. Snapshot current cloudflared invoke path from poller lifecycle scripts
2. Write Communications README + secret placement note
3. Operator decides Telegram: enable / defer / disable residuals
4. If enable: one job template + rate limit note; then WO-SRV-001 wire

## Risks

- Token leak via accidental commit
- Notification spam from ecoflow_read_cycle FAIL codes (seen in live logs)
- Tunnel config drift between Pacific and older desk copies

## Notes

Live poller already shows tunnel + public URL healthy. This WO is organization and policy, not a rebuild of Cloudflare.
