# WORK ORDER — AdSense and AdMob end-of-day

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-MIG-38-2026-09-29 |
| **Date** | 2026-09-30 (HST) |
| **Status** | OPEN — code landed; jobs gated off; page not deployed; old files removed on GitHub |
| **Owner** | RootRecord |
| **Related** | Agent 38. Depends on Public website checkout (agent 07) and Stripe, Vercel, and live-data pages (agent 10). Both destination folders are already in place. No later function depends on this one. |

**Scope:** Bring the AdSense and AdMob end-of-day snapshots onto the live system as gated Pacific jobs and one status card on the existing Vercel app. The code, gated jobs, status card, archive, and GitHub deletion on `online-safe-20260920` have landed. Live Google calls, job enablement, sends, and deploy still need sign-off. This file stays in drafts.

---

## 1. Intent

The old jobs pulled a 7-day HST report and wrote a file snapshot. AdSense used the AdSense Management API (`PAGE_VIEWS`, `CLICKS`, `ESTIMATED_EARNINGS`, `PAGE_VIEWS_RPM`, `IMPRESSIONS`, dimension `DATE`). AdMob used the network report (`ESTIMATED_EARNINGS`, `IMPRESSIONS`, `CLICKS`, `AD_REQUESTS`, `MATCHED_REQUESTS`, dimension `DATE`). Each job wrote a markdown snapshot and updated `state/store/adsense-report.json` or `state/store/admob-report.json`. Discord posting defaulted off. The clients were desk OAuth only, not ad tags on public sites. OAuth client and token JSON lived under `~/Ava/Data/secrets`, not in git. Scheduler times were 21:00 HST (AdSense) and 21:05 HST (AdMob).

The live system already runs Energy BLE, the poller, Hawaiʻi weather, the US-Mainland globe, cameras, Kokoro, and `geology_collect.py`. Those stay. This function is not in the live scheduler. The public site is the one Next.js app in `3 - RootRecord-Website`. The new job writes last files under Database and, when built, shows a status card on that same app. It does not import an old ad-page theme.

---

## 2. Current reality

Folder name: **Advertising**. Same name in all three places. No lowercase twin and no symlink. Not installed. Not a subfolder of Energy, Geology, Weather, Reports, Security, Communications, System, or Media.

| Place | Path |
| --- | --- |
| Server code | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Advertising/scripts` (Python package `Advertising`; `Advertising/lib/envload.py` for keys) |
| Database data | `2 - RootRecord-Database/Advertising/` |
| Database logs | `2 - RootRecord-Database/Logs/Advertising/` |

Public UI, when built: `3 - RootRecord-Website`. Data and logs stay on the Database paths above. No `Logs/` directory on the server. `Advertising/lib/envload.py` allowlists key names only. No second env file. No token JSON on disk. No write-back of refreshed tokens into `master-key.env`.

### 2.1 What exists

| Item | Location / status |
| --- | --- |
| Folder `Advertising` (code, data, logs) | Landed. Jobs `adsense_eod` and `admob_eod` are in `ON_AT`, gated off |
| Public website checkout | `3 - RootRecord-Website` is in place, including `/data` |
| Stripe, Vercel, and live-data pages | Pacific `Website/` is in place (`stripe_poll.py`, `vercel_builds.py`, `live_data_pages.py`). Build does not pause for agents 07 or 10 |
| Visual direction | US-Mainland globe, full-screen dark globe and glass cards. `1 - Servers/2 - RootRecord-US-Mainland-Server/mirror/network-globe/network-globe/` and `Documentation/08-ideas/2026-09-29-globe-landing-overlay.md` |
| Old AdSense source | `/home/rootrecord/old ollama/old skills/advertising/adsense-eod/` (`scripts/adsense.py`, `scripts/job.py`, `SKILL.md`, `INDEX.md`, `DAILY.md`, `references/migrate.md`) |
| Old AdMob source | `/home/rootrecord/old ollama/old skills/advertising/admob-eod/` (`scripts/admob.py`, `scripts/job.py`, `SKILL.md`, `INDEX.md`, `DAILY.md`, `references/migrate.md`) |
| Old last files | `/home/rootrecord/old ollama/old skills/state/store/adsense-report.json` and `admob-report.json`. `state/store/` has 119 files and is shared |
| Old git repo | `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server`, local checkout `/home/rootrecord/old ollama/old skills`, branch `online-safe-20260920`. Twelve tracked files under `advertising/`. `main` does not contain `advertising/` |
| Shared helper to leave | `apps.core` (imported by the old jobs). Leave it |
| `master-key.env` | `/home/rootrecord/master/master-key.env`. None of these names are present: `GOOGLE_ADSENSE_CLIENT_ID`, `GOOGLE_ADSENSE_CLIENT_SECRET`, `GOOGLE_ADSENSE_REFRESH_TOKEN`, `GOOGLE_ADSENSE_ACCOUNT_NAME`, `GOOGLE_ADSENSE_CURRENCY`, `GOOGLE_ADMOB_CLIENT_ID`, `GOOGLE_ADMOB_CLIENT_SECRET`, `GOOGLE_ADMOB_REFRESH_TOKEN`, `GOOGLE_ADMOB_ACCOUNT_NAME` |
| Scheduler map | `adsense-eod / admob-eod` at 21:00 / 21:05 is GATED `RR_ADSENSE` / `RR_ADMOB` |
| Migration matrix | Row 71, Advertising (AdMob/AdSense EOD), status **partial** |

### 2.2 Completed so far

- [x] Draft work order written. Not on the active index.
- [x] Advertising code, no-key snapshots, and gated-off jobs.
- [x] Status card on the one Vercel app. Not deployed.
- [x] Old files archived, then removed from the old repo locally and on GitHub `online-safe-20260920` (`cf46347f`).
- [x] Library rows corrected after phase 4.

### 2.3 Known friction

- Ad account secrets are absent from `master-key.env`. The scripts must write `not_configured` and make no Google call until Alexander adds values and signs off a live call.
- Old AdMob `status()` hardcodes a client id. Do not copy that id into the new status output or into this work order.
- AdMob reused the AdSense OAuth client file and kept a separate token. Client id and secret fall back to the AdSense names. Refresh tokens stay separate.
- `jobs.py`, the Vercel app shell, and `master-key.env` are shared. Pause if another agent is already editing one of them.
- `state/store/` is shared. Phase 4 archives and removes only the two report JSON files.
- `Solar-Pacific-RootRecord-Server` is shared. Phase 4 removes only this function’s files, on `online-safe-20260920`. Do not force-push. If push protection rejects the push, stop and record it.

---

## 3. Tasks

Build only after Alexander accepts this draft and says to build. Until then, do not edit runtime files, restart services, send messages, actuate hardware, or spend cloud money.

1. Pause if `jobs.py`, the Vercel app shell, or `master-key.env` is already being edited. Do not pause for agents 07 or 10: `3 - RootRecord-Website` and Pacific `Website/` are already in place.
2. Add `Advertising/__init__.py` and `Advertising/lib/envload.py` on the Energy and Website allowlist pattern. Allow only the nine key names in section 2.1. Never print values. No second env file. No committed secrets. AdMob client id and secret fall back to `GOOGLE_ADSENSE_CLIENT_ID` and `GOOGLE_ADSENSE_CLIENT_SECRET`. Refresh tokens do not fall back.
3. Add `Advertising/scripts/adsense_eod.py` and `Advertising/scripts/admob_eod.py`. Stdlib HTTP, same shape as `Website/scripts/stripe_poll.py`. A 7-day HST window. Missing keys write `ok: false` and `detail: not_configured`, exit 0, and do not call Google. Do not write token JSON. Do not write refreshed tokens back into `master-key.env`. Access tokens stay in memory.
4. Write last snapshots under `2 - RootRecord-Database/Advertising/`. Logs, if a run needs a line, go under `2 - RootRecord-Database/Logs/Advertising/` only. Do not put a `Logs/` directory on the server. Do not copy old markdown reports, `DAILY.md`, or `state/store/*-report.json` into Pacific, Database, the website, or git.
5. Propose gated `ON_AT` blocks only in `Automations/scripts/jobs.py`, same style as `stripe_poll`: `adsense_eod` at `21:00` behind `RR_ADSENSE=1`; `admob_eod` at `21:05` behind `RR_ADMOB=1`. Both stay off. No boot report. No Discord post.
6. Add one glass card at `3 - RootRecord-Website/src/app/data/advertising/page.tsx`, linked from `/data`, same dark glass as the live-data pages. Show last-run status only (configured or not, HST date). Do not show earnings, account names, or client ids. No ad tags. No old theme. Do not deploy.
7. After the migration works, and before the Library update: copy `advertising/**` (12 files) and only `state/store/adsense-report.json` and `state/store/admob-report.json` into `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/`, keeping the path each had inside the old repo. Generated data that lived beside that source goes into this archive too, and still does not go into the live Folders. After the archive copy is on disk, delete those same paths from the local checkout on `online-safe-20260920`, commit, and push that branch. Do not force-push. Do not delete the GitHub repository. If the archive copy fails, do not delete. If push protection rejects the push, stop and record it.
8. Leave `apps.core`. Leave the other 117 files in `state/store/`. Leave dated `github-history` trees. Leave `~/.ollama/skills` (no advertising folder there).
9. After phase 4, add a short result note to this work order (what landed, what was archived, what was removed on GitHub) and correct only the Library pages this function made stale: migration matrix row 71, and the `adsense-eod / admob-eod` row in the scheduler map. Do not rewrite unrelated work orders.

---

## 4. Non-goals

- Do not overwrite Energy BLE, the poller, Hawaiʻi weather, the globe collector, camera grabs, Kokoro, or `geology_collect.py`.
- Do not build other agents’ functions. Do not import an old ad-page theme, background, or CSS skin.
- Do not publish earnings, account names, or client ids on the public page.
- Do not port the boot report or Discord posting. Sends stay off.
- Do not import old snapshots, `DAILY.md` notebook text, token files, logs, caches, virtualenvs, `node_modules`, or `__pycache__` into Pacific, Database, the website, or git.
- Do not open a second Vercel site.
- Do not restore files under `~/.ollama/skills/energy`, automations, or `coms/ssh/local-data-globe`.
- Do not edit other agents’ files. Do not delete `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server`.
- Android apps already in `6 - Android Development` stay there.

---

## 5. Key file / path reference

| Path | Role |
|------|------|
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Advertising/scripts/adsense_eod.py` | AdSense end-of-day snapshot. No key writes `not_configured` and does not call Google |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Advertising/scripts/admob_eod.py` | AdMob end-of-day snapshot. Same no-key behavior |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Advertising/lib/envload.py` | Allowlist loader for the nine key names. Never prints values |
| `2 - RootRecord-Database/Advertising/` | Last snapshots. Not imported from the old desk |
| `2 - RootRecord-Database/Logs/Advertising/` | Run logs only. No server-side `Logs/` directory |
| `3 - RootRecord-Website/src/app/data/advertising/page.tsx` | Status card on the one Vercel app. No earnings. Not deployed |
| `3 - RootRecord-Website/src/app/data/page.tsx` | Add the link to the status card |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Website/scripts/stripe_poll.py` | Pattern for the no-key snapshot |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Website/lib/envload.py` | Pattern for the allowlist loader |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Automations/scripts/jobs.py` | Shared. Build may add only the two gated-off `ON_AT` blocks |
| `/home/rootrecord/master/master-key.env` | Only secret file. Alexander adds values. This draft does not edit it |
| `/home/rootrecord/old ollama/old skills/advertising/` | Old source, 12 files. Archive, then remove from the old repo |
| `/home/rootrecord/old ollama/old skills/state/store/adsense-report.json` | Old generated last file. Archive, then remove. Leave the rest of `state/store/` |
| `/home/rootrecord/old ollama/old skills/state/store/admob-report.json` | Old generated last file. Archive, then remove |
| `apps.core` | Shared. Leave it |
| `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/` | Phase 4 archive, original relative paths |
| `Documentation/00-architecture/Old-Repo-Migration-Matrix.md` | Row 71. Correct only after phase 4 |
| `Documentation/00-architecture/G1-Scheduler-To-G3-Jobs-Map-2026-09-29.md` | `adsense-eod / admob-eod` row. Correct only after phase 4 |
| `Documentation/08-ideas/2026-09-29-globe-landing-overlay.md` | Visual direction for the status card |

---

## 6. Open items

**Additional requirements:**

- Alexander accepts this draft before any build.
- Alexander adds secret values to `master-key.env` if a real Google call is wanted. The code ships able to run with the keys absent.
- Sign-off before a live Google call, before enabling `RR_ADSENSE` or `RR_ADMOB`, before any send, before putting tokens into `master-key.env`, and before deploying the page.
- Phase 4 archive-then-delete of the old function’s files is already ordered. It is not a deletion of live Ecosystem files. If the archive copy fails, do not delete.
- `config/` is not required. Account names and currency are key names, not a second config file.

---

## 7. Notes & constraints

- No force-push.
- Secrets stay out of git. Key names, not values: `GOOGLE_ADSENSE_CLIENT_ID`, `GOOGLE_ADSENSE_CLIENT_SECRET`, `GOOGLE_ADSENSE_REFRESH_TOKEN`, `GOOGLE_ADSENSE_ACCOUNT_NAME`, `GOOGLE_ADSENSE_CURRENCY`, `GOOGLE_ADMOB_CLIENT_ID`, `GOOGLE_ADMOB_CLIENT_SECRET`, `GOOGLE_ADMOB_REFRESH_TOKEN`, `GOOGLE_ADMOB_ACCOUNT_NAME`.
- Prefer small reversible steps.
- Sends, speaker playback, OBS, hardware switching, deletion of live Ecosystem files, and cloud spend need Alexander’s sign-off. Do not do those things in this draft.
- New periodic jobs stay gated off.
- Do not import system-generated data into the live Folders.

**Small test, run 2026-09-30 HST with no keys.** Each script exited 0, wrote `detail: not_configured`, and made no HTTP call. With dummy AdSense client keys and the network blocked, AdSense attempted one token request and wrote nothing secret. AdMob stayed `not_configured` because its refresh token does not fall back. The final files are the no-key snapshots.

### Result note

Landed 2026-09-30 HST. Jobs stay off. The page is not deployed.

- Server code: `Advertising/lib/envload.py`, `Advertising/scripts/adsense_eod.py`, `Advertising/scripts/admob_eod.py`.
- No-key test: `Database/Advertising/adsense-last.json` and `admob-last.json` are `ok: false`, `detail: not_configured`, generated `2026-09-30T01:02:25-10:00`. No Google call.
- Jobs: `adsense_eod` at 21:00 behind `RR_ADSENSE=1`, `admob_eod` at 21:05 behind `RR_ADMOB=1`, both off. Neighboring uncommitted jobs in `jobs.py` were left in place.
- Public card: `3 - RootRecord-Website/src/app/data/advertising/page.tsx`, linked from `/data`. Checked in the browser at `http://localhost:3001/data/advertising`. AdSense and AdMob both read “Not configured · 2026-09-30”. No earnings. Not pushed, so Vercel production is unchanged.
- Archive: `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/advertising/` (12 files) and `state/store/adsense-report.json`, `state/store/admob-report.json`.
- Local deletion and GitHub: `online-safe-20260920` `cf46347f` on `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server`. The two report JSON files were gitignored (`**/store/`), removed from the working tree, and were not on GitHub. `apps.core` was not edited. `origin/skills-rebuild` still contains `advertising/` (12 files). `main` does not.
- Library: migration matrix row 71 and the scheduler map row for adsense-eod / admob-eod.

---

*Work order prepared 2026-09-30 HST. Update status when closed.*

---

## Archive / location note

This file is a draft. Do not promote it onto the active index.

**Active / accepted WOs** — filename when saved:

```text
AdSense_and_AdMob_end_of_day_Work_Order_WO-MIG-38-2026-09-29.md
```

Location after acceptance:

```text
Documentation/06-development/Work-Orders/
```

**Drafts (not on active index)** — this file lives here:

```text
Documentation/06-development/Work-Orders/drafts/
```

See `drafts/README.md` and WO-WOGEN-001. Do not auto-promote.

**Closed WOs:** set Status → COMPLETE/CLOSED → `git mv` into:

```text
Documentation/06-development/Work-Orders/Complete/
```

Human session logs archive under `Documentation/01-operations/archive/YYYY-Www/` (WO-ARCH) — separate from closed work orders.
