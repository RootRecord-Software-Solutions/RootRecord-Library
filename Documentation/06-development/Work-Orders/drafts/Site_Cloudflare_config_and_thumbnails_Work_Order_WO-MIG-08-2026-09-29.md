# WORK ORDER — Site Cloudflare config and thumbnails

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-MIG-08-2026-09-29 |
| **Date** | 2026-09-29 (HST) |
| **Status** | BUILT — manifest, checker, and archive landed. DNS not changed. Not on the active index. |
| **Owner** | RootRecord |
| **Related** | Agent 08. Depends on 7. Public website checkout. Later: 9. Cloudflare workers. Template: `Documentation/01-operations/templates/TEMPLATE Work Order.md`. Globe: `Documentation/08-ideas/2026-09-29-globe-landing-overlay.md`. Staging: `Documentation/00-architecture/Website-RootRecord-Cloud-Staging.md`. |

**Scope:** Routing and thumbnail assets for the one Vercel site. Add a local route manifest and an on-demand checker under `Communications/Site`. Archive the old avaivy.cloud skin unchanged. Do not apply that skin, do not change DNS or tunnels, and do not import generated images or HTML into the live Folders. This file is the before-documentation. It is not on the active index.

---

## 1. Intent

The old GitHub repo `rootrecordsoftwaresolutions/old` (`web/` and `Thumbnails/`) held Ava Ivy Cloudflare ingress for `avaivy.cloud`, `www.avaivy.cloud`, and `directory.avaivy.cloud` (origin `127.0.0.1:8080`), a second ingress for old RootMC and Ava hostnames, a DNS helper (`deploy-dns.sh`), the avaivy.cloud static skin (CSS, a little JS, shell HTML), and 24 thumbnail images. About 3,500 HTML files under `web/sites/avaivy.cloud/{earthquakes,news,weather,states}` are generated pages for other functions.

The live system already does the following, and this work must keep it:

- Desk tunnel: Pacific `Communications/network/cloudflare/` (`cloudflared` binary, `cf-status.json`, `cf-blocker.json`). Token name `ROOTSERVER_TUNNEL_TOKEN`.
- Globe: `www.rootrecord.cloud` → `127.0.0.1:8090` in `1 - Servers/2 - RootRecord-US-Mainland-Server/mirror/.cloudflared/config-globe.yml`, plus `ssh.rootrecord.cloud`. Visual direction is that full-screen dark globe and glass overlay. The Home card target is `https://rootrecord.cloud/home` and stays off until routing exists.
- Vercel app: `rootrecordsoftwaresolutions/RootRecord-Cloud`, staging clone under `Communications/website/RootRecord-Cloud` (gitignored by Pacific). `3 - RootRecord-Website` is empty. Apex `rootrecord.cloud` redirects to `www`, which is the globe, so the public domain does not reach Vercel today.

When building is allowed: a local route manifest and a checker for the one Vercel site. `www` stays the globe. The Vercel app is the only public site. Old avaivy ingress is reference, not applied. Old CSS skins are archived, not imported.

---

## 2. Current reality

### Folder

One capitalized folder, `Site`, inside the existing Communications domain. No lowercase twin and no symlink. The live tunnel stays at `Communications/network/cloudflare` and is not this folder.

- Code: `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/Site/scripts` plus `config/` for the route manifest. Python module name `Site`. No `Logs/` on the server.
- Database: `2 - RootRecord-Database/Communications/Site/`
- Logs: `2 - RootRecord-Database/Logs/Communications/Site/`

Public UI, when a page exists, stays in `3 - RootRecord-Website` (agent 07). This function does not add a page and does not edit that app.

Secrets: `/home/rootrecord/master/master-key.env` only. This function's allowlist is empty. It does not load `CLOUDFLARE_ACCOUNT_ID` or `ROOTSERVER_TUNNEL_TOKEN`. No second env file. Key names only; values are not written here.

### 2.1 What exists

| Item | Location / status |
| --- | --- |
| Folder `Communications/Site` | Absent. Not created in this draft. |
| Database `Communications/` | Absent. |
| Logs `Communications/` | Present for the relay. Not this function. |
| Public website checkout | `3 - RootRecord-Website` is empty. |
| Vercel staging clone | `Communications/website/RootRecord-Cloud`, gitignored. Do not edit. |
| Desk tunnel | `Communications/network/cloudflare/`. Keep. |
| Globe ingress | `mirror/.cloudflared/config-globe.yml`. `www.rootrecord.cloud` → `127.0.0.1:8090`. Keep. |
| Old source | GitHub `rootrecordsoftwaresolutions/old`: `web/`, `Thumbnails/`. |
| Token dump | `web/cloudflare/cloudflare.txt` embeds tunnel-token previews. Stay out of this work order, the manifest, the Library archive, and git. |
| Master keys (names only) | `CLOUDFLARE_ACCOUNT_ID`, `ROOTSERVER_TUNNEL_TOKEN`. Not loaded by this function. |

### 2.2 Completed so far

- [x] Old source read (Cloudflare YAML, skin file list, thumbnail file list).
- [x] Folder name and the three paths written in this draft.
- [x] Route manifest, checker, and theme archive. Checker PASS 2026-09-30 00:05 HST.
- [x] Phase 4 archive and GitHub deletion of this function's files. Commit `c5b935a` on `cursor/radio-idle-obs-gates`. Token dump left.
- [x] Phase 5 result note. Staging page left unchanged because DNS did not change.

### 2.3 Known friction

- `3 - RootRecord-Website` is still empty. Public website checkout is not done. This build staged the Site files and did not check the site out.
- Apex `rootrecord.cloud` redirects to `www`, which is the globe. The Home card stays off until a DNS change is signed off. This draft does not make that change.
- `web/cloudflare/cloudflare.txt` contains token previews. It is excluded from any tracked or archived path until a secrets-safe handling is signed off. It is not deleted from GitHub in the meantime.
- A push to `RootRecord-Cloud` `main` deploys production. This function does not push.

---

## 3. Tasks

Build order, after Alexander accepts this draft and says to build. Do not start these from the draft itself.

1. Pause if `3 - RootRecord-Website` has no Vercel checkout. Name the missing function: Public website checkout. Do not check the site out. Do not edit the staging clone. Pause if `jobs.py`, the Vercel app shell, or `master-key.env` is already being edited.
2. Add `Communications/Site/config/routes.yml`: `www.rootrecord.cloud` kept on the globe origin; `ssh.rootrecord.cloud` kept; Vercel noted as the one site whose Home URL is `https://rootrecord.cloud/home`, flag `home_card: off` until a DNS change is signed off. No tokens, no `credentials-file`, no avaivy hostnames, no second tunnel.
3. Add `Communications/Site/scripts/site_check.py` (stdlib only). It reads that manifest, refuses secret-looking keys, and writes a last file under Database `Communications/Site/` plus a log line under Logs `Communications/Site/`. On demand only. No `jobs.py` edit. Add `Communications/Site/README.md`.
4. Copy the old skin unchanged into `5 - RootRecord-Library/Archive/Website-Themes/avaivy.cloud/`: `css/`, `directory/directory.css`, and the small shell `index.html` files (`index.html`, `context`, `directory`, `energy`, `status`, `system`, `uptime`, `wiki`). Keep that archive out of the Vercel build and out of folder 3.
5. Do not copy thumbnail JPGs or the generated HTML trees into Pacific, Database, the website, or git.
6. Phase 4, only after the checker passes: copy this function's old files into `Old repos deleted and merged/old/`, preserving repo-relative paths (`web/cloudflare*.yml`, `web/cloudflare/` except the token dump, the skin files, `Thumbnails/`). Then delete those same paths from the `old` repo on this machine and on GitHub, commit, and push. No force-push. Do not delete the GitHub repository. If the archive copy fails, do not delete.
7. Phase 5: append a result note to this same work order and correct only Library pages this function made stale (migration matrix row 89, and the staging note that the public domain does not reach Vercel — only if routing actually changed).

---

## 4. Non-goals

- Do not overwrite the desk tunnel, the globe ingress, `cf-status.json`, `cf-blocker.json`, or `config-globe.yml`.
- Do not run `deploy-dns.sh`, call the Cloudflare API, start a second `cloudflared`, or change Vercel project settings.
- Do not import avaivy CSS, backgrounds, or per-product skins into the Vercel app.
- Do not take the generated page trees. Leave them and name them: `web/sites/avaivy.cloud/earthquakes/`, `news/`, `weather/`, `states/` (other agents: weather dataset, news builders, quake pages). Leave `web/web-media/` (report archive) and `web/AGENTS.md` (shared web notes). Leave `web/sites/README.txt` (it points at `broadcast.py`, another function).
- Do not edit agent 09 (Cloudflare workers), `jobs.py`, folder 3, or the RootRecord-Cloud clone.
- Do not replace EcoFlow BLE, the poller, Hawaiʻi weather, the globe collector, camera grabs, Kokoro, or `geology_collect.py`.
- Do not restore files under `~/.ollama/skills/energy`, automations, or `coms/ssh/local-data-globe`.

---

## 5. Key file / path reference

| Path | Role |
|------|------|
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/Site/scripts` | Code. Add at build time. Not created by this draft. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/Site/config/routes.yml` | Route manifest. Add at build time. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/Site/scripts/site_check.py` | On-demand checker. Add at build time. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/Site/README.md` | Folder readme. Add at build time. |
| `2 - RootRecord-Database/Communications/Site/` | Last file from the checker. Runtime output only. |
| `2 - RootRecord-Database/Logs/Communications/Site/` | Checker log line only. |
| `5 - RootRecord-Library/Archive/Website-Themes/avaivy.cloud/` | Unchanged old skin. Out of the Vercel build. |
| `1 - Servers/2 - RootRecord-US-Mainland-Server/mirror/.cloudflared/config-globe.yml` | Live globe ingress. Read-only. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/network/cloudflare/` | Live desk tunnel. Read-only. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/website/` | Vercel staging clone. Read-only. |
| `3 - RootRecord-Website` | One Vercel app, owned by agent 07. Empty today. Do not edit. |
| `5 - RootRecord-Library/Documentation/00-architecture/Website-RootRecord-Cloud-Staging.md` | Staging record. Read-only until phase 5, and only if routing changed. |
| `5 - RootRecord-Library/Documentation/08-ideas/2026-09-29-globe-landing-overlay.md` | Visual direction. Read-only. |
| GitHub `rootrecordsoftwaresolutions/old` `web/cloudflare-config.yml`, `web/cloudflare-avaivy.ingress.yml`, `web/cloudflare/`, `Thumbnails/`, and the skin files in task 4 | Old source. Phase 4 archive, then delete those paths only. |
| `Old repos deleted and merged/old/` | Phase 4 archive root. Preserve repo-relative paths. |
| `/home/rootrecord/master/master-key.env` | Only secrets file. This function's allowlist is empty. Do not edit. |

---

## 6. Open items

**Additional requirements:**

- Accept this draft before any build. Until then, do not edit runtime files, restart services, send messages, actuate hardware, or spend cloud money.
- Build pause if Public website checkout has not filled `3 - RootRecord-Website`. Name that function. Do not build it here.
- Sign-off before DNS or Cloudflare API changes, running `deploy-dns.sh`, starting or restarting `cloudflared`, editing or pushing the Vercel app, cloud spend, speaker, OBS, hardware, sends, or deletion of live Ecosystem files.
- Sign-off before `web/cloudflare/cloudflare.txt` (token previews) is copied anywhere or removed from GitHub.
- Phase 4 deletion of ordinary source files waits until the archive copy is on disk. If the copy fails, do not delete.
- One test, at build time: `nice -n 10 python3 Communications/Site/scripts/site_check.py` exits 0; the manifest keeps `www` on the globe and `home_card: off`; a fixture that adds a `token` or `credentials-file` key exits non-zero; folder 3, the globe overlay, and the tunnel config are unchanged; no new `cloudflared` process.

---

## 7. Notes & constraints

- No force-push.
- Secrets stay out of git. Do not print env values. Do not commit tunnel tokens or `cloudflare.txt`.
- Prefer small reversible steps.
- New periodic jobs stay gated off. Do not edit `jobs.py`.
- Do not delete the GitHub repository `old`. Phase 4 removes only this function's old files, and only after they are in `Old repos deleted and merged`.
- Shared files left in place: generated trees `earthquakes/`, `news/`, `weather/`, `states/`; `web/web-media/`; `web/AGENTS.md`; `web/sites/README.txt`.
- Phase 4 result (2026-09-30 00:06 HST): Manifest `Communications/Site/config/routes.yml` and checker `Communications/Site/scripts/site_check.py` landed. `nice -n 10 python3 scripts/site_check.py` exited 0 (`home_card` off, `www` globe). A fixture with `token` and a fixture with `credentials-file` each exited 2. Globe ingress, `cf-status.json`, and `cf-blocker.json` were unchanged. `cloudflared` stayed at one process. Folder 3 was empty at that check. A Vercel checkout appeared in `3 - RootRecord-Website` afterward. This function did not edit it.
- Skin copied unchanged to `5 - RootRecord-Library/Archive/Website-Themes/avaivy.cloud/` and to `Old repos deleted and merged/old/web/sites/avaivy.cloud/` (css, directory.css, shell index.html). Not applied to the Vercel app.
- Cloudflare YAML and the avaivy tunnel notes, plus 24 thumbnail files, are in `Old repos deleted and merged/old/` under their old paths. Alexander allowed the thumbnail import: the same 24 files are in `3 - RootRecord-Website/media/thumbnails/`, staged in that repo, not pushed. `web/cloudflare/cloudflare.txt` was not copied and was not deleted.
- Removed from GitHub `rootrecordsoftwaresolutions/old` branch `cursor/radio-idle-obs-gates` in `c5b935a` (49 files). No force-push. The repository was not deleted. The local clone is `/tmp/rr-old-mig08`.
- Left in that repo and named here: `web/cloudflare/cloudflare.txt`; `web/sites/avaivy.cloud/{earthquakes,news,weather,states}/`; `web/sites/avaivy.cloud/js/` and `directory/directory.js`; `web/web-media/`; `web/AGENTS.md`; `web/sites/README.txt`.
- Library page corrected: migration matrix row 89, missing → partial. `Website-RootRecord-Cloud-Staging.md` was not changed. The public domain still does not reach Vercel.

---

*Work order prepared 2026-09-29 HST. Built 2026-09-30 HST. Not promoted to the active index.*

---

## Archive / location note

**Active / accepted WOs** — filename when saved:

```text
Site_Cloudflare_config_and_thumbnails_Work_Order_WO-MIG-08-2026-09-29.md
```

Location when promoted (not now):

```text
Documentation/06-development/Work-Orders/
```

**Drafts (not on active index)** — this file:

```text
Documentation/06-development/Work-Orders/drafts/
```

See `drafts/README.md` and WO-WOGEN-001. Do not auto-promote.

**Closed WOs:** set Status → COMPLETE/CLOSED → `git mv` into:

```text
Documentation/06-development/Work-Orders/Complete/
```

Human session logs archive under `Documentation/01-operations/archive/YYYY-Www/` (WO-ARCH) — separate from closed work orders.
