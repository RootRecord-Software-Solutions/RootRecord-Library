# Proposal — Relay quiet mode without losing messages

| Field | Value |
| --- | --- |
| **Date (HST)** | 2026-09-29 |
| **State** | PROPOSED |
| **Grounding** | NPU/FLM evidence addendum 03:02 HST: quiet mode logs `[quiet] update N consumed — replies OFF` (Pacific `ebc32a7`) |
| **Needs sign-off from** | Alexander |

## Problem
In quiet mode (`RR_RELAY_REPLIES=0`, the default), updates are consumed (marked read), so those messages are never answered later.

## Proposal
While quiet, record the consumed update metadata (chat, time, message id; text only if Alexander approves) in the git-ignored relay state under `2 - RootRecord-Database/Intake/council-relay/`. When replies are opted in, offer a one-time "held messages" digest instead of silently dropping them.

## Resource impact / safety
Small state file. No inference while quiet. No token handling changes.
