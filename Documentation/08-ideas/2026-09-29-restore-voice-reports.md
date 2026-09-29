# Proposal — Restore voice reports

| Field | Value |
| --- | --- |
| **Date (HST)** | 2026-09-29 |
| **State** | PROPOSED |
| **Grounding** | MIGRATION-DOCS-INDEX G0 scavenger list (`voice`, `voice-events`, `startup-voice`, `kokoro`, `radio`; day/morning/evening report packets); WO-RPT-001 ("voice-safe summaries on top, Carly seal before public") |
| **Needs sign-off from** | Alexander (enabling voice output); Carly seal before anything public |

## Problem
Legacy generations produced spoken and on-air reports. G3 has the Reports worklog foundation and weather reports, but no voice layer.

## Proposal
After the residual close-out, do a diff-only scavenger pass of the G0/G1 voice packets. Then add a local-only voice report built from existing measured data (Energy SOC, weather reports, worklog roll-up), rendered on demand, never resident, and off by default.

## Scope and non-goals
No public or broadcast output and no Telegram posting without sign-off. No bulk G0 import.

## Resource impact / safety
The TTS engine is loaded on demand and unloaded after each report. Measure RAM on the first test.

## Open questions
Which TTS engine (e.g. `kokoro` lineage) fits the RAM budget next to the NPU route?
