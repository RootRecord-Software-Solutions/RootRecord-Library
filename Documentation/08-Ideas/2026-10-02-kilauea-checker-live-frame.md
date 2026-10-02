# Kīlauea checker (live frame + fountaining) — LIVE

| Field | Value |
| --- | --- |
| **Date (HST)** | 2026-10-02 ~03:25 (LIVE ~03:21; WIP path ~03:25) |
| **Proposed by** | Alexander (via Report Instructor → Wren) |
| **State** | **LIVE** (Pacific local, no commit; soft gate needs poller restart) |
| **Grounding** | Report Instructor ~03:21 HST — code + job on Pacific desk |
| **Needs sign-off from** | — (built; soak pending poller restart) |
| **Related WO** | none |

## Live fact (as of ~03:21 HST)

Kīlauea 15-minute image checker is **LIVE on Pacific** (local desk; no commit/push). Soft default in `run-poller.sh` is on for soak (`RR_VOICE_KILAUEA_IMAGE` `:-1`); the running poller must be restarted before the gate/job takes effect. **Not** in `LOCAL_DATA_POLL_JOBS` — report-side only (EcoFlow/cams-style forever-Pacific; ungated by exclusive ML2 data-poll).


## WIP — general `*_current` intake + solar archive-on-replace (~03:25 HST)

**Not verified yet.** Path change only; the LIVE Pacific checker above remains.

| Side | Planned |
| --- | --- |
| **ML2** | Pull product streams using a live `*_current` path and stream home for analysis; Kīlauea USGS HVO stills are the first consumer of this general pattern |
| **Pacific (solar)** | For every `*_current` product, when a second `*_current` lands, rename the previous one into dated `archive/`; `archive/` is history only and the live path stays `*_current` |
| **Looker** | Prefer `_current` when available; fallback to `-last` |
| **EcoFlow / cams** | Stay forever-Pacific (unchanged); this naming/archive pattern is not a move to ML2 |

Wiring overnight. Kīlauea is the first consumer; the archive-on-replace pattern is general to every `*_current` product stream. Alexander will ping when the first `_current` banks + archive-on-replace are verified. Do **not** claim verified until that ping.

### WIP — report blend (~03:28 HST)

When the Kīlauea checker runs, the spoken/written report should state whether a still was viewed (**Y/N**) and, when viewed, what conditions looked like. Mainland keeps each `*_current` product, `cams_current.json`, and `look-last` when Report Instructor writes it. The looker prefers Cams `*_current`, then `-last`, then live USGS; Report Instructor owns the report text. This blend stays **WIP, not verified**, until Mainland verifies the first bank; do not claim it is live.
ML2/Mainland only polls and banks stills as `*_current` for solar; Pacific LLMs do the looking/vision, no vision runs on the Mainland host, and this remains WIP pending first-bank verification.

## Paths

| Piece | Where |
| --- | --- |
| Look script | Pacific `Geology/scripts/kilauea_look.py` (Gemma; same stack as `panel_look`) |
| Voice | `voice_reports` `kilauea_image_check` (Carly) + `voice_deliver` title |
| Job | `jobs.py` `voice_kilauea_image_check` every **900 s** |
| Gate | `RR_VOICE_KILAUEA_IMAGE` in `run-poller.sh` (soft default `:-1` / on for soak) |
| Bank | Database `Cams/kilauea-look-last.json` + `lava-fountain-ref.jpg` |

## Flow

USGS HVO still (prefer fresh Cams v3/v1/v2; else live GET) → Gemma look vs optional fountain ref → Carly voice: “Kilauea observation image was checked” + measured finding.

Smoke example (glow on V3 Halemaʻumaʻu): *Kilauea observation image was checked. Measured finding: glow at the vent…*

## Scope note

Do not invent more. Soft default noted; **poller restart required** before the gate is live in the running process. Living voice copy: [voice desk](../01-Operations/2026-09-30-voice-desk.md).
