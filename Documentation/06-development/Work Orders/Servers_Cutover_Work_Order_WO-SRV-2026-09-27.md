# WORK ORDER — Pacific Runtime Path Cutover (`skills` → `1 - Servers`)

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-SRV-2026-09-27 |
| **Date** | 2026-09-27 (HST) |
| **Status** | IN PROGRESS — Runtime live; Energy Phase 1 desk fill done; residual non-Energy paths remain |
| **Owner** | RootRecord |
| **Related** | WO-ECO; WO-MAP; WO-ECO-001; path inventory 2026-09-28 |
| **Updated** | 2026-09-28 ~16:15 HST — Energy desk fill |

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
| Stack control | `…/Automations/scripts/stack/{schedule,do}-stack-reload.sh`, `stop-poller-stack.sh` |
| cloudflared | `…/Communications/network/cloudflare/bin/cloudflared` |
| Legacy skills tree | `~/.ollama/skills` — still referenced by non-Energy domain jobs |
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
- [x] **Energy Phase 1** — org read scripts + jobs rewire + desk lib/db/config fill (2026-09-28)
- [ ] Energy stack reload + ≥15 min SUMMARY/ENERGY soak
- [ ] Clear residual Energy inventory rows after soak
- [ ] Import remaining domains one at a time
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
2. Complete Energy Phase 1 soak; then residual Energy path cleanup (WO-ECO-001 / WO-SRV-001).
3. Import next domains one at a time; rewire jobs as each lands.
4. Align `repos.conf` local_path with Ecosystem Servers path.
5. Audit user systemd units / drop-ins for old skills paths.
6. Document final paths in Master-Prompt map (WO-MAP).

---

## 5. Non-goals

- Teardown of Old-main zip / forensic tree in the same change
- Library or Website moves
- Bulk-deleting G2 skill tree before domain soak

---

## 6. Key file / path reference

| Path | Role |
| --- | --- |
| `…/1 - Servers/1 - RootRecord-Pacific-Solar-Server` | **Live runtime root** |
| `Automations/scripts/jobs.py` | Job catalog |
| `Automations/scripts/stack/schedule-stack-reload.sh` | Deploy reload trigger |
| Library path inventory | Exhaustive residual path table |
| `~/.ollama/skills` | Legacy references still in external domain jobs |

---

## 7. Notes & constraints

- No force-push.
- Secrets stay out of git.
- Prefer small reversible steps.
- Residual legacy job paths are acceptable until domains are imported.

---

*Work order prepared 2026-09-27 HST. Inventory closed 2026-09-28 HST. Energy desk fill 2026-09-28 HST.*
