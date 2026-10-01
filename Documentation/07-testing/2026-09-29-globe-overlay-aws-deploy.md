# Globe overlay: AWS deploy + AWS Ohio node (2026-09-29)

- Date: 2026-09-29, 16:09–16:17 HST
- Host: AWS t3.micro (us-east-2), `network-globe-web.service`. No restart.
- Status: deploy **PASS / LANDED**; AWS-node fix **PASS / LANDED**; real-browser visual check **VERIFY PENDING**; AWS-side collector **PROPOSED**.
- Related: [design doc](../08-ideas/2026-09-29-globe-landing-overlay.md) · [v2 record](./2026-09-29-globe-overlay-v2-spin-click-info.md) · [allowlist record](./2026-09-29-aws-globe-static-allowlist.md)

## Deploy
**Deploy (approved v2, 16:09–16:11 HST): LANDED, all checks PASS.**
- Backups: desk `/home/rootrecord/Database/GITHUB/globe-overlay-deploy.bak-20260929-160933/`; AWS `/home/ubuntu/backups/globe-landing-20260930-020957/` (`index.html`, md5/sha before, `ls` and service state). The deployed v2 overlay files are in `/home/ubuntu/backups/globe-landing-20260930-020957/overlay-v2-as-deployed-021621/`.
- Changes: created `$H/overlay/` with the 3 runtime files (644), and added 1 include line before `</body>`. `index.html` md5 went from `f3d03774…` to `6d9b5af6…`. No restart (`network-globe-web` MainPID 266222, active since 14:43:28 HST).
- Public checks, all PASS: overlay.js/css/config return 200 with the right MIME types and matching sha256; the include appears once on `/` and `/index.html`; `/overlay/preview-server.js`, `/overlay/sample-state.json`, `/overlay/README.md`, `/server.js` and `/data/hawaii.ndjson` all return 404; `/health` and `/api/state` return 200.
- Caching: Cloudflare/browsers cache `overlay.js` for 4 h (`max-age=14400`). The config uses `max-age=0` (DYNAMIC), so `enabled:false` reverts immediately. After the 16:16 update the edge already served the new hash (`cf-cache-status: EXPIRED`), but a returning browser can hold the old JS for up to 4 h unless hard-refreshed.
- Revert: (1) `enabled:false` in `overlay-config.json`; (2) `sed -i '\#/overlay/overlay.js#d' $H/index.html`; (3) restore `index.html` from `/home/ubuntu/backups/globe-landing-20260930-020957/` and `rm -r $H/overlay`. To undo only the AWS-node update, copy back `/home/ubuntu/backups/globe-landing-20260930-020957/overlay-v2-as-deployed-021621/*`.

## Missing Ohio lines: cause
**Why there were no Ohio lines (read-only check, 16:12 HST).** The live AWS `server.js` (allowlist build, sha256 `4ba42236…`) draws only the desk's own flows from `data/hawaii.ndjson`. Every record is `network-globe-telemetry` from `HawaiiRoot`. `buildState` emits one origin point (Hawaiʻi, 21.31 / -157.86) plus Hawaiʻi→destination arcs. It has no AWS point, no desk↔AWS link and no AWS-side collector. `collector.js` on AWS is the desk-side collector; no ss/tcpdump runs on AWS. `index.html` filters nothing. The overlay and the hiding rules dropped nothing: they only hide fields in the info card, and `stableData` keeps every item. The mirror `server.js` has an AWS origin and a collector, but it was never deployed.

## Fix
**Fix: overlay only, deployed 16:16 HST, no restart.**
- `overlay.js` adds `withAwsPoint` and `withAwsLink`. They are pure functions in `RR_OVERLAY_UTIL`, applied before the stableData reuse.
- Point: one synthetic AWS point, Ohio 39.96 / -83.0, labelled "AWS us-east-2 · Ohio". It is skipped if the data already has a `type:aws` point, or an origin within 1°.
- Link: one arc from the desk-flow origin to Ohio (`protocol:persistent`, colour `#38bdf8`, altitude 0.28). It is skipped if any persistent arc exists or an arc already starts in Ohio. It is not drawn when there are no desk flows.
- No IP on either one. Info cards: "Desk link · Hawaiʻi desk → AWS Ohio" and "AWS region · 40, -83 · Mainland node · feed + page".
- Flag: `globe.awsNode {enabled, lat, lng, label, link, linkColor}`. Set `enabled:false` in `overlay-config.json` to switch it off (not cached).
- `/api/state` is unchanged: it still has only `origin` and `dest` point types; the AWS items are added client-side.
- Files: `overlay.js` sha256 `e08a20e2…f4c2` (md5 `24cc1906…`), `overlay-config.json` sha256 `08feebc8…6a6f`, `overlay.css` unchanged (`75b3e837…`).

## Tests
**Tests.**
- jsdom unit tests: 18/18 PASS, including 2 new awsNode tests (point and link added once, no IP, suppressed when the data already has them). Log: `test-reports/Globe-Landing/v3-awsnode-unit-test-run.log`.
- Real globe.gl preview (AWS runtime schema, prod config), screenshots `test-reports/Globe-Landing/v3-awsruntime-desktop-1440x900-aws-link-info.png`, `…-aws-point-info.png` and `v3-awsruntime-mobile-390x844-aws-point-info.png`: both info cards render. The Source and Role values were shortened afterwards so they fit, and re-tested 18/18.
- Headless has no WebGL, so the globe canvas is blank in the screenshots. Visually confirming the Ohio line and point in a real browser is VERIFY PENDING.

## Proposal
**PROPOSED, not built: AWS's own flows.** A systemd timer or cron job every 30–60 s would run `ss -tunH state established` (or read `/proc/net/tcp`) and write at most 200 aggregated remote endpoints to `data/aws-conns.json`. `server.js` would merge them as Ohio-origin arcs through its existing geo cache.
- RAM: no resident daemon. Each run is a sh/awk process of about 2–5 MB for under 1 s (about 10–15 MB if written in Python); `server.js` grows by less than 1 MB.
- Do not use tcpdump: it needs root, keeps 5–10 MB resident and uses CPU, on a t3.micro with 908 MB.
- Needs a `server.js` change and a web restart, so it needs sign-off. It must also not collide with the other worker's fallback/history files.
