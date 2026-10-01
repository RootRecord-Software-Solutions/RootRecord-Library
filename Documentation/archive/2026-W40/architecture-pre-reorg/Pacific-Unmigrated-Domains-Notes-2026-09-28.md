# Unmigrated Domains Without Pacific Folders

| Field | Value |
| --- | --- |
| **Date** | 2026-09-28 (HST) |
| **Status** | **SUPERSEDED** for Plumbing + Reports placement |
| **Purpose** | Historical note from earlier 2026-09-28; placement decisions later resolved |
| **Rule** | Documentation only — do not re-open settled folder decisions from this file |

> **Authoritative status:** [Servers_Cutover_Work_Order_WO-SRV-2026-09-27.md](../06-development/Work-Orders/Servers_Cutover_Work_Order_WO-SRV-2026-09-27.md) and [Pacific-Domain-Import-Playbook-2026-09-28.md](./Pacific-Domain-Import-Playbook-2026-09-28.md).  
> Residual work is **runtime verification / legacy retirement**, not “missing Pacific folders” for the domains below.

---

## 1. Plumbing (ollama / FLM) — RESOLVED

| Item | Value |
| --- | --- |
| Legacy path | `~/.ollama/skills/plumbing/scripts/` |
| Jobs | `ollama_warmup`, `flm_npu_warmup` (ON_BOOT) |
| Pacific placement | **`System/scripts/plumbing/`** (gates PASS per WO-SRV 2026-09-29: non-NPU + NPU on demand) |

Standing inference note (updated 2026-09-29): prefer FLM `llama3.2:1b` **on demand** on NPU `:52625` (started per request by `run-infer.sh`, stopped on exit; no resident warmup); Ollama dolphin lanes = CPU fallback (`--keepalive 0`). Enforcement remains Bruce’s single-flight path.

---

## 2. Reports / worklog — RESOLVED

| Item | Value |
| --- | --- |
| Legacy path | `~/.ollama/skills/reports/scripts/` |
| Jobs | `worklog_scan` → `worklog_once.sh` |
| Data | `/home/rootrecord/Database/WORKLOG/` |
| Pacific placement | **`Reports/`** domain (worklog_scan PASS; roll-up VERIFY PENDING — WO-RPT-001) |

---

## 3. Still outside this note

| Topic | Where to look |
| --- | --- |
| Telegram / A-Eyes verification | WO-SRV + [G3-Runtime-Verification-Checklist-2026-09-28.md](./G3-Runtime-Verification-Checklist-2026-09-28.md) |
| Path retirement tracking | [Residual-Path-Retirement-Table-2026-09-28.md](./Residual-Path-Retirement-Table-2026-09-28.md) |
| Weather (disabled) | WO-WXG-001 / jobs.py disabled entry |
| Full historical path table | [Pacific-Jobs-Path-Inventory-2026-09-28.md](./Pacific-Jobs-Path-Inventory-2026-09-28.md) (historical — see its banner) |

---

*Superseding banner added 2026-09-28 ~21:40 HST. Original placement questions for Plumbing/Reports are closed.*
