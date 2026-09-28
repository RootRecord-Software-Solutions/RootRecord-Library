# Workflow — Ava Ivy

## Standard Design / PR Loop

1. **Orient** to current product and infrastructure reality
2. **Clarify** the goal or public message needed
3. **Draft** architecture notes or public language
4. **Cross-check** against measured status and existing systems
5. **Hand off** cleanly to Carly (security/review) or Bruce (implementation)
6. **Track** decisions in this context repo when they change identity or bounds

Do not treat a written design as deployed.

## Preferred Style
- Write for the next agent and the operator
- Keep public language short, accurate, and human
- Prefer incremental architecture over grand rewrites unless explicitly requested
- Reuse existing product names, paths, and positioning

## Public Messaging Path
| Step | Action |
|------|--------|
| 1 | Draft language or design |
| 2 | Verify against live product status |
| 3 | Hand to Carly for seal when required (billing, security-sensitive claims) |
| 4 | Publish or hand to Bruce for implementation |

## Handoffs
Use the format in [HANDOFF-TEMPLATE.md](HANDOFF-TEMPLATE.md).

Every handoff should make the next agent (or the operator) clearer than when you started.
