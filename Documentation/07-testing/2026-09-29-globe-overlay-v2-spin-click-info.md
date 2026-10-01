# Test record: globe overlay v2 (Stop/Resume spin, click-info card, hover highlight, 1 s mesh re-creation fix)

| Field | Value |
| --- | --- |
| **Date / time (HST)** | 2026-09-29 15:43–16:06 HST |
| **Tester** | Grok (executor, globe-overlay v2 pass) |
| **Change under test** | Mainland checkout `mirror/network-globe/network-globe/overlay/`: `overlay.js` (md5 `95ceda53…`, 30.3 KB), `overlay.css` (`6a469f81…`), `overlay-config.json` (`b90c77d5…`, new `globe.*` flags), `preview-server.js` (probe/delay/allowlist schema), `sample-state.json` (synthetic RFC 5737 IPs), new `test/overlay.test.js`. `index.html` and `server.js` are **unchanged** in v2. Design: [globe landing overlay §v2](../08-ideas/2026-09-29-globe-landing-overlay.md) |
| **State** | **PASS**: unit/integration tests 16/16, real-library wiring probe, 8 screenshots, cleanup. **VERIFY PENDING**: real-browser mouse drag/zoom/click/hover over WebGL. **PROPOSED**: AWS deploy (not run) |
| **Evidence** | `/home/rootrecord/RootRecord-Ecosystem/test-reports/Globe-Landing/v2-*.png`, `v2-unit-test-run.log`; preview logs `/tmp/rr-globe-preview-v2-{R,M}.log` |
| **Commits** | Library: auto-sync (see worklog). Mainland: none (not in auto-sync; no git writes) |
| **Backup** | `/home/rootrecord/Database/GITHUB/globe-overlay-v2.bak-20260929-154351/` |

## What was tested

1. **Stop/Resume spin.** Toggles `globe.controls().autoRotate`, persists in `localStorage` (`rr-globe-overlay:v1:spin`) and overrides the page's `autoRotate=true` after a reload. `spinDefault:auto` follows reduced motion.
2. **Click info.** Arc and point clicks, through handlers the overlay registers on the real instance, open the info card with safe fields only. Esc, × and a click on empty globe close it. Spin pauses while the card is open and resumes on close. The card survives the page's 1 s data refresh.
3. **Hover highlight** is keyed by flow and survives new objects. Tooltips are escaped and omit process names.
4. **Fix for the 1 s mesh re-creation** (`stableData`): identity is kept across polls, changed fields are applied, vanished flows are dropped.
5. **Robustness:**
   - Existing page handlers are chained, not replaced.
   - All v2 flags off means nothing is wired.
   - If globe.gl fails to load (TDZ `globe`), the cards still render with no overlay error.
   - Both page versions work: the live AWS `index.html` copy and the repo mirror.

## Grounding (read-only, 15:44–15:47 HST)

- AWS `index.html` md5 is **`f3d0377428a3ac467941c99a075b9d24`**, unchanged; the public page matches.
- AWS `server.js` sha256 is `4ba42236…`, the allowlist version (`AWS-LIVE-SERVER.md`).
- `overlay/` doesn't exist on AWS yet; public `/overlay/overlay.js`, `/server.js` and `/data/hawaii.ndjson` return 404.
- Live `/api/state` arc keys: `startLat/Lng, endLat/Lng, process, protocol, endpoint (= remote IP), port, city, country, org, color, altitude, stroke`. Point keys: `lat, lng, label, type ∈ {origin, dest}`. Only key names and types were printed, no values.
- Page source: `const globe = Globe()(…)` at the top level of a classic script, with **no** `onArcClick`/`onPointClick`/`onGlobeClick`/hover handlers. Unpinned `https://unpkg.com/globe.gl`.
- globe.gl 2.46.2 / three-globe 2.45.2 / data-bind-mapper source, installed in a box scratch dir (not on the desk):
  - Click/hover props are kapsule props with no-arg getters.
  - `onClick` ignores background clicks.
  - The data join uses `id = d => d` (object identity).
  - `arcsTransitionDuration` / `pointsTransitionDuration` default to 1000 ms.
  - **Cause of the flaky interaction:** the page's 1 s `arcsData()`/`pointsData()` refresh re-creates every mesh and re-plays its grow-in.

## How

```bash
# 1) unit/integration: on the agent box (scratch /workspace/gltest, jsdom 24, node 20) — not on the desk, not on AWS
SRC=src node --test --test-timeout=60000 overlay.test.js      # src = overlay files + mirror index + read-only AWS index copy
# 2) real-library probe + screenshots on the desk, 127.0.0.1:8794, via /tmp/rr-memwatch-run.sh (nice 10, kill < 2 GB), PID-based stop
PREVIEW_SCHEMA=aws-runtime PREVIEW_PAGE=<backup>/aws-runtime-readonly/index.public.html PREVIEW_CONFIG=prod node overlay/preview-server.js 8794
PREVIEW_SCHEMA=mirror PREVIEW_CONFIG=full node overlay/preview-server.js 8794
firefox --headless --no-remote --profile ~/snap/firefox/common/rr-shot-profile --window-size=W,H --screenshot <test-reports>/v2-….png 'http://127.0.0.1:8794/?preview_select=arc:0&preview_hover=arc:1'
```

The preview probe (preview-only, injected by `preview-server.js`) waits for `RR_OVERLAY.wired()` and live arcs. It then calls **the handlers the overlay registered on the real globe.gl instance** (`globe.onArcClick()(globe.arcsData()[i])`, and so on) and prints a badge. A 3 s `/__preview_delay` image holds the load event so `firefox --screenshot` captures the result.

## Pass criteria (written before running)

1. `node --check` passes and the config is valid JSON. All unit/integration tests pass.
2. Spin: the button toggles `autoRotate`, the choice persists across reload, and the label/`aria-pressed` update.
3. Info card:
   - Public IP shown.
   - Private IP shows "private (hidden)"; the desk-link IP shows "hidden (desk link)".
   - The origin shows no coordinates.
   - No process names; HTML in feed strings renders as text.
   - Last seen is in HST.
4. The card and the hover survive a data refresh.
5. With the real library, the probe shows `wired=true`, click getters are `function`, and `stableId=true`.
6. Layout: the card fits at 1440×900, 390×844 and 360×640 and doesn't overlap other cards (phone: the stack hides while the card is open).
7. Cleanup: 0 processes left, port closed.

## Result

| # | Result |
| --- | --- |
| 1 | **PASS**: 16/16 (`v2-unit-test-run.log`, 16:01 HST, 5.6 s) |
| 2 | PASS (tests 6 and 7; screenshots `v2-…-spin-off.png` show amber `▶ Resume spin`, probe `autoRotate=false`) |
| 3 | PASS (tests 2–5 and 8–9; screenshots) |
| 4 | PASS (tests 9, 10, 15) |
| 5 | **PASS**: every probe badge read `wired=true · arcClick=function · pointClick=function · stableId=true · autoRotate=false` (the latter because the card pauses spin) |
| 6 | PASS after one fix: on the phone, the first 390×844 shot showed the info card overlapping the sign-up/status cards. Added `#rr-ov.has-info .ov-col{display:none}` (≤ 640 px) and re-shot |
| 7 | PASS: preview, memwatch and firefox all at 0; port 8794 closed; temp tarballs removed from `~/snap/firefox/common/` |
| real mouse | **VERIFY PENDING**: headless Firefox paints no WebGL (blank globe), so real pointer raycasting, drag/zoom, hover colour and the `.clickable` cursor need a hand check after deploy |

**Screenshots** (`/home/rootrecord/RootRecord-Ecosystem/test-reports/Globe-Landing/`, globe blank because headless has no WebGL; the yellow top badge is the preview-only probe):

| File | Scenario |
| --- | --- |
| `v2-awsruntime-desktop-1440x900-arc-info.png` | live AWS page copy: arc click → Connection card (San Francisco, Example CDN, IP 203.0.113.10, TCP 443), arc 1 hovered |
| `v2-awsruntime-desktop-1440x900-origin-point-info.png` | origin point → "Origin · Hawaii", flows 5, ports, **no coordinates** |
| `v2-awsruntime-desktop-1440x900-spin-off.png` | stored `spin=off` → `▶ Resume spin` |
| `v2-awsruntime-mobile-390x844-arc-info.png` | phone: card replaces the stack (after the fix) |
| `v2-awsruntime-mobile-360x640-point-info.png` | small phone: Endpoint card (Tokyo, 35.7, 139.7) |
| `v2-awsruntime-mobile-390x844-spin-off.png` | phone: Resume spin pill |
| `v2-mirror-desktop-1440x900-desklink-info-rail.png` | mirror page, rail open (with `↻ Spin on/off`): persistent **Desk link** → IP "hidden (desk link)", ASN shown |
| `v2-mirror-desktop-1440x900-dest-point-info.png` | mirror page: Endpoint card with Traffic 85.3 KB/s |

## Resource impact

| When | Load (1/5/15) | MemAvailable | Swap used | Peak RSS |
| --- | --- | --- | --- | --- |
| before (15:44) | n/a | 6.60 GB | unchanged | n/a |
| during (15:58–15:59) | 5.6–7.3 / 5.0–5.3 / 3.7–3.9 (other agents active) | min 6.08 GB (memwatch) | unchanged | node preview ≈ 50 MB; firefox about 5 s per shot |
| after (16:00) | ~5.6 | 6.79 GB | unchanged | n/a |

The unit tests ran on the agent box, with no desk load.

## Cleanup confirmation

- [x] No test process left (`preview-server`, `rr-memwatch`, `rr-shot-profile` all at 0). PID-based stop only; no `pkill -f`. On the box, one `pkill -f` killed its own shell once; the leftovers were rechecked and were 0.
- [x] Port 8794 closed. 8791 (another agent) untouched.
- [x] No model, no sudo, no restart, no AWS write. AWS access was read-only: `md5sum`, `sha256sum`, `ls`, and public curl status codes / key names.

## Open items / caveats

- AWS deploy PROPOSED; steps are in the design doc and `overlay/README.md`: 3 files + 1 include line, no restart.
- Pin `globe.gl` (finding 7). A proper tooltip fix belongs in `index.html` (finding 8). Both need sign-off.
- "Last seen" is the time the overlay last saw the flow in `/api/state`, because neither server sends per-flow timestamps. A server-side `lastSeen` field on arcs would make it exact.
