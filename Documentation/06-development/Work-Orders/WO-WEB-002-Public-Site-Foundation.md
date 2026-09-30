# WO-WEB-002 — RootRecord Public Site Foundation Pass

| Field | Value |
|-------|--------|
| **Priority** | P2 |
| **Status** | Draft — local folder `3 - RootRecord-Website` was removed 2026-09-30. Do not recreate it or bind port 3001. `https://rootserver.rootrecord.cloud/` is the poller. The website sync row stays disabled. |
| **Surfaces** | rootrecord.info, rootrecord.online, avaivy.cloud, rootrecord.cloud (status only) |
| **Depends on** | WO-WEB-001 for status contract; operator design preference |
| **Related** | Private all-connections URL atlas; agent context REPOS/INFRASTRUCTURE |

## Goal

Define a minimal, honest public presence for RootRecord Software Solutions that matches live infrastructure (Pacific poller, tunnel, domains) and does not over-claim features still in migration.

## Principles

1. **Truth over polish** — only show systems that are actually online
2. **One status truth** — Pacific node status comes from the poller path (see WO-WEB-001)
3. **No dual origins** — marketing site must not invent a second API host that races `:8787` / `:8799`
4. **Docs link out** — deep technical material stays in Library; public site is orientation + status

## Scope (in)

- Site map proposal (home, about/mission, status, contact/operator)
- Content outline per page (short copy, no code dumps)
- Domain role table (which hostname is for what)
- Tech stack recommendation options (static vs light CMS vs existing stack) — pick later with operator
- Accessibility / mobile baseline notes
- Placeholder for future: Energy dashboard embed, Geology feed, agent roster (Ava/Bruce/Carly) if public-safe

## Scope (out)

- Full brand redesign or logo work in this WO
- RootMC game economy UI
- Private ops dashboards on public DNS
- Auth walls for internal tools on the marketing host

## Proposed site map

| Path | Purpose |
|------|---------|
| `/` | Who we are + live system at a glance |
| `/status` | Pacific solar/server health (contract from WO-WEB-001) |
| `/about` | Mission, Hawaii / Pacific context, operator-led |
| `/work` or `/systems` | High-level domains (Energy, Weather, Geology, Automations) — links to public-safe summaries |
| `/contact` | Preferred contact channel only |

## Domain role table (draft — confirm with operator)

| Host | Role |
|------|------|
| `rootserver.rootrecord.cloud` | Pacific poller public edge |
| `rootrecord.info` / `.online` | Marketing / orientation (this WO) |
| `avaivy.cloud` / agent hosts | Agent surfaces — not marketing home |
| Internal FastAPI / desk ports | Never public without explicit decision |

## Acceptance criteria

1. Written site map + domain role table committed under `Documentation/05-public-surface/`
2. Operator signs off on stack choice before implementation repo work
3. Status page (or stub) uses the single status contract
4. No secrets, no private repo trees, no ops credentials on public pages

## Suggested phases

1. **Docs only** (this WO) — map, roles, content outline
2. **Stub** — static status + home if operator approves stack
3. **Enrich** — after Energy/Weather imports, optional live widgets

## Risks

- Publishing stale architecture from G1/G2 docs
- SEO/content that implies product readiness beyond migration state
- Accidental exposure of internal URLs from all-connections atlas

## Notes

Implementation may live in a separate Website repo or existing host; this WO only defines foundation so build work is not inventing product claims.
