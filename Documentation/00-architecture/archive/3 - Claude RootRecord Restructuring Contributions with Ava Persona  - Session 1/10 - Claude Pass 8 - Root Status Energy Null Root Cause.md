# Claude — Pass 8: Found the Exact Reason `root-status`'s Energy Field Is Always Null

**Document Status:** Collaborative Architectural Draft — Claude Contribution, Pass 8
**Contributor:** Claude
**Connects to:** Pass 3, which noted from `0-master-prompt/state/state.json`'s own `next_action` field that the five-minute updater still needed to be "connected to the real connection, power, and worklog collectors." This pass independently confirms that gap from a completely different code path, and pins down exactly where it breaks.

---

## 1. The finding

`root-status/` is described in its own `SKILL.md` as the *"central transmission skill"* — it reads clean status JSON from `energy` and `system-stats`, merges them into one file, and that merged file is what feeds the website, AWS, and GitHub push. The live merged output currently on disk (`root-status/status/root-status-5min.json`) has a fully populated `system` block — real CPU, load, and memory figures, both instantaneous and five-minute-averaged — and an `energy` field that is simply `null`.

`root-status/lib/paths.py` shows exactly why: it expects to read energy status from

```text
/home/rootrecord/Database/ROOTRECORD/status/energy-status.json
```

marked in the source with a `# future` comment. But the `energy` skill itself — checked directly in `energy/lib/paths.py` and `energy/config/devices.conf` — writes measured samples only under

```text
/home/rootrecord/Database/ENERGY/{samples,ports,soc,watts}
```

and its SQLite database separately at `/home/rootrecord/Database/ROOTRECORD/rootrecord.db`. Nothing in the `energy` skill produces a file at the path `root-status` is waiting on. These aren't two systems that merely haven't been started yet — they're two systems that don't currently agree on which directory tree the handoff between them happens in.

---

## 2. Why this is worth pinning down precisely rather than leaving as a general "not wired up yet"

Pass 3 flagged this gap already, but only indirectly — as a to-do note the master-prompt's own state file had written about itself. That's a real signal, but it doesn't tell you what to actually go build. This pass closes that gap: the missing piece isn't a network connection or a scheduler — it's one small adapter step that doesn't exist yet: something that reads `energy`'s raw measured files (or its SQLite rows) and writes a clean `energy-status.json` in the shape `root-status` already knows how to merge. `root-status/lib/merge.py`'s `_load()` function already handles a missing file gracefully (it returns `{}` and the merge just carries `null` through) — so nothing is actually broken or erroring; it's a genuinely absent step, silently tolerated by design.

---

## 3. Recommendation

* Add a small `energy-status` writer (naturally, a natural sibling to `energy/db/store.py`, following the same `SKILL.md`-documented "one script per concern" pattern Pass 4 noted as this subsystem's own good convention) that reads the latest measured samples and/or queries `rootrecord.db`, and writes the clean status JSON to the exact path `root-status/lib/paths.py` already expects: `/home/rootrecord/Database/ROOTRECORD/status/energy-status.json`.
* Once that exists, drop the `# future` comment in `root-status/lib/paths.py` — comments marking something as "not yet real" are easy to forget to remove once it becomes real, and Pass 2 already surfaced one example of a stale "future" note (`agents/ava-ivy/references/GITHUB-IDENTITY.md`) outliving the condition it described.
* This is a good, small, low-risk first candidate for closing one of the two `"unknown"` fields Pass 3 flagged in `0-master-prompt/state/state.json` (`connections.rootrecord_server`, `connections.mainland_server`, and by extension the `power` block) — it's fully scoped, doesn't touch anything else, and has an obvious, verifiable success condition: `root-status-5min.json`'s `energy` field stops being `null`.

---

*End of Pass 8. This closes out the "why is a field null" thread opened indirectly in Pass 3. Remaining unopened territory: `RootRecord-Website`'s actual page implementations, and `github/scripts/` beyond the one file sampled here.*
