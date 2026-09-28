# WORK ORDER — Pacific Runtime Path Cutover (`skills` → `1 - Servers`)

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-SRV-2026-09-27 |
| **Date** | 2026-09-27 (HST) |
| **Status** | OPEN — Design before move |
| **Owner** | RootRecord |
| **Related** | WO-ECO; WO-MAP; `repos.conf` skills row |

**Scope:** Plan and execute a safe cutover from live `~/.ollama/skills` (Solar-Pacific desk tree) toward `RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server` without breaking poller, jobs, or github_sync. Mainland under `1 - Servers/2 - …` is in scope only when its path is intentional.

---

## 1. Intent

The Ecosystem tree defines Servers as the long-term home for deployed runtime. Today the authoritative running code and `repos.conf` **skills** path still point at `~/.ollama/skills`. Moving directories without updating jobs, systemd units, and sync config will take the desk offline.

---

## 2. Current reality

### 2.1 What exists

| Item | Location / status |
| --- | --- |
| Live skills tree | `/home/rootrecord/.ollama/skills` |
| GitHub | `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server` |
| Target local shape | `1 - Servers/1 - RootRecord-Pacific-Solar-Server` |
| Mainland target | `1 - Servers/2 - RootRecord-US-Mainland-Server` |
| Legacy zip | `Solar-Pacific-RootRecord-Server-Old-main.zip` (forensic; do not run) |
| Poller / jobs | Hard-coded paths under `~/.ollama/skills/...` in many scripts |

### 2.2 Completed so far

- [x] Target tree shape documented in WO-ECO
- [x] GitHub sync healthy for skills (inplace)
- [ ] Inventory all absolute path references
- [ ] Decide symlink vs physical move vs dual-run period
- [ ] Cutover with rollback plan

### 2.3 Known friction

- Hundreds of scripts assume `~/.ollama/skills`
- User systemd units and drop-ins point at skills paths
- Historical coupling noted in Session 02 (not permanent architecture, but real)

---

## 3. Tasks

1. Inventory path references (`jobs.py`, systemd, shell scripts, Python).
2. Choose strategy: long-lived symlink from old path → new tree, or staged move with path variable.
3. Update `repos.conf` local_path for skills (or new id) only when paths match.
4. Update systemd units / drop-ins; reboot-test once.
5. Verify poller, EcoFlow, A-EYES, weather, github_sync after cutover.
6. Document final paths in Master-Prompt map (WO-MAP).

---

## 4. Non-goals

- Teardown of Old-main zip / forensic tree in the same change
- Library or Website moves
- Changing agent persona content

---

## 5. Key file / path reference

| Path | Role |
| --- | --- |
| `~/.ollama/skills` | Current live runtime |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server` | Target |
| `github/scripts/repos.conf` | skills row |
| `automations/scripts/jobs.py` | Absolute paths |
| user systemd units | Boot persistence |

---

## 6. Open items

**Additional requirements:**

- Final directory names under `1 - Servers/`
- Whether GitHub repo is renamed when local name changes
- 

---

## 7. Notes & constraints

- No force-push.
- Secrets stay out of git.
- Prefer small reversible steps.
- Operational restoration beats path purity; cut over only with a rollback path.

---

*Work order prepared 2026-09-27 HST. Update status when closed.*
