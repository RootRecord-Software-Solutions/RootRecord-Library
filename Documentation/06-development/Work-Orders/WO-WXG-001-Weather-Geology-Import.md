# WO-WXG-001 — Weather + Geology Domain Import

| Field | Value |
|-------|--------|
| **Priority** | P1 |
| **Status** | Draft — Weather poller recycled 2026-09-30 02:24:58 HST to load resource edits. County reports regenerated 02:34. `noaa_homepage` still failed a bot-check at 02:33. Geology and voice jobs stay **OFF**. Do not enable `RR_*` flags from this draft alone. |
| **Target** | Pacific `Weather/`, `Geology/` |
| **Depends on** | Operator source for NWS / Kīlauea (and any residual G1/G2 scripts) |
| **Related** | Migration priority P1; Old inventory; solar_weather cron notes |

## Goal

Complete Weather and Geology under Pacific domain folders so poller jobs and public-safe feeds no longer depend on residual skill trees or one-off desk scripts.

## Scope (in)

### Weather
- NWS (or chosen provider) fetch + parse
- Local storage of samples/summaries under declared data root
- Optional link to Energy hybrid (solar_weather) **without** dual writers — decide single owner
- Jobs wired via WO-SRV-001 after files land

### Geology
- Kīlauea / HVO-style monitoring scripts that operator already trusts
- Alert or sample write paths documented
- Clear separation from Weather (shared schedule OK; shared process only if intentional)

## Scope (out)

- New scientific models or ML prediction layers
- Public alert SMS/Telegram until Communications WO approves
- Replacing USGS/HVO as authority — we only mirror/summarize

## Acceptance criteria

1. `Weather/scripts/` and `Geology/scripts/` contain runnable entrypoints used by jobs
2. Domain READMEs list schedule, data paths, and failure behavior
3. No G2 residual paths remain for these domains in `jobs.py`
4. One successful scheduled cycle each without blocking Energy jobs

## Suggested order inside this WO

1. Weather first (NWS + any solar_weather dependency clarification)
2. Geology second (Kīlauea)
3. Joint schedule note in Automations README

## Risks

- Rate limits / ToS of weather providers
- Alert fatigue if geology alerts are too chatty
- Overlap with Core-Ops hybrid if solar_weather still runs on desk

## Notes

Align with all-connections `crons/solar_weather.py` only after deciding **one** runtime home (Pacific vs desk).

- *2026-09-29 02:50 HST:* weather retention policy **PROPOSED** (not applied) in `Pacific/Weather/README.md` §Retention; steady growth ≈ 0.23 GB/day once the `_current` set is filled.
