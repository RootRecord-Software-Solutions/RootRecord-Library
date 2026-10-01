# Website staging — RootRecord-Cloud (Vercel) in Pacific `Communications/website/`

| Field | Value |
| --- | --- |
| **Date (HST)** | 2026-09-29 14:01–14:15 HST |
| **Author** | Grok (executor, website-staging pass) for Alexander |
| **State** | Folder removed 2026-09-30. Do not start it again. The 2026-09-29 Communications tree was removed the same day. Live data proxy **FAIL** (origin 530). Deploy and Vercel settings **not touched**. Auto-sync stays **off**. |
| **Repo** | `rootrecordsoftwaresolutions/RootRecord-Cloud` (`main` @ `84dec4a`, 2026-09-28 18:39 HST) |
| **Checkout** | Folder removed 2026-09-30. Do not start it again. |
| **Leftover snapshot** | Removed 2026-09-30 from `Communications/website/RootRecord-Cloud/`. It had no `.git`. There is no desk checkout. |
| **Pacific-tracked** | `Communications/website/README.md`, `Communications/website/.env.example` (names only), `.gitignore` entry, `Communications/README.md` row |
| **Test record** | [07-testing/2026-09-29-website-rootrecord-cloud-staging.md](../07-testing/2026-09-29-website-rootrecord-cloud-staging.md) |
| **Backup** | `/home/rootrecord/Database/GITHUB/website-staging.bak-20260929-140240/` |

## What the repo is

"This repository owns the Vercel web project for `rootrecord.cloud`" (`AGENTS.md`). 50 tracked files, 1.2 MB working tree (of which `src/lib/blogPosts.ts` 659 KB, `media/banner.jpg` 177 KB).

| Item | Value |
| --- | --- |
| Framework | **Next.js 15** App Router + TypeScript (`next ^15.3.0` → 15.5.23 from lockfile, React 19.2.8, TS 5.9.3); `package.json` name `rootrecord-online` |
| Scripts | `dev` (`next dev --port 3001`), `build`, `start`, `lint`. No `postinstall` / `postbuild` hooks |
| `vercel.json` | `{"framework": "nextjs"}` only — no rewrites, crons, regions or headers |
| `next.config.ts` | empty config (comment: `/api/*` handled in-app, no external rewrite) |
| Deploy | **Vercel Git integration**: GitHub deployments by `vercel[bot]`, environment *Production*, latest `84dec4a` 2026-09-28 18:41 HST, status `Vercel success`. **Any push to `main` = production deploy** |
| Pages | `/` (dashboard, dynamic), `/blog` + 280 `/blog/[slug]` SSG posts, `/dev`, `/goals` (+ `[id]`, `new`), `/login`, `/reports`, `/status`, `/timeline` |
| API routes | `/api/[...path]` — allowlisted GET proxy (22 exact paths + photo/media prefixes) to the desk origin; `/api/auth/session` → account API `/api/auth/me` with the `ava_session` cookie/Bearer; `/api/chat` → origin `/api/chat` with a static fallback reply |
| Helper | `scripts/auto-push.py` — **commits and pushes to `origin main`** (Windows-era helper; would trigger a production deploy). Never run it from the desk |
| Own `.gitignore` | `node_modules/ .next/ out/ .vercel/ .env .env.* !.env.example *.log` |
| Upstream `.env.example` | comments only (mentions `AVA_ORIGIN_URL`) |

### Environment variables (names only — all optional, all have code defaults, none secret today)

| Name | Side | Default in code | Used in |
| --- | --- | --- | --- |
| `AVA_ORIGIN_URL` | server | `https://origin.avaivy.cloud` | `desk-api.ts`, `/api/[...path]`, `/api/chat` |
| `AVA_PUBLIC_API` | server | — (falls back to origin) | `desk-api.ts` |
| `NEXT_PUBLIC_AVA_API` | browser (build-inlined) | unset ⇒ same-origin `/api/*` | `desk-api.ts` |
| `NEXT_PUBLIC_GOALS_API` | browser | `https://api-goals.rootrecord.info` | `goals-api.ts` |
| `NEXT_PUBLIC_ACCOUNT_API` | browser + server | `https://api.rootrecord.info` | `AuthBar.tsx`, `/api/auth/session` |
| `ROOTRECORD_API_ACCOUNT_URL` | server | → `NEXT_PUBLIC_ACCOUNT_API` | `/api/auth/session` |

Listed in Pacific `Communications/website/.env.example`. Real values belong only in Vercel project settings (not inspected — no Vercel CLI/token used).

## Staging decision — Option B (own clone, gitignored in Pacific)

| Consideration | Option A (copy files into Pacific) | **Option B (nested clone, ignored)** |
| --- | --- | --- |
| Deploy source | Pacific copy would **not** deploy; two sources of truth drift | Same repo Vercel deploys from; history kept |
| Pacific ignore rules | `*.jpg` drops `media/banner.jpg`; `node_modules/.next` need new rules | Site keeps its own `.gitignore` |
| Auto-sync risk | Every site edit churns Pacific commits | Nested `.git` excluded **before** clone (else `git add -A` would record an embedded gitlink) |
| Existing folder | `Communications/website/` was **empty** (created 13:28 HST today) | Nothing to move or delete; README + `.env.example` tracked beside the clone |

Pacific precedent: `us-mainland-server/` was excluded from Pacific as its own repo, and `repos.conf` already models the site as a separate repo (`website` row, disabled). Order used: `.gitignore` entry → `git check-ignore` verified → `git clone`.

## Build / smoke (details in the test record)

`npm ci --ignore-scripts` 30 packages in 8 s (506 MB `node_modules`); `npm run build` 33 s wall, compiled + type-checked, **293 static pages**, First Load JS 103–142 kB; min MemAvailable 5.7 GB. `next start` on 127.0.0.1:3099 for ~5 s: `/`, `/blog`, `/status` 200; `/api/not-allowed` 404 (allowlist works); `/api/health` **530** passed through from `origin.avaivy.cloud` → server stopped, port closed. The build did not modify any tracked file in the clone.

## Live-surface findings (read-only)

1. `https://root-record-cloud.vercel.app` → **200** (Vercel site up).
2. `https://rootrecord.cloud` → **301 → `https://www.rootrecord.cloud`** → **530 (Cloudflare 1033)**. `www.rootrecord.cloud` is routed to the **AWS Network Globe tunnel** (`US-Mainland-Server/mirror/.cloudflared/config-globe.yml`), whose connector is down (see [US-Mainland-Server](./US-Mainland-Server.md)). So the public domain does not reach the Vercel site today, contrary to `AGENTS.md`.
3. `origin.avaivy.cloud` → **530**: no connector; every desk-data panel on the live site shows `OFFLINE` (by design, no invented numbers).
4. The desk tunnel (`cloudflared` PID 105450) serves `rootserver.rootrecord.cloud` → poller `:8799`: `/health` 200 (plain-text ENERGY line, includes a Database filesystem path), `/api/health` and `/api/status` 404 — it does **not** implement the `/api/*` JSON contract the site expects, so `AVA_ORIGIN_URL` cannot simply be repointed there.

## Auto-sync (not changed)

`repos.conf` row `website 0 mirror /home/rootrecord/.ollama/skills/website/site rootrecordsoftwaresolutions/RootRecord-Website origin` refers to a **different** repo (RootRecord-Website) and a G2 path. If Alexander wants desk edits of this site to sync, the row would be:

```text
cloud	0	inplace	/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/website/RootRecord-Cloud	rootrecordsoftwaresolutions/RootRecord-Cloud	origin
```

Recommended to keep it **disabled (`0`)**: with `1`, every desk edit would auto-push to `main` = **Vercel production deploy**. Also, `push-repo-once.sh` `is_runtime_code_tree()` matches any path containing `RootRecord-Pacific-Solar-Server`, so a pull into this nested clone would **arm a Pacific poller stack reload** — exclude `*/Communications/website/*` there first if the row is ever enabled.

## Sign-off items

1. `www.rootrecord.cloud`: Vercel domain (site) vs AWS globe tunnel — pick one; today neither serves it.
2. Desk origin for live data: revive `origin.avaivy.cloud` or build the `/api/*` contract on `rootserver.rootrecord.cloud`, then set `AVA_ORIGIN_URL` in Vercel.
3. Auto-sync row for the clone (above) — keep disabled unless deploy-on-edit is wanted; fix `is_runtime_code_tree` first.
4. Retire or guard `scripts/auto-push.py` (upstream change — needs a push = deploy).
5. `rootserver.rootrecord.cloud/health` exposes a filesystem path publicly (minor).

*Website staging 2026-09-29 HST.*
