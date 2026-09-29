# WO-ECO-001 — Action Plan (Phase 1: EcoFlow Live Read)

| Field | Value |
|-------|--------|
| **Parent WO** | [WO-ECO-001](WO-ECO-001-Energy-Domain-Import.md) |
| **Phase** | 1 of N — live BLE/API read only |
| **Status** | **Desk fill done** — org push + pull + lib/db/config copy complete; stack reload + soak pending |
| **Target repo** | `RootRecord-Software-Solutions/RootRecord-Pacific-Solar-Server` |
| **Data authority** | Keep writing to existing Database paths; do not invent a second store |
| **Date drafted** | 2026-09-28 |
| **Updated** | 2026-09-28 ~16:15 HST |

---

## 0. Objective (Phase 1)

Move the **already-live** EcoFlow read chain out of the G2 skill tree and into Pacific `Energy/`, then rewire only the Energy-related entries in `Automations/scripts/jobs.py`.

After Phase 1:

- `ecoflow_read_cycle` and `ecoflow_read_boot` run from `Energy/scripts/read/`
- No `~/.ollama/skills/energy/...` paths remain for those jobs (except intentional `ENERGY_EFLIB_PATH` vendor until soak)
- Hybrid reports, actions/, Core-Ops writers stay **untouched**

---

## 1. Why this first

| Signal | Evidence |
|--------|----------|
| Live telemetry | Poller window: `river2pro`, `delta2`, `ENERGY status=live` |
| Empty domain (pre-import) | Pacific `Energy/` was README + `.gitkeep` only |
| Residual paths | `jobs.py` pointed at `/home/rootrecord/.ollama/skills/energy/...` |
| Priority | Migration P0 = Energy; WO-ECO-001 |

---

## 2. Source inventory

```text
/home/rootrecord/.ollama/skills/energy/scripts/read/
  leapfrog-read.sh      ← ecoflow_read_cycle (every 15s)
  delta2-read.sh
  river2pro-read.sh
  actions/              ← Phase 2+ (leave in place)
```

Also: `ECOFLOW_DUAL_READ`, `ECOFLOW_LOCK=/tmp/ecoflow-ble.lock`, READS helpers, heartbeat builtin.

---

## 3. Target layout (Pacific — org)

```text
RootRecord-Pacific-Solar-Server/Energy/
  README.md
  scripts/read/{leapfrog,delta2,river2pro}-read.sh
  lib/ (py, paths, config, envload, vendor; fill remaining from G2 if needed)
  db/ config/  (fill from G2 skill if missing after pull)
```

Ecosystem path:

```text
/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server/Energy/
```

---

## 4. Non-goals (Phase 1)

- Hybrid / solar_weather writers (Core-Ops)
- `scripts/actions/`
- Changing BLE lock or Database measured-data paths
- Weather, Geology, A-Eyes, GitHub, Telegram
- Deleting old skill tree until soak ≥1 hour

---

## 5. Steps (status)

| Step | Status |
|------|--------|
| A Snapshot | Operator |
| B–C Scripts on org Pacific | **Done** |
| D Relative ROOT in read scripts | **Done** |
| E jobs.py rewire | **Done** on org |
| F Desk pull + lib/db/config fill | **Done** 2026-09-28 (pull already up to date; `cp -an` from G2) |
| G Stack reload + live verify | **Operator** — run schedule-stack-reload; soak ≥15 min |
| H Docs | **This update** |
| I Old tree | Do not delete yet |

### Desk execution log — 2026-09-28 HST

```text
PACIFIC=/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server
git pull --ff-only origin main     → Already up to date
mkdir -p Energy/{lib,db,config}
cp -an ~/.ollama/skills/energy/lib/.    Energy/lib/
cp -an ~/.ollama/skills/energy/db/.     Energy/db/
cp -an ~/.ollama/skills/energy/config/. Energy/config/
chmod +x Energy/scripts/read/*.sh Energy/lib/py
# NEXT: Automations/scripts/stack/schedule-stack-reload.sh
# NEXT: tail -f /home/rootrecord/Database/Logs/Automations/automations_current.log
```

### Remaining desk commands

```bash
PACIFIC="/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server"
cd "$PACIFIC"
./Automations/scripts/stack/schedule-stack-reload.sh
# then watch ≥15 min:
tail -f /home/rootrecord/Database/Logs/Automations/automations_current.log
```

---

## 6. Rollback

Revert jobs.py Energy paths to `~/.ollama/skills/energy/...`, reload poller.

---

## 7. Phase 2+ backlog

actions/, hybrid reports, single-writer vs Core-Ops, vendor in-repo optional.

---

## 8. Acceptance criteria

- [x] Three read scripts under Pacific `Energy/scripts/read/` (org git)
- [x] jobs.py cycle + boot + READS point at Pacific Energy (org git)
- [x] Desk pull + lib/db/config fill complete
- [ ] Poller SUMMARY/ENERGY soak OK (≥15 min)
- [ ] Old skill `read/` not deleted without operator OK

---

## Related

- [WO-ECO-001](WO-ECO-001-Energy-Domain-Import.md)
- [WO-SRV-001](WO-SRV-001-Residual-Jobs-Path-Rewire.md)
- Org Pacific: `RootRecord-Software-Solutions/RootRecord-Pacific-Solar-Server`
