# WORK ORDER — Inbox, drain, overnight relay, reply feedback

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-MIG-31-2026-09-29 |
| **Date** | 2026-09-30 (HST) |
| **Status** | BUILT — local inbox landed 2026-09-30. Cloudflare drain paused (D1 sync has no Folder). Not promoted to the active index. |
| **Owner** | RootRecord |
| **Related** | Agent 31, wave D. One send pipe, then the messages. No later function depends on this one. Cloudflare drain waits on agent 30 (D1 sync). Matrix row 63. Scheduler map rows `inbox-drain` and `overnight-relay`. |

**Scope:** Add an Inbox under Communications that reads the live quiet-mode relay hold. It records subscribe and unsubscribe from held Telegram texts, copies held rows into a local feedback file, writes a late-night status file, and can append a local reply-feedback line. It does not poll Telegram, Discord, or Slack, and it does not call Cloudflare. This draft does not authorize runtime edits, a job enablement, a relay restart, a send, a D1 delete, or a GitHub deletion.

---

## 1. Intent

Old `inbox` (`scripts/inbox.py`) polled Telegram, Discord, and Slack. In a private chat, `/subscribe` and `/unsubscribe` toggled public report DMs. Other text was answered by chat inference. Old `inbox-drain` (`scripts/job.py`, `scripts/offline_inbox.py`) ran every 5 minutes, selected Cloudflare D1 `ava_offline_inbox`, stored rows in a local feedback sqlite, deleted those edge rows, and deleted `ava_ecoflow` for host `ava-core`. Old `overnight-relay` (`scripts/job.py`) ran at 22:20 HST, read the first line of the newest `solar-weather-*.md`, and posted a late-night status to Discord `automations`. Old `reply-feedback` (`scripts/reply_feedback.py`, `scripts/feedback_store.py`) remembered outbound Telegram message ids and, on a positive reaction, appended gold JSONL. The skill trees say do not invent watts and do not dump balances, ads, or player counts.

The live system already holds unsent replies. With `RR_RELAY_REPLIES=0`, `Communications/telegram/scripts/council-relay.py` consumes each message and appends it to `2 - RootRecord-Database/Logs/Communications/Relay-Inbox/relay-inbox_current.jsonl`, cut hourly into `Archive/`. `relay-inbox-replay.py` lists that store. `--send` still needs `RR_RELAY_REPLIES=1`. `getUpdates` allows `message` only, and a second poller exits 409. That hold stays. This function reads it. It does not copy the old D1 loops over it.

---

## 2. Current reality

### 2.1 What exists

Folder name, used in all three places: `Inbox` (inside Communications). No lowercase twin. No second top-level domain. No `Logs/` directory on the server. Package name `Inbox`.

| Item | Location / status |
| --- | --- |
| Server code | `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/Inbox/scripts` — not created yet. |
| Database data | `2 - RootRecord-Database/Communications/Inbox/` — not created yet. Subscriber file, `feedback.jsonl`, drain ledger, `overnight-last.txt`, reply-feedback JSONL. |
| Database logs | `2 - RootRecord-Database/Logs/Communications/Inbox/` — not created yet. |
| Live hold (keep) | `Communications/telegram/scripts/council-relay.py` `inbox_hold` / `inbox_rotate`. Store `2 - RootRecord-Database/Logs/Communications/Relay-Inbox/`. Do not move it. Do not edit the relay in this build. |
| Replay (keep) | `Communications/telegram/scripts/relay-inbox-replay.py`. Listing is the default. `--send` stays refused unless `RR_RELAY_REPLIES=1`. |
| Discord and Slack pollers | `Communications/Discord/` and `Communications/Slack/` already exist, with gated jobs. They are other functions. Do not edit them. |
| D1 sync | No Folder. Cloudflare `SELECT` / `DELETE` and the `ava_ecoflow` clear stay paused. Name D1 sync. Do not build it. |
| `master-key.env` key names | None for this function. The local commands do not read tokens. Do not add an allowlist, a second env file, or a key. Do not print values. |
| Old source | Checkout `/home/rootrecord/old ollama/old skills`, remote `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server`, branch `online-safe-20260920`. Paths `inbox/`, `inbox-drain/`, `overnight-relay/`, `reply-feedback/`. `reply-feedback/store/` is gitignored (pattern `**/store/`). |

### 2.2 Completed so far

- [x] Old `inbox.py`, `offline_inbox.py`, `job.py` (drain and overnight), `reply_feedback.py`, and `feedback_store.py` read. Live `council-relay.py` hold and `relay-inbox-replay.py` read.
- [x] This draft written. Not on the active work-order index.
- [x] Alexander accepted this draft and said to build.
- [x] D1 sync has no Folder. The Cloudflare half stayed paused. D1 sync was not built.
- [x] `Inbox` code, Database READMEs, and Logs README created. Message-text files stay git-ignored.
- [x] `jobs.py` gated blocks added, both default off.
- [x] Temp-dir proof test passed (subscribe, drain, overnight fixture, replay `--send` exit 3).
- [x] Phase 4 archive and GitHub deletion done. Phase 5 result note written. Matrix row 63 and the scheduler map rows corrected.

### 2.3 Known friction

- D1 sync (agent 30) has no Folder. When told to build, pause that half and name D1 sync. Do not build it. Do not call Cloudflare.
- The local inbox does not need D1. Quiet mode already stores the unsent replies.
- `jobs.py`, the Vercel app shell, and `master-key.env` are shared. If any of them is already being edited at build time, pause and name the file.
- A second `getUpdates` loop hits 409. Subscribe handling reads held JSONL. It does not poll.
- Discord and Slack subscribe, and the Discord overnight post, are sends on other functions' pipes. This function writes files only.
- `allowed_updates` is `message` only. Reactions are not in the hold. This build does not widen that list and does not restart the relay.
- Old `reply-feedback/store/*.jsonl` is generated training data. Archive it with the old tree. Do not import it.
- Do not invent watts. If no local solar line is passed in, the overnight file says the solar line is absent.

---

## 3. Tasks

Do not start these until Alexander accepts this draft and says to build.

1. Pause the Cloudflare half. D1 sync has no Folder. Name D1 sync. Do not build it. Do not `SELECT` or `DELETE` `ava_offline_inbox`. Do not clear `ava_ecoflow`.
2. Pause if `jobs.py`, the Vercel app shell, or `master-key.env` is already being edited.
3. Add `Communications/Inbox/scripts/inbox.py`. It reads a Relay-Inbox directory (default the live hold path; tests pass `--inbox`). It does not import `council-relay.py` in a way that calls `main` or `api`. It does not send.
4. `subscribe`: from held records whose `chat_type` is `private`, parse `/subscribe`, `/unsubscribe`, `/start`, and `/help` (same first-token rules as the old inbox). Write `2 - RootRecord-Database/Communications/Inbox/subscribers.json`. No confirmation message.
5. `drain`: copy held records that are not already in the local ledger into `2 - RootRecord-Database/Communications/Inbox/feedback.jsonl`. Append the ledger beside it. Leave the Relay-Inbox files in place. No HTTP.
6. `overnight`: write `2 - RootRecord-Database/Communications/Inbox/overnight-last.txt` with the HST time and, only when `--solar-line` is given, that line. No Discord post. No invented watts.
7. `feedback`: append one JSON object to `2 - RootRecord-Database/Communications/Inbox/reply-feedback.jsonl` when `--note` is given. Do not read or copy old `store/*.jsonl`.
8. Append one run line under `2 - RootRecord-Database/Logs/Communications/Inbox/`. Mode 0600 on files that contain message text.
9. If `jobs.py` is free, add two gated blocks, both default off: `inbox_drain` (`RR_INBOX_DRAIN`, 300s, `inbox.py drain`) and `overnight_relay` (`RR_OVERNIGHT_RELAY`, 22:20 HST, `inbox.py overnight`). Do not turn the gates on. Do not change the night-sleep gate. Do not edit the Discord or Slack job blocks.
10. Add `Communications/Inbox/README.md` naming the Folder and the three paths.
11. Run the proof test in Notes. Do not set `RR_RELAY_REPLIES`, `RR_INBOX_DRAIN`, or `RR_OVERNIGHT_RELAY`. Do not restart the relay. Do not read the live Relay-Inbox during the test.
12. After that test passes: copy `inbox/`, `inbox-drain/`, `overnight-relay/`, and `reply-feedback/` (including gitignored `store/` and any `__pycache__` beside that source) into `/home/rootrecord/RootRecord-Ecosystem/Old repos deleted and merged/Solar-Pacific-RootRecord-Server/`, keeping those paths. Generated store files go to that archive and do not go into Pacific, Database, the website, or git. If the archive copy fails, do not delete. After the copy is on disk, delete those same paths from the old checkout on this machine, and delete the tracked files on GitHub branch `online-safe-20260920`. Commit that deletion and push it. Do not force-push. Do not delete the GitHub repository. `store/` was never tracked; delete it only on this machine after the archive copy.
13. Then add the phase 5 result note to this work order. Correct only Library matrix row 63 and the scheduler map rows for `inbox-drain` and `overnight-relay`.

---

## 4. Non-goals

- Do not build D1 sync, the economy brief, MySQL desk facts, Discord, or Slack.
- Do not replace `council-relay.py`, `relay-inbox-replay.py`, `ensure-relay.sh`, EcoFlow BLE, the poller, Hawaiʻi weather, the globe collector, camera grabs, Kokoro, or `geology_collect.py`.
- Do not widen `allowed_updates` or restart the relay.
- Do not set `RR_RELAY_REPLIES=1`, `RR_INBOX_DRAIN=1`, or `RR_OVERNIGHT_RELAY=1`.
- Do not edit `master-key.env` or add a second env file.
- Do not open a second top-level domain. Do not add a `Logs/` directory on the server. Do not add a lowercase `inbox` folder.
- Do not import logs, samples, gold JSONL, sqlite, caches, or other generated runtime output into Pacific, Database source, the website, or git. The new subscriber file, feedback file, ledger, overnight file, and reply-feedback file stay under Database.
- Do not send Telegram, Discord, or Slack. Do not play speakers, switch hardware, or spend cloud money from this draft.
- Do not delete the GitHub repository. Do not restore files under `~/.ollama/skills/`.

---

## 5. Key file / path reference

| Path | Role |
|------|------|
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/Inbox/scripts/inbox.py` | New CLI. Read held JSONL. Write local files. No network. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/Inbox/README.md` | Folder name and the three paths. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Automations/scripts/jobs.py` | Two proposed gated blocks only, if the file is not already being edited. Default off. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/telegram/scripts/council-relay.py` | Keep. Quiet hold. Do not edit. |
| `1 - Servers/1 - RootRecord-Pacific-Solar-Server/Communications/telegram/scripts/relay-inbox-replay.py` | Keep. `--send` still refused without `RR_RELAY_REPLIES=1`. |
| `2 - RootRecord-Database/Logs/Communications/Relay-Inbox/` | Existing hold. Read in production. Not the test input. |
| `2 - RootRecord-Database/Communications/Inbox/` | `subscribers.json`, `feedback.jsonl`, drain ledger, `overnight-last.txt`, `reply-feedback.jsonl`. |
| `2 - RootRecord-Database/Logs/Communications/Inbox/` | One run line per command. |
| `/home/rootrecord/master/master-key.env` | Not read. Not edited. |
| `inbox/`, `inbox-drain/`, `overnight-relay/`, `reply-feedback/` on `Solar-Pacific-RootRecord-Server` `online-safe-20260920` | Old source. Archive, then delete those paths only. |
| `reply-feedback/store/` | Gitignored generated data. Archive, then delete on this machine only. |
| `5 - RootRecord-Library/Documentation/00-architecture/Old-Repo-Migration-Matrix.md` | Phase 5 only: correct row 63. |
| `5 - RootRecord-Library/Documentation/00-architecture/G1-Scheduler-To-G3-Jobs-Map-2026-09-29.md` | Phase 5 only: correct `inbox-drain` and `overnight-relay`. |

---

## 6. Open items

**Additional requirements:**

- Alexander accepts this draft and says to build before any file outside this draft is written.
- At build time, the Cloudflare half stays paused until D1 sync has a Folder. Name that function. Do not build it.
- At build time, pause if `jobs.py`, the Vercel app shell, or `master-key.env` is already being edited.
- Sends, relay restarts, D1 deletes, and turning `RR_INBOX_DRAIN` or `RR_OVERNIGHT_RELAY` on need a separate sign-off. This draft does not give it.
- Phase 4 deletes only the four old paths after the archive copy is on disk.
- Phase 5 result note is empty until the build, the archive, and the GitHub deletion exist.

---

## 7. Notes & constraints

- No force-push.
- Secrets stay out of git. This function has no `master-key.env` key names.
- Prefer small reversible steps.
- Sign-off gate: do not set `RR_RELAY_REPLIES=1`. Do not pass `--send` to the replay script against the live inbox. Do not post to Discord, Slack, or Telegram. Do not call Cloudflare. Do not restart the relay, play speakers, switch hardware, or spend cloud money.
- Proof test, temp directory only: write one synthetic held JSONL line (`chat_type` `private`, text `/subscribe`). Run `inbox.py subscribe`, `inbox.py drain`, and `inbox.py overnight --solar-line "fixture"` against that directory and a temp Database root. Expect a subscriber entry, one feedback line, and `overnight-last.txt` containing the fixture line. Then run `relay-inbox-replay.py --inbox` that temp directory `--send` with `RR_RELAY_REPLIES` unset and expect exit 3. No network. Do not point either command at the live Relay-Inbox.
- Phase 4 archive root: `/home/rootrecord/RootRecord-Ecosystem/Old repos deleted and merged/Solar-Pacific-RootRecord-Server/`. If the archive copy fails, do not delete.
- After phase 4, add a short result note here (what landed, archive path, GitHub deletion commit) and correct only matrix row 63 and the scheduler map rows for `inbox-drain` and `overnight-relay`.

---

*Work order prepared 2026-09-30 HST. Update status when closed.*

---

## Archive / location note

This file is a draft. It is not on the active index. Do not auto-promote.

```text
Documentation/06-development/Work-Orders/drafts/Inbox_drain_overnight_relay_reply_feedback_Work_Order_WO-MIG-31-2026-09-29.md
```

See `drafts/README.md` and WO-WOGEN-001. Promotion is Alexander's decision: move into `Documentation/06-development/Work-Orders/`, set Status, and add an index row.

**Closed WOs:** set Status → COMPLETE/CLOSED → `git mv` into `Documentation/06-development/Work-Orders/Complete/`.

Human session logs archive under `Documentation/01-operations/archive/YYYY-Www/` (WO-ARCH) — separate from closed work orders.

### Phase 4 / phase 5 result

Landed 2026-09-30: `Communications/Inbox/scripts/inbox.py` reads the quiet-mode hold and writes local files only. Jobs `inbox_drain` (`RR_INBOX_DRAIN`, 300s) and `overnight_relay` (`RR_OVERNIGHT_RELAY`, 22:20 HST) are in `jobs.py` and default off. Proof on `/tmp/rr-inbox-mig31.*`: one subscriber, one feedback line, overnight file contained `fixture`, `relay-inbox-replay.py --send` exited 3 with `RR_RELAY_REPLIES` unset. Temp dir removed. Live Relay-Inbox was not read. No send, no relay restart, no Cloudflare call.

Cloudflare `SELECT` / `DELETE` and the `ava_ecoflow` clear did not run. **D1 sync** has no Folder. That function was not built.

Archive: `/home/rootrecord/RootRecord-Ecosystem/Old repos deleted and merged/Solar-Pacific-RootRecord-Server/` paths `inbox/`, `inbox-drain/`, `overnight-relay/`, `reply-feedback/` (31 files, copy matched before delete). GitHub `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server` branch `online-safe-20260920` commit `7763b4e8` deleted the 22 tracked files. `reply-feedback/store/` was gitignored; it was archived and removed on this machine only. No shared file inside those four trees was left behind. `apps.core` was not part of these trees and was not deleted. The GitHub repository was not deleted. No force-push.
