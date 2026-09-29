# RootRecord Repository Map (Draft)

**Contributor:** Grok (xAI)  
**Date:** 2026-09-27  
**Status:** Draft for collaborative review  
**Evidence basis:** Public GitHub surface under `rootrecordsoftwaresolutions`, prior conversation analysis, MULTI-AGENT-IDENTITY document, Solar-Pacific structure, and observed agent-context model.  
**Related prior work:**  
- `Restructuring RootRecord.md`  
- `Grok-Reasoning-Frameworks-Exploration.md`  
- Phase 0 recommendation from Grok’s full contribution

---

## 1. Purpose of This Map

This document is the canonical inventory of repositories and local caches that constitute the RootRecord ecosystem after the clean-system reset.

For every entry it records:

- Purpose
- Authority classification (Canonical / Operational Control / Identity / Transitional / Archival / Experimental)
- Owner
- Runtime location (where the live system actually runs or is cached)
- Primary dependencies
- Backup / recovery posture
- Notes / open questions

The map exists so that agents and humans stop inferring purpose from names or historical accumulation.

---

## 2. Layer Model

```
ORGANIZATIONAL LAYER (RootRecord Software Solutions / rootrecordsoftwaresolutions)
├── Operational Control Plane
├── Canonical Data
├── Public Presentation
└── Secondary Execution / Recovery

AGENT IDENTITY LAYER (individual GitHub accounts)
├── AvaIvy
├── BruceMonitor
└── CarlyMal

LOCAL CACHE / OPERATIONAL LAYER (Solar/Pacific machine)
├── /home/rootrecord/Documents/RootRecord Library/
│   ├── Handoff-Context/
│   └── Agent Context/
└── master-key.env + operational state
```

---

## 3. Organizational Layer Repositories

### 3.1 Solar-Pacific-RootRecord-Server

| Field | Value |
|-------|-------|
| **URL** | https://github.com/rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server |
| **Purpose** | Primary operational control plane. Contains 0-master-prompt, automations (jobs.py + poller), plumbing (single-flight inference), root-status, agents scaffolding, weather orchestration, energy, a-eyes, handoff material, and system context. |
| **Authority** | **Operational Control Plane** (canonical for running operations on Solar/Pacific) |
| **Owner** | RootRecord Software Solutions (organizational) |
| **Runtime** | Solar/Pacific machine (primary working tree / clone) |
| **Key Dependencies** | master-key.env, local Database/, Ollama/FLM, Cloudflare tunnel |
| **Backup Posture** | Code in Git; operational state and Database/ require separate backup strategy |
| **Notes** | This is the living heart of the current system. Do not treat it as temporary scaffolding. Many of the architectural principles are already embodied here. |

### 3.2 RootRecord-Weather-Database

| Field | Value |
|-------|-------|
| **URL** | https://github.com/rootrecordsoftwaresolutions/RootRecord-Weather-Database |
| **Purpose** | Canonical source-preserving weather data and media for Hawaiʻi. Raw sources + derived reports. |
| **Authority** | **Canonical Data** |
| **Owner** | RootRecord Software Solutions |
| **Runtime** | Collected and generated on Solar/Pacific; published via Git synchronization |
| **Key Dependencies** | Weather collectors / pollers in Solar-Pacific, external NWS and satellite sources |
| **Backup Posture** | Git history + local source material; treat raw sources as authoritative |
| **Notes** | Already correctly separated from AI runtime. Model example of data-first design. |

### 3.3 RootRecord-Website

| Field | Value |
|-------|-------|
| **URL** | https://github.com/rootrecordsoftwaresolutions/RootRecord-Website |
| **Purpose** | Public-facing Next.js / Vercel presentation and service interface for rootrecord.cloud |
| **Authority** | **Public Presentation** (not source of truth) |
| **Owner** | RootRecord Software Solutions |
| **Runtime** | Vercel |
| **Key Dependencies** | Status feeds, weather products, future paid APIs |
| **Backup Posture** | Standard Git + Vercel deployment history |
| **Notes** | Must consume versioned contracts; must never become the canonical data store. |

### 3.4 US-Mainland-Server

| Field | Value |
|-------|-------|
| **URL** | https://github.com/rootrecordsoftwaresolutions/US-Mainland-Server |
| **Purpose** | Secondary infrastructure node for service continuity, synchronization, offloading, and recovery when Solar/Pacific is unavailable. |
| **Authority** | **Secondary Execution / Recovery** |
| **Owner** | RootRecord Software Solutions |
| **Runtime** | US Mainland / AWS / EC2 (intended) |
| **Key Dependencies** | Synchronization contracts with Solar-Pacific, shared job definitions, credentials via master-key.env model |
| **Backup Posture** | Must be able to operate in degraded mode from last-known-good state |
| **Notes** | Currently described as a stub/secondary node. Job ownership / lease semantics are required before dual execution is safe. |

### 3.5 RootRecord-Master-Prompt (if distinct)

| Field | Value |
|-------|-------|
| **URL** | Referenced in 0-master-prompt documentation |
| **Purpose** | Shared architectural / context material (may be overlapping with or extracted from Solar-Pacific 0-master-prompt) |
| **Authority** | **Canonical Context** (or Transitional if still fully inside Solar-Pacific) |
| **Owner** | RootRecord Software Solutions |
| **Notes** | Confirm whether this is a separate repository or still a directory. Prefer a single source of truth for the master prompt family. |

---

## 4. Agent Identity Layer

These repositories belong to individual agent identities, not the organization.

### 4.1 AvaIvy / Agent-Context

| Field | Value |
|-------|-------|
| **URL** | https://github.com/AvaIvy/Agent-Context (expected) |
| **Purpose** | Ava’s persistent identity, personality, operating context, skills, and self-updating memory. |
| **Authority** | **Agent Identity** (canonical for Ava) |
| **Owner** | AvaIvy (individual account) |
| **Local Cache** | `/home/rootrecord/Documents/RootRecord Library/Agent Context/Ava-Agent-Context` |
| **Sync** | Watchdog / poller pushes from local cache → remote (on-edit or hourly) |
| **Secrets** | Must never contain credentials; all secrets via host master-key.env |
| **Notes** | Ava = Visionary Architect. Context should emphasize architecture, exploration, and design. |

### 4.2 BruceMonitor / Agent-Context

| Field | Value |
|-------|-------|
| **URL** | https://github.com/BruceMonitor/Agent-Context (expected) |
| **Purpose** | Bruce’s persistent identity and operational context. |
| **Authority** | **Agent Identity** |
| **Owner** | BruceMonitor |
| **Local Cache** | `.../Bruce-Agent-Context` |
| **Notes** | Bruce = Systems / Infrastructure / Implementation. Context should emphasize runbooks, deployment, and operational reality. |

### 4.3 CarlyMal / Carly-Agent-Context

| Field | Value |
|-------|-------|
| **URL** | https://github.com/CarlyMal/Carly-Agent-Context (expected) |
| **Purpose** | Carly’s persistent identity and security-focused context. |
| **Authority** | **Agent Identity** |
| **Owner** | CarlyMal |
| **Local Cache** | `.../Carly-Agent-Context` |
| **Notes** | Carly = Security Specialist / Independent Reviewer. Context should contain threat models, audit patterns, and critique protocols. |

---

## 5. Local Operational Layer (Solar/Pacific Machine)

These are not GitHub repositories but are critical parts of the map.

| Path | Purpose | Authority | Notes |
|------|---------|-----------|-------|
| `/home/rootrecord/master-key.env` | Single source of all credentials and configuration | **Canonical Secrets** | Never in Git. chmod 600. Backed up separately. |
| `/home/rootrecord/master-key.env.schema` | Documented variable contract (no secrets) | Canonical (versioned in Git) | Recommended immediate addition. |
| `/home/rootrecord/.env-backups/` | Rotated backups of master-key.env | Operational | Retention + restore test required. |
| `/home/rootrecord/Documents/RootRecord Library/Handoff-Context/` | Org-owned structural + current-state layer | **Canonical Handoff** | MASTER-PROMPT links, CURRENT-STATE, ACTIVE-AGENTS, CRITICAL-STATE, recovery procedures. |
| `/home/rootrecord/Documents/RootRecord Library/Agent Context/` | Local working copies of the three agent context repos | Cache | Synced by watchdog. |
| `/home/rootrecord/Database/` | Operational data, GITHUB bak, intake, etc. | Operational State | Requires its own backup strategy. |

---

## 6. Classification Legend

| Classification | Meaning |
|----------------|---------|
| **Canonical** | Authoritative source of truth for that concern |
| **Operational Control Plane** | Where the live control and scheduling actually runs |
| **Agent Identity** | Belongs to a specific agent account; not org-owned |
| **Public Presentation** | Consumes data; must not become source of truth |
| **Secondary Execution / Recovery** | Can take over designated work; not primary owner |
| **Transitional** | Currently in use but expected to move or be clarified |
| **Archival / Experimental** | Not authoritative; keep only for history or experiments |

---

## 7. Immediate Open Questions (for next intake)

1. Exact GitHub URLs and visibility of the three Agent-Context repositories (confirm public/private and exact names).
2. Is `RootRecord-Master-Prompt` a separate repository or still only a directory inside Solar-Pacific?
3. Are there any other repositories under the organization or related accounts that should appear on this map?
4. Current backup frequency and restore-test status for master-key.env and the agent context repos.
5. Whether any top-level directories inside Solar-Pacific should be extracted into focused repositories (current recommendation: mostly no).

---

## 8. Recommended Next Actions from This Draft

1. Human or agent verification of the three Agent-Context repository URLs and visibility.
2. Addition of `master-key.env.schema` and validation script.
3. Creation of the Handoff-Context directory structure with initial files.
4. Short ADR recording the decision that Solar-Pacific remains the operational control plane.
5. Update of this map once the above are confirmed (treat this draft as living).

---

## 9. Evidence Status Summary

- Existence and high-level purpose of Solar-Pacific, Weather-Database, Website, US-Mainland-Server: **Confirmed** (public GitHub).
- Detailed internal structure of Solar-Pacific (0-master-prompt, automations, plumbing, etc.): **Confirmed** from public tree and SKILL.md files.
- Per-agent context repositories and local cache model: **Confirmed** from conversation and MULTI-AGENT document; exact current remote state needs live verification.
- master-key.env as single secrets source: **Confirmed** from operator statements.
- Exact backup and restore posture: **Unknown** — requires live check.

---

**End of Draft Repository Map**  
This document is intended to be updated as verification proceeds. Claude and other contributors should treat gaps marked Unknown as high-priority clarification items.
