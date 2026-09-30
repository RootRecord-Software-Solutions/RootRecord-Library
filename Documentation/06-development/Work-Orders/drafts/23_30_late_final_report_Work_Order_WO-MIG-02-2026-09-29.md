# WORK ORDER — 23:30 late-final report

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-MIG-02-2026-09-29 |
| **Date** | 2026-09-29 (HST) |
| **Status** | OPEN — draft, not accepted for execution |
| **Owner** | RootRecord |
| **Related** | Agent 02; G1 job `late-final-report`; Pacific `Reports/scripts/report_board.py`; `Media/Voice/scripts/voice_reports.py` `late_report`; Agent 01 Night-sleep scheduler gate |

**Scope:** Re-add the G1 23:30 HST second fire of the optional late report as a gated slot on the existing report board. In scope: one Reports subfolder, a text-only runner, and a disabled `jobs.py` block. Out of scope: a new report template, a fifth board slot, playback, sends, the night-sleep gate itself, and any other agent's function.

This file is the before-documentation. It is not on the active work-order index.

---

## 1. Intent

G1 `late-final-report` is the same `late_report.run` as the 21:00 late report, fired again at 23:30 HST (misfire grace 600 seconds, job name "Final report (23:30)"). `reports/sort/late-report/scripts/job.py` skips when the board slot `late` is already `done` or `running`. The slot is optional and is never caught up. The cron is skipped while night sleep is on. G1 then generated speech and played it. Playback stays out.

The live system already keeps the 21:02 Ava roll-up (`voice_late_report`, gated `RR_VOICE_ROLLUPS`) and the board slot `late` at 21:02 (`mandatory: False`, `catch_up_allowed: False`). Catch-up never runs `late`. Nothing fires at 23:30. This work adds that second chance only: if the existing late slot is not done, run the existing template roll-up as text. Do not replace the roll-up, the board, the poller, or Kokoro.

---

## 2. Current reality

### 2.1 What exists

Folder name: **Late-Final**, a subfolder of the existing Reports domain (same pattern as `Reports/News`). No new top-level domain. No lowercase twin. No `Logs/` directory on the server.

| Item | Location / status |
| --- | --- |
| Code | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Reports/Late-Final/scripts` — not created. Build paused. |
| Database | `2 - RootRecord-Database/Reports/Late-Final/` — not created. Last-run JSON only, when built. The due ledger stays `2 - RootRecord-Database/Reports/board/daily-reports-due.json`. |
| Logs | `2 - RootRecord-Database/Logs/Reports/Late-Final/` — not created. |
| Secrets | None. No `master-key.env` key names. |
| G1 source | `Solar-Pacific-RootRecord-Server-Old` `scheduler-clock/scripts/scheduler.py` job id `late-final-report` calls `_run("late_report")` at hour 23, minute 30. Same runner as job id `late-report` at 21:00. |
| Live late roll-up | `voice_late_report` at 21:02 in `Automations/scripts/jobs.py`, gated `RR_VOICE_ROLLUPS`. Template is `voice_reports.py` `_rollup(..., "late")`. |
| Live board | `Reports/scripts/report_board.py`. Slots: morning 09:02, midday 12:02, late 21:02. Late is optional and is never caught up. |
| Night-sleep scheduler gate | No Folder on the server. Only the agent brief exists: `5 - RootRecord-Library/Migration Agents/Sent/01-night-sleep-scheduler-gate.md`. |

### 2.2 Completed so far

- [x] Old source read (scheduler job + `late-report` `job.py` skip-if-done). Live board and `voice_late_report` read. Draft written.
- [ ] Night-sleep scheduler gate Folder — absent. Build paused on this.
- [ ] `Reports/Late-Final/scripts/late_final.py`
- [ ] Gated `jobs.py` block `voice_late_final_report` at 23:30 (`RR_VOICE_LATE_FINAL=1`)
- [ ] `--dry-run` test
- [ ] Phase 4 archive and GitHub file removal
- [ ] Phase 5 Library corrections

### 2.3 Known friction

- The 23:30 cron and the 21:00 cron share one G1 script. A separate "final report" template would not match the old function.
- G1 played the report. G3 delivery is off. This slot writes text only.
- Night sleep is a real dependency. G1 skipped this cron while `night-mode.json` said `sleeping`. That gate is Agent 01's function. It has no Folder yet.

---

## 3. Tasks

1. Pause. The Night-sleep scheduler gate has no Folder. Name that function and stop. Do not build the gate. Do not add `Reports/Late-Final`. Do not edit `jobs.py`.
2. When that Folder exists and Alexander says to build: pause again if `Automations/scripts/jobs.py` is already being edited.
3. Add `Reports/Late-Final/scripts/late_final.py`. Read the existing `late` slot (`report_board.py status` or `Reports/board/daily-reports-due.json`). If status is `done` or `running`, write the last-run JSON and exit. Otherwise run `voice_reports.py late_report --no-voice`. Call the night-sleep gate from Agent 01's Folder; skip the run when it says sleeping. Do not change `_rollup`. Do not add a fifth board slot. Do not play audio.
4. Add one gated block in `jobs.py`, left disabled: id `voice_late_final_report`, `at_times` `["23:30"]`, `enabled` only when `RR_VOICE_LATE_FINAL=1` at poller start. Command: `nice -n 10 python3` on `late_final.py`. Text only. No delivery.
5. Prove it with `python3 late_final.py --dry-run`. It prints skip or would-run, writes only the Late-Final last JSON, and does not call Kokoro or the speaker.
6. After that works: phase 4, then the result note in this same file, then the Library corrections in section 7.

---

## 4. Non-goals

- Do not overwrite `voice_reports.py`, the 21:02 `voice_late_report` job, EcoFlow BLE, the weather poller, the radar archive, the hurricane board, `geology_collect.py`, or Kokoro.
- Do not edit other agents' files or their work orders.
- Do not import logs, samples, last-state files, generated reports, images, radar frames, zip archives, database dumps, caches, virtualenvs, `node_modules`, or `__pycache__` into Pacific, Database, the website, or git.
- Do not send messages, play speakers, drive OBS, switch hardware, delete live Ecosystem files, or spend cloud money.
- Do not delete a GitHub repository. Do not force-push.
- Do not restore files under `~/.ollama/skills/energy`, automations, or `coms/ssh/local-data-globe`.

---

## 5. Key file / path reference

| Path | Role |
| --- | --- |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Reports/Late-Final/scripts/late_final.py` | New runner. Not created. Build paused. |
| `2 - RootRecord-Database/Reports/Late-Final/` | Last-run JSON. Not created. |
| `2 - RootRecord-Database/Logs/Reports/Late-Final/` | Logs. Not created. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Reports/scripts/report_board.py` | Existing board. Read the `late` slot. Do not add a slot. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Media/Voice/scripts/voice_reports.py` | Existing `late_report` template. Call with `--no-voice`. Do not edit. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Automations/scripts/jobs.py` | Proposed gated block only, and only after the pause clears. |
| `2 - RootRecord-Database/Reports/board/daily-reports-due.json` | Existing due ledger. |
| G1 `scheduler-clock/scripts/scheduler.py` | Shared with every G1 cron. Leave it. |
| G1 `reports/sort/late-report/` | Shared with the 21:00 late report, already ported. Leave it. |
| G1 `reports/sort/daily-report-board/` | Shared with the board, already ported. Leave it. |

---

## 6. Open items

**Additional requirements:**

- Build stays paused until the Night-sleep scheduler gate has a Folder. Do not build that function here.
- `jobs.py` edit waits until that pause clears and the file is not already being edited.
- Playback, Telegram, OBS, hardware switching, and cloud spend need Alexander's sign-off. They are not part of this function.
- Phase 4 and phase 5 have not started.

---

## 7. Notes & constraints

- No force-push.
- Secrets stay out of git. This function has no `master-key.env` keys.
- Prefer small reversible steps.
- Sign-off gates: no speaker playback, no sends, no OBS, no hardware actuation, no cloud spend, no deletion of live Ecosystem files. The job stays gated off (`RR_VOICE_LATE_FINAL` unset or not `1`).
- Small test, when the build is allowed: `python3 "1 - Servers/1 - RootRecord-Pacific-Solar-Server/Reports/Late-Final/scripts/late_final.py" --dry-run`. Expected: JSON line `skip` or `would-run`, last-run file under `2 - RootRecord-Database/Reports/Late-Final/` only, no WAV, no playback.
- Shared old-repo files named above stay. Nothing belongs only to this job, so phase 4 archives nothing and deletes nothing on GitHub. Do not delete the repository.

### Result (phase 4–5)

Not started. The Night-sleep scheduler gate Folder is missing, so the runner was not added.

- Landed: this draft only.
- Archived: nothing.
- Removed on GitHub: nothing. Shared files left in place.
- Library pages still say the 23:30 slot was not re-added. Correct these only after the migration works: `Documentation/00-architecture/G1-Scheduler-To-G3-Jobs-Map-2026-09-29.md`, `Documentation/00-architecture/Voice-Reports-G3.md`, `Documentation/00-architecture/Old-Repo-Migration-Matrix.md` (row 15), `Documentation/07-testing/2026-09-29-old-repo-ports-breadth-batch5.md`.

---

*Work order prepared 2026-09-29 HST. Update status when closed.*

---

## Archive / location note

**Active / accepted WOs** — filename when saved:

```text
23_30_late_final_report_Work_Order_WO-MIG-02-2026-09-29.md
```

Location when accepted (not this draft):

```text
Documentation/06-development/Work-Orders/
```

**Drafts (not on active index)** — this file:

```text
Documentation/06-development/Work-Orders/drafts/
```

See `drafts/README.md` and WO-WOGEN-001. Do not auto-promote.

**Closed WOs:** set Status → COMPLETE/CLOSED → `git mv` into:

```text
Documentation/06-development/Work-Orders/Complete/
```

Human session logs archive under `Documentation/01-operations/archive/YYYY-Www/` (WO-ARCH) — separate from closed work orders.
