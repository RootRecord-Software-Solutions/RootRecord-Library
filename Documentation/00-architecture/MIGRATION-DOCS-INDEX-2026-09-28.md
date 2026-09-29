# Pacific Migration Documentation Index (2026-09-28)

Single entry point for agents and operators working the Pacific server cutover **and** the broader product/archive inventory.

**Authority:** [RootRecord-Software-Solutions](https://github.com/RootRecord-Software-Solutions) — Library, Pacific, Database.

---

## Lineage & process

| Doc | Purpose |
| --- | --- |
| [Migration-Lineage-Three-Generations-2026-09-28.md](./Migration-Lineage-Three-Generations-2026-09-28.md) | G3 / G2 / G1 / **G0** named; import order rule |
| [Pacific-Domain-Import-Playbook-2026-09-28.md](./Pacific-Domain-Import-Playbook-2026-09-28.md) | Step-by-step Phase 0–4; retirement stub pattern |
| [Pacific-Jobs-Path-Inventory-2026-09-28.md](./Pacific-Jobs-Path-Inventory-2026-09-28.md) | **Historical** path inventory — live status is WO-SRV |
| [Pacific-Server-Library-Dependency-Map-2026-09-28.md](./Pacific-Server-Library-Dependency-Map-2026-09-28.md) | Library files touched; domain status |
| [Pacific-Unmigrated-Domains-Notes-2026-09-28.md](./Pacific-Unmigrated-Domains-Notes-2026-09-28.md) | **Superseded** for Plumbing/Reports placement (resolved under System + Reports) |

## G3 verification & residual close-out (Ava → Bruce)

| Doc | Purpose |
| --- | --- |
| [G3-Runtime-Verification-Checklist-2026-09-28.md](./G3-Runtime-Verification-Checklist-2026-09-28.md) | Runtime gate before legacy retirement (supports WO-SRV) |
| [Residual-Path-Retirement-Table-2026-09-28.md](./Residual-Path-Retirement-Table-2026-09-28.md) | Pre-filled old→new table; Bruce fills Verified/Retired |
| [Communications-Notify-Policy-Draft-2026-09-28.md](./Communications-Notify-Policy-Draft-2026-09-28.md) | Notify policy for WO-COM-001 — Carly security-sealed with conditions; operator acceptance still required |

## Product & archive inventory (Minecraft, apps, mirrors)

| Doc | Purpose |
| --- | --- |
| **[Product-Archive-Repo-Catalog-2026-09-28.md](./Product-Archive-Repo-Catalog-2026-09-28.md)** | **Full catalog** — RootMC Paper suite, Nukkit legacy, Business/Weather Manager, Solana, web, Ava stacks, **~79 inventory mirrors**, future migration tracks A–H |

**Rule:** Document now; **migrate products only after** Pacific residual domains catch up. Do **not** bulk-merge plugins into Pacific server core.

## G1 (Old) archive

| Doc | Purpose |
| --- | --- |
| **[G1 README — migration status](https://github.com/rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server-Old/blob/main/README.md)** | **Single list** of migrated / not migrated / archive + operations |
| [Solar-Pacific-Old-Inventory-Map-2026-09-28.md](./Solar-Pacific-Old-Inventory-Map-2026-09-28.md) | High-value packet → G3 mapping (Library side) |
| [Solar-Pacific-Old-Full-TopLevel-Catalog-2026-09-28.md](./Solar-Pacific-Old-Full-TopLevel-Catalog-2026-09-28.md) | All **95** G1 tops classified |

### G1 scheduler skills — retired (2026-09-28)

Folders kept; `SKILL.md` kept; **`MIGRATED.md`** added on `-Old`. Do not run.

| G1 skill | Superseded by (org Pacific) |
| --- | --- |
| `hybrid-night-poller/` | `Automations/scripts/rootserver_poller.py` + stack |
| `heartbeat/` | `jobs.py` builtin `heartbeat` |
| `net-gate/` | `Automations/scripts/poller/internet_gate.py` + tunnel jobs |

Repo: [`Solar-Pacific-RootRecord-Server-Old`](https://github.com/rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server-Old).

## G0 (deepest archive) — `old`

| Item | Link |
| --- | --- |
| **Repo** | [`rootrecordsoftwaresolutions/old`](https://github.com/rootrecordsoftwaresolutions/old) (private) |
| **G0 README** | [README.md on `old`](https://github.com/rootrecordsoftwaresolutions/old/blob/main/README.md) |
| **Shape** | ~200 **flattened** skill tops (G1 groups many of these) |
| **Role** | Feature scavenger only — **not** day-to-day ops |
| **Recovery order** | After G2→G3 and selective G1 — then G0 **diff-only** |

**Do not** start bulk recovery from G0 while Automations / Energy / System residuals are still in flight (high noise, low urgency).

### G0 unique vs G1 — thin scavenger list

| Theme | G0 packet examples |
| --- | --- |
| **Broadcast / boards** | `broadcast`, `broadcast-loop`, `broadcast-render` |
| **Day / evening reports** | `day-reports*`, `morning-report*`, `midday-report*`, `evening-report*`, `late-report*`, `hybrid-reports`, `energy-report` |
| **Hurricane / weather depth** | `hurricane-desk`, `hurricane-fetch`, `hurricane-obs`, `hurricane-radio`, `hurricane-tracker`, `live-wx`, `nws-hawaii`, `rr-noaa`, `radar-archive` |
| **Voice / media** | `voice`, `voice-events`, `startup-voice`, `kokoro`, `radio`, `youtube-download`, `obs-studio` |
| **Agents / ops** | `carly-mal`, `bruce-monitor`, `ava-ops`, `ava-ivy`, `avaivy-cloud` |
| **Council** | `council-telegram`, `council-health`, `council-quake`, `council-bruce-stats` |
| **Crypto / edge nodes** | `bitcoin`, `bitcoin-cash`, `dogecoin`, `solana`, `xmrig`, `freeltc`, `ltc-node`, `pi-node` |
| **Energy ancestry (flat)** | `ecoflow-ble-poller`, `ecoflow-automations`, `ecoflow-ac-solar-gate`, `ecoflow-quota`, `ecoflow-river-car` |

Best use: scavenger pass when redesigning **AI processing**, **weather/reports**, or **broadcast** — not while closing residual job paths.

## Session records

| Doc | Purpose |
| --- | --- |
| [Grok-Pacific-Automations-Domain-Wiring-Session-2026-09-28.md](./Grok-Pacific-Automations-Domain-Wiring-Session-2026-09-28.md) | Automations wiring session |
| Ops worklog `2026-09-28 System Operator Worklog — Session 01.md` | Operator confirmation |

## Work orders

| ID | Focus |
| --- | --- |
| WO-SRV | G2 → G3 path cutover (**authoritative** static audit + residual list) |
| WO-OLD | G1 selective recovery (blocked on G2 verification close-out) |
| WO-ECO | Ecosystem umbrella |
| WO-GH | repos.conf hygiene |
| WO-MAP | Master-Prompt map |
| WO-CF | Tunnel token |
| WO-AEYES | Capture rate |
| WO-COM-001 | Communications surface (notify policy draft linked above) |

See [`Documentation/06-development/Work-Orders/README.md`](../06-development/Work-Orders/README.md) (hyphen only — no space-named folder).

---

## Hard stops (cannot complete without operator / desk shell)

1. **G3 runtime verification** for Telegram, A-Eyes, Energy actions, Pacific poller — then legacy executable retirement (preserve `SKILL.md`)  
2. **Master-Prompt** file edits on desk `0 - Master-Prompt/` (not in Library)  
3. **repos.conf** on live Github scripts path  
4. **systemd unit** audit on desk  
5. **Secrets / tokens** restore (local only; never from git history)  

Weather remains **disabled** until its domain WO; not part of the active verification residual set above.

**Documented without executing product migration:** full product/archive catalog (Paper, Nukkit, apps, mirrors); Automations G1 retirement; G0/G1 READMEs.

---

*Index updated 2026-09-28 ~21:40 HST — hard stops + lineage blurbs aligned with WO-SRV; stale placement notes superseded.*
