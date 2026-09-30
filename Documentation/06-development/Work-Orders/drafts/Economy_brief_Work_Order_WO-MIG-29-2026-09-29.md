# WORK ORDER — Economy brief

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-MIG-29-2026-09-29 |
| **Date** | 2026-09-30 (HST) |
| **Status** | OPEN — draft, not accepted for execution |
| **Owner** | RootRecord |
| **Related** | Agent 29, wave D. Depends on 03 Council persona prompts, 21 Discord poller, 28 MySQL desk facts. Matrix row 51. Scheduler row `economy-brief` 15:00 HST. |

**Scope:** Migrate the Economy brief only: a daily markdown file under Reports. Discord posting, MySQL access, and council persona prompts are other functions. This draft does not build, send, schedule, or delete anything. It is not on the active index.

---

## 1. Intent

The old function wrote one daily file, `economy-brief-YYYY-MM-DD.md`, at 15:00 HST. The file recorded whether the snapshot was ok, wallet count, circulating gold, net gold, bonds outstanding and principal, and the Kīlauea alert level and multiplier. Gold stays in-game. It never converts to dollars. After the file, the old job posted a Discord card. Night sleep skipped the run.

The live system already keeps EcoFlow BLE, the weather poller, the globe collector, camera grabs, Kokoro, and `geology_collect.py`. Kīlauea `alert_level` and `multiplier` already land in `2 - RootRecord-Database/Geology/Volcanoes/kilauea-last.json`. This function reads that file. It does not collect volcano data.

Nothing under `Reports/Economy-Brief` exists yet. Matrix row 51 and the scheduler map still mark the brief missing, blocked on MySQL credentials and a Discord post.

---

## 2. Current reality

### 2.1 What exists

Folder name: **Economy-Brief**, a subfolder of Reports. One capitalized name in all three paths. No lowercase twin and no symlink.

| Item | Location / status |
| --- | --- |
| Server code | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Reports/Economy-Brief/scripts` — folder staged (`.gitkeep`). `economy_brief.py` not written. No `config/`. No `Logs/` on the server. |
| Database data | `2 - RootRecord-Database/Reports/Economy-Brief/` — folder staged (`.gitkeep`). Markdown stays out of git. |
| Database logs | `2 - RootRecord-Database/Logs/Reports/Economy-Brief/` — folder staged (`.gitkeep`). Run lines stay out of git. |
| Secrets | `/home/rootrecord/master/master-key.env` only. No MySQL, Discord, RootMC, or economy key names are present. This function adds none and reads no passwords. MySQL credentials stay with MySQL desk facts. Discord channel ids stay with the Discord poller. |
| Old runtime | `reports/sort/economy-brief/scripts/job.py` in the gitignored `reports/` tree of `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server`. Local checkout: `/home/rootrecord/old ollama/old skills`, branch `online-safe-20260920`. |
| GitHub-tracked shim | `origin/ns/apps/core/crons/on_time/economy_brief.py` in that same repo. It execs `~/.ollama/skills/economy-brief/scripts/job.py`. Do not restore that path. |
| Live Kīlauea facts | `2 - RootRecord-Database/Geology/Volcanoes/kilauea-last.json` (`alert_level`, `multiplier`). Missing file means `unknown` / `1.0`. |
| Dependency Folders | Discord poller: `Communications/Discord/` is in place. MySQL desk facts: `System/MysqlDesk/` is in place. Council persona prompts: no Folder yet. The lowercase `Communications/discord` README remains; this function does not use it. |

### 2.2 Completed so far

- [x] Draft work order written (this file). Status stays OPEN — draft, not accepted for execution.
- [x] Economy-Brief code, Database, and Logs folders created and staged. Runtime files stay gitignored.
- [ ] Alexander accepts this draft and says to build.
- [x] Discord poller Folder `Communications/Discord/` and MySQL desk facts Folder `System/MysqlDesk/` are in place.
- [ ] Council persona prompts Folder. The brief does not call it. Measured markdown does not wait on that Folder.
- [x] `economy_brief.py` writes the markdown under Database `Reports/Economy-Brief/`.
- [x] Fixture dry-run PASS 2026-09-30 00:41 HST. `economy-brief-2026-09-30.md` from a 4-wallet fixture. Gold-never-dollars note present. No `$`. `posted` false. Kīlauea line read `WATCH` / `2.5` from `kilauea-last.json`. No Discord. No MySQL.
- [x] Phase 4 archive copy is on disk. Local gitignored `reports/sort/economy-brief/` removed after `diff -rq`. Shim deleted and pushed: `27f7c442` on `online-safe-20260920`.
- [x] Phase 5: matrix row 51, the `economy-brief` scheduler row, and the Reports README status line corrected.

### 2.3 Known friction

- The brief cannot take a live snapshot until MySQL desk facts exists. Do not query MySQL from this function.
- Discord is a later decision. `Communications/discord` is not a poller.
- `reports/` in the old repo is gitignored, so the skill tree is local-only. The shim is the only GitHub file.
- `jobs.py`, the Vercel app shell, and `master-key.env` are shared. Leave them if another agent is editing them.

---

## 3. Tasks

1. Stop here until Alexander accepts this draft and says to build. Until then, do not edit runtime files, restart services, send messages, actuate hardware, or spend cloud money.
2. On build, pause if any of these Folders is missing. Name the missing function. Do not build it.
   - Council persona prompts (agent 03)
   - Discord poller (agent 21)
   - MySQL desk facts (agent 28)
3. When those Folders are in place, add `Reports/Economy-Brief/scripts/economy_brief.py`. It writes the same markdown sections into `2 - RootRecord-Database/Reports/Economy-Brief/economy-brief-YYYY-MM-DD.md`. Numbers come from the MySQL desk-facts snapshot. Alert and multiplier come from `kilauea-last.json`. A run line goes to `2 - RootRecord-Database/Logs/Reports/Economy-Brief/`.
4. If `System/NightSleep/scripts/night_sleep.py` exists, skip when it says night sleep. Do not implement night sleep.
5. Compose the old Discord card only behind a send flag that defaults off. A send needs Alexander's sign-off and the Discord poller. The smoke test never posts.
6. Leave `jobs.py` untouched. Proposed block only, default off, 15:00 HST:

```python
{
    "id": "reports_economy_brief",
    "enabled": os.environ.get("RR_ECONOMY_BRIEF", "0") == "1",
    "description": "Daily economy brief markdown. Discord stays off unless signed off.",
    "at_times": ["15:00"],
    "builtin": "",
    "command": 'nice -n 10 python3 "…/Reports/Economy-Brief/scripts/economy_brief.py"',
    "timeout_sec": 120,
    "cwd": "…/Reports/Economy-Brief/scripts",
    "env": {},
}
```

7. Small test, no network and no Discord: `python3 economy_brief.py --fixture <tiny json> --dry-run` writes the markdown from the fixture, includes the note that gold never converts to dollars, and contains no `$`.
8. After the migration works, archive this function's old files (phase 4), then update this work order and the three Library pages (phase 5).

---

## 4. Non-goals

- Do not build Council persona prompts, the Discord poller, or MySQL desk facts.
- Do not edit `minecraft/rootmc-economy/scripts/rootmc_economy.py`. That SQL and Discord formatter is shared. The player-economy report is out of this work. Do not re-import the RootMC Android app.
- Do not edit Discord, Slack, or Telegram services, `jobs.py`, the Vercel app, or `master-key.env`.
- Do not replace EcoFlow BLE, the weather poller, the globe collector, camera grabs, Kokoro, or `geology_collect.py`.
- Do not restore `~/.ollama/skills/economy-brief` or anything under `~/.ollama/skills/energy`, automations, or `coms/ssh/local-data-globe`.
- Do not add a public website page. Do not import logs, samples, last-state files, generated reports, or `__pycache__` into Pacific, Database git, the website, or git.
- Do not rewrite other agents' files or other work orders.

---

## 5. Key file / path reference

| Path | Role |
|------|------|
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Reports/Economy-Brief/scripts/economy_brief.py` | Writer. Fixture dry-run PASS 2026-09-30 00:41 HST. Discord send stays refused. |
| `2 - RootRecord-Database/Reports/Economy-Brief/` | Daily markdown and last snapshot. Runtime output. Out of git. |
| `2 - RootRecord-Database/Logs/Reports/Economy-Brief/` | Run log only. |
| `2 - RootRecord-Database/Geology/Volcanoes/kilauea-last.json` | Read-only alert level and multiplier. |
| `System/NightSleep/scripts/night_sleep.py` | Call `should_run` only if that file exists. |
| `/home/rootrecord/master/master-key.env` | Sole secrets file. No keys added by this function. |
| `/home/rootrecord/old ollama/old skills/reports/sort/economy-brief/` | Old local source, including `scripts/job.py`, `SKILL.md`, `INDEX.md`, `DAILY.md`, `references/migrate.md`, and `__pycache__`. Gitignored. |
| `/home/rootrecord/old ollama/old skills/origin/ns/apps/core/crons/on_time/economy_brief.py` | Removed. Commit `27f7c442`, pushed to `online-safe-20260920`. |
| `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/reports/sort/economy-brief/` | Phase 4 archive of the gitignored tree, same in-repo path. |
| `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/origin/ns/apps/core/crons/on_time/economy_brief.py` | Phase 4 archive of the shim. |
| `5 - RootRecord-Library/Documentation/00-architecture/Old-Repo-Migration-Matrix.md` | Row 51. Correct only after phase 4. |
| `5 - RootRecord-Library/Documentation/00-architecture/G1-Scheduler-To-G3-Jobs-Map-2026-09-29.md` | `economy-brief` row. Correct only after phase 4. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Reports/README.md` | Status line. Correct only after phase 4. |

---

## 6. Open items

**Additional requirements:**

- Alexander accepts this draft before any build.
- Build pauses while Council persona prompts, the Discord poller, or MySQL desk facts has no Folder.
- Discord send, a `jobs.py` edit, speaker playback, OBS, hardware switching, deletion of live Ecosystem files, and cloud spend need a separate sign-off. Phase 4 deletion of the old function's files is already ordered, and only after the archive copy is on disk.
- Shared file left in the old repo and named here: `minecraft/rootmc-economy/scripts/rootmc_economy.py`.

---

## 7. Notes & constraints

- No force-push. Do not delete the GitHub repository `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server`.
- Secrets stay out of git. Never print env values. Never add a second env file.
- Prefer small reversible steps.
- Sign-off gates: live Discord post; registering the 15:00 job; any cloud spend; any hardware or speaker action. The fixture dry-run is the proof and does none of those.
- Test, once the script exists: `python3 economy_brief.py --fixture <tiny json> --dry-run`. Pass means the markdown is written from the fixture, the gold-never-dollars note is present, and the file contains no `$`. No network. No Discord.
- Phase 4, only after the brief works: copy the gitignored `reports/sort/economy-brief/` tree (source, `DAILY.md`, and `__pycache__`) and the shim into `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/`, keeping each in-repo path. Then delete those same paths from the old checkout. Commit and push only the shim deletion on `online-safe-20260920`. `reports/` is gitignored, so that tree is a local delete. If the archive copy fails, do not delete.
- Phase 5: add a short result note below (what landed, what was archived, what was removed on GitHub) and correct only matrix row 51, the `economy-brief` scheduler row, and the Reports README status.

---

*Work order prepared 2026-09-30 HST. Update status when closed.*

---

## Archive / location note

**Active / accepted WOs** — filename when saved:

```text
Economy_brief_Work_Order_WO-MIG-29-2026-09-29.md
```

Location after promotion (not done):

```text
Documentation/06-development/Work-Orders/
```

**Drafts (not on active index)** — this file:

```text
Documentation/06-development/Work-Orders/drafts/Economy_brief_Work_Order_WO-MIG-29-2026-09-29.md
```

See `drafts/README.md` and WO-WOGEN-001. Do not auto-promote.

**Closed WOs:** set Status → COMPLETE/CLOSED → `git mv` into:

```text
Documentation/06-development/Work-Orders/Complete/
```

Human session logs archive under `Documentation/01-operations/archive/YYYY-Www/` (WO-ARCH) — separate from closed work orders.

---

## Result note

2026-09-30 00:41 HST. `economy_brief.py` is in place. Fixture dry-run PASS. Discord was not posted. MySQL was not queried.

Archived, same in-repo paths, under `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/`:

- `reports/sort/economy-brief/` (source, `DAILY.md`, and `__pycache__`)
- `origin/ns/apps/core/crons/on_time/economy_brief.py` (copy of the shim)

The gitignored tree was removed from `/home/rootrecord/old ollama/old skills/reports/sort/economy-brief/` after `diff -rq` matched. The shim was deleted in `27f7c442` and pushed to `origin/online-safe-20260920` (`98a7b651..50d3b0a6`). The GitHub repository was not deleted. Shared file left in place: `minecraft/rootmc-economy/scripts/rootmc_economy.py`.

Library pages corrected: matrix row 51, the `economy-brief` scheduler row, and the Reports README status line.
