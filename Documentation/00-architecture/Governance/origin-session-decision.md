# Origin session decision

Source: G1 `origin-session/` (`SKILL.md`, `references/migrate.md`, `scripts/origin_session.py`). The script was not installed.

Evidence label: **Historical**.

## What it did

`origin_session.py` wrote `origin-session.json` under the old origin state directory. The payload was an id (`pid` plus a UTC timestamp), the process id, and `started_at`. Council used that id to catch up when the desk started. If the file was missing or unreadable, the id was an empty string.

The skill description is "Origin operator session helper." Topic index: `boot-idle-origin`.

## Do not restore

`references/migrate.md` status is **moved**, from services. It says do not restore the old body. No Pacific module writes this file. No Database or Logs folder was created for it.

## `origin/` was not imported

`origin-session` is this helper only. The `origin/` app (about 4342 paths in the G1 catalog) is a different tree. It was not bulk-imported into Pacific, Database, the website, or the Library. Matrix row 77 still owns that app. This work order does not mine it.
