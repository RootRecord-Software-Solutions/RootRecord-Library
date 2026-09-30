# Design: globe landing overlay for `www.rootrecord.cloud`

| Field | Value |
| --- | --- |
| **Date (HST)** | 2026-09-29, 14:19–14:40 HST |
| **Requested by** | Alexander (design brief, relayed by the parent agent) |
| **Built by** | Grok (executor, globe-landing pass) |
| **State** | **LANDED (desk checkout, uncommitted) / preview PASS / AWS deploy PROPOSED, needs sign-off.** Interactive drag/zoom is VERIFY PENDING in a real browser (headless Firefox shows no WebGL canvas) |
| **Code** | Mainland checkout `1 - Servers/2 - RootRecord-US-Mainland-Server/mirror/network-globe/network-globe/overlay/` plus one line in `index.html` and one allowlisted route block in the mirror `server.js` |
| **Test record** | [2026-09-29-globe-landing-overlay-preview](../07-testing/2026-09-29-globe-landing-overlay-preview.md) |
| **Screenshots** | `/home/rootrecord/RootRecord-Ecosystem/test-reports/Globe-Landing/` (11 PNGs) |
| **Backup** | `/home/rootrecord/Database/GITHUB/globe-landing.bak-20260929-141948/` (`mainland/` originals, `library/` README and worklog copies, `aws-runtime-readonly/` read-only copies of the live AWS `index.html` + `server.js`) |
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

Runtime switches: `?overlay=0` turns the overlay off for one load, and `?embed=1` (existing) also keeps it off.

## Files

| Path (Mainland checkout, `mirror/network-globe/network-globe/`) | Change |
| --- | --- |
| `overlay/overlay.js` | new: vanilla IIFE |
| `overlay/overlay.css` | new |
| `overlay/overlay-config.json` | new: flags |
| `overlay/README.md` | new: flags, preview, deploy, revert |
| `overlay/preview-server.js`, `overlay/sample-state.json` | new, **desk preview only (not deployed)** |
| `index.html` | +1 line: `<script src="/overlay/overlay.js" defer></script>` |
| `server.js` (mirror) | +17 lines: `OVERLAY_FILES` allowlist (3 exact paths, `no-store`, `nosniff`) before the 404 |

**Revert:** delete the one line in `index.html` and the `OVERLAY_FILES` block, then `rm -r overlay/`. The originals are in the backup `mainland/`.

## Deploy to AWS: PROPOSED, needs sign-off, not run

The brief said not to deploy while the tunnel task was running. That task finished at 14:12–14:30 (`www` returns 200, served by the Express runtime).

**Do not copy the mirror `server.js` / `index.html` over the runtime; they are different implementations.** The runtime needs no server change, because `express.static(__dirname)` already serves `overlay/`.

1. `ssh rr-aws-ip "md5sum /home/ubuntu/network-globe/network-globe/index.html"` should return `f3d0377428a3ac467941c99a075b9d24`. Stop if it doesn't.
2. Take a dated backup on the host: `ssh rr-aws-ip 'B=$HOME/backups/globe-landing-$(date +%Y%m%d-%H%M%S) && mkdir -p $B && cp -a /home/ubuntu/network-globe/network-globe/index.html $B/ && echo $B'`
3. `ssh rr-aws-ip "mkdir -p /home/ubuntu/network-globe/network-globe/overlay"`, then scp **only** `overlay.js`, `overlay.css` and `overlay-config.json` into it.
4. Add the include line idempotently: `ssh rr-aws-ip "grep -q /overlay/overlay.js …/index.html || sed -i 's#</body>#  <script src=\"/overlay/overlay.js\" defer></script>\n</body>#' …/index.html"`
5. No restart needed.
6. Verify:
   - `curl -sI https://www.rootrecord.cloud/overlay/overlay.js` shows a javascript content type (text/html means the file is missing).
   - `curl -s https://www.rootrecord.cloud/ | grep -c /overlay/overlay.js` returns 1.
   - The config JSON parses, and `/health` returns JSON.
   - Hand check on a desktop and a phone: drag and zoom outside the cards; close, reload and restore.
7. Revert: set `"enabled": false` in the config (instant), or `sed -i '\#/overlay/overlay.js#d' index.html`, or restore the backup and `rm -r overlay`.

The exact commands are in the checkout's `overlay/README.md`.

## Findings and sign-off items

1. **P0 security: the live `www.rootrecord.cloud` serves its app directory publicly.** The runtime has `app.use(express.static(__dirname))`. At 14:29 HST, 1-byte range requests (206) succeeded for `/server.js`, `/package.json`, `/README.md` and **`/data/hawaii.ndjson`** (the desk's network-flow feed); contents were not read beyond 1 byte. Proposed fix: replace the line with `app.use('/overlay', express.static(path.join(__dirname, 'overlay')))`, which keeps the index fallback, then restart `network-globe-web.service`. **Needs sign-off: AWS change + restart.** Not done.
2. **Repo mirror ≠ AWS runtime** (`index.html` and `server.js`). Decide which is canonical and sync them. The mirror's HUD also prints the AWS **account id** (`acct …`); the runtime currently shows "No AWS telemetry connected".
3. **Sign-up backend down** (`api-goals.rootrecord.info` unreachable, `api.rootrecord.info` 503), so the card stays a placeholder.
4. **`/home` routing.** `rootrecord.cloud/*` 301s to `www` (the globe). A Cloudflare rule or Worker for `/home*` → Vercel is needed before `cards.home.enabled: true`.
5. **Mainland checkout isn't auto-synced.** The overlay files are uncommitted there, alongside another agent's uncommitted unit/cron/README edits. This needs the `repos.conf` / manual-commit sign-off.
6. Nice-to-have: the mirror `/healthz` exposes `origin` (lat/lng label). The overlay never shows it, but the endpoint is public.
