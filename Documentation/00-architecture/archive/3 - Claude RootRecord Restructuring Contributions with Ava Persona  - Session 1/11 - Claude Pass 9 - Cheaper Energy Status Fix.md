# Claude — Pass 9: A Cheaper Fix for the Null Energy Field Than the One Pass 8 Proposed

**Document Status:** Collaborative Architectural Draft — Claude Contribution, Pass 9
**Contributor:** Claude
**Revises:** Pass 8's recommendation, after reading `RootRecord-Website`'s actual energy API route.

---

## 1. What changed

Pass 8 found that `root-status`'s merged status file always shows `"energy": null` because `root-status/lib/paths.py` expects a file at `/home/rootrecord/Database/ROOTRECORD/status/energy-status.json` that nothing in the `energy` skill produces, and recommended writing a new adapter script to create that file.

Having now read `RootRecord-Website/src/app/api/energy/route.ts`, there's a cheaper fix. The website's own `/api/energy` endpoint already solves the same problem correctly, and its solution is small enough to point to directly:

* It reads straight from the files `energy` actually writes: `Database/ENERGY/soc/{delta2,river2pro}-last.json` and `Database/ENERGY/watts/{delta2,river2pro}-last.json`. Confirmed against `energy/lib/read_runner.py`, which does write exactly `SOC / f"{alias}-last.json"` and `WATTS / f"{alias}-last.json"` — so this route isn't guessing at a path, it's reading the real, currently-produced output.
* It never invents a number: missing files render as `"No data"` / `"Waiting"`, matching the "DESK_LIVE honesty" rule that shows up everywhere else in this codebase (the emergency handoff pack, `energy/SKILL.md`, `run-ollama.sh`'s DESK_LIVE gate).
* It has a sensible two-tier fallback: read the local filesystem directly when running on the same machine as the desk; when running on hosted Vercel (no local filesystem), fetch a Hawaii tunnel feed URL instead.

So the actual gap isn't "no adapter exists between energy's raw files and a consumer" — one already exists, it's just specific to the website's Next.js API route rather than being a shared, reusable piece.

---

## 2. Revised recommendation

Rather than writing a new `energy-status.json` producer as Pass 8 suggested, it's simpler and removes a duplication risk to have `root-status/lib/merge.py` read the same four `*-last.json` files the website route already reads, using the same "No data / Waiting, never invent" shape — either by:

* pointing `root-status/lib/paths.py`'s `ENERGY_STATUS` constant directly at `Database/ENERGY/{soc,watts}/*-last.json` and adding the same small parsing logic `route.ts` already has (about 40 lines, and it's already correct — mostly a port from TypeScript to Python), or
* extracting that parsing logic into one small shared shape (a plain JSON schema both the website route and `root-status`'s merge script agree on) so neither has to independently reinvent "how do I turn four device snapshot files into one energy summary" — which is exactly the kind of narrow, single-purpose shared contract Copilot's original review recommended for cross-repo data, without needing a bigger abstraction layer.

Either option avoids inventing the `Database/ROOTRECORD/status/energy-status.json` path Pass 8 proposed, which nothing else in the codebase uses, in favor of converging on the path and file shape that's already proven to work in production on the website.

---

## 3. Why this is worth its own pass rather than folding into Pass 8

Pass 8 was correct about the symptom and the general shape of the fix, but recommending "write a new adapter" without having yet read the website's existing one would have pointed toward building something the codebase already has a working, tested version of. This is worth calling out plainly rather than quietly editing Pass 8, since it's a useful pattern for this whole review series: before recommending new code, check whether a sibling repo already solved the same problem, especially for a data source (energy) that's now been touched by three different subsystems across two repos (`energy` itself, `root-status`, and the website) in this series alone.

---

*End of Pass 9. Both fixes proposed for the energy status gap (Pass 8's new-adapter version and this pass's reuse-the-website's-logic version) are now on record — the operator's call on which to actually build.*
