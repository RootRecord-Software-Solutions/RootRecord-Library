# G3 Runtime Verification Runbook — 2026-09-28

## Purpose

Operator-facing verification procedure for the G2 residual → G3 Pacific cutover under **WO-SRV-2026-09-27**.

This runbook is for live desk/runtime verification only. A successful static source audit is not runtime verification. Do not record **LIVE** or **VERIFIED** unless the corresponding commands below have actually been run on the operator desk.

Related records:

- [G3-Runtime-Verification-Checklist-2026-09-28.md](./G3-Runtime-Verification-Checklist-2026-09-28.md)
- [Residual-Path-Retirement-Table-2026-09-28.md](./Residual-Path-Retirement-Table-2026-09-28.md)
- [WO-SRV-2026-09-27](../06-development/Work-Orders/Servers_Cutover_Work_Order_WO-SRV-2026-09-27.md)

## Operator evidence rules

- Run commands from the Pacific desk/runtime environment.
- Use the canonical Pacific root exactly:
  `/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server`
- Paths containing spaces must be double-quoted.
- Do not expose Telegram tokens, device credentials, API keys, or other secrets in pasted evidence.
- Redact message text if it contains private content; retain enough command/output context to prove the path and result.
- Do not delete legacy runtime files during verification. Retirement happens only after the family passes and the old → new mapping is recorded.
- Legacy `SKILL.md` files are documentation artifacts and are retained.

---

## 1. Telegram / council_relay

### Preconditions

- Pacific repository is present at the canonical root.
- `Communications/telegram/scripts/ensure-relay.sh`, `council-relay.py`, and `Communications/telegram/config/relay.conf` are present.
- Operator can inspect the live relay process/service and recent Telegram relay logs.
- No physical or message-side actuation beyond one controlled smoke message is required.

### Commands

From the Pacific root:

```bash
PACIFIC="/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server"
cd "$PACIFIC"

test -x "Communications/telegram/scripts/ensure-relay.sh"
test -f "Communications/telegram/scripts/council-relay.py"
test -f "Communications/telegram/config/relay.conf"

pgrep -af 'council-relay.py|telegram.*relay' || true
ps -ef | grep -E '[c]ouncil-relay.py|[t]elegram.*relay' || true

bash "Communications/telegram/scripts/ensure-relay.sh"

pgrep -af 'council-relay.py|telegram.*relay' || true

# ensure-relay.sh's pgrep also matches the legacy council-relay.py, so confirm the live relay runs from Pacific:
for RELAY_PID in $(pgrep -f '^python3 .+/council-relay\.py'); do
  readlink "/proc/$RELAY_PID/cwd"
  tr '\0' ' ' < "/proc/$RELAY_PID/cmdline"; echo
done
```

Then, using the normal operator Telegram test route, send **one controlled smoke message** through the council relay and inspect the corresponding relay log/output. Do not paste message content if it is sensitive.

If the relay uses Telegram `getUpdates`, verify that exactly one live relay process is polling the bot token. Use the operator's existing service/process inspection command if the deployment wraps the relay in systemd or another supervisor.

### Pass criteria

- Exactly one active council relay owns Telegram `getUpdates` for the bot.
- `ensure-relay.sh` resolves and launches/validates the Pacific relay path.
- The running `council-relay.py` cmdline/cwd resolve to Pacific `Communications/telegram/scripts/`, not `/home/rootrecord/.ollama/skills/` (`ensure-relay.sh`'s pgrep alone would also accept the legacy relay).
- One controlled smoke message traverses the expected Pacific relay path.
- No second relay process or competing `getUpdates` owner appears.
- No new repeated relay/HTTP conflict error is produced by the smoke test.

### Fail criteria

- More than one relay process owns or attempts to own `getUpdates`.
- The live process resolves to the legacy `/home/rootrecord/.ollama/skills/.../coms/telegram` runtime.
- Smoke message does not traverse the Pacific relay.
- Repeated Telegram conflict/failure appears during the test.

### Record in Residual-Path-Retirement-Table

Record: family, timestamp HST, Pacific executable/config paths, process-count evidence, smoke-test result, relevant redacted log excerpt, pass/fail, and whether the legacy Telegram executable is now eligible for retirement.

---

## 2. Plumbing / single-flight

### Preconditions

- Pacific `System/scripts/plumbing/` contains the migrated warmup and inference helpers.
- Operator can run the normal Ollama/FLM warmup path without changing model configuration.
- The check must not trigger physical actuation.

### Commands

From the Pacific root:

```bash
PACIFIC="/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server"
cd "$PACIFIC"

test -x "System/scripts/plumbing/single-flight.sh"
test -x "System/scripts/plumbing/run-infer.sh"
test -x "System/scripts/plumbing/run-ollama.sh"
test -x "System/scripts/plumbing/ollama-warmup.sh"
test -x "System/scripts/plumbing/flm-warmup.sh"

bash "System/scripts/plumbing/ollama-warmup.sh"

bash "System/scripts/plumbing/single-flight.sh" --help 2>&1 | head -40 || true
```

For the actual inference gate, use the operator's normal single inference test with the Pacific `run-infer.sh` path. If the local script contract requires arguments not shown above, use its documented invocation rather than inventing arguments.

### NPU / FastFlowLM gate

The documented NPU path is **FastFlowLM (FLM)** on `127.0.0.1:52625`. Do not mark NPU inference verified merely because `/dev/accel/accel0` exists. A live FLM runtime must be installed and reachable.

Use these read-only checks before any inference claim:

```bash
find "$HOME" -type f -name flm -perm -111 2>/dev/null | head -20
ls -la "$HOME/.local/opt/fastflowlm" 2>&1 || true
systemctl status ava-flm.service --no-pager -l 2>&1 || true
curl -sf -m 2 "http://127.0.0.1:52625/v1/models" || true
```

If the documented FastFlowLM binary/runtime or service is absent, record **NPU runtime unavailable** and stop the NPU verification gate. Do not invent an installer, restore an undocumented service, or substitute stock Ollama as proof of NPU execution. CPU/Ollama fallback may be verified separately, but it does not satisfy an NPU verification claim.

Operator installation evidence on 2026-09-29 shows the AMD NPU prerequisite stack has now been installed: `amdxdna-dkms 7.0.0-rc1+git20260310.6b13cb8f4-resolute1`, `libxrt-npu2 1:2.25.0-4~resolute1`, and `libxrt2`. `/dev/accel/accel0` is present and `modinfo amdxdna` resolves the installed driver and supported NPU firmware entries. The DKMS install emitted a BUILD_EXCLUSIVE warning and did not build the module for the current kernel/config, so this is **prerequisite stack installed, NPU runtime not yet verified**. No `flm` binary or FastFlowLM service has been established by this evidence. A reboot is required before the next validation/install stage. Do not mark the NPU gate PASS until FastFlowLM is installed and `flm validate`, XRT/NPU visibility, and the approved inference gate have actually passed.

> **Current (2026-09-29 ~03:45 HST):** FastFlowLM 1.0.6 is installed at `/usr/bin/flm` (no `ava-flm.service`, no `~/.local/opt/fastflowlm`). FLM runs **on demand** only: an idle desk has no FLM process and :52625 is closed — do not record that as "NPU runtime unavailable". Check with `command -v flm && flm validate`, then one `FLM_MODEL=llama3.2:1b bash System/scripts/plumbing/run-infer.sh ava "Reply with exactly one word: ready"` and confirm afterwards: 0 flm processes, :52625 closed, lock IDLE, `ollama ps` empty. Evidence: `2 - RootRecord-Database/Logs/Migration/g3-npu-flm-evidence-20260929T125429Z.md`; test records in `Documentation/07-testing/`.

```bash
bash "System/scripts/plumbing/run-infer.sh" <operator-approved-test-arguments>
```

Inspect the single-flight state under the canonical Pacific Database location:

```bash
find "/home/rootrecord/RootRecord-Ecosystem/2 - RootRecord-Database/Github/plumbing/state" -maxdepth 2 -type f -print 2>/dev/null | head -50
```

### Pass criteria

- Warmup resolves through `System/scripts/plumbing/`.
- One approved inference request passes through the Pacific single-flight gate.
- No concurrent duplicate gate execution is observed.
- State is written/read under `/home/rootrecord/RootRecord-Ecosystem/2 - RootRecord-Database/Github/plumbing/state`, not the legacy `~/.ollama/skills/plumbing/state` location.

### Fail criteria

- Warmup or inference resolves to the legacy plumbing path.
- Single-flight allows two simultaneous requests or deadlocks unexpectedly.
- State still depends on the legacy runtime state directory.
- The command cannot reach the Pacific helper.

### Record in Residual-Path-Retirement-Table

Record: warmup command/result, inference-gate command/result, observed state path, timestamp HST, redacted output excerpt, pass/fail, and legacy `plumbing/scripts` retirement eligibility.

---

## 3. Security/Cameras

### Preconditions

- Pacific `Security/Cameras/` runtime files are present.
- Camera credentials remain outside Git and are available to the runtime.
- Operator can inspect the camera service and Database path.
- The verification must not publish or delete stored frames.

### Commands

From the Pacific root:

```bash
PACIFIC="/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server"
cd "$PACIFIC"

test -f "Security/Cameras/ensure_cam_server.sh"
test -f "Security/Cameras/grab_all.sh"
test -f "Security/Cameras/grab_frame.py"
test -f "Security/Cameras/cam_server.py"

bash "Security/Cameras/ensure_cam_server.sh"

ps -ef | grep -E '[c]am_server.py' || true

# ensure_cam_server.sh only checks that :8791 is listening, so a legacy cam server would also satisfy it.
# Confirm the :8791 listener runs from the Pacific path, not /home/rootrecord/.ollama/skills:
ss -ltnp 'sport = :8791'
CAM_PID="$(ss -ltnpH 'sport = :8791' | grep -oE 'pid=[0-9]+' | head -1 | cut -d= -f2)"
readlink "/proc/$CAM_PID/cwd"
tr '\0' ' ' < "/proc/$CAM_PID/cmdline"; echo

find "/home/rootrecord/RootRecord-Ecosystem/2 - RootRecord-Database/Media/Images" -maxdepth 2 -type f -print 2>/dev/null | head -20
```

Run one normal frame-grab test using the operator's documented camera invocation. If the deployment exposes a wrapper/argument contract, use that exact contract; do not invent camera credentials or arguments.

### Pass criteria

- Camera server resolves to the Pacific `Security/Cameras/cam_server.py`.
- The process listening on `:8791` has its cwd/cmdline under Pacific `Security/Cameras/`, not `/home/rootrecord/.ollama/skills/`.
- The camera service is reachable/healthy according to the existing operator check.
- One frame path is created or observed under `/home/rootrecord/RootRecord-Ecosystem/2 - RootRecord-Database/Media/Images/`.
- No frame data is written into the Pacific Git tree.

### Fail criteria

- Camera server resolves to the legacy `/home/rootrecord/.ollama/skills/a-eyes/scripts/` runtime.
- The `:8791` listener's cwd or cmdline resolves under `/home/rootrecord/.ollama/skills/` (a legacy cam server satisfies `ensure_cam_server.sh`'s port-only check).
- Frame capture fails.
- Frame data is written into the Pacific repository instead of Database.
- Credentials are required from Git-tracked files.

### Record in Residual-Path-Retirement-Table

Record: camera-server process/path evidence, frame-path evidence only (not sensitive image content), timestamp HST, pass/fail, redacted log excerpt, and Security/Cameras legacy executable retirement eligibility.

---

## 4. Energy actions

### Preconditions

- Pacific `Energy/scripts/actions/` exists.
- Device credentials/configuration are available through the existing non-Git configuration mechanism.
- The operator has confirmed that the selected test is non-destructive.

### Commands

Start with a path-only reachability check:

```bash
PACIFIC="/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server"
cd "$PACIFIC"

test -d "Energy/scripts/actions"
test -x "Energy/scripts/actions/solar-gate-status.sh"
test -x "Energy/scripts/actions/river2pro-read.sh"
```

Preferred non-destructive verification:

```bash
bash "Energy/scripts/actions/solar-gate-status.sh"
```

If the operator's live configuration does not permit that status check, stop at the path-only reachability check and record that limitation. Do **not** substitute a hardware-changing command.

### Pass criteria

- Pacific Energy action path is reachable.
- The selected status/read operation completes without a destructive state change.
- Output resolves to Pacific scripts/configuration and the expected Database/state locations.
- No hardware state is changed solely for verification.

### Fail criteria

- Action path resolves to the legacy `/home/rootrecord/.ollama/skills/energy` tree.
- Status/read check fails because the migrated path is incomplete.
- Verification requires an unapproved physical state change.
- Credentials or secrets would have to be exposed in evidence.

### Record in Residual-Path-Retirement-Table

Record: exact safe action/read command, result, Pacific script path, timestamp HST, redacted output excerpt, pass/fail, and the specific legacy Energy action set eligible for retirement.

---

## 5. Pacific poller

### Preconditions

- Operator desk has access to the live Pacific runtime.
- The current scheduler/poller configuration is the Pacific `Automations/scripts/jobs.py`.
- `automations_current.log` is available through the established runtime log location.

### Commands

From the Pacific root:

```bash
PACIFIC="/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server"
cd "$PACIFIC"

test -f "Automations/scripts/jobs.py"

python3 -m py_compile "Automations/scripts/jobs.py"

grep -nE '/home/rootrecord/\.ollama/skills|RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server'   "Automations/scripts/jobs.py" || true
```

Use the normal operator command/service check to confirm the live poller is executing the Pacific `jobs.py`.

Then inspect a short fixed observation window of the current log:

```bash
tail -n 100 "/home/rootrecord/RootRecord-Ecosystem/2 - RootRecord-Database/Logs/Automations/automations_current.log"
```

Record a fresh short-window tail after the poller has had an opportunity to execute its scheduled work. Use the established log location if the deployment exposes `automations_current.log` through a different documented path.

### Pass criteria

- `jobs.py` compiles.
- The live poller resolves to the Pacific `Automations/scripts/jobs.py`.
- Active Energy, Telegram, Security/Cameras, Network Globe, Ollama/FLM plumbing paths resolve to Pacific paths.
- No repeated FAIL storm appears in the short observation window.
- Disabled Weather remains disabled.

### Fail criteria

- Live poller still executes the legacy `automations/scripts/jobs.py`.
- An active migrated function resolves to a legacy executable path.
- Repeated FAIL entries form a new storm during the observation window.
- Verification requires enabling Weather or another out-of-scope domain.

### Record in Residual-Path-Retirement-Table

Record: poller process/service evidence, `jobs.py` path, observation-window start/end in HST, redacted FAIL/error excerpt if any, pass/fail, and the affected legacy function(s) eligible for retirement.

---

## Operator evidence paste template

Use one block per family after actual verification:

```
Family:
Timestamp (HST):
Result: PASS | FAIL

Commands run:
-

Evidence:
- Process/path:
- Key output:
- Log excerpt (redacted, no secrets):
- Observation window (if applicable):

Legacy path still present:
Pacific path verified:

Next retirement step:
- If PASS: retire only the completed legacy executable/function and record old → new path.
- If FAIL: leave legacy runtime in place; record blocker and rerun after correction.
```

## Retirement gate

A migrated family is eligible for legacy executable retirement only when:

1. The corresponding Pacific runtime was actually exercised on the live desk.
2. The family-specific pass criteria above were satisfied.
3. Evidence was recorded with timestamp HST and redacted output/log evidence.
4. The exact old → new path mapping was recorded in `Residual-Path-Retirement-Table-2026-09-28.md`.
5. The legacy `SKILL.md` remains retained for documentation.
6. No other active job still depends on the legacy executable.

After those gates pass, retire that completed legacy executable/function immediately and update the table. Do not batch unrelated retirements.

## Canonical Database boundary — verified 2026-09-29

- Active Pacific source code uses `/home/rootrecord/RootRecord-Ecosystem/2 - RootRecord-Database` as the Database authority.
- Older `/home/rootrecord/Database/` references found in historical evidence, backups, or operator tooling are not evidence that the legacy root remains the active source boundary.
- Do not rewrite historical evidence paths merely to make old evidence look current.

## NPU installation evidence — 2026-09-29

- Host is Ubuntu **26.04 / resolute** with kernel `7.0.0-34-generic`.
- AMD XDNA2/XRT prerequisite packages are installed: `amdxdna-dkms`, `libxrt-npu2`, and `libxrt2`.
- `/dev/accel/accel0` is present and `modinfo amdxdna` resolves the driver and firmware entries.
- DKMS reported a `BUILD_EXCLUSIVE` mismatch for the current kernel/config; treat the driver as **not yet runtime-verified** until after reboot and live validation.
- FastFlowLM itself is not yet established by this evidence.
- 2026-09-29 02:07 HST desk check: `xrt-smi` is **not installed** (XRT tools package missing) and no `flm` binary; `amdxdna` is loaded. Post-reboot list: WO-SRV "Pre-reboot checkpoint 2026-09-29".
- Next gate: reboot, validate XRT/NPU visibility, install the current FastFlowLM runtime for Ubuntu 26.04 if absent, run `flm validate`, then perform the approved non-destructive inference test.

## Explicitly out of scope for this runbook

- Website/Mainland enablement.
- User-account Library deletion.
- Weather enablement.
- Fabrication of missing Master-Prompt `08-repository-and-file-links.md`.
- Moving any work order to `Complete/` before its acceptance criteria are satisfied.


## Documentation refresh — 2026-09-29

- Active Pacific Database references in this runbook now use `/home/rootrecord/RootRecord-Ecosystem/2 - RootRecord-Database`.
- Historical evidence paths under `/home/rootrecord/Database/` are retained when they describe what was actually observed at the time; they are not rewritten into false current evidence.
- The human `/home/rootrecord/RootRecord-Ecosystem/Pull.sh` workflow is explicitly operator-controlled and may coexist with automated `github_sync_all`; it is not a runtime conflict.
- **Current refresh — 2026-09-29 ~01:11 HST:** Telegram tokens are provisioned; live relay/model verification remains pending. Pacific poller source now defaults to the canonical Database root; verify the live post-restart log/energy line before closing the poller gate.

## Current-state requirements — 2026-09-29 ~03:45 HST

Apply these before running any section above. Test records (one per run, with resource impact and cleanup): [`Documentation/07-testing/`](../07-testing/README.md). Test-safety policy: light tests only, one test per change, no resident models, clean up every test process.

- **Database root:** `/home/rootrecord/RootRecord-Ecosystem/2 - RootRecord-Database` with Title-case top-level folders `Energy/`, `System/`, `Weather/`, `Github/`, `RootRecord/`, `Worklog/`, `Intake/` (plus `AI/`, `Archive/`, `Logs/`, `Geology/`, `Media/`, `Users/`). Upper-case `ENERGY/`, `SYSTEM/`, `WEATHER/`, `GITHUB/`, `ROOTRECORD/`, `WORKLOG/` and lower-case `intake/` under the new root are historical names (Database `92bd69c`). The old root `/home/rootrecord/Database/` is **not** a data path any more: it holds only `GITHUB/` (backups, flags, worktrees) and `README.md`; the old data is archived in `2 - RootRecord-Database/Archive/Previous-Datasets/G2-old-root-20260929/`.
- **NPU inference:** `llama3.2:1b` **on demand**. `System/scripts/plumbing/run-infer.sh` starts `flm serve` (via `setsid nice -n 10`, `--pmode balanced`, `--ctx-len ${FLM_CTX_LEN:-4096}`, port 52625) only for a request and stops it on exit; `FLM_ON_DEMAND=0` disables this. An idle desk therefore shows **no** FLM process and a closed :52625 — that is expected, not a failure. `llama3.2:3b` is installed but not the default.
- **No resident models:** the FLM warmup is non-resident unless `FLM_WARMUP_RESIDENT=1` (Pacific `ff298b2`, after the 03:10–03:13 HST OOM loop). Ollama CLI calls use `--keepalive ${OLLAMA_KEEP_ALIVE:-0}` (`3039c3f`). `OLLAMA_KEEP_ALIVE=0` in `ollama.service` is still open (needs sudo).
- **Relay quiet mode is the default:** `ensure-relay.sh` exports `RR_RELAY_REPLIES=${RR_RELAY_REPLIES:-0}` (Pacific `ebc32a7`). Caveat: in quiet mode incoming Telegram messages are consumed (marked read) and **will not be answered later**. Replies also stay BLOCKED until the `*-telegram` models exist and Alexander opts in (`RR_RELAY_REPLIES=1`).
- **Required venvs (git-ignored):** `Pacific/Energy/.venv` (without it `ecdsa`/eflib are missing and readings fall back to frozen cloud values) and `Pacific/Weather/.venv` (from `Weather/requirements.txt`).
- Weather and relay start only at poller boot (ON_BOOT); a mid-session crash is not re-ensured until the next poller start.

## Geology verification — 2026-09-29 ~13:40 HST

Run at `nice -n 10`; each call is ≤ 10 s per HTTP request, no delivery, no model.

```bash
PAC="/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server"
DB="/home/rootrecord/RootRecord-Ecosystem/2 - RootRecord-Database"
nice -n 10 python3 "$PAC/Geology/scripts/geology_collect.py" --dry-run      # fetch + summarise, write nothing
nice -n 10 python3 "$PAC/Geology/scripts/geology_collect.py" all            # one real pull
python3 -m json.tool "$DB/Geology/collector-last.json"                       # every source ok:true, ms < 10000
python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));print(d.get("alert_level"),d.get("color_code"),d.get("erupting"))' "$DB/Geology/Volcanoes/kilauea-last.json"
RR_VOICE_REPORT_OUT=/tmp/eq-test RR_VOICE_QUAKE_DRY=1 nice -n 10 python3 "$PAC/Media/Voice/scripts/voice_reports.py" earthquake_report --no-voice
```

After the next poller start with `RR_GEOLOGY=1`: `collector-last.json` `at` advances every ~5 min; the Daily JSONL files gain no duplicate ids. Evidence: `2 - RootRecord-Database/Logs/Migration/migration-geology-evidence-20260929T2319Z.md`; record [geology](../07-testing/2026-09-29-geology-earthquakes-hvo-collector.md).
