# Test record — Mainland One tunnel SSH and Mainland Two direct SSH

| Field | Value |
| --- | --- |
| **Date / time (HST)** | 2026-10-01 19:23–19:41 HST |
| **Tester** | Grok, for Alexander |
| **Change under test** | SSH after the Mainland One restart; DNS for `ssh.rootrecord.cloud` and `ml1.rootrecord.cloud`; desk `~/.ssh/config`; start of the same path for Mainland Two at `3.149.238.83` |
| **State** | Mainland One tunnel SSH **PASS**. `ml1.rootrecord.cloud` **FAIL**. Mainland Two direct SSH **PASS**. `ml2.rootrecord.cloud` **BLOCKED** |
| **Evidence** | [2026-10-01 mainland rename and SSH tunnels](../01-operations/2026-10-01-mainland-rename-and-ssh-tunnels.md) |
| **Commits** | none |
| **Backup** | `config-globe.yml.bak-before-ml1` on the Mainland One host. `~/.ssh/known_hosts.old` after `ssh-keygen -R ssh.rootrecord.cloud`. No new desk backup directory |

The full command log, DNS table, rename list, and what was left unchanged are in the operations record linked above. This file is the pass/fail gate.

## What was tested

1. Whether the desk could still reach Mainland One on the address saved in `~/.ssh/config`.
2. Whether SSH to the new address `3.140.195.32` worked, and whether a Cloudflare path would still work after the next address change.
3. Whether `ml2.rootrecord.cloud` could be created the same way for `3.149.238.83`.

## How

Old address, from the desk:

```bash
ssh -o BatchMode=yes -o ConnectTimeout=12 -i ~/.ssh/rootrecordkey.pem ubuntu@18.118.30.226 'uptime'
curl -sS -m 8 -o /dev/null -w '%{http_code}\n' https://www.rootrecord.cloud/
curl -sS -m 8 -o /dev/null -w '%{http_code}\n' https://api.rootrecord.cloud/api/state
```

New Mainland One address, then the tunnel:

```bash
ssh -o BatchMode=yes -o ConnectTimeout=12 -i ~/.ssh/rootrecordkey.pem ubuntu@3.140.195.32 'hostname; uptime'
ssh -o BatchMode=yes -o ConnectTimeout=20 ml1 'echo CONNECTED; hostname; uptime'
```

Mainland Two:

```bash
ssh -o BatchMode=yes -o ConnectTimeout=12 ml2 'echo CONNECTED; hostname; uptime'
```

`ml2` in `~/.ssh/config` is direct to `3.149.238.83` with `/home/rootrecord/Downloads/rr-stream-server.pem`.

## Pass criteria

1. A command on Mainland One returns hostname and uptime without using `18.118.30.226`.
2. That path is `cloudflared access ssh`, so a later public-IP change does not change the desk alias.
3. The same kind of path exists for `ml2.rootrecord.cloud`.

## Result

| Gate | State | Evidence |
| --- | --- | --- |
| Old address `18.118.30.226` ports 22, 80, 443, 8091, 8787 | **FAIL** (host unreachable) | each connect timed out at 4 s; ping 0/2; API curl timed out at 8 s |
| Desk internet | **PASS** | `https://www.rootrecord.cloud/` HTTP 200 in 0.32 s |
| Direct SSH `ubuntu@3.140.195.32` | **PASS** | hostname `ip-172-31-10-115`, up 5 min at 05:28 UTC |
| `ssh ml1` / `ssh rr-aws` via `ssh.rootrecord.cloud` | **PASS** | `CONNECTED`, same hostname, up about 10 min; `http://127.0.0.1:8091/api/state` on that host returned 200 |
| `ml1.rootrecord.cloud` | **FAIL** | `websocket: bad handshake`. DNS CNAME exists. Live tunnel ingress does not list that name |
| New tunnel object | **BLOCKED** | API create returned 403. No origin cert on the desk or the host |
| Direct SSH `ubuntu@3.149.238.83` as `ssh ml2` | **PASS** | `CONNECTED`, hostname `ip-172-31-15-254`, up 8 min at 05:41 UTC |
| `ml2.rootrecord.cloud` | **BLOCKED** | `cloudflared` 2026.9.3 installed. `cloudflared tunnel login` was waiting. The browser showed the Cloudflare sign-in page. No certificate, no tunnel, no DNS name |

`api.rootrecord.cloud` was not changed. It is still an A record for `18.118.30.226`.

## Resource impact

| When | Load (1/5/15) | MemAvailable | Swap used | Peak RSS |
| --- | --- | --- | --- | --- |
| Mainland One at 05:28 UTC | 0.11, 0.27, 0.16 | not recorded | not recorded | not recorded |
| Mainland One at the passing `ssh ml1` | 0.01, 0.13, 0.13 | not recorded | not recorded | not recorded |
| Mainland Two at 05:39 UTC | 0.18, 0.08, 0.03 | not recorded | not recorded | not recorded |
| Mainland Two at the passing `ssh ml2` | 3.05, 1.00, 0.36 | not recorded | not recorded | not recorded |

Desk memory was not sampled. The load on Mainland Two rose during `dpkg` of cloudflared. No desk service was restarted.

## Cleanup confirmation

- The local `cloudflared access ssh --url 127.0.0.1:2222` and `:2223` listeners were killed.
- `/home/ubuntu/.cloudflared/api.env` on Mainland Two was deleted after the failed `tunnel create`.
- `cloudflared tunnel login` on Mainland Two was still running as pid 2836 at 05:41 UTC, waiting for a sign-in. That process was left on purpose.
- No Ollama or FLM model was started.
