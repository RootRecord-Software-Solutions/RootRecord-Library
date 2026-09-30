# WORK ORDER — Desk product apps not imported

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-MIG-14-2026-09-29 |
| **Date** | 2026-09-29 (HST) |
| **Status** | OPEN — pages landed; deletion is on the remote-tracking branch |
| **Owner** | RootRecord |
| **Related** | Agent 14. Depends on 7. Public website checkout. No later function depends on this one. Template: `Documentation/01-operations/templates/TEMPLATE Work Order.md`. Globe: `Documentation/08-ideas/2026-09-29-globe-landing-overlay.md`. |

**Scope:** Bring the seven unimported desk apps (clients, companions, fern-forest, finance-desk, pantry, product-prices, look) into one `Products` folder: source and prompts on Pacific, empty stores under Database, four glass-card pages on the one Vercel site. Old themes go to the Library theme archive, not into the Vercel build. Runtime stores, camera grabs, companion process starts, and Stripe calls stay out. This file is the before-documentation. It is not on the active index.

---

## 1. Intent

The old function is seven skill folders at the root of `/home/rootrecord/old ollama/old skills` (remote `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server`). They never landed under Android or the website.

- **Clients** is a web-dev gig desk, not memberships. One static site lives at `clients/gigs/nibble.love/`. That skill’s own rule is not to dump client sites into RootRecord product sites.
- **Companions** starts optional Ava companion processes and an Electron Dev-Desk. Those scripts can reach Discord, Slack, and Telegram.
- **Fern Forest** is a parcel reference for three Leila Road TMKs. The county PDFs hold owner names and mailing addresses. Power numbers are not in those files.
- **Finance desk** builds a ledger payload through `apps.core.services.public_finance` and `stripe_poll`, and holds BM SQLite scripts that take `--db` outside the skill.
- **Pantry** logs shelf counts through `scripts/pantry.py` into `store/stock.json`. It does not invent items.
- **Product prices** stores shelf prices in `store/prices.json` and appends `store/sightings.jsonl`. It does not invent prices.
- **Look** captions USGS and NHC stills with Moondream, and includes a Night Owl DVR grabber.

The live system already runs EcoFlow BLE, the poller, Hawaiʻi weather, the globe collector, camera grabs, Kokoro, and `geology_collect.py`. Those stay as they are. This work order does not replace them.

Public pages, when the build is allowed, use the US-Mainland globe direction: full-screen dark globe, glass cards, one viewport. Each app’s old theme stays out of the Vercel app.

---

## 2. Current reality

### 2.1 What exists

| Item | Location / status |
| --- | --- |
| Folder | **Products**. Installed. One capitalized folder. Python package name `Products`. No lowercase twin and no symlink. |
| Server code | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Products/scripts/` — landed |
| Database data | `2 - RootRecord-Database/Products/` — empty stores landed |
| Database logs | `2 - RootRecord-Database/Logs/Products/` — directory only |
| Subfolders (same name in all three places) | `Clients`, `Companions`, `FernForest`, `FinanceDesk`, `Pantry`, `ProductPrices`, `Look` |
| `master-key.env` | No keys for this function. Do not add an allowlist entry. Do not read values. Store paths are constants under the Database folder. |
| Keys that stay out | `PANTRY_STORE`, `PRODUCT_PRICES_DIR`, `DVR_IP`, `DVR_USER`, `DVR_PASS`, `DVR_CHANNELS`, `DVR_STREAM`, and every `AVA_*` / Discord / Slack / Telegram token used by the old companion scripts |
| Old source | Removed from `/home/rootrecord/old ollama/old skills`. Archive copy is under `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/`. |
| Public website checkout | `3 - RootRecord-Website` is empty. Agent 07 has not put the one Vercel app there. |
| Theme archive | `5 - RootRecord-Library/Archive/Website-Themes/clients/gigs/nibble.love/` and `companions/dev-desk/renderer/styles.css` |
| `jobs.py` | Live. This function does not edit it and does not add a job. |

These apps do not belong inside Energy, Geology, Weather, Reports, Security, Communications, System, or Media.

### 2.2 Completed so far

- [x] Old source read. Folder name and the three paths chosen.
- [x] This draft written.
- [x] Alexander said to complete the work.
- [x] `7. Public website checkout` is the Vercel app in `3 - RootRecord-Website`.
- [x] `Products` source, empty Database stores, theme archive, and four glass-card routes: `/clients`, `/fern-forest`, `/pantry`, `/product-prices`.
- [x] Small test: empty pantry prints `empty on file`. Product-prices lookup of "sour patch" prints `{}` and exits 1.
- [x] Phase 4 archive is on disk. The seven directories are gone from the old clone. Commit `3d54403b` is an ancestor of `origin/online-safe-20260920` at `0e3ebe2b`.
- [x] Result note below. Library pages this function made stale are corrected. This file stays in drafts.

### 2.3 Known friction

- Public website checkout now fills `3 - RootRecord-Website`. This work order did not check that site out and did not edit the gitignored RootRecord-Cloud clone under Communications.
- `finance_desk.py` and `look.py` import `apps.core`, which is outside these seven directories. That tree stays. Finance and Look source is copied for archive, and is not wired into a running path.
- Fern Forest PDFs and text extracts contain owner names and mailing addresses. The public card does not show them.
- `clients/references/gigs.md` names a person on the nibble.love about page. The public clients card lists the gig domain and page names only.
- `look/store/camera-dvr/CONNECTION.json` and companion `telegram-context.json` files hold connection material. They are not copied into Pacific, Database, the website, or git. They ride along only in the phase 4 archive of the old repo.
- Pantry `store/stock.json` and product-prices `store/prices.json` plus `sightings.jsonl` are runtime output. The new stores start empty. Those files are archived in phase 4 and are not imported.

---

## 3. Tasks

1. Stop here until Alexander accepts this draft and says to build. Until then, do not edit runtime files, restart services, send messages, actuate hardware, or spend cloud money.
2. At build time, pause if `3 - RootRecord-Website` is still empty. Name the missing function: Public website checkout. Do not build it. Do not scaffold a second Vercel app. Pause if `jobs.py`, the Vercel app shell, or `master-key.env` is already being edited.
3. Add `Products/scripts/` with source and prompts only.
   - Pantry CLI, retargeted to `2 - RootRecord-Database/Products/Pantry/`. Leave the store empty. Do not read `PANTRY_STORE`.
   - Product-prices CLI, retargeted to `2 - RootRecord-Database/Products/ProductPrices/`. Leave the store empty. Do not read `PRODUCT_PRICES_DIR`.
   - Fern Forest public facts only: TMK, lot, acreage, and the public qPublic link. No owner name, no mailing address, no watts.
   - Clients gig index from the gig table: domain and page list. Do not rehost nibble.love.
4. Copy companion, finance, and look source into `Products/scripts/Companions/`, `Products/scripts/FinanceDesk/`, and `Products/scripts/Look/` so the old repo can be archived later. Do not import them into a running path. Do not start companion processes. Finance scripts keep `--db` outside the folder. Do not copy sqlite dumps. Do not copy `stock.json`, `prices.json`, `sightings.jsonl`, DVR frames, `CONNECTION.json`, or `telegram-context.json` into Pacific, Database, the website, or git.
5. Add four glass-card routes on the one Vercel app in `3 - RootRecord-Website`: Clients, Fern Forest, Pantry, Product prices. Visual direction is the globe overlay (dark full-screen globe, glass cards, one viewport). Data and logs stay under the Database paths above. Do not build Companions, Finance, or Look pages.
6. Copy these themes unchanged into `5 - RootRecord-Library/Archive/Website-Themes/` and keep that archive out of the Vercel build:
   - `clients/gigs/nibble.love/` (HTML, CSS, JS)
   - `companions/dev-desk/renderer/styles.css`
7. Small test, no network and no jobs: the pantry script on an empty store prints an empty pantry; a product-prices lookup returns no price.
8. After that works, archive the seven repo-root directories into `/home/rootrecord/RootRecord-Ecosystem/Old repos deleted and merged/Solar-Pacific-RootRecord-Server/`, keeping `clients/`, `companions/`, `fern-forest/`, `finance-desk/`, `pantry/`, `product-prices/`, and `look/`. Generated data beside that source goes into the archive too, and still does not go into the live Folders. Then delete only those paths in the old clone and on GitHub. Commit that deletion and push it. Do not force-push. Do not delete the GitHub repository. If the archive copy fails, do not delete.
9. Shared files left in the old repo, named here: anything under `apps.core` (imported by `finance_desk.py` and `look.py`) and any Ava-Core tree the companion scripts exec. Those are not inside the seven directories.
10. Update this same work order with what landed, the archive path, and the GitHub deletion. Correct only Library pages this function made stale.

---

## 4. Non-goals

- Do not build Public website checkout, and do not edit another agent’s files.
- Do not overwrite EcoFlow BLE, the poller, Hawaiʻi weather, the globe collector, camera grabs, Kokoro, or `geology_collect.py`.
- Do not edit `jobs.py`. No new periodic job.
- Do not add a second website, and do not put old CSS, backgrounds, or per-product skins in the Vercel app.
- Do not rehost nibble.love. Do not publish Fern Forest owner names or mailing addresses. Do not publish watts from the parcel PDFs.
- Do not start companion processes, call Stripe, or run the DVR grabber or a Moondream cam poller.
- Do not import runtime JSON, sqlite dumps, DVR frames, caches, virtualenvs, `node_modules`, or `__pycache__` into Pacific, Database, the website, or git.
- Do not re-import Android apps already in `6 - Android Development` (Kilauea, RootMC, Account Hub, Weather, Tokens, Business, Farms, Goals, Ava Ops).
- Do not delete a whole GitHub repository. Do not delete live Ecosystem files. Do not restore files under `~/.ollama/skills/energy`, automations, or `coms/ssh/local-data-globe`.

---

## 5. Key file / path reference

| Path | Role |
| --- | --- |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Products/scripts/` | New server code. Package name `Products`. No `config/`. No server `Logs/`. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Products/scripts/Pantry/` | Pantry CLI, empty-store path constant |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Products/scripts/ProductPrices/` | Product-prices CLI, empty-store path constant |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Products/scripts/FernForest/` | Public parcel facts only |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Products/scripts/Clients/` | Gig index only |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Products/scripts/Companions/` | Source copy. Not a running path. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Products/scripts/FinanceDesk/` | Source copy. Not a running path. `--db` stays outside. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Products/scripts/Look/` | Source copy. Not a running path. No grabber. |
| `2 - RootRecord-Database/Products/Pantry/` | Empty pantry store |
| `2 - RootRecord-Database/Products/ProductPrices/` | Empty prices store |
| `2 - RootRecord-Database/Products/FernForest/` | Public facts file. No PII PDFs in git. |
| `2 - RootRecord-Database/Logs/Products/` | Logs only, created when the build runs |
| `3 - RootRecord-Website` | Four glass-card routes, after checkout exists |
| `5 - RootRecord-Library/Archive/Website-Themes/` | Unchanged nibble.love tree and Dev-Desk `styles.css` |
| `/home/rootrecord/old ollama/old skills/clients/` | Old gig desk and nibble.love theme |
| `/home/rootrecord/old ollama/old skills/companions/` | Old companion starters and Dev-Desk |
| `/home/rootrecord/old ollama/old skills/fern-forest/` | Old parcel PDFs and text |
| `/home/rootrecord/old ollama/old skills/finance-desk/` | Old ledger helper and BM SQLite scripts |
| `/home/rootrecord/old ollama/old skills/pantry/` | Old pantry script and `store/stock.json` |
| `/home/rootrecord/old ollama/old skills/product-prices/` | Old prices script and store files |
| `/home/rootrecord/old ollama/old skills/look/` | Old `look.py` and DVR grabber |
| `Old repos deleted and merged/Solar-Pacific-RootRecord-Server/{clients,companions,fern-forest,finance-desk,pantry,product-prices,look}/` | Phase 4 archive, after the migration works |
| `/home/rootrecord/master/master-key.env` | Not used. No new key names. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Automations/scripts/jobs.py` | Not edited |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Energy/lib/envload.py` | Pattern only: allowlist, never print values, no second env file |

---

## 6. Open items

**Additional requirements:**

- The four glass-card routes are committed on the website repo as `74df825`. That commit is not pushed.
- The first push of `3d54403b` was rejected by push protection on older commit `679fd86c`. Do not force-push and do not allow-list that secret. The remote-tracking branch `origin/online-safe-20260920` is now `0e3ebe2b`, which contains that deletion and does not contain the seven directories.
- This file stays in drafts until a human promotes it.

---

## 7. Notes & constraints

- No force-push.
- Secrets stay out of git. This function adds no `master-key.env` keys.
- Prefer small reversible steps.
- Sign-off gates: do not send messages, play audio, touch OBS, switch hardware, delete live Ecosystem files, or spend cloud money. Do not start companion processes, call Stripe, or run the DVR grabber. Phase 4 deletes old-repo files only, and only after the archive copy is on disk. If the archive copy fails, do not delete.
- Small test that proves the new behavior: pantry script on an empty Database store prints an empty pantry; product-prices lookup on an empty store returns no price. No network. No jobs.
- Phase 4 result:
  - Landed: `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Products/` (Pantry, ProductPrices, FernForest, Clients run; Companions, FinanceDesk, and Look are source copies and are not started). Empty stores under `2 - RootRecord-Database/Products/`. Logs directory `2 - RootRecord-Database/Logs/Products/`. Themes in `5 - RootRecord-Library/Archive/Website-Themes/clients/gigs/nibble.love/` and `.../companions/dev-desk/renderer/styles.css`.
  - Landed after checkout: glass-card routes `/clients`, `/fern-forest`, `/pantry`, and `/product-prices` on the one Vercel app in `3 - RootRecord-Website`. Production build lists all four. Pantry shows “Empty on file.” Product prices show “No price on file.” Fern Forest shows the three TMKs and qPublic links. Clients lists nibble.love and does not rehost it.
  - Archived: `/home/rootrecord/RootRecord-Ecosystem/Old repos deleted and merged/Solar-Pacific-RootRecord-Server/{clients,companions,fern-forest,finance-desk,pantry,product-prices,look}/`. File counts matched the old tree before deletion (15, 36, 11, 11, 9, 6, 8).
  - Removed on this machine: those seven directories in `/home/rootrecord/old ollama/old skills`, commit `3d54403b` on `online-safe-20260920` (94 tracked files). `apps.core` and Ava trees were not in those directories and were left.
  - GitHub: the direct push was rejected (push protection on older commit `679fd86c`, an OpenAI API key in `ecosystem-history/references/archives-pull-20260916/august-emergency-txt/chatgpt improvements.txt`). The secret was not allow-listed and the repository was not deleted. Later, `origin/online-safe-20260920` points at `0e3ebe2b`, which includes `3d54403b`. That tip does not contain the seven directories.
  - Runtime files that were not tracked (`pantry/store/stock.json`, `product-prices/store/prices.json`, `product-prices/store/sightings.jsonl`, `look/store/camera-dvr/`) are in the archive and are gone from the old working tree. They were not in the GitHub tree at HEAD, so the deletion commit does not include them. They were not copied into Pacific, Database, or the website.

---

*Work order prepared 2026-09-29 HST. Update status when closed.*

---

## Archive / location note

**Draft (not on the active index):**

```text
Desk_product_apps_not_imported_Work_Order_WO-MIG-14-2026-09-29.md
```

Location:

```text
Documentation/06-development/Work-Orders/drafts/
```

Do not auto-promote. See `drafts/README.md` and WO-WOGEN-001.

**Active / accepted WOs** move to `Documentation/06-development/Work-Orders/` only after a human accepts this draft.

**Closed WOs:** set Status → COMPLETE/CLOSED → `git mv` into `Documentation/06-development/Work-Orders/Complete/`.
