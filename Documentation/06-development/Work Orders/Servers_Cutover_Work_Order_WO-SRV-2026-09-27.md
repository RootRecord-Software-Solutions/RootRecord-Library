# WORK ORDER — Pacific Runtime Path Cutover (`skills` → `1 - Servers`)

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-SRV-2026-09-27 |
| **Date** | 2026-09-27 (HST) |
| **Status** | **IN PROGRESS** — **systemd on Pacific**; tunnel READY; residual job domains still on G2 |
| **Owner** | RootRecord |
| **Related** | WO-ECO; WO-ECO-001; WO-MAP; WO-GH |
| **Updated** | 2026-09-28 ~16:25 HST |

**Scope:** Move authoritative runtime off `~/.ollama/skills` onto `RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server`. **Policy: do not run the old desk.**

---

## 1. Intent

Servers tree is the only live runtime home. Domain-by-domain import until `jobs.py` has zero `~/.ollama/skills` absolute paths.

---

## 2. Current reality (2026-09-28 ~16:23 HST)

### 2.1 Locked on Pacific

| Item | Status |
| --- | --- |
| Live runtime root | `/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server` |
| GitHub | `RootRecord-Software-Solutions/RootRecord-Pacific-Solar-Server` |
| **systemd ExecStart** | `/bin/bash "…/Automations/scripts/poller/run-poller.sh"` (**not** skills) |
| Unit | `rr-rootserver-poller.service` — **active (running)** |
| Log | `/home/rootrecord/Database/Logs/Automations/automations_current.log` |
| Tunnel | READY (cloudflared from Pacific Communications) |
| jobs catalog | Pacific `Automations/scripts/jobs.py` |

### 2.2 Completed

- [x] Automations core on Pacific (poller, stack, jobs)
- [x] systemd unit rewritten off G2 skills path
- [x] Path-with-spaces quoting in unit + Energy/network_globe job commands
- [x] Energy job **command** paths on Pacific
- [ ] Energy lib `read_runner.py` fill + BLE cycle OK
- [ ] Import System, Github, Telegram, A-Eyes, Weather domains
- [ ] `repos.conf` → Ecosystem paths only
- [ ] Zero skills paths in jobs.py
- [ ] Reboot-test unit still Pacific

### 2.3 Residual G2 (migrate next)

| Domain | jobs still on skills |
| --- | --- |
| Energy lib modules | need desk fill `read_runner.py` from G2 energy |
| system-stats | sys_stats_cycle |
| github | setup + sync_all |
| plumbing | ollama / flm warmup |
| telegram | council_relay |
| a-eyes | cam, grab, timelapse |
| reports | worklog_scan |
| Weather | disabled (path missing) |

---

## 3. Domain layout (standing)

```text
1 - RootRecord-Pacific-Solar-Server/
├─ Automations/scripts/{rootserver_poller.py,jobs.py,poller/,stack/}
├─ Communications/{network/cloudflare,network/scripts,telegram,github,…}
├─ Energy/   System/   Weather/   Geology/   Security/   Github/
```

---

## 4. Remaining tasks

1. Complete Energy `read_runner` fill + soak (WO-ECO-001).
2. Import System (sys-stats) → rewire job.
3. Import Github sync → rewire + repos.conf (WO-GH).
4. Communications telegram; A-Eyes; Weather.
5. Master-Prompt map (WO-MAP).
6. Archive G2 runtime use when jobs clean.

---

## 5. Notes

- No force-push; no secrets in git.
- Always quote Pacific paths (spaces in `1 - Servers`).
- Never point poller ExecStart at `~/.ollama/skills`.

---

*Updated 2026-09-28 HST after successful systemd cutover to Pacific.*
