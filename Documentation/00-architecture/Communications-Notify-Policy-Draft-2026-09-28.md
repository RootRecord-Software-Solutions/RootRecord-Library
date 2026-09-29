# Communications Notify Policy — Draft

| Field | Value |
| --- | --- |
| **Date** | 2026-09-28 (HST) |
| **Status** | Draft — operator/Ava policy; not execution |
| **Feeds** | WO-COM-001 |
| **Rule** | No secrets. No second tunnel. Docs only until accepted. |

---

## Single home

All messaging and network edges live under Pacific:

```text
Communications/
  network/cloudflare/     # tunnel (LIVE)
  network/scripts/
  telegram/               # council_relay residual
  discord/                # shell; WO-COM-002 before LIVE
  slack/ email/ github/
```

No parallel notify homes under G2 skills for new work.

---

## What may notify (proposed)

| Class | May notify? | Channel preference | Notes |
| --- | --- | --- | --- |
| Energy **critical** (e.g. sustained offline / safety-relevant) | Yes | Telegram (once relay verified) | Prefer sparse; not every FAIL code |
| Geology / hazard alert (when domain live) | Yes | Telegram | Align with product alert policy |
| Poller **FAIL storm** (repeated path/script failure) | Yes, rate-limited | Telegram | Not every single FAIL line |
| Routine ecoflow read FAIL / transient BLE | No | Log only | Avoid spam (seen in live logs) |
| Heartbeat / normal cycle success | No | Log only | |
| Discord | Deferred | — | Requires WO-COM-002 fresh token first |

Exact thresholds (e.g. N FAILs in M minutes) left for Bruce to implement surgically once this policy is accepted.

---

## Rate limit stance

- Prefer **batch or cooldown** over 1:1 event spam  
- One owner process per bot (Telegram: single getUpdates)  
- If unsure, **log only** until operator tightens policy  

---

## Secrets placement (policy only)

| Secret | Location class |
| --- | --- |
| Cloudflare tunnel token | Local only (existing: `~/.cloudflared/…`) |
| Telegram bot token | Local env / host secret — never git |
| Discord bot token | Local only; **new** token on enable (WO-COM-002) |

Docs may name env keys or path *classes*; never values.

---

## Acceptance for WO-COM-001 (policy portion)

- [ ] Operator accepts or edits the notify table above  
- [ ] Telegram residual may be wired under this policy  
- [ ] Discord stays gated on WO-COM-002  
- [ ] Communications README points here or absorbs the table when sealed  

*Ava draft for Bruce clarity. Does not change runtime by itself. 2026-09-28 HST.*
