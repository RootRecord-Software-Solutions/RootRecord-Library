# WORK ORDER — Stripe, Vercel, and live-data pages

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-MIG-10-2026-09-29 |
| **Date** | 2026-09-29 (HST) |
| **Status** | OPEN — pages are in the Vercel app; jobs off; GitHub push of the old-repo branch blocked |
| **Owner** | RootRecord |
| **Related** | Agent 10. Build pauses on agent 07 (Public website checkout) until `3 - RootRecord-Website` holds the one Vercel app. Agent 38 (AdSense and AdMob end-of-day) depends on this function later. |

**Scope:** Bring Stripe balance snapshots, Vercel failed-build records, and live-data pages that read Energy, Weather, and Geology files already on disk. Public pages are in the one Vercel app at `/data`, using glass cards. Old page skins stay out of that app. Jobs stay off. The old folders are archived and removed locally. A production deploy and the GitHub push of the old-repo branch are still waiting.

---

## 1. Intent

Old `stripe-poll` refreshed a Stripe balance snapshot (available, pending, 30-day income, fees, payouts, and the last 40 USD transactions) and kept the previous good file when a poll failed. Old `vercel-builds` listed Vercel deployments, saved redacted failed-build logs, and cleared them after a clean deploy of the same project and target or after 5 days. Old `live-data-pages` turned on-disk facts into public pages and omitted numbers it did not have. Old `holding` is a static “we’ll be back” skin.

The live system already has Energy BLE, the poller, Hawaiʻi weather, the US-Mainland globe, cameras, Kokoro, and `geology_collect.py`. Those stay. The newer public site is the existing Next.js Vercel app. This function adds behavior to that one app. It does not replace the app with old page skins.

---

## 2. Current reality

Folder name: **Website**. Same name in all three places. No lowercase twin and no symlink. This function is not a subfolder of Energy, Geology, Weather, Reports, Security, Communications, System, or Media. The existing `Communications/website/` staging clone stays where it is.

| Place | Path |
| --- | --- |
| Server code | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Website/scripts` (Python package `Website`) |
| Database data | `2 - RootRecord-Database/Website/` |
| Database logs | `2 - RootRecord-Database/Logs/Website/` |

Public pages, after checkout exists: `3 - RootRecord-Website`. Data and logs stay on the Database paths above. `Website/lib/envload.py` allowlists key names only. No second env file. No `Logs/` directory on the server.

### 2.1 What exists

| Item | Location / status |
| --- | --- |
| Folder `Website` (code, data, logs) | Landed. Jobs `stripe_poll` and `vercel_builds` are in `EVERY_SECONDS`, gated off |
| `3 - RootRecord-Website` | Still empty. Public pages are staged under Pacific `Website/staged/`, not deployed |
| Vercel staging clone | `Communications/website/RootRecord-Cloud`, gitignored. Next.js app. Live-data proxy to `origin.avaivy.cloud` returns 530 |
| Visual direction | US-Mainland globe, full-screen dark globe and glass cards. `1 - Servers/2 - RootRecord-US-Mainland-Server/mirror/network-globe/network-globe/` and `Documentation/08-ideas/2026-09-29-globe-landing-overlay.md`. `www.rootrecord.cloud` is that globe |
| Old `stripe-poll` | `/home/rootrecord/old ollama/old skills/stripe-poll` |
| Old `vercel-builds` | `/home/rootrecord/old ollama/old skills/vercel-builds` |
| Old `live-data-pages` | `/home/rootrecord/old ollama/old skills/live-data-pages` |
| Old `holding` | `/home/rootrecord/old ollama/old skills/holding` |
| Old git repo | `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server`, branch `online-safe-20260920`. Shared with other functions |
| Nested holding repo | `holding/site` → `Ava-Core-Dev/holding` |
| Shared helper to leave | `origin/scripts/config.py` defines `vercel_token` and `vercel_team_id` for other functions |
| `master-key.env` | `/home/rootrecord/master/master-key.env`. None of these names are present: `STRIPE_SECRET_KEY`, `AVA_STRIPE_SECRET_KEY`, `VERCEL_TOKEN`, `VERCEL_API_TOKEN`, `VERCEL_TEAM_ID`, `VERCEL_ORG_ID` |
| Theme archive | `5 - RootRecord-Library/Archive/Website-Themes/holding/` holds an unchanged copy of `holding/site`. Old repo not deleted |
| Scheduler map | `stripe-poll` every 30 minutes and `vercel-builds` every 5 minutes are OUT (website / payment keys) |

### 2.2 Completed so far

- [x] Draft work order written. Not on the active index.
- [x] Website code, no-key Stripe snapshot, live-page JSON, and gated-off jobs.
- [x] Public page shell staged under `Website/staged/`. Holding skin copied into the theme archive. Folder 3 stays empty for the checkout.
- [ ] Public website checkout exists in `3 - RootRecord-Website`.
- [x] Old folders archived, then removed from the local old repo (`577ad693`). GitHub push of that branch was rejected by push protection on an older commit. `Ava-Core-Dev/holding` was not found, so that remote was not changed.

### 2.3 Known friction

- Checkout (agent 07) is missing. Building public pages before that folder exists would invent a second site home.
- `Communications/website/RootRecord-Cloud` is a newer Vercel checkout staged beside Pacific. Do not copy old skins over it, and do not start a second Vercel project. Page edits wait until folder 3 is the one app, and pause if that shell is already being edited.
- Stripe and Vercel key names are absent from `master-key.env`. Polls must no-op cleanly until Alexander adds values.
- Old Vercel ingest deletes fixed or 5-day-old error logs. That deletion waits for a later sign-off.
- `Solar-Pacific-RootRecord-Server` is shared. Phase 4 removes only this function’s four folders.
- `jobs.py` and `master-key.env` are shared. Pause if another agent is editing either file.

---

## 3. Tasks

Build only after Alexander accepts this draft and says to build. Until then, do not edit runtime files, restart services, send messages, actuate hardware, or spend cloud money.

1. Pause if `3 - RootRecord-Website` is still empty. That missing folder is Public website checkout (agent 07). Do not check the site out and do not build that function.
2. Pause if `jobs.py`, the Vercel app shell, or `master-key.env` is already being edited.
3. Add `Website/lib/envload.py` on the Energy allowlist pattern. Allow only `STRIPE_SECRET_KEY`, `AVA_STRIPE_SECRET_KEY`, `VERCEL_TOKEN`, `VERCEL_API_TOKEN`, `VERCEL_TEAM_ID`, and `VERCEL_ORG_ID`. Never print values. No second env file. No committed secrets.
4. Port the Stripe poll. Write `2 - RootRecord-Database/Website/stripe-snapshot.json`. On failure, keep the last `ok` file. With no key, write `ok: false` and `detail: not_configured`. Leave the job gated off.
5. Port Vercel failed-build ingest. A missing token returns `missing_vercel_token` and does not call the API. Save redacted failed-build records under `2 - RootRecord-Database/Logs/Website/`. Do not prune or delete those records until a later sign-off. Do not run `auto-push.py`. Do not change Vercel project settings. Leave the job gated off.
6. Port live-data page builders that read files this system already writes: power from Energy, weather from Weather, Kīlauea from Geology. Missing numbers stay omitted. Chat, voice packs, day board, Minecraft, and context stay out.
7. Public pages in the one Vercel app use the globe glass-card direction. Do not import old themes, backgrounds, CSS skins, or the holding page into the Vercel build.
8. Propose gated `jobs.py` blocks only, default off: `stripe_poll` about every 30 minutes behind `RR_STRIPE=1`; `vercel_builds` about every 5 minutes behind `RR_VERCEL_BUILDS=1`. Live pages are on demand from last files, not a new always-on poller. Do not edit `jobs.py` beyond that gated block.
9. After the migration works, and before the Library update: copy `holding/site` unchanged into `5 - RootRecord-Library/Archive/Website-Themes/holding/` and keep that archive out of the Vercel build. Copy the four old folders into `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/`, keeping the path each had inside the old repo. Copy the nested holding site under `Old repos deleted and merged/holding/`. Generated data that lived beside that source goes into this archive too, and still does not go into the live Folders. After the archive copy is on disk, delete those same files from the old repo on this machine and on GitHub. Commit that deletion and push it. Do not force-push. Do not delete either GitHub repository. If the archive copy fails, do not delete.
10. Leave shared `origin/scripts/config.py`. It stays because other functions use `vercel_token` and `vercel_team_id`.
11. After phase 4, add a short result note to this work order (what landed, what was archived, what was removed on GitHub) and correct only the Library pages this function made stale: migration matrix row 75, the scheduler map’s stripe/vercel OUT row, and the website-staging note if the one app’s home changed. Do not rewrite unrelated work orders.

---

## 4. Non-goals

- Do not overwrite Energy BLE, the poller, Hawaiʻi weather, the globe collector, camera grabs, Kokoro, or `geology_collect.py`.
- Do not build Public website checkout, Cloudflare config, Cloudflare workers, AdSense, or AdMob.
- Do not import old snapshots, build logs, collected images, database dumps, caches, virtualenvs, `node_modules`, or `__pycache__` into Pacific, Database, the website, or git.
- Do not open a second Vercel project or mix old backgrounds into the app.
- Do not publish the holding page.
- Do not restore files under `~/.ollama/skills/energy`, automations, or `coms/ssh/local-data-globe`.
- Do not edit other agents’ files. Do not delete `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server` or `Ava-Core-Dev/holding`.
- Android apps already in `6 - Android Development` stay there.

---

## 5. Key file / path reference

| Path | Role |
|------|------|
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Website/scripts` | New server code. Package name `Website` |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Website/lib/envload.py` | Allowlist loader for the six key names. Never prints values |
| `2 - RootRecord-Database/Website/stripe-snapshot.json` | Stripe last file. Not imported from the old desk |
| `2 - RootRecord-Database/Website/` | Live-page JSON written from Energy, Weather, and Geology last files |
| `2 - RootRecord-Database/Logs/Website/` | Redacted Vercel failed-build records. No server-side `Logs/` directory |
| `3 - RootRecord-Website` | One Vercel app for public pages. Empty until agent 07 checks it out |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/website/RootRecord-Cloud` | Existing gitignored staging clone. Leave it. Do not skin it with old pages |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Automations/scripts/jobs.py` | Shared. Build may add only the two gated-off blocks |
| `/home/rootrecord/master/master-key.env` | Only secret file. Alexander adds values. This draft does not edit it |
| `/home/rootrecord/old ollama/old skills/stripe-poll` | Old source. Archive, then remove from the old repo |
| `/home/rootrecord/old ollama/old skills/vercel-builds` | Old source. Archive, then remove from the old repo |
| `/home/rootrecord/old ollama/old skills/live-data-pages` | Old source. Archive, then remove from the old repo |
| `/home/rootrecord/old ollama/old skills/holding` | Old source, including the holding skin. Archive, then remove from the old repo |
| `/home/rootrecord/old ollama/old skills/origin/scripts/config.py` | Shared. Leave it |
| `5 - RootRecord-Library/Archive/Website-Themes/holding/` | Unchanged copy of `holding/site`. Out of the Vercel build |
| `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/` | Phase 4 archive of the four folders, original relative paths |
| `Old repos deleted and merged/holding/` | Phase 4 archive of the nested `Ava-Core-Dev/holding` site |
| `Documentation/00-architecture/Old-Repo-Migration-Matrix.md` | Row 75. Correct only after phase 4 |
| `Documentation/00-architecture/G1-Scheduler-To-G3-Jobs-Map-2026-09-29.md` | Stripe/Vercel OUT row. Correct only after phase 4 |
| `Documentation/00-architecture/Website-RootRecord-Cloud-Staging.md` | Correct only if this function changes the one app’s home |
| `Documentation/08-ideas/2026-09-29-globe-landing-overlay.md` | Visual direction for public pages |

---

## 6. Open items

**Additional requirements:**

- Alexander accepts this draft before any build.
- Alexander adds secret values to `master-key.env` if a real Stripe or Vercel call is wanted. The code ships able to run with the keys absent.
- Sign-off before enabling `RR_STRIPE` or `RR_VERCEL_BUILDS`, before a live Stripe or Vercel API call, before any production deploy or domain change, before pruning Vercel build records, and before the phase-4 GitHub push.
- `config/` is added only if the page catalog cannot live in the script. It is not required for the draft.

---

## 7. Notes & constraints

- No force-push.
- Secrets stay out of git. The plan lists key names, not values: `STRIPE_SECRET_KEY`, `AVA_STRIPE_SECRET_KEY`, `VERCEL_TOKEN`, `VERCEL_API_TOKEN`, `VERCEL_TEAM_ID`, `VERCEL_ORG_ID`.
- Prefer small reversible steps.
- Sends, speaker playback, OBS, hardware switching, deletion of live Ecosystem files, and cloud spend need Alexander’s sign-off. Do not do those things in this draft.
- New periodic jobs stay gated off.
- Do not import system-generated data into the live Folders.
- Phase 4 archive is on disk and the local old-repo commit is `577ad693`. The GitHub push of `online-safe-20260920` was rejected by push protection on an older commit. History was not rewritten.

**Small test, run 2026-09-30 HST with no keys.** Stripe printed `stripe not_configured` and wrote that detail. Vercel printed `vercel missing_vercel_token` and wrote no log. The power page JSON includes only fields present on the Energy last files.

### Result note

Landed 2026-09-30 HST. Folder 3 is still empty, so the public pages stay staged.

- Server code: `Website/lib/envload.py`, `Website/scripts/stripe_poll.py`, `Website/scripts/vercel_builds.py`, `Website/scripts/live_data_pages.py`. Readmes: Pacific `Website/README.md`, Database `Website/README.md`, `Logs/Website/README.md`.
- No-key test: Stripe wrote `Database/Website/stripe-snapshot.json` with `detail: not_configured`. Vercel printed `missing_vercel_token` and wrote no log. Live pages wrote `Database/Website/pages/{power,weather,kilauea}.json`.
- Jobs: `stripe_poll` (1800 s, `RR_STRIPE=1`) and `vercel_builds` (300 s, `RR_VERCEL_BUILDS=1`) in `EVERY_SECONDS`, both off.
- Staged shell remains at `Website/staged/`. The live pages are now in `3 - RootRecord-Website/src/app/data/` (`/data`, `/data/power`, `/data/weather`, `/data/kilauea`), glass cards reading Database `Website/pages/*.json`. Not pushed, so Vercel production is unchanged.
- Theme archive: `5 - RootRecord-Library/Archive/Website-Themes/holding/`.
- Old-repo archive: `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/{stripe-poll,vercel-builds,live-data-pages,holding}/`.
- Local deletion commit on `online-safe-20260920`: `577ad693`. Not pushed. GitHub rejected the branch because an older commit trips push protection. History was not rewritten. `Ava-Core-Dev/holding` returned repository not found, so that remote was left as it is.
- Library: migration matrix row 75 and the scheduler map rows for stripe-poll and vercel-builds. `ltc-pending` stays OUT. Shared `origin/scripts/config.py` was not edited.

---

*Work order prepared 2026-09-29 HST. Update status when closed.*

---

## Archive / location note

This file is a draft. Do not promote it onto the active index.

**Active / accepted WOs** — filename when saved:

```text
Stripe_Vercel_and_live_data_pages_Work_Order_WO-MIG-10-2026-09-29.md
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
