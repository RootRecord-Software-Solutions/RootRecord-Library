# WORK ORDER — Pacific Runtime Path Cutover (`skills` → `1 - Servers`)

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-SRV-2026-09-27 |
| **Status** | **IN PROGRESS** — Energy + System + Reports + Github + Plumbing + Telegram plumbing LIVE; residual A-Eyes hourly wrapper remains |
| **Updated** | 2026-09-28 ~21:25 HST (Session 04) |

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
| Communications/network (cloudflare + globe command) | LIVE — command + cwd now Pacific |
| Stack reload | Automated reload **does not** open status window (window-close was tearing down stack) |

## Residual G2 (from Pacific `jobs.py` 2026-09-28 ~21:10 HST)

| Domain | Jobs / constants | Notes |
| --- | --- | --- |
| Telegram / coms | `council_relay` | G3 surface + `System/scripts/plumbing/single-flight.sh` landed; runtime verification pending |
| A-Eyes | cam server, frame grab, timelapse | G3 surface landed; hourly wrapper remains legacy pending safety-block clearance |
| Weather | `weather_poller` | Already **disabled** |
| Network globe | cwd | **LIVE** — cwd now Pacific |

## Next

1. Recheck council relay paths after the G3 single-flight landing; runtime verification remains required  
2. Resolve the remaining A-Eyes hourly wrapper source/path, then recheck all A-Eyes scheduler paths  
3. Verify G3 runtime behavior before retiring corresponding legacy functions  
4. Final grep of `jobs.py` + cwd cleanup

Import each residual function into its **existing** Pacific folder; rewire jobs; verify; then retire the completed legacy function immediately. No parallel names.
