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

Current operator evidence on 2026-09-28 showed `/dev/accel/accel0` present but no FastFlowLM binary under the checked home tree and no `ava-flm.service`. Therefore the NPU gate remains blocked until an authorized/documented FastFlowLM installation procedure is available and the live `:52625` endpoint is verified.

```bash
bash "System/scripts/plumbing/run-infer.sh" <operator-approved-test-arguments>
```

Inspect the single-flight state under the Pacific/Data-bound location:

```bash
find "/home/rootrecord/Database/GITHUB/plumbing/state" -maxdepth 2 -type f -print 2>/dev/null | head -50
```

### Pass criteria

- Warmup resolves through `System/scripts/plumbing/`.
- One approved inference request passes through the Pacific single-flight gate.
- No concurrent duplicate gate execution is observed.
- State is written/read under `/home/rootrecord/Database/GITHUB/plumbing/state`, not the legacy `~/.ollama/skills/plumbing/state` location.

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

test -x "Security/Cameras/ensure_cam_server.sh"
test -x "Security/Cameras/grab_all.sh"
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
tail -n 100 "/home/rootrecord/Database/Logs/Automations/automations_current.log"
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

## Explicitly out of scope for this runbook

- Website/Mainland enablement.
- User-account Library deletion.
- Weather enablement.
- Fabrication of missing Master-Prompt `08-repository-and-file-links.md`.
- Moving any work order to `Complete/` before its acceptance criteria are satisfied.
