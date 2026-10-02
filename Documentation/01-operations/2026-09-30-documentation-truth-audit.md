# Documentation Truth Audit

## Audit Date

2026-09-30, about 18:00 HST, on `/home/rootrecord/RootRecord-Ecosystem`.

The desk clock and the GitHub sync log use different zones. Sync lines stamped `2026-10-01T03:58Z` are the same evening in HST.

**Correction after this audit (same evening):** the `website` catalog row is enabled. It mirrors Pacific `Website/Home/` to `RootRecord-Software-Solutions/RootRecord-Website`. Rows below that say the website row is `enabled=0`, or that the desk has no website folder, describe the desk at about 18:00 HST. They are not the catalog after the public page was published.

Labels in this report are only `VERIFIED`, `STALE`, `UNKNOWN`, `HISTORICAL`, or `CONFLICT`.

## Verified Architecture

`pwd` is `/home/rootrecord/RootRecord-Ecosystem`.

One git repository. Branch `main`. Remote `git@github.com:RootRecord-Software-Solutions/RootRecord-Ecosystem.git`. HEAD at audit time moved during the audit because poller job `github_sync_all` committed and pushed. The checkout is not a set of nested clones.

Tracked top-level entries in `git ls-tree HEAD`:

```text
0 - Master-Prompt
1 - Servers
2 - RootRecord-Database
4 - RootRecord-Node
5 - RootRecord-Library
6 - Android Development
Pull.sh
Push.sh
README.md
test-reports
verify.sh
```

Also on disk, not separate git repositories:

| Path | What it is |
| --- | --- |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/` | Directory inside the umbrella. VERIFIED. No `.git` here. |
| `1 - Servers/2 - RootRecord-US-Mainland-One/` | Directory inside the umbrella. VERIFIED. No `.git` here. |
| `1 - Servers/3 - User Nodes/` | Directory inside the umbrella. |
| `2 - RootRecord-Database/` | Directory inside the umbrella. VERIFIED. No `.git` here. |
| `5 - RootRecord-Library/` | Directory inside the umbrella. VERIFIED. No `.git` here. |
| `Github-worktrees/pacific`, `database`, `library` | Separate git checkouts used as mirror publishes. Ignored by the umbrella. Each has its own `origin`. |
| `Old repos deleted and merged/` | Ignored local archive. Contains a nested `.git` under `ollama-skills-g2-2026-09-30`. |
| `7 - Client Projects/` | Empty directory. Not in `HEAD`. UNKNOWN purpose. |
| `3 - RootRecord-Website/` | Not on disk. The umbrella `.gitignore` ignores that name. |
| `/home/rootrecord/Database/` | Not on disk. |

The seven architecture categories exist and hold the 31 reorganized pages:

```text
Documentation/01-AI-and-Agent-Runtime/          5 files
Documentation/02-Runtime-Jobs-and-Control/      5 files
Documentation/03-Pacific-Server-Current-Architecture/  6 files
Documentation/04-Migration-and-Legacy-Recovery/ 6 files
Documentation/05-Products-Repositories-and-Applications/  3 files
Documentation/06-Domains-and-External-Systems/  5 files
Documentation/07-Communications/                1 file
```

The same 31 filenames also exist under `Documentation/00-architecture/` and under `Documentation/archive/2026-W40/architecture-pre-reorg/`. SHA-256 matched across all three copies except `Repository-Ownership-Model.md`, which had diverged. The new-path copy and the `00-architecture` copy were then rewritten to the same verified text. The archive copy was not edited.

`00-architecture/` still holds current material that was not part of the 31: `Decisions/`, `Governance/`, `Schemas/`, and `archive/`.

## Verified Runtime Facts

### systemd

No RootRecord system timer is enabled. User timers are Ubuntu snap and insights timers only.

| unit | enabled | active | ExecStart | WorkingDirectory | environment | restart | description |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ollama.service` | enabled | active | `/usr/local/bin/ollama serve` | unset | `PATH` only. User `ollama` | `always`, 3s | Ollama Service |
| `rr-rootserver-poller.service` | enabled | active | `run-poller.sh` | Pacific tree | `POLLER_LOG`, `POLLER_PUBLIC_HOST=rootserver.rootrecord.cloud`, `POLLER_BIND=127.0.0.1`, `POLLER_PORT=8799`. Drop-in appends the automations log | `on-failure`, 5s | RootRecord Pacific RootServer Poller |
| `ava-ecoflow-ble.service` | enabled | active | `Energy/scripts/ble/ble-owner.py` | unset (user home) | none in the unit | `on-failure`, 5s | RootRecord EcoFlow BLE Owner |
| `network-globe-hawaii.service` | static | active | `local-data-globe/collector.js` | `Communications/network/local-data-globe` | none in the unit | `no` | RootRecord Hawaii Network Globe Collector |

`systemctl cat ollama` printed that the unit changed on disk and the loaded copy is outdated. `systemctl show` still matched the fragment read from `/etc/systemd/system/ollama.service`. No `daemon-reload` was run.

### Ollama

- Binary: `/usr/local/bin/ollama`, version `0.34.4`. VERIFIED.
- Service: enabled and active, as above. VERIFIED.
- Model store: `/usr/share/ollama/.ollama` (65G). The service user is `ollama`, home `/usr/share/ollama`. VERIFIED.
- `~/.ollama/models` is 4K. It is not the model store. `~/.ollama/skills` exists. The disabled `skills` sync row does not point there.
- Installed tags from `ollama list`: `rr-energy` 1.6 GB, `ava-telegram` 2.0 GB, `bruce-telegram` 2.0 GB, `carly-telegram` 2.0 GB, `rr-cameras` 1.6 GB, `rr-council-bruce` 2.0 GB, `rr-council-ava` 2.0 GB, `rr-council-carly` 2.0 GB, `rr-exec` 1.6 GB, `rr-reason` 2.0 GB, `rr-security` 2.0 GB, `rr-system` 1.6 GB, `rr-weather` 1.6 GB, `gemma4:e4b` 9.6 GB, `deepseek-coder-v2:16b` 8.9 GB, `starcoder2:15b` 9.1 GB, `phi4:14b` 9.1 GB, `qwen2.5:14b` 9.0 GB, `nomic-embed-text` 274 MB, `qwen2.5:1.5b-instruct-q8_0` 1.6 GB, `llama3.2:3b-instruct-q4_K_M` 2.0 GB, `gemma2:9b-instruct-q4_K_M` 5.8 GB, `qwen2.5:7b-instruct-q4_K_M` 4.7 GB, `mistral:7b-instruct-v0.3-q4_K_M` 4.4 GB, `qwen2.5-coder:7b-instruct-q4_K_M` 4.7 GB.
- Not installed as Ollama tags: `ava`, `ava-architect`, `ava-pr`, `bruce`, `bruce-ops`, `bruce-philosophy`, `carly`, `carly-appsec`, `carly-energy`. IDENTITY pages now say that.

### Council and inference

Runtime files:

```text
Automations/scripts/jobs.py
verify.sh   (ecosystem root; calls Pacific System/scripts/verify.py)
Communications/telegram/scripts/council-relay.py
Communications/telegram/scripts/ensure-relay.sh
Communications/telegram/scripts/desk-live.py
System/scripts/plumbing/run-infer.sh
System/scripts/state-aggregate.py
Automations/execution/execution-broker.py
```

Running council process environment, keys only: `FLM_MODEL=llama3.2:3b`, `FLM_PMODE=performance`, `RR_NPU_ONLY=1`, `RR_NPU_PERSONA=1`, `RR_RELAY_REPLIES=0`. `FLM_CTX_LEN` is unset, so `run-infer.sh` uses `${FLM_CTX_LEN:-4096}`. VERIFIED from the process and the script default.

`flm list` shows `llama3.2:1b` and `llama3.2:3b` installed. Other FLM names in that list are not installed. `flm --version` is `FLM v1.0.6`. `/dev/accel/accel0` exists.

`relay.conf` has `SANDBOX_REPLIES=1`. `council-relay.py` answers the sandbox chat when that flag is 1, and keeps the live council quiet unless `RR_RELAY_REPLIES=1`. No send was performed. The gate values are VERIFIED. A successful sandbox post was not observed.

`RR_NPU_ONLY=1` skips the Ollama fallback. Other callers still default to `llama3.2:1b` and may fall back. Specialist routing stays off unless `RR_SPECIALIST_ROUTING=1`. That variable is unset in the running relay.

### Gates

`2 - RootRecord-Database/System/control-panel/execution-gates.json` is absent. `gates.py` then loads the seed `Apps/Control-Panel/execution-gates.json`. VERIFIED.

Seed: `modes.build`, `modes.recovery`, and `modes.deployment` are false. `steps.build.cursor_api` is false. `steps.recovery.run_existing_program` is false. Read and diagnose inspect stay open in the seed.

`execution-broker.py` refuses a capability when its monitor gate is closed. It does not launch a side effect. `cursor_fallback` in `jobs.py` is `enabled: False`.

`service_supervisor` is enabled. `supervise-services.sh` respawns the weather poller and `council-relay.py` only, at most 3 times per 30 minutes, then blocks. It is not a general restart gate.

### Jobs in the running poller

`run-poller.sh` exports `RR_NIGHT_SLEEP=1`, `RR_VOICE_DELIVER=1`, `RR_TELEGRAM_DEST=sandbox`, and these at `1`: `RR_VOICE_NWS`, `RR_VOICE_KILAUEA`, `RR_VOICE_SECURITY`, `RR_VOICE_BANDWIDTH`, `RR_VOICE_SYSTEM_PERF`, `RR_VOICE_ENERGY`, `RR_VOICE_REMAINING`, `RR_VOICE_QUAKE`, `RR_VOICE_SOLAR`, `RR_GEOLOGY`, `RR_NET_SAMPLES`. The running poller environment matches that list.

Hard-on in `jobs.py`: `self_terminal`, `cloudflare_tunnel`, `github_setup_remotes`, `ollama_warmup`, `flm_npu_warmup`, `council_relay`, `security_camera_server`, `security_timelapse_catchup`, `weather_poller`, `network_globe_hawaii`, `ecoflow_read_boot`, `heartbeat`, `ecoflow_read_cycle`, `sys_stats_cycle`, `github_sync_all`, `worklog_scan`, `security_camera_frame_grab`, `service_supervisor`, `ensure_tunnel_online`, `automations_log_hourly_archive`, `security_timelapse_hourly_compile`, `security_timelapse_daily_render`, `reports_daily_roll_up`, `reports_weekly_archive`.

On because the running poller set the matching variable: `geology_collect`, `system_net_sample`, `voice_system_perf`, `voice_nws_weather`, `voice_energy_report`, `voice_remaining_tasks`, `voice_earthquake_report`, `voice_kilauea_report`, `voice_solar_desk`, `voice_security_desk`, `voice_bandwidth_desk`.

Hard-off: `country_location_pollers`, `discord_poller`, `weather_retention`, `log_retention`, `path_index`, `api_prices`, `cursor_fallback`.

Off because the variable is unset and the default is `0`: `council_quake_telegram`, `geology_kilauea_cams`, `geology_kilauea_public_draft`, `smart_devices_collect`, `system_uptime_log`, `system_python_drop`, `weather_radar_zip`, `earthquake_discord_post`, `communications_slack`, `stripe_poll`, `vercel_builds`, `council_health`, `energy_river_car_drive`, `inbox_drain`, `public_health`, `kilauea_draft_count`, `note_work_draft`, `voice_hourly_chime`, `weather_us_states`, `ai_processing_report_hourly`, `ai_usage_report`, `template_reports_daily`, `voice_morning_report`, `voice_midday_report`, `voice_late_report`, `voice_late_final_report`, `voice_hurricane_desk`, `media_hurricane_radio`, `bruce_stats_posts`, `adsense_eod`, `admob_eod`, `overnight_relay`, `reports_board_catchup`.

### State files

`state-aggregate.py` writes `2 - RootRecord-Database/System/status/rootrecord-state.json` and reads `desk-live.txt` under Database `Intake/`. `desk-live.py` writes the desk file. `ecosystem-skip-autocommit.txt` skips `System/status`, samples, layers, worklogs, and logs for the umbrella auto-commit. Database `.gitignore` also ignores live logs, `Energy/state`, `Weather/`, and control-panel live settings.

`state-aggregate.py` still opens `Documentation/00-architecture/Old-Repo-Migration-Matrix.md`. That path exists because the duplicate copy remains. The canonical page is `Documentation/04-Migration-and-Legacy-Recovery/Old-Repo-Migration-Matrix.md`. The Python path was not changed.

## Verified Repository Facts

Classification uses the filesystem, `git ls-tree`, `repos.conf`, worktree remotes, and `gh api`. A document was not enough.

| Item | Class |
| --- | --- |
| `RootRecord-Software-Solutions/RootRecord-Ecosystem` | Current GitHub repository. This desk's git root. `repos.conf` row `ecosystem`, `enabled=1`, mode `inplace`. |
| `RootRecord-Software-Solutions/RootRecord-Pacific-Solar-Server` | Current GitHub repository. On this desk, a directory plus mirror checkout `Github-worktrees/pacific`. Row `pacific`, `enabled=1`, mode `mirror`. |
| `RootRecord-Software-Solutions/RootRecord-Database` | Current GitHub repository. Directory plus `Github-worktrees/database`. Row `database`, `enabled=1`, mode `mirror`. |
| `RootRecord-Software-Solutions/RootRecord-Library` | Current GitHub repository. Directory plus `Github-worktrees/library`. Row `library`, `enabled=1`, mode `mirror`. |
| `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server` | Historical GitHub repository. Still exists. Row `skills`, `enabled=0`, path under `Old repos deleted and merged/ollama-skills-g2-2026-09-30`. |
| `rootrecordsoftwaresolutions/RootRecord-Website` | GitHub repository. Still exists. Not a directory with `.git` on this desk. Row `website`, `enabled=0`, path inside that old snapshot. Pacific `Website/` is a directory inside the umbrella. |
| `RootRecord-Software-Solutions/US-Mainland-One` | GitHub repository. Still exists. Row `mainland`, `enabled=0`, path inside that old snapshot. The live tree is `1 - Servers/2 - RootRecord-US-Mainland-One/` and has no `.git`. |
| `rootrecordsoftwaresolutions/RootRecord-Weather-Database` | GitHub repository. Still exists. Not a nested clone. Desk weather bytes are `2 - RootRecord-Database/Weather/`, ignored by the Database `.gitignore`. |
| `AvaIvy/AvaIvy-Agent-Context` | Personal GitHub repository. `AvaIvy/Agent-Context` resolves to this full name. Not synced by `repos.conf`. |
| `CarlyMal/Carly-Agent-Context` | Personal GitHub repository. `CarlyMal/Agent-Context` resolves to this full name. Not synced by `repos.conf`. |
| `BruceMonitor/Agent-Context` | Personal GitHub repository. Not synced by `repos.conf`. |
| `RootRecord/rootrecord-weather-manager-download` | GitHub repository. Not a checkout on this desk. |
| `RootRecord/rootrecord-business-manager-download` | GitHub repository. Not a checkout on this desk. |
| `RootRecord/Doc-Repo` | GitHub repository. Not a checkout on this desk. |
| `6 - Android Development/` | Directory inside the umbrella. |
| `4 - RootRecord-Node/` | Directory inside the umbrella. README is empty. UNKNOWN role. |
| `7 - Client Projects/` | Empty untracked directory. UNKNOWN role. |

### GitHub sync

`Github/scripts/repos.conf` is the catalog. `sync-all.sh` runs enabled rows through `push-repo-once.sh`. `jobs.py` job `github_sync_all` is enabled. There is no crontab and no RootRecord systemd timer.

Observed at 2026-09-30 17:58 HST in the automations log: `ecosystem`, `pacific`, and `database` pushed; `library` was already even with GitHub. `skills` last appeared at 17:38 HST, before `repos.conf` was written at 17:45:46 HST with `skills` disabled. `website` and `mainland` produced no log lines.

`Pull.sh` and `Push.sh` are manual. Their headers say not to schedule them. They look for `.git` inside Pacific, Database, and Library, which are directories, and they do not pull or push the umbrella.

`STALE` sentences that said `skills` stays enabled, that sync is "one timer", and that `/home/rootrecord/Database/` holds the flags were corrected in the current ownership page, the master-prompt link file, and the three `REPOS.md` files.

## Documentation Fixed Automatically

| File | Problem | Fix | Evidence |
| ---- | ------- | --- | -------- |
| 16 reorganized architecture pages | Relative links still assumed every page lived in one folder | Retargeted to the new category folders. `archive/README.md` from the migration index now points at `00-architecture/archive/README.md` | Link check: those targets exist. The archive snapshot was not edited |
| `Repository-Ownership-Model.md` (new path and `00-architecture` copy) | Said `skills` stays enabled, `/home/rootrecord/Database/` holds flags, and `Pull.sh` pulls this desk | Rewrote the sync, flag, and history paragraphs to match `repos.conf` and the filesystem | `repos.conf` `skills/website/mainland` are `0`. `/home/rootrecord/Database` is absent. Live folders have no `.git` |
| `0 - Master-Prompt/prompts/08-repository-and-file-links.md` | Same stale sync and path claims. Said the website desk folder was gone and nothing local exists | Pointed at Pacific `Website/`, the real Mainland directory, disabled sync rows, and the new ownership path | Those directories exist. `3 - RootRecord-Website/` does not |
| `5 - RootRecord-Library/README.md` | Map omitted the seven new categories and named `adr/` and `schemas/`, which are not directories | Map lists the seven categories and drops the missing names | `ls` of `Documentation/` |
| `README.md` (umbrella) | System-map link used `00-architecture/SYSTEM-MAP.md` | Link uses `03-Pacific-Server-Current-Architecture/SYSTEM-MAP.md` | File exists there |
| `Documentation/02-agents/README.md` | Team-constitution link used the old folder. Personal mirror names disagreed with GitHub `full_name` | New folder path. `AvaIvy/AvaIvy-Agent-Context` and `CarlyMal/Carly-Agent-Context` | `gh api` full names. File exists |
| Agent `CONTEXT/REPOS.md` (Ava, Bruce, Carly) | Called sync "one timer" and called `02-agents` an empty placeholder index | Poller job, not a systemd timer. Index description matches the files on disk | `systemctl --user list-timers` has no RootRecord timer. `02-agents/` contains modes, requests, handoff, capabilities |
| `IDENTITY.md` (Ava, Bruce, Carly) | "Live Models" listed tags absent from `ollama list` | Installed tags versus absent names | `ollama list` |
| Bruce `ROLE-AND-BOUNDS.md` | Inference path `plumbing/scripts/run-infer.sh` | `System/scripts/plumbing/run-infer.sh` | `find` of `run-infer.sh` |
| Living READMEs and five idea pages and four open work orders | Current pointers still named `Documentation/00-architecture/<moved file>` | Pointers use the new category folder | Same filename exists in the new folder |
| `03-security/README.md`, `04-data/README.md`, `05-public-surface/README.md`, `07-testing/README.md`, `2026-09-30-voice-desk.md` | Broken or old-folder links | Completed work orders linked under `Complete/`. Moved pages linked in their new folders | Targets exist |
| Pacific `Media/Voice`, `Apps/Control-Panel`, `Geology` READMEs | Old architecture paths | New category paths | Targets exist |

The poller job `github_sync_all` committed some of those edits as `auto:` desk-sync commits while this audit was running. This report and the still-uncommitted path fixes are committed separately as documentation.

## Current Documentation Still Unverified

| File | Claim | Why Unverified | Required Command/Test |
| ---- | ----- | -------------- | --------------------- |
| `relay.conf` / SYSTEM-MAP "sandbox answers" | A sandbox message receives an inference reply | `SANDBOX_REPLIES=1` and `RR_RELAY_REPLIES=0` were read. No message was sent | Operator send in the sandbox chat only, then read the relay log for a post line. Do not enable live-council replies |
| `4 - RootRecord-Node/README.md` | The directory is part of the product | The README is empty. The directory is tracked. No other source in this audit assigned a role | Read any non-README file under `4 - RootRecord-Node` and ask Alexander what the node is |
| `7 - Client Projects/` | A client-project home | Empty. Not in `HEAD` | `ls -la "7 - Client Projects"` and ask Alexander whether to keep the directory |
| `ollama.service` warning | Loaded unit differs from the on-disk fragment | `systemctl cat` warned. `systemctl show` matched the fragment that was read. No reload was performed | `systemctl show ollama -p FragmentPath,DropInPaths,ExecStart,Environment` compared with `systemctl cat ollama` after a human decides whether `daemon-reload` is allowed |
| Personal GitHub packs | Library packs match `AvaIvy/AvaIvy-Agent-Context`, `CarlyMal/Carly-Agent-Context`, and `BruceMonitor/Agent-Context` | The repositories exist. This desk does not sync them. Their trees were not diffed | `gh repo clone` into a temp directory and `diff -rq` against `Agent Context/`. Do not point `repos.conf` at them |
| `Documentation/02-Runtime-Jobs-and-Control/G3-Runtime-Verification-Checklist-2026-09-28.md` "PASS" rows dated 2026-09-28 and 2026-09-29 | Each PASS row is still true tonight | The file is a dated checklist. This audit verified the council model, poller, Ollama, and FLM version. It did not re-run the checklist | `bash verify.sh` and the checklist commands, read-only |
| Master prompt sentence that geology `*-last.json` publication is not signed off | Sign-off state | `hawaii-last.json` is tracked. No sign-off document was opened in this pass | Read the sign-off list in `2026-09-30-whats-left-for-alexander.md` and compare with `git ls-files '2 - RootRecord-Database/Geology/**/*-last.json'` |

## Contradictions Requiring Human Decision

| File(s) | Conflict | Evidence | Decision Needed |
| ------- | -------- | -------- | --------------- |
| `Documentation/00-architecture/<31 files>` and `Documentation/01-AI-and-Agent-Runtime` through `07-Communications` | Two live copies. Runtime still reads the old matrix path | SHA-256 matched for 30 files. `state-aggregate.py` sets `MATRIX` to `Documentation/00-architecture/Old-Repo-Migration-Matrix.md`. `Apps/Control-Panel/Lib/rr_migration.json` still names old paths | Keep the duplicates until a runtime change retargets those readers, or accept the duplicates as the compatibility copies. Do not delete them in a docs-only pass |
| `Work-Orders/Servers_Cutover_Work_Order_WO-SRV-2026-09-27.md` | A log line says the Mainland folder is a clone of `US-Mainland-One` | The directory exists and has no `.git`. The GitHub repository still exists. The sync row is disabled and does not point at this directory | Leave the sentence as a dated log, or add a later note that the desk copy is no longer a nested clone. This audit only retargeted the doc link |
| Agent IDENTITY vs ROLE-AND-BOUNDS | No character conflict found | IDENTITY holds name, role summary, and personality. ROLE-AND-BOUNDS holds ownership and walls. Carly IDENTITY says "Never Clara". No current pack calls her Clara | None for character. Do not invent a personality winner |

```text
CONFLICT
Canonical candidate:
  Documentation/04-Migration-and-Legacy-Recovery/Old-Repo-Migration-Matrix.md
Conflicting files:
  Documentation/00-architecture/Old-Repo-Migration-Matrix.md
  1 - Servers/1 - RootRecord-Pacific-Solar-Server/System/scripts/state-aggregate.py
Evidence:
  Both markdown copies hashed equal before this audit.
  state-aggregate.py line sets MATRIX to the 00-architecture path.
Required human decision:
  Retarget the Python constant in a runtime change, then decide whether the 00-architecture duplicates stay as compatibility copies.
```

## Historical Material Left Untouched

- `Documentation/archive/2026-W40/architecture-pre-reorg/` including its copy of `Repository-Ownership-Model.md`, which still says `skills` stays enabled.
- `Documentation/00-architecture/archive/` session notes.
- `Documentation/01-operations/archive/` and `0 - Human Operator Work Logs/`.
- `Documentation/07-testing/2026-09-29-*.md` bodies. They still cite `00-architecture/` paths. Those paths still resolve because the duplicates remain.
- `Work-Orders/Complete/` and `Work-Orders/drafts/`.
- `2 - RootRecord-Database/Logs/Migration/`.
- `Apps/Control-Panel/Lib/rr_migration.json` and `2 - RootRecord-Database/System/PathIndex/paths.txt` (runtime config and a generated index).

## Broken Links Remaining

Current Library markdown outside archive, work logs, and `Work-Orders/Complete` has two matches that are not files. They are IPA spellings in `Documentation/07-testing/2026-09-29-pronunciation-candidates-proposed.md`: `](/mˌɑhˈɛlɛ/)` and `](/ipa/)`. Left in place so the test record stays intact.

Inside `Work-Orders/Complete/Ops_Weekly_Archive_Work_Order_WO-ARCH-2026-09-27.md`, `](./Complete/)` does not resolve. That completed work order was not rewritten.

Old-path citations that still resolve, and were left alone: dated testing records, drafts, completed work orders, operator work logs, and `rr_migration.json`.

## Recommended Cursor Follow-Up

## Prompt 1 — sandbox reply observation

```text
You are updating one specific RootRecord documentation fact.

DO NOT change runtime behavior.

Files:
5 - RootRecord-Library/Documentation/03-Pacific-Server-Current-Architecture/SYSTEM-MAP.md
5 - RootRecord-Library/Documentation/01-operations/2026-09-30-documentation-truth-audit.md

Question:
Does a message in the sandbox chat receive an inference reply while RR_RELAY_REPLIES=0 and SANDBOX_REPLIES=1?

Commands/evidence to inspect:
Pacific Communications/telegram/config/relay.conf keys SANDBOX_REPLIES and ENABLED only. Do not print chat ids or tokens.
The running council-relay.py environment for RR_RELAY_REPLIES, RR_NPU_ONLY, FLM_MODEL.
One operator-sent sandbox message, then the relay log line that says post or quiet. Do not set RR_RELAY_REPLIES=1.

If verified:
Say the sandbox post was observed, with the log timestamp and no message body.

If disproved:
Mark the "sandbox answers" sentence STALE and quote the quiet log line.

If still unknown:
Leave the sentence as configured-but-not-observed.

Do not guess.
```

## Prompt 2 — RootRecord-Node role

```text
You are updating one specific RootRecord documentation fact.

DO NOT change runtime behavior.

Files:
4 - RootRecord-Node/README.md
5 - RootRecord-Library/Documentation/01-operations/2026-09-30-documentation-truth-audit.md

Question:
What is 4 - RootRecord-Node on this desk?

Commands/evidence to inspect:
find "4 - RootRecord-Node" -type f
git ls-files "4 - RootRecord-Node"
Ask Alexander if the tree is empty of purpose.

If verified:
Write a short README that states only what the files show.

If disproved:
Do not invent a product role.

If still unknown:
Leave the README empty and keep the audit row UNKNOWN.

Do not guess.
```

## Prompt 3 — Client Projects directory

```text
You are updating one specific RootRecord documentation fact.

DO NOT change runtime behavior.

Files:
7 - Client Projects/
5 - RootRecord-Library/Documentation/01-operations/2026-09-30-documentation-truth-audit.md

Question:
Is the empty 7 - Client Projects directory a current home or an unused folder?

Commands/evidence to inspect:
ls -la "7 - Client Projects"
git status --short -- "7 - Client Projects"
git check-ignore -v "7 - Client Projects"

If verified:
One sentence in the audit report.

If disproved:
Do not delete the directory in a documentation pass.

If still unknown:
Leave UNKNOWN.

Do not guess.
```

## Prompt 4 — ollama unit reload warning

```text
You are updating one specific RootRecord documentation fact.

DO NOT change runtime behavior. Do not run daemon-reload unless Alexander asks.

Files:
5 - RootRecord-Library/Documentation/01-operations/2026-09-30-documentation-truth-audit.md

Question:
Does the loaded ollama.service differ from /etc/systemd/system/ollama.service?

Commands/evidence to inspect:
systemctl cat ollama
systemctl show ollama -p FragmentPath -p DropInPaths -p ExecStart -p Environment -p User -p Restart -p ActiveState -p UnitFileState

If verified:
Record the differing fields only.

If disproved:
Record that the warning did not correspond to a visible field difference.

If still unknown:
Keep the audit row UNKNOWN.

Do not guess.
```

## Prompt 5 — personal mirror drift

```text
You are updating one specific RootRecord documentation fact.

DO NOT change runtime behavior. Do not add a repos.conf row.

Files:
5 - RootRecord-Library/Agent Context/Ava-Agent-Context/
5 - RootRecord-Library/Agent Context/Bruce-Agent-Context/
5 - RootRecord-Library/Agent Context/Carly-Agent-Context/
5 - RootRecord-Library/Documentation/01-operations/2026-09-30-documentation-truth-audit.md

Question:
Do the GitHub personal packs match the Library packs?

Commands/evidence to inspect:
gh api repos/AvaIvy/AvaIvy-Agent-Context --jq .full_name
gh api repos/CarlyMal/Carly-Agent-Context --jq .full_name
gh api repos/BruceMonitor/Agent-Context --jq .full_name
Clone each into /tmp and diff -rq against the Library pack. Do not print secrets.

If verified:
State match or list differing filenames.

If disproved:
List differing filenames. Do not choose which personality text wins.

If still unknown:
Leave UNKNOWN.

Do not guess.
```

## Prompt 6 — checklist PASS rows

```text
You are updating one specific RootRecord documentation fact.

DO NOT change runtime behavior.

Files:
5 - RootRecord-Library/Documentation/02-Runtime-Jobs-and-Control/G3-Runtime-Verification-Checklist-2026-09-28.md

Question:
Which PASS rows from 2026-09-28 and 2026-09-29 are still true on 2026-09-30?

Commands/evidence to inspect:
bash verify.sh
The checklist's own read-only commands.
Do not start jobs, send, or restart.

If verified:
Add a dated note per row that was re-run. Do not erase the old PASS line.

If disproved:
Mark that row STALE with the command output.

If still unknown:
Leave the old row and say it was not re-run.

Do not guess.
```

## Prompt 7 — geology publication sign-off

```text
You are updating one specific RootRecord documentation fact.

DO NOT change runtime behavior.

Files:
0 - Master-Prompt/prompts/08-repository-and-file-links.md
5 - RootRecord-Library/Documentation/01-operations/2026-09-30-whats-left-for-alexander.md

Question:
Is publication of Geology *-last.json signed off?

Commands/evidence to inspect:
git ls-files "2 - RootRecord-Database/Geology/**/*-last.json"
The sign-off list in 2026-09-30-whats-left-for-alexander.md

If verified:
Say signed off or not signed off, and cite the list line.

If disproved:
Correct only the sign-off sentence.

If still unknown:
Leave the master-prompt sentence unchanged.

Do not guess.
```

## Prompt 8 — duplicate architecture copies

```text
You are updating one specific RootRecord documentation fact.

DO NOT change runtime behavior in this pass. Do not delete the duplicates until the reader is retargeted.

Files:
1 - Servers/1 - RootRecord-Pacific-Solar-Server/System/scripts/state-aggregate.py
1 - Servers/1 - RootRecord-Pacific-Solar-Server/Apps/Control-Panel/Lib/rr_migration.json
5 - RootRecord-Library/Documentation/00-architecture/
5 - RootRecord-Library/Documentation/04-Migration-and-Legacy-Recovery/Old-Repo-Migration-Matrix.md

Question:
After a later runtime change, should Documentation/00-architecture/ keep duplicate copies of the 31 moved pages?

Commands/evidence to inspect:
rg -n "Documentation/00-architecture/" --glob '!**/archive/**' --glob '!**/Worklog/**'
python3 hash compare of each of the 31 names in 00-architecture versus the new folder.

If verified:
Retarget state-aggregate.py MATRIX only in a runtime-approved change, then remove a duplicate only if no reader remains.

If disproved:
Keep both copies and say so in the ownership page.

If still unknown:
Keep both copies.

Do not guess.
```

## Prompt 9 — mainland clone sentence

```text
You are updating one specific RootRecord documentation fact.

DO NOT change runtime behavior.

Files:
5 - RootRecord-Library/Documentation/06-development/Work-Orders/Servers_Cutover_Work_Order_WO-SRV-2026-09-27.md

Question:
Should the 2026-09-29 log line that calls 1 - Servers/2 - RootRecord-US-Mainland-One a clone stay as history?

Commands/evidence to inspect:
find "1 - Servers/2 - RootRecord-US-Mainland-One" -name .git
The WO paragraph that cites b61d63c.

If verified:
Add one later sentence that the desk copy has no .git on 2026-09-30. Do not delete the old log line.

If disproved:
Leave the log line untouched.

If still unknown:
Leave the log line untouched.

Do not guess.
```

## Final Truth State

| Topic | State |
| --- | --- |
| Umbrella is one git root on `main` | VERIFIED |
| Pacific, Database, Library, Mainland are directories here | VERIFIED |
| Seven new architecture categories hold the 31 pages | VERIFIED |
| Duplicate copies under `00-architecture/` and the archive | VERIFIED copies. CONFLICT on which copy runtime should read |
| `skills` sync row enabled | STALE in older sentences. Current `repos.conf` is disabled. VERIFIED |
| `/home/rootrecord/Database/` | STALE. Path absent. VERIFIED |
| GitHub sync is a poller job, not a systemd timer | VERIFIED |
| `ecosystem`, `pacific`, `database`, `library` rows executing | VERIFIED at 17:58 HST |
| `website` and `mainland` rows | VERIFIED disabled. Not executing |
| Ollama installed, enabled, active, models listed above | VERIFIED |
| Identity "live model" tags that are absent | STALE before this audit. IDENTITY now matches `ollama list` |
| Council model `llama3.2:3b`, context default 4096, no Ollama fallback | VERIFIED |
| Sandbox reply actually posted | UNKNOWN |
| `cursor_api` and `cursor_fallback` | VERIFIED off |
| `service_supervisor` scope | VERIFIED weather poller and council relay only |
| Agent personality conflict | None found. VERIFIED |
| `4 - RootRecord-Node` role | UNKNOWN |
| `7 - Client Projects` role | UNKNOWN |
| Dated 2026-09-29 PASS / LANDED sections | HISTORICAL |
| Archive and completed work orders | HISTORICAL. Left untouched |
