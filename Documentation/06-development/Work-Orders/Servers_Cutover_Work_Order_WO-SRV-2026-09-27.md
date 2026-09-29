# WORK ORDER — Pacific Runtime Path Cutover (`skills` → `1 - Servers`)

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-SRV-2026-09-27 |
| **Status** | **IN PROGRESS** — Pacific source paths landed for active residuals; runtime verification + legacy retirement remain |
| **Updated** | 2026-09-28 — continued migration audit |

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

## Current Source Audit — 2026-09-28

- Current Pacific `Automations/scripts/jobs.py` was re-read from the canonical repository after the A-Eyes hourly and plumbing migrations.
- Active scheduler surfaces for Energy actions, Telegram, A-Eyes, Network Globe, Ollama warmup, and FLM warmup point to Pacific paths.
- Telegram `relay.conf` had legacy `RUN_OLLAMA` and `RUN_INFER` fallback paths; both are now rewired to Pacific `System/scripts/plumbing/`.
- A-Eyes scheduler entries and wrappers were re-read directly from Pacific and contain Pacific paths; no active A-Eyes scheduler entry retains the legacy executable path.
- The only remaining `jobs.py` legacy path is the disabled Weather job; it remains intentionally disabled and is not brought into scope by this work order.
- The legacy repository still contains old scheduler/path references for migrated functions. These remain in place because G3 runtime verification has not been performed from this desk session; removing them now would violate the documented migration sequence.
- Legacy `SKILL.md` files remain preserved by explicit operator instruction.

## Static Runtime-Source Audit — 2026-09-28

- Direct fetch of migrated Pacific Telegram and System plumbing scripts found one embedded legacy executable fallback in `Communications/telegram/scripts/council-relay.py`.
- The fallback `/home/rootrecord/.ollama/skills/plumbing/scripts/run-infer.sh` was replaced with a repository-relative Pacific `System/scripts/plumbing/run-infer.sh` resolution in commit `f3bd0a6620e7ee3f0c9877541efe00171c4752c3`.
- Direct fetch of Pacific `run-infer.sh`, `run-ollama.sh`, `single-flight.sh`, `ollama-warmup.sh`, and `flm-warmup.sh` found no legacy skills-tree references.
- Pacific `Communications/telegram/scripts/status.sh` and `load_env.sh` do not exist at the inspected paths; no deletion was performed or inferred from that absence.
- Runtime verification remains unavailable from this desk session, so legacy runtime functions remain in the old repository.

## Pacific Runtime Static Audit — 2026-09-28

- Direct fetch inspection covered the migrated A-Eyes runtime scripts, Telegram runtime scripts, System plumbing scripts, and `Automations/scripts/jobs.py`.
- No embedded `/home/rootrecord/.ollama/skills/` or `~/.ollama/skills/` references were found in the inspected migrated A-Eyes, Telegram, or System plumbing runtime files.
- `Automations/scripts/jobs.py` contains one remaining legacy path pair only for `weather_poller`; that job is explicitly `enabled: False` and documented as disabled until the Weather domain path exists on the desk. No active scheduler entry in the inspected file retains a legacy executable/cwd path.
- Current `jobs.py` source blob: `4276087c42c4ff36f50e79fb5e827ac7d5f01866`.
- This is a static source audit only. It does not satisfy the required G3 runtime verification gate, so no legacy runtime function was retired.

## Extended Pacific Runtime Static Audit — 2026-09-28

- Direct fetch inspection extended to Pacific Automations poller/watch scripts, representative Energy action scripts, Reports runtime scripts, Github sync/remotes scripts, and the Network Globe ensure script.
- No embedded `/home/rootrecord/.ollama/skills/` or `~/.ollama/skills/` references were found in the inspected files.
- Representative source SHAs: `Automations/scripts/rootserver_poller.py` `93fbe25580cf7adfc0363cdf23d85d49ac4d4167`; `Automations/scripts/poller/poller-watch.py` `563b5c909e65ac9fd3c24ac7efa495e90164cacc`; `Energy/scripts/actions/river2pro-ac-always-on-on.sh` `6c40d2b24982ccf2c75f83745cfa94f05582d2c0`; `Energy/scripts/actions/solar-gate-arm.sh` `3c95f02f13f9fdc2c7906107166b13948c90430b`; `Reports/scripts/worklog_once.sh` `a12bd78fd75ed3beb7530f2235e62b4f13001643`; `Github/scripts/setup-all-remotes.sh` `22253d003c01488f618f195d7a3a983dbfd51f46`; `Communications/network/scripts/ensure-network-globe-hawaii.sh` `d8da6b7f3303248d77cc17a42e2ff61d32b7848d`.
- This remains a static audit; runtime verification is not established by source inspection.

## Legacy Retirement Gate — 2026-09-28

- Direct legacy-repository search confirms the old executable implementations remain present for the migrated plumbing warmups, single-flight/inference surfaces, Telegram relay, A-Eyes hourly scheduler, and Energy action wrappers.
- Their continued presence is intentional: the documented sequence requires successful G3 runtime verification before each corresponding legacy function is removed.
- Legacy `SKILL.md` documentation remains outside the retirement target and must be preserved.
- No legacy executable was deleted during this audit because this desk session has no remote runtime shell and therefore cannot establish the required G3 runtime verification.

## Next

1. Verify G3 runtime behavior for Telegram, A-Eyes, Energy actions, and the Pacific poller  
2. After successful verification, retire each corresponding legacy function immediately and document old → new paths  
3. Final grep of `jobs.py` + cwd cleanup  
4. Move this work order to `Documentation/06-development/Work-Orders/Complete/` only after all acceptance criteria are satisfied

Import each residual function into its **existing** Pacific folder; rewire jobs; verify; then retire the completed legacy function immediately. No parallel names.
