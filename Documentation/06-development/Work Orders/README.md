# Work Orders

Active implementation and migration work for RootRecord. Use the template at `Documentation/01-operations/templates/TEMPLATE Work Order.md` for new items.

**Standing policy (2026-09-28):** Do not run the old desk (`~/.ollama/skills`) as the poller host. Complete domain imports into `1 - Servers/1 - RootRecord-Pacific-Solar-Server` until `jobs.py` has zero skills absolute paths.

---

## Active backlog (updated 2026-09-28 ~16:25 HST)

| ID | Title | Status |
| --- | --- | --- |
| [WO-ECO-2026-09-27](./Ecosystem_Migration_Work_Order_WO-ECO-2026-09-27.md) | Ecosystem migration & repository foundation | **IN PROGRESS** — Pacific runtime + systemd live |
| [WO-SRV-2026-09-27](./Servers_Cutover_Work_Order_WO-SRV-2026-09-27.md) | Pacific runtime path cutover (G2 → G3) | **IN PROGRESS** — **systemd on Pacific**; residual job domains remain |
| [WO-MAP-2026-09-27](./MasterPrompt_RepoMap_Work_Order_WO-MAP-2026-09-27.md) | Master-Prompt repository ownership map | OPEN |
| [WO-OLD-2026-09-28](./Old_Server_Selective_Recovery_Work_Order_WO-OLD-2026-09-28.md) | Selective recovery from Old (G1) | OPEN — blocked on G2→G3 residual clear |
| [WO-GH-2026-09-27](./GitHub_Catalog_Hygiene_Work_Order_WO-GH-2026-09-27.md) | GitHub catalog hygiene | OPEN — repos.conf still transitional |
| [WO-DATA-2026-09-27](./Database_Boundary_Work_Order_WO-DATA-2026-09-27.md) | Database boundary & publication policy | OPEN |
| [WO-AGENT-2026-09-27](./AgentContext_CanonicalHome_Work_Order_WO-AGENT-2026-09-27.md) | Agent context canonical home | OPEN |
| [WO-CF-2026-09-27](./Cloudflare_Tunnel_Recovery_Work_Order_WO-CF-2026-09-27.md) | Cloudflare tunnel credential recovery | OPEN — tunnel READY observed on Pacific |
| [WO-ARCH-2026-09-27](./Ops_Weekly_Archive_Work_Order_WO-ARCH-2026-09-27.md) | Weekly operations log archive | OPEN |
| [WO-AEYES-2026-09-27](./A-EYES_Work_Order_WO-AEYES-2026-09-27.md) | A-EYES capture / timelapse | OPEN — still G2 job paths |

**Related:** [WO-ECO-001](../Work-Orders/WO-ECO-001-Energy-Domain-Import.md) — Energy commands on Pacific; **fill `read_runner.py`** then soak.

---

## Suggested attack order (100% new layout)

1. **Energy lib fill** — `read_runner.py` + modules from G2 energy → Pacific; manual read OK; restart unit; SUMMARY soak.
2. **System domain** — import system-stats → Pacific `System/`; rewire `sys_stats_cycle`.
3. **Github domain** — move sync scripts off skills; rewire github_* jobs; fix repos.conf (WO-GH).
4. **Communications** — telegram / council-relay under Pacific Communications.
5. **A-Eyes** — import under Pacific domain; rewire a_eyes_* jobs.
6. **Weather** — import path; re-enable weather_poller.
7. **Retire G2** — zero skills paths in jobs.py; archive `~/.ollama/skills` runtime use.
8. **WO-MAP / WO-ECO close** when foundation settled.

Architecture maps:

- `Documentation/00-architecture/Migration-Lineage-Three-Generations-2026-09-28.md`
- `Documentation/00-architecture/Solar-Pacific-Old-Inventory-Map-2026-09-28.md`
- `Documentation/00-architecture/Pacific-Domain-Import-Playbook-2026-09-28.md`

---

## Rules

- One WO per coherent outcome; link related IDs.
- Keep **Status** accurate (`OPEN`, `IN PROGRESS`, `BLOCKED`, `CLOSED`).
- Closed WOs: weekly archive under `Documentation/06-development/archive/YYYY-Www/`.
- No secrets in WO text.
- **Never bulk-merge G1 `origin/` into G3 runtime.**
- **Never point systemd poller ExecStart at `~/.ollama/skills`.**
- Canonical Work Orders directory is `Work Orders/` (space). Hyphenated `Work-Orders/` is transitional for proposal IDs.
- Pacific paths contain spaces — always quote in shell/job command strings.
