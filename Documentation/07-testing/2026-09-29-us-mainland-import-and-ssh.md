# Test record — US-Mainland-Server import, layout setup, and SSH path checks

| Field | Value |
| --- | --- |
| **Date / time (HST)** | 2026-09-29 13:45–13:55 HST |
| **Tester** | Grok (executor, us-mainland-import pass) |
| **Change under test** | Desk clone of `rootrecordsoftwaresolutions/US-Mainland-Server` into `1 - Servers/2 - RootRecord-US-Mainland-Server`; root `.env.example`, README layout section, `.gitignore` bytecode rule; local `~/.ssh/config` `rr-aws` ProxyCommand path. [Architecture](../00-architecture/US-Mainland-Server.md) |
| **State** | Import **PASS** · setup **LANDED** (uncommitted) · `rr-aws` **FAIL** (remote: no tunnel connector) · `rr-aws-ip` **FAIL** (stale IP) · read-only SSH to current IP **PASS** |
| **Evidence** | this record (outputs quoted below) |
| **Commits** | Mainland: none (not in auto-sync, no git writes) · Library: see worklog *us-mainland-import pass* |
| **Backup** | `/home/rootrecord/Database/GITHUB/us-mainland-import.bak-20260929-134629/` (target tgz + listing, `ssh/config`, clone originals, Library files) |

## What was tested

1. Pre-checks: target folder, `gh auth status`, repo visibility.
2. Clone and placement without deleting the pre-existing target content.
3. `.env.example` contains names only; `.env` ignored.
4. `rr-aws` after the ProxyCommand path fix — exactly one `ssh -o BatchMode=yes -o ConnectTimeout=5 rr-aws uptime`.
5. Read-only diagnosis of why (DNS, HTTPS status of the tunnel hostnames, TCP 22 on the `rr-aws-ip` address).
6. One read-only SSH session to the address the desk globe collector actually uses ([redacted public IP]).

## How (exact commands / procedure)

```bash
gh auth status          # logged in as rootrecordsoftwaresolutions (keyring), scopes repo/workflow/read:org/gist
gh repo view rootrecordsoftwaresolutions/US-Mainland-Server --json visibility,...   # PUBLIC, main, pushed 2026-09-29T04:40Z
# target existed (empty Communications/ from 2026-09-27, not a git repo) -> git refuses non-empty dir:
git clone https://github.com/rootrecordsoftwaresolutions/US-Mainland-Server.git "1 - Servers/.us-mainland-clone-staging"
# conflict check per entry, then mv each entry (incl. .git) into the target; rmdir the empty staging dir
git status --short      # clean, HEAD b61d63c
# ssh config: one line changed (backup first)
ssh -o BatchMode=yes -o ConnectTimeout=5 rr-aws uptime          # wrapped in timeout 40
getent hosts ssh.rootrecord.cloud; curl -s -o /dev/null -w '%{http_code}' https://ssh.rootrecord.cloud
python3 -c 'socket connect [redacted public IP]:22, 6 s'
ssh -o BatchMode=yes -o ConnectTimeout=5 -o HostName=[redacted public IP] rr-aws-ip '<read-only: hostname, uptime, df, free, systemctl list-units, ls, du, git log -1>'
```

## Pass criteria (written before running)

1. Clone lands at the target with a clean `git status`, token-free remote URL, and nothing pre-existing deleted.
2. `.env.example` has no values; `git check-ignore .env` true.
3. SSH: `uptime` output returned within the timeout = PASS; otherwise FAIL with the cause recorded. No mutating command sent.

## Result

| # | Result | State |
| --- | --- | --- |
| 1 | HEAD `b61d63c`, `origin https://github.com/rootrecordsoftwaresolutions/US-Mainland-Server.git` (no token), status clean; placeholder `Communications/` still present (untracked, empty) | **PASS** |
| 2 | 57 variable names, 0 values; `.env`, `.env.local` ignored, `.env.example` tracked via existing `!.env.example` rule | **PASS** |
| 3a | `rr-aws`: cloudflared starts from the new path, then `websocket: bad handshake` / `Connection closed by UNKNOWN port 65535`, exit 255 (0.7 s) | **FAIL** (remote side) |
| 3b | `ssh.rootrecord.cloud` + `www.rootrecord.cloud` resolve to Cloudflare, HTTPS **530 / error code 1033** (no tunnel connector) | cause found |
| 3c | `[redacted public IP]:22` connect timeout (errno 11) | **FAIL** (stale IP) |
| 3d | [redacted public IP]: `[redacted internal hostname]`, up 3 d 9 h, load 0.32, disk 5.1/6.7 G (77 %), 514 MB RAM avail; running `rr-rootserver-poller`, `network-globe-feed-server`, `network-globe-connection-history`, `github-poller`; no cloudflared; `hawaii.ndjson` 1,815,325,001 B; repo HEAD `b61d63c` | **PASS** (read-only) |

**Finding:** Hawaii feed grows ≈ 39 MB/h and the AWS trim script is missing (desk journal: `maintain-hawaii-feed.sh: No such file or directory`, exit 127 every 15 min) → root disk full in ≈ 40 h. Escalated as P0 in the [plan](../08-ideas/2026-09-29-aws-mainland-improvement-plan.md).

## Resource impact

| When | Load (1/5/15) | MemAvailable | Swap used | Peak RSS |
| --- | --- | --- | --- | --- |
| before (13:45) | not recorded | 6,800 MB | 491 MB | — |
| during | not recorded | not recorded (clone 1.7 s, ssh < 3 s each) | not recorded | not recorded |
| after | see worklog | see worklog | — | — |

## Cleanup confirmation

- [x] no ssh / cloudflared process left (`pgrep -af "cloudflared access"` = none)
- [x] staging dir removed (empty after the move); no temp files left (`/tmp/rr-probe.html` removed)
- [x] no model, no sudo, no restart, no git write (clone only), no AWS mutation

## Open items / caveats

- Enable auto-sync row (sign-off), then the 3 pending files commit + reach AWS in ~60 s.
- P0 disk fix on AWS, Elastic IP / `rr-aws-ip` HostName update, cloudflared on AWS — all need Alexander's OK.
