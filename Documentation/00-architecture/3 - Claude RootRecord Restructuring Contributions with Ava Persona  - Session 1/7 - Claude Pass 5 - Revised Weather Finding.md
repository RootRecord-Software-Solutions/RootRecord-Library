# Claude — Pass 5: Revising Pass 1's Weather Finding After Actually Diffing the Code

**Document Status:** Collaborative Architectural Draft — Claude Contribution, Pass 5
**Contributor:** Claude
**Revises:** Pass 1, Section 2 ("Confirmed finding: the weather duplication is not hypothetical")

---

## 1. Why this revision exists

Pass 1 flagged that `Solar-Pacific-RootRecord-Server/weather/` and `US-Mainland-Server/weather/` are structurally near-identical trees and called that "two live implementations of the same collector logic," recommending a canonicalization decision. That was based on directory-listing comparison alone. This pass actually diffs the shared files between the two trees. The conclusion needs correction: they are not two copies of the same code. They're meaningfully different in a way that could be an intentional split, an incomplete migration, or a live bug — and the file evidence doesn't cleanly settle which. Section 4's instruction to "distinguish confirmed facts from proposals" and "identify uncertainty clearly" applies directly here, so this pass documents the uncertainty rather than resolving it by assumption.

---

## 2. What the diff actually shows

`weather/core/path_resolver.py` differs in a way that isn't cosmetic:

* Solar-Pacific's version implements a full URL-to-path resolver with both a `current_path()` (latest snapshot) and an `archive_path()` (dated, timestamped historical copy), with a docstring explicitly citing an `nws_plan.md` specification for both.
* US-Mainland's version has a one-line docstring stating plainly: *"URL -> deterministic `*_current` path. No archive/history path exists here."* It implements only `current_path()` — there is no `archive_path()` method at all.

Consistent with that, Solar-Pacific's `weather/core/` contains `archiver.py` and `daily_zip.py`; neither file exists anywhere in Mainland's `weather/core/`.

That much would support a clean reading: **Solar-Pacific is the archival/canonical-history node; Mainland is a deliberately lean current-conditions-only execution node**, which would actually line up well with Section 24 of the baseline document (Mainland as an "automation/offloading" layer, not a replacement for canonical ownership).

The problem is that the rest of Mainland's own tree doesn't consistently agree with that reading:

* `weather/core/hst_time.py` (present on both sides, and functionally similar) still defines `hst_archive_timestamp()` and a comment stating it is *"Used by scheduler/run_cycle.py to fire archive/consolidate.py exactly once."*
* `weather/core/validators.py` contains a comment referring to *"core/archiver.py writes anything"* as something the validators are meant to account for.
* `weather/fetch/_engine.py`'s own docstring describes its pipeline as *"clean -> validate -> archive -> manifest-update,"* with an inline comment about building *"the exact byte stream that will be archived."*

None of `archiver.py`, `daily_zip.py`, or an `archive/consolidate.py` actually exist in Mainland's tree. So Mainland's `path_resolver.py` has apparently had its archive capability deliberately removed, while three other files in the same tree (`hst_time.py`, `validators.py`, `fetch/_engine.py`) still read as if an archive step exists downstream and will run. If the archive step is genuinely gone, those are just stale comments and harmless. If anything in Mainland's scheduler actually calls toward an archive step that no longer exists, that's a silent no-op or a runtime error waiting to surface — not a design decision, a partially-finished edit.

The rest of the diff (`manifest.py` at 30 lines on Mainland vs. 131 on Solar-Pacific; `run_poller.py` at 7 lines vs. 39; a noticeably terser one-line `config/README.md` on Mainland vs. Solar-Pacific's fuller "Owns / Does NOT own / Depends on" convention) is consistent with either reading too: it could be a leaner node by design, or an earlier snapshot of Solar-Pacific's code that was forked before the fuller version was written and never resynced.

---

## 3. What this changes about Pass 1's recommendation

Pass 1 asked: *"which of these two trees is authoritative, is the other one stale, a fork, or a live duplicate collector."* The honest answer after this pass is: **it looks like an intentional current-vs-archival split that wasn't finished being carried through the whole tree** — which is a narrower, more specific problem than "duplicate collector," and a different fix:

* This is not a "pick a winner and delete the other" situation. Mainland's leaner shape may be exactly right for its role.
* It is a "finish or reverse one specific decision" situation: either finish removing the archive references from `hst_time.py`, `validators.py`, and `_engine.py` on the Mainland side to match `path_resolver.py`'s stance, or confirm the archive step is still meant to run on Mainland and restore `archiver.py`/`daily_zip.py` there. Right now the tree can't consistently tell you which.

---

## 4. Recommendation

* Before touching any code: run Mainland's actual scheduler once with logging on and confirm empirically whether an archive step fires, errors, or silently no-ops. This is a five-minute check that resolves the ambiguity this pass couldn't resolve from static reading alone, and matches the master-prompt's own **Confirmed / Hypothesis / Unknown** discipline — this is currently a documented **Unknown**, not a confirmed bug.
* Once confirmed, update whichever side is behind: either strip the remaining archive references from Mainland's `hst_time.py`/`validators.py`/`_engine.py` docstrings and comments, or port `archiver.py`/`daily_zip.py` over. Either way, make Mainland's `config/README.md` state its own current/archive scope as explicitly as Solar-Pacific's does, so the next reader doesn't have to re-derive this from a diff the way this pass did.
* This is a good candidate for the ADR Pass 3 suggested reserving for genuinely contested calls — "should Mainland's weather node retain archival capability" is exactly that kind of decision, and recording the answer once avoids a third pass rediscovering the same ambiguity.

---

*End of Pass 5. This also stands as a general caution for the remaining open items from Passes 1–4: directory-listing-level comparisons are a good first signal but not sufficient on their own before recommending a fix — worth diffing actual file contents before finalizing any of the remaining canonicalization calls.*
