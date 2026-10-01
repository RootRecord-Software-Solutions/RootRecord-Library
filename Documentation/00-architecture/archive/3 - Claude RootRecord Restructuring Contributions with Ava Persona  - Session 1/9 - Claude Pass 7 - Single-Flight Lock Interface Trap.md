# Claude — Pass 7: The Single-Flight Lock Works — But Two of Its Four Subcommands Don't Do What Their Names Promise

**Document Status:** Collaborative Architectural Draft — Claude Contribution, Pass 7
**Contributor:** Claude
**New territory:** `Solar-Pacific-RootRecord-Server/plumbing/` (the inference single-flight lock both Grok and Copilot cited approvingly as an already-solved idempotency example) and `a-eyes/` (camera/timelapse subsystem, not previously reviewed).

---

## 1. Why this is worth a closer look

Grok's review specifically pointed to the single-flight inference lock as evidence that "the same discipline should extend to data-plane jobs" — i.e., held it up as a model to imitate elsewhere. That assessment was made from the master-prompt's description of the lock, not from reading `plumbing/scripts/single-flight.sh` itself. Having read the actual script, the underlying mechanism is genuinely solid — but two of the four subcommands it exposes don't provide the guarantee their names imply, and nothing currently calls them, which is the only reason this hasn't surfaced as a live bug yet.

---

## 2. What the script actually does

`single-flight.sh` exposes four subcommands: `acquire`, `release`, `status`, `run`.

The real mutual-exclusion mechanism is a `flock` held on a file descriptor (`exec 9>"$LOCK"; flock -n 9`). `flock`'s guarantee is scoped to that file descriptor's lifetime — the lock is held only as long as the process that opened it stays alive, and releases automatically the instant that process exits, regardless of what the script's own code does afterward.

* **`run <job-id> -- <cmd>`** is safe: it opens the fd, takes the lock, executes `<cmd>` while still inside the same process, and only then exits — so the lock is held for exactly as long as the wrapped command runs. Both actual callers in this repo, `run-infer.sh` and `run-ollama.sh`, exclusively use this subcommand.
* **`acquire <job-id>`** takes the lock, writes a holder marker file, prints `"[ok] acquired"`, and returns. But the script process then exits at the end of that shell invocation — and the moment it does, the `flock` on fd 9 is released automatically by the kernel, whether or not anyone has called `release` yet. The holder marker file survives, but the actual OS-level exclusion does not.
* **`release <job-id>`** only deletes that marker file. It has nothing left to release by the time it runs, in any workflow where `acquire` and `release` are invoked as two separate script executions (which is the only way they can be used, since they're separate subcommands).

So `acquire`/`release`, used as a pair the way their names invite — "acquire before starting some external work, release when it's done" — would provide no actual protection against a second process starting the same class of job during that window. Only the informational marker file would exist; nothing would stop a second `acquire` from succeeding immediately, because there'd be nothing left holding the lock to block it.

---

## 3. Why this hasn't been a problem yet

Checked against the rest of the repo: `acquire` and `release` are documented in the script's own usage banner but are not invoked anywhere else in the codebase. The only other reference to the script is `plumbing/INSTALL.sh`, which runs `single-flight.sh status` once as an install-time smoke test. Every real caller uses `run`, which is the safe form. This is a latent interface trap, not a live incident — but it's exactly the kind of thing that gets discovered the hard way once a future agent or contributor reads the usage banner, reasonably assumes `acquire`/`release` behave like a held mutex (the way `threading.Lock.acquire()/release()` does in a language most agents are trained on), and wires a new integration around that assumption.

---

## 4. Recommendation

Pick one of two fixes, both small:

* **Remove `acquire`/`release` from the public interface** and keep only `run` and `status`, since `run` is the only form that's actually safe and it's also the only form anything currently uses. This is the simpler fix and matches Section 4's "prefer simplification where functionality can remain equivalent."
* **Or, if standalone acquire/hold/release is genuinely needed for some future workflow** (e.g. a long-running job that can't easily be wrapped as a single `run` invocation), make `acquire` daemonize and hold the fd open in a background process, with `release` signaling that process to exit and drop the lock. That's a real fix, not just a rename — it's more work than removing the two subcommands, so worth doing only if there's an actual upcoming use case for it.

Either way, this is a five-line fix to a file that's already otherwise well-built, and worth closing before something gets written against the documented-but-unsafe interface rather than the safe one.

---

## 5. Smaller note: `a-eyes/` is a third undocumented subsystem

While in the same part of the tree: `a-eyes/` (camera capture, timelapse generation, a small cam-server, and a `CAMERAS.md` reference doc) is a working subsystem with no mention anywhere in the baseline document, Copilot's review, or Grok's review — the same category of gap Pass 6 raised for the Mainland radio/broadcast services. Flagging it here rather than opening a new pass for it: it should get folded into the same "what existing subsystems aren't yet named in the architecture conversation" question raised in Pass 6, rather than treated as a separate issue.

---

*End of Pass 7. Still unopened from the original archive set: `RootRecord-Website`'s actual page implementations, and the `system-stats/` and `github/` directories in Solar-Pacific.*
