# WO-ECO-001 — Action Plan (Phase 1: EcoFlow Live Read)

| Field | Value |
|-------|--------|
| **Parent WO** | [WO-ECO-001](WO-ECO-001-Energy-Domain-Import.md) |
| **Phase** | 1 of N — live BLE/API read only |
| **Status** | **Poller on Pacific** — systemd cutover done; Energy scripts/jobs on Pacific; **read_runner.py still missing on desk/org** → ecoflow_read FAIL code=1 |
| **Target repo** | `RootRecord-Software-Solutions/RootRecord-Pacific-Solar-Server` |
| **Data authority** | `/home/rootrecord/Database/ENERGY/` |
| **Date drafted** | 2026-09-28 |
| **Updated** | 2026-09-28 ~16:25 HST |

**Operator policy:** Do not run the old desk. Complete Energy lib fill, then migrate remaining G2 job domains into Pacific until zero `~/.ollama/skills` references remain in `jobs.py`.

---

## 0. Objective (Phase 1)

- [x] EcoFlow **command paths** in `jobs.py` → Pacific `Energy/scripts/read/`
- [x] systemd poller → Pacific `run-poller.sh`
- [ ] Full Energy **lib** (`read_runner.py` + BLE stack) present under Pacific
- [ ] `ecoflow_read_cycle` succeeds (SUMMARY lines)
- [ ] No G2 energy path required at runtime

---

## 5. Steps (status)

| Step | Status |
|------|--------|
| Org read scripts + jobs rewire | **Done** |
| Path quoting for spaces in Pacific paths | **Done** |
| Desk systemd cutover to Pacific | **Done** 2026-09-28 ~16:23 HST — unit active |
| Tunnel READY + ENERGY heartbeat from Database | **Observed** |
| Desk fill `read_runner.py` + related lib from G2 | **In progress (operator)** |
| Manual delta2-read + cycle OK | **Pending** |
| Soak ≥15 min without structural Energy FAIL | **Pending** |
| Commit non-secret Energy lib to org (optional) | Pending |
| Retire G2 energy runtime use | After soak |

### systemd (locked)

```text
ExecStart=/bin/bash "/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server/Automations/scripts/poller/run-poller.sh"
POLLER_LOG=/home/rootrecord/Database/Logs/Automations/automations_current.log
```

### Known gap

Org `Energy/lib/` lacks `read_runner.py`. Scripts call `lib/py` → `lib/read_runner.py`. Until desk `cp -an` from G2 energy lib supplies it, cycle/boot exit 1. Heartbeat can still show B1/B2 from Database.

### Desk fill commands

```bash
PACIFIC="/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server"
G2="/home/rootrecord/.ollama/skills/energy"
cp -an "$G2/lib/." "$PACIFIC/Energy/lib/"
cp -an "$G2/db/." "$PACIFIC/Energy/db/"
cp -an "$G2/config/." "$PACIFIC/Energy/config/"
ls -la "$PACIFIC/Energy/lib/read_runner.py"
export ENERGY_EFLIB_PATH="$PACIFIC/Energy/lib/vendor"
bash -x "$PACIFIC/Energy/scripts/read/delta2-read.sh" 2>&1 | tail -40
systemctl --user restart rr-rootserver-poller.service
```

---

## 8. Acceptance criteria

- [x] Read scripts on Pacific org git
- [x] jobs.py Energy commands on Pacific (quoted)
- [x] systemd poller on Pacific
- [ ] `read_runner.py` present under Pacific Energy/lib
- [ ] ecoflow_read_cycle OK / SUMMARY in log
- [ ] No runtime dependency on `~/.ollama/skills/energy` for reads

---

## Related

- WO-SRV (systemd + residual domain imports)
- WO-SRV-001 residual path rewire
- Org Pacific Automations + Energy READMEs
