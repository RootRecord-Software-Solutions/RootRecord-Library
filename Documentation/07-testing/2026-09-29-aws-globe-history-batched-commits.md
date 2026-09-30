# Test record: AWS globe history recorder with batched SQLite commits and a persisted cursor

| Field | Value |
| --- | --- |
| **Date / time (HST)** | 2026-09-29 15:45–15:52 HST (copy tests), 15:49:50 live restart |
| **Tester** | Grok (executor) for Alexander Storey (AWS changes approved 15:40 HST) |
| **Change under test** | AWS `~/network-globe/network-globe/connection-history.py` (`network-globe-connection-history.service`). [Proposal Phase 2](../08-ideas/2026-09-29-aws-fallback-rebuild.md) |
| **State** | **PASS**: copy test, synthetic trim/restart test and live test. Flows and counters still update, and writes are **~27× lower** |
| **Evidence** | the outputs below; mirror `US-Mainland-Server mirror/network-globe/network-globe/connection-history.py` (new, sha256 `ed1423a3…0d56`) + `connection-history.aws-live-2026-09-26.py` (the old live copy) |
| **Commits** | Library: desk auto-sync (see the worklog). Mainland: none (checkout not in auto-sync) |
| **Backup** | AWS `~/rootrecord/bin.bak-fallback-phase2-20260929-154333/connection-history.py` (matched live before the swap, `cmp` OK) |

## What was wrong (read from the live script)

1. `ingest()` ran `c.commit()` after **every record**. That was ~300 write syscalls/s, **43.9 MB of writes per minute** for the process, and 138 GB written in 3.4 days, which was the main cause of the iowait.
2. The byte cursor lived only in memory, so **every restart re-read the whole feed** and counted it again.
3. When the feed shrank (`size < offset`, which is what an in-place trim does), the cursor reset to 0. The retained ~48 MiB window was then **counted a second time**. Today's `sum(observations)` was 2.23 M, inflated by this.
4. When a 2 MB chunk ended mid-line, the partial last line was counted as consumed and lost.

## Fix

- One transaction, committed every `GLOBE_HISTORY_COMMIT_SEC` (default 5 s), plus a commit before the daily send.
- Only whole lines are consumed; a partial tail waits for the next pass.
- The cursor is saved as `data/hawaii-history-cursor.json` `{inode, offset}` after each commit.
  - First start: begin at the end of the file, because the DB already holds what the feed contained.
  - Same inode after a shrink: `offset = size`, because the retained window was already counted.
  - New inode: start from 0.
- `GLOBE_HISTORY_SEND=0` turns off the daily Telegram send. It is only for test copies; the default is unchanged (send).

## How (exact procedure)

```bash
# copy test: DB copied with sqlite backup() to ~/rootrecord/tmp-hist-test/copy.sqlite3 (disk, not tmpfs), real feed read-only
GLOBE_DB=$T/copy.sqlite3 GLOBE_HISTORY_STATE=$T/cursor.json GLOBE_HISTORY_SEND=0 nice -n 10 python3 connection-history.py &
# 60 s: /proc/<pid>/io write_bytes + syscw for the NEW copy and the OLD live service side by side
# synthetic test: 100-line feed, then +50 lines + a partial line, complete it, in-place trim (like maintain-hawaii-feed.sh), +10, restart, +7 while down
# live: mv .connection-history.py.new -> connection-history.py (after py_compile); systemctl restart network-globe-connection-history; 60 s io
```

## Results

| Check | Result |
| --- | --- |
| Copy vs live side by side (60 s) | **new: 1.86 MB written, 872 syscw** · old live: **43.9 MB, 17,878 syscw** |
| Copy: flows / counters | rows 1,759 → 1,761, `sum(observations)` 2,228,114 → 2,229,905, `max(last_seen)` advanced 60 s |
| Synthetic A–F | A start at the end: 0 · B +50 whole lines + 1 partial: 50/100 packets · C partial completed: 51/102 · **D in-place trim: unchanged 51/102** · E +10 after the trim: 61/122 · **F restart after +7 written while down: 68/136 (resumed, no re-ingest)**: all as expected |
| Live after the restart (60 s) | **1.60 MB written, 745 syscw** (was 43.9 MB / 17,878), RSS 24 MB. Rows 1,762; observations 2,232,490 → 2,234,018; cursor saved |
| Live in-place trim | at 15:55 HST the feed shrank from 65.9 MB to ~53 MB (a desk-side trim), and the cursor followed on the same inode (16:09 cursor offset = file size, 60,177,922) |
| Unchanged | `/health` flows 71 · `/api/state` 200 (the web server reads the feed itself, not the DB) · daily send code path unchanged |

## Verdict

**PASS.** Rollback: restore the backup file and `sudo systemctl restart network-globe-connection-history`. The daily send at HST midnight wasn't exercised; that code only gained an early return when `GLOBE_HISTORY_SEND=0`.
