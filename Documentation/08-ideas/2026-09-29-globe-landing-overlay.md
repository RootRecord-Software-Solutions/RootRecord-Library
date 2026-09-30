# Design: globe landing overlay for `www.rootrecord.cloud`

| Field | Value |
| --- | --- |
| **Date (HST)** | 2026-09-29, 14:19–14:40 HST (v1), 15:44–16:06 HST (v2: spin toggle, click info, hover, interaction fix) |
| **Requested by** | Alexander (design brief, relayed by the parent agent) |
| **Built by** | Grok (executor, globe-landing pass) |
| **State** | **v1 + v2 LANDED (desk checkout, uncommitted) / preview PASS / unit tests 16/16 PASS / AWS deploy PROPOSED, needs sign-off.** Real-browser mouse interaction (drag/zoom, click, hover over WebGL) is VERIFY PENDING, because headless Firefox paints no WebGL. **Update 16:10–16:16 HST: AWS deploy LANDED** (3 files + 1 include line, no restart) plus the AWS Ohio node; [deploy record](../07-testing/2026-09-29-globe-overlay-aws-deploy.md). The real-browser check is still VERIFY PENDING |
| **Code** | Mainland checkout `1 - Servers/2 - RootRecord-US-Mainland-Server/mirror/network-globe/network-globe/overlay/` plus one line in `index.html` and one allowlisted route block in the mirror `server.js` |
| **Test records** | v1: [2026-09-29-globe-landing-overlay-preview](../07-testing/2026-09-29-globe-landing-overlay-preview.md) · v2: [2026-09-29-globe-overlay-v2-spin-click-info](../07-testing/2026-09-29-globe-overlay-v2-spin-click-info.md) |
| **Screenshots** | `/home/rootrecord/RootRecord-Ecosystem/test-reports/Globe-Landing/`: 11 v1 PNGs, 8 `v2-*.png`, and `v2-unit-test-run.log` |
| **Backup** | `/home/rootrecord/Database/GITHUB/globe-landing.bak-20260929-141948/` (`mainland/` originals, `library/` README and worklog copies, `aws-runtime-readonly/` read-only copies of the live AWS `index.html` + `server.js`) · v2: `/home/rootrecord/Database/GITHUB/globe-overlay-v2.bak-20260929-154351/` (`mainland/` overlay + index/server + `AWS-LIVE-SERVER.md`; `library/` these docs + README + worklog; `aws-runtime-readonly/index.public.html` = live page, md5 `f3d03774…`) |
| **Related** | [US-Mainland-Server](../00-architecture/US-Mainland-Server.md) · [AWS Mainland plan](./2026-09-29-aws-mainland-improvement-plan.md) · [website staging record](../07-testing/2026-09-29-website-rootrecord-cloud-staging.md) |

## Brief

The Network Globe at `www.rootrecord.cloud` becomes the primary landing page. The full-screen interactive globe stays, with transparent glass cards over it:

1. **Sign-up card.** It is wired to the existing sign-up flow if one works; otherwise it is a clearly marked placeholder that submits nowhere.
2. **Website Home card.** It links to `rootrecord.cloud/home`, where the Vercel site will live, and stays hidden behind a flag until Vercel is ready.
3. **Quick status/health card.** It shows live desk and AWS health from existing public endpoints only, with no paths and no secrets.

Other requirements:

- Everything fits one viewport with no scrolling, on desktop and mobile.
- Every card can be closed, has a restore affordance, and its closed state is remembered in `localStorage`.
- There is an optional collapsible left rail, controlled by a flag.
- The globe stays draggable and zoomable outside the cards.
- Vanilla JS/CSS, self-contained, easy to revert.

## What exists (measured 14:19–14:30 HST)

- **Two different globe servers.** The repo mirror `server.js` is a raw `http` server with `/healthz`, `/api/state`, `/api/history`, `/api/aws` and a 404 for everything else. The **live AWS runtime** is a different **Express** `server.js` (md5 `5b5ef979…`, read-only copy in the backup): `express.static(__dirname)`, `/health` → `{status, service, uptime, flows, geo}`, `/api/state`, and `index.html` for every other path. The runtime `index.html` (`f3d03774…`) also differs from the mirror (`d512f430…`), but it has the same `.hud`, `.label` and `.help` structure, so one CSS file fits both. **The repo mirror has drifted from what runs on AWS.**
- **Sign-up.** Vercel `/login` exists (200) and posts to `https://api-goals.rootrecord.info/api/auth/signup`, which is unreachable (curl 000). `api.rootrecord.info/api/auth/me` returns 503. The Library has no memberships doc. **Decision: placeholder mode**, with `link` mode ready for when the API is back.
- **Desk health.** `rootserver.rootrecord.cloud/health` is plain text, contains a filesystem path and has no CORS, so it is **not used**. The desk's liveness is taken from the globe's own feed instead: `stats.hawaiiActiveFlows` on the mirror server, and `collector:"hawaii-feed"` + `activeFlows` on the runtime.
- **`/home`.** `rootrecord.cloud` returns 301 → `www` (this globe), so `/home` would land on the globe until Cloudflare/Vercel routing for `/home` exists. The Home card therefore stays **off**.

## Layout

```
Desktop (≥ 641 px)                                   Mobile (≤ 640 px)
┌──┬────────────────────────────────────┬────────┐   ┌──┬───────────────┐
│R │ [legacy HUD, shifted by rail]      │ Signup │   │R │ [compact HUD] │
│a │                                    ├────────┤   │a ├───────────────┤
│i │          interactive globe         │ Home*  │   │i │    globe      │
│l │  (drag / zoom everywhere outside   ├────────┤   │l │               │
│* │   the cards: overlay root has      │ Status │   │  ├───────────────┤
│  │   pointer-events:none)             │        │   │  │ Signup        │
│  │ help (moved left)       label      │  [dock]│   │  │ Home* / Status│
└──┴────────────────────────────────────┴────────┘   │  │   [+ dock]    │
 * = behind a flag                                    └──┴───────────────┘
```

- `#rr-ov` is `position:fixed; inset:0; z-index:20; pointer-events:none`. Only the cards, the rail and the dock buttons take `pointer-events:auto`, so every pixel outside a card goes to the globe canvas.
- Desktop: a 300 px right column that never grows past the viewport (`top/bottom` edges, `min-height:0`, `overflow:hidden`). On short screens (≤ 560 px tall) the card paragraphs are hidden.
- Mobile: the cards stack at the bottom (max 58 vh), the HUD becomes a 4-column compact strip, and `.label` / `.help` are hidden. Card paragraphs are hidden below 700 px height.
- Close (×) removes the card and adds a `+ <name>` pill to the **restore dock** (bottom-right on desktop, a bottom row on mobile; the column moves up when the dock is showing). State is stored in `localStorage` under `rr-globe-overlay:v1:closed:<id>`, plus `:rail` for whether the rail is open.
- Left rail (flag): 52 px of icons, 184 px when open. Menu toggles open/closed, Globe closes all cards, and Sign up / Website / Status reopen or link. The legacy HUD shifts via `--rr-rail-w`.
- Glass: `rgba(8,10,28,.46)` + `backdrop-filter: blur(14px) saturate(140%)`, 1 px light border, 16 px radius.
- Status card rows: **AWS globe node** (health + uptime), **Hawaiʻi desk stream** (live flow count), **AWS telemetry**, **Data freshness**, plus an optional **Desk health** row. Each row has a dot (ok = green, warn = amber, bad = red, grey = unknown). The footer reads "checked HH:MM:SS HST". Polling pauses while the tab is hidden or the card is closed.
- Safety: all values are written with `textContent`. `origin`, `hostname`, `account`, paths and tokens are never rendered. URLs in the config must start with `https://` or `/`. Fetches use `credentials:"omit"` and a 6 s timeout.

## Flags (`overlay/overlay-config.json`)

| Flag | Production default | Notes |
| --- | --- | --- |
| `enabled` | `true` | Master off switch, no code change needed |
| `allowUrlOverrides` | `false` | `?ov_rail / ov_home / ov_signup / ov_status = 0|1`, `?ov_reset=1`. Preview only |
| `rail.enabled` / `rail.startCollapsed` | `false` / `true` | Optional left rail |
| `legacyHud` | `compact` | `keep` / `compact` / `hide` |
| `cards.signup.enabled` / `.mode` / `.url` | `true` / `placeholder` / Vercel `/login?next=/` | Switch `mode` to `link` when the goals auth API answers |
| `cards.home.enabled` / `.url` | **`false`** / `https://rootrecord.cloud/home` | Turn on when Alexander says Vercel `/home` is routed |
| `cards.status.enabled` / `.pollSec` / `.healthUrls` / `.stateUrl` / `.deskHealthUrl` / `.staleSec` | `true` / 15 / `["/healthz","/health"]` / `/api/state` / `null` / 90 | The first health URL that returns JSON wins, so it works with both server shapes |
| `globe.spinToggle` / `.spinDefault` / `.pauseSpinWhileInfoOpen` (v2) | `true` / `on` / `true` | Stop/Resume spin pill, remembered in `localStorage` (`rr-globe-overlay:v1:spin`); `auto` = off when the OS asks for reduced motion |
| `globe.clickInfo` / `.hover` / `.showIp` / `.showProcess` (v2) | `true` / `true` / `true` (public IPs only) / `false` | Click-info card and hover highlight; the visibility rules are in the v2 section |
| `globe.stableData` / `.hardenTooltips` (v2) | `true` / `true` | Fix for the 1 s mesh re-creation, and escaped tooltips |

Runtime switches: `?overlay=0` turns the overlay off for one load, and `?embed=1` (existing) also keeps it off.

## Files

| Path (Mainland checkout, `mirror/network-globe/network-globe/`) | Change |
| --- | --- |
| `overlay/overlay.js` | new: vanilla IIFE |
| `overlay/overlay.css` | new |
| `overlay/overlay-config.json` | new: flags |
| `overlay/README.md` | new: flags, preview, deploy, revert |
| `overlay/preview-server.js`, `overlay/sample-state.json`, `overlay/test/overlay.test.js` | new, **desk preview/test only (not deployed)**. v2 added preview probe queries, a load-delay image, the allowlist-server schema, richer synthetic data (RFC 5737 IPs) and 16 jsdom tests |
| `index.html` | +1 line: `<script src="/overlay/overlay.js" defer></script>` |
| `server.js` (mirror) | +17 lines: `OVERLAY_FILES` allowlist (3 exact paths, `no-store`, `nosniff`) before the 404 |

**Revert:** delete the one line in `index.html` and the `OVERLAY_FILES` block, then `rm -r overlay/`. The originals are in the backup `mainland/`.

## Deploy to AWS: PROPOSED, needs sign-off, not run (updated 16:03 HST for v2 and the allowlist server)

The live AWS `server.js` has been the **allowlist version** since 14:43 HST (the other agent's fix; see Mainland `mirror/network-globe/network-globe/AWS-LIVE-SERVER.md`, sha256 `4ba42236…`). It serves only `/`, `/index.html`, `/health`, `/api/state` and `/overlay/overlay.js|overlay.css|overlay-config.json`; everything else returns 404.

v2 stays inside those three overlay files, so **no server change, no new route and no restart** are needed. The AWS `index.html` gets only the one include line. Re-checked read-only at 15:46 HST: AWS `index.html` md5 is still `f3d0377428a3ac467941c99a075b9d24`, `overlay/` doesn't exist yet, and `/overlay/overlay.js` returns 404.

**Do not copy the mirror `server.js`/`index.html` to AWS.**

1. `ssh rr-aws-ip "md5sum /home/ubuntu/network-globe/network-globe/index.html"` should return `f3d0377428a3ac467941c99a075b9d24`. Stop if it doesn't.
2. Take a dated backup on the host: `ssh rr-aws-ip 'B=$HOME/backups/globe-landing-$(date +%Y%m%d-%H%M%S) && mkdir -p $B && cp -a /home/ubuntu/network-globe/network-globe/index.html $B/ && echo $B'`
3. `ssh rr-aws-ip "mkdir -p /home/ubuntu/network-globe/network-globe/overlay"`, then scp **only** `overlay.js`, `overlay.css` and `overlay-config.json`. Not `preview-server.js`, `sample-state.json`, `test/` or `README.md`, which the allowlist wouldn't serve anyway.
4. Add the include line idempotently: `ssh rr-aws-ip "grep -q /overlay/overlay.js …/index.html || sed -i 's#</body>#  <script src=\"/overlay/overlay.js\" defer></script>\n</body>#' …/index.html"`
5. No restart is needed (files are read from disk per request).
6. Verify with curl:
   - `/overlay/overlay.js` gives 200 with a javascript content type.
   - `/` contains the include once.
   - The config parses as JSON.
   - `/health` returns JSON.
   - `/overlay/preview-server.js` returns 404.
7. Verify by hand in a real browser, desktop and phone:
   - Stop spin, reload: rotation stays stopped. Resume spin works.
   - Clicking an arc or a point opens the info card, with no private IPs and no process names.
   - Hover highlights the item.
   - Drag and zoom work outside the cards.
   - Esc, × and a click on empty globe close the card.
   - Cards close and restore.
8. Revert: set `enabled: false` in the config (instant). To disable only v2, set `globe.clickInfo`, `hover`, `spinToggle`, `stableData` and `hardenTooltips` to `false`. Or delete the include line, or restore the backup and `rm -r overlay`.

The exact commands are in the checkout's `overlay/README.md`.

## Findings and sign-off items

1. **[FIXED 14:43 HST by the AWS agent, re-checked 15:46 HST: 404s]** **P0 security: the live `www.rootrecord.cloud` served its app directory publicly.** The runtime has `app.use(express.static(__dirname))`. At 14:29 HST, 1-byte range requests (206) succeeded for `/server.js`, `/package.json`, `/README.md` and **`/data/hawaii.ndjson`** (the desk's network-flow feed); contents were not read beyond 1 byte. Proposed fix: replace the line with `app.use('/overlay', express.static(path.join(__dirname, 'overlay')))`, which keeps the index fallback, then restart `network-globe-web.service`. **Needs sign-off: AWS change + restart.** Not done by this pass; the other agent landed an allowlist equivalent.
2. **Repo mirror ≠ AWS runtime** (`index.html` and `server.js`). Decide which is canonical and sync them. The mirror's HUD also prints the AWS **account id** (`acct …`); the runtime currently shows "No AWS telemetry connected".
3. **Sign-up backend down** (`api-goals.rootrecord.info` unreachable, `api.rootrecord.info` 503), so the card stays a placeholder.
4. **`/home` routing.** `rootrecord.cloud/*` 301s to `www` (the globe). A Cloudflare rule or Worker for `/home*` → Vercel is needed before `cards.home.enabled: true`.
5. **Mainland checkout isn't auto-synced.** The overlay files are uncommitted there, alongside another agent's uncommitted unit/cron/README edits. This needs the `repos.conf` / manual-commit sign-off.
6. Nice-to-have: the mirror `/healthz` exposes `origin` (lat/lng label). The overlay never shows it, but the endpoint is public.
7. **(v2) Unpinned `https://unpkg.com/globe.gl`.** Both pages load whatever the latest globe.gl is; it was 2.46.2 at 16:00 HST. A major release could break the page and the overlay hooks. Pin it, e.g. `globe.gl@2.46.2`. That changes `index.html` beyond the one include line, so it needs sign-off.
8. **(v2) The page's own tooltip leaked the desk process name and used unescaped HTML** (`arcLabel`/`pointLabel` template strings). Overlay flag `globe.hardenTooltips` fixes it at runtime. The proper fix is in `index.html`.

## v2 (2026-09-29 15:44–16:06 HST): spin toggle, click info, hover highlight, interaction fix

All of v2 is inside `overlay.js`, `overlay.css` and `overlay-config.json`. It adds no server route and no second include.

**Finding the globe instance.** The AWS page (and the mirror page) declare `const globe = Globe()(document.getElementById('globe'))…` at the top level of a classic `<script>`, then set `globe.controls().autoRotate = true`. A top-level `const` is a global lexical binding: it is not `window.globe`, but other classic scripts can use it by name. The overlay is a classic deferred script that starts after the config fetch, so it can use `globe` directly. `findGlobe()` wraps the lookup in try/catch because the binding stays in TDZ if the globe.gl CDN fails. It retries every 250 ms for 10 s.

**Spin.** A `⏸ Stop spin` / `▶ Resume spin` pill leads the restore dock (bottom-right on desktop, the bottom row on phones), with a `↻ Spin on/off` rail item when the rail is on. It sets `globe.controls().autoRotate` and stores `rr-globe-overlay:v1:spin` = `on` or `off`. After a reload, the stored value overrides the page's `autoRotate = true`. Options: `spinDefault: on | off | auto` (auto means off when the OS asks for reduced motion). While an info card is open, rotation pauses without changing the stored choice (`pauseSpinWhileInfoOpen`).

**Click info.** The overlay chains onto any existing handler: `globe.onArcClick`, `onPointClick` (and `onGlobeClick` to close). A glass card appears bottom-left, beside the rail if there is one; on phones it replaces the bottom card stack until closed. It re-reads the live data every 2 s by flow key, and shows "No longer in the live snapshot" when the flow disappears.

| Field | Arc (connection) | Point |
| --- | --- | --- |
| Location | `city, country` (desk link → "Hawaiʻi ↔ Mainland") | label; coordinates rounded to 0.1°, **hidden for the origin** |
| Network / ASN | `org`, `asn` (mirror only) | up to 3 networks of flows at that point |
| IP | **public** remote IP only; private/reserved → "private (hidden)"; desk link → "hidden (desk link)"; flag `showIp` | none |
| Protocol / ports | `TCP · port 443` | up to 4 `proto port` |
| Traffic | `bytesPerSec`, `bytes`, `packets` when present (mirror schema) | sum of `bytesPerSec` |
| Flows | flows ending at the same place | flows touching the point |
| Last seen | when the overlay last saw the flow in `/api/state` (`now · HH:MM:SS HST` / `N s ago`). Neither server sends a per-flow timestamp | same |
| Never shown | process name (unless `showProcess`), `sourceNode`/`sourceRegion`, hostname, account, origin coordinates, paths. Free text is scrubbed of private IPs and path-like tokens, and all values use `textContent` | same |

**Hover.** `onArcHover` / `onPointHover` turn the item amber (arc stroke ×1.9, point radius ×1.7), matched by flow key. Pointer cursor: globe.gl adds `.clickable` once click handlers exist.

**Existing click handlers: none were broken, because none existed.** The real defect behind flaky hover, tooltips and clicks:

- `poll()` replaces `arcsData` and `pointsData` with freshly parsed objects **every 1 s**.
- three-globe's data-bind-mapper joins by **object identity**, and arcs and points have 1000 ms transitions by default.
- So every mesh was torn down and re-created each second and re-played its grow-in animation.

The overlay fixes it without touching `index.html`. `stableData` wraps `globe.arcsData` / `globe.pointsData` on the instance: for each incoming item with a known flow key it copies the new values onto the *previous* object, so identity is kept and three-globe updates the mesh in place. New flows still animate in, and vanished flows are removed. This was verified against the globe.gl 2.46.2 / three-globe 2.45.2 / data-bind-mapper source and in the unit tests (`stableId=true` in the real-library preview probe).

**Tooltip hardening** (`hardenTooltips`) is described in finding 8.

**Tests.** `overlay/test/overlay.test.js`: jsdom plus a kapsule-style globe stub, **16/16 pass**. Real globe.gl in headless Firefox was checked through the preview probe. Record: [v2 test record](../07-testing/2026-09-29-globe-overlay-v2-spin-click-info.md).



## Deploy + v3 AWS node (2026-09-29 16:09–16:17 HST)

Status: overlay deploy **LANDED** (16:10 HST); AWS-node update **LANDED** (16:16 HST); real-browser interaction **VERIFY PENDING**; AWS-side collector **PROPOSED**.

**Deploy (approved v2, 16:09–16:11 HST): LANDED, all checks PASS.**
- Backups: desk `/home/rootrecord/Database/GITHUB/globe-overlay-deploy.bak-20260929-160933/`; AWS `/home/ubuntu/backups/globe-landing-20260930-020957/` (`index.html`, md5/sha before, `ls` and service state). The deployed v2 overlay files are in `/home/ubuntu/backups/globe-landing-20260930-020957/overlay-v2-as-deployed-021621/`.
- Changes: created `$H/overlay/` with the 3 runtime files (644), and added 1 include line before `</body>`. `index.html` md5 went from `f3d03774…` to `6d9b5af6…`. No restart (`network-globe-web` MainPID 266222, active since 14:43:28 HST).
- Public checks, all PASS: overlay.js/css/config return 200 with the right MIME types and matching sha256; the include appears once on `/` and `/index.html`; `/overlay/preview-server.js`, `/overlay/sample-state.json`, `/overlay/README.md`, `/server.js` and `/data/hawaii.ndjson` all return 404; `/health` and `/api/state` return 200.
- Caching: Cloudflare/browsers cache `overlay.js` for 4 h (`max-age=14400`). The config uses `max-age=0` (DYNAMIC), so `enabled:false` reverts immediately. After the 16:16 update the edge already served the new hash (`cf-cache-status: EXPIRED`), but a returning browser can hold the old JS for up to 4 h unless hard-refreshed.
- Revert: (1) `enabled:false` in `overlay-config.json`; (2) `sed -i '\#/overlay/overlay.js#d' $H/index.html`; (3) restore `index.html` from `/home/ubuntu/backups/globe-landing-20260930-020957/` and `rm -r $H/overlay`. To undo only the AWS-node update, copy back `/home/ubuntu/backups/globe-landing-20260930-020957/overlay-v2-as-deployed-021621/*`.

**Why there were no Ohio lines (read-only check, 16:12 HST).** The live AWS `server.js` (allowlist build, sha256 `4ba42236…`) draws only the desk's own flows from `data/hawaii.ndjson`. Every record is `network-globe-telemetry` from `HawaiiRoot`. `buildState` emits one origin point (Hawaiʻi, 21.31 / -157.86) plus Hawaiʻi→destination arcs. It has no AWS point, no desk↔AWS link and no AWS-side collector. `collector.js` on AWS is the desk-side collector; no ss/tcpdump runs on AWS. `index.html` filters nothing. The overlay and the hiding rules dropped nothing: they only hide fields in the info card, and `stableData` keeps every item. The mirror `server.js` has an AWS origin and a collector, but it was never deployed.

**Fix: overlay only, deployed 16:16 HST, no restart.**
- `overlay.js` adds `withAwsPoint` and `withAwsLink`. They are pure functions in `RR_OVERLAY_UTIL`, applied before the stableData reuse.
- Point: one synthetic AWS point, Ohio 39.96 / -83.0, labelled "AWS us-east-2 · Ohio". It is skipped if the data already has a `type:aws` point, or an origin within 1°.
- Link: one arc from the desk-flow origin to Ohio (`protocol:persistent`, colour `#38bdf8`, altitude 0.28). It is skipped if any persistent arc exists or an arc already starts in Ohio. It is not drawn when there are no desk flows.
- No IP on either one. Info cards: "Desk link · Hawaiʻi desk → AWS Ohio" and "AWS region · 40, -83 · Mainland node · feed + page".
- Flag: `globe.awsNode {enabled, lat, lng, label, link, linkColor}`. Set `enabled:false` in `overlay-config.json` to switch it off (not cached).
- `/api/state` is unchanged: it still has only `origin` and `dest` point types; the AWS items are added client-side.
- Files: `overlay.js` sha256 `e08a20e2…f4c2` (md5 `24cc1906…`), `overlay-config.json` sha256 `08feebc8…6a6f`, `overlay.css` unchanged (`75b3e837…`).

**PROPOSED, not built: AWS's own flows.** A systemd timer or cron job every 30–60 s would run `ss -tunH state established` (or read `/proc/net/tcp`) and write at most 200 aggregated remote endpoints to `data/aws-conns.json`. `server.js` would merge them as Ohio-origin arcs through its existing geo cache.
- RAM: no resident daemon. Each run is a sh/awk process of about 2–5 MB for under 1 s (about 10–15 MB if written in Python); `server.js` grows by less than 1 MB.
- Do not use tcpdump: it needs root, keeps 5–10 MB resident and uses CPU, on a t3.micro with 908 MB.
- Needs a `server.js` change and a web restart, so it needs sign-off. It must also not collide with the other worker's fallback/history files.

**Tests.**
- jsdom unit tests: 18/18 PASS, including 2 new awsNode tests (point and link added once, no IP, suppressed when the data already has them). Log: `test-reports/Globe-Landing/v3-awsnode-unit-test-run.log`.
- Real globe.gl preview (AWS runtime schema, prod config), screenshots `test-reports/Globe-Landing/v3-awsruntime-desktop-1440x900-aws-link-info.png`, `…-aws-point-info.png` and `v3-awsruntime-mobile-390x844-aws-point-info.png`: both info cards render. The Source and Role values were shortened afterwards so they fit, and re-tested 18/18.
- Headless has no WebGL, so the globe canvas is blank in the screenshots. Visually confirming the Ohio line and point in a real browser is VERIFY PENDING.

Record: [07-testing/2026-09-29-globe-overlay-aws-deploy.md](../07-testing/2026-09-29-globe-overlay-aws-deploy.md)
