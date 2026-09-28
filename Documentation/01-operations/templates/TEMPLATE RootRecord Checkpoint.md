# RootRecord Checkpoint — {{YYYY-MM-DD}} {{HH:MM}} HST

## Checkpoint Purpose

Snapshot of Pacific RootRecord state at **{{HH:MM}} HST** on **{{YYYY-MM-DD}}**.

This checkpoint records what was verified and what remains intentionally deferred. It does not retroactively rewrite earlier logs.

---

## Current State

### Runtime

- Poller: {{active | inactive | unknown}} — `rr-rootserver-poller.service`
- HTTP listener: {{127.0.0.1:8799 or N/A}}
- Poller log: `/home/rootrecord/.ollama/skills/logs/store/rootserver-poller.log`
- Pretty poller: {{manual | auto | not running}}

### Core subsystems

| Subsystem | Status | Notes |
| --- | --- | --- |
| System / telemetry | {{ok | degraded | down}} | {{path or sample note}} |
| Worklog scan | {{ok | degraded | down}} | |
| Ollama | {{ok | degraded | down}} | |
| EcoFlow BLE | {{ok | degraded | down}} | |
| A-EYES | {{ok | degraded | down}} | |
| Weather | {{ok | degraded | down}} | |
| GitHub sync | {{ok | degraded | down}} | |
| Cloudflare tunnel | {{ok | degraded | down}} | |

### Services (user systemd)

| Unit | State |
| --- | --- |
| `rr-rootserver-poller.service` | {{active | inactive}} |
| `ava-ecoflow-ble.service` | {{active | inactive}} |
| {{other}} | {{active | inactive}} |

---

## Verified this checkpoint

- {{Fact}}
- {{Fact}}

---

## Intentionally deferred

- {{Item}}
- {{Item}}

---

## Blockers

| Blocker | Owner | Next step |
| --- | --- | --- |
| {{Item}} | {{who}} | {{action}} |

---

## Operating principle at checkpoint

{{One short principle — e.g. do not rebuild working architecture for missing local config only.}}

---

## Checkpoint time

**{{YYYY-MM-DD}} {{HH:MM}} HST**

**Status:** {{One-line status}}

---

## Archive note

Filename when saved:

```text
{{YYYY-MM-DD}} RootRecord Checkpoint — {{HH_MM}} HST.md
```

Weekly archive: move checkpoints older than the current week into `Documentation/01-operations/archive/` without rewriting content.
