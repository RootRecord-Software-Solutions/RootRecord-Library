# WORK ORDER — Cloudflare workers

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-MIG-09-2026-09-29 |
| **Date** | 2026-09-29 (HST) |
| **Status** | OPEN — code landed locally. Route not attached. Deploy not signed off. |
| **Owner** | RootRecord |
| **Related** | Agent 09. Depends on 7. Public website checkout and 8. Site Cloudflare config and thumbnails. No later function depends on this one. |

**Scope:** Bring Cloudflare Workers in front of the one Vercel site, as a Communications subfolder. In scope: one worker, a path allowlist, and a timeout proxy to that site. Out of scope: the live `cloudflared` tunnel, EcoFlow polling, extra public sites, old HTML skins, deploy, DNS, D1, and any other agent's function.

---

## 1. Intent

The old function was edge code left in `cloudflare-workers`. It is not on the live server. The 2026-09-20 snapshot under `old ollama/github-history/09202026 1830/cloudflare-workers/workers/` is five Wrangler workers (`rootrecord-cloud`, `rootrecord-api`, `ava-api`, `rootmc-api`, `kilauea-public`) plus a holding config. They proxy named public paths, hide `/ops` and other private routes, and fall back to HTML holding pages. Routes cover `rootrecord.cloud`, `rootrecord.info`, `rootrecord.online`, `avaivy.cloud`, `api.rootmc.net`, and `kilauea.cloud`. Crons probe an old origin every few minutes. D1 and Hyperdrive bindings sit in the toml files.

The live system already has a poller-owned Cloudflare tunnel. That stays. EcoFlow BLE and the poller stay the energy source. This work adds one worker in front of the one Vercel site. The origin is that site. It is not `origin.avaivy.cloud` and it is not a `pages.dev` skin. Old site themes are not imported.

---

## 2. Current reality

Folder name, used in all three places: **Cloudflare-Workers**. Domain: Communications. One capitalized subfolder. No lowercase twin, no symlink, no `Logs/` directory on the server. This function is TypeScript Workers, so there is no Python package. `scripts/` is the wrangler package.

### 2.1 What exists

| Item | Location / status |
| --- | --- |
| Server code | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/Cloudflare-Workers/scripts` — landed. `src/worker.ts`, `src/publicPaths.ts`, `src/proxy.ts`, `src/envload.ts`. |
| Config | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/Cloudflare-Workers/config/wrangler.toml` — landed. No route, no cron, no account id, no D1 id. Origin var is `https://root-record-cloud.vercel.app`. |
| Database data | `2 - RootRecord-Database/Communications/Cloudflare-Workers/` — folder only. No samples imported. |
| Database logs | `2 - RootRecord-Database/Logs/Communications/Cloudflare-Workers/` — folder only. No log lines written. |
| Secret key name | `/home/rootrecord/master/master-key.env` already has `CLOUDFLARE_ACCOUNT_ID`. Allowlist that name only, same pattern as `Energy/lib/envload.py`. Never print the value. A deploy token is not in that file today. Do not add one until a deploy is signed off. Do not add a second env file. |
| Live tunnel (keep) | `Communications/network/cloudflare/` — poller starts `bin/cloudflared`. Public host `rootserver.rootrecord.cloud`. Job `cloudflare_tunnel`. Do not replace the binary, the token file, or the job. |
| Old source read | `old ollama/github-history/09202026 1830/cloudflare-workers/`. Skill desk says live git root was `Ava-Core/workers`. `Solar-Pacific-RootRecord-Server-Old` is not checked out on this machine. `node_modules` and `.wrangler-out` stay out of the live tree. |
| Public site | `3 - RootRecord-Website` is empty. Staged clone `Communications/website/RootRecord-Cloud/` is gitignored and belongs to agent 07, not this function. |
| Matrix | Library `Old-Repo-Migration-Matrix.md` row 62 now says partial, at `Communications/Cloudflare-Workers/`. |

### 2.2 Completed so far

- [x] Old source read. Five workers, shared path policy, and the live tunnel boundary are identified.
- [x] Folder name and the three paths are fixed above.
- [x] Worker source landed under `Communications/Cloudflare-Workers/`.
- [x] Local typecheck and path check passed, with no deploy.
- [x] Phase 5 result note and the two Library corrections below.
- [x] Dependency folders from agents 07 and 08 are on disk. `3 - RootRecord-Website` is the one Vercel app. `Communications/Site/config/routes.yml` keeps `www.rootrecord.cloud` on the globe and `home_card` off. No route is attached until that DNS change is signed off.
- [ ] Phase 4 archive and old-repo deletion. No `Ava-Core/workers` checkout is on this machine.

### 2.3 Known friction

- 7. Public website checkout and 8. Site Cloudflare config and thumbnails now have folders. This function does not edit them. The Site manifest still has no hostname for the Vercel app.
- The single public host and its route come from agent 08. Do not invent extra zones.
- Old wrangler files embed an account id and D1 database ids. The new config reads `CLOUDFLARE_ACCOUNT_ID` from `master-key.env` at deploy time and does not commit those ids.
- `old ollama/` copies are shared history, not this repo's working tree. Do not delete them in phase 4.

---

## 3. Tasks

1. Stop after this draft. Wait until Alexander accepts it and says to build. Until then, do not edit runtime files, restart services, send messages, actuate hardware, or spend cloud money.
2. At build time, pause if `3 - RootRecord-Website` (7. Public website checkout) is still empty, or if 8. Site Cloudflare config and thumbnails has no folder yet. Name the missing function. Do not build it.
3. Pause if `jobs.py`, the Vercel app shell, or `master-key.env` is already being edited.
4. Create `Communications/Cloudflare-Workers/` with `scripts/` and `config/` only. Mirror `Communications/Cloudflare-Workers/` under Database and under `Logs/`. Do not put logs on the server.
5. Bring and adapt `publicPaths.ts` (reads by name; writes refused except a path that is explicitly public), `proxy.ts` (timeout proxy), one `worker.ts`, and one wrangler config. The route is the single public host from agent 08. The origin is the one Vercel site.
6. Leave out old HTML skins (`maintenancePage`, `feedbackPage`, `statusPage`, and any other holding page), `ava-api`, `rootmc-api`, `kilauea-worker`, and `rootrecord-api` as extra sites, `ecoflow.ts`, the ephemeral Icecast `trycloudflare.com` radio URL, `.bak` files, and crons. Do not add a job to `jobs.py`.
7. Allowlist `CLOUDFLARE_ACCOUNT_ID` in a loader that follows `Energy/lib/envload.py`. Never print values.
8. Prove the worker locally: `tsc --noEmit` in `scripts/`, then a local wrangler dev check that a private path returns 404 and an allowlisted path is forwarded. No deploy.
9. After that check passes, phase 4: copy this function's old-repo source (not `node_modules`, not `.wrangler-out`) into `/home/rootrecord/RootRecord-Ecosystem/Old repos deleted and merged/<old-repo-name>/`, keeping the path it had inside the old repo. Generated data that lived beside that source goes into the archive too, and still does not go into the live Folders. After the archive copy is on disk, delete those same files from the old repo on this machine and on GitHub. Commit that deletion and push it. Do not force-push. Do not delete the GitHub repository. If `Ava-Core/workers` is not checked out here, record that and do not delete. If the archive copy fails, do not delete. `sql/rootmc-live.sql` is RootMC: leave it and name it here. Do not delete `old ollama/` snapshots.
10. Phase 5: add the result note in section 7 of this file (what landed, what was archived, what was removed on GitHub) and set the new status. Correct only the Library pages this function made stale: `Old-Repo-Migration-Matrix.md` row 62, and the Communications README line that lists `cloudflare-workers` as edge code separate from the poller binary. Do not rewrite unrelated work orders. Do not promote this file onto the active index until Alexander accepts it.

---

## 4. Non-goals

- Do not replace `Communications/network/cloudflare/bin/cloudflared`, `~/.cloudflared/rootserver.token`, or the `cloudflare_tunnel` job.
- Do not replace EcoFlow BLE, the poller, Hawaiʻi weather, the globe collector, camera grabs, Kokoro, or `geology_collect.py`.
- Do not port `workers/src/shared/ecoflow.ts` over the live energy poller.
- Do not import old themes, backgrounds, CSS skins, holding pages, or per-product styling into the Vercel app. Do not add a public page from this function.
- Do not stand up `avaivy.cloud`, `rootrecord.online`, `rootrecord.info` as a second site, `kilauea.cloud`, or `api.rootmc.net` from this worker.
- Do not re-import Kilauea, RootMC, Account Hub, Weather, Tokens, Business, Farms, Goals, or Ava Ops.
- Do not edit another agent's files. `sql/rootmc-live.sql` stays for RootMC.
- Do not import logs, samples, last-state files, generated reports, collected images, database dumps, caches, virtualenvs, `node_modules`, or `__pycache__` into Pacific, Database, the website, or git.
- Do not add a periodic job. Crons stay off. Do not edit `jobs.py`.
- Do not restore files under `~/.ollama/skills/energy`, automations, or `coms/ssh/local-data-globe`.
- Do not delete a whole GitHub repository. Do not force-push.

---

## 5. Key file / path reference

| Path | Role |
|------|------|
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/Cloudflare-Workers/scripts/` | Worker package: `package.json`, `tsconfig.json`, `src/worker.ts`, `src/publicPaths.ts`, `src/proxy.ts`. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/Cloudflare-Workers/config/` | One wrangler toml. No route, no baked account id, no D1 ids. |
| `2 - RootRecord-Database/Communications/Cloudflare-Workers/` | Data: samples, last files, stores. |
| `2 - RootRecord-Database/Logs/Communications/Cloudflare-Workers/` | Logs only. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Energy/lib/envload.py` | Pattern for the allowlist loader. Key name: `CLOUDFLARE_ACCOUNT_ID`. |
| `/home/rootrecord/master/master-key.env` | Only secret file. Do not edit it in this draft. Do not commit it. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/network/cloudflare/` | Live tunnel. Do not overwrite. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Automations/scripts/jobs.py` | Shared. Do not edit. Pause if another agent is editing it. |
| `3 - RootRecord-Website` | Agent 07. Checked out. This function adds no page here. |
| `old ollama/github-history/09202026 1830/cloudflare-workers/` | Read-only snapshot of the old function. Not the phase 4 delete target. |
| `Old repos deleted and merged/<old-repo-name>/` | Phase 4 archive, after the migration works. |
| `5 - RootRecord-Library/Documentation/00-architecture/Old-Repo-Migration-Matrix.md` | Row 62. Correct in phase 5 only. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/README.md` | Edge-workers line. Correct in phase 5 only. |

---

## 6. Open items

**Additional requirements:**

- Sign-off before `wrangler deploy`, attaching a route, creating D1, changing DNS, or any other Cloudflare spend.
- Sign-off before sends, speaker playback, OBS, hardware switching, or deletion of live Ecosystem files. Phase 4 deletion is only the old function's files, and only after the archive copy is on disk.
- Small test that proved the new behavior (2026-09-30 HST): `tsc --noEmit`, then `node dist/check.js`. Private `/ops` is 404 and was not forwarded. `GET /status` was forwarded to `https://root-record-cloud.vercel.app/status`. No `wrangler dev` and no deploy. `wrangler dev` stays off until the route from agent 08 exists.
- Both dependency folders are on disk. The Site manifest still has no hostname for this worker, so the route stays off.

---

## 7. Notes & constraints

- No force-push.
- Secrets stay out of git. Never print `master-key.env` values. Never commit the account id or D1 ids from the old toml.
- Prefer small reversible steps.
- New code wins. If a newer worker already exists under `Communications/Cloudflare-Workers/` at build time, enhance that version. Do not copy the five old workers over it.
- One Vercel site. Workers sit in front of it. Data and logs stay on the Database paths in section 2.
- Phase 4 result (2026-09-30 HST):
  - Landed: `Communications/Cloudflare-Workers/scripts` and `config/wrangler.toml`. Origin is `https://root-record-cloud.vercel.app`. `tsc --noEmit` passed. `node dist/check.js` passed: `/ops` and `/api/finance` are 404 and were not forwarded; `POST /status` is 405; `GET /status` and `GET /api/solar` were forwarded to that origin. `CLOUDFLARE_ACCOUNT_ID` is present. The value was not printed. No `wrangler deploy`.
  - Route: still unbound. `3 - RootRecord-Website` and `Communications/Site` are on disk. `routes.yml` keeps `www.rootrecord.cloud` on the globe and `home_card` off, so this worker does not take a hostname.
  - Archived: nothing. `Ava-Core/workers` is not checked out on this machine. `Solar-Pacific-RootRecord-Server-Old` is not checked out. The `old ollama/` snapshot was left in place.
  - Removed on GitHub: nothing. No deletion, no push, no force-push. `sql/rootmc-live.sql` was left for RootMC.
- This file stays in `drafts/`. It is not on the active index.

---

*Work order prepared 2026-09-29 HST. Update status when closed.*

---

## Archive / location note

**Active / accepted WOs** — filename when saved:

```text
Cloudflare_workers_Work_Order_WO-MIG-09-2026-09-29.md
```

This file is a draft. It is not accepted for execution. Do not move it to the active index until Alexander accepts it.

Location while draft:

```text
Documentation/06-development/Work-Orders/drafts/
```

See `drafts/README.md` and WO-WOGEN-001. Do not auto-promote.

**Closed WOs:** set Status → COMPLETE/CLOSED → `git mv` into:

```text
Documentation/06-development/Work-Orders/Complete/
```

Human session logs archive under `Documentation/01-operations/archive/YYYY-Www/` (WO-ARCH) — separate from closed work orders.
