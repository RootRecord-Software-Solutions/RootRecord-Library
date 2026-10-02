# Database logs and reports — operator handbook

How RootRecord keeps logs and reports on disk, what git actually publishes, who writes which file, and what an AI or a person is allowed to change without guessing.

Nothing in this page starts a service, sends a message, spends money, or turns a job on.

**Written:** 30 September 2026, from GitHub trees (Database `main`, Pacific `jobs.py` and report scripts, Ecosystem `Pull.sh` / `Push.sh` / `repos.conf`) plus Library architecture already in this repo. Desk clocks in the sources are Hawaii time (`Pacific/Honolulu`, HST, UTC−10, no DST).

**Desk path for the data tree:**

```text
/home/rootrecord/RootRecord-Ecosystem/2 - RootRecord-Database
```

That folder is the live Database. GitHub `RootRecord-Software-Solutions/RootRecord-Database` is the published layout of the same tree, minus ignored runtime.

---

## 1. What “the database” is

It is a **git-backed folder tree**, not a single SQL server.

Pacific code decides what runs. This tree decides **where bytes go**. Library holds the writing about it. That split is the Database README and WO-DATA, not a metaphor.

| Layer | Repository | Role |
| --- | --- | --- |
| Runtime | `RootRecord-Pacific-Solar-Server` | Jobs, poller, report scripts. **No `Logs/` directory on the server.** |
| Data | `RootRecord-Database` | `Logs/`, `Reports/`, `Worklog/`, domain last-files, media, sqlite stores |
| Docs | `RootRecord-Library` (this repo) | Handbooks, work orders, human session logs |
| Umbrella | `RootRecord-Ecosystem` | One `.git` at `/home/rootrecord/RootRecord-Ecosystem`. Folders `1 - Servers/…`, `2 - RootRecord-Database`, `5 - RootRecord-Library` |

On the desk those three named folders sit **inside one git root**. They are not three clones you `cd` into and `git pull` as separate repos. Pacific `Github/scripts/repos.conf` publishes them with `mode=mirror` from Database `GITHUB/worktrees/<id>` so the umbrella does not grow nested `.git` directories (a gitlink). Database README: “This directory is inside the umbrella git root. It does not have its own `.git`.”

Ecosystem `Pull.sh` / `Push.sh` still loop those same three paths and **error if `.git` is missing**. They log under Database `Logs/Github/Manual/`. They are **manual only**. Automatic authority is Pacific job `github_sync_all` (`Github/scripts/sync-all.sh`), signed as Option B on 29 September 2026. Do not schedule Pull/Push.

`4-data/README.md` in this Library still lists `/home/rootrecord/Database/` as “live desk writes.” G3 verification (29 September 2026) says that old root is **not** a data path any more: it holds `GITHUB/` backups/worktrees and a README. Old data was archived under Database `Archive/Previous-Datasets/G2-old-root-20260929/`. Treat the Ecosystem path above as current.

### 1.1 SQL that exists, and what it is not

Several **sqlite** files live *inside* this tree. None of them is “the Database.”

| Store | Path (under Database) | Git |
| --- | --- | --- |
| Energy layers | `RootRecord/rootrecord.db` and `RootRecord/layers/*.db` | Ignored (`/RootRecord/`) |
| Host samples | `System/system.db` | Listed in umbrella skip-autocommit |
| Geology backfill | `Geology/Earthquakes/*.db` | Ignored |
| News | `Reports/News/**/*.db` | Ignored |
| Grok usage ledger | `Reports/AI-Usage/` (runtime; folder marker tracked) | Ignored contents |
| Context session | `ContextSession/*.db` | Ignored |
| US-States weather | under `Weather/` | Whole `Weather/` ignored; weather also has a **separate** `RootRecord-Weather-Database` working tree |

MySQL appears only as **desk facts** (`System/MysqlDesk/`, WO-MIG-28): a last JSON plus a log line. That is not the log store. Postgres is not the layout authority in these repos.

`RR_DATABASE_ROOT` (default the Ecosystem Database path) is how scripts point at this tree in tests. Do not invent a second root.

### 1.2 What is committed vs runtime-only

Database `.gitignore` is the contract. High-churn streams stay on disk; archives or `.gitkeep` keep the folders in git.

**Never commit (selected; read the file for the full list):**

- Binary media: `*.png` `*.jpg` `*.wav` `*.mp4` … (desk screenshots under `Logs/Migration/*.png` called out twice)
- `/Energy/state/`, `/Energy/ports/`, `*.pid`, `*.lock`
- Live poller/BLE/relay: `/Logs/Energy/ava-ecoflow-ble.log`, `/Logs/Automations/automations_current.log`, `/Logs/Communications/council-relay.log`
- FLM/Ollama runtime logs that may hold prompts; `inference_current.jsonl`; `routing_current.jsonl`
- Held Telegram text (`Logs/Communications/Relay-Inbox/`, Inbox copies)
- Whole `/Weather/` (belongs with the weather database tree)
- Night-sleep, playback, Cloud TTS, Site, Discord, MysqlDesk, PathIndex, CodeReview, River-Car runtime dirs
- Economy-Brief, CloudNarrative, AI-Usage **contents** (`.gitkeep` stays)
- `/Logs/Reports/News/`, US-States and CountryLocations weather logs
- `/Archive/Previous-Datasets/*/*` except each dataset `README.md`

**Usually tracked:** domain READMEs, `.gitkeep` layout, Migration evidence markdown, hourly `Logs/Automations/Archive/automations_YYYY-MM-DD_HH00.log`, AI processing report markdown under `Logs/AI/Reports/`, Generated report `_current.md` plus Archive, Worklog segment markdown (but see skip-autocommit), Geology `*-last.json` and Daily JSONL.

Pacific `Github/scripts/ecosystem-skip-autocommit.txt` extra-blocks the **umbrella** from auto-committing, among other paths:

```text
2 - RootRecord-Database/Worklog
2 - RootRecord-Database/Logs
```

plus Energy samples/soc/watts and System sample/sqlite trees. Intentional commits of other Database paths can still sync. Live telemetry is meant to stay on the desk.

Database `.gitignore` also ignores `/System/control-panel/`. That is where Root Monitor writes `automation-overrides.json` and `power-automations.json` (1 October 2026). They are desk state, not a published log. The public service-window file is Pacific `Website/Home/service-notice.json`, which the website mirror does publish. Contract: [Desk automations and service windows](../Documentation/11-Runtime-Jobs-and-Control/Desk-Automations-and-Service-Windows.md).

---

## 2. Folder map (what is actually on GitHub)

Database top-level on `main` (30 September 2026): `AI`, `Advertising`, `Communications`, `ContextSession`, `Energy`, `Geology`, `Logs`, `Media`, `Products`, `Reports`, `Security`, `System`, `Website`, `Worklog`, plus `.gitignore` and README.

The Database README’s Logs sketch (`Automations`, `Energy`, `Communications`, `Network`, `System`, `Weather`, `Github`, `Security`) is **incomplete**. The live `Logs/` tree also has AI, Advertising, ContextSession, Geology, Media, Migration, Products, Reports, Website.

### 2.1 `Logs/` — stream of what just happened

Domain folders. Current files at the domain root (or a named subfolder). Dated history in `Archive/` when that policy exists.

| Folder | What is there (verified) | Writer (Pacific unless noted) |
| --- | --- | --- |
| `Logs/Automations/` | Live `automations_current.log` (gitignored). `stack_reload_current.log`. Hourly `Archive/automations_YYYY-MM-DD_HH00.log` | Poller / `POLLER_LOG`. Job `automations_log_hourly_archive` → `archive_automations_log_hourly.sh`. Stack reload → `STACK_RELOAD_LOG` |
| `Logs/AI/` | `Inference/inference_current.jsonl` (ignored); daily `Archive/inference_YYYY-MM-DD.jsonl` when rotate runs. `Reports/ai-processing-report_current.md` + Archive. `FLM/`, `Ollama/{Runtime,Errors,Pulls,Builds}`, `Routing/` | `run-infer.sh`, `ai-log-rotate.sh`, `ai_processing_report.py` (job gated `RR_AI_REPORT`) |
| `Logs/Energy/` | BLE log ignored. `Archive/` README states an older daily-compress policy (see §6) | EcoFlow readers |
| `Logs/Communications/` | `council-relay.log` ignored. Slack `poll.log`. BruceStats jsonl. Empty markers for CouncilHealth/Persona/Quake, MetaAI, Cloudflare-Workers. Relay-Inbox / Inbox READMEs only | Relay, Slack poller, gated communications jobs |
| `Logs/Github/Manual/` | `pull-YYYYMMDD-HHMMSS.log`, `push-…` | Ecosystem `Pull.sh` / `Push.sh` |
| `Logs/Github/Archive/` | Placeholder README | — |
| `Logs/Migration/` | Evidence markdown (`g3-*-evidence-…`, geology, jobs.py additions). PNGs ignored | Migration agents; **historical**, not a live writer |
| `Logs/Reports/` | `Late-Final/late-final.jsonl` (tracked sample). `.gitkeep` for AI-Usage, CloudNarrative, Economy-Brief. News logs ignored | Matching Reports scripts |
| `Logs/System/LogRetention/` | Dry-run reports `log-retention_dry-run_YYYY-MM-DD_HHMM.md` | `log_retention.py` |
| `Logs/Weather/Retention/` | Weather retention dry-run markdown | `weather-retention.py` |
| `Logs/Weather/RadarZip/` | `radar_zip.log` | `weather_radar_zip` |
| `Logs/Media/MorningBootReplay/` | `replay.log` | Morning boot replay (gated) |
| `Logs/Website/` | Empty until Vercel token **and** `RR_VERCEL_BUILDS=1` | `vercel_builds.py` — missing token does not write |
| `Logs/Advertising/` | README: run lines only if a run needs one; snapshots live under `Advertising/` | `adsense_eod` / `admob_eod` (do not invent a server `Logs/`) |
| `Logs/ContextSession/` | README: CLI prints JSON; **does not write a log file** | WO-MIG-43 |
| `Logs/Geology/Earthquake-Discord/` | `.gitkeep` | Gated Discord post |
| `Logs/Network/`, `Logs/Security/`, `Logs/Products/` | Archive READMEs / `.gitkeep` | Domain jobs as they land |
| `Logs/Mainland/` | Named in Library test notes for AWS fallback deploy log; not in the GitHub Logs listing above | AWS fallback on the desk |

**Naming patterns in use (do not invent a fourth):**

| Pattern | Example |
| --- | --- |
| Live tail | `*_current.log`, `inference_current.jsonl` |
| Hourly cut | `automations_YYYY-MM-DD_HH00.log` |
| Daily JSONL | `inference_YYYY-MM-DD.jsonl` |
| Dry-run report | `log-retention_dry-run_YYYY-MM-DD_HHMM.md` |
| Manual git | `pull-YYYYMMDD-HHMMSS.log` |
| Migration evidence | `g3-titlecase-rename-evidence-20260929T130752Z.md` (UTC `Z`) |
| JSONL append | `late-final.jsonl`, `bruce-stats.jsonl` |

**Severity / levels:** there is no syslog facility across `Logs/`. The poller log uses job `RUN` / `FAIL` / `OK` style lines (`FAIL` is what template fill and work-order generators grep). AI JSONL uses `exit_code`, not INFO/WARN. Do not add a logging framework without a work order.

Root Monitor’s header **log Ns** is seconds since `automations_current.log` was written. A climbing number means the poller log went quiet. Closing Root Monitor does **not** stop the poller.

`https://rootserver.rootrecord.cloud/` is the poller via tunnel, not a public website. Do not create `3 - RootRecord-Website` or bind port 3001. Website **logs** are Database `Logs/Website/` (Vercel failed-build records), not that URL.

### 2.2 `Reports/` — shaped output

Code lives in Pacific `Reports/`. Data lives in Database `Reports/` (and sometimes Ecosystem `test-reports/`).

| Database path | Role | Git | Job / gate |
| --- | --- | --- | --- |
| `Reports/Generated/` | Four Library **templates** filled from measured data: worklog session, checkpoint, event-action (AI inference), work-order draft. Plus `template-fill-validation_current.json`, `_rejected.md`, `Archive/<name>_YYYY-MM-DDTHHMM.md` | Tracked drafts | `template_reports_daily` at 18:40 HST. **Off** unless `RR_TEMPLATE_REPORTS=1` in the poller env **at poller start** |
| `Reports/Late-Final/` | `last.json` status of the 23:30 second-chance late roll-up | `last.json` is on GitHub | `voice_late_final_report` / `late_final.py`. Off unless `RR_VOICE_LATE_FINAL=1` |
| `Reports/Economy-Brief/` | Daily markdown `economy-brief-YYYY-MM-DD.md` from MySQL facts + Kīlauea last JSON. **Never a `$`.** Discord send refuses unless `RR_ECONOMY_BRIEF_SEND=1`, and even then the script does not post | Contents ignored | Script exists. Pacific Reports README: job **PROPOSED** `RR_ECONOMY_BRIEF` 15:00, **not in `jobs.py`** as of this read |
| `Reports/CloudNarrative/` | Prompt packages + narrative text over existing voice templates. Does not replace `voice_reports.py`, Kokoro, or send | Contents ignored | `cloud_narrative.py`. README: `cloud_narrative_dry_run` off unless `RR_CLOUD_NARRATIVE=1`, command `--dry-run`. **That id was not in Pacific `jobs.py` on this read** — treat as operator-gated / unregistered until Alexander says otherwise. Live API needs `RR_CLOUD_NARRATIVE_SPEND=1` and `--spend` |
| `Reports/AI-Usage/` | Local token ledger + `last-summary.json`. **No network** | Contents ignored | `ai_usage_report` hourly, off unless `RR_AI_USAGE=1` |
| `Reports/News/` | Hawaiʻi / state / global news sqlite + last JSON | sqlite ignored; Hawaiʻi summary may stay trackable | Collectors exist. `reports_hawaii_news` / state / global jobs **PROPOSED** (`RR_HAWAII_NEWS`, `RR_STATE_NEWS`, `RR_GLOBAL_NEWS`). Not enabled here |
| `Reports/board/` | `daily-reports-due.json` due ledger | Runtime | `report_board.py`. Job `reports_board_catchup` PROPOSED (`RR_REPORT_BOARD`) |

**Generated vs curated:**

- **Generated** (`Reports/Generated/`, `template_fill.py`) copies Library `Documentation/01-Operations/Templates/` structure. It **never writes into the Library** (`guard_out()`). A person copies a reviewed file into `01-Operations/` or `Work-Orders/drafts/` by hand. The work-order output is a draft, not on the active index.
- **Curated briefs** (Economy-Brief, CloudNarrative, voice roll-ups) are domain products. Voice markdown often lands under Ecosystem `test-reports/Voice/` (`RR_VOICE_REPORT_OUT`), not under `Reports/Generated/`. Late-Final **runs** that same `late_report` template; it does not invent a fifth template.
- **AI processing report** is a third home: Database `Logs/AI/Reports/` (metadata only: lengths, never prompt text). Architecture: Library `Documentation/../Documentation/10-AI-and-Agent-Runtime/AI-Processing-Logs-and-Reports.md`. Older notes also mention non-git `test-reports/AI-Processing/`; the job description writes the Database Logs path. If both exist on disk, do not merge them without a work order.
- **Human narrative** stays in Library `Documentation/01-Operations/0 - Human Operator Work Logs/`. That is not Database `Reports/`.

`Logs/Reports/` is **run logs for report jobs**, not the reports themselves.

### 2.3 `Worklog/` — machine file activity, not the human diary

Pacific `Reports/scripts/worklog_once.sh` → `worklog_lib.sh`. Job `worklog_scan` is **enabled**, about every 90 s.

| File | Role |
| --- | --- |
| `worklog_current.md` | Live segment. Path/size/mtime only. `NEW_FILE` / `MOD_FILE` / `NEW_DIR` / `DELETED` plus optional `domain=` |
| `YYYYMMDD-HHMMSS-YYYYMMDD-HHMMSS.md` | Closed hour (or longer) segments |
| `.last_scan` `.hour_start` `.segment_start` `.seen_index` `.seen_dirs` `.poller.pid` | Scanner state |

Scope is **full `/home/rootrecord`**, pruned (models, snap, cache, git blobs). Directory mode **700**, current file **600**. It skips its own `Worklog/` tree, `.git`, `Github/`, private Desktop trees Alexander named, and secrets via scrub against `master-key.env`. It does **not** record keystrokes, clipboard, or file contents.

`domain_tag` still has a `*/Database/` pattern from the old root. New paths are `…/2 - RootRecord-Database/…`. Tags can be empty on Database files; that is a known leftover, not a reason to rename folders.

This is **not** the Library session worklog. Job `reports_daily_roll_up` (18:30 HST, enabled) counts today’s Worklog lines into:

```text
5 - RootRecord-Library/Documentation/01-Operations/0 - Human Operator Work Logs/
YYYY-MM-DD System Operator Worklog — Session auto.md
```

Measured counts only. No invented prose.

Job `reports_weekly_archive` (19:00 HST, enabled) moves **Library** human `YYYY-MM-DD …md` files older than this HST week’s Monday into `Documentation/01-Operations/Archive/YYYY-Www/` (`TZ=Pacific/Honolulu`). It does not touch Database `Worklog/` and does not touch Work-Orders.

---

## 3. Boundaries (do not collapse these)

| Name | Is | Is not |
| --- | --- | --- |
| Database `Logs/` | Append-only operational streams + dry-run reports | Pacific source. Do not add `Logs/` under the server tree |
| Database `Reports/` | Shaped products and ledgers | The poller log. Not Library publication |
| Database `Worklog/` | File mtime scanner | Human “what we decided.” Not Root Monitor |
| Library `01-Operations/` | People and Session auto | A dump of `automations_current.log` |
| Ecosystem `test-reports/` | Non-git smoke / voice / template outputs in some jobs | Canonical Database layout |
| Domain last-files (`Energy/soc`, `System/last`, …) | Current measurements | Logs. Worklog *notices* them as MOD_FILE |
| Weather reports under `Weather/Hawai'i/` | County/HFO markdown the weather daemon writes | Database `Reports/` |

Pacific Reports README: Reports **aggregates and shapes**. Communications, Website, cameras **own capture and delivery**. Do not fold those domains into `Reports/` to make the tree look tidy.

---

## 4. Who writes (desk jobs)

Poller user unit `rr-rootserver-poller` reads `Automations/scripts/jobs.py` **once at start**. Changing `enabled` or an `RR_*` env does nothing until the next poller start. Alexander names that restart. Do not restart because a log looks stale.

### 4.1 On by default (logs / reports related)

| Job id | When | Writes |
| --- | --- | --- |
| (poller itself) | Always while the unit is up | `Logs/Automations/automations_current.log` |
| `automations_log_hourly_archive` | Hourly | Copy current → `Archive/automations_YYYY-MM-DD_HH00.log`, then truncate current. Empty current → no-op. `flock` |
| `worklog_scan` | ~90 s | `Worklog/` |
| `github_sync_all` | Periodic | Git; skip-autocommit keeps Logs/Worklog off the umbrella |
| `reports_daily_roll_up` | 18:30 HST | Library Session auto.md |
| `reports_weekly_archive` | 19:00 HST | Library ops archive week folder |

### 4.2 Present in `jobs.py`, default **off** (need Alexander + usually `RR_*` and a poller start)

| Job id | Gate | Writes |
| --- | --- | --- |
| `log_retention` | `enabled: False`; command **`--dry-run`** at 04:20 | `Logs/System/LogRetention/` + `System/LogRetention/log-retention.json`. **`--apply` on live Logs refuses unless `RR_LOG_RETENTION_APPLY=1`**. Separate sign-off |
| `weather_retention` | False; `--dry-run` at 00:30 | `Logs/Weather/Retention/` + moves only on `--apply` (not signed) |
| `ai_processing_report_hourly` | `RR_AI_REPORT=1` | rotate JSONL + AI processing report |
| `ai_usage_report` | `RR_AI_USAGE=1` | `Reports/AI-Usage/` |
| `template_reports_daily` | `RR_TEMPLATE_REPORTS=1` at 18:40 | `Reports/Generated/` (and historically `test-reports/Templates/` — follow the live script paths) |
| `voice_*_report` / `voice_late_final_report` | `RR_VOICE_*` family | Voice markdown (often `test-reports/Voice/`); Late-Final `last.json` + `Logs/Reports/Late-Final/late-final.jsonl` |
| Communications, news, Vercel, Discord, Slack, geology extras, … | matching `RR_*` | Matching `Logs/<Domain>/` |

Do not set `RR_*`, Telegram replies, voice/speakers, or spend flags unless Alexander names that flag.

Work orders that **propose** a `jobs.py` block (economy brief, cloud narrative, Hawaii news, report board) are not a license to paste them. Standing rule: `jobs.py` only on his request or an accepted WO, copy from TEMPLATE, leave `enabled` false.

### 4.3 Root Monitor

Reads files the stack already writes (Energy/System JSON, automations log, systemd, `/proc`). It does not append Database logs except:

- **Settings:** confirm → backup → atomic write. No auto-restart.
- **AWS Fallback** in `write` mode: one flag file on AWS after confirm.

On/off controls are labeled buttons (`Name: On` / `Name: Off`), not switches.

Batteries: **B1** = River 2 Pro (live pack). **B2** = Delta 2 (often quiet / dead; a waiting read is normal). **B3** = laptop battery, not a third EcoFlow.

---

## 5. Lifecycle: create → write → review → prune

### 5.1 Create a new log domain

Match work orders from waves A–G (Slack, News, NightSleep, …):

1. **One Title-case folder name** in all three places that need it: Pacific package, Database data dir if any, `Logs/<Domain>/` or `Logs/<Parent>/<Name>/`.
2. No lowercase twin. No symlink. No `Logs/` on Pacific.
3. Script default `RR_DATABASE_ROOT` → Ecosystem Database path.
4. `.gitignore` the runtime file **in the same change** if it is high-churn, secrets, sqlite, or last-json. Keep `.gitkeep` or README so git holds the directory.
5. One line per run is enough for most jobs. Do not print DSNs, tokens, prompt text, or Telegram bodies.
6. Job block: copy TEMPLATE in `jobs.py`, `enabled` false, do not restart the poller.
7. Prove with a temp `RR_DATABASE_ROOT` when the WO says so. Do not `unlink` live logs to “clean up.”

### 5.2 Write

- Append. Prefer flock on hot files (`inference_current.lock`, automations archive lock).
- Timestamps: HST for operator-facing names (`date` / `ZoneInfo("Pacific/Honolulu")`). ISO with `-10:00` in JSON. UTC `Z` only where migration evidence already used it.
- AI inference: lengths only (`prompt_chars` / `reply_chars`). FLM stdout goes through `flm-log-redact.awk` unless `FLM_LOG_REDACT=0`.
- Worklog: path/size/mtime. Scrub `master-key.env`.

### 5.3 Review

- Tail `automations_current.log` on the desk (it is not on GitHub).
- Hourly Archive is what `github_sync` can see for the poller stream.
- Generated reports: read `_current.md` + validation JSON. Copy to Library by hand after a person agrees. Never auto-promote a work order.
- Session auto.md is counts. Overnight human worklogs are a different file.

### 5.4 Rotate (live, signed)

| Mechanism | What | Delete? |
| --- | --- | --- |
| `archive_automations_log_hourly.sh` | Hourly copy + truncate live poller log | No |
| `ai-log-rotate.sh` | Move yesterday’s JSONL lines to `Archive/` | No (move lines) |
| Template fill | Previous `_current` → `Archive/` when **content** changed | No |
| Worklog segments | New `worklog_current.md` after hour mark | Old segment stays as dated md |
| `weekly_archive_logs.sh` | Library human logs → week archive | No (`git mv` when Library has `.git`) |

`Logs/Energy/Archive/README.md` still describes **daily compress at boot, weekly zip, monthly zip**. Automations Archive README says **no automatic deletion** until a retention policy is approved. Treat the Energy README as **legacy intent**, not the live poller policy. Do not start zip jobs from that README.

### 5.5 Prune / archive (gated)

`System/LogRetention/scripts/log_retention.py` (WO-MIG-41, COMPLETE as a **dry-run** tool):

- Scans only `2 - RootRecord-Database/Logs/`
- Log-like names: `.log` `.out` `.log.gz` `.log.N` `.log.old`. **Skips `.jsonl`**
- Live writers (`*_current.log`, undated active `.log`) stay
- Dated/rotated older than **7 days** → move candidates
- Live `.log` over **10 MB** → copytruncate candidate (keep 5, like weather)
- Default `--dry-run`. Would-delete count must stay **0**. Never `unlink` / `rmdir` / `rmtree`
- `--apply` moves to `Archive/Previous-Datasets/Logs-<YYYYMM>/` mirroring the path under `Logs/`
- Dry-run on live tree 30 September 2026: 46 files scanned, **would move 0**, copytruncate 0, delete 0

`weather-retention.py` is the same shape for weather **data**, not this handbook’s log tree. Job stays `--dry-run`. Do not switch either job to `--apply` on live trees without a named sign-off.

Old Ava `log-cleanup` **unlinked** files. That body is not restored. Do not port it.

---

## 6. Maintenance rules (safe change)

**Do**

- Put new log files under Database `Logs/<existing or WO-named domain>/`
- Gitignore the hot file in the same PR as the writer
- Leave `.gitkeep` so empty dirs survive clone
- Keep FLM/Ollama/inbox/relay text local
- Use `nice -n 10` as existing jobs do
- Compile / `bash -n` after script edits (Teaching Desk)

**Do not**

- Enable `RR_*`, Telegram replies, Kokoro/`aplay`, or `--spend` / `--send` / `--apply` on live data
- Restart poller, relay, or cameras to “pick up” a gitignore
- Create a website tree or treat `rootserver.rootrecord.cloud` as the site
- Retire `/home/rootrecord/Database/`, skills trees, or dual Title-case folders unless Alexander names that tree
- Commit `automations_current.log`, inference JSONL, BLE logs, sqlite, Weather/, or Previous-Datasets dumps
- Write secrets into Migration evidence or Library guides
- Duplicate Ecosystem Master-Prompt or `5 - RootRecord-Library` into this handbook; this page is the operator map, those trees are copies/context
- Collapse Worklog, Logs, and Reports into one folder because names overlap

**Alexander-only (say so, then stop)**

- Poller restart
- `RR_LOG_RETENTION_APPLY=1` or live `--apply`
- Registering or enabling jobs in `jobs.py`
- Cloud narrative spend, economy Discord send, Vercel token use
- Any delete of live Ecosystem files
- Changing skip-autocommit so Logs start publishing to the public umbrella

---

## 7. Failure modes (seen in these repos)

| Symptom | Likely cause | What not to do |
| --- | --- | --- |
| Empty `Logs/Website/` or Advertising | Token missing or gate off; README says no file | Do not invent a log to “fill” git |
| Clone missing live logs | gitignore + skip-autocommit | Do not `git add -f` the current poller log |
| `Pull.sh` “Missing git repository” | Nested folders have no `.git` (by design) | Do not `git init` inside Database |
| Umbrella gitlink / dirty submodule | Nested `.git` appeared | Mirror mode exists to prevent this |
| Duplicate reports (`test-reports/` vs `Reports/Generated/` vs `Logs/AI/Reports/`) | Jobs grew three output homes | Do not copy files between them to “sync” |
| Worklog huge / disk growth | Full-home scan every 90 s; sqlite WAL under `~/.local` shows up | Do not disable `worklog_scan` without him; do not log Github/ or Worklog into itself (already skipped) |
| `log Ns` climbing in Root Monitor | Poller quiet or writing elsewhere | Do not assume closing the window stopped it |
| Quiet B2 / Delta 2 `WAITING` | Pack does not transmit | Do not schedule a drive test |
| Clock skew in names | Mix of local `date`, HST zoneinfo, UTC `Z` | Compare with `-10:00` JSON, not UTC, for same-day ops |
| Gitignore “swallowing” a new domain | Pattern like `/Logs/Reports/News/` or `/Weather/` | Check `git check-ignore -v` on the desk before assuming a writer is broken |
| Template reports missing | Gate off **or** poller started before the env was set | Do not restart to experiment |
| Late-Final `result: ran` but voice off | Script is text-only (`--no-voice`); night-sleep may skip | Do not enable speakers to “finish” the report |
| News sqlite absent on GitHub | Ignored by design | Data is on the desk |

Energy samples under `Energy/samples/` **are** committed in bulk (hundreds of `read-delta2-*.json`). That is measurement data, not `Logs/`. Skip-autocommit tries to keep new sample churn off the umbrella. Do not “clean” samples by deleting Logs.

---

## 8. Commands that only look (when you are on the desk)

These do not start the poller. They still read private files. Do not paste tails that contain tokens into git.

```bash
DB="/home/rootrecord/RootRecord-Ecosystem/2 - RootRecord-Database"
PAC="/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server"

# Live poller log (local only)
tail -n 80 "$DB/Logs/Automations/automations_current.log"

# Hourly archives that git may see
ls "$DB/Logs/Automations/Archive" | tail

# Worklog head
head "$DB/Worklog/worklog_current.md"

# Retention dry-run as the scheduled command (changes nothing)
python3 "$PAC/System/LogRetention/scripts/log_retention.py" --dry-run

# Weekly Library archive, no moves
DRY_RUN=1 bash "$PAC/Reports/scripts/weekly_archive_logs.sh"

# Template fill, no writes, no model
python3 "$PAC/Reports/template_fill.py" --all --draft none --dry-run
```

Hand-run `worklog_once.sh` **does** write Worklog. That is a write. Do not loop it.

---

## 9. Where else to read (do not copy them here)

| Page | Why |
| --- | --- |
| [For an AI](./Teaching-Desk/For-an-AI.md) | Edit rules, what you leave alone |
| [Root Monitor handbook](./Root-Monitor-Operators-Handbook/Root-Monitor-Operators-Handbook.md) | What the window shows vs the poller |
| [Desk automations and service windows](../Documentation/11-Runtime-Jobs-and-Control/Desk-Automations-and-Service-Windows.md) | Job overrides, power schedules, and the public service-window file |
| [AI processing logs](../Documentation/../Documentation/10-AI-and-Agent-Runtime/AI-Processing-Logs-and-Reports.md) | JSONL fields, redaction, gate |
| [Template report generation](../Documentation/../Documentation/10-AI-and-Agent-Runtime/Template-Report-Generation.md) | Generated reports, validator, never-write-Library |
| [Voice reports G3](../Documentation/../Documentation/10-AI-and-Agent-Runtime/Voice-Reports-G3.md) | `_current` + Archive convention for voice |
| [04-Data](../Documentation/04-Data/README.md) | Boundary; path row is partly stale (old `/home/rootrecord/Database/`) |
| [WO-RPT-001](../Documentation/06-Development/Work-Orders/Complete/WO-RPT-001-Reports-Worklog-Domain-Import.md) | Worklog spine |
| [WO-MIG-41](../Documentation/06-Development/Work-Orders/drafts/Log_retention_apply_Work_Order_WO-MIG-41-2026-09-29.md) | Log retention; apply still unsigned |
| Database README on GitHub | Layout authority; Logs sketch lagging the tree |
| Pacific `Reports/README.md` | Worklog + future radio spine; proposed jobs |
| Pacific `Logs/Automations` README (in Database) | POLLER_LOG, hourly cut |
| Ecosystem `Pull.sh` / `Push.sh` | Manual git; logs in `Logs/Github/Manual/` |

The desk path `5 - RootRecord-Library` is the live Library the automated sync publishes; update this file on the desk, do not open Cursor PRs for routine docs. Do not “fix” Ecosystem by pasting this guide into Master-Prompt.

---

## 10. Short checklist before you touch logs or reports

1. Writer belongs in Pacific. File belongs in Database. Story belongs in Library.
2. Is the path gitignored on purpose? If yes, a missing GitHub file is success.
3. Is the job off? Leave it off.
4. Rotation already exists for this class? Reuse it. Do not add zip-at-boot from the Energy Archive README.
5. Retention `--apply` is not yours tonight.
6. After an edit: compile or `bash -n`. Do not restart.

*Investigated 30 September 2026. If a job id or gitignore line moved after that, believe the desk files over this page and update this handbook in Library — do not patch Database from here.*
