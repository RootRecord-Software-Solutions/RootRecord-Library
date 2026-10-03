# Kīlauea checker (live frame + fountaining) — LIVE

| Field | Value |
| --- | --- |
| **Date (HST)** | 2026-10-02 ~03:31 (LIVE ~03:21; bank verified ~03:31) |
| **Proposed by** | Alexander (via Report Instructor → Wren) |
| **State** | **LIVE** (Pacific local, no commit; soft gate needs poller restart) |
| **Grounding** | Report Instructor ~03:21 HST — code + job on Pacific desk |
| **Needs sign-off from** | — (built; soak pending poller restart) |
| **Related WO** | none |

## Live fact (as of ~03:21 HST)

Kīlauea 15-minute image checker is **LIVE on Pacific** (local desk; no commit/push). Soft default in `run-poller.sh` is on for soak (`RR_VOICE_KILAUEA_IMAGE` `:-1`); the running poller must be restarted before the gate/job takes effect. **Not** in `LOCAL_DATA_POLL_JOBS` — report-side only (EcoFlow/cams-style forever-Pacific; ungated by exclusive ML2 data-poll).


## Verified — `*_current` bank + archive-on-replace (~03:31 HST)

The first `*_current` bank is verified. ML2 `geology_kilauea_cams` takes **USGS stills only** (no vision on the mainland host), writes an ephemeral handoff, and streams it to Pacific under the exclusive `RR_LOCAL_DATA_POLL=0` gate. Scratch is wiped after the stream. Pacific receives the files into the durable Cams bank; vision/looking remains Pacific-only.

| Piece | Verified behavior |
| --- | --- |
| **ML2 intake** | `geology_kilauea_cams`: USGS still intake only → handoff → Pacific Cams; enabled under exclusive `RR_LOCAL_DATA_POLL=0` and kept in `LOCAL_DATA_POLL_JOBS` as a soft toggle; no mainland vision; scratch wiped after stream |
| **Live Cams bank** | `Geology/Volcanoes/Hawaii/Cams/v1cam_current.jpg`, `v2cam_current.jpg`, `v3cam_current.jpg`, and `cams_current.json` |
| **Manifest** | `cams_current.json` records `photo_viewed` plus per-camera `fetched_at`, `bytes`, `sha`, `ok`, and `error` |
| **Pacific receiver** | Any filename containing `_current` is archived on replacement as `archive/YYYYMMDD/<stem>_<HHMMSS><ext>`; the live `_current` path is always newest for LLM reads |
| **Archive example** | `Geology/Volcanoes/Hawaii/Cams/archive/20261002/v3cam_current_033046.jpg` |
| **Looker** | Prefers `*_current` over `*-last`; `v3cam_current.jpg` smoke-verified with `source_kind=current` |
| **EcoFlow / cams** | EcoFlow stays Pacific forever; Cams are Pacific’s durable/LLM-readable bank, not a mainland vision move |

The bank and archive behavior are **VERIFIED**. The pattern is general to every `*_current` product stream; Kīlauea is the first consumer.

### Verified — report blend (~03:33 HST)

Report Instructor confirmed the spoken/written report blend. It states whether a still was viewed (**Y/N**) and, when viewed, what conditions looked like. The bank paths above, archive-on-replace, Pacific-only looking, and report blend are verified.

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
