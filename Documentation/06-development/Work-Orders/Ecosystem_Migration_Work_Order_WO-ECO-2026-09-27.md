# WORK ORDER — RootRecord Ecosystem Migration & Repository Foundation

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-ECO-2026-09-27 |
| **Date** | 2026-09-27 (HST) |
| **Status** | IN PROGRESS — Pacific runtime is live on the Ecosystem path (confirmed again 2026-09-30 01:24 HST). Remaining work is operator sign-off, not a broken cutover. See `Documentation/01-operations/2026-09-30-whats-left-for-alexander.md`. |
| **Owner** | RootRecord |
| **Related** | Library online; WO-SRV; domain wiring 2026-09-28 |
| **Updated** | 2026-09-30 02:35 HST — open items are the operator list, not a broken cutover. Root Monitor is the login window. |

**Scope:** Establish clean ownership boundaries between the local `RootRecord-Ecosystem` tree and independent GitHub repositories; migrate durable knowledge and runtime artifacts out of the legacy single-tree model.

---

## 1. Intent

The long-term shape:

```text
RootRecord-Ecosystem
├─ 0 - Master-Prompt          # governance / identity / architecture (boot path)
├─ 1 - Servers                # deployed runtime systems
├─ 2 - RootRecord-Database    # generated data + telemetry + media
├─ 3 - RootRecord-Website     # public surface
├─ 4 - RootRecord-Node        # future distributed nodes
└─ 5 - RootRecord-Library     # durable knowledge / docs / agent context
```

**Rule of thumb:**

| Kind of material | Home |
| --- | --- |
| Runnable code / services | `1 - Servers` → matching GitHub runtime repo |
| Generated data, logs, media | `2 - RootRecord-Database` (and weather DB repo where applicable) |
| Public presentation | `3 - RootRecord-Website` |
| Future node deployments | `4 - RootRecord-Node` |
| Decisions, history, agent context, work orders | `5 - RootRecord-Library` |
| Always-on agent bootstrap | `0 - Master-Prompt` |

---

## 2. Current GitHub Reality (as of 2026-09-28)

### 2.1 Online and in use

| Repository | Owner | Role |
| --- | --- | --- |
| **RootRecord-Library** | `RootRecord-Software-Solutions` | Durable knowledge, agent context, architecture sessions, ops logs, work orders |
| **RootRecord-Pacific-Solar-Server** | `RootRecord-Software-Solutions` | **Primary desk runtime** (Automations domain live; other domains importing) |
| **RootRecord-Database** | `RootRecord-Software-Solutions` | Generated data, telemetry & media — local `/home/rootrecord/RootRecord-Ecosystem/2 - RootRecord-Database` |
| **US-Mainland-Server** | `rootrecordsoftwaresolutions` | Continuity node |
| **RootRecord-Website** | `rootrecordsoftwaresolutions` | Public Next.js surface |
| **RootRecord-Weather-Database** | `rootrecordsoftwaresolutions` | Generated weather data & media |

### 2.2 Completed

- [x] Org repo Library online and synced
- [x] Org repo **RootRecord-Pacific-Solar-Server** online
- [x] Live runtime path: `…/1 - Servers/1 - RootRecord-Pacific-Solar-Server`
- [x] Domain folders + Automations core wired (poller, jobs, stack, Communications/network)
- [x] Poller confirmed active from Ecosystem path (2026-09-28)
- [x] Pacific source imports for Energy, A-Eyes, Github, Plumbing, and Telegram landed; runtime verification remains tracked under WO-SRV
- [x] `repos.conf` Pacific catalog row aligned to the Ecosystem path; Website/Mainland remain intentionally disabled
- [x] Master-Prompt `08-repository-and-file-links.md` authored (desk ownership table, 2026-09-29)

### 2.3 Transitional friction

- Current Pacific `jobs.py` active scheduler surfaces resolve to Pacific paths. `weather_poller` is enabled and was restarted 2026-09-29 22:04 HST. Geology and voice jobs stay off.
- Org placement: **Library + Pacific Server + Database** under `RootRecord-Software-Solutions`; other operational repos under `rootrecordsoftwaresolutions`
- Prior remote `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server` is legacy for Pacific runtime

---

## 3. Ownership Contract (working draft)

### RootRecord-Library

- **GitHub:** https://github.com/RootRecord-Software-Solutions/RootRecord-Library
- **Contains:** agent contexts, architecture notes, human operator logs, work orders, ADRs, guides, handoffs
- **Does not contain:** runtime services, live telemetry, secrets, generated databases

### RootRecord Pacific Solar Server (runtime)

- **GitHub:** https://github.com/RootRecord-Software-Solutions/RootRecord-Pacific-Solar-Server
- **Local (live):** `/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server`
- **Contains:** Automations (poller/jobs/stack), Communications (network/cloudflare + messaging shells), Weather helpers, domain shells (Energy, Security, System, Github, Geology)
- **Does not contain:** long-term documentation archives, library agent packs, bulk generated data

### US Mainland Server

- **GitHub:** https://github.com/rootrecordsoftwaresolutions/US-Mainland-Server
- **Local (target):** `1 - Servers/2 - RootRecord-US-Mainland-Server`

### RootRecord-Website

- **GitHub:** https://github.com/rootrecordsoftwaresolutions/RootRecord-Website
- **Local:** `3 - RootRecord-Website`

### RootRecord-Database + Weather Database

- **GitHub:** https://github.com/RootRecord-Software-Solutions/RootRecord-Database
- **Local / canonical:** `/home/rootrecord/RootRecord-Ecosystem/2 - RootRecord-Database`
- **GitHub weather publication:** https://github.com/rootrecordsoftwaresolutions/RootRecord-Weather-Database

### Master-Prompt

- **Local:** `0 - Master-Prompt`
- **Role:** first load for agents — answers *where does this go?*

**Boundary rule:** When ownership is ambiguous, prefer Library for decisions/history and Server for runnable code.

---

## 4. Migration checklist

### 4.1 Knowledge

- [x] Library repo online and auto-synced
- [x] Agent CONTEXT maps updated for Pacific path (2026-09-28)
- [x] WO-SRV / WO-CF updated for domain layout
- [x] Master-Prompt repository links section (`prompts/08-repository-and-file-links.md`, 2026-09-29)

### 4.2 Runtime

- [x] Pacific server live under `1 - Servers/…`
- [x] Automations core path-wired and operator-verified
- [ ] Import remaining out-of-scope domains one at a time (including Weather/Geology where separately authorized)
  - *Update 2026-09-29 ~13:40 HST:* **Geology** imported (LANDED, manual PASS, jobs gated OFF: `RR_GEOLOGY`, `RR_KILAUEA_CAMS`, `RR_VOICE_QUAKE`); old-repo batch 1 (sun times `RR_SUN_TIMES`, uptime log `RR_UPTIME_LOG`, MP4 converter on demand). Old-repo matrix: 27 migrated / 27 partial / 36 missing of 90 rows (as of 14:12 HST; was 24 / 28 / 38 at 13:50) — [Old-Repo-Migration-Matrix](../../00-architecture/Old-Repo-Migration-Matrix.md). Box stays open until the missing rows are ported or BLOCKED with sign-off.
- [x] `repos.conf` Pacific path alignment

### 4.3 Data / Website / Node

- [ ] Keep generated content out of Library and runtime git trees
- [ ] Website continues via existing mirror — `www.rootrecord.cloud` serves the AWS globe (200) as of 16:10 HST. The `website` sync row stays disabled. Real-browser check and a Vercel deploy are still open.
- [ ] Node: leave placeholder — superseded. Desk checkout is imported (139 tracked files, working tree clean 22:18 HST). AWS trim, tunnel, allowlist, and fallback Phase 2 are PASS. A real fallback and a relay send are still VERIFY PENDING. The `mainland` sync row stays disabled.
- [x] **Resolved 2026-09-29:** the active Pacific source paths use the canonical Ecosystem Database root `/home/rootrecord/RootRecord-Ecosystem/2 - RootRecord-Database`. The older `/home/rootrecord/Database/` tree is retained only where historical/runtime evidence or operator-controlled workflows still reference it; it is not the active Database authority. See WO-DATA for the boundary record. The poller source was corrected to this root in the latest Pacific sync; its live post-restart check remains part of WO-SRV.
  - *Desk check 2026-09-29 ~00:52 HST:* some active Pacific sources still hardcode the old root: plumbing `single-flight.sh` (`STATE_DIR`) and `flm-warmup.sh`; Energy `solar-gate-{status,arm,disarm}.sh`; `ble-owner.py` LOG/PID and `devices.conf` `ble_log`. The running poller log is also still at `/home/rootrecord/Database/Logs/Automations/`. Tracked in WO-SRV Next #1; see `2 - RootRecord-Database/Logs/Migration/g3-energy-plumbing-evidence-20260929T104618Z.md`.
  - *Update ~00:57 HST:* those plumbing, solar-gate, BLE-owner and `devices.conf` paths now use the canonical root (Pacific `87a6469`). Still on the old root: the poller (`run-poller.sh` `POLLER_LOG`; `rootserver_poller.py` `ENERGY_ROOT` and system-status), which needs a poller restart, and the `Github/scripts/common.sh` `DATABASE_ROOT` default.
  - *Update ~01:12 HST:* poller realigned + restarted, PASS (Pacific `d9f074b`); `common.sh` DATABASE_ROOT LANDED (`75d86f2`). Ignore rules for the BLE and poller logs added (Database `a05805a`) but BLOCKED — both are tracked (`git rm --cached` needs approval). Evidence `2 - RootRecord-Database/Logs/Migration/g3-poller-realign-evidence-20260929T111731Z.md`.
  - *Update ~01:37 HST:* remaining no-restart defaults LANDED (Pacific `58ee023`); live logs untracked (Database `eabe62e`); G2 retirements reverted, G2 code KEPT (skills `1dcee66`). **Residual path survey:** `2 - RootRecord-Database/Logs/Migration/g3-residual-path-survey-20260929T113523Z.md` (FX 4 files · MM 2 docs · KI 13 · ND 5). **Standing rule (Alexander, 2026-09-29):** never retire or delete G2/legacy code. "No live references" is not grounds — unimported automations (e.g. the older repo `rootrecordsoftwaresolutions/old`) may need it. Retirement happens only with Alexander's explicit sign-off.
  - *Update ~01:54 HST:* old-root data archived (move, not delete) to `Archive/Previous-Datasets/G2-old-root-20260929/`; Weather hooked in on Pacific + canonical `WEATHER/` (git-ignored). Evidence: `2 - RootRecord-Database/Logs/Migration/g3-weather-archive-evidence-20260929T115429Z.md`.
  - *Update ~02:01 HST — Ollama layout (Alexander's deliberate choice):* Database `AI/Ollama/{Modelfiles/{Production,Development,Archive},Config}` and `Logs/AI/Ollama/{Runtime,Errors,Pulls,Builds}`. **Symlink exception:** `~/.ollama/modelfiles` → `AI/Ollama/Modelfiles` and `~/.ollama/logs` → `Logs/AI/Ollama` are intentional; do not replace them. Ollama runs as the system service `ollama.service` (User=ollama, models in the service's own store, not `~/.ollama/models`) and logs to journald, so `Logs/AI/Ollama/` stays empty until something writes there. Git: `Runtime/`, `Errors/`, `Pulls/` contents ignored; `Builds/` and Modelfiles tracked; `.gitkeep` keeps the empty folders.
  - *Pre-reboot ~02:08 HST:* `store.py` canonical (`abc78b2`), `push-repo-once.sh` G2-pull reload removed (`abc78b2`), Pacific vendor canonical + READMEs (`99cc71e`, `662bf97`), relay retry fix `b3754fb` pending next start, weather ≈ 3 GB/day. Checkpoint + post-reboot list: WO-SRV "Pre-reboot checkpoint 2026-09-29"; snapshot `2 - RootRecord-Database/Logs/Migration/g3-pre-reboot-checkpoint-20260929T120755Z.md`.
- [x] **Database repo `.gitignore` — volatile runtime state excluded (2026-09-29 ~00:56 HST).** Added `/ENERGY/state/`, `/ENERGY/ports/`, `/GITHUB/plumbing/state/`, `*.pid` and `*.lock`, so pid, lock and state json files are not auto-committed to the Database repo every 5 s. Reasons: **privacy** (e.g. the single-flight holder file records the full inference command, prompt included) and **commit churn**. No tracked file matched, so nothing was untracked. Evidence: `2 - RootRecord-Database/Logs/Migration/g3-dbroot-realign-evidence-20260929T105845Z.md`.

---

## 5. Sync system (standing)

Catalog: Pacific `Github/scripts/repos.conf` (the `skills` row still points at the legacy `.ollama/skills` tree)

| id | enabled | mode | local (desk) | github_slug |
| --- | --- | --- | --- | --- |
| pacific | 1 | inplace | `…/1 - Servers/1 - RootRecord-Pacific-Solar-Server` | `RootRecord-Software-Solutions/RootRecord-Pacific-Solar-Server` |
| database | 1 | inplace | `…/2 - RootRecord-Database` | `RootRecord-Software-Solutions/RootRecord-Database` |
| library | 1 | inplace | `…/5 - RootRecord-Library` | `RootRecord-Software-Solutions/RootRecord-Library` |
| skills | 1 | inplace | `/home/rootrecord/.ollama/skills` (legacy G2 tree) | `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server` |
| website | 0 (disabled) | mirror | `/home/rootrecord/.ollama/skills/website/site` | `rootrecordsoftwaresolutions/RootRecord-Website` |
| mainland | 0 (disabled) | inplace | `/home/rootrecord/.ollama/skills/us-mainland-server` | `rootrecordsoftwaresolutions/US-Mainland-Server` |

Deploy standing rule: push → sync merge → `schedule-stack-reload` when runtime code is pulled.

---

## 6. Notes & constraints

- No force-push.
- Secrets stay out of git.
- Prefer structure over sprawl.
- Residual legacy runtime paths are retained only where the corresponding Pacific implementation has not yet passed required runtime verification and retirement criteria. For migrated functions, static source presence alone does not authorize legacy removal.

---

*Work order prepared 2026-09-27 HST. Updated 2026-09-28 HST after Pacific Automations domain wiring and live poller confirmation.*
## NPU prerequisite installation update — 2026-09-29

**2026-09-29 03:02 HST:** `llama3.2:3b` pre-pulled (2.7 GB) and kept as default; FLM warmup pmode `balanced`; relay replies opt-in (`RR_RELAY_REPLIES=0` default, Pacific `ebc32a7`).

**2026-09-29 02:56 HST — NPU/FLM PASS** (supersedes the pending note below): xrt-smi sees RyzenAI-npu6 (FW 1.1.2.64), `flm validate` OK, gated llama3.2:1b inference on the NPU in 1.04 s, parallel refused. Open: default model `llama3.2:3b` not downloaded; relay will reply via FLM once it runs. Evidence `2 - RootRecord-Database/Logs/Migration/g3-npu-flm-evidence-20260929T125429Z.md`.

The operator installed the documented AMD XDNA2/XRT prerequisite stack on the Pacific host: `amdxdna-dkms`, `libxrt-npu2`, and `libxrt2`. The host exposes `/dev/accel/accel0`, and `modinfo amdxdna` resolves the installed driver and firmware entries. The DKMS install reported a `BUILD_EXCLUSIVE` mismatch for kernel `7.0.0-34-generic`, so the NPU is **not yet runtime-verified**. A reboot and post-reboot validation are required before FastFlowLM can be marked installed/verified. No production deployment or legacy retirement is implied by this prerequisite installation.

**2026-09-29 03:24 HST:**
- Database top-level folders are now Title-case (`Energy`, `System`, `Weather`, `Github`, `RootRecord`, `Worklog`, `Intake`; Database `92bd69c`).
- FLM warmup is opt-in only after an OOM restart loop (a resident 3b model used about 10 GB); Ollama CLI calls use `--keepalive 0`.
- EcoFlow BLE is live again through the new `Pacific/Energy/.venv`; the cloud API values were stale. See WO-SRV for details.

**2026-09-29 ~03:45 HST — status summary (truth-gated):**
- Runtime inference is now `llama3.2:1b` **on demand** on the NPU (`run-infer.sh` starts `flm serve` per request and stops it on exit; Pacific `753168e`, `7000197`) — route **PASS**, own-session fix **VERIFY PENDING**. `llama3.2:3b` is installed but unused; it is no longer the default. The warmup is non-resident unless `FLM_WARMUP_RESIDENT=1` (`ff298b2`).
- Database Title-case rename **PASS** (Database `92bd69c`, Pacific `1368822`). Energy freshness **PASS** via `Pacific/Energy/.venv`; B1/B2 low (flagged).
- Relay replies are off by default (`RR_RELAY_REPLIES=0`); messages are consumed and will not be answered later.
- Per-test records with evidence and SHAs: [`Documentation/07-testing/`](../../07-testing/README.md). Full truth-gated table and open items: WO-SRV "Status summary — 2026-09-29 ~03:45 HST".
- Open items (not done): `OLLAMA_KEEP_ALIVE=0` in `ollama.service` BLOCKED (sudo); `*-telegram` models missing (replies BLOCKED until Alexander opts in); timelapse after 05:00 HST VERIFY PENDING; Energy arm/disarm + AC hardware tests need approval; B1 physical check; weather retention PROPOSED; Weather repo decision; ON_BOOT-only weather/relay (no mid-session recovery); 27 dormant G2 old-root files KEPT; `npu-status.sh` G2-only (optional copy); security items unremediated (camera stills in public Database repo, `CONNECTION.json` in Pacific history `6328af6`, G2 tracking `a-eyes/store/CONNECTION.json`). Canonical camera path: Pacific `Security/Cameras/`.

## Old-repo migration pass — 2026-09-29 ~13:12–13:45 HST

- Survey of G1 `Solar-Pacific-RootRecord-Server-Old` and G0 `old` (read-only shallow clones in `/tmp`, deleted afterwards; nothing written to either repo) → [Old-Repo-Migration-Matrix](../../00-architecture/Old-Repo-Migration-Matrix.md): **24 migrated · 28 partial · 38 missing** (90 rows; 14 touched this pass, as of 13:50 HST).
- Ported this pass (all LANDED, manual PASS, periodic jobs gated OFF): Geology collector, Kīlauea cams, quake backfill, earthquake voice report, sun times, uptime log, MP4 converter, hurricane desk + Kīlauea voice reports (text), G0 nearest-location quake tag. Details in WO-SRV "Geology + old-repo migration pass".
- BLOCKED (need Alexander): deliveries (Telegram/Discord/speakers), OBS, log-cleanup (deletes), actuation, cloud keys/spend, load-categories field map, fs-index / python-drop-runner / broadcast scope, Hawaiʻi news target.
- Addendum ~13:46 HST: voice `hurricane_desk` + `kilauea_report` LANDED (text PASS, gated `RR_VOICE_HURRICANE` / `RR_VOICE_KILAUEA`). jobs.py registrations (7, all OFF) are a **sign-off item** under the jobs.py standing rule; blocks in Database `Logs/Migration/migration-jobs-py-additions-20260929.md`.
- Addendum ~14:10 HST (breadth batch 4): web facts, live-wx chat lines, host net/security desks, solar / security / bandwidth voice desks LANDED (smoke PASS); Hawaiʻi news ported but 0 posts (FAIL on content). Jobs PROPOSED only ([Pending-Job-Registrations](../../00-architecture/Pending-Job-Registrations-2026-09-29.md)). Matrix now **27 migrated · 27 partial · 36 missing** (90 rows; 23 touched). [Record](../../07-testing/2026-09-29-old-repo-ports-breadth-batch4.md).
- Addendum ~14:40 HST (breadth batch 5):
  - Voice text fixes and Hawaiʻi news seeds: news now **278 posts**.
  - LANDED with smoke PASS: HLS fetcher, `official_weather` and `boot_brief` voice reports (text), report board and catch-up, load categories, global hurricane board, host hardware, speech scrub, and the G1 scheduler map.
  - Jobs PROPOSED only (`weather_official_hls` (`RR_OFFICIAL_HLS`), `voice_official_weather` (`RR_VOICE_OFFICIAL`), `voice_boot_brief` (`RR_VOICE_BOOT`, ON_BOOT), `reports_board_catchup` (`RR_REPORT_BOARD`), `weather_hurricane_global` (`RR_HURRICANE_GLOBAL`)).
  - Matrix **35 / 22 / 33**; nothing clean left to port.
  - [Record](../../07-testing/2026-09-29-old-repo-ports-breadth-batch5.md).
- Legacy sources **KEPT** (standing rule). Backups: `/home/rootrecord/Database/GITHUB/migration-hurricane-desk.bak-20260929-133959/`, `/home/rootrecord/Database/GITHUB/migration-geology.bak-20260929-131652/`, `/home/rootrecord/Database/GITHUB/migration-old-repos.bak-20260929-133118/`. Breadth backup: `/home/rootrecord/Database/GITHUB/migration-breadth.bak-20260929-135720/`.

## State at pause — 2026-09-29 16:25 HST

- **§4.2 Runtime:** the old-repo matrix is now **35 migrated / 22 partial / 33 missing** (supersedes the 27 / 27 / 36 note in §4.2). All ports are gated OFF; their jobs are PROPOSED in [Pending-Job-Registrations](../../00-architecture/Pending-Job-Registrations-2026-09-29.md).
- **§4.3 Node (US-Mainland / AWS):** no longer only a placeholder. Desk checkout imported (**PASS**). AWS feed trim + cron, tunnel (`www` 200) and the static allowlist: **PASS**. AWS fallback Phase 2 LANDED on the trimmed-micro t3.micro profile (908 MB RAM), with Root Monitor write mode: **PASS**. A real fallback and a relay send are VERIFY PENDING. Details: [US-Mainland-Server](../../00-architecture/US-Mainland-Server.md).
- **§4.3 Website:** `www.rootrecord.cloud` serves the AWS globe (200) with landing overlay v2 (LANDED 16:10 HST; real-browser check VERIFY PENDING). Vercel untouched. The RootRecord-Cloud staging build passed on the desk; no deploy.
- **New ecosystem folder:** `6 - Android Development` (9 apps, 80.7 MB). Not a git repo, not in `repos.conf`. Build VERIFY PENDING. [Inventory](../../00-architecture/Android-Apps-Inventory.md).
- **§5 sync table:** the `mainland` row is still disabled (sign-off to repoint + enable). The Mainland checkout is in this umbrella and was clean at 22:18 HST (139 tracked files). Do not enable the row inside this snapshot.
- Sign-offs: [worklog "State at pause, 16:25 HST"](../../01-operations/0%20-%20Human%20Operator%20Work%20Logs/2026-09-29%20System%20Operator%20Worklog%20%E2%80%94%20Overnight.md#state-at-pause-1625-hst-2026-09-29).
