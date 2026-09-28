# WORK ORDER — Cloudflare Tunnel Credential Recovery

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-CF-2026-09-27 |
| **Date** | 2026-09-27 (HST) |
| **Status** | OPEN — Config recovery |
| **Owner** | RootRecord |
| **Related** | Session 02 worklog; 09:27 checkpoint |

**Scope:** Restore local Cloudflare tunnel credential so the poller can bring `rootserver.rootrecord.cloud` back online. Do not change poller architecture to work around a missing token file.

---

## 1. Intent

Morning restoration confirmed internet OK and tunnel start attempted, then:

`Tunnel DOWN — token file missing: /home/rootrecord/.cloudflared/rootserver.token`

Public endpoint is configuration recovery, not a runtime rewrite.

---

## 2. Current reality

### 2.1 What exists

| Item | Location / status |
| --- | --- |
| Poller tunnel job | `jobs.py` ON_BOOT `cloudflare_tunnel` / `ensure_tunnel_online` |
| Expected token | `/home/rootrecord/.cloudflared/rootserver.token` |
| cloudflared binary | `/home/rootrecord/.ollama/skills/automations/bin/cloudflared` |
| Public host | `rootserver.rootrecord.cloud` |
| Local service | `http://127.0.0.1:8799` |

### 2.2 Completed so far

- [x] Internet connectivity verified at boot
- [x] Poller attempts tunnel start
- [ ] Token / credential restored from backup or Cloudflare dashboard
- [ ] Tunnel UP verified
- [ ] Public URL verified

### 2.3 Known friction

- Clean OS rebuild; local secrets were not all restored at once
- Token must never be committed to git

---

## 3. Tasks

1. Locate prior token or recreate tunnel token in Cloudflare Zero Trust for rootserver.
2. Place token only at `/home/rootrecord/.cloudflared/rootserver.token` (permissions restricted).
3. Confirm `cloudflared` binary present and executable.
4. Restart or wait for `ensure_tunnel_online` / poller cycle; verify tunnel UP in poller log.
5. Hit `https://rootserver.rootrecord.cloud/` (or status path) without changing job definitions.

---

## 4. Non-goals

- Rewriting tunnel_start builtin
- Moving public host or local service ports without a separate decision
- Committing token material anywhere under Library or skills git trees

---

## 5. Key file / path reference

| Path | Role |
| --- | --- |
| `/home/rootrecord/.cloudflared/rootserver.token` | Tunnel credential (local only) |
| `automations/scripts/jobs.py` | tunnel jobs |
| `automations/bin/cloudflared` | Binary |
| poller log | Verify Tunnel UP / DOWN messages |

---

## 6. Open items

**Additional requirements:**

- Cloudflare account access confirmation
- Whether any secondary hostnames need the same token family
- 

---

## 7. Notes & constraints

- No force-push.
- Secrets stay out of git.
- Prefer small reversible steps.
- Do not rebuild working architecture merely because local config is missing.

---

*Work order prepared 2026-09-27 HST. Update status when closed.*
