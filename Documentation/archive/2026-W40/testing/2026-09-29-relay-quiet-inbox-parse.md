# Test record — Relay quiet-mode inbox + replay (parse only)

| Field | Value |
| --- | --- |
| **Date / time (HST)** | 2026-09-29 04:02:14–04:03 HST |
| **Tester** | executor agent (g3-proposals-impl) |
| **Change under test** | `council-relay.py` quiet-mode hold → `Database/Logs/Communications/Relay-Inbox/relay-inbox_current.jsonl` (hourly `Archive/`), `relay-inbox-replay.py`, Database `.gitignore`. Proposal: [08-ideas relay quiet mode](../08-ideas/2026-09-29-relay-quiet-mode-message-hold.md) |
| **State** | **PASS** (parse / refusal / ignore) · live hold **VERIFY PENDING (next poller start)** |
| **Evidence** | `2 - RootRecord-Database/Logs/Migration/g3-proposals-impl-evidence-20260929T140900Z.md` |
| **Commits** | Pacific `5353e1f` (relay + replay) · `52573e7` (README) · Database `57172d0` (.gitignore + Relay-Inbox README) |
| **Backup** | `/home/rootrecord/Database/GITHUB/g3-proposals-impl.bak-20260929-035910/` |

## How (exact commands / procedure)
The relay module was imported (`main()` was not run) and `api()` was replaced with a tripwire that raises. `inbox_hold()` was then called for 4 synthetic updates in a temp dir, after seeding a record from the previous hour. After that:

```bash
env -u RR_RELAY_REPLIES python3 relay-inbox-replay.py --inbox "$T"          # list
env -u RR_RELAY_REPLIES python3 relay-inbox-replay.py --inbox "$T" --json
env -u RR_RELAY_REPLIES python3 relay-inbox-replay.py --inbox "$T" --send   # must refuse
RR_RELAY_REPLIES=0      python3 relay-inbox-replay.py --inbox "$T" --send   # must refuse
env -u RR_RELAY_REPLIES python3 relay-inbox-replay.py                        # real inbox
git check-ignore -v --no-index Logs/Communications/Relay-Inbox/{relay-inbox_current.jsonl,Archive/2026-09-29/relay-inbox_2026-09-29_0400.jsonl,replayed.jsonl,README.md}
```

## Pass criteria (written before running)
1. Each held line is valid JSON with ts, chat id, from, persona target, message_id and text. The files are 0600.
2. The earlier-hour record is rotated into `Archive/YYYY-MM-DD/relay-inbox_YYYY-MM-DD_HH00.jsonl`.
3. Replay lists every item. `--send` without `RR_RELAY_REPLIES=1` is refused (rc 3), with no ledger written and `api()` never called.
4. The inbox files are git-ignored and the README is not.

## Result
1. Keys: chat_id, chat_type, from, message_id, persona_target, received_ts, status, text, ts, update_id. Targets: `bruce` (mention), `pipeline:ava>bruce>carly>ava` (trigger), `ava` (private), `ava` (default). Mode `-rw-------`. **PASS**
2. `Archive/2026-09-29/relay-inbox_2026-09-29_0300.jsonl` was created. **PASS**
3. records=5, pending=5, unparsed=0. Both sends were refused (rc 3), no `replayed.jsonl` was written, and the tripwire never fired. The real inbox had records=0 (not created yet). **PASS**
4. The three data paths are ignored by `.gitignore:89`, and `README.md` is re-included by `.gitignore:90`. **PASS**
5. `py_compile` passed for both scripts. The running relay (PID 105964) was not touched.

## Resource impact
Two short python runs (< 0.5 s). Load/memory not recorded.

## Cleanup confirmation
- [x] temp dir `/tmp/rr-relay-inbox-test.*` removed · [x] no process left · [x] nothing sent, no model

## Open items / caveats
- It runs live from the next poller start (the relay is in the poller unit cgroup, `KillMode=control-group`). Check: the first quiet message produces a `held in Relay-Inbox` log line and one JSONL line.
- Sending held replies (`--send` + `RR_RELAY_REPLIES=1`) needs Alexander's sign-off.
