# Work Orders

**Standing policy:** Do not run the old desk (`~/.ollama/skills`) as the poller host.

---

## Active backlog (updated 2026-09-28 ~16:50 HST)

| ID | Title | Status |
| --- | --- | --- |
| WO-ECO-2026-09-27 | Ecosystem migration | **IN PROGRESS** — Pacific + Energy + System LIVE |
| [WO-SRV-2026-09-27](./Servers_Cutover_Work_Order_WO-SRV-2026-09-27.md) | Pacific runtime cutover | **IN PROGRESS** — Energy + System done |
| WO-MAP / WO-OLD / WO-GH / WO-DATA / WO-AGENT / WO-CF / WO-ARCH / WO-AEYES | (unchanged) | OPEN / residual |

**WO-ECO-001** — Energy Phase 1 **COMPLETE**. **System** Phase 1 **LIVE** (`sys_stats_cycle` on Pacific).

---

## Attack order remaining

1. ~~Energy~~ ~~System~~
2. worklog (reports) **or** github **or** plumbing — operator pick
3. Telegram → A-Eyes → Weather
4. Retire G2; zero skills paths in jobs.py

## Live snapshot

```text
systemd   Pacific run-poller.sh
Energy    SUMMARY + ENERGY live (fix code=126 after restart if needed)
System    sys-sample on Pacific System/scripts/
Log       /home/rootrecord/Database/Logs/Automations/automations_current.log
```
