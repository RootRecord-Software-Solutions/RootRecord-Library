# Claude — Pass 6: A Recovery Baseline That's Right in Substance, Ambiguous in Naming — Plus an Undocumented Subsystem

**Document Status:** Collaborative Architectural Draft — Claude Contribution, Pass 6
**Contributor:** Claude
**New territory:** `US-Mainland-Server/mirror/` and `US-Mainland-Server/RECOVERY.md`, not previously reviewed in Passes 1–5.

---

## 1. The nested `network-globe/network-globe/` isn't a duplication bug — but it's built to look like one

At first glance, `mirror/network-globe/` looks like an accidental double-extraction:

```text
mirror/network-globe/
├── index.html, server.js, package.json, README.md, ARCHITECTURE.md, EXTENDING.md, HAWAII-MERGE.md, scripts/
└── network-globe/
    ├── index.html, server.js, package.json, README.md, ARCHITECTURE.md, EXTENDING.md
    └── data/.gitkeep
```

`RECOVERY.md` clears this up immediately once read: the nesting is deliberate. It states plainly that the **canonical application path is `mirror/network-globe/network-globe/`**, and that this is intentional because it's meant to mirror the actual runtime path on the recovery target machine, `/home/ubuntu/network-globe/network-globe/`. The repo's directory structure is built to be droppable straight onto the recovery host without path translation — a genuinely sound recovery-repo pattern, and a good concrete instance of the "recoverable, inspectable" requirement from Section 36 of the baseline document.

The problem is narrower than the structure itself: the outer copy isn't just an empty wrapper — it has its own `HAWAII-MERGE.md`, its own `scripts/patch-green-arcs.js`, and an `index.html`/`server.js` that both differ in content from the inner, canonical copy. Nothing in the directory naming signals "this outer level is not the one to edit." A future contributor (human or AI) skimming the tree with `RECOVERY.md` unread has no structural cue to avoid editing the outer copy and assuming it's live.

**Recommendation:** rename the outer directory to something that can't be mistaken for the canonical target — e.g. `mirror/network-globe-reference/` or `mirror/_outer/` — and reserve the exact name `network-globe` for the one nested path that actually matches the runtime target. This preserves the good recovery pattern while removing the naming coincidence that currently makes it look like a mistake.

---

## 2. `mirror/rootrecord/systemd/` describes a subsystem the architecture document doesn't mention at all

Sitting inside the same `mirror/` directory is a set of systemd unit files with no corresponding section anywhere in the baseline document, Copilot's review, or Grok's review:

```text
rr-weather.service       rr-radio.service        rr-chat.service
rr-packer.service        rr-noaa.service         rr-earthquake.service
rr-audio-recv.service    rr-radar.service         rr-icecast.service
rr-dropins.service       rr-hurricane.service     rr-cloudflared.service
rr-youtube.service
```

Weather, radar, hurricane, earthquake, and Cloudflare tunnel units line up with what the baseline document already discusses. `rr-radio`, `rr-audio-recv`, `rr-icecast`, `rr-youtube`, and `rr-chat` don't correspond to anything in Section 37's architectural model or the repository list in Section 38 — this looks like a live audio/broadcast capability (Icecast streaming, YouTube integration, an audio receiver service) that exists in deployment but has never been named in the restructuring conversation at all.

This matters for the same reason Section 22 already flags for the rest of the global layer: *"existing global code, automation, databases, configurations, or pages must not automatically be treated as authoritative simply because they exist."* Right now this subsystem is neither claimed as canonical nor flagged as historical accumulation to retire — it's simply absent from the discussion, which means whoever eventually rebuilds the global layer has no way to know whether it should be preserved, migrated, or is safe to ignore.

**Recommendation:** add one line to Section 33's open-questions list (or a new question) asking explicitly what the radio/audio/broadcast subsystem (`rr-radio`, `rr-audio-recv`, `rr-icecast`, `rr-youtube`, `rr-chat`, `rr-packer`, `rr-dropins`) is for and whether it's in active use — this is exactly the kind of undiscovered-territory item the multi-AI review process exists to surface, and it wasn't visible to Copilot's or Grok's earlier passes because it sits outside the repositories they were working from at the time.

---

*End of Pass 6. Remaining unexplored territory from the supplied archives: `RootRecord-Website`'s actual page implementations (only skimmed for the solar/website duplication question in Pass 2) and the `a-eyes` and `plumbing` directories in Solar-Pacific, neither opened yet in this series.*
