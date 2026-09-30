# Test record — AWS globe `server.js`: static allowlist (close file exposure on www.rootrecord.cloud)

| Field | Value |
| --- | --- |
| **Date / time (HST)** | 2026-09-29 14:39–14:50 HST |
| **Tester** | Grok (executor) for Alexander Storey |
| **Change under test** | AWS `/home/ubuntu/network-globe/network-globe/server.js`: `express.static(__dirname)` replaced by an explicit allowlist, catch-all → 404, bind 127.0.0.1. P0 follow-up to [the trim/tunnel record](./2026-09-29-aws-hawaii-trim-and-cloudflared.md). WO-SRV |
| **State** | **PASS** (every sensitive path 404, `/` + `/health` + `/api/state` 200, data streaming). Separate finding: the feed-server on public `:8787` is **still exposed** (not changed) |
| **Evidence** | AWS `~/rootrecord/bin.bak-globe-static-allowlist-20260929-144149/access-evidence.before.txt`, `sha256.{before,after}.txt`; Mainland mirror `mirror/network-globe/network-globe/AWS-LIVE-SERVER.md` (full diff) |
| **Commits** | Library: desk auto-sync (see the worklog). Mainland: none (uncommitted, not in auto-sync) |
| **Backup** | AWS `/home/ubuntu/rootrecord/bin.bak-globe-static-allowlist-20260929-144149/` (`server.js`, `index.html`, `network-globe-web.service`). Desk `/home/rootrecord/Database/GITHUB/globe-static-allowlist.bak-20260929-144459/` |

## What was tested

When the tunnel came back up at 14:12 HST, `server.js` had `app.use(express.static(__dirname))`, so every file in the globe folder was public. Its catch-all also returned `index.html` with a 200 for any unknown path. The AWS `index.html` (which differs from the repo copy and was not changed) loads **no local assets**: only `https://unpkg.com/globe.gl` and the `three-globe` earth texture from unpkg. It polls `/api/state` every 1 s, with no websocket or SSE.

## How (exact commands / procedure)

```bash
# probe: body discarded, 1-byte range, codes only
curl -s -o /dev/null -r 0-0 -w '%{http_code}' https://www.rootrecord.cloud<path>
# patch applied by a reviewed python script -> node --check -> tested as a throwaway copy in /tmp/globe-test on 127.0.0.1:8099
# (dummy sensitive files + overlay test file, ../ traversal probes), then atomic mv over server.js
sudo systemctl restart network-globe-web
```

## Pass criteria (written before running)

1. Every sensitive path returns 404 over `https://www.rootrecord.cloud`.
2. `/`, `/index.html` and `/?embed=1` return 200. The page's own assets (unpkg) are reachable.
3. `/health` returns JSON, and `/api/state` returns changing flow counts.
4. `/overlay/{overlay.js,overlay.css,overlay-config.json}` are served only if present, and anything else under `/overlay/` returns 404.
5. The services stay active. If anything fails, restore the backup and restart.

## Result

| Path (via www) | Before 14:40 | After 14:43 |
| --- | --- | --- |
| `/server.js`, `/package.json`, `/package-lock.json`, `/README.md`, `/RATIONALE.md`, `/collector.js`, `/telegram-relay.js`, `/feed-server.js`, `/connection-history.py`, `/*.service`, `/ensure-network-globe-hawaii.sh`, `/health-check.sh`, `/maintain-hawaii-feed.sh`, `/scripts/maintain-hawaii-feed.sh` | **206** (real file) | **404** |
| `/data/hawaii.ndjson`, `/data/hawaii-connections.sqlite3` (+`-journal`), `/data/geo-cache.json`, `/data/hawaii-offset.json` | **206** (real file) | **404** |
| `/node_modules/express/package.json` | **206** (real file) | **404** |
| `/network-globe.log` | 416 (empty file, exists) | **404** |
| `/.env`, `/.git/config`, `/.cloudflared/config-globe.yml`, `/data/`, `/scripts/`, `/does-not-exist` | 206 text/html (catch-all `index.html`; the files don't exist or are dotfiles, so nothing leaked) | **404** |
| `/overlay/overlay.js`, `/overlay/overlay.css`, `/overlay/overlay-config.json` | — | 404 (no `overlay/` folder on AWS yet). In the 8099 test with a file present, it returned 206. `/overlay/secret.txt` and `..%2f` / `%2e%2e%2f` / `../` traversal all returned 404 |
| `/`, `/index.html`, `/?embed=1` | 200 | **200** (5346 B) |
| `/health` | — | **200** `{"status":"ok",…,"flows":119,"geo":524}` |
| `/api/state` | — | **200**, 40 KB; activeFlows 119 → 119 → 123, arcs 119 → 122 over about 6 s (streaming) |
| unpkg `globe.gl`, `earth-night.jpg` | — | reachable (206 on a 1-byte range) |

After the change, the listener is `127.0.0.1:8090` (before it was `*:8090`; the security group already blocked 8090 from outside, so a direct request timed out). The AWS sha256 went from the backup copy to `4ba42236…e0e9fc`. A restore was not needed.

## Was anything fetched by outside IPs while exposed? (14:12:12–14:43:29 HST)

- There is no per-request log. `server.js` has no access logging, cloudflared at `info` level doesn't log requests, and Cloudflare-side logs aren't available.
- The cloudflared counters just before the fix (14:41:49) showed **55 requests in total** since the tunnel started: 24 × 200, 27 × 206, 2 × 416. At least 33 of them were my own checks (the 29-path probe and 4 page checks), and the rest were other desk checks (the parent's 206 probe and page/preview checks). No browsing session was visible: a single open page polls `/api/state` every second and would have added hundreds of requests.
- A byte bound comes from the web process's `/proc/<pid>/io` `wchar`, which counts every socket write. Over the whole exposed lifetime it was **4.6 MB**, and it also includes the geo-cache file rewrites. So **no full download of `hawaii.ndjson` (≥ 50 MB) happened**. Small files (source, the ~0.3 MB sqlite, `geo-cache.json`) can't be ruled out from local evidence alone, but the request count leaves little room for an outside client.

## Separate finding (not changed; needs a decision)

- **`network-globe-feed-server` (`feed-server.js`) listens on `0.0.0.0:8787`, and `http://[redacted public IP]:8787/hawaii.ndjson` is publicly reachable** (a HEAD returned 200 with `X-Feed-Size: 60981903`). It serves up to 2 MB per request from `?from=`, so the whole feed can be read in chunks.
- This existed before today (the process has been up since 2026-09-26 05:34 HST). Its `wchar` since then is only **5.5 KB**, so essentially nothing has been served from it.
- Fix options: set `Environment=GLOBE_BIND=127.0.0.1` in its unit, or close TCP 8787 in the EC2 security group, once it's confirmed that nothing external uses it.

## Resource impact

| When | Load (1/5/15) | MemAvailable | Swap used | Peak RSS |
| --- | --- | --- | --- | --- |
| before (14:15) | 1.39/1.17/0.74 | 446 MB | none | server.js 84.5 MB |
| after (14:44) | 1.31/1.34/1.16 | 467 MB | none | server.js 80.9 MB |

## Cleanup confirmation

- [x] The test instance on 127.0.0.1:8099 was stopped by PID, and `/tmp/globe-test` and the patch script were removed.
- [x] Only the intended listener remains: `127.0.0.1:8090`.
- [x] No models are involved.

## Open items / caveats

- The Mainland mirror `mirror/network-globe/network-globe/` also holds a separate, in-progress repo `server.js`/`index.html` (overlay work, not mine). The AWS version is kept as `server.aws-live-2026-09-29-allowlist.js` plus `AWS-LIVE-SERVER.md`. Any future deploy must carry the allowlist forward.
- The feed-server on `:8787` is still public (above).
