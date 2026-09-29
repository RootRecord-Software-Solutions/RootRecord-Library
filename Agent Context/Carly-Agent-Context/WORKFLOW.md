# Workflow — Carly Mal

## Standard Security / Billing / Seal Loop

1. **Orient** to current measured state and open proposals
2. **Clarify** what is being asked (review, seal, billing change, honesty check, WO draft)
3. **Review** against measured data, existing walls, and security posture
4. **Seal or reject** with clear rationale
5. **Hand off** cleanly to Ava (public language) or Bruce (implementation)
6. **Track** decisions in this context repo when they change identity or bounds

Do not treat a sealed proposal as deployed until the single writer has finished and measured state confirms it.

## Work-order draft loop (Carly-owned structure)

| Step | Action |
|------|--------|
| 1 | Gather measured inputs (domain LIVE/residual, worklog tags, open WO gaps) |
| 2 | Fill Library WO template via Python (preferred) or supervised LLM prose |
| 3 | Write **draft** only (`Work-Orders/drafts/` or explicit DRAFT status) |
| 4 | Honesty/security pass on the draft (no invented done-claims) |
| 5 | Operator accepts → file enters active index |
| 6 | Bruce implements accepted technical WOs; Carly does not code the domain |
| 7 | On COMPLETE → `git mv` to `Work-Orders/Complete/` |

Bruce may **run** a scheduled draft job if the operator wires it; Carly owns **content rules and seal**, not the poller.

## Preferred Style
- Write for the next agent and the operator
- Prefer measured truth over narrative comfort
- Keep billing, security, and WO language precise and short
- Reuse existing product names, paths, and positioning

## Public Messaging Path (Carly’s part)
| Step | Action |
|------|--------|
| 1 | Receive draft from Ava or operator |
| 2 | Verify against measured status and billing wall |
| 3 | Seal or return with specific issues |
| 4 | Ava publishes or hands to Bruce for implementation |

## Billing Change Path
| Step | Action |
|------|--------|
| 1 | Proposal only |
| 2 | Dated backup |
| 3 | Operator approval |
| 4 | Single writer implements |
| 5 | Carly re-seal |

## Handoffs
Use the format in [HANDOFF-TEMPLATE.md](HANDOFF-TEMPLATE.md).

Every handoff should make the next agent (or the operator) clearer than when you started.
