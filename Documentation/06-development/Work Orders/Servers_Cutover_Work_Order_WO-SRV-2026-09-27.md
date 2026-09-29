# WORK ORDER — Pacific Runtime Path Cutover (`skills` → `1 - Servers`)

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-SRV-2026-09-27 |
| **Date** | 2026-09-27 (HST) |
| **Status** | **IN PROGRESS** — Energy Phase 1 **LIVE**; next domain = **System** |
| **Owner** | RootRecord |
| **Related** | WO-ECO; WO-ECO-001 (Phase 1 complete); WO-MAP; WO-GH |
| **Updated** | 2026-09-28 ~16:40 HST |

**Scope:** Move authoritative runtime off `~/.ollama/skills` onto `RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server`. **Policy: do not run the old desk.**

---

## 1. Intent

Servers tree is the only live runtime home. Domain-by-domain import until `jobs.py` has zero `~/.ollama/skills` absolute paths.

---

## 2. Current reality (2026-09-28 ~16:40 HST)

### 2.1 Locked on Pacific

| Item | Status |
| --- | --- |
| Live runtime root | `/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server` |
| GitHub | `RootRecord-Software-Solutions/RootRecord-Pacific-Solar-Server` |
| systemd ExecStart | `/bin/bash "…/Automations/scripts/poller/run-poller.sh"` |
| Unit | `rr-rootserver-poller.service` — **active (running)** |
| Log | `/home/rootrecord/Database/Logs/Automations/automations_current.log` |
| Tunnel | READY (Pacific cloudflared); brief reconnect storms recoverable |
| jobs catalog | Pacific `Automations/scripts/jobs.py` |
| **Energy** | **LIVE** — SUMMARY delta2 / river2pro; ENERGY status=live |
| Energy package | `ln -sfn Energy energy` at Pacific root; `Energy/lib/py` PYTHONPATH |

### 2.2 Completed

- [x] Automations core on Pacific (poller, stack, jobs)
- [x] systemd unit off G2 skills path
- [x] Path-with-spaces quoting (unit + jobs)
- [x] open-poller-window launcher → Pacific path
- [x] Energy Phase 1 (scripts, lib fill, package symlink, SUMMARY soak)
- [ ] Import System (sys-stats) — **next**
- [ ] Github, Telegram, A-Eyes, Weather, plumbing, worklog
- [ ] `repos.conf` → Ecosystem only
- [ ] Zero skills paths in jobs.py
- [ ] Reboot-test unit still Pacific

### 2.3 Residual G2

| Domain | Jobs |
| --- | --- |
| system-stats | `sys_stats_cycle` ← **next** |
| reports | `worklog_scan` |
| github | setup + sync_all |
| plumbing | ollama / flm warmup |
| telegram | council_relay |
| a-eyes | cam, grab, timelapse |
| Weather | disabled |
| energy actions | Phase 2 |

---

## 3. Domain layout (standing)

```text
1 - RootRecord-Pacific-Solar-Server/
├─ Automations/scripts/{rootserver_poller.py,jobs.py,poller/,stack/}
├─ Communications/{network/cloudflare,network/scripts,telegram,github,…}
├─ Energy/   (LIVE Phase 1)
├─ System/   (next import)
├─ Weather/  Geology/  Security/  Github/
└─ energy → Energy  (symlink for Python package name)
```

---

## 4. Remaining tasks

1. **System** — copy system-stats → Pacific `System/`; rewire `sys_stats_cycle`.
2. Optional same pass: worklog + plumbing under System/.
3. Github sync + repos.conf (WO-GH).
4. Telegram; A-Eyes; Weather.
5. Master-Prompt map (WO-MAP).
6. Archive G2 runtime when jobs clean.

---

## 5. Notes

- No force-push; no secrets in git.
- Always quote Pacific paths (spaces in `1 - Servers`).
- Never point poller ExecStart at `~/.ollama/skills`.
- Energy: maintain `energy` → `Energy` symlink on every checkout.

---

*Updated 2026-09-28 ~16:40 HST — Energy Phase 1 LIVE + soak.*
