# Pacific `jobs.py` Path Inventory

| Field | Value |
| --- | --- |
| **Date** | 2026-09-28 (HST) |
| **Source file** | `RootRecord-Pacific-Solar-Server/Automations/scripts/jobs.py` (SHA at inventory: live main) |
| **Live catalog path** | `…/1 - Servers/1 - RootRecord-Pacific-Solar-Server/Automations/scripts/jobs.py` |
| **Purpose** | Complete list of absolute/legacy path references so domain imports can rewire without guessing |
| **Rule** | Documentation only — no code changes in this artifact |

---

## 1. Summary

| Category | Count (approx.) | Notes |
| --- | --- | --- |
| Jobs using **legacy** `~/.ollama/skills/…` | Majority of external domains | Energy, a-eyes, github, plumbing, telegram, system-stats, reports |
| Jobs using **mixed** paths | Boot self_terminal, CF bin, Weather, network ensure | Paths under skills but PascalCase domain names (cutover transitional) |
| Jobs with **no filesystem skill path** | heartbeat, ensure_tunnel_online, builtins | Engine-owned |

**Important transitional pattern:** some boot jobs already use `~/.ollama/skills/Automations/…` and `~/.ollama/skills/Communications/…` (PascalCase under skills). Live operator confirmation showed the **running** jobs path is the Ecosystem Servers tree. Treat Ecosystem path as authoritative for the catalog file; legacy absolute strings inside the catalog still execute against whatever exists on disk at those paths.

---

## 2. Constants / helpers

| Symbol | Path value | Domain |
| --- | --- | --- |
| `ECOFLOW_DUAL_READ` | `…/skills/energy/scripts/read/{delta2,river2pro}-read.sh` | Energy |
| `ECOFLOW_ACTIONS` | `…/skills/energy/scripts/actions` | Energy |
| `ECOFLOW_LOCK` | `/tmp/ecoflow-ble.lock` | local lock (OK) |
| `READS[].script` | delta2 / river2pro under `…/skills/energy/scripts/read/` | Energy |

---

## 3. ON_BOOT

| id | Paths | Domain | Import status |
| --- | --- | --- | --- |
| `self_terminal` | `process` → `…/skills/Automations/scripts/rootserver_poller.py`; `watch` → `…/skills/Automations/scripts/poller/poller-watch.py` | Automations | Core in Pacific repo; **absolute strings still skills-prefixed** |
| `cloudflare_tunnel` | `cloudflared_bin` → `…/skills/Communications/network/cloudflare/bin/cloudflared`; token `~/.cloudflared/rootserver.token` | Communications | Binary in Pacific repo; absolute string skills-prefixed |
| `github_setup_remotes` | `…/skills/github/scripts/setup-all-remotes.sh`; cwd `…/skills/github` | Github | **Unimported** |
| `ollama_warmup` | `…/skills/plumbing/scripts/ollama-warmup.sh` | Plumbing | **Unimported** |
| `flm_npu_warmup` | `…/skills/plumbing/scripts/flm-warmup.sh` | Plumbing | **Unimported** |
| `council_relay` | `…/skills/coms/telegram/scripts/ensure-relay.sh`; cwd `…/skills/coms/telegram` | Communications/telegram | **Unimported** (shell only in Pacific) |
| `a_eyes_cam_server` | `…/skills/a-eyes/scripts/ensure_cam_server.sh`; cwd `…/skills/a-eyes` | Security/A-EYES | **Unimported** |
| `a_eyes_timelapse_catchup` | `…/skills/a-eyes/scripts/timelapse_catchup.sh` | Security/A-EYES | **Unimported** |
| `weather_poller` | `…/skills/Weather/scripts/ensure-weather-poller.sh`; cwd `…/skills/Weather` | Weather | Ensure script in Pacific; absolute string skills-prefixed |
| `network_globe_hawaii` | command `…/skills/Communications/network/scripts/ensure-network-globe-hawaii.sh`; cwd `…/skills/coms/ssh/local-data-globe` | Communications/network | Ensure in Pacific; **cwd still legacy coms/ssh** |

---

## 4. ONCE_AT_START

| id | Paths | Domain |
| --- | --- | --- |
| `ecoflow_read_boot` | `ECOFLOW_DUAL_READ`; cwd `…/skills/energy` | Energy — **Unimported** |

---

## 5. EVERY_SECONDS

| id | Paths | Domain |
| --- | --- | --- |
| `heartbeat` | (builtin) | Automations engine |
| `ecoflow_read_cycle` | `…/skills/energy/scripts/read/leapfrog-read.sh`; cwd `…/skills/energy` | Energy — **Unimported** |
| `sys_stats_cycle` | `…/skills/system-stats/scripts/sys-sample.sh`; cwd `…/skills/system-stats` | System — **Unimported** |
| `github_sync_all` | `…/skills/github/scripts/sync-all.sh`; cwd `…/skills/github` | Github — **Unimported** |
| `worklog_scan` | `…/skills/reports/scripts/worklog_once.sh`; cwd `…/skills/reports/scripts` | Reports — **Unimported** |
| `a_eyes_frame_grab` | `…/skills/a-eyes/scripts/grab_all.sh`; cwd `…/skills/a-eyes` | Security/A-EYES — **Unimported** |

---

## 6. EVERY_MINUTE / EVERY_HOUR / ON_AT

| id | Paths | Domain |
| --- | --- | --- |
| `ensure_tunnel_online` | (builtin) | Automations |
| `a_eyes_timelapse_hourly_compile` | `…/skills/a-eyes/scripts/timelapse_hourly.sh` | Security/A-EYES |
| `a_eyes_timelapse_daily_render` | `…/skills/a-eyes/scripts/timelapse_daily.sh` | Security/A-EYES |

---

## 7. Energy domain — expected layout after import (doc only)

When Energy source is provided, target shape under Pacific repo:

```text
Energy/
  README.md
  scripts/
    read/
      delta2-read.sh
      river2pro-read.sh
      leapfrog-read.sh
    actions/          # ecoflow_command() scripts
  # store/ secrets stay local — never commit tokens
```

**jobs.py rewires after import (future code step):**

| Current | Target (illustrative) |
| --- | --- |
| `…/skills/energy/scripts/read/…` | `…/Energy/scripts/read/…` under Ecosystem Servers root |
| cwd `…/skills/energy` | cwd → Energy domain root on Ecosystem path |

Prefer resolving from `REPO_ROOT` relative paths once engine supports it; until then absolute Ecosystem paths match the live catalog home.

**Data remains:** `/home/rootrecord/Database/ENERGY/` (not in git).

---

## 8. Related documents

| Doc | Role |
| --- | --- |
| [Pacific-Server-Library-Dependency-Map-2026-09-28.md](./Pacific-Server-Library-Dependency-Map-2026-09-28.md) | Library file inventory |
| [Grok-Pacific-Automations-Domain-Wiring-Session-2026-09-28.md](./Grok-Pacific-Automations-Domain-Wiring-Session-2026-09-28.md) | Wiring session |
| WO-SRV | Cutover work order |
| WO-AEYES | A-EYES interval / path notes |

---

*Inventory from live `jobs.py` content 2026-09-28 HST. Documentation only.*
