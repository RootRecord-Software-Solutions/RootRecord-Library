# Proposal — Kīlauea checker (live frame + fountaining)

| Field | Value |
| --- | --- |
| **Date (HST)** | 2026-10-02 ~03:15 |
| **Proposed by** | Alexander (via Report Instructor → Wren) |
| **State** | PROPOSED |
| **Grounding** | Alexander idea ~03:15 HST; Report Instructor owns build; soft idea only — not built |
| **Needs sign-off from** | Alexander |
| **Related WO** | none yet |

## Problem (measured)

No measured gap recorded in this pass. Alexander stated a new Kīlauea checker as an idea, not as a live failure.

## Proposal

A new Kīlauea checker that:

- Pulls a live frame from official sources
- Adds that frame to the image analyzer
- Checks for volcano updates every 15 minutes
- Generates, in Carly voice: "Kilauea observation image was checked"
- Checks for fountaining; a training image of what fountaining looks like can be found for that purpose

## Scope and non-goals

Soft idea only. Report Instructor owns the build. Do not treat this page as authorization to code, enable a job, or change Geology runtime. No implementation detail beyond what Alexander said.

## Resource impact / safety

Not assessed. Build owner decides after sign-off.

## How it would be tested

Not specified. Leave to Report Instructor after sign-off.

## Open questions

- Which official source supplies the live frame
- How fountaining training images are chosen and stored
- Whether the Carly-voice line is local desk only or broader
