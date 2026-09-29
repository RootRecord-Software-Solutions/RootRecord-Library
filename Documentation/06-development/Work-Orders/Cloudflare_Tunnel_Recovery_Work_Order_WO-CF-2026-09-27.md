# WORK ORDER — Cloudflare Tunnel Credential Recovery

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-CF-2026-09-27 |
| **Date** | 2026-09-27 (HST) |
| **Status** | OPEN — Config recovery (paths updated 2026-09-28) |
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
- [ ] Token / credential restored from backup or Cloudflare dashboard (if still missing on any rebuild)
- [ ] Tunnel UP verified in poller log after every clean OS restore
- [ ] Public URL verified end-to-end after credential restore

### 2.3 Known friction

- Clean OS rebuilds may omit local secrets
- Token must never be committed to git

---

## 3. Tasks

1. Use the authoritative local secret path only. Do not copy credential material from repository history, mirrors, transcripts, documentation, backups, or other archival artifacts. If the local credential is unavailable, stop for operator-directed credential reissuance through Cloudflare.
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
