# 03 — Security

Security review, credential hygiene, honesty seals, and billing-wall posture for RootRecord.

| Field | Value |
| --- | --- |
| **Primary agent** | **Carly Mal** (Agent Gamma) |
| **Canonical identity pack** | [`Agent Context/Carly-Agent-Context/`](../../Agent%20Context/Carly-Agent-Context/) |
| **Rule** | No secrets, tokens, or credential values in Library docs |

---

## What belongs here

- Sealed security notes and AppSec findings (after review)
- Credential **placement class** docs (path/env *names*, never values)
- Honesty / public-copy seal records when they are durable Library artifacts
- Billing-wall language constraints (proposal-only until operator approves)

## What does **not** belong here

- Runtime code or poller jobs → Pacific (`RootRecord-Pacific-Solar-Server`)
- Live tunnel tokens, bot tokens, `master-key.env` values
- Invented metrics or “LIVE” claims without measured desk evidence

---

## Related work orders & policy drafts

| Doc | Topic |
| --- | --- |
| [WO-COM-002](../06-development/Work-Orders/WO-COM-002-Discord-Bot-Credential-Rotation.md) | Discord fresh-token gate |
| [WO-CF-2026-09-27](../06-development/Work-Orders/Cloudflare_Tunnel_Recovery_Work_Order_WO-CF-2026-09-27.md) | Tunnel credential recovery (local only) |
| [Communications-Notify-Policy-Draft](../00-architecture/Communications-Notify-Policy-Draft-2026-09-28.md) | Notify vs log-only (pending Carly seal) |
| [WO-COM-001](../06-development/Work-Orders/WO-COM-001-Communications-Surface.md) | Communications surface organization |
| [WO-DATA-2026-09-27](../06-development/Work-Orders/Database_Boundary_Work_Order_WO-DATA-2026-09-27.md) | Database boundary (no secret dumps) |
| [INTERACTION-MODES](../02-agents/INTERACTION-MODES.md) | Build match key is numeric Telegram id. Username is a label. Agents cannot build. Carly reject blocks. |

---

## Standing Carly loop

1. Orient to measured state and open proposals  
2. Review / seal / return with clear rationale  
3. Hand off implementation to **Bruce**; public wording to **Ava**  

This folder may stay sparse until seals land. Empty is better than speculative content.

*README added 2026-09-28 HST — section pointer only.*
