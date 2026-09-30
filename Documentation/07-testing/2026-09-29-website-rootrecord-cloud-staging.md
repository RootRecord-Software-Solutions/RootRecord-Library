# Test record — RootRecord-Cloud website staging (clone, npm ci, production build, brief start)

| Field | Value |
| --- | --- |
| **Date / time (HST)** | 2026-09-29 14:02–14:08 HST |
| **Tester** | Grok (executor, website-staging pass) |
| **Change under test** | Pacific `.gitignore` entry `Communications/website/RootRecord-Cloud/` + nested clone of `rootrecordsoftwaresolutions/RootRecord-Cloud` @ `84dec4a`. [Architecture](../00-architecture/Website-RootRecord-Cloud-Staging.md) |
| **State** | Clone + ignore **PASS** · `npm ci` **PASS** · `npm run build` **PASS** · `next start` smoke **PASS** · origin data **FAIL** (530, external) |
| **Evidence** | this record (outputs quoted); logs were in `/tmp/rr-website-*.log` (not kept) |
| **Commits** | see worklog *website-staging pass* |
| **Backup** | `/home/rootrecord/Database/GITHUB/website-staging.bak-20260929-140240/` (empty-folder listing, Pacific `.gitignore`, `Communications/README.md`, Library 07 README + worklog) |

## What was tested

1. The nested clone is invisible to Pacific git (no gitlink, no files) while `README.md` / `.env.example` beside it stay trackable.
2. Dependencies install from the lockfile without lifecycle scripts, within the memory limit.
3. Production build compiles and type-checks.
4. The built app serves pages locally and the `/api` allowlist behaves; then everything is stopped.

## How (exact commands / procedure)

```bash
# Pacific .gitignore += Communications/website/RootRecord-Cloud/   ; git check-ignore -> IGNORED (.git/HEAD, package.json, node_modules/x); README.md tracked
cd ".../Communications/website" && git clone https://github.com/rootrecordsoftwaresolutions/RootRecord-Cloud.git RootRecord-Cloud
git -C ".../Pacific" status --short --ignored -- Communications/website   # !! RootRecord-Cloud/
export NEXT_TELEMETRY_DISABLED=1
/tmp/rr-memwatch-run.sh <log> npm ci --ignore-scripts --no-audit --no-fund      # setsid + nice 10; kill group if MemAvailable < 2048 MB
/tmp/rr-memwatch-run.sh <log> npm run build
setsid nice -n 10 ./node_modules/.bin/next start -H 127.0.0.1 -p 3099 &   # curl / /blog /status /api/health /api/not-allowed ; kill group
```

## Pass criteria (written before running)

1. `git status --ignored` in Pacific shows the clone only as `!!`; nothing from it staged or committed.
2. `npm ci` exit 0; MemAvailable never < 2 GB.
3. `npm run build` exit 0 with route table; no tracked file in the clone modified.
4. Local pages return 200; a non-allowlisted `/api` path returns 404; no server process or port left.

## Result

| # | Result | State |
| --- | --- | --- |
| 1 | `!! Communications/website/RootRecord-Cloud/`; Pacific HEAD has 0 paths under it (`git ls-tree … \| grep -c RootRecord-Cloud` = 0) | **PASS** |
| 2 | 30 packages in 8 s (9.05 s wall), `node_modules` 506 MB, min MemAvailable 6,497 MB, peak RSS 283 MB (measured on the wrapper tree) | **PASS** |
| 3 | Next.js 15.5.23 "Compiled successfully in 9.7s", types valid, 293/293 static pages, 33.2 s wall, `.next` 113 MB, min MemAvailable 5,737 MB, peak RSS 505 MB, load after 4.48 (1 min); clone `git status` clean | **PASS** |
| 4 | `/` 200 (12.7 kB, 0.31 s), `/blog` 200, `/status` 200, `/api/not-allowed` 404 `{"detail":"not found"}`, `/api/health` **530** (upstream `origin.avaivy.cloud` has no tunnel connector); server killed, `pgrep` none, port 3099 closed | **PASS** (app) · origin **FAIL** (external) |

Read-only live checks: `root-record-cloud.vercel.app` 200; `rootrecord.cloud` 301 → `www.rootrecord.cloud` 530 (routed to the AWS globe tunnel, down); GitHub deployments: `vercel[bot]` Production `84dec4a` success.

## Resource impact

| When | Load (1/5/15) | MemAvailable | Swap used | Peak RSS |
| --- | --- | --- | --- | --- |
| before (14:02) | not recorded | 6,624 MB | 491 MB | — |
| during npm ci | 1.69 / 1.42 / 1.60 (end) | min 6,497 MB | not recorded | 283 MB |
| during build | 4.48 / 2.12 / 1.82 (end) | min 5,737 MB | not recorded | 505 MB |
| after | see worklog | see worklog | — | — |

## Cleanup confirmation

- [x] no test process left (`next start` group killed; `pgrep -af "next start|next-server"` = none)
- [x] port 3099 closed; temp outputs removed
- [x] no deploy, no push, no Vercel CLI, no model, no sudo, no restart; `scripts/auto-push.py` not run
- [ ] `node_modules/` (506 MB) and `.next/` (113 MB) **kept** in the ignored clone for the next build (delete with `rm -rf node_modules .next` inside the clone if disk is needed)

## Open items / caveats

- Live desk data on the site is OFFLINE until an origin answers the `/api/*` contract (sign-off).
- `www.rootrecord.cloud` routing decision (Vercel vs AWS globe).
- `npm` reported no audit (disabled with `--no-audit`); run `npm audit` separately if wanted (network, read-only).
