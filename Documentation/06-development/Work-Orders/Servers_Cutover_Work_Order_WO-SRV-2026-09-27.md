# WORK ORDER — Pacific Runtime Path Cutover (`skills` → `1 - Servers`)

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-SRV-2026-09-27 |
| **Status** | **IN PROGRESS** — Energy + System + Reports + Github LIVE; residual domains remain |
| **Updated** | 2026-09-28 ~20:25 HST (Session 03 inventory) |

**Policy:** Do not run the old desk as the poller host.

**Domain naming SOP (standing):** One Pacific folder per domain (the capitalized name already in the tree). Python package name **matches that folder**. Never add a lowercase sibling symlink (e.g. no `energy` → `Energy`) to satisfy G2 imports — rewrite imports instead. Full text: [Pacific-Domain-Import-Playbook-2026-09-28.md](../../00-architecture/Pacific-Domain-Import-Playbook-2026-09-28.md) § Standing rules.

---

## Locked on Pacific

| Item | Status |
| --- | --- |
| systemd ExecStart | Pacific `run-poller.sh` (quoted) |
| Energy (reads + leapfrog) | LIVE — folder **`Energy/` only** |
| System | LIVE — folder **`System/` only** |
| Reports (worklog + roll-up + archive) | LIVE — folder **`Reports/` only** (WO-RPT-001 foundation) |
| Github (setup-remotes + sync-all) | LIVE — folder **`Github/` only** |
| Communications/network (cloudflare + globe command) | LIVE path for command; cwd residual remains |

## Residual G2 (from live `jobs.py` 2026-09-28)

| Domain | Jobs / constants | Notes |
| --- | --- | --- |
| Plumbing | `ollama_warmup`, `flm_npu_warmup` | No Pacific folder yet |
| Telegram / coms | `council_relay` | Shell only in Pacific |
| A-Eyes | cam server, frame grab, 3× timelapse | Larger; WO-AEYES |
| Weather | `weather_poller` | Already **disabled** |
| Energy actions | `ECOFLOW_ACTIONS` constant | Still points at skills |
| Network globe | cwd still legacy | Command path already Pacific |

## Next (Session 03 rewire order)

1. Energy actions constant  
2. Plumbing (folder decision + two warmups)  
3. Telegram / council_relay  
4. A-Eyes  
5. Final grep of `jobs.py` + cwd cleanup  

Import next residual domain into its **existing** Pacific folder; rewire jobs; no parallel names.
