# 2026-10-01 — Mainland rename, SSH, and tunnels

| Field | Value |
| --- | --- |
| **When** | 2026-10-01 19:23–19:41 HST (UTC 2026-10-02 05:23–05:41) |
| **Operator** | Alexander |
| **Writer** | Grok, from the same desk session |
| **State** | Evening checks are below. Alexander locked the radio plan the same day. That lock is [What is true now](#what-is-true-now). `ssh.rootrecord.cloud` is retired. Mainland One is radio only |
| **Commits** | none |
| **Secrets** | No tokens, private keys, or credential files are copied here. Key paths and public fingerprints only |

This is the record of three requests in one sitting: check Mainland One after a restart, publish an SSH path that survives the next address change, rename the two Mainland folders and GitHub repositories, then start the same SSH path for Mainland Two.

## Names

| What | Now |
| --- | --- |
| Mainland One desk folder | `1 - Servers/2 - RootRecord-US-Mainland-One/` |
| Mainland One GitHub | https://github.com/RootRecord-Software-Solutions/US-Mainland-One |
| Mainland One on the AWS host | `/home/ubuntu/US-Mainland-Server/` (that directory was not renamed). The radio runtime is `/home/ubuntu/rootrecord-radio` |
| Mainland Two desk folder | `1 - Servers/3 - RootRecord-US-Mainland-Two/` |
| Mainland Two GitHub | https://github.com/RootRecord-Software-Solutions/US-Mainland-Two |
| Mainland Two on its host | `/home/ubuntu/US-Mainland-Server-2/` in the unit files (directory on the machine was not renamed) |
| Old folder | `1 - Servers/2 - RootRecord-US-Mainland-Server/` (gone from disk; git still has it as a deletion until the rename is added) |
| Old Two folder in `.gitignore` | `1 - Servers/3 - RootRecord-US-Mainland-Server 2/` |
| Old GitHub names | `US-Mainland-Server` and `US-Mainland-Server-2`. GitHub redirects both to the new names |

Mainland One has no `.git` of its own. The umbrella publishes it with the `mainland` row. Mainland Two has its own `.git`. The umbrella ignores it.

## Desk SSH config

File: `~/.ssh/config`. Written 2026-10-01. No other hosts are in that file. The table is what the aliases did during the evening checks. The locked hostnames are in [What is true now](#what-is-true-now). `ssh.rootrecord.cloud` is retired.

| Alias | How it connects | Key | Result this evening |
| --- | --- | --- | --- |
| `ml1` | `cloudflared access ssh` to hostname `ssh.rootrecord.cloud` | `~/.ssh/rootrecordkey.pem` | **PASS**. Remote hostname `ip-172-31-10-115` |
| `rr-aws` | same tunnel as `ml1` | same pem | same path as `ml1` |
| `rr-aws-ip` | direct `ubuntu@3.140.195.32:22` | same pem | **PASS** before the tunnel was switched on |
| `ml2` | direct `ubuntu@3.149.238.83:22` | `/home/rootrecord/Downloads/rr-stream-server.pem` | **PASS**. Remote hostname `ip-172-31-15-254` |

The cloudflared binary used by `ml1` and `rr-aws` is:

`1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/network/cloudflare/bin/cloudflared`

Version on the desk binary is 2026.9.1. Both AWS hosts that were checked have the package `cloudflared` 2026.9.3.

`ProxyCommand` for `ml1` and `rr-aws`:

```text
cloudflared access ssh --hostname %h
```

`%h` is `ssh.rootrecord.cloud`, because that is the hostname the live tunnel ingress actually serves. `ml1.rootrecord.cloud` is not in that ingress.

## Mainland One after the restart

Alexander restarted Mainland One. The saved aliases still pointed at `18.118.30.226`.

| Check | Result |
| --- | --- |
| `ssh rr-aws` to `18.118.30.226:22` | timed out |
| TCP 22, 80, 443, 8091, 8787 on `18.118.30.226` | each timed out at 4 s |
| ping `18.118.30.226` | 2 sent, 0 received |
| `https://api.rootrecord.cloud/api/state` | curl exit 28, timeout 8 s, HTTP 000 |
| `https://www.rootrecord.cloud/` | HTTP 200 in 0.32 s (Vercel, not the AWS host) |
| DNS `ssh.rootrecord.cloud` and `api.rootrecord.cloud` | still A `18.118.30.226` at that moment |

The desk could reach the internet. The old public address did not answer.

Alexander then gave the new address `3.140.195.32`.

| Check | Result |
| --- | --- |
| `ssh -i ~/.ssh/rootrecordkey.pem ubuntu@3.140.195.32` | **PASS** |
| Hostname | `ip-172-31-10-115` |
| Uptime at 05:28 UTC | 5 minutes |
| Host key | ED25519 `SHA256:KdsqhyZ0zGl+ezS07KKNUh9U5kO2WPgJt37VgewFbXA` |
| `cloudflared` | `/usr/bin/cloudflared`, symlink from `/usr/local/bin/cloudflared`, version 2026.9.3 |
| Unit | `cloudflared-network-globe.service` **active** |
| Other `cloudflared.service` | inactive |
| `sudo` | not required for the read; the service restart later used `sudo` and succeeded |

`~/.cloudflared` on that host, mode `0700`, contained:

- `939b16f7-7d13-4776-bd4d-80fe8021fc72.json` (credential file, not read out)
- `config-globe.yml`
- `config-globe.yml.bak-api`

Local ingress in `config-globe.yml` before the edit:

```yaml
tunnel: 939b16f7-7d13-4776-bd4d-80fe8021fc72
credentials-file: /home/ubuntu/.cloudflared/939b16f7-7d13-4776-bd4d-80fe8021fc72.json
ingress:
  - hostname: api.rootrecord.cloud
    service: http://127.0.0.1:8091
  - service: http_status:404
```

The bak file still had `www.rootrecord.cloud` → `http://127.0.0.1:8090` and `ssh.rootrecord.cloud` → `ssh://localhost:22`. No `cert.pem` was on the host. `/root/.cloudflared` was absent.

The unit file is `/etc/systemd/system/cloudflared-network-globe.service`. It runs:

```text
/usr/bin/cloudflared --no-autoupdate --config /home/ubuntu/.cloudflared/config-globe.yml tunnel run
```

Description text still says the tunnel is for `api.rootrecord.cloud` and that DNS for the API is an A record.

## Why a new tunnel object was not created

The desk token is `API_TOKEN` in `/home/rootrecord/master/master-key.env`, with `CLOUDFLARE_ACCOUNT_ID`. The token is not copied here.

| Call | Result |
| --- | --- |
| `GET /user/tokens/verify` | 401, `Invalid API Token` |
| `GET /zones?name=rootrecord.cloud` | 200. Zone exists. Account name on the zone: Alexanderstorey94@gmail.com's Account |
| `GET /accounts/…/cfd_tunnel` | 200 and an empty list |
| `GET` the known tunnel id | 401 Not authorized |
| `POST` create tunnel `ml2-probe` was not kept; the real create call returned | 403, code 10000, Authentication error |
| `GET` and `PUT` `/cfd_tunnel/…/configurations` | 401 Not authorized |
| `GET /accounts/…/access/apps` | 200, zero apps |
| `POST` an Access SSH app for `ml1.rootrecord.cloud` | 403 `auth.forbidden` |
| `POST` and `PUT` DNS records | 200 |

So this token can edit DNS for `rootrecord.cloud` and cannot create a tunnel, edit tunnel ingress, or create an Access application.

`cloudflared tunnel create` on a host also fails without `cert.pem`. There is no origin certificate on the desk or on either host that was checked.

## What was changed for Mainland One SSH

The tunnel that is already running is remotely configured. After `systemctl restart cloudflared-network-globe.service` the log said it registered QUIC connections in `cmh01` and `ord07`, then replaced the local ingress with the dashboard config:

```text
www.rootrecord.cloud  → http://127.0.0.1:8090
ssh.rootrecord.cloud  → ssh://127.0.0.1:22
(no hostname)         → http_status:404
```

A local rule for `ml1.rootrecord.cloud` was written into `config-globe.yml` and into the desk mirror `mirror/.cloudflared/config-globe.yml`. The running connector does not use that rule. The log line `Updated to new configuration` is the remote config winning.

Because `ssh.rootrecord.cloud` was already in the live ingress, its DNS was moved onto the tunnel:

| Name | Before | After |
| --- | --- | --- |
| `ssh.rootrecord.cloud` | A `18.118.30.226`, proxy off | CNAME `939b16f7-7d13-4776-bd4d-80fe8021fc72.cfargotunnel.com`, proxied |
| `ml1.rootrecord.cloud` | absent | CNAME to the same tunnel, proxied |
| `api.rootrecord.cloud` | A `18.118.30.226`, proxy off | **unchanged**. Still the dead address |

`ml1.rootrecord.cloud` through `cloudflared access ssh` returns `websocket: bad handshake` and `failed to connect to origin`. The edge has the CNAME and does not have an ingress rule for that name.

`ssh.rootrecord.cloud` through `cloudflared access ssh` reaches sshd. The first ProxyCommand attempt failed on a stale `known_hosts` line (a different ED25519 key). `ssh-keygen -R ssh.rootrecord.cloud` removed it. The new key matches `3.140.195.32`. A later `ssh ml1` printed `CONNECTED`, hostname `ip-172-31-10-115`, uptime about 10 minutes, and `http://127.0.0.1:8091/api/state` on that host returned HTTP 200.

A listener test (`cloudflared access ssh --url 127.0.0.1:2222`, then SSH to that port) also returned `CONNECTED`. That listener was stopped. Nothing was left listening on 2222 or 2223.

Host key warning text is normal when the instance is replaced. The fingerprint above is the one that matched the new address.

## Mainland rename

Alexander renamed the folders and the GitHub repositories, then asked for every reference to be updated.

Confirmed with `gh repo view`: both new repositories exist. Asking GitHub for the old names returns the new names (redirect).

### Git

| Item | State |
| --- | --- |
| Umbrella index | still lists 176 paths under `1 - Servers/2 - RootRecord-US-Mainland-Server/`. On disk those files are the One folder. `git status` shows them deleted until they are added at the new path. Not staged. Not committed |
| Mainland One `.git` | none |
| Mainland Two `origin` | was `git@github.com:RootRecord-Software-Solutions/US-Mainland-Server-2.git`. Set to `git@github.com:RootRecord-Software-Solutions/US-Mainland-Two.git`. That is local git config, not a commit |
| `.gitignore` | the nested-repo ignore is now `1 - Servers/3 - RootRecord-US-Mainland-Two/` |

`repos.conf` mainland row, enabled:

```text
mainland	1	mirror	/home/rootrecord/RootRecord-Ecosystem/1 - Servers/2 - RootRecord-US-Mainland-One	RootRecord-Software-Solutions/US-Mainland-One	origin
```

### Text that was rewritten

A script replaced desk paths, GitHub slugs, and the names `US-Mainland-Server` / `US-Mainland-Server-2` in live text files. `/home/ubuntu/US-Mainland-Server` and `/home/ubuntu/US-Mainland-Server-2` were protected and put back, so unit files and pull scripts still start in those host directories.

Places that now say One and Two include:

- `.gitignore`, root `README.md`, Pacific `README.md`, Library `README.md`
- `0 - Master-Prompt/MASTER-PROMPT.md`, `README.md`, `prompts/07-current-state.md`, `prompts/08-repository-and-file-links.md`
- `Github/scripts/repos.conf` and `Github/README.md`
- Control panel `rr_pages.py`, `Lib/rr_ssh.py`, `Lib/rr_migration.json`
- `Media/Voice/scripts/radio_push.py` desk path. The radio runtime it replaces is `/home/ubuntu/rootrecord-radio`
- Agent context `REPOS.md` and `ROLE-AND-BOUNDS.md` for Ava, Bruce, and Carly
- Live library docs, work orders, and the operators handbook
- Mainland One `README.md`, `SKILL.md`, `INDEX.md`, `references/GITHUB-IDENTITY.md` (commit identity label is now `US-MAINLAND-ONE`)
- Mainland Two `README.md` title and the git-pull unit description

The current architecture stub is `Documentation/../15-Domains-and-External-Systems/US-Mainland-One.md`. The long page is `Documentation/15-Domains-and-External-Systems/US-Mainland-One.md`. The September 29 page is a historical import record. Its names were rewritten with the same script, so it no longer says the old folder name, and it still describes 2026-09-29.

### Left unchanged on purpose

| Left as-is | Why |
| --- | --- |
| `/home/ubuntu/US-Mainland-Server` and `/home/ubuntu/US-Mainland-Server-2` | Those are directories on the hosts. Renaming the strings in unit files would point systemd at folders that were not renamed |
| `Documentation/archive/` and `01-operations/archive/` | Frozen records of the old names |
| `2 - RootRecord-Database/Worklog/` | Generated scan logs of paths as they were that hour |
| `2 - RootRecord-Database/Archive/Github-desk-backups/` | Point-in-time backups. A first pass edited them. They were reverted |
| `Github-worktrees/` and `Old repos deleted and merged/` | Not the live trees |
| `api.rootrecord.cloud` A record | Left alone that evening. The later lock aims it at Mainland Two. The API process is not there yet |

## Mainland Two

Address given: `3.149.238.83`.

| Key | User | Result |
| --- | --- | --- |
| `~/.ssh/rootrecordkey.pem` (RSA `SHA256:kbmyxc3HSNGp+olzxbhiJulDS48G0IfmDRwZTqd4XWE`) | ubuntu, ec2-user, admin, root | publickey denied |
| `~/.ssh/id_ed25519` | ubuntu | denied |
| `~/.ssh/id_ed25519_rootrecord` | ubuntu | denied |
| `/home/rootrecord/Downloads/rr-stream-server.pem` (RSA `SHA256:Jt2eZPiX8QFjd+gJ6CH2eErHoYJV9OaoW0ij0Zorj3U`) | ubuntu | **PASS** |

Host key for `3.149.238.83` was added to `known_hosts` on first contact. Hostname `ip-172-31-15-254`. At 05:39 UTC the host had been up 7 minutes. `sudo -n` works for ubuntu. `cloudflared` was not installed. `~/.cloudflared` did not exist.

Installed on the host:

```text
cloudflared-linux-amd64.deb from the GitHub latest release
package cloudflared 2026.9.3
```

The deb was removed from `/tmp` after `dpkg`.

`POST` create tunnel `ml2` returned the same 403 as before. On the host, `cloudflared tunnel create ml2` exited 1: no origin certificate. A copy of the desk API token was placed in `/home/ubuntu/.cloudflared/api.env` for that attempt and then deleted.

`cloudflared tunnel login` was started so it could write `cert.pem` after an account login. Process 2836 was still running at 05:41 UTC, logging to `/tmp/cf-login.log`. The desk browser opened the URL it printed and landed on the Cloudflare sign-in page. Nobody signed in. The certificate was not issued. `ml2.rootrecord.cloud` was not created in DNS. No tunnel id exists for Two.

`ssh ml2` at 05:41 UTC printed `CONNECTED` and hostname `ip-172-31-15-254` (uptime 8 minutes). That is the direct address, not a tunnel.

## What is true now

Alexander locked this on 1 Oct 2026. The evening sections above are the checks from that sitting. They are not the live routes.

Mainland One is radio only going forward. `www.rootrecord.cloud` stays on Vercel. Do not point `www` at the tunnel. `ssh.rootrecord.cloud` is retired. `api.rootrecord.cloud` is aimed at Mainland Two. The API process is not there yet. Do not treat it as live on Mainland One. `rootserver.rootrecord.cloud` stays on the Pacific desk. Earthquake and hurricane voice reports are Pacific poller jobs, not the Mainland globe. Pollers are planned to move to Mainland Two later. They have not moved.

Desk SSH:

| Alias | How it connects | Direct fallback |
| --- | --- | --- |
| `ml1` | `cloudflared access ssh` to `ml1.rootrecord.cloud` | none on this alias |
| `rr-aws` | same tunnel hostname as `ml1` | none on this alias |
| `rr-aws-ip` | direct `ubuntu@3.140.195.32:22` | this alias is the fallback |
| `ml2` | `cloudflared access ssh` to `ml2.rootrecord.cloud` | `ml2-ip` is `3.149.238.83` |

Do not restart cloudflared over `ssh ml1`. That session is the tunnel.

Tunnel `Mainland-One`, id `939b16f7-7d13-4776-bd4d-80fe8021fc72`:

| Hostname | Service |
| --- | --- |
| `ml1.rootrecord.cloud` | `ssh://localhost:22` |
| `radio.rootrecord.cloud` | `http://127.0.0.1:8092` |

Tunnel `Mainland Two`, id `bd8e68a4-8a97-4b20-afd9-b058473a0a22`:

| Hostname | Service |
| --- | --- |
| `ml2.rootrecord.cloud` | SSH |

## Radio

The station page is [2026-10-01 radio station](./2026-10-01-radio-station.md).

The listener stream is `https://radio.rootrecord.cloud/radio/live.mp3`. That response is `audio/mpeg` at 128 kbps. Now-playing is `https://radio.rootrecord.cloud/radio/now.json`. The public mix is not the library file format.

The station library is one filetype, Opus (`.opus`). Reports are 24 kbps mono. Chimes are 48 kbps. Music is 96 kbps. A report file is `<report>_current.opus`. A chime is `hour-HH-MM.opus`. Music is `.opus`.

Hawaii still renders a WAV. `Media/Voice/scripts/radio_push.py` encodes that one report to Opus and replaces it on the Mainland runtime. Prune keeps both `*_current.ogg` and `*_current.opus` until that report is replaced, then deletes only that report's old ogg.

The runtime on the host is `/home/ubuntu/rootrecord-radio`. The checkout and the desk folder `1 - Servers/2 - RootRecord-US-Mainland-One` are the radio tree only, commit `9b7fccf`. The old globe and poller directories are not in that tree.

A watchdog on Mainland One is `rr-radio-watchdog.timer`. It runs once a minute. The script is `/home/ubuntu/radio-watchdog.sh`. It starts one `rr-radio-station.service` when a release is ready, and restarts that service only if the heartbeat is older than 30 seconds. The old `rr-radio-stream` and `rr-radio-watch` units stay masked. The host pull is `/home/ubuntu/aws-git-pull.sh`. It fast-forwards the checkout, copies the Opus music bed and chimes into the runtime, and restarts the station when `stream.js` or `radio.js` changed.

The public station is playing that Opus bed. Reports still arrive over `ssh ml1` into `audio/reports`, outside git. Only the current Hawaii daypart rollup is kept. The guide is [2026-10-01 radio station](./2026-10-01-radio-station.md).

The published site requests `https://radio.rootrecord.cloud/radio/live.mp3` and `.../now.json` from `Website/Home/radio/index.html`, `Website/Home/live/index.html`, `assets/radio.js`, `assets/live-radio.js`, and `assets/broadcast-mode.js`. Those pages stay on `www.rootrecord.cloud`.
