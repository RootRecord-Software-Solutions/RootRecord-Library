# WORK ORDER — Cloudflare Tunnel Credential Recovery

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-CF-2026-09-27 |
| **Date** | 2026-09-27 (HST) |
| **Status** | OPEN — Config recovery (paths updated 2026-09-28); security wording tightened 2026-09-28 |
| **Owner** | RootRecord |
| **Related** | Session 02 worklog; WO-SRV; domain wiring 2026-09-28 |
| **Updated** | 2026-09-28 (HST) |

**Scope:** Restore the local Cloudflare tunnel credential so the poller can bring `rootserver.rootrecord.cloud` online. Do not change poller architecture to work around a missing token file.

---

## 1. Intent

Public endpoint recovery is configuration recovery, not a runtime rewrite. Poller tunnel job remains the owner of cloudflared lifecycle.

**Security boundary:** Credential recovery must use the authoritative local secret path only. Do not copy, reconstruct, or recover credential material from repository history, mirrors, transcripts, documentation, backups, archives, or other historical artifacts.

If the authoritative local credential is unavailable, **stop** and require operator-directed credential reissuance through the authoritative Cloudflare provider interface. This work order does not authorize an alternate recovery source.

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
- [ ] Local authoritative token / credential available at the approved secret path
- [ ] Tunnel UP verified in poller log after every clean OS restore
- [ ] Public URL verified end-to-end after credential restore

### 2.3 Known friction

- Clean OS rebuilds may omit local secrets
- Token must never be committed to git
- Historical copies are non-authoritative and must not be used as recovery sources

---

## 3. Tasks

1. Verify whether the authoritative local credential is present at `/home/rootrecord/.cloudflared/rootserver.token` without displaying or copying its value.
2. If the authoritative local credential is unavailable, **stop** and require operator-directed credential reissuance through the authoritative Cloudflare provider interface.
3. Place/restrict the credential only at `/home/rootrecord/.cloudflared/rootserver.token` as directed by the operator; never record its value.
4. Confirm `Communications/network/cloudflare/bin/cloudflared` is present and executable.
5. Restart or wait for `ensure_tunnel_online` / poller cycle; verify tunnel UP in poller log.
6. Verify `https://rootserver.rootrecord.cloud/` end-to-end without changing job definitions.

---

## 4. Non-goals

- Rewriting tunnel_start builtin
- Moving public host or local service ports without a separate decision
- Committing token material anywhere under Library or server git trees
- Recovering token material from repository history, mirrors, transcripts, documentation, backups, archives, or other historical artifacts
- Changing poller ownership or introducing a second tunnel lifecycle owner

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

## 6. Acceptance criteria

- Credential provenance is authoritative/local only; no historical artifact is used as a recovery source.
- Credential value is never displayed, logged, committed, or entered into documentation.
- If the authoritative credential is unavailable, the WO stops pending operator-directed provider reissuance.
- Poller remains the sole tunnel lifecycle owner.
- Tunnel UP is verified from runtime evidence, not merely file/config presence.
- Public endpoint is verified end-to-end after credential recovery.
- No architecture or job-definition change is made under this WO.

---

## 7. Notes & constraints

- No force-push.
- Secrets stay out of git.
- Prefer small reversible steps.
- Do not rebuild working architecture merely because local config is missing.
- Runtime recovery and provider credential issuance are operator/runtime responsibilities; this document only defines the security boundary and acceptance bar.

---

*Work order prepared 2026-09-27 HST. Paths updated 2026-09-28 HST for domain layout. Security wording tightened 2026-09-28 HST by Carly Mal.*
