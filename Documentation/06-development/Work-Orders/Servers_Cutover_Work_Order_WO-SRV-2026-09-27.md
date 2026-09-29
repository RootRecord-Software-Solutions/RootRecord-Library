# WORK ORDER — Pacific Runtime Path Cutover (`skills` → `1 - Servers`)

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-SRV-2026-09-27 |
| **Status** | **IN PROGRESS** — Pacific source paths landed for active residuals; runtime verification + legacy retirement remain |
| **Updated** | 2026-09-28 ~21:50 HST (Session 04) |

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
| A-Eyes | cam server, frame grab, timelapse | G3 surface landed, including hourly wrapper; runtime verification pending |
| Weather | `weather_poller` | Already **disabled** |
| Network globe | cwd | **LIVE** — cwd now Pacific |

### Legacy `SKILL.md` preservation rule

- Legacy domain `SKILL.md` files are intentional documentation artifacts and must remain in the old repository after a function/domain migration.
- Retirement applies to completed executable/runtime functions and their active scheduler references, not to the legacy `SKILL.md` documentation files.
- Do not delete or otherwise remove legacy `SKILL.md` files solely because the associated runtime has migrated to Pacific.

## Static Cutover Check — 2026-09-28 ~21:50 HST

- Pacific `RootRecord-Pacific-Solar-Server` search returned no `/home/rootrecord/.ollama/skills/` references.
- Pacific `jobs.py` now points the active A-Eyes hourly wrapper at `A-Eyes/scripts/timelapse_hourly.sh`.
- Pacific `System/scripts/plumbing/single-flight.sh` is present; Telegram G3 configuration no longer requires the legacy plumbing path.
- The legacy repository still contains historical `/home/rootrecord/.ollama/skills/` references across residual and non-residual trees. These are not treated as completed migrations without runtime verification and explicit scope.

## Next

1. Verify G3 runtime behavior for Telegram, A-Eyes, Energy actions, and the Pacific poller  
2. After successful verification, retire each corresponding legacy function immediately and document old → new paths  
3. Final grep of `jobs.py` + cwd cleanup  
4. Move this work order to `Documentation/06-development/Work-Orders/Complete/` only after all acceptance criteria are satisfied

Import each residual function into its **existing** Pacific folder; rewire jobs; verify; then retire the completed legacy function immediately. No parallel names.
