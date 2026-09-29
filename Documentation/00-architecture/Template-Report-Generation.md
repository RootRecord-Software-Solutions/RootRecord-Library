# Template report generation (Library templates, filled from measured data)

**Date:** 2026-09-29 HST · **Pass:** g3-template-reports · **State:** LANDED / gated (job OFF by default)

## 1. What it does

`Pacific/Reports/template_fill.py` (stdlib only) writes one report per Library operations template in
[`01-operations/templates/`](../01-operations/templates/), using the same headings, tables, field order, date formats and
status vocabulary. Everything except a few free-text fields comes from measured sources. `template_validate.py`
checks each output against its template before it is written.

| Template | Output (Database `Reports/Generated/`) | Free-text fields (specialist) |
| --- | --- | --- |
| `TEMPLATE System Operator Worklog — Session.md` | `System-Operator-Worklog-Session_current.md` | Purpose, Next useful step, closing Status |
| `TEMPLATE RootRecord Checkpoint.md` | `RootRecord-Checkpoint_current.md` | Operating principle, closing Status |
| `TEMPLATE Event Action Log.md` | `Event-Action-Log_current.md` ("AI Inference Activity Log") | Scope, closing Status |
| `TEMPLATE Work Order.md` | `Work-Order_current.md` ("Desk Sign-off Backlog", `WO-GEN-<date>`) | Intent, Scope |

Also written: `template-fill-validation_current.json` (per template: validation result, draft metadata, a 300-character reply preview).
A previous `_current.md` moves to `Reports/Generated/Archive/<name>_YYYY-MM-DDTHHMM.md` only when the content changed.
An output that fails validation goes to `<name>_rejected.md` and the `_current` copy stays as it was.

**Never writes into the Library.** `guard_out()` refuses any path under the Library root. The Library copies are for people:
someone reviews a generated file and copies it into `01-operations/` or `06-development/Work-Orders/drafts/` by hand.
The Work Order output says "generated draft, not on the active index" and must not be auto-promoted.

## 2. Sources (read-only)

| Source | Used for |
| --- | --- |
| Library `07-testing/README.md` index rows for the date | worklog timetable and completed items, work order §2.2 / §2.3 |
| Library `08-ideas/README.md` | checkpoint "Intentionally deferred" (PROPOSED rows) |
| Library `01-operations/0 - Human Operator Work Logs/<date> *.md`, the "Needs Alexander sign-off" section | blockers tables, work order tasks, next step |
| Library `06-development/Work-Orders/*.md` `\| **Status** \|` rows | work order §2.1 |
| Database `Logs/AI/Inference/inference_current.jsonl` (+ `Archive/inference_<date>.jsonl`) | event log timeline/outcomes, worklog counts |
| Database `Logs/Automations/automations_current.log` (+ hourly `Archive/automations_<date>_HH00.log`) | FAIL lines, `github_sync_all`, tunnel lines |
| Database `System/last/host-last.json`, `Energy/soc/*-last.json`, newest `Media/Images/*.jpg`, Weather county `*_current.md`, `Worklog/worklog_current.md` | checkpoint subsystem freshness |
| `systemctl --user is-active`, `/proc/*/comm`, 127.0.0.1:8799 / :11434 | checkpoint runtime and services |

**Status vocabulary mapping (checkpoint):** fresh = `ok`, stale = `degraded`, missing or too old = `down`. Thresholds:
telemetry and BLE ≤ 15 min ok / ≤ 6 h degraded; worklog and A-EYES ≤ 30 min / ≤ 6 h; weather ≤ 3 h / ≤ 12 h.
The tunnel shows `degraded` if the last tunnel line in the poller log is a timeout. Services show `active` or `inactive`.
The poller shows `active`, `inactive` or `unknown`. The worklog header shows `ACTIVE` when the date is today, otherwise `CLOSED`.
The event log uses `IN PROGRESS` or `CLOSED`. The work order uses `OPEN — …`.

## 3. Free text: specialist, facts only

For each template in `--model-templates`, the script makes **one** call:
`nice -n 10 run-infer.sh rr-exec "<prompt>"`, with `RR_CALLER=template_fill` and `DESK_LIVE_FILE` unset.
It only calls when `single-flight.sh status` is IDLE and MemAvailable ≥ 3 GB. `--draft auto` skips the call quietly otherwise.
`run-infer.sh` starts FLM (NPU) on demand and falls back to Ollama `rr-exec` with keep_alive 0.
The prompt starts: *"Use ONLY the facts below. Do not add any number, name, path, date or claim that is not in the facts…"*.
It then lists `KEY: <instruction>` lines and at most 30 fact lines. Each field is accepted only if:

- it parses as `KEY: value` (bullets, bold and `-`/`—` separators are tolerated);
- it is 300 characters or less, contains no `{{`, and is not "No data";
- **every number in it appears in the facts** (`template_validate.number_ok`);
- for the worklog's "Next useful step", it names a real sign-off item. It is then written as `Alexander sign-off: <item>`,
  never as a bare instruction such as "restart the poller".

Any other field uses fixed deterministic text, so the report is always complete. Which fields came from the model is recorded
in the validation JSON (`draft.fields`).

**Known limitation (measured 2026-09-29):** on the NPU path, `run-infer.sh` currently sends its generic voice system prompt
("You are RootRecord rr-exec…"), not the `rr-exec` Modelfile SYSTEM. The 1B model sometimes ignores the `KEY:` format.
In the samples it did so for the work order twice, and those fields fell back. Applying the gated specialist hook
([AI-Specialist-Models-and-Routing.md](./AI-Specialist-Models-and-Routing.md) §4, `RR_SPEC_SYSTEM`) should fix this.
That needs Alexander's approval, and `run-infer.sh` was not edited here.

## 4. Structure validator (`Reports/template_validate.py`)

`validate(template, output, corpus, vocab)` compares the output with the template, ignoring fenced blocks:

- **Headings:** same count, level and order. Template placeholders such as `{{AREA}}` match any text. Any mismatch → **reject**.
- **Tables:** the header cells of every table must match the template's, in order. A mismatch → **reject**.
- **Bold fields:** `**X:**` and `| **X** |` labels must appear in template order → **reject** on mismatch.
- **Leftover `{{…}}`** outside fences → **reject**.
- **Vocabulary rules** for each template (for example checkpoint Status ∈ ok/degraded/down) → **reject**.
- **Numbers:** every number in the output that is not in the source corpus is **flagged** (listed in `unsupported_numbers`), not rejected.
  HH:MM matches HH:MM:SS sources, and parts of dates and versions are checked separately.

CLI: `template_validate.py <template.md> <output.md> [--corpus file]` exits 1 on reject. Negative tests (2026-09-29):
renamed heading, renamed table column and wrong vocabulary were all rejected. Invented values (`73.4`, `417`, `9137`) were all flagged.

Limit: the check is per number, not per meaning. A draft that reuses a real number in the wrong place (for example "18 testing
records" when 18 is the poller FAIL count) passes. Offline test with a fake reply: an invented `99` was rejected, and a bare
"Restart the poller." failed the NEXT check and fell back to `Alexander sign-off: Poller restart`.

Note: the number check is strongest for model text, which is checked against the facts given to the model. Deterministic
cells are built from source values, so they are added to the corpus.

## 5. Usage

```bash
R="/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server/Reports"
python3 "$R/template_fill.py" --all --draft none --dry-run                       # validate only: no writes, no model
python3 "$R/template_fill.py" --all --draft auto                                 # what the job runs
python3 "$R/template_fill.py" --all --draft model --model-templates worklog      # one model call only
python3 "$R/template_fill.py" --template checkpoint --date 2026-09-29 --draft none
```

**Job:** `jobs.py` ON_AT `template_reports_daily` at 18:40 HST. It runs `nice -n 10 python3 …/template_fill.py --all --draft auto`
with a timeout of 900 s. It is **OFF** unless `RR_TEMPLATE_REPORTS=1` is set in the poller's environment at poller start.
Enabling it needs a poller restart, which needs Alexander's sign-off. With the default `--draft auto`, that is up to 4 light model calls a day.
Use `--model-templates worklog` to cut it to 1.

**Adding a template:** write `render_<key>()`, mirroring the template line by line. Copy static sections with
`section_verbatim()`. Then add a `TEMPLATES` row (template file, output name, vocab rules) and run `--dry-run` until the validator passes.

## 6. Resource policy

The script uses stdlib only. A run without the model takes about 0.3 s. Each model call is one on-demand FLM start/stop (NPU),
about 6–9 s including cold start, with a peak FLM RSS of about 2.0 GB. Ollama is only a fallback, with keep_alive 0.
There are no warmups and nothing stays resident.

Tests: [07-testing/2026-09-29-template-report-samples.md](../07-testing/2026-09-29-template-report-samples.md).

*Created 2026-09-29 HST (g3-template-reports).*
