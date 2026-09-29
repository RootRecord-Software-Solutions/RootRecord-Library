# WORK ORDER — Pacific Runtime Path Cutover (`skills` → `1 - Servers`)

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-SRV-2026-09-27 |
| **Status** | **IN PROGRESS** — Energy + System + Reports + Github + Plumbing LIVE; residual domains remain |
| **Updated** | 2026-09-28 ~20:55 HST (Session 04) |

**Policy:** Do not run the old desk as the poller host.

**Domain naming SOP (standing):** One Pacific folder per domain (the capitalized name already in the tree). Python package name **matches that folder**. Never add a lowercase sibling symlink (e.g. no `energy` → `Energy`) to satisfy G2 imports — rewrite imports instead. Full text: [Pacific-Domain-Import-Playbook-2026-09-28.md](../../00-architecture/Pacific-Domain-Import-Playbook-2026-09-28.md) § Standing rules.

---

## Locked on Pacific

| Item | Status |
| --- | --- |
| systemd ExecStart | Pacific `run-poller.sh` (quoted) |
| Energy (reads + leapfrog + actions) | LIVE — folder **`Energy/` only**; `ECOFLOW_ACTIONS` → `Energy/scripts/actions` |
| System | LIVE — folder **`System/` only** |
| Plumbing (ollama + FLM warmup) | LIVE under **`System/scripts/plumbing/`** |
| Reports (worklog + roll-up + archive) | LIVE — folder **`Reports/` only** (WO-RPT-001 foundation) |
| Github (setup-remotes + sync-all) | LIVE — folder **`Github/` only** |
| Communications/network (cloudflare + globe command) | LIVE path for command; cwd residual remains |
| Stack reload | Automated reload **does not** open status window (window-close was tearing down stack) |

## Residual G2 (from live `jobs.py` 2026-09-28 ~20:55 HST)

| Domain | Jobs / constants | Notes |
| --- | --- | --- |
| Telegram / coms | `council_relay` | Shell only in Pacific — next |
| A-Eyes | cam server, frame grab, 3× timelapse | Larger; WO-AEYES |
| Weather | `weather_poller` | Already **disabled** |
| Network globe | cwd still legacy | Command path already Pacific |

## Next

1. Telegram / council_relay → `Communications/`  
2. A-Eyes  
3. Final grep of `jobs.py` + cwd cleanup  

Import next residual domain into its **existing** Pacific folder; rewire jobs; no parallel names.
