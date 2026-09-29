# Claude — Pass 4: A One-Character-Class .gitignore Gap Is Already Leaking Backup Files Into the Repo

**Document Status:** Collaborative Architectural Draft — Claude Contribution, Pass 4
**Contributor:** Claude
**Builds on:** Pass 1 (weather/comms duplication), Pass 3 (`0-master-prompt` governance layer already mature)

---

## 1. The finding

`Solar-Pacific-RootRecord-Server/.gitignore` already shows clear intent to keep dated backup artifacts out of the tracked tree:

```text
# dated change backups — live under /home/rootrecord/Database/GITHUB
automations.bak-*/
*.bak-*/
```

There's also a documented operational rule (surfaced in Pass 1's review of the emergency handoff pack) that backups are a deliberate safety step, not clutter: the change gate is **bak → Carly seal → Bruce veto** before working code lands. So the intent here is sound on both sides — take a backup before a risky edit, but don't let that backup live in the canonical tree permanently.

The pattern actually used doesn't do what it's meant to do. `*.bak-*/` (note the trailing slash) only matches **directories** whose name ends in `.bak-<something>`. The files this repo actually produces during the gate step are individual files with no trailing directory component:

```text
energy/lib/envload.py.bak-20260924-183017
energy/lib/ecoflow_api.py.bak-20260924-181154
energy/lib/read_runner.py.bak-20260924-180812
energy/lib/config.py.bak-20260924-183017
energy/config/devices.conf.bak-20260924-180812
energy/db/condense.py.bak-20260924-152919
energy/db/store.py.bak-20260924-152919
energy/db/schema.sql.bak-20260924-152919
energy/db/test_aggregate.py.bak-20260924-153517
energy/scripts/aggregate.py.bak-20260924-153517
energy/scripts/condense_closed_periods.py.bak-20260924-153517
energy/scripts/verify_rootrecord_db.py.bak-20260924-152919
weather/config/*.bak-*
weather/fetch/*.bak-*
system-stats/lib/*.bak-*
automations/scripts/*.bak-*
coms/ssh/context/*.bak-*
coms/ssh/local-data-globe/*.bak-*
```

28 such files across 8 directories, all committed, none matched by the existing rule. The `.gitignore` file itself even has a nearby comment acknowledging this exact class of problem happened once already — *"stray git-internal backups (accidental commit 2026-09-24, see cleanup commit)"* — so this isn't a one-off; it's a recurring pattern the ignore rules have been chasing without quite closing.

---

## 2. Why this is worth a dedicated note rather than folding into a general "clean up the repo" item

This is small, mechanical, and fully verifiable from the file evidence alone — exactly the kind of finding that's cheap to fix and easy to verify closed, unlike the weather/comms canonicalization questions from Pass 1, which need a human decision about system-of-record. It's also a good illustration of a pattern worth watching for elsewhere in this migration: **the written rule and the actual glob often disagree by one small technical detail**, and the only way to catch that is to check the rule against real committed files, not just read the rule and nod at the intent. The same read-the-actual-state discipline Section 29 of the baseline document asks for applied here.

---

## 3. Recommendation

* Fix the pattern to also match files, not only directories: add `*.bak-*` (no trailing slash) alongside the existing `*.bak-*/`, so both the directory and file forms are ignored going forward.
* Remove the 28 already-committed backup files from the tracked tree in one cleanup commit, after confirming none of them are the only copy of something (Section 29's "written ≠ deployed" discipline applies here too — check before deleting, don't assume).
* Since the `.gitignore` comment says these backups are meant to live under `/home/rootrecord/Database/GITHUB` instead, confirm whether the bak-step tooling is actually writing them there and only accidentally also leaving a copy in the working tree, or whether it's writing directly into the working tree and relying on `.gitignore` alone. If it's the latter, the fixed ignore pattern solves it going forward; if it's the former, there's a small script bug to find as well.

---

## 4. A separate, positive note: `energy/` is a clean example worth pointing to

While reviewing the backup-file pattern, the `energy/` subsystem itself (EcoFlow power control — 190 files, the largest single directory in Solar-Pacific) turned out to be one of the better-organized parts of the repo, and worth citing as a positive reference pattern for other subsystems rather than only surfacing problems:

* One executable script per action (`scripts/actions/delta2-usb-on.sh`, etc.), with shared logic factored into `lib/`, and its own `SKILL.md` documenting exactly how to add a new action or device without needing an AI session to do it.
* An explicit honesty rule baked into the skill itself — never invent a wattage or state-of-charge reading, report `WAITING`/`No data` and exit non-zero instead — which is the same "empirical only" discipline from the emergency handoff pack (Pass 1), independently re-stated at the subsystem level.
* A single declared BLE owner (`ava-ecoflow-ble.service`) with an explicit "do not dual-start pollers" rule — i.e., the idempotency/locking concern Grok raised abstractly for distributed jobs has already been solved concretely here, at least for this one subsystem.
* Scheduled polling buckets (`scripts/poll/{1m,5m,15m,30m,hour,daily}/`) exist as empty stubs, deliberately left disabled until the underlying atomic actions are proven — a concrete, current example of the cautious rollout discipline the baseline document asks for in the abstract.

This is worth naming because the final synthesis shouldn't read as purely corrective — `energy/` is a working template for what "operations vs. skills, done right, with idempotency handled" looks like in this codebase, and the weather/comms cleanup from Pass 1 could reasonably use it as the pattern to converge toward rather than designing a new one.

---

*End of Pass 4. Remaining open threads from earlier passes: the weather/comms canonicalization decision (Pass 1) and the agent-identity migration cutover (Pass 2) are still the two items that need a human decision rather than further code reading — happy to draft the concrete migration checklist for either on request.*
