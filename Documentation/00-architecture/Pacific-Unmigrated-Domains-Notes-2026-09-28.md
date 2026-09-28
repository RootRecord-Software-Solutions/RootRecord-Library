# Unmigrated Domains Without Pacific Folders

| Field | Value |
| --- | --- |
| **Date** | 2026-09-28 (HST) |
| **Purpose** | Document residual job domains that lack a top-level folder on `RootRecord-Pacific-Solar-Server` |
| **Rule** | Documentation only — no layout invention beyond notes |

---

## 1. Plumbing (ollama / FLM)

| Item | Value |
| --- | --- |
| Legacy path | `~/.ollama/skills/plumbing/scripts/` |
| Jobs | `ollama_warmup`, `flm_npu_warmup` (ON_BOOT) |
| Pacific folder | **None** |

**Decision needed at import:** create `Plumbing/` domain, or place under `System/scripts/plumbing/`.

Standing inference note from jobs header: prefer FLM llama3.2:3b on NPU `:52625`; Ollama dolphin lanes = CPU fallback.

---

## 2. Reports / worklog

| Item | Value |
| --- | --- |
| Legacy path | `~/.ollama/skills/reports/scripts/` |
| Jobs | `worklog_scan` → `worklog_once.sh` |
| Data | `/home/rootrecord/Database/WORKLOG/` |
| Pacific folder | **None** |

**Decision needed at import:** `Reports/` domain, or under `Automations/scripts/reports/`, or `System/`.

Observed healthy in poller window 2026-09-28.

---

## 3. Related

- Full path table: [Pacific-Jobs-Path-Inventory-2026-09-28.md](./Pacific-Jobs-Path-Inventory-2026-09-28.md)
- Domain status: [Pacific-Server-Library-Dependency-Map-2026-09-28.md](./Pacific-Server-Library-Dependency-Map-2026-09-28.md)

---

*Docs only 2026-09-28 HST.*
