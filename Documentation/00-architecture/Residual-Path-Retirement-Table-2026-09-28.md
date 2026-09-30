# Residual Path Retirement Table

| Field | Value |
| --- | --- |
| **Date** | 2026-09-28 (HST) |
| **Supports** | WO-SRV-2026-09-27 |
| **Rule** | Pre-filled from existing static audits. Bruce fills Verified / Retired after G3 checklist. Docs only. **Standing rule (Alexander, 2026-09-29): never retire or delete G2/legacy code; "no live references" is not grounds. Retire only with Alexander's explicit sign-off.** **2026-09-30 exception:** he allowed removal of `~/.ollama/skills` files that were byte-identical to Pacific. Unique and diverged files stayed. Dangerous leftover scripts were fail-closed, not deleted. The 27 GB `/home/rootrecord/old ollama/old skills` tree was not in that pass. Rows below that name skills `1dcee66` are the 2026-09-29 record. |

---

## Operator runbook

Use the companion [G3 Runtime Verification Runbook](./G3-Runtime-Verification-Runbook-2026-09-28.md) for exact desk commands and evidence requirements. This table remains the retirement record.

## How to use

1. Run [G3 Runtime Verification Checklist](./G3-Runtime-Verification-Checklist-2026-09-28.md)  
2. Mark **Verified** only with evidence (cycle OK + path on Pacific)  
3. Mark **Retired** only after Alexander's explicit sign-off, then legacy **executable** removed or `MIGRATED.md` placed  
4. Keep legacy `SKILL.md` files  

Pacific root (desk):  
`/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server`

---

## Residuals (from WO-SRV audit 2026-09-28)

| Surface | Legacy pattern (historical) | Pacific target | Static source OK | Verified (runtime) | Retired |
| --- | --- | --- | --- | --- | --- |
| Telegram / council_relay | `…/skills/coms/telegram/…` | `Communications/telegram/` (+ plumbing under `System/scripts/plumbing/`) | Yes (paths rewired in source) | Poll/auth PASS 2026-09-29T11:16Z (01:16 HST): PID 804326 single, no 401. Replies BLOCKED (`*-telegram` models absent) — `2 - RootRecord-Database/Logs/Migration/g3-poller-realign-evidence-20260929T111731Z.md` | KEPT (restored 2026-09-29, retire only with Alexander sign-off) — G2 `council-relay.py`, `ensure-relay.sh` back in `~/.ollama/skills` (dormant; skills `1dcee66`) |
| Security/Cameras cam / grab / timelapse | `…/.ollama/skills/a-eyes/scripts/…` | `Security/Cameras/` (hourly wrapper on Pacific) | Yes | PASS (cam server + frame grab; timelapse compile VERIFY PENDING) 2026-09-29T10:12–10:16Z (00:12–00:16 HST) — `2 - RootRecord-Database/Logs/Migration/g3-runtime-evidence-20260929T101550Z.md` | KEPT (restored 2026-09-29, retire only with Alexander sign-off) — G2 `grab_all.sh`, `cam_server.py`, `ensure_cam_server.sh` back in `~/.ollama/skills` (dormant; skills `1dcee66`) |
| Energy actions | `…/skills/energy/scripts/actions` | `Energy/scripts/actions` | Yes — source LANDED / runtime VERIFY PENDING | Partial — `solar-gate-status` PASS (read-only) 2026-09-29T10:57:45Z (00:57 HST), after the Database-root realignment: it reads `…/2 - RootRecord-Database/Energy/ports/solar-gate-state.json` (= `paths.PORTS`) and returns the correct `WAITING` / no-data answer. The actuating actions (arm/disarm, AC always-on) stay VERIFY PENDING (they change hardware; not approved) — `2 - RootRecord-Database/Logs/Migration/g3-dbroot-realign-evidence-20260929T105845Z.md` | KEPT (restored 2026-09-29, retire only with Alexander sign-off) — G2 `solar-gate-status.sh` (actuating wrappers never removed) back in `~/.ollama/skills` (dormant; skills `1dcee66`) |
| Energy BLE owner | `…/.ollama/skills/energy/scripts/ble/ble-owner.py` | `Energy/scripts/ble/ble-owner.py` | Yes — `ava-ecoflow-ble.service` + `devices.conf` repointed 2026-09-29 | PASS 2026-09-29T10:35:14Z (00:35 HST) — `2 - RootRecord-Database/Logs/Migration/g3-cutover-evidence-20260929T103720Z.md` | KEPT (restored 2026-09-29, retire only with Alexander sign-off) — G2 `ble-owner.py` back in `~/.ollama/skills` (dormant; skills `1dcee66`) |
| Plumbing warmups / single-flight | `…/skills/plumbing/…` | `System/scripts/plumbing/` | Yes — source LANDED / runtime VERIFY PENDING | Non-NPU PASS 2026-09-29T10:57:46Z (00:57 HST), after the exec-bit fix and the Database-root realignment. One inference went through the Pacific gate (rc 0) and a parallel run was refused (rc 75); the holder was written and read under `…/2 - RootRecord-Database/Github/plumbing/state` (git-ignored). NPU/FLM BLOCKED (no FLM) — `2 - RootRecord-Database/Logs/Migration/g3-dbroot-realign-evidence-20260929T105845Z.md` | KEPT (restored 2026-09-29, retire only with Alexander sign-off) — G2 `ollama-warmup.sh`, `run-ollama.sh`, `run-infer.sh` (`single-flight.sh`, `flm-warmup.sh`, `npu-status.sh` never removed) back in `~/.ollama/skills` (dormant; skills `1dcee66`) |
| System sampling | `…/.ollama/skills/system-stats/scripts/sys-sample.sh` | `System/scripts/sys-sample.sh` | Present on Pacific; `jobs.py` points here | PASS 2026-09-29T10:12–10:16Z (00:12–00:16 HST) — `2 - RootRecord-Database/Logs/Migration/g3-runtime-evidence-20260929T101550Z.md` | KEPT (restored 2026-09-29, retire only with Alexander sign-off) — G2 `sys-sample.sh` back in `~/.ollama/skills` (dormant; skills `1dcee66`) |
| Reports worklog | `…/.ollama/skills/reports/scripts/worklog_once.sh` | `Reports/scripts/worklog_once.sh` | Present on Pacific; `jobs.py` points here | PASS 2026-09-29T10:12–10:16Z (00:12–00:16 HST) — `2 - RootRecord-Database/Logs/Migration/g3-runtime-evidence-20260929T101550Z.md` | KEPT (restored 2026-09-29, retire only with Alexander sign-off) — G2 `worklog_once.sh` back in `~/.ollama/skills` (dormant; skills `1dcee66`) |
| Weather poller | `…/skills/weather/…` | `Weather/` (imported 2026-09-29, Pacific venv) | Yes — `weather_poller` enabled (Pacific `e977252`) | PASS 2026-09-29T11:50Z (01:50 HST); reports PASS 01:59 HST — `2 - RootRecord-Database/Logs/Migration/g3-weather-archive-evidence-20260929T115429Z.md` | KEPT (G2 copy; retire only with Alexander sign-off) |
| Network globe cwd | legacy `coms/ssh/…` | Pacific `Communications/network/` | Yes — collector moved to `Communications/network/local-data-globe/`; `network-globe-hawaii.service` repointed 2026-09-29 | PASS 2026-09-29T10:33:44Z (00:33 HST) — `2 - RootRecord-Database/Logs/Migration/g3-cutover-evidence-20260929T103720Z.md` | KEPT (restored 2026-09-29, retire only with Alexander sign-off) — G2 `collector.js`, `telegram-relay.js` back in `~/.ollama/skills` (dormant; skills `1dcee66`) |

### G3 runtime evidence — 2026-09-29

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

### Staged migrations — 2026-09-29

- **Network globe — STAGED (awaiting unit repoint).** G2 `~/.ollama/skills/coms/ssh/local-data-globe/collector.js` plus its required `telegram-relay.js` and `package.json` copied to Pacific `Communications/network/local-data-globe/` (no `node_modules`, no secrets; the copies contain no `.ollama/skills` paths; `node --check` OK). Proposed unit: `Communications/network/local-data-globe/network-globe-hawaii.service.proposed` (WorkingDirectory + ExecStart → Pacific). Not installed; the live `network-globe-hawaii.service` still runs the G2 collector.
- **Energy BLE owner — STAGED (awaiting unit repoint + `devices.conf`).** G2 `~/.ollama/skills/energy/scripts/ble/ble-owner.py` (stdlib only) copied to Pacific `Energy/scripts/ble/ble-owner.py`; log/pid moved to `/home/rootrecord/Database/Logs/Energy/ava-ecoflow-ble.log` and `/home/rootrecord/Database/ENERGY/state/ava-ecoflow-ble.pid` (env-overridable); `py_compile` OK. Proposed unit: `Energy/scripts/ble/ava-ecoflow-ble.service.proposed`, which also lists the `devices.conf` `ble_log` (line 24) and `owner_script` (line 98) changes. Not installed; the live `ava-ecoflow-ble.service` still runs the G2 owner.
- **Telegram relay — code fix landed.** Pacific `Communications/telegram/scripts/ensure-relay.sh` now checks the relay is alive 3 s after launch and prints `[FAIL] … last log: …` (token-redacted) with exit 1 instead of a false `[ok]`. `bash -n` OK. Takes effect the next time the poller runs `council_relay`; nothing was restarted. The relay itself still needs `TELEGRAM_AVA_TOKEN` provisioned.
- **Update 2026-09-29 ~00:35 HST:** both staged units were installed after operator approval and PASSed; see `2 - RootRecord-Database/Logs/Migration/g3-cutover-evidence-20260929T103720Z.md`.
- **Update 2026-09-29 ~00:52 HST:** Energy `solar-gate-status` runs read-only but reads the old Database root → VERIFY PENDING. Plumbing gate works after an exec-bit fix, but its state is on the old root → FAIL (state path). The two G2 retirements made for these rows at 00:46 HST were reverted (files restored from backup). B1 (River 2 Pro) = 0% is a cloud-API/device reading, not a migration fault. G2 `cam_server.py` and `ensure_cam_server.sh` retired (cam-server PASS; `2 - RootRecord-Database/Logs/Migration/g2-retire-aeyes-cam-evidence-20260929T105103Z.md`). See `2 - RootRecord-Database/Logs/Migration/g3-energy-plumbing-evidence-20260929T104618Z.md`.
- **Update 2026-09-29 ~01:00 HST:** the Energy and Plumbing paths were realigned to the canonical Database root (Pacific `87a6469`), and volatile state is now git-ignored in the Database repo. Re-run: Plumbing non-NPU PASS, `solar-gate-status` PASS (read-only). Retired G2 `solar-gate-status.sh` and `ollama-warmup.sh`. See `2 - RootRecord-Database/Logs/Migration/g3-dbroot-realign-evidence-20260929T105845Z.md`.

---

## Source LANDED / runtime VERIFY PENDING (no residual action required for path)

Energy reads + leapfrog · System · Reports foundation · Github sync · Cloudflare tunnel · Network globe command  

Record any post-check confirmation in WO-SRV notes if useful; do not re-open closed path work.

---

## Retirement note

- Prefer `MIGRATED.md` on old packet: status, date, canonical Pacific path, “do not run”  
- Do not bulk-delete G1/G2 trees  
- Do not remove legacy `SKILL.md` solely because runtime moved  

*Pre-filled for Bruce. Empty columns are intentional. 2026-09-28 HST.*

## Current status refresh — 2026-09-29 ~01:11 HST

- Historical evidence blocks above are retained as historical captures and are not rewritten to match later runtime state.
- Current Pacific state: Network Globe and Energy BLE owner are PASS and their G2 executables are retired; Security camera server/frame grab, System sampling, Reports worklog, Plumbing non-NPU, and read-only `solar-gate-status` have also passed the documented checks.
- Telegram tokens have been provisioned; relay/model runtime verification is still pending.
- Energy actuating actions and Security timelapse remain VERIFY PENDING; NPU/FastFlowLM remains BLOCKED.
- Pacific poller source has now been corrected to the canonical Database root. Its post-restart runtime verification remains open before the poller gate can be closed.

## Current status refresh — 2026-09-29 ~03:45 HST

- **All G2 entries in this table are KEPT** (retire only with Alexander sign-off). Nothing is RETIRED. The ~01:11 HST bullet above ("their G2 executables are retired") and the ~00:52/~01:00 HST "retired" notes are superseded: every G2 file was restored (skills `1dcee66`) and stays dormant.
- The 27 dormant G2 files that still name old-root paths are **KEPT** unchanged.
- Runtime states since the ~01:37 refresh: Plumbing NPU/FLM **PASS** (install/validate), on-demand `llama3.2:1b` route **PASS** (own-session fix VERIFY PENDING); Weather **PASS**; post-reboot **PASS**; Database Title-case rename **PASS** (Database `92bd69c`). Paths in the table rows above already use the Title-case forms where they describe the current state (`Energy/ports`, `Github/plumbing/state`); historical capture blocks keep the names observed at the time.
- Still VERIFY PENDING: Security timelapse (after 05:00 HST), Energy arm/disarm + AC (need approval).
- Per-test records: [`Documentation/07-testing/`](../07-testing/README.md).

## Old-repo migration pass — 2026-09-29 ~13:40 HST (copy/port only; nothing retired)

| Surface | Legacy source (KEPT, unchanged) | Pacific target (new copy) | Static source OK | Verified (runtime) | Retired |
| --- | --- | --- | --- | --- | --- |
| USGS earthquakes (hourly + M2 poll) | G1 `earthquakes/`, `earthquake-hourly`, `earthquake-m2-poll`; G2 skill copies | `Geology/scripts/geology_collect.py` | yes | manual PASS; poller VERIFY PENDING (`RR_GEOLOGY`) | **KEPT** |
| HVO Kīlauea / Mauna Loa status | G1 `kilauea/*` (HANS pulls) | `Geology/scripts/geology_collect.py` | yes | manual PASS; poller VERIFY PENDING | **KEPT** |
| Kīlauea cams | G1 `kilauea-cams` | `Geology/scripts/kilauea_cams.py` | yes | manual PASS; poller VERIFY PENDING (`RR_KILAUEA_CAMS`) | **KEPT** |
| Quake backfill | G0 `old` `backfillquakes.py` | `Geology/scripts/earthquakes_backfill.py` | yes | manual PASS (on demand) | **KEPT** |
| Earthquake voice report | G1 `earthquake-hourly` spoken script | `Media/Voice/scripts/voice_reports.py earthquake_report` | yes | text PASS; WAV VERIFY PENDING (`RR_VOICE_QUAKE`) | **KEPT** |
| Sun times | G1 `hourly-solar-weather` `sun_times` | `Energy/scripts/sun_times.py` | yes | manual PASS (`RR_SUN_TIMES`) | **KEPT** |
| Uptime log | G1 `uptime-log` | `System/scripts/uptime_log.py` | yes | manual PASS (`RR_UPTIME_LOG`) | **KEPT** |
| MP4 converter | G1 `mp4-converter` | `Media/Video/scripts/mp4_converter.py` | yes | manual PASS (on demand) | **KEPT** |
| Hurricane desk voice | G1 `weather/hurricane-desk` | `Media/Voice/scripts/voice_reports.py hurricane_desk` | yes | text PASS; WAV VERIFY PENDING (`RR_VOICE_HURRICANE`) | **KEPT** |
| Kīlauea hourly desk voice | G1 `hourly-clip-reports` Kīlauea desk, `persona._kilauea_line` | `Media/Voice/scripts/voice_reports.py kilauea_report` | yes | text PASS; WAV VERIFY PENDING (`RR_VOICE_KILAUEA`) | **KEPT** |
| Web facts | G1 `websites/web-facts` | `Communications/web-facts/scripts/web_facts.py` | yes | manual PASS (on demand) | **KEPT** |
| Live weather chat lines | G1 `weather/live-wx` | `Communications/live-wx/scripts/live_wx.py` | yes | manual PASS (on demand) | **KEPT** |
| Hawaiʻi news collector | G0 `old/operations/news/{_collector.py,hawaii/news.py}` | `Reports/News/scripts/{_collector,hawaii_news}.py` | yes | rc 0, 0 posts at 14:05 → PASS 278 posts with 16 seed feeds at 14:25; job PROPOSED (`RR_HAWAII_NEWS`) | **KEPT** |
| Host net counters + security snapshot | G1 `host-metrics` | `System/scripts/host_desks.py` | yes | manual PASS (temp root); job PROPOSED (`RR_NET_SAMPLES`) | **KEPT** |
| Solar / security / bandwidth desk voice | G1 `hourly-clip-reports` desks | `Media/Voice/scripts/voice_reports.py solar_desk \| security_desk \| bandwidth_desk` | yes | text PASS; WAV VERIFY PENDING; jobs PROPOSED | **KEPT** |
| Official statement (HLS) | G1 `weather/official-weather-media` | `Weather/scripts/official_statement.py` + `Media/Voice/scripts/voice_reports.py official_weather` | yes | manual PASS; text PASS, WAV VERIFY PENDING; jobs PROPOSED (`RR_OFFICIAL_HLS`, `RR_VOICE_OFFICIAL`) | **KEPT** |
| Boot brief | G1 `boot` (boot-prelims) | `voice_reports.py boot_brief` | yes | text PASS, WAV VERIFY PENDING; job PROPOSED (`RR_VOICE_BOOT`). Morning replay: `Media/MorningBootReplay` dry-run, speakers off | **KEPT** |
| Daily report board / catch-up | G1 `reports/sort/daily-report-board`, `daily-reports-catchup` | `Reports/scripts/report_board.py` | yes | manual PASS (temp root); job PROPOSED (`RR_REPORT_BOARD`) | **KEPT** |
| Load categories | G1 `load-categories` | `Energy/scripts/load_categories.py` | yes | manual PASS (on demand) | **KEPT** |
| Global hurricane board | G1 `weather/hurricane-tracker` | `Weather/hurricanes/scripts/global_board.py` | yes | manual PASS (temp root); job PROPOSED (`RR_HURRICANE_GLOBAL`) | **KEPT** |
| Host hardware | G1 `host-metrics` (temp / drives / GPU / NPU) | `System/scripts/host_hw.py` | yes | manual PASS (on demand) | **KEPT** |
| Speech scrub | G1 `persona/scripts/speech_scrub.py` | `Media/Voice/scripts/speech_scrub.py` | yes | manual PASS (on demand; not wired) | **KEPT** |

All legacy sources stay in place; the **Retired** column changes only with Alexander's explicit sign-off. Full matrix: [Old-Repo-Migration-Matrix](./Old-Repo-Migration-Matrix.md).

## Status at pause — 2026-09-29 16:25 HST

- Nothing was RETIRED today. Every G2 / G1 / G0 source in this table stays **KEPT**.
- AWS (outside this table): `github-poller` and `rr-rootserver-poller` were **disabled, not retired**; their files and units are kept, and the re-enable steps are in the [Phase 2 reclaim record](../07-testing/2026-09-29-aws-fallback-phase2-reclaim-retention.md).
