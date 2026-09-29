# Work Orders

Active implementation and migration work for RootRecord. Use the template at `Documentation/01-operations/templates/TEMPLATE Work Order.md` for new items.

**Standing policy (2026-09-28):** Do not run the old desk (`~/.ollama/skills`) as the poller host. Complete domain imports into `1 - Servers/1 - RootRecord-Pacific-Solar-Server` until `jobs.py` has zero skills absolute paths.

---

## Active backlog (updated 2026-09-28 ~16:40 HST)

| ID | Title | Status |
| --- | --- | --- |
| [WO-ECO-2026-09-27](./Ecosystem_Migration_Work_Order_WO-ECO-2026-09-27.md) | Ecosystem migration & repository foundation | **IN PROGRESS** — Pacific + systemd + Energy LIVE |
| [WO-SRV-2026-09-27](./Servers_Cutover_Work_Order_WO-SRV-2026-09-27.md) | Pacific runtime path cutover (G2 → G3) | **IN PROGRESS** — Energy done; **next: System** |
| [WO-MAP-2026-09-27](./MasterPrompt_RepoMap_Work_Order_WO-MAP-2026-09-27.md) | Master-Prompt repository ownership map | OPEN |
| [WO-OLD-2026-09-28](./Old_Server_Selective_Recovery_Work_Order_WO-OLD-2026-09-28.md) | Selective recovery from Old (G1) | OPEN — blocked on residual G2 clear |
| [WO-GH-2026-09-27](./GitHub_Catalog_Hygiene_Work_Order_WO-GH-2026-09-27.md) | GitHub catalog hygiene | OPEN |
| [WO-DATA-2026-09-27](./Database_Boundary_Work_Order_WO-DATA-2026-09-27.md) | Database boundary & publication policy | OPEN |
| [WO-AGENT-2026-09-27](./AgentContext_CanonicalHome_Work_Order_WO-AGENT-2026-09-27.md) | Agent context canonical home | OPEN |
| [WO-CF-2026-09-27](./Cloudflare_Tunnel_Recovery_Work_Order_WO-CF-2026-09-27.md) | Cloudflare tunnel credential recovery | OPEN — tunnel READY on Pacific |
| [WO-ARCH-2026-09-27](./Ops_Weekly_Archive_Work_Order_WO-ARCH-2026-09-27.md) | Weekly operations log archive | OPEN |
| [WO-AEYES-2026-09-27](./A-EYES_Work_Order_WO-AEYES-2026-09-27.md) | A-EYES capture / timelapse | OPEN — still G2 job paths |

**Related:** [WO-ECO-001](../Work-Orders/WO-ECO-001-Energy-Domain-Import.md) — **Phase 1 COMPLETE / LIVE** (SUMMARY soak 16:39–16:40 HST).

---

## Suggested attack order (100% new layout)

1. ~~**Energy**~~ — **DONE** Phase 1 LIVE (systemd + lib + SUMMARY).
2. **System** — import system-stats → Pacific `System/`; rewire `sys_stats_cycle` (optional: worklog + plumbing).
3. **Github** — sync scripts + repos.conf (WO-GH).
4. **Communications** — telegram / council-relay.
5. **A-Eyes** — import; rewire a_eyes_*.
6. **Weather** — import; re-enable weather_poller.
7. **Retire G2** — zero skills paths in jobs.py; archive skills runtime use.
8. **WO-MAP / WO-ECO close** when foundation settled.

Architecture maps:

- `Documentation/00-architecture/Migration-Lineage-Three-Generations-2026-09-28.md`
- `Documentation/00-architecture/Solar-Pacific-Old-Inventory-Map-2026-09-28.md`
- `Documentation/00-architecture/Pacific-Domain-Import-Playbook-2026-09-28.md`

---

## Snapshot — what is live (2026-09-28 ~16:40 HST)

```text
Runtime:  …/1 - Servers/1 - RootRecord-Pacific-Solar-Server
systemd:  rr-rootserver-poller.service  ExecStart=Pacific run-poller.sh
Log:      /home/rootrecord/Database/Logs/Automations/automations_current.log
Public:   https://rootserver.rootrecord.cloud/
Energy:   SUMMARY=delta2 / river2pro alternating; ENERGY status=live
```

Still G2-commanded: sys_stats, worklog, github_*, plumbing, telegram, a-eyes_*.

---

## Rules

- One WO per coherent outcome; link related IDs.
- Keep **Status** accurate (`OPEN`, `IN PROGRESS`, `BLOCKED`, `CLOSED`).
- Closed WOs: weekly archive under `Documentation/06-development/archive/YYYY-Www/`.
- No secrets in WO text.
- **Never bulk-merge G1 `origin/` into G3 runtime.**
- **Never point systemd poller ExecStart at `~/.ollama/skills`.**
- Canonical Work Orders directory is `Work Orders/` (space).
- Pacific paths contain spaces — always quote in shell/job command strings.
- Energy package: `ln -sfn Energy energy` at Pacific root on every checkout.
