# WO-WEB-001 — Public Status / Solar Board Alignment

| Field | Value |
|-------|--------|
| **Priority** | P1 |
| **Status** | Draft |
| **Surfaces** | `rootserver.rootrecord.cloud`, optional `ava.rootmc.net` / `rootrecord.info/ava/status` |
| **Depends on** | WO-ECO-001 preferred (real energy JSON); tunnel + poller already live |

## Goal

Make the public solar/status board reflect Pacific G3 truth (poller + Energy domain) instead of mixed origin `:8787` vs poller `:8799` ambiguity.

## Scope (in)

- Document which host is canonical for **Pacific node** status (`rootserver.rootrecord.cloud` → poller)
- Ensure status JSON fields (battery, solar, load, CPU, uptime) have a single declared producer
- Propose minimal public page or API contract for “Pacific Solar Server health”
- Align Library / agent context so agents do not send status traffic to the wrong origin

## Scope (out)

- Full redesign of avaivy.cloud / rootrecord.online marketing
- RootMC homepage activity card
- Replacing Cloudflare tunnel topology without operator approval

## Acceptance criteria

1. One written source of truth for Pacific status URL + JSON shape
2. Public board (or stub) does not claim data it cannot fetch
3. Agent docs updated so `:8787` vs `:8799` roles stay distinct
4. No second cloudflared connector spun up for this WO

## Proposed deliverables

- Short API contract note under `Documentation/05-public-surface/`
- Optional static/status page copy if Website repo is the home
- Checklist for operator: health URL, sample JSON, fail behavior

## Risks

- Pointing public DNS at the wrong process (historical api.rootmc.net → FastAPI issue)
- Caching stale solar numbers at the edge

## Notes

Can draft the contract before Energy import; full board value rises after WO-ECO-001.
