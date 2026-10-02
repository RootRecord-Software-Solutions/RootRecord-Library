# Test record: globe landing overlay, local preview and screenshots

| Field | Value |
| --- | --- |
| **Date / time (HST)** | 2026-09-29 14:19–14:36 HST |
| **Tester** | Grok (executor, globe-landing pass) |
| **Change under test** | New `overlay/` (js/css/config) + 1 include line in `index.html` + an allowlisted overlay route in the mirror `server.js`, in the Mainland checkout `mirror/network-globe/network-globe/`. Design: [2026-09-29-globe-landing-overlay](../08-ideas/2026-09-29-globe-landing-overlay.md) |
| **State** | **PASS** (preview: syntax, routes, layout at 5 viewport sizes, both server schemas, failure view, cleanup). **VERIFY PENDING**: globe drag/zoom under the cards in a real browser (headless Firefox rendered no WebGL canvas). **PROPOSED**: AWS deploy (not run) |
| **Evidence** | Screenshots in `/home/rootrecord/RootRecord-Ecosystem/test-reports/Globe-Landing/`; preview logs `/tmp/rr-globe-preview.log`, `/tmp/rr-globe-preview-{A,B,C}.log` |
| **Commits** | Library: see worklog (auto-sync). Mainland: none (checkout not in auto-sync; uncommitted by rule) |
| **Backup** | `/home/rootrecord/Database/GITHUB/globe-landing.bak-20260929-141948/` |

## What was tested

- `overlay.js`, `overlay.css` and `overlay-config.json` render the Sign-up (placeholder), Website Home and Live status cards, the restore dock and the left rail over the globe page.
- The mirror `server.js` route serves exactly three overlay paths.
- The status card works against both the mirror schema (`/healthz` + `stats.updated` / `hawaiiActiveFlows`) and the **live AWS Express schema** (`/health` + `collector:"hawaii-feed"`), using a read-only copy of the runtime `index.html`. It degrades to red/grey when the endpoints fail.

## How

```bash
G=".../1 - Servers/2 - RootRecord-US-Mainland-Server/mirror/network-globe/network-globe"
node --check overlay/overlay.js overlay/preview-server.js server.js; python3 -m json.tool overlay/overlay-config.json
# preview server on 127.0.0.1:8794 (8791 was already taken by another agent's python3), via /tmp/rr-memwatch-run.sh (nice 10, kill < 2 GB)
PREVIEW_CONFIG=full node overlay/preview-server.js 8794                                   # A: mirror schema, rail + home on
PREVIEW_SCHEMA=aws-runtime PREVIEW_PAGE=<backup>/aws-runtime-readonly/index.html PREVIEW_CONFIG=prod node overlay/preview-server.js 8794   # B
PREVIEW_SCHEMA=down PREVIEW_CONFIG=prod node overlay/preview-server.js 8794                # C: 503 on health/state
curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8794/<path>
firefox --headless --no-remote --profile ~/snap/firefox/common/rr-shot-profile --window-size=W,H --screenshot <test-reports>/<name>.png 'http://127.0.0.1:8794/?…'
```

The real `server.js` was **not** run on the desk (it does packet capture, geo lookups and AWS CLI calls). Its new route was checked by `node --check` plus a diff review: 3 exact paths, a hasOwnProperty lookup, no user path joins.

## Pass criteria (written before running)

1. All JS passes `node --check`; the config is valid JSON.
2. Preview routes: `/`, the 3 overlay files, health and `/api/state` return 200; unknown paths and `/overlay/../server.js` return 404.
3. At 1440×900, 1280×540, 390×844 and 360×640, everything fits the viewport, nothing overlaps the HUD, and there is no scrollbar.
4. Closed cards are hidden, the dock shows `+ <name>`, and the preset `localStorage` state is honoured. The rail opens and collapses per state.
5. The sign-up card is visibly badged "Preview · not live" and says it submits nowhere. There is no `action` attribute and the handler calls `preventDefault` with no fetch.
6. The status card shows green on healthy data for both schemas and red/grey on 503. No hostname, origin, account id or path appears in the card.
7. Cleanup: no preview/firefox process is left and port 8794 is closed.

## Result

| # | Result |
| --- | --- |
| 1 | PASS |
| 2 | PASS: 200 ×6, `/nope` 404, `/overlay/../server.js` 404 (A); B: `/health` 200, `/healthz` 200 HTML fallback (as on AWS), and the overlay include was injected once |
| 3 | PASS after one fix: on mobile the restore dock first sat top-right over the HUD title. It was moved to a bottom row with the column shifted up (`#rr-ov.has-dock`), and the shots were re-taken |
| 4 | PASS (`…rail-open-status-closed`, `…cards-closed`, `…short-cards-closed`) |
| 5 | PASS (code review + screenshots) |
| 6 | PASS: A shows 4 green rows; B shows node up · 16m, desk live · 67 flows, telemetry amber "not connected", freshness "feed answering"; C shows red unreachable/no data and grey unknown |
| 7 | PASS: `pgrep` 0, port 8794 closed, temp tarballs removed |
| drag/zoom | **VERIFY PENDING**: guaranteed by `pointer-events:none` on the overlay root (cards only `auto`), but headless Firefox `--screenshot` paints no WebGL, so the globe area is blank in every shot. Check by hand in a real browser after deploy |

**Screenshots** (`/home/rootrecord/RootRecord-Ecosystem/test-reports/Globe-Landing/`):

| File | Scenario |
| --- | --- |
| `desktop-1440x900-rail.png` | A: rail collapsed, all 3 cards |
| `desktop-1440x900-rail-open-status-closed.png` | A: rail open, Status closed → dock `+ Status` |
| `desktop-1440x900-production-flags.png` | A with `?ov_rail=0&ov_home=0` (= production flags) |
| `desktop-1280x540-short-cards-closed.png` | short desktop, Home closed |
| `desktop-1440x900-status-down.png` | C: endpoints 503 |
| `mobile-390x844-rail.png` | A: phone, rail + 3 cards |
| `mobile-390x844-cards-closed.png` | A: phone, Sign-up + Home closed → bottom dock |
| `mobile-390x844-production-flags.png` | phone, production flags |
| `mobile-360x640-short.png` | small phone, production flags |
| `awsruntime-desktop-1440x900-production-flags.png` | B: live AWS page copy + runtime schema |
| `awsruntime-mobile-390x844-production-flags.png` | B: phone |

## Resource impact

| When | Load (1/5/15) | MemAvailable | Swap used | Peak RSS |
| --- | --- | --- | --- | --- |
| before (14:23) | ~1.7 | 6.67 GB | n/a | n/a |
| during (14:24–14:31) | 2.07–2.21 / 1.76–1.83 / 1.70–1.72 | min 6.21 GB (memwatch) | unchanged | node preview ≈ 50 MB; headless firefox short-lived (≈ 1–2 s per shot) |
| after (14:31) | ~2.2 | 6.44 GB | unchanged | n/a |

## Cleanup confirmation

- [x] No test process left: preview server, memwatch wrapper and headless firefox all at 0. One cleanup `pkill -f` also matched its own shell (the run was aborted); the leftovers were rechecked and were 0. The later runs used a PID-based stop.
- [x] Port 8794 closed. Port 8791 (another agent's python3) was untouched.
- [x] No model loaded, no sudo, no restarts, no AWS writes. AWS access was read-only: `md5sum`, `ss`, `systemctl cat`, `scp` **from** AWS of `index.html` + `server.js` into the backup, and public curl status codes.

## Open items / caveats

- **P0 security finding** (see the design doc): the live runtime `express.static(__dirname)` serves `/server.js`, `/package.json`, `/README.md` and `/data/hawaii.ndjson` publicly (206 on a 1-byte range). Not fixed; needs sign-off.
- The AWS deploy is PROPOSED; the steps are in the design doc and in `overlay/README.md`.
- The mirror and the AWS runtime `index.html` / `server.js` differ; they need reconciling.
- The Home card stays off until `/home` routes to Vercel. The sign-up card stays a placeholder until the goals auth API is back.

- **Follow-up (16:03 HST):** the P0 static-exposure finding was fixed by the AWS agent at 14:43 HST (allowlist `server.js`); re-checked at 15:46 HST, `/server.js` and `/data/hawaii.ndjson` now return 404. v2 (spin/click-info/hover) is in [2026-09-29-globe-overlay-v2-spin-click-info](./2026-09-29-globe-overlay-v2-spin-click-info.md).
