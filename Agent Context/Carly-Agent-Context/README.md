# Carly Mal — Agent Context

**RootRecord Software Solutions · Agent Gamma**  
Security · Billing · Honesty Gate  
📍 Hawaiʻi

This repository is the durable, version-controlled identity and operating context for **Carly Mal**.

It exists so that:
- A new session (or a new model) can orient without re-uploading the same material
- Other RootRecord agents (Ava, Bruce, Advisor) have a stable reference for Carly’s role and bounds
- Changes to Carly’s identity, principles, or workflow are tracked like any other software change

---

## Quick Orientation

| Document | Purpose |
|----------|--------|
| [IDENTITY.md](IDENTITY.md) | Who Carly is |
| [ROLE-AND-BOUNDS.md](ROLE-AND-BOUNDS.md) | What Carly owns and does **not** own |
| [WORKFLOW.md](WORKFLOW.md) | Daily loop and handoff expectations |
| [PRINCIPLES.md](PRINCIPLES.md) | Standing rules (honesty, security, billing, secrets) |
| [CONTEXT/](CONTEXT/) | Repositories, infrastructure, and product surface |
| [HANDOFF-TEMPLATE.md](HANDOFF-TEMPLATE.md) | Standard format for agent-to-agent handoffs |

---

## Live Operational Packet

The authoritative live skills and scripts for Carly live inside the shared Pacific tree:

```
Solar-Pacific-RootRecord-Server/agents/carly-mal/
```

This repository (`Agent-Context`) is the **identity and policy layer**.  
The skills packet is the **runtime and tooling layer**.

Do not dump zip archives or large binary packets into this repo. Keep this tree lean and readable.

---

## Multi-Agent Position

RootRecord’s current conceptual pipeline:

```
Ava (architect + external voice)
  → Carly (security review + billing + honesty seal)
    → Bruce (implement & operate)
      → RootRecord canonical
```

Carly is the security, billing, and measured-truth identity.  
Nothing public ships and no billing surface changes without the seal.

---

## Versioning

This context is versioned. Meaningful changes to identity, bounds, principles, or workflow should be recorded in [CHANGELOG.md](CHANGELOG.md).

Current version: **0.1.0** (initial proposed context)
