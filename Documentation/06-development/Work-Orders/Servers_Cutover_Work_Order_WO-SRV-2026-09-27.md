# WORK ORDER — Pacific Runtime Path Cutover (`skills` → `1 - Servers`)

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-SRV-2026-09-27 |
| **Status** | **IN PROGRESS** — G3 PASS: poller on canonical root, network globe, BLE owner, cam server, frame grab, System sampling, Reports worklog, Plumbing non-NPU, read-only `solar-gate-status`, Telegram relay login/polling, NPU `llama3.2:1b` on demand. Open: Telegram replies off until sign-off (quiet mode; models were rebuilt), Energy actuating actions + timelapse VERIFY PENDING. G2 code KEPT (retire only with Alexander sign-off). Header corrected 2026-09-29 evening; earlier "NPU BLOCKED" / "models missing" notes below are historical. |
| **Updated** | 2026-09-30 afternoon — Council path: NPU `llama3.2:3b`, sandbox replies on, live council still gated. State snapshot and a refuse-by-default execution broker are in place. See `Documentation/01-operations/HANDOFF.md`. The 02:35 list below is that morning's check. Delta 2 was not transmitting then; freshness is now a measured `observed` / `stale` / `dead` field, not a standing label. |

**Policy:** Do not run the old desk as the poller host.

**Domain naming SOP (standing):** One Pacific folder per domain (the capitalized name already in the tree). Python package name **matches that folder**. Never add a lowercase sibling symlink (e.g. no `energy` → `Energy`) to satisfy G2 imports — rewrite imports instead. Full text: [Pacific-Domain-Import-Playbook-2026-09-28.md](../../00-architecture/Pacific-Domain-Import-Playbook-2026-09-28.md) § Standing rules.

---

## Locked on Pacific

| Item | Status |
| --- | --- |
| systemd ExecStart | Pacific `run-poller.sh` (quoted) |
| Energy (reads + leapfrog + actions) | Reads **PASS** 2026-09-29 22:10 HST (`SUMMARY=` from `src=api`, B2 7%, B1 100%). Actuating actions still pending. Folder **`Energy/` only**. |
| System | source LANDED / runtime **PASS** 2026-09-29 22:13 HST. `sys_stats_cycle` wrote `2 - RootRecord-Database/System/samples/sys-20260929-221323.json`. |
| Plumbing (ollama + FLM warmup) | source LANDED / runtime **PASS** — non-NPU 00:57 HST, NPU `llama3.2:1b` 02:52 HST, both under **`System/scripts/plumbing/`** |
| Reports (worklog + roll-up + archive) | source LANDED / runtime **PASS** 2026-09-29 22:13 HST. Catch-up scan 22:11–22:13; the next scan was 22:13:36–22:13:37. Roll-up and weekly archive are closed under WO-RPT-001. |
| Github (setup-remotes + sync-all) | source LANDED / runtime **PASS** 2026-09-29 22:01 HST. Automatic authority is `github_sync_all` (WO-GH-001). |
| Communications/network (cloudflare + globe command) | source LANDED / runtime **PASS** 2026-09-29 22:13 HST. Globe process is Pacific `Communications/network/local-data-globe/collector.js`. Tunnel was HTTP 200 earlier tonight (WO-CF). |
| Stack reload | Automated reload **does not** open status window (window-close was tearing down stack) |

## Residual G2 (from Pacific `jobs.py` 2026-09-28 ~21:10 HST)

| Domain | Jobs / constants | Notes |
| --- | --- | --- |
| Telegram / coms | `council_relay` | G3 surface + `System/scripts/plumbing/single-flight.sh` landed; runtime verification pending |
| Security/Cameras (formerly A-Eyes) | cam server, frame grab, timelapse | G3 surface landed, including hourly wrapper; runtime verification pending |
| Weather | `weather_poller` | Enabled. Restarted 2026-09-29 22:04 HST after `Weather/.venv` was rebuilt. Geology and voice stay off. The 2026-09-28 “disabled” notes below are historical. |
| Network globe | cwd | runtime **PASS** 2026-09-29 22:13 HST. Live process is Pacific `collector.js` (pid 744076). |

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
| Plumbing (NPU / FLM) | **PASS** 2026-09-29 02:52 HST | FLM 1.0.6 + XRT 2.25; llama3.2:1b via `flm-warmup.sh` + `run-infer.sh` (single-flight) → `[ok] FLM/NPU`, 1.04 s; parallel refused rc 75. Evidence `2 - RootRecord-Database/Logs/Migration/g3-npu-flm-evidence-20260929T125429Z.md` |
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
3. `jobs.py` vs intake: re-checked — `jobs.py` only mentions intake in its header comment, already the canonical `2 - RootRecord-Database/Intake/`; relay state is canonical too. Old `/home/rootrecord/Database/intake/council-relay/` remains (historical). `jobs.py` not touched.
4. `Logs/Communications/council-relay.log` is 0 bytes because the relay's stdout is block-buffered (nohup to file); stderr errors would still appear.
5. `devices.conf` G2 `log_dir`/`state_dir`/`skill_root` — fixed in `58ee023` (see above).
6. Security timelapse check must wait for the 05:00–19:00 HST window.
7. B1 (River 2 Pro) reads 0% — needs a physical check.
8. FLM/NPU BLOCKED (no FLM binary/service).
9. Needs decision: `Energy/db/store.py` still defaults to old-root `ROOTRECORD/rootrecord.db` (no canonical copy); `push-repo-once.sh` still treats `~/.ollama/skills` pulls as runtime code (arms a stack reload).
## NPU prerequisite installation update — 2026-09-29

The operator installed the documented AMD XDNA2/XRT prerequisite stack on the Pacific host: `amdxdna-dkms`, `libxrt-npu2`, and `libxrt2`. The host exposes `/dev/accel/accel0`, and `modinfo amdxdna` resolves the installed driver and firmware entries. The DKMS install reported a `BUILD_EXCLUSIVE` mismatch for kernel `7.0.0-34-generic`, so the NPU is **not yet runtime-verified**. A reboot and post-reboot validation are required before FastFlowLM can be marked installed/verified. No production deployment or legacy retirement is implied by this prerequisite installation.

### FastFlowLM install — paste-ready for Alexander (prepared 2026-09-29 02:50 HST, NOT run)

Checked on the desk (read-only): Ubuntu 26.04.1, kernel 7.0.0-34. The in-tree `amdxdna` 0.7.0 is loaded, firmware `npu_7.sbin` loaded, and `/dev/accel/accel0` exists (root:render). The `ppa:lemonade-team/stable` PPA is already configured. `libxrt2` and `libxrt-npu2` 2.25.0-4~resolute1 are installed; `libxrt-npu2` already ships the XDNA plugin (`libxrt_driver_xdna.so`). Memlock is unlimited for `rootrecord`.
- **`xrt-smi` comes from `libxrt-utils`** (checked with `dpkg -c`). `libxrt-utils-npu` adds `xrt-runner`/`aiebu-*`.
- **FastFlowLM:** the repo moved to `ROCm/FastFlowLM`. The latest release is **v1.0.6** (2026-09-18), `fastflowlm_1.0.6_ubuntu26.04_amd64.deb`, sha256 `22e6fdb62773de1a31426bfcbbf34f14f415358ea976a714c7b5fb0183d33ad7` (matches the GitHub digest). It installs `/opt/fastflowlm/bin/flm` with a `/usr/bin/flm` symlink, which `System/scripts/plumbing/flm-warmup.sh` finds through `PATH`. It has no postinst and all dependencies are user-space.
- **No reboot needed.** The kernel driver and firmware are already live, and these packages are user-space only (the DKMS build is not needed while the in-tree driver works).

```bash
sudo apt update
sudo apt install -y libxrt-utils libxrt-utils-npu
cd /tmp && curl -fLO https://github.com/ROCm/FastFlowLM/releases/download/v1.0.6/fastflowlm_1.0.6_ubuntu26.04_amd64.deb
echo "22e6fdb62773de1a31426bfcbbf34f14f415358ea976a714c7b5fb0183d33ad7  fastflowlm_1.0.6_ubuntu26.04_amd64.deb" | sha256sum -c -
sudo apt install -y ./fastflowlm_1.0.6_ubuntu26.04_amd64.deb
# verify (no sudo)
xrt-smi examine
flm validate
```
After that, `flm_npu_warmup` picks it up at the next poller start; no restart is required for the install itself.

## Weather hook-in + old-root archive — 2026-09-29 ~01:54 HST

- Weather **PASS** (Pacific `Weather/`, venv `Weather/.venv`, job `weather_poller` enabled, data → canonical `Weather/Hawai'i/`). Reports written 2026-09-29 22:13 HST (county reports and manifest). Some NOAA products returned HTML error pages, HTTP 500, or 403; the poller stayed up. Venv rebuilt 22:04 HST after the interpreter was missing. One poller restart 01:49 HST → PID 880218; relay 880530 and weather 880724 now under the poller unit. Old-root data archived to `2 - RootRecord-Database/Archive/Previous-Datasets/G2-old-root-20260929/` (4.5 GB, README only in git). `store.py` → canonical `ROOTRECORD/`; G2 pulls no longer arm a stack reload. Evidence: `2 - RootRecord-Database/Logs/Migration/g3-weather-archive-evidence-20260929T115429Z.md`.

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

- Docs-only pulls no longer reload the stack (02:23 HST, Alexander-approved, Pacific `31fd21e`): `push-repo-once.sh` skips the reload when every pulled file is `*.md`/`*.markdown`/`README*`; code/config/mixed/unknown diffs reload as before.

**Open items:** `ava-/bruce-/carly-telegram` models missing (replies BLOCKED); timelapse check after 05:00 HST; Energy actuating/hardware tests; B1 0% physical check; WEATHER repo decision (canonical `WEATHER/` is not its own RootRecord-Weather-Database repo; data local only); 27 dormant G2 files still use old-root paths; poller stop takes 30 s then SIGKILL; weather rewrites tracked `Pacific/Weather/reports/README.md` each report cycle (commit churn).

**Post-reboot verification list**
1. NPU: `lsmod | grep amdxdna`, `/dev/accel/accel0`; `xrt-smi examine` (XRT tools package may be missing → record, don't install blindly); `flm validate` once FLM is installed.
2. Poller: `systemctl --user status rr-rootserver-poller` active, one `rootserver_poller.py`, NRestarts 0, log `2 - RootRecord-Database/Logs/Automations/automations_current.log` growing; `ENERGY` status line matches fresh `ENERGY/soc/*-last.json`.
3. Relay: exactly one `council-relay.py`, started by boot job `council_relay`, retry fix active (`b3754fb`), no 401 in `Logs/Communications/council-relay.log`.
4. BLE owner (`ava-ecoflow-ble`): one owner, canonical pid/log. Globe: `network-globe-hawaii` active (started by boot job; unit is static). cam_server: one process.
5. Weather: one `Weather/scripts/run_poller.py` (Pacific venv), fresh files under `WEATHER/Hawai'i/`, no Traceback.
6. Ollama: `systemctl status ollama` active, `ollama list` = 12 models. cloudflared: one poller child, tunnel connected.
7. Auto-sync: new `auto:` commits in Pacific/Database/Library; no `index.lock`; no poller reload triggered by G2 pulls.

- *Viewer fix 02:20 HST:* status window flashing **fixed — PASS** (read-only `poller-dashboard.py`, single instance, survives reloads). Cause: every Pacific pull (incl. docs-only) triggers a stack reload that killed/reopened `poller-watch`; no gnome-terminal (ptyxis `-e` without hold); G2 autostart. Relay re-crashed 02:08 (old code), restarted once 02:12 with retry fix. Evidence `2 - RootRecord-Database/Logs/Migration/g3-poller-viewer-evidence-20260929T121959Z.md`.

- *Post-reboot 02:33 HST (boot 02:28:09):* **PASS**: poller 3226 (NRestarts 0, status = fresh energy), relay 4634 (boot job, retry fix live, no 401), BLE 3195, globe 5436, cam 5223, weather 5355 (upstream NWS 500s only), ollama 12 models, cloudflared 3509, auto-sync committing, 1 dashboard (autostart→Pacific), 0 G2 duplicates. NPU **partial**: amdxdna + accel0 + firmware OK; `xrt-smi`/`flm` missing (Alexander). Evidence `2 - RootRecord-Database/Logs/Migration/g3-post-reboot-evidence-20260929T123313Z.md`.

## Follow-ups 2026-09-29 ~02:50 HST (no restarts; effective at next natural start)

- Relay log: `ensure-relay.sh` launches with `PYTHONUNBUFFERED=1` (argv unchanged) → `council-relay.log` fills in real time from the next relay start.
- 30 s poller stop, **cause found**: after SIGTERM, the rest of the scheduler pass kept launching jobs. `ensure_tunnel_online` respawned cloudflared and waited up to 45 s for it (logs 02:13:13 → 02:13:25; systemd SIGKILLed python + a new cloudflared). **Fix:** `run_job()` returns right away once `_stop` is set (4 lines, `rootserver_poller.py`; tested on a separate copy, not the live poller). Takes effect at the next poller start; the unit is unchanged.
- Stack-stop weather pattern → `[Ww]eather/scripts/run_poller\.py`. This matches the design: a reload restarts weather, and a weather started by the boot job already sits in the poller cgroup, so `systemctl stop` stops it anyway. The `ensure-weather-poller.sh` match is `[Ww]eather/`, so no duplicates are possible. Note: `weather_poller` and `council_relay` are ON_BOOT only, so a crash mid-session is not auto-restarted until the next poller start.
- Weather retention: PROPOSED in `Pacific/Weather/README.md` §Retention (not applied).
- Evidence: `2 - RootRecord-Database/Logs/Migration/g3-followups-evidence-20260929T124741Z.md`.

- *NPU/FLM 02:56 HST:* **PASS** (was BLOCKED). llama3.2:1b pulled (1.3 GB); one gated NPU inference 1.04 s; parallel refused (75); test server stopped. **Needs Alexander:** warmup/run-infer default `llama3.2:3b` is not downloaded (next poller start will try to fetch it); once FLM is up the relay starts posting Telegram replies via FLM; `--pmode default` is not a listed FLM mode. FLM log moved to git-ignored `Logs/AI/FLM/`; old tracked `GITHUB/logs/flm.log` needs an approved `git rm --cached`. Evidence `2 - RootRecord-Database/Logs/Migration/g3-npu-flm-evidence-20260929T125429Z.md`.
- *03:02 HST (Alexander's choices):* `llama3.2:3b` pre-pulled (2.7 GB, `flm check` OK; listed with 1b). Defaults stay `llama3.2:3b` (warmup, run-infer, job). Warmup `--pmode "${FLM_PMODE:-balanced}"`. **Relay quiet by default:** `RR_RELAY_REPLIES=0` (exported by `ensure-relay.sh`; `council-relay.py` consumes updates with a `[quiet]` log line, no infer, no `sendMessage`; set `=1` to opt in). Offline test: off → 0 infer / 0 sendMessage; on → posts (fake API). Effective at next relay start (Pacific `ebc32a7`). `GITHUB/logs/flm.log` untracked (approved `git rm --cached`, Database `4331c0f`; file kept on disk, now ignored).

- *03:09–03:24 HST — Database Title-case rename:* **PASS**. `ENERGY→Energy`, `SYSTEM→System`, `WEATHER→Weather`, `GITHUB→Github`, `ROOTRECORD→RootRecord`, `WORKLOG→Worklog`, `intake→Intake`. There was one stack stop and one start (03:09:39). Database `92bd69c` has 455 tracked renames, and bulk stays ignored under the new names. Pacific code: `1368822`. No old-name folder came back. Evidence: `Logs/Migration/g3-titlecase-rename-evidence-*.md`.
- *03:10–03:13 HST — OOM restart loop (FIXED):* at every poller start, the `flm_npu_warmup` boot job ran `flm serve llama3.2:3b`, which mapped about 10 GB (9.6 GB shmem). The kernel OOM-killed the whole poller unit 11 times (NRestarts 11). **Fix** (Pacific `ff298b2`): `flm-warmup.sh` is now opt-in only (`FLM_WARMUP_RESIDENT=1`), so no model stays resident. Since 03:13:28 the poller is stable (PID 105444). `run-infer.sh`/`run-ollama.sh` now use `ollama run --keepalive ${OLLAMA_KEEP_ALIVE:-0}` (`3039c3f`). Ollama service env: no `OLLAMA_KEEP_ALIVE` is set (server default 5m). Changing that needs sudo, so it's reported only. **Open (Alexander):** FLM on-demand needs a smaller footprint (1b model or a lower `--ctx-len`) before it can be re-enabled.
- *03:20 HST — EcoFlow stale data, root cause:* Pacific `Energy/` had no `.venv`. `lib/py` fell back to system python3 without `ecdsa`, so eflib was unavailable, every read fell back to the EcoFlow cloud API, and those values were frozen (B2 78% and B1 0% with 168 W out). This was not caused by the rename. **Fix:** created `Pacific/Energy/.venv` (git-ignored) from the pinned G2 energy venv freeze, with no restart. BLE reads resumed at 03:20:31: B2 52.2%→51.69% and B1 5.25%, `src=ble`.
- *Laptop battery:* the dashboard has a B3 "System (laptop)" bar, and the status line has `LAP=100%/Full/AC` (sysfs, read-only; `0ea16cd`; status line applies from the next poller start).
- *03:29 HST — NPU on demand, llama3.2:1b (Alexander's choice):* **PASS**. The defaults are now `llama3.2:1b` in `flm-warmup.sh`, `run-infer.sh` and the jobs.py warmup description; env overrides are kept. The warmup is still opt-in (`FLM_WARMUP_RESIDENT=1`). `run-infer.sh` starts `flm serve` only when FLM is down and the inference lock is idle, using `setsid nice -n 10`, `--pmode balanced` and `--ctx-len ${FLM_CTX_LEN:-4096}`. It stops the server on exit (TERM, then KILL after 10 s). A server that was already running is left alone. `FLM_ON_DEMAND=0` turns this off.
  - Test: one on-demand request took 4.8 s end to end, including the cold start, and was answered on the NPU. FLM peak RSS was about 1.9 GB and minimum available memory 6.0 GB. Afterwards there were 0 flm processes, port 52625 was closed and the lock was IDLE.
  - `llama3.2:3b` stays installed but unused.
  - Evidence: `Logs/Migration/g3-npu-flm-evidence-*.md`.

## Status summary — 2026-09-29 ~03:45 HST (truth-gated)

Test records: [`Documentation/07-testing/`](../../07-testing/README.md). Database root: `/home/rootrecord/RootRecord-Ecosystem/2 - RootRecord-Database` with Title-case folders (`Energy`, `System`, `Weather`, `Github`, `RootRecord`, `Worklog`, `Intake`; `AI`, `Archive`, `Logs` unchanged). The old root `/home/rootrecord/Database/` now holds only `GITHUB/` (backups/flags) and `README.md`; the old data is in `Archive/Previous-Datasets/G2-old-root-20260929/`.

| Surface | State | Evidence / test record |
| --- | --- | --- |
| Poller on new Database root | PASS | `d9f074b`, `75d86f2`, `f27604d`, Database `eabe62e` — [record](../../07-testing/2026-09-29-poller-database-root-realign.md) |
| Status viewer (dashboard, single window; docs-only pulls don't reload) | PASS | `884c832`, `89a8d6d`, `4a4107a`, `31fd21e` — [record](../../07-testing/2026-09-29-poller-dashboard-single-window.md) |
| Weather (Pacific `Weather/`, `Weather/.venv`) | PASS | `b72db19`, `e977252` — [record](../../07-testing/2026-09-29-weather-pacific-venv-hook.md) |
| Post-reboot 02:28 HST, all services | PASS | `g3-post-reboot-evidence-20260929T123313Z.md`, Library `65d654f` — [record](../../07-testing/2026-09-29-post-reboot-all-services.md) |
| NPU / FastFlowLM install + validate | PASS | `g3-npu-flm-evidence-20260929T125429Z.md` — [record](../../07-testing/2026-09-29-npu-flm-install-validate.md) |
| Database Title-case rename (one stack restart 03:09 HST) | PASS | Database `92bd69c`, Pacific `1368822`; docs `0b7be45` (Pacific), `7d2e79b` (Library), `66cbae7` (Database) — [record](../../07-testing/2026-09-29-database-titlecase-rename.md) |
| OOM loop from resident FLM warmup (03:10–03:13 HST) | FAIL → fixed; fix PASS | `ff298b2` (non-resident warmup, `FLM_WARMUP_RESIDENT=1` opt-in), `3039c3f` (`--keepalive 0`); poller PID 105444 stable since 03:13:28 — [record](../../07-testing/2026-09-29-oom-flm-warmup-resident.md) |
| EcoFlow data freshness (`Energy/.venv`) | PASS (battery levels flagged) | WO-SRV 03:20 entry; `Energy/soc/*-last.json` `source: ble` — [record](../../07-testing/2026-09-29-ecoflow-stale-data-energy-venv.md) |
| Laptop battery B3 / `LAP=` | **PASS** 2026-09-29 22:10 HST | `LAP=46%/Discharging/batt` on the energy status line. The 03:38 gap was the pre-commit poller. — [record](../../07-testing/2026-09-29-laptop-battery-b3-dashboard.md) |
| NPU route `llama3.2:1b` on demand | **PASS** (route and own-session, 22:16 HST) | `753168e`, `7000197`; exit 0 and server stopped — [record](../../07-testing/2026-09-29-npu-llama3.2-1b-on-demand.md) |
| Telegram relay | login/polling PASS; replies BLOCKED (models); quiet mode default | `ebc32a7`, `b3754fb` |
| G2 legacy files | KEPT (retire only with Alexander sign-off) | skills `1dcee66` |

**Open items (not done):**
1. `OLLAMA_KEEP_ALIVE=0` in `ollama.service` — **BLOCKED** (needs sudo; the server default is still 5m; the CLI wrappers already pass `--keepalive 0`).
2. `ava-/bruce-/carly-telegram` models missing — relay replies **BLOCKED**. Relay quiet mode is the default (`RR_RELAY_REPLIES=0`) until Alexander opts in. Caveat: in quiet mode incoming messages are consumed (marked read) and will **not** be answered later.
3. Security timelapse check after 05:00 HST — **VERIFY PENDING**.
4. Energy arm/disarm and AC hardware tests — **VERIFY PENDING** (need Alexander's approval).
5. B1 (River 2 Pro) physical check — **VERIFY PENDING**. API at 22:10 HST: B1 100%, B2 (Delta 2) 7%, laptop 46% and discharging. The 03:39 BLE snapshot (B1 5.23%, B2 47.56%) is historical.
6. Weather retention policy — **PROPOSED** (Pacific `Weather/README.md` §Retention, awaiting sign-off).
7. Whether `Weather/` gets its own repo (RootRecord-Weather-Database) — **PROPOSED** / needs decision; weather data is local only.
8. Weather and relay start only at poller boot (ON_BOOT); no mid-session auto-recovery — open design item.
9. 27 dormant G2 files still use old-root paths — **KEPT** unchanged (retire only with Alexander sign-off).
10. `npu-status.sh` exists only in G2 (`~/.ollama/skills/plumbing/scripts/`) — optional Pacific copy, **PROPOSED**.
11. Security items unremediated — **BLOCKED** pending Alexander: camera stills in the public Database repo; `CONNECTION.json` in Pacific history (`6328af6`); G2 still tracks `a-eyes/store/CONNECTION.json`.
12. Laptop `LAP=` status field — **VERIFY PENDING** until the next poller start (`0ea16cd`).
13. `run-infer.sh` own-session fix (`7000197`) — **VERIFY PENDING** on the next real NPU request.

Canonical camera path: Pacific `Security/Cameras/` (no A-Eyes compatibility layer).

## Geology + old-repo migration pass — 2026-09-29 ~13:12–13:45 HST

Copy/port only; no poller restart (PID 105444 untouched); no delivery, playback or model load; G1/G0 sources **KEPT**. Backups: `/home/rootrecord/Database/GITHUB/migration-geology.bak-20260929-131652/`, `/home/rootrecord/Database/GITHUB/migration-old-repos.bak-20260929-133118/`. Evidence: `2 - RootRecord-Database/Logs/Migration/migration-geology-evidence-20260929T2319Z.md`. Matrix: [Old-Repo-Migration-Matrix](../../00-architecture/Old-Repo-Migration-Matrix.md).

| Item | Pacific path | Gate | State |
| --- | --- | --- | --- |
| USGS Hawaiʻi + global quakes, HVO Kīlauea / Mauna Loa | `Geology/scripts/geology_collect.py` | `geology_collect` 300 s, `RR_GEOLOGY=1` | LANDED · manual **PASS** · poller cycle VERIFY PENDING |
| Kīlauea cams | `Geology/scripts/kilauea_cams.py` | `geology_kilauea_cams` 600 s, `RR_KILAUEA_CAMS=1` | LANDED · manual **PASS** |
| Quake backfill | `Geology/scripts/earthquakes_backfill.py` | on demand | LANDED · **PASS** (`--days 1`) |
| Earthquake voice report | `Media/Voice/scripts/voice_reports.py earthquake_report` | `voice_earthquake_report` :08, `RR_VOICE_QUAKE=1` | LANDED · text **PASS** · WAV VERIFY PENDING |
| Sun times | `Energy/scripts/sun_times.py` | `energy_sun_times` hourly, `RR_SUN_TIMES=1` | LANDED · **PASS** |
| Uptime log | `System/scripts/uptime_log.py` | `system_uptime_log` 60 s, `RR_UPTIME_LOG=1` | LANDED · **PASS** |
| MP4 converter | `Media/Video/scripts/mp4_converter.py` | on demand | LANDED · **PASS** |

**Needs Alexander:** set the five flags at the next poller start (then close the VERIFY PENDING cells); approve any delivery (Telegram council-quake, Discord, speakers — **BLOCKED** until then); approve a full-range backfill; accept Database git churn from `Geology/*-last.json` every 5 min. Records: [geology](../../07-testing/2026-09-29-geology-earthquakes-hvo-collector.md), [batch 1](../../07-testing/2026-09-29-old-repo-ports-batch1.md).

### Addendum ~13:46 HST — voice batch 3 + jobs.py standing rule

- Also LANDED (text PASS, WAV VERIFY PENDING): `voice_reports.py hurricane_desk` (job `voice_hurricane_desk`, `RR_VOICE_HURRICANE=1`, 05:50/09:50/12:50/16:55/20:50) and `voice_reports.py kilauea_report` (job `voice_kilauea_report`, `RR_VOICE_KILAUEA=1`, :03). [Test record](../../07-testing/2026-09-29-voice-reports-batch3-hurricane-kilauea.md). Backup `/home/rootrecord/Database/GITHUB/migration-hurricane-desk.bak-20260929-133959/`.
- **Standing rule received 13:45 HST:** `Automations/scripts/jobs.py` is edited only when Alexander asks or a work order requires it. This pass had already added 7 gated blocks (`geology_collect`, `geology_kilauea_cams`, `system_uptime_log`, `voice_earthquake_report`, `voice_kilauea_report`, `energy_sun_times`, `voice_hurricane_desk`); per instruction they are **left in place, not reverted**, all OFF. **Sign-off item:** keep them (then set the flags at the next poller start) or remove them. Exact blocks + line numbers: `2 - RootRecord-Database/Logs/Migration/migration-jobs-py-additions-20260929.md`. No further jobs.py edits after 13:45 HST.
- 13:49 HST: G0 nearest-location tag ported into `Geology/scripts/geology_collect.py` (dataset `Geology/config/global-locations.json`, verbatim G0 copy); temp + one real `quakes` run **PASS**. No new job (rides `geology_collect`). Backup `/home/rootrecord/Database/GITHUB/migration-quake-locations.bak-20260929-134920/`.

### Addendum ~14:10 HST — breadth batch 4 (steering 13:53: breadth over depth, gated off, light smoke each)

- LANDED + smoke: `Communications/web-facts/scripts/web_facts.py` (on demand, **PASS**); `Communications/live-wx/scripts/live_wx.py` (on demand, **PASS**); `System/scripts/host_desks.py net-sample|net-usage|security` (**PASS**, temp root); `Media/Voice/scripts/voice_reports.py solar_desk|security_desk|bandwidth_desk` (text **PASS**, WAV VERIFY PENDING); `Reports/News/scripts/{_collector,hawaii_news}.py` (rc 0, **FAIL on content** — 0 posts, 25 × HTTP 404).
- **No jobs.py edit** (standing rule). Their jobs are PROPOSED with exact blocks in [Pending-Job-Registrations-2026-09-29](../../00-architecture/Pending-Job-Registrations-2026-09-29.md): `system_net_sample` (`RR_NET_SAMPLES`), `voice_solar_desk` (`RR_VOICE_SOLAR`), `voice_security_desk` (`RR_VOICE_SECURITY`), `voice_bandwidth_desk` (`RR_VOICE_BANDWIDTH`), `reports_hawaii_news` (`RR_HAWAII_NEWS`).
- BLOCKED / not ported: official-weather-media (HLS/HWO not collected, OBS), report ledger / catch-up / readiness (playback + report_generation), sunrise-restore (playback), economy brief (MySQL + Discord), council health / Bruce stats (bot tokens + chat-probe model load + alert sends), load categories (field map).
- [Test record with check-later list](../../07-testing/2026-09-29-old-repo-ports-breadth-batch4.md). Backup `/home/rootrecord/Database/GITHUB/migration-breadth.bak-20260929-135720/`.


### Addendum ~14:40 HST: breadth batch 5 (user 14:16: fix voice text, seed news, port the rest; steering 14:27: document everything)

- **Fixes:**
  - Voice clock says "two oh one p.m.".
  - Watts are spoken as words, and a device at zero is "idle".
  - Sun times are spoken as words.
  - Re-smoke of 6 reports: **PASS** (text).
- **Hawaiʻi news:** 16 seed feeds give **278 posts** (**PASS**, temp root).
- **LANDED + smoke PASS:**
  - `Weather/scripts/official_statement.py` (HLS)
  - `Media/Voice/scripts/voice_reports.py official_weather` and `boot_brief` (text; WAV VERIFY PENDING)
  - `Reports/scripts/report_board.py`
  - `Energy/scripts/load_categories.py`
  - `Weather/hurricanes/scripts/global_board.py`
  - `System/scripts/host_hw.py`
  - `Media/Voice/scripts/speech_scrub.py`
  - Verification doc [G1-Scheduler-To-G3-Jobs-Map](../../00-architecture/G1-Scheduler-To-G3-Jobs-Map-2026-09-29.md)
- **No jobs.py edit.** PROPOSED blocks are in [Pending-Job-Registrations-2026-09-29](../../00-architecture/Pending-Job-Registrations-2026-09-29.md): `weather_official_hls` (`RR_OFFICIAL_HLS`), `voice_official_weather` (`RR_VOICE_OFFICIAL`), `voice_boot_brief` (`RR_VOICE_BOOT`, ON_BOOT), `reports_board_catchup` (`RR_REPORT_BOARD`), `weather_hurricane_global` (`RR_HURRICANE_GLOBAL`).
- **Correction:** the weather poller already collects HWO; only HLS was missing.
- **Matrix:** now **35 migrated / 22 partial / 33 missing**. No clean candidates remain; everything left is BLOCKED or OUT.
- [Test record with a check-later list per smoke test](../../07-testing/2026-09-29-old-repo-ports-breadth-batch5.md). Backup `/home/rootrecord/Database/GITHUB/migration-breadth2.bak-20260929-141732/`.

## US-Mainland-Server desk checkout — 2026-09-29 ~13:45–14:00 HST

Second server folder now populated: `1 - Servers/2 - RootRecord-US-Mainland-Server/` = clone of `rootrecordsoftwaresolutions/US-Mainland-Server` at `b61d63c` (placeholder `Communications/` kept). No AWS change, no poller restart, no jobs.py edit. Backup `/home/rootrecord/Database/GITHUB/us-mainland-import.bak-20260929-134629/`. [Architecture](../../00-architecture/US-Mainland-Server.md) · [Test record](../../07-testing/2026-09-29-us-mainland-import-and-ssh.md) · [Plan](../../08-ideas/2026-09-29-aws-mainland-improvement-plan.md).

| Item | State |
| --- | --- |
| Desk checkout (clone, clean, token-free remote) | **PASS** |
| `.env.example` (names only) + README layout + `.gitignore` bytecode rule | LANDED (uncommitted) |
| Auto-sync (`repos.conf` `mainland` row disabled, stale G2 path) | **BLOCKED** — sign-off to repoint + enable |
| `rr-aws` ProxyCommand path fixed locally | LANDED; SSH **FAIL** (no cloudflared connector on AWS, Cloudflare 1033) |
| `rr-aws-ip` [redacted public IP] | **FAIL** — AWS IP is now [redacted public IP] (read-only SSH PASS) |
| AWS disk (`hawaii.ndjson` 1.82 GB, +39 MB/h, trim script missing) | **FAIL** risk — full ≈ 40 h; P0 fix PROPOSED |
| Title-case restructure of the Mainland repo | PROPOSED (coordinated with AWS paths) |

Note: the Smart-Devices pass earlier today (13:31 HST, before the 13:45 standing rule) added one gated block `smart_devices_collect` (`RR_SMART_DEVICES=1`, OFF) to Pacific `jobs.py` at Alexander's request; it is not in the 7-block list above.

### Addendum 14:05–14:35 HST — AWS P0 fixes (approved)

- `hawaii.ndjson` trimmed 1.83 GB → 50.3 MB, and free disk went 1.5G → 3.2G: **PASS**. Auto-trim runs from the `ubuntu` crontab `*/15` on AWS: **LANDED**, fired 14:15.
- `www.rootrecord.cloud` 530/1033 → **200**: cloudflared reinstalled and the existing tunnel [redacted tunnel ID] plus a `server.js` :8090 unit brought up, with no DNS change: **PASS**.
- `rr-aws-ip` HostName → [redacted public IP]: **PASS**. `rr-aws` works through the tunnel with the pinned key, but the desk `known_hosts` is stale (needs OK).
- Details: [test record](../../07-testing/2026-09-29-aws-hawaii-trim-and-cloudflared.md) and [architecture change log](../../00-architecture/US-Mainland-Server.md).


## State at pause — 2026-09-29 16:25 HST

Docs-only refresh (no runtime change). The consolidated sign-off list is in the [worklog "State at pause, 16:25 HST"](../../01-operations/0%20-%20Human%20Operator%20Work%20Logs/2026-09-29%20System%20Operator%20Worklog%20%E2%80%94%20Overnight.md#state-at-pause-1625-hst-2026-09-29).

| Surface | State | Record |
| --- | --- | --- |
| 04:00 approved landings: `service_supervisor` job, relay quiet-mode inbox, Pacific `npu-status.sh`, weather retention (dry run, job disabled) | LANDED / VERIFY PENDING (next poller start). Closes the worklog note "WO-SRV open items need updating" | [supervisor](../../07-testing/2026-09-29-service-supervisor-dry-run.md) · [relay inbox](../../07-testing/2026-09-29-relay-quiet-inbox-parse.md) · [npu-status](../../07-testing/2026-09-29-npu-status-pacific-copy.md) · [retention](../../07-testing/2026-09-29-weather-retention-dry-run.md) |
| AWS Hawaii feed trim + `*/15` auto-trim cron | **PASS** | [trim + cloudflared](../../07-testing/2026-09-29-aws-hawaii-trim-and-cloudflared.md) |
| AWS tunnel, `www.rootrecord.cloud` 200 | **PASS** | same record |
| Globe `server.js` static allowlist (P0) | **PASS** | [allowlist](../../07-testing/2026-09-29-aws-globe-static-allowlist.md) |
| Globe overlay v2 + AWS Ohio node on AWS | LANDED · real browser VERIFY PENDING | [AWS deploy](../../07-testing/2026-09-29-globe-overlay-aws-deploy.md) |
| AWS fallback Phase 2 (trimmed-micro, t3.micro 908 MB), Root Monitor write mode | **PASS** · real fallback VERIFY PENDING · relay send VERIFY PENDING | [deploy](../../07-testing/2026-09-29-aws-fallback-phase2-runtime-deploy.md) · [reclaim](../../07-testing/2026-09-29-aws-fallback-phase2-reclaim-retention.md) · [history](../../07-testing/2026-09-29-aws-globe-history-batched-commits.md) |
| Root Monitor toggle buttons + camera viewer button; desktop launcher | **PASS** / LANDED | [toggle buttons](../../07-testing/2026-09-29-root-monitor-toggle-buttons.md) |
| Android apps import (outside Pacific) | copy **PASS** · build VERIFY PENDING | [Android import](../../07-testing/2026-09-29-android-apps-import.md) |
| Old-repo matrix | 35 / 22 / 33 (unchanged since 14:40) | [matrix](../../00-architecture/Old-Repo-Migration-Matrix.md) |
| AWS feed server `:8787` | open finding, public (sign-off) | [US-Mainland-Server](../../00-architecture/US-Mainland-Server.md) |
| G2 / G1 / G0 legacy sources | KEPT | — |
