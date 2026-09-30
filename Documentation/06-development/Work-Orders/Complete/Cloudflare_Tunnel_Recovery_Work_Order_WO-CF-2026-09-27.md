# WORK ORDER — Cloudflare Tunnel Credential Recovery

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-CF-2026-09-27 |
| **Date** | 2026-09-27 (HST) |
| **Status** | COMPLETE — signed off 2026-09-29 ~21:41 HST. Binary restored, poller log `Tunnel READY`, https://rootserver.rootrecord.cloud/ returned HTTP 200. Token stayed in the local file and was not read into git. |
| **Owner** | RootRecord |
| **Related** | Session 02 worklog; WO-SRV; domain wiring 2026-09-28 |
| **Updated** | 2026-09-28 (HST) |

**Scope:** Restore local Cloudflare tunnel credential so the poller can bring `rootserver.rootrecord.cloud` online. Do not change poller architecture to work around a missing token file.

---

## 1. Intent

Public endpoint is configuration recovery, not a runtime rewrite. Poller tunnel job remains the owner of cloudflared lifecycle.

---

## 2. Current reality (2026-09-28)

### 2.1 What exists

| Item | Location / status |
| --- | --- |
| Poller tunnel job | `Automations/scripts/jobs.py` ON_BOOT `cloudflare_tunnel` / `ensure_tunnel_online` |
| Expected token | `/home/rootrecord/.cloudflared/rootserver.token` (local only) |
| **cloudflared binary (new)** | `…/Communications/network/cloudflare/bin/cloudflared` |
| CF config store (new) | `…/Communications/network/cloudflare/config/` |
| Public host | `rootserver.rootrecord.cloud` |
| Local service | `http://127.0.0.1:8799` |
| Operator observation | Public URL shown active in poller window banner |

### 2.2 Completed so far

- [x] Internet connectivity verified at boot
- [x] Poller attempts tunnel start via jobs catalog
- [x] Binary path moved under Communications/network/cloudflare (domain layout)
- [x] Default `CLOUDFLARED_BIN` in `run-poller.sh` + `rootserver_poller.py` points at new path
- [x] Token file present at the local path (poller started the tunnel; token was not printed or committed)
- [x] Tunnel UP verified in the poller log (`Tunnel READY`, 2026-09-29 21:39 HST)
- [x] Public URL returned HTTP 200 (2026-09-29 ~21:41 HST)

### 2.3 Known friction

- Clean OS rebuilds may omit local secrets
- Token must never be committed to git

---

## 3. Tasks

1. Locate prior token or recreate tunnel token in Cloudflare Zero Trust for rootserver.
2. Place token only at `/home/rootrecord/.cloudflared/rootserver.token` (permissions restricted).
3. Confirm `Communications/network/cloudflare/bin/cloudflared` present and executable.
4. Restart or wait for `ensure_tunnel_online` / poller cycle; verify tunnel UP in poller log.
5. Hit `https://rootserver.rootrecord.cloud/` without changing job definitions.

---

## 4. Non-goals

- Rewriting tunnel_start builtin
- Moving public host or local service ports without a separate decision
- Committing token material anywhere under Library or server git trees

---

## 5. Key file / path reference

| Path | Role |
| --- | --- |
| `/home/rootrecord/.cloudflared/rootserver.token` | Tunnel credential (local only) |
| `Automations/scripts/jobs.py` | tunnel jobs |
| `Communications/network/cloudflare/bin/cloudflared` | Binary |
| `Communications/network/cloudflare/config/` | CF status / blocker notes |
| poller log | Verify Tunnel UP / DOWN messages |

---

## 6. Notes & constraints

- No force-push.
- Secrets stay out of git.
- Prefer small reversible steps.
- Do not rebuild working architecture merely because local config is missing.

---

*Work order prepared 2026-09-27 HST. Paths updated 2026-09-28 HST for domain layout.*
