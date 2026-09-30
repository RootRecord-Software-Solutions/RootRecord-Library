# WORK ORDER — Public website checkout

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-MIG-07-2026-09-29 |
| **Date** | 2026-09-30 (HST) |
| **Status** | BUILT — checkout landed in folder 3. Not on the active index. |
| **Owner** | RootRecord |
| **Related** | Agent 07. Later: 8 Site Cloudflare config and thumbnails; 9 Cloudflare workers; 10 Stripe, Vercel, and live-data pages; 11 US all-states weather dataset; 12 State and global news builders; 13 Country location pollers; 14 Desk product apps not imported; 38 AdSense and AdMob end-of-day. [Website-RootRecord-Cloud-Staging.md](../../../00-architecture/Website-RootRecord-Cloud-Staging.md). [2026-09-29-globe-landing-overlay.md](../../../08-ideas/2026-09-29-globe-landing-overlay.md). |

**Scope:** Check the current Vercel app, `rootrecordsoftwaresolutions/RootRecord-Cloud`, into `3 - RootRecord-Website` as the one public site. Do not fill that checkout from the old `RootRecord-Website` skin or from `site-backgrounds`. The checkout landed 2026-09-30. No deploy and no push of `RootRecord-Cloud` `main`.

---

## 1. Intent

The old public site is `RootRecord-Website` at `~/.ollama/skills/website/site` (`ee3d9c1`, pages `/energy`, `/home`, `/home/status`). That tree is the old skin. It must not become the live app.

The live public app is already RootRecord-Cloud (Next.js 15, package name `rootrecord-online`). Its pages are `/`, `/blog`, `/dev`, `/goals`, `/login`, `/reports`, `/status`, and `/timeline`, plus an allowlisted `/api` proxy. That app is checked out at `3 - RootRecord-Website` @ `84dec4a`. The earlier Communications file tree had no `.git` and was removed 2026-09-30.

New code wins. Folder 3 gets a real checkout of RootRecord-Cloud. The older skills-site tree is not copied over it. The globe overlay is the visual direction for public pages; this function does not restyle anything and does not import old backgrounds.

What stays as it is: the disabled `website` row in `repos.conf`, live EcoFlow, weather, the globe, cameras, and Kokoro.

---

## 2. Current reality

Folder name: **Website**. This function is the one Vercel app. It does not get a Pacific `Website/scripts` package, and it does not open a second domain beside Energy or Geology.

| Place | Path |
| --- | --- |
| Code | `3 - RootRecord-Website/` — git checkout of `rootrecordsoftwaresolutions/RootRecord-Cloud` |
| Database | `2 - RootRecord-Database/Website/` — named, left empty of samples, `node_modules`, `.next`, and caches |
| Logs | `2 - RootRecord-Database/Logs/Website/` only. No `Logs/` directory on the server |

`master-key.env` keys for this function: none. Do not add a second env file. Do not print values. These names already exist as comments-only defaults in `Communications/website/.env.example` and stay names-only inside the clone. They are not copied into `master-key.env`:

- `AVA_ORIGIN_URL`
- `AVA_PUBLIC_API`
- `NEXT_PUBLIC_AVA_API`
- `NEXT_PUBLIC_GOALS_API`
- `NEXT_PUBLIC_ACCOUNT_API`
- `ROOTRECORD_API_ACCOUNT_URL`

### 2.1 What exists

| Item | Location / status |
| --- | --- |
| Folder 3 | `3 - RootRecord-Website/` checkout of RootRecord-Cloud @ `84dec4a`. Ecosystem root `.gitignore` ignores it. |
| Newer app, not a checkout | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/website/RootRecord-Cloud/` — source tree, no `.git`, gitignored by the Pacific `.gitignore` |
| Staging notes | `Communications/website/README.md` and `.env.example` (names only). Library: `Documentation/00-architecture/Website-RootRecord-Cloud-Staging.md`. Staging SHA noted there: `84dec4a` |
| Old site | `~/.ollama/skills/website/site` — `RootRecord-Website` @ `ee3d9c1`. `repos.conf` row `website` is disabled (`0`) and still points at this path |
| Old backgrounds | `/home/rootrecord/old ollama/old skills/site-backgrounds` |
| Ecosystem ignore | No root `.gitignore`. `.git/info/exclude` is empty. Folder 3 is not ignored |
| Theme archive | `5 - RootRecord-Library/Archive/Website-Themes/site-backgrounds/` — unchanged copy of the five theme files |

### 2.2 Completed so far

- [x] Draft work order written. Not on the active index.
- [x] Ignore rule for `3 - RootRecord-Website/` in the ecosystem root `.gitignore` before the clone
- [x] Token-free clone of RootRecord-Cloud into folder 3 @ `84dec4ad3ecf96962dbf6e6c83ebd08c7ea78932`
- [x] Unchanged copy of `site-backgrounds` into `Archive/Website-Themes/` and `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/site-backgrounds/`
- [x] Proof test (git remote, HEAD, old pages absent, ecosystem ignore)
- [x] Local removal of `site-backgrounds` committed on `online-safe-20260920` as `00505833`
- [x] GitHub check: `main` (`1dcee662`) and `fix/weather-change-detection` (`ed967aed`) have no `site-backgrounds`. The local branch was not published. Push protection rejected it because commit `679fd86c` contains a secret. That protection was not bypassed.
- [x] Removal of the Communications snapshot (signed off 2026-09-30)
- [x] Result note below. Library pages that named the Communications tree as the checkout are corrected.

### 2.3 Known friction

- The Communications tree is the newer app with its git metadata missing. Moving those files into folder 3 would still not be a checkout.
- A push of RootRecord-Cloud `main` is a Vercel production deploy. Auto-sync stays off.
- The skills checkout `origin` URL embeds a personal access token. Do not copy that URL. Rotate that token. This work order does not contain the token.
- Pacific `.gitignore` does not cover folder 3. A clone with its own `.git` becomes a gitlink if the ecosystem repo adds it. The ignore has to land before the clone.
- `www.rootrecord.cloud` is still the globe tunnel, not this Vercel app. Routing that hostname is not this function.

---

## 3. Tasks

Build only after Alexander accepts this draft and says to build. No earlier Folder is required. Agents 8, 9, 10, 11, 12, 13, 14, and 38 wait on this checkout.

1. Add a tracked ignore for `3 - RootRecord-Website/` in the ecosystem repo before the clone, the same way Pacific ignores `Communications/website/RootRecord-Cloud/`. Confirm with `git check-ignore` before `git clone`.
2. Clone `rootrecordsoftwaresolutions/RootRecord-Cloud` into `3 - RootRecord-Website` with a token-free remote (`https://github.com/rootrecordsoftwaresolutions/RootRecord-Cloud.git` or SSH). If `main` has moved past `84dec4a`, keep the newer `main` and record the SHA here. Do not overlay `~/.ollama/skills/website/site` or `site-backgrounds`.
3. Copy `site-backgrounds` unchanged into `5 - RootRecord-Library/Archive/Website-Themes/`. Keep that archive out of the Vercel app.
4. Leave `Communications/website/RootRecord-Cloud/` on disk until Alexander signs off on removing it.
5. Do not edit `jobs.py`. Do not enable the `repos.conf` `website` row. Do not run `scripts/auto-push.py`.
6. Run the small test in section 7. Skip a second `npm ci` unless Alexander asks. The 2026-09-29 staging build already passed.
7. After the checkout works, and only then: copy this function's old files into `/home/rootrecord/RootRecord-Ecosystem/Old repos deleted and merged/<old-repo-name>/`, keeping the path they had inside the old repo. Generated data that lived beside that source goes into the archive too, and still does not go into the live Folders. After the archive copy is on disk, delete those same files from the old repo on this machine and on GitHub. Commit that deletion and push it. Do not force-push. Do not delete the GitHub repository. If the archive copy fails, do not delete. Shared files named in section 4 stay.
8. Then add the phase-4 result note to this work order and correct only the Library pages this function made stale.

---

## 4. Non-goals

- A second Vercel project, or a mix of old backgrounds in the one app.
- Importing old themes, CSS skins, or per-product styling into the Vercel app.
- Importing `public-chat`, `public-edge`, `public-finance`, `public-health`, or `websites`. Those stay for agents 8 (Cloudflare config and thumbnails), 9 (Cloudflare workers), and 10 (Stripe, Vercel, and live-data pages).
- Stripe, live-data pages, Cloudflare config, workers, weather datasets, news builders, country pollers, desk product apps, and AdSense. Those are other agents.
- Editing `jobs.py`, enabling auto-sync, or running `scripts/auto-push.py`.
- Replacing live EcoFlow BLE, the poller, Hawaiʻi weather, the globe collector, camera grabs, Kokoro, or `geology_collect.py`.
- Putting `node_modules`, `.next`, logs, samples, caches, or other generated output into Pacific, Database, the website checkout's tracked files, or git.
- Restoring files under `~/.ollama/skills/energy`, automations, or `coms/ssh/local-data-globe`.
- Deleting a whole GitHub repository.
- Promoting this draft onto the active work-order index.

---

## 5. Key file / path reference

| Path | Role |
|------|------|
| `3 - RootRecord-Website/` | Code. Destination checkout of RootRecord-Cloud. Empty until the build. |
| `2 - RootRecord-Database/Website/` | Database path. Create empty of runtime output during the build. |
| `2 - RootRecord-Database/Logs/Website/` | Logs path. No server `Logs/` directory. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/website/RootRecord-Cloud/` | Existing newer tree without `.git`. Leave until sign-off. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/website/README.md` | Staging note. Correct only after phase 4, with the Library page below. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/website/.env.example` | Names only. Do not put values here or in a second env file. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/.gitignore` | Already ignores `Communications/website/RootRecord-Cloud/`. Pattern to match for folder 3. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Github/scripts/repos.conf` | `website` row stays disabled. Do not retarget it in this function. |
| `~/.ollama/skills/website/site` | Old RootRecord-Website skin. Do not copy into folder 3. Do not reuse its remote URL. |
| `/home/rootrecord/old ollama/old skills/site-backgrounds` | Old backgrounds. Archive unchanged. Do not apply. |
| `5 - RootRecord-Library/Archive/Website-Themes/` | Theme archive. Out of the Vercel build. |
| `5 - RootRecord-Library/Documentation/00-architecture/Website-RootRecord-Cloud-Staging.md` | Says the site lives under Communications. Correct after phase 4. |
| `5 - RootRecord-Library/Documentation/08-ideas/2026-09-29-globe-landing-overlay.md` | Visual direction. Not a restyle task for this function. |
| `/home/rootrecord/master/master-key.env` | No new keys from this function. |
| `Old repos deleted and merged/<old-repo-name>/` | Phase 4 archive. Deletion only after this copy is on disk. |

---

## 6. Open items

**Additional requirements:**

- Alexander accepts this draft and says to build before any clone, ignore-rule edit, archive copy, or service action.
- Sign-off before removing `Communications/website/RootRecord-Cloud/`.
- Sign-off is already the phase-4 order for archive-then-delete of this function's old files. Shared packets in section 4 are not part of that delete.
- Confirm, during the build, whether `site-backgrounds` is tracked in a GitHub repo. If it exists only on disk, archive it locally and do not delete a GitHub repository to match it.
- Rotate the personal access token embedded in the skills checkout `origin` URL. Do not write the token into this file.

---

## 7. Notes & constraints

- No force-push.
- Secrets stay out of git. The skills remote URL is not a template for the new remote.
- Prefer small reversible steps.
- No push, no Vercel project-settings change, no production deploy, and no cloud spend without Alexander's sign-off.
- Sends, speaker playback, OBS, hardware switching, and deletion of live Ecosystem files need Alexander's sign-off. The Communications snapshot was removed under that sign-off on 2026-09-30.
- Phase 4 removes only this function's old files, and only after they are under `Old repos deleted and merged/`. If the archive copy fails, do not delete. Do not delete the GitHub repository.
- New periodic jobs stay gated off. This function adds no job.

**Small test, after a build order.** In `3 - RootRecord-Website`: `git remote` names `RootRecord-Cloud` and the URL contains no token; `HEAD` is a real commit; `src/app/energy` and `src/app/home` are absent; `git check-ignore` shows the ecosystem repo ignores the checkout. That is the proof. Do not run `npm ci` again unless Alexander asks.

**Result (2026-09-30).** Folder 3 is a checkout of `rootrecordsoftwaresolutions/RootRecord-Cloud` at `84dec4a` (`84dec4ad3ecf96962dbf6e6c83ebd08c7ea78932`). `origin` is `https://github.com/rootrecordsoftwaresolutions/RootRecord-Cloud.git` with no token. `src/app/energy` and `src/app/home` are absent. The ecosystem repo ignores the checkout (`!! 3 - RootRecord-Website/`).

`site-backgrounds` (5 files) was copied unchanged to `5 - RootRecord-Library/Archive/Website-Themes/site-backgrounds/` and to `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/site-backgrounds/`. Both copies matched the source (`diff -rq`). The local old repo `online-safe-20260920` commit `00505833` deletes those files. GitHub `main` of `Solar-Pacific-RootRecord-Server` (`1dcee662`) does not contain `site-backgrounds`, so there was nothing to delete on `main`. Neither GitHub branch contains `site-backgrounds`, so there is nothing to delete on GitHub. Push of `online-safe-20260920` was rejected by GitHub push protection because an older commit on that branch (`679fd86c`) contains a secret. That protection was not bypassed, and history was not rewritten. No force-push.

Left in place and named: `~/.ollama/skills/website/site` (`RootRecord-Website`), `public-chat`, `public-edge`, `public-finance`, `public-health`, and `websites` (agents 8, 9, and 10). The Communications `RootRecord-Cloud/` tree was removed 2026-09-30 after sign-off. Folder 3 at `84dec4a` was checked first and was left in place.

Corrected: `Documentation/00-architecture/Website-RootRecord-Cloud-Staging.md`, `Communications/website/README.md`, `Communications/README.md`. No unrelated work orders were rewritten. No Vercel deploy. `repos.conf` `website` row stays disabled. `jobs.py` was not edited.

---

*Work order prepared 2026-09-30 HST. Update status when closed.*

---

## Archive / location note

This file is a draft. It is not on the active index. Do not auto-promote.

```text
Documentation/06-development/Work-Orders/drafts/Public_website_checkout_Work_Order_WO-MIG-07-2026-09-29.md
```

See `drafts/README.md` and WO-WOGEN-001. Promotion is a human decision: move it to `Documentation/06-development/Work-Orders/`, set Status OPEN or IN PROGRESS, and add a row to the index.

**Closed WOs:** set Status → COMPLETE/CLOSED → `git mv` into `Documentation/06-development/Work-Orders/Complete/`.
