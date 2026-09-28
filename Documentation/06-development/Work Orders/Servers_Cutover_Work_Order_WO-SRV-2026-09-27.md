# WORK ORDER — Pacific Runtime Path Cutover (`skills` → `1 - Servers`)

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-SRV-2026-09-27 |
| **Date** | 2026-09-27 (HST) |
| **Status** | IN PROGRESS — Runtime live; inventory done; domain imports pending |
| **Owner** | RootRecord |
| **Related** | WO-ECO; WO-MAP; path inventory 2026-09-28 |
| **Updated** | 2026-09-28 (HST) — inventory closed |

**Scope:** Plan and execute a safe cutover from live `~/.ollama/skills` toward `RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server` without breaking poller, jobs, or github_sync.

---

## 1. Intent

The Ecosystem tree defines Servers as the long-term home for deployed runtime. Cutover moves authoritative running code into that tree under a domain-based layout (Automations, Communications, Weather, …).

---

## 2. Current reality (2026-09-28)

### 2.1 What exists

| Item | Location / status |
| --- | --- |
| **Live runtime (confirmed)** | `/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server` |
| **GitHub** | `RootRecord-Software-Solutions/RootRecord-Pacific-Solar-Server` |
| Poller unit | `rr-rootserver-poller.service` — **active** |
| Public | `https://rootserver.rootrecord.cloud/` |
| Jobs catalog | `…/Automations/scripts/jobs.py` |
| cloudflared | `…/Communications/network/cloudflare/bin/cloudflared` |
| Legacy skills tree | `~/.ollama/skills` — still referenced by external-domain jobs |
| **Path inventory** | Library `Documentation/00-architecture/Pacific-Jobs-Path-Inventory-2026-09-28.md` |

### 2.2 Completed so far

- [x] Target tree shape documented in WO-ECO
- [x] GitHub org repo for Pacific Solar Server online
- [x] Domain folders created (Automations, Communications, Weather, Energy, …)
- [x] Automations core reorganized: `scripts/poller/`, `scripts/stack/`, `jobs.py` at scripts root
- [x] Path wiring for Automations + Communications network + Weather ensure scripts
- [x] Poller running from Ecosystem path (operator confirmed 2026-09-28)
- [x] EcoFlow BLE reads, system samples, worklog scan observed healthy in poller window
- [x] **Inventory remaining absolute path references in `jobs.py`** (full table in path inventory doc)
- [x] Domain README residual-path notes on Pacific repo (Energy, Security, System, Github, …)
- [ ] Import remaining domains (energy first) into Pacific repo — **source required**
- [ ] Update `repos.conf` skills/pacific row to Ecosystem path when catalog is ready
- [ ] Full systemd unit path audit + reboot-test

### 2.3 Observed live signals (2026-09-28 ~01:42–01:43 HST)

- systemd: **active**
- ENERGY snapshot: B2=100%, B1≈4.8%, src=sqlite
- EcoFlow SUMMARY lines: river2pro + delta2 (ble/api)
- SYSTEM samples writing under Database/SYSTEM
- worklog_scan OK
- One transient `ecoflow_read_cycle FAIL code=-15` (signal/timeout — not structural)

---

## 3. Domain layout (standing)

```text
1 - RootRecord-Pacific-Solar-Server/
├─ Automations/scripts/
│   ├─ rootserver_poller.py
│   ├─ jobs.py
│   ├─ poller/          # run, open-window, watch, internet_gate
│   └─ stack/           # stop, do-reload, schedule-reload
├─ Communications/
│   ├─ network/cloudflare/{bin,config}
│   ├─ network/scripts/
│   └─ discord|email|slack|telegram|github/
├─ Weather/scripts/
├─ Energy/  Security/  System/  Logs/  Github/  Geology/
└─ Pull.sh  Push.sh
```

---

## 4. Remaining tasks

1. ~~Inventory remaining `~/.ollama/skills` absolute paths in `jobs.py`~~ **Done** — see path inventory.
2. Import domains one at a time (energy first); rewire jobs as each lands — **blocked on operator source**.
3. Align `repos.conf` local_path with Ecosystem Servers path.
4. Audit user systemd units / drop-ins for old skills paths.
5. Document final paths in Master-Prompt map (WO-MAP).

---

## 5. Non-goals

- Teardown of Old-main zip / forensic tree in the same change
- Library or Website moves
- Importing Energy (or other) code without operator-provided source

---

## 6. Key file / path reference

| Path | Role |
| --- | --- |
| `…/1 - Servers/1 - RootRecord-Pacific-Solar-Server` | **Live runtime root** |
| `Automations/scripts/jobs.py` | Job catalog |
| Library path inventory | Exhaustive residual path table |
| `~/.ollama/skills` | Legacy references still in external domain jobs |

---

## 7. Notes & constraints

- No force-push.
- Secrets stay out of git.
- Prefer small reversible steps.
- Residual legacy job paths are acceptable until domains are imported.

---

*Work order prepared 2026-09-27 HST. Inventory closed 2026-09-28 HST (docs only).*
