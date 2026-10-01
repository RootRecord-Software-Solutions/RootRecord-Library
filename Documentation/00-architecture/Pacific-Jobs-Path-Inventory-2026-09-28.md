# Pacific `jobs.py` Path Inventory

| Field | Value |
| --- | --- |
| **Date** | 2026-09-28 (HST) |
| **Status** | **HISTORICAL SNAPSHOT** — earlier same-day inventory |
| **Source file** | `RootRecord-Pacific-Solar-Server/Automations/scripts/jobs.py` (at time of inventory) |
| **Purpose** | Audit trail of absolute/legacy path references so domain imports could rewire without guessing |
| **Rule** | Documentation only — no code changes in this artifact |

> **Do not treat tables below as current LIVE status.**  
> **Authoritative cutover status:** [Servers_Cutover_Work_Order_WO-SRV-2026-09-27.md](../06-development/Work-Orders/Servers_Cutover_Work_Order_WO-SRV-2026-09-27.md)  
> **Runtime gate:** [G3-Runtime-Verification-Checklist-2026-09-28.md](./G3-Runtime-Verification-Checklist-2026-09-28.md)  
> **Retirement tracking:** [Residual-Path-Retirement-Table-2026-09-28.md](./Residual-Path-Retirement-Table-2026-09-28.md)  
> Later 2026-09-28 WO-SRV audits report Pacific **source paths landed** for Energy, System/Plumbing, Reports, Github, Telegram, A-Eyes; residual is **runtime verification**, not “unimported folder.”

---

## 1. Summary (at inventory time)

| Category | Count (approx.) | Notes |
| --- | --- | --- |
| Jobs using **legacy** `~/.ollama/skills/…` | Majority of external domains | Energy, a-eyes, github, plumbing, telegram, system-stats, reports |
| Jobs using **mixed** paths | Boot self_terminal, CF bin, Weather, network ensure | Paths under skills but PascalCase domain names (cutover transitional) |
| Jobs with **no filesystem skill path** | heartbeat, ensure_tunnel_online, builtins | Engine-owned |

**Important transitional pattern:** some boot jobs already used `~/.ollama/skills/Automations/…` and `~/.ollama/skills/Communications/…` (PascalCase under skills). Live operator confirmation showed the **running** jobs path is the Ecosystem Servers tree. Treat Ecosystem path as authoritative for the catalog file; legacy absolute strings inside the catalog still execute against whatever exists on disk at those paths.

---

## 2. Constants / helpers (inventory-time)

| Symbol | Path value | Domain |
| --- | --- | --- |
| `ECOFLOW_DUAL_READ` | `…/skills/energy/scripts/read/{delta2,river2pro}-read.sh` | Energy |
| `ECOFLOW_ACTIONS` | `…/skills/energy/scripts/actions` | Energy |
| `ECOFLOW_LOCK` | `/tmp/ecoflow-ble.lock` | local lock (OK) |
| `READS[].script` | delta2 / river2pro under `…/skills/energy/scripts/read/` | Energy |

---

## 3. ON_BOOT (inventory-time)

| id | Paths | Domain | Import status then |
| --- | --- | --- | --- |
| `self_terminal` | `process` → `…/skills/Automations/scripts/rootserver_poller.py`; `watch` → `…/skills/Automations/scripts/poller/poller-watch.py` | Automations | Core in Pacific repo; absolute strings still skills-prefixed |
| `cloudflare_tunnel` | `cloudflared_bin` → `…/skills/Communications/network/cloudflare/bin/cloudflared`; token `~/.cloudflared/rootserver.token` | Communications | Binary in Pacific repo; absolute string skills-prefixed |
| `github_setup_remotes` | `…/skills/github/scripts/setup-all-remotes.sh`; cwd `…/skills/github` | Github | Listed unimported at inventory time |
| `ollama_warmup` | `…/skills/plumbing/scripts/ollama-warmup.sh` | Plumbing | Listed unimported |
| `flm_npu_warmup` | `…/skills/plumbing/scripts/flm-warmup.sh` | Plumbing | Listed unimported |
| `council_relay` | `…/skills/coms/telegram/scripts/ensure-relay.sh`; cwd `…/skills/coms/telegram` | Communications/telegram | Listed unimported |
| `a_eyes_cam_server` | `…/skills/a-eyes/scripts/ensure_cam_server.sh`; cwd `…/skills/a-eyes` | A-Eyes | Listed unimported |
| `a_eyes_timelapse_catchup` | `…/skills/a-eyes/scripts/timelapse_catchup.sh` | A-Eyes | Listed unimported |
| `weather_poller` | `…/skills/Weather/scripts/ensure-weather-poller.sh`; cwd `…/skills/Weather` | Weather | Ensure script in Pacific; absolute string skills-prefixed |
| `network_globe_hawaii` | command `…/skills/Communications/network/scripts/ensure-network-globe-hawaii.sh`; cwd `…/skills/coms/ssh/local-data-globe` | Communications/network | Ensure in Pacific; cwd still legacy at inventory time |

---

## 4–6. ONCE_AT_START / EVERY_SECONDS / HOURLY (inventory-time)

See original sections retained conceptually:

- Energy read/cycle, sys_stats, github_sync_all, worklog_scan, a_eyes_frame_grab were skills-prefixed at inventory time  
- `a_eyes_timelapse_hourly_compile` / daily similarly  
- Weather remains **disabled** in later WO-SRV scope  

For **current** path strings, re-read Pacific `Automations/scripts/jobs.py` or WO-SRV audit sections — do not patch from this file.

---

## 7. Energy domain — expected layout (still valid as target shape)

```text
Energy/
  README.md
  scripts/
    read/
      delta2-read.sh
      river2pro-read.sh
      leapfrog-read.sh
    actions/
```

**Data remains:** `/home/rootrecord/Database/ENERGY/` (not in git).

---

## 8. Related documents

| Doc | Role |
| --- | --- |
| [WO-SRV](../06-development/Work-Orders/Servers_Cutover_Work_Order_WO-SRV-2026-09-27.md) | **Authoritative** cutover + static audits |
| [G3-Runtime-Verification-Checklist-2026-09-28.md](./G3-Runtime-Verification-Checklist-2026-09-28.md) | Runtime gate |
| [Residual-Path-Retirement-Table-2026-09-28.md](./Residual-Path-Retirement-Table-2026-09-28.md) | Retirement tracking |
| [Pacific-Domain-Import-Playbook-2026-09-28.md](./Pacific-Domain-Import-Playbook-2026-09-28.md) | Import rules |
| [MIGRATION-DOCS-INDEX-2026-09-28.md](./MIGRATION-DOCS-INDEX-2026-09-28.md) | Entry point |

---

*Historical inventory from live `jobs.py` content earlier 2026-09-28 HST. Banner + authority pointers added ~21:40 HST same day. Documentation only.*
