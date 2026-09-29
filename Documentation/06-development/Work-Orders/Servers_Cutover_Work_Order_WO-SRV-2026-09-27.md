# WORK ORDER — Pacific Runtime Path Cutover (`skills` → `1 - Servers`)

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-SRV-2026-09-27 |
| **Status** | **IN PROGRESS** — G3 PASS: poller on canonical root, network globe, BLE owner, cam server, frame grab, System sampling, Reports worklog, Plumbing non-NPU, read-only `solar-gate-status`, Telegram relay login/polling. Open: Telegram replies BLOCKED (models), Energy actuating actions + timelapse VERIFY PENDING, NPU BLOCKED, poller §5 gate. G2 code KEPT (retire only with Alexander sign-off) |
| **Updated** | 2026-09-29 ~01:37 HST — status + open findings refresh; G2 retirements reverted; residual path survey |

**Policy:** Do not run the old desk as the poller host.

**Domain naming SOP (standing):** One Pacific folder per domain (the capitalized name already in the tree). Python package name **matches that folder**. Never add a lowercase sibling symlink (e.g. no `energy` → `Energy`) to satisfy G2 imports — rewrite imports instead. Full text: [Pacific-Domain-Import-Playbook-2026-09-28.md](../../00-architecture/Pacific-Domain-Import-Playbook-2026-09-28.md) § Standing rules.

---

## Locked on Pacific

| Item | Status |
| --- | --- |
| systemd ExecStart | Pacific `run-poller.sh` (quoted) |
| Energy (reads + leapfrog + actions) | source LANDED / runtime VERIFY PENDING — folder **`Energy/` only**; `ECOFLOW_ACTIONS` → `Energy/scripts/actions` |
| System | source LANDED / runtime VERIFY PENDING — folder **`System/` only** |
| Plumbing (ollama + FLM warmup) | source LANDED / runtime VERIFY PENDING — under **`System/scripts/plumbing/`** |
| Reports (worklog + roll-up + archive) | source LANDED / runtime VERIFY PENDING — folder **`Reports/` only** (WO-RPT-001 foundation) |
| Github (setup-remotes + sync-all) | source LANDED / runtime VERIFY PENDING — folder **`Github/` only** |
| Communications/network (cloudflare + globe command) | source LANDED / runtime VERIFY PENDING — command + cwd now Pacific |
| Stack reload | Automated reload **does not** open status window (window-close was tearing down stack) |

## Residual G2 (from Pacific `jobs.py` 2026-09-28 ~21:10 HST)

| Domain | Jobs / constants | Notes |
| --- | --- | --- |
| Telegram / coms | `council_relay` | G3 surface + `System/scripts/plumbing/single-flight.sh` landed; runtime verification pending |
| Security/Cameras (formerly A-Eyes) | cam server, frame grab, timelapse | G3 surface landed, including hourly wrapper; runtime verification pending |
| Weather | `weather_poller` | Already **disabled** |
| Network globe | cwd | source LANDED / runtime VERIFY PENDING — cwd now Pacific |

### Legacy `SKILL.md` preservation rule

- Legacy domain `SKILL.md` files are intentional documentation artifacts and must remain in the old repository after a function/domain migration.
- Retirement applies to completed executable/runtime functions and their active scheduler references, not to the legacy `SKILL.md` documentation files.
- Do not delete or otherwise remove legacy `SKILL.md` files solely because the associated runtime has migrated to Pacific.

## Static Cutover Check — 2026-09-28 ~21:50 HST

- Pacific `RootRecord-Pacific-Solar-Server` search returned no `/home/rootrecord/.ollama/skills/` references.
- Pacific `jobs.py` now points the active A-Eyes hourly wrapper at `A-Eyes/scripts/timelapse_hourly.sh`. **Superseded** by Pacific commits `66ca49d` / `2e6be6e`: the hourly job now runs `Security/Cameras/timelapse_hourly.sh`.
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
- Current `jobs.py` source blob: `57ba4768208519c6db2a75c07c37e1e504675830`.
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

*Refreshed 2026-09-29 ~00:52 HST.* Done tonight: globe and BLE owner cut over and PASS; cam server, frame grab, System sampling and Reports worklog PASS; their G2 executables retired (see sections below).

1. **Database-root drift — source correction landed.** Pacific `run-poller.sh` and `rootserver_poller.py` now default to `/home/rootrecord/RootRecord-Ecosystem/2 - RootRecord-Database`; the operator restart/recheck is the remaining runtime gate. The next cleanup items are the remaining `Github/scripts/common.sh` default and the 30-second `Logs/Energy/ava-ecoflow-ble.log` Git-ignore treatment. Historical evidence below retains the old root exactly as observed at the time.
2. **Telegram:** `TELEGRAM_AVA_TOKEN`, `TELEGRAM_BRUCE_TOKEN`, and `TELEGRAM_CARLY_TOKEN` have been provisioned in the operator environment. Run runbook §1 and verify the three `*-telegram` Ollama models. After runtime PASS, retire G2 `council-relay.py` and the retained G2 plumbing functions it references.
3. **Energy actuating actions:** an operator-approved hardware test (arm/disarm, AC always-on).
4. **Security/Cameras timelapse:** observe an hourly compile in the 05–19 HST window; then retire G2 `grab_frame.py` and the timelapse scripts.
5. **NPU/FLM:** blocked until FastFlowLM is installed.
6. Re-score the Pacific poller (§5) once Telegram passes. Then do a final grep of `jobs.py` and clean up cwd.
7. Move this work order to `Documentation/06-development/Work-Orders/Complete/` only after all acceptance criteria are satisfied.

Import each residual function into its **existing** Pacific folder; rewire jobs; verify; then retire the completed legacy function immediately. No parallel names.


## Final Static Scheduler + Action Audit — 2026-09-28

- Direct fetch of the current Pacific `Automations/scripts/jobs.py` confirms all inspected active residual scheduler surfaces use Pacific paths: Telegram, A-Eyes, Network Globe, Energy reads/actions, System plumbing warmups, Reports, Github, and the Pacific poller/watch process.
- The sole remaining legacy path pair in `jobs.py` is `weather_poller`, which is explicitly `enabled: False` and remains outside the active cutover scope.
- Direct fetch of representative Energy action wrappers and A-Eyes wrappers found no `/home/rootrecord/.ollama/skills/` or `~/.ollama/skills/` references. Inspected source SHAs include Energy `river2pro-ac-always-on-on.sh` `6c40d2b24982ccf2c75f83745cfa94f05582d2c0`, `river2pro-ac-always-on-off.sh` `7a8d51147ee4d38a1ff145b39b8ac9b944558276`, `solar-gate-arm.sh` `3c95f02f13f9fdc2c7906107166b13948c90430b`, `solar-gate-disarm.sh` `cf4de448d0d6950070e167c974b0779743c8eb31`, `solar-gate-status.sh` `90e361a6362eb739de63c9ef8b380410a2ecf1bb`; and A-Eyes `ensure_cam_server.sh` `9e7bf1d3b08f9b80b34d4070c33b621fba58b5bd`, `grab_all.sh` `8c8a610155d28b011420ac347319d85ab4cf2fb4`, `timelapse_catchup.sh` `af717738f1474389427db6e7d16179b491ff111f`, `timelapse_daily.sh` `b562e22430569a680d929a668d6953f8808b5041`, `timelapse_hourly.sh` `3298a47163a6f60966745cf13bb4f7ed9d57c930`.
- Two guessed Energy filenames (`delta2-ac-always-on-on.sh` / `delta2-ac-always-on-off.sh`) do not exist at the inspected Pacific paths; no deletion or replacement was inferred from that 404.
- Static inspection does not establish live runtime behavior. Legacy runtime implementations remain pending the documented G3 runtime verification gate; legacy `SKILL.md` documentation remains preserved.


## Legacy → Pacific Function Mapping Audit — 2026-09-28

- Legacy search confirms the corresponding runtime implementations remain in the old repository for the migrated surfaces. Representative mappings are: `coms/telegram/scripts/council-relay.py` → `Communications/telegram/scripts/council-relay.py`; `plumbing/scripts/run-infer.sh` / `run-ollama.sh` / `single-flight.sh` → `System/scripts/plumbing/`; `energy/scripts/actions/river2pro-ac-always-on-on.sh` → `Energy/scripts/actions/river2pro-ac-always-on-on.sh`; and the legacy `automations/scripts/jobs.py` scheduler → Pacific `Automations/scripts/jobs.py`.
- The old Telegram `SKILL.md` remains present and is intentionally preserved as documentation per operator instruction.
- Legacy presence is not treated as failure at this stage. The documented sequence remains: verify the Pacific function live, then remove only that completed legacy runtime function and document old → new immediately.
- No deletion was performed during this mapping audit; no live runtime claim is made.


## Final Pacific Repository Legacy-Path Search — 2026-09-28

- Repository search across the Pacific source for representative legacy scheduler/executable paths returned no matches for the inspected Automations, Telegram, A-Eyes, Energy-action, or Plumbing legacy path families.
- Direct fetch remains authoritative where search indexing can lag. Current `Automations/scripts/jobs.py` blob `57ba4768208519c6db2a75c07c37e1e504675830` contains exactly one legacy path pair: the disabled `weather_poller` command/cwd at lines 168/171. The job is explicitly `enabled: False` and remains outside active cutover scope.
- No additional active legacy scheduler path was found in the current jobs source. No source change is warranted from this audit.
- Runtime verification remains the only unresolved WO-SRV acceptance gate for migrated active functions; no legacy runtime function was retired.


## Supporting-File Mapping Audit — 2026-09-28

- Direct legacy/G3 inspection confirms the migrated Telegram `ensure-relay.sh` and `voices.conf` exist on Pacific with the same content blob SHAs as their inspected legacy counterparts: `fa12a398916e49934571fdcf8cc8fe3a6558547a` and `dc2d5b5ec84db25104e95c0bf69003933e90a7c0`.
- The legacy Telegram `status.sh`, `load_env.sh`, and `post-voice.sh` exist in the old repository, but corresponding Pacific paths returned 404 during direct inspection. No deletion, migration failure, or replacement was inferred from absence alone; none is currently identified as an active scheduler dependency.
- Direct Pacific inspection confirms the migrated A-Eyes runtime files `ensure_cam_server.sh`, `grab_all.sh`, `grab_frame.py`, `timelapse_engine.py`, and `cam_server.py` are present. No legacy skills-tree reference was found in the inspected active runtime surfaces.
- This audit does not satisfy live runtime verification. No legacy runtime function was retired, and legacy `SKILL.md` preservation remains unchanged.


## Active Telegram Dependency Check — 2026-09-28

- Direct inspection of the active Pacific scheduler confirms `council_relay` invokes only `Communications/telegram/scripts/ensure-relay.sh`.
- Direct inspection of Pacific `ensure-relay.sh` confirms it starts `council-relay.py` directly and does not invoke legacy `status.sh`, `load_env.sh`, or `post-voice.sh`.
- Direct inspection of Pacific `council-relay.py` confirms its voice configuration is `Communications/telegram/config/voices.conf`, which is present. The inspected state directory remains under `/home/rootrecord/Database/intake/council-relay`.
- Therefore the three legacy Telegram supporting scripts found earlier are not identified as active Pacific scheduler/runtime dependencies from the inspected source. No replacement or deletion is inferred from their absence.
- This remains a source/dependency audit only; live runtime verification is still required before legacy runtime retirement.


## Active Scheduler Surface Audit — 2026-09-28

- Direct fetch of current Pacific `Automations/scripts/jobs.py` confirms the inspected enabled scheduler surfaces for the poller/watch stack, Github remotes/sync, System warmups, Telegram, A-Eyes, Network Globe, Energy reads/snapshot, System sampling, and Reports all resolve to Pacific paths.
- The sole remaining legacy `.ollama/skills` command/cwd pair is the explicitly disabled `weather_poller` entry; no enabled scheduler entry in the inspected file retains a legacy executable/cwd path.
- This confirms the static scheduler-source boundary documented for WO-SRV. It does not establish live process health or successful hardware/service execution.
- No source change, runtime retirement, or work-order completion is warranted from this audit alone.


## Legacy Function Retirement Inventory — 2026-09-28

- Direct legacy inspection reconfirmed the residual executable implementations that remain pending the documented verify-then-retire sequence: Telegram `council-relay.py`; Plumbing `run-infer.sh`, `run-ollama.sh`, and `single-flight.sh`; representative Energy action wrappers including `river2pro-ac-always-on-on.sh` and `solar-gate-arm.sh`; and the legacy Automations scheduler surface.
- Legacy `single-flight.sh` still defaults its state to `/home/rootrecord/.ollama/skills/plumbing/state`; the Pacific implementation uses `/home/rootrecord/Database/GITHUB/plumbing/state`. This is an intentional G3 data-boundary change and must be included in runtime verification before retirement of the legacy function.
- Pacific representative Energy action and poller sources are present and use Pacific/Data paths. No deletion was performed.
- The legacy Telegram runtime still contains its historical fallback path; the Pacific counterpart was already rewired to repository-relative G3 plumbing. Legacy presence remains expected until live verification and immediate post-verification retirement.
- Legacy `SKILL.md` files remain documentation artifacts and are not retirement targets.


## Domain Naming Correction — 2026-09-28

Operator correction: the camera/security runtime previously migrated under **A-Eyes/** is not the intended Pacific domain name. The canonical domain is **Security/**. The A-Eyes work is therefore treated as an intermediate misnamed import and must be realigned before runtime verification or legacy retirement.

- Pacific target: `Security/`
- Persistent security logs: `/home/rootrecord/RootRecord-Ecosystem/2 - RootRecord-Database/Logs/Security/`
- Persistent security media: the new RootRecord-Database `Media/` authority, using its documented Images/Timelapses locations.
- Do not continue troubleshooting the old A-Eyes path as the final architecture.
- Do not retire the legacy runtime until the renamed Security implementation passes the normal G3 verification gate.
- Runtime-only camera credentials/configuration must remain outside Git; do not commit `CONNECTION.json`.


## G3 Runtime Evidence (read-only) — 2026-09-29

Read-only desk capture 2026-09-29T10:12–10:16Z (00:12–00:16 HST); evidence file `2 - RootRecord-Database/Logs/Migration/g3-runtime-evidence-20260929T101550Z.md` (RootRecord-Database repo). Scored against the G3 Runtime Verification Runbook. No retirement performed.

| Row | State | Evidence / note |
| --- | --- | --- |
| Security/Cameras — cam server | PASS | `:8791` listener is `python3 cam_server.py` with cwd Pacific `Security/Cameras`; `/health` 200; no cam process under `.ollama/skills` |
| Security/Cameras — frame grab | PASS | `security_camera_frame_grab` wrote ch1–ch4 frames to `2 - RootRecord-Database/Media/Images/`; Pacific tree clean; `store/` git-ignored |
| Security/Cameras — timelapse | VERIFY PENDING | hourly/catchup ran from Pacific but only skipped (outside window / no frames); no compile observed |
| Telegram council relay | FAIL | No `council-relay.py` process; relay exits at start with `No data: poll token` (74× in relay log). `TELEGRAM_AVA_TOKEN` is not supplied: `SECRETS_1` (`~/.config/ava-council/secrets.env`) is missing and `SECRETS_2` has no Telegram key. `ensure-relay.sh` still logs `[ok] started` without checking the process survived. |
| Energy actions | VERIFY PENDING | Pacific `Energy/scripts/actions/` present and executable; no `solar-gate-status` run in the log |
| Energy BLE owner | FAIL | `ava-ecoflow-ble.service` runs G2 `~/.ollama/skills/energy/scripts/ble/ble-owner.py`; Pacific `Energy/config/devices.conf` `owner_script` points there; no Pacific counterpart |
| System sampling | PASS | `sys_stats_cycle` runs Pacific `System/scripts/sys-sample.sh` → `OK wrote /home/rootrecord/Database/SYSTEM/samples/…json` |
| Reports worklog | PASS | `worklog_scan` runs Pacific `Reports/scripts/worklog_once.sh` → `OK wrote/updated /home/rootrecord/Database/WORKLOG/worklog_current.md` |
| Plumbing (non-NPU) | VERIFY PENDING | `ollama_warmup` from Pacific `System/scripts/plumbing/` → `[ok] ollama up`; no inference through the Pacific single-flight gate (state dir `/home/rootrecord/Database/GITHUB/plumbing/state` absent) |
| Plumbing (NPU / FLM) | BLOCKED | no `flm` binary, no `ava-flm.service`, `:52625` unreachable |
| Network globe | FAIL | `network-globe-hawaii.service` ExecStart/WorkingDirectory = G2 `~/.ollama/skills/coms/ssh/local-data-globe/collector.js` (running); Pacific has no collector |
| systemd ExecStart | PASS | `rr-rootserver-poller.service` (user) ExecStart = Pacific `Automations/scripts/poller/run-poller.sh`; MainPID = Pacific `rootserver_poller.py` (imports `jobs` from its own dir) |
| Pacific poller (§5) | FAIL | poller, `jobs.py` and log are Pacific; log fresh; no `.ollama/skills` refs in the last 3000 lines; no FAIL storm. Fails only because Network Globe resolves to the legacy runtime and the relay is not running |
| Preconditions: single poller / relay / cloudflared | PASS | 1 Pacific `rootserver_poller.py`, no G2 poller; 0 relays (no second getUpdates owner); 1 `cloudflared` (Pacific binary) |

Retirement eligibility (after this evidence): Security/Cameras cam server + frame grab, System sampling, Reports worklog. The Retired column is untouched; retirement is a separate step.


## G2 Legacy Retirement — 2026-09-29

- Retired after the G3 runtime PASS in `2 - RootRecord-Database/Logs/Migration/g3-runtime-evidence-20260929T101550Z.md`, with a read-only dependency check first (G2 skills tree, systemd user/system units and timers, crontab, shell rc files, Pacific tree, running processes). Removed files backed up to `/home/rootrecord/Database/GITHUB/g2-retire.bak-20260929-002518/`; a `MIGRATED.md` was placed in each G2 scripts folder.
  - `~/.ollama/skills/a-eyes/scripts/grab_all.sh` → Pacific `Security/Cameras/grab_all.sh`
  - `~/.ollama/skills/system-stats/scripts/sys-sample.sh` → Pacific `System/scripts/sys-sample.sh`
  - `~/.ollama/skills/reports/scripts/worklog_once.sh` → Pacific `Reports/scripts/worklog_once.sh`
- Not retired (still referenced by G2 scripts that stay in place): `a-eyes/scripts/cam_server.py` and `ensure_cam_server.sh` (`install_aeyes_web.sh` checks them out, pkills and relaunches them), and `a-eyes/scripts/grab_frame.py` (imported by G2 `timelapse_engine.py` and `cam_server.py`; checked out by `install_aeyes_web.sh`). The Security/Cameras timelapse part stays open.
- The only other references to the retired files were in the dormant G2 `automations/scripts/jobs.py` (no G2 poller runs) and in G2 documentation (`SKILL.md`, `references/CAMERAS.md`). Legacy `SKILL.md` files are kept.


## Staged Migrations — 2026-09-29

- **Network globe — STAGED (awaiting unit repoint).** G2 `~/.ollama/skills/coms/ssh/local-data-globe/collector.js` plus its required `telegram-relay.js` and `package.json` copied to Pacific `Communications/network/local-data-globe/` (no `node_modules`, no secrets; the copies contain no `.ollama/skills` paths; `node --check` OK). Proposed unit: `Communications/network/local-data-globe/network-globe-hawaii.service.proposed` (WorkingDirectory + ExecStart → Pacific). Not installed; the live `network-globe-hawaii.service` still runs the G2 collector.
- **Energy BLE owner — STAGED (awaiting unit repoint + `devices.conf`).** G2 `~/.ollama/skills/energy/scripts/ble/ble-owner.py` (stdlib only) copied to Pacific `Energy/scripts/ble/ble-owner.py`; log/pid moved to `/home/rootrecord/Database/Logs/Energy/ava-ecoflow-ble.log` and `/home/rootrecord/Database/ENERGY/state/ava-ecoflow-ble.pid` (env-overridable); `py_compile` OK. Proposed unit: `Energy/scripts/ble/ava-ecoflow-ble.service.proposed`, which also lists the `devices.conf` `ble_log` (line 24) and `owner_script` (line 98) changes. Not installed; the live `ava-ecoflow-ble.service` still runs the G2 owner.
- **Telegram relay — code fix landed.** Pacific `Communications/telegram/scripts/ensure-relay.sh` now checks the relay is alive 3 s after launch and prints `[FAIL] … last log: …` (token-redacted) with exit 1 instead of a false `[ok]`. `bash -n` OK. Takes effect the next time the poller runs `council_relay`; nothing was restarted. The relay itself still needs `TELEGRAM_AVA_TOKEN` provisioned.
- Unit changes above need operator approval; no systemd unit, `jobs.py`, `devices.conf` or credential was changed.


## G3 Cutover — 2026-09-29 (operator-approved)

- Evidence: `2 - RootRecord-Database/Logs/Migration/g3-cutover-evidence-20260929T103720Z.md`. Unit/config backup: `/home/rootrecord/Database/GITHUB/g3-cutover.bak-20260929-003344/`. Poller not restarted; `jobs.py` and credentials unchanged.
- **network-globe-hawaii — PASS.** Unit repointed to Pacific `Communications/network/local-data-globe/collector.js` at 00:33:44 HST; MainPID cmdline and cwd are Pacific; active, no restarts; SSH stream to AWS ready. The remaining warnings (remote `maintain-hawaii-feed.sh` missing, exit 127; one SSH reconnect at start) also appeared with the G2 collector before the cutover — pre-existing and remote-side.
- **ava-ecoflow-ble — PASS.** Old owner stopped and confirmed gone, unit repointed to Pacific `Energy/scripts/ble/ble-owner.py`, `devices.conf` `ble_log` → `/home/rootrecord/Database/Logs/Energy/ava-ecoflow-ble.log` and `owner_script` → Pacific; started 00:35:14 HST; pid file matches MainPID, heartbeats every 30 s, no journal errors, one owner. A first attempt aborted in its own safety check (false match on the shell) and restarted the unchanged G2 unit, so the old owner was down about 2 s.
- **G2 retired** after a dependency check (G2 tree, systemd user/system units, cron, rc files, Pacific, processes; no live reference): `~/.ollama/skills/coms/ssh/local-data-globe/collector.js`, `telegram-relay.js` (only used by that collector) and `~/.ollama/skills/energy/scripts/ble/ble-owner.py`. Backup: `/home/rootrecord/Database/GITHUB/g2-retire.bak-20260929-003720/`; `MIGRATED.md` placed in both folders; `SKILL.md` kept. Dormant references left: G2 `jobs.py` (globe cwd), G2 `stop-poller-stack.sh` (kill pattern), G2 `start.sh` / `package.json`, G2 `energy/config/devices.conf`.


## Verified status refresh — 2026-09-29

- **Security/Cameras:** cam server and frame-grab passed live verification; `Security/Cameras/grab_all.sh`, `System/scripts/sys-sample.sh`, and `Reports/scripts/worklog_once.sh` legacy executables were retired after evidence. Security timelapse remains verification-pending.
- **Network Globe:** live systemd unit was repointed to Pacific and passed runtime verification; G2 collector/relay files were retired after dependency checks.
- **Energy BLE owner:** live systemd unit was repointed to Pacific and passed runtime verification; G2 BLE owner was retired after dependency checks.
- **Telegram:** token has been provisioned; runtime verification remains pending, including the required `*-telegram` model check; no legacy retirement.
- **Energy actions:** verification remains pending; no destructive hardware action is required or authorized for verification.
- **Plumbing / NPU:** non-NPU verification remains pending; FastFlowLM/NPU remains blocked because the documented runtime is unavailable.
- **Pacific poller:** runtime is on the Pacific path, but the overall acceptance gate remains open while Telegram and remaining verification items are unresolved.
- **Database boundary:** active Pacific source paths now target `/home/rootrecord/RootRecord-Ecosystem/2 - RootRecord-Database`. Historical evidence may still contain `/home/rootrecord/Database/` and should not be rewritten as if it were current.
- **Operator GitHub pull workflow:** the human `/home/rootrecord/RootRecord-Ecosystem/Pull.sh` remains intentionally available. Its coexistence with the 5-second automated GitHub sync is resolved and is not a migration blocker.

## Energy status, Plumbing gate, B1 reading — 2026-09-29

- Evidence: `2 - RootRecord-Database/Logs/Migration/g3-energy-plumbing-evidence-20260929T104618Z.md` (including a correction section). Poller not restarted; `jobs.py` and credentials unchanged.
- **Energy `solar-gate-status` — VERIFY PENDING.** Read the script first: it only reads `solar-gate-state.json`, with no BLE and no writes. Ran it once at 00:43 HST: `WAITING` / `No data - solar gate state not written yet` (exit 2), the correct answer because the gate has never been armed. But it and `solar-gate-arm/disarm.sh` hardcode the old `/home/rootrecord/Database/ENERGY/ports/`, while `Energy/lib/paths.py` moved to the canonical Database root at 00:42 HST. **Actuating actions** stay VERIFY PENDING (a hardware change needs approval).
- **Plumbing non-NPU — FAIL (state path); gate itself works.** The first test failed with exit 126: Pacific `run-infer.sh`, `run-ollama.sh` and `single-flight.sh` had lost their exec bit in the migration (git 100644; the G2 copies are 755), which also broke the relay's `RUN_INFER`. I restored mode 775 (backup `/home/rootrecord/Database/GITHUB/g3-plumbing.bak-20260929-004500/`; Pacific `cbe57eb`). Retest at 00:45 HST: one inference through the Pacific gate returned `Ok`; a parallel run was refused (exit 75). But state went to the old `/home/rootrecord/Database/GITHUB/plumbing/state`, and the runbook (revised 00:46 HST) requires the canonical root. **NPU/FLM BLOCKED.**
- **G2 retirement for these rows reverted.** `solar-gate-status.sh` and `ollama-warmup.sh` were retired at 00:46 HST and then restored byte-identical from `/home/rootrecord/Database/GITHUB/g2-retire.bak-20260929-004619/` once the rows no longer passed. Their `MIGRATED.md` files were removed.
- **G2 A-Eyes cam server retired** (cam-server PASS re-checked; evidence `2 - RootRecord-Database/Logs/Migration/g2-retire-aeyes-cam-evidence-20260929T105103Z.md`): `~/.ollama/skills/a-eyes/scripts/cam_server.py` and `ensure_cam_server.sh` → Pacific `Security/Cameras/`. Backup: `/home/rootrecord/Database/GITHUB/g2-retire.bak-20260929-005103/`. The earlier blocker, G2 `install_aeyes_web.sh`, turned out to be a manual one-shot installer for the dormant G2 poller that nothing invokes, so it doesn't block. Kept: `grab_frame.py` (G2 `timelapse_engine.py` imports it; timelapse pending), the timelapse scripts, `install_aeyes_web.sh` (obsolete; do not run).
- **Telegram — second blocker.** The relay's voice models `ava-telegram`, `bruce-telegram` and `carly-telegram` are not in `ollama list`, so relay inference would fail even with a token.
- **B1 = 0% (River 2 Pro) — finding only, not migration scope.** The data comes from the EcoFlow cloud API (`source: api`), not BLE. It was frozen at `soc=26%` for 40 min (23:40–00:19 HST); after a 5-minute gap in reads, every read since 00:24:37 HST says `soc=0%` with the same outputs (the canonical-root `river2pro-last.json` agrees). This is a late report of a real discharge or an API/device artifact, and it started before both cutovers. Check the unit's display.

## Database-root realignment + re-verification — 2026-09-29 ~00:57 HST

- Evidence: `2 - RootRecord-Database/Logs/Migration/g3-dbroot-realign-evidence-20260929T105845Z.md`. Pacific `87a6469`. Backup `/home/rootrecord/Database/GITHUB/g3-dbroot.bak-20260929-005646/`. Bruce Monitor Agent's last-hour commits were read first; none of the target files had been fixed, so nothing was skipped. Existing data was not moved.
- Paths now default to `/home/rootrecord/RootRecord-Ecosystem/2 - RootRecord-Database` (env-override convention): `single-flight.sh` `RR_PLUMBING_STATE`, `flm-warmup.sh` `FLM_LOG`, `solar-gate-*.sh` `SOLAR_GATE_STATE`, `ble-owner.py` `ENERGY_BLE_LOG`/`ENERGY_BLE_PID`, and the `devices.conf` `[paths]` entries `energy_data`/`samples`/`ports`/`soc`/`watts`/`ble_log` (nothing in the code reads `[paths]`).
- **ava-ecoflow-ble — one controlled restart, PASS.** Stopped at 00:57:25 HST, confirmed no owner, started at 00:57:27. New MainPID 780266 = the canonical-root pid file, one owner, heartbeat in the canonical `Logs/Energy/ava-ecoflow-ble.log`, NRestarts 0. The old owner removed its pid file on stop. About 2 s without an owner; no rollback needed.
- **Plumbing non-NPU — PASS** (00:57 HST). **Energy `solar-gate-status` — PASS (read-only)**; the actuating actions stay VERIFY PENDING.
- **G2 retired** after a dependency check: `~/.ollama/skills/energy/scripts/actions/solar-gate-status.sh` and `~/.ollama/skills/plumbing/scripts/ollama-warmup.sh`. Backup `/home/rootrecord/Database/GITHUB/g2-retire.bak-20260929-005845/`; MIGRATED.md placed. Kept: G2 `single-flight.sh`, `run-ollama.sh` and `run-infer.sh` (the G2 Telegram relay references them), `flm-warmup.sh`, `npu-status.sh`, and the Energy actuating actions.
- **Open — poller log / poller paths:** not moved; they need a poller restart. See Next #1.

## Poller realign + restart — 2026-09-29 ~01:12 HST

- Evidence: `2 - RootRecord-Database/Logs/Migration/g3-poller-realign-evidence-20260929T111731Z.md`. Backup `/home/rootrecord/Database/GITHUB/g3-poller.bak-20260929-011046/`.
- **Poller paths + log — PASS.** Pacific `d9f074b` (`rootserver_poller.py` ENERGY_ROOT/system-status, `run-poller.sh` + `open-poller-window.sh` POLLER_LOG) plus unit `Environment=POLLER_LOG` and `logging.conf` append targets → canonical `Logs/Automations/automations_current.log`. One restart 01:11:28 (old PID ignored SIGTERM, SIGKILL at 30 s); MainPID 804007, NRestarts 0, one poller + one cloudflared. Status line B2=85% = fresh `delta2-last.json` 85; served system-status.json = canonical file.
- **Github `common.sh` — LANDED** (Pacific `75d86f2`): DATABASE_ROOT → canonical; BAK_ROOT pinned to `/home/rootrecord/Database/GITHUB` (outside the Database git tree).
- **Log git churn — BLOCKED:** Database `.gitignore` rules for `Logs/Energy/ava-ecoflow-ble.log` and `Logs/Automations/automations_current.log` added (`a05805a`) but both files are tracked; needs an owner-approved `git rm --cached`.
- **Telegram relay — PASS (poll/auth), replies BLOCKED:** PID 804326 up and single, no 401/Unauthorized; `*-telegram` models absent. G2 `council-relay.py`, `ensure-relay.sh`, `run-ollama.sh`, `run-infer.sh` RETIRED (skills `8297c26`); G2 `single-flight.sh` kept (`npu-status.sh`).
- **01:19 HST stack reload** (auto-pull of Bruce `480990b`) restarted the poller (PID 817736) and killed the relay; `ensure-relay.sh` then failed (unquoted `LOG=` path with spaces). One-line quote fix (Pacific `f27604d`), relay re-run once → PID 821015 up, no 401. See evidence addendum.

## G2 retirements reverted — 2026-09-29 ~01:29 HST

- **KEPT (restored 2026-09-29, retire only with Alexander sign-off).** Alexander rejected tonight's G2 retirements (no live references is not grounds; unimported automations may need them). All 14 files restored byte-identical with original modes from `/home/rootrecord/Database/GITHUB/g2-retire.bak-*` (verified against `git show <parent>:<path>`): a-eyes `grab_all.sh`, `cam_server.py`, `ensure_cam_server.sh`; system-stats `sys-sample.sh`; reports `worklog_once.sh`; coms/ssh/local-data-globe `collector.js`, `telegram-relay.js`; energy `ble/ble-owner.py`, `actions/solar-gate-status.sh`; plumbing `ollama-warmup.sh`, `run-ollama.sh`, `run-infer.sh`; coms/telegram `council-relay.py`, `ensure-relay.sh`. All 8 MIGRATED.md markers removed (backup `/home/rootrecord/Database/GITHUB/g2-restore.bak-20260929-012907/`); SKILL.md kept. Skills `1dcee66`.
- Restored copies are dormant: nothing started/enabled/restarted; systemd units and running processes still use Pacific paths only (one each: BLE owner, globe collector, cam server, relay, poller). Earlier "G2 retired" bullets above are superseded by this entry.

## Status + findings refresh — 2026-09-29 ~01:37 HST

**Standing rule (Alexander, 2026-09-29):** never retire or delete G2/legacy code. "No live references" is not grounds — unimported automations (e.g. the older repo `rootrecordsoftwaresolutions/old`) may need it. Retirement happens only with Alexander's explicit sign-off.

- **Poller realign — PASS** (Pacific `d9f074b`): energy/system-status/log on the canonical Database root; status line matches fresh readings.
- **`Github/scripts/common.sh` — LANDED** (`75d86f2`): DATABASE_ROOT canonical; BAK_ROOT intentionally stays `/home/rootrecord/Database/GITHUB`.
- **Relay quoting fix — LANDED** (`f27604d`); **relay login/polling PASS**, replies **BLOCKED** (`ava-telegram`/`bruce-telegram`/`carly-telegram` models missing).
- **Live logs untracked — PASS** (Database `eabe62e`): BLE, poller-current and relay logs git-ignored, still written on disk; hourly archive is the synced copy.
- **G2 retirements reverted — KEPT** (skills `1dcee66`): all 14 files restored, MIGRATED.md markers removed, restored copies dormant.
- **Remaining no-restart defaults — LANDED** (Pacific `58ee023`): `devices.conf` `log_dir`/`state_dir` → canonical root, `skill_root` → Pacific `Energy` (no code reads `[paths]`; G2 energy uses its own G2 `devices.conf`, so nothing G2 depends on it); stack-reload log default → canonical `Logs/Automations/stack_reload_current.log` (next reload); `daily_roll_up.sh` WORKLOG_DIR → canonical (next 18:30 HST run).
- Residual path survey: `2 - RootRecord-Database/Logs/Migration/g3-residual-path-survey-20260929T113523Z.md`.
- Evidence: `2 - RootRecord-Database/Logs/Migration/g3-poller-realign-evidence-20260929T111731Z.md`.

**Open findings:**
1. Relay PID 821015 was started from the desk agent session (cgroup `app-grok-bot-*.scope`), not the poller unit; if it dies it only returns at the next poller start (boot job `council_relay`).
2. Poller stop takes 30 s and is SIGKILLed (TimeoutStopSec) on every restart/reload; an auto-pull stack reload (01:19 HST) also kills the relay because it lives in the poller cgroup.
3. `jobs.py` vs intake: re-checked — `jobs.py` only mentions intake in its header comment, already the canonical `2 - RootRecord-Database/intake/`; relay state is canonical too. Old `/home/rootrecord/Database/intake/council-relay/` remains (historical). `jobs.py` not touched.
4. `Logs/Communications/council-relay.log` is 0 bytes because the relay's stdout is block-buffered (nohup to file); stderr errors would still appear.
5. `devices.conf` G2 `log_dir`/`state_dir`/`skill_root` — fixed in `58ee023` (see above).
6. Security timelapse check must wait for the 05:00–19:00 HST window.
7. B1 (River 2 Pro) reads 0% — needs a physical check.
8. FLM/NPU BLOCKED (no FLM binary/service).
9. Needs decision: `Energy/db/store.py` still defaults to old-root `ROOTRECORD/rootrecord.db` (no canonical copy); `push-repo-once.sh` still treats `~/.ollama/skills` pulls as runtime code (arms a stack reload).
## NPU prerequisite installation update — 2026-09-29

The operator installed the documented AMD XDNA2/XRT prerequisite stack on the Pacific host: `amdxdna-dkms`, `libxrt-npu2`, and `libxrt2`. The host exposes `/dev/accel/accel0`, and `modinfo amdxdna` resolves the installed driver and firmware entries. The DKMS install reported a `BUILD_EXCLUSIVE` mismatch for kernel `7.0.0-34-generic`, so the NPU is **not yet runtime-verified**. A reboot and post-reboot validation are required before FastFlowLM can be marked installed/verified. No production deployment or legacy retirement is implied by this prerequisite installation.

## Weather hook-in + old-root archive — 2026-09-29 ~01:54 HST

- Weather **PASS** (Pacific `Weather/`, venv `Weather/.venv`, job `weather_poller` enabled, data → canonical `WEATHER/Hawai'i/`; reports VERIFY PENDING). One poller restart 01:49 HST → PID 880218; relay 880530 and weather 880724 now under the poller unit. Old-root data archived to `2 - RootRecord-Database/Archive/Previous-Datasets/G2-old-root-20260929/` (4.5 GB, README only in git). `store.py` → canonical `ROOTRECORD/`; G2 pulls no longer arm a stack reload. Evidence: `2 - RootRecord-Database/Logs/Migration/g3-weather-archive-evidence-20260929T115429Z.md`.

## Pre-reboot checkpoint 2026-09-29

Snapshot: `2 - RootRecord-Database/Logs/Migration/g3-pre-reboot-checkpoint-20260929T120755Z.md`. Verdict **READY** (caveats below). Rule: never retire/delete G2/legacy code without Alexander's explicit sign-off.

**Final state tonight**
- Poller realign **PASS** (Pacific `d9f074b`); status line = fresh `delta2-last.json`.
- Weather hooked in **PASS** (Pacific `Weather/`, venv, job enabled; `b72db19`/`e977252`); reports **PASS** (generated 01:59:13 HST incl. `solar_calculation_table_current.md`). Growth ≈ 2 MB/min (≈ 3 GB/day); git-ignored.
- Old-root data archived (move) → `2 - RootRecord-Database/Archive/Previous-Datasets/G2-old-root-20260929/` (4.5 GB, README only in git).
- `Energy/db/store.py` → canonical `ROOTRECORD/` (`abc78b2`); `push-repo-once.sh` no longer reloads the poller on G2 pulls (`abc78b2`); Pacific `Energy/lib/vendor/` canonical (`99cc71e`); READMEs → canonical root (`99cc71e`, `662bf97`).
- Relay retry-on-network-error fix `b3754fb` — **pending until the next relay start** (the reboot).
- Live logs untracked (Database `eabe62e`). G2 retirements reverted, all 14 files restored (skills `1dcee66`).
- Ollama layout (Alexander's choice): Database `AI/Ollama/…` + `Logs/AI/Ollama/…`, symlinks `~/.ollama/{modelfiles,logs}` intentional. `ollama.service` runs as **User=ollama** and logs to journald — it may lack permission to write under `/home/rootrecord` (home is 750).
- NPU prereqs installed (`amdxdna-dkms`, `libxrt-npu2`, `libxrt2`; `/dev/accel/accel0`); **FLM pending after reboot** (no `flm`, no `xrt-smi`).

**Open items:** `ava-/bruce-/carly-telegram` models missing (replies BLOCKED); timelapse check after 05:00 HST; Energy actuating/hardware tests; B1 0% physical check; WEATHER repo decision (canonical `WEATHER/` is not its own RootRecord-Weather-Database repo; data local only); 27 dormant G2 files still use old-root paths; poller stop takes 30 s then SIGKILL; weather rewrites tracked `Pacific/Weather/reports/README.md` each report cycle (commit churn).

**Post-reboot verification list**
1. NPU: `lsmod | grep amdxdna`, `/dev/accel/accel0`; `xrt-smi examine` (XRT tools package may be missing → record, don't install blindly); `flm validate` once FLM is installed.
2. Poller: `systemctl --user status rr-rootserver-poller` active, one `rootserver_poller.py`, NRestarts 0, log `2 - RootRecord-Database/Logs/Automations/automations_current.log` growing; `ENERGY` status line matches fresh `ENERGY/soc/*-last.json`.
3. Relay: exactly one `council-relay.py`, started by boot job `council_relay`, retry fix active (`b3754fb`), no 401 in `Logs/Communications/council-relay.log`.
4. BLE owner (`ava-ecoflow-ble`): one owner, canonical pid/log. Globe: `network-globe-hawaii` active (started by boot job; unit is static). cam_server: one process.
5. Weather: one `Weather/scripts/run_poller.py` (Pacific venv), fresh files under `WEATHER/Hawai'i/`, no Traceback.
6. Ollama: `systemctl status ollama` active, `ollama list` = 12 models. cloudflared: one poller child, tunnel connected.
7. Auto-sync: new `auto:` commits in Pacific/Database/Library; no `index.lock`; no poller reload triggered by G2 pulls.
