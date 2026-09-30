# Pacific Migration Documentation Index (2026-09-28)

Single entry point for agents and operators working the Pacific server cutover **and** the broader product/archive inventory.

**Authority:** [RootRecord-Software-Solutions](https://github.com/RootRecord-Software-Solutions) — Library, Pacific, Database.

**Desk git root (2026-09-29):** this checkout is one repository, [RootRecord-Ecosystem](https://github.com/RootRecord-Software-Solutions/RootRecord-Ecosystem). Library, Pacific, and Database here are directories in that tree. Older notes in this index that assume three nested clones describe the migration as it stood, not the current desk.

**What Alexander still has to decide (2026-09-30 02:35 HST):** [What's left for Alexander](../01-operations/2026-09-30-whats-left-for-alexander.md). The runtime cutover is live. Root Monitor is the login window. Delta 2 silence is expected. Closed work orders are in `Work-Orders/Complete/`. The open list is Root Monitor `Lib/rr_migration.json` (16 items).

**Team constitution (standing):** [Local-Multi-Agent-Team-and-Migration-to-Build-2026-09-28.md](./Local-Multi-Agent-Team-and-Migration-to-Build-2026-09-28.md) — Ava → Carly → Bruce; small local models; migrate then build.

---

## Lineage & process

| Doc | Purpose |
| --- | --- |
| [Local-Multi-Agent-Team-and-Migration-to-Build-2026-09-28.md](./Local-Multi-Agent-Team-and-Migration-to-Build-2026-09-28.md) | **Team OS** — roles, truth gates, migrate→build, hardware capacity |
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
| [Communications-Notify-Policy-Draft-2026-09-28.md](./Communications-Notify-Policy-Draft-2026-09-28.md) | Notify policy draft for WO-COM-001 (Carly conditional seal may land via PR; check main) |
| **[07-testing/README.md](../07-testing/README.md)** | **Testing thread** (2026-09-29): one record per test run (HST time, method, pass criteria, state, resource impact, evidence, SHAs, cleanup) + test-safety policy + index |
| **[08-ideas/README.md](../08-ideas/README.md)** | **Ideas & feature proposals** (2026-09-29): all PROPOSED; auto-recovery, `npu-status.sh` Pacific copy, AI processing log, voice reports, relay message hold, weather retention/repo |
| [AI-Specialist-Models-and-Routing.md](./AI-Specialist-Models-and-Routing.md) | **AI specialists + router** (2026-09-29): one Modelfile per function/topic, keyword router `route-specialist.py`, FLM system-message route, gated `run-infer.sh` hook (off by default), resource policy, how to add a specialist |
| [Template-Report-Generation.md](./Template-Report-Generation.md) | **Template reports** (2026-09-29): `Reports/template_fill.py` fills the 4 `01-operations/templates/` from measured data into Database `Reports/Generated/` (never the Library); `template_validate.py` rejects structure mismatches and flags unsupported numbers; `rr-exec` drafts free text only; job `template_reports_daily` OFF unless `RR_TEMPLATE_REPORTS=1` |
| [Voice-Reports-G3.md](./Voice-Reports-G3.md) | **Voice (2026-09-29)**: Kokoro-82M G3 port, persona map, phrase-clip cache, G1→G3 report map, gates (delivery OFF), naming standard (PROPOSED) |
| [AI-Processing-Logs-and-Reports.md](./AI-Processing-Logs-and-Reports.md) | **AI processing (2026-09-29)**: run-infer JSONL fields, rotation, report, `RR_AI_REPORT` gate, FLM log redaction |
| Ops worklog `2026-09-29 System Operator Worklog — Overnight.md` | Overnight docs pass steps (HST) + **Needs Alexander sign-off** list |

## 2026-09-29 afternoon: AWS Mainland node, globe landing, Root Monitor, Android

| Doc | Purpose |
| --- | --- |
| [US-Mainland-Server.md](./US-Mainland-Server.md) | **AWS continuity node**: desk checkout, change log, and the current AWS state table (at pause, 16:25 HST) |
| [07-testing/2026-09-29-aws-hawaii-trim-and-cloudflared.md](../07-testing/2026-09-29-aws-hawaii-trim-and-cloudflared.md) | **AWS Hawaii feed trim + `*/15` auto-trim cron; cloudflared tunnel restored** (`www` 530 → 200): PASS |
| [07-testing/2026-09-29-aws-globe-static-allowlist.md](../07-testing/2026-09-29-aws-globe-static-allowlist.md) | **AWS static allowlist** (P0: globe `server.js` no longer serves its folder; sensitive paths 404): PASS |
| [08-ideas/2026-09-29-aws-fallback-rebuild.md](../08-ideas/2026-09-29-aws-fallback-rebuild.md) | **AWS fallback rebuild**: small fallback node with per-function toggles; Phase 2 LANDED on the trimmed t3.micro profile (908 MB RAM); real fallback VERIFY PENDING |
| [08-ideas/2026-09-29-globe-landing-overlay.md](../08-ideas/2026-09-29-globe-landing-overlay.md) | **Globe landing overlay** for `www.rootrecord.cloud` (glass cards; v2 spin / click info; AWS Ohio node): AWS deploy LANDED 16:10 HST; real-browser check VERIFY PENDING. Records: [preview](../07-testing/2026-09-29-globe-landing-overlay-preview.md), [v2](../07-testing/2026-09-29-globe-overlay-v2-spin-click-info.md), [AWS deploy](../07-testing/2026-09-29-globe-overlay-aws-deploy.md) |
| [07-testing/2026-09-29-root-monitor-toggle-buttons.md](../07-testing/2026-09-29-root-monitor-toggle-buttons.md) | **Control Panel (Root Monitor) toggle buttons**: switches → labelled buttons, visible camera viewer button: PASS |
| [Control-Panel-GTK.md](./Control-Panel-GTK.md) | Root Monitor (GTK4 Control Panel): pages, settings, AWS Fallback page, sign-off items |
| [Android-Apps-Inventory.md](./Android-Apps-Inventory.md) | **Android apps inventory**: 9 apps imported into `6 - Android Development` (80.7 MB); build VERIFY PENDING. [Test record](../07-testing/2026-09-29-android-apps-import.md) |

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
| **[Old-Repo-Migration-Matrix.md](./Old-Repo-Migration-Matrix.md)** | G1 + G0 → G3 matrix (90 rows: migrated / partial / missing, target, blockers), 2026-09-29 pass |
| **[Pending-Job-Registrations-2026-09-29.md](./Pending-Job-Registrations-2026-09-29.md)** | Job registrations: 7 gated blocks already in jobs.py (sign-off) + 10 PROPOSED blocks not in jobs.py (net sampler, solar / security / bandwidth desks, Hawaiʻi news; 14:40: HLS fetcher, official-weather + boot-brief voice, report-board catch-up, global hurricane board) |
| **[G1-Scheduler-To-G3-Jobs-Map-2026-09-29.md](./G1-Scheduler-To-G3-Jobs-Map-2026-09-29.md)** | G1 `scheduler-clock` job ids (64) → G3 state (LIVE / GATED / PROPOSED / ON DEMAND / BLOCKED / OUT); matrix row 15 verification |

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

Weather: **enabled and PASS** since 2026-09-29 (Pacific `Weather/`; see WO-SRV).

**Migration evidence 2026-09-29** (`2 - RootRecord-Database/Logs/Migration/`): `g3-poller-realign-evidence-20260929T111731Z.md`, `g3-residual-path-survey-20260929T113523Z.md`, `g3-weather-archive-evidence-20260929T115429Z.md`, `g3-pre-reboot-checkpoint-20260929T120755Z.md` (post-reboot list in WO-SRV "Pre-reboot checkpoint 2026-09-29").

**More evidence 2026-09-29** (same folder): `g3-runtime-evidence-20260929T101550Z.md`, `g3-cutover-evidence-20260929T103720Z.md`, `g3-energy-plumbing-evidence-20260929T104618Z.md`, `g2-retire-aeyes-cam-evidence-20260929T105103Z.md`, `g3-dbroot-realign-evidence-20260929T105845Z.md`, `g3-poller-viewer-evidence-20260929T121959Z.md`, `g3-post-reboot-evidence-20260929T123313Z.md`, `g3-followups-evidence-20260929T124741Z.md`, `g3-npu-flm-evidence-20260929T125429Z.md` (addenda 03:02 and 03:29 HST), `g3-titlecase-rename-evidence-20260929T130752Z.md`. Per-test records: [07-testing](../07-testing/README.md).

**Documented without executing product migration:** full product/archive catalog (Paper, Nukkit, apps, mirrors); Automations G1 retirement; G0/G1 READMEs.

**Strategy:** close residual verification before build-mode expansion — see [Local Multi-Agent Team](./Local-Multi-Agent-Team-and-Migration-to-Build-2026-09-28.md).

---

*Index updated 2026-09-28 ~22:16 HST — team constitution doc linked.*

*Index updated 2026-09-29 ~03:45 HST — Testing folder (`Documentation/07-testing/`) and the full 2026-09-29 evidence list added.*

*Index updated 2026-09-29 ~13:40 HST — Old-Repo-Migration-Matrix linked; Geology collector + ports batch 1 test records in `07-testing/`. ~14:10 HST — Pending-Job-Registrations linked; breadth batch 4 test record. ~14:40 HST — G1-Scheduler-To-G3-Jobs-Map linked; breadth batch 5 test record (`07-testing/2026-09-29-old-repo-ports-breadth-batch5.md`); matrix now 35 / 22 / 33.*

*Index updated 2026-09-29 ~16:30 HST: new section "2026-09-29 afternoon" links US-Mainland-Server, the AWS trim + cloudflared and static-allowlist records, the AWS fallback rebuild and globe landing overlay proposals, the Root Monitor toggle-buttons record, Control-Panel-GTK and Android-Apps-Inventory. Current state and sign-offs: worklog section "State at pause, 16:25 HST".*

*Index updated 2026-09-30 01:29 HST: operator remaining-work list linked. Desk check after the 01:09 boot: Pacific stack up, River BLE live, Delta 2 dead and not transmitting.*
