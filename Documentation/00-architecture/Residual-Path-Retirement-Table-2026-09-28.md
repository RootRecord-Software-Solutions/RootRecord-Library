# Residual Path Retirement Table

| Field | Value |
| --- | --- |
| **Date** | 2026-09-28 (HST) |
| **Supports** | WO-SRV-2026-09-27 |
| **Rule** | Pre-filled from existing static audits. Bruce fills Verified / Retired after G3 checklist. Docs only. |

---

## Operator runbook

Use the companion [G3 Runtime Verification Runbook](./G3-Runtime-Verification-Runbook-2026-09-28.md) for exact desk commands and evidence requirements. This table remains the retirement record.

## How to use

1. Run [G3 Runtime Verification Checklist](./G3-Runtime-Verification-Checklist-2026-09-28.md)  
2. Mark **Verified** only with evidence (cycle OK + path on Pacific)  
3. Mark **Retired** only after legacy **executable** removed or `MIGRATED.md` placed  
4. Keep legacy `SKILL.md` files  

Pacific root (desk):  
`/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server`

---

## Residuals (from WO-SRV audit 2026-09-28)

| Surface | Legacy pattern (historical) | Pacific target | Static source OK | Verified (runtime) | Retired |
| --- | --- | --- | --- | --- | --- |
| Telegram / council_relay | `…/skills/coms/telegram/…` | `Communications/telegram/` (+ plumbing under `System/scripts/plumbing/`) | Yes (paths rewired in source) | | |
| A-Eyes cam / grab / timelapse | `…/skills/a-eyes/…` | `A-Eyes/scripts/` (hourly wrapper on Pacific) | Yes | | |
| Energy actions | `…/skills/energy/scripts/actions` | `Energy/scripts/actions` | Yes — marked LIVE | | confirm only |
| Plumbing warmups / single-flight | `…/skills/plumbing/…` | `System/scripts/plumbing/` | Yes — marked LIVE | | confirm only |
| Weather poller | `…/skills/Weather/…` | `Weather/` (when imported) | N/A — **disabled** | leave disabled | leave until Weather WO |
| Network globe cwd | legacy `coms/ssh/…` | Pacific `Communications/network/` | Yes — cwd LIVE | | |

---

## Already LIVE (no residual action required for path)

Energy reads + leapfrog · System · Reports foundation · Github sync · Cloudflare tunnel · Network globe command  

Record any post-check confirmation in WO-SRV notes if useful; do not re-open closed path work.

---

## Retirement note

- Prefer `MIGRATED.md` on old packet: status, date, canonical Pacific path, “do not run”  
- Do not bulk-delete G1/G2 trees  
- Do not remove legacy `SKILL.md` solely because runtime moved  

*Pre-filled for Bruce. Empty columns are intentional. 2026-09-28 HST.*
