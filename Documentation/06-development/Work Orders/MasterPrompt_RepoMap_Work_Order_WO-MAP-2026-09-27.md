# WORK ORDER — Master-Prompt Repository Ownership Map

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-MAP-2026-09-27 |
| **Date** | 2026-09-27 (HST) |
| **Status** | OPEN — Blocked on final new-repo name list |
| **Owner** | RootRecord |
| **Related** | WO-ECO-2026-09-27; `0 - Master-Prompt/prompts/08-repository-and-file-links.md` |

**Scope:** Add a short canonical ownership contract to the Master-Prompt boot path so agents answer *where does this go?* without loading full Library history. Do not paste the entire ecosystem tree into boot prompts.

---

## 1. Intent

Master-Prompt is the first thing agents load. Library holds deep *why* and history. After Library went online under `RootRecord-Software-Solutions`, the dual-layer split is agreed; the short map is still unwritten because additional repos are still being named.

---

## 2. Current reality

### 2.1 What exists

| Item | Location / status |
| --- | --- |
| Master-Prompt tree | `RootRecord-Ecosystem/0 - Master-Prompt/` (prompts 00–09, state, manifest) |
| Intended file | `prompts/08-repository-and-file-links.md` |
| Library (canonical) | `RootRecord-Software-Solutions/RootRecord-Library` |
| Runtime repos | Solar-Pacific, US-Mainland, Website, Weather-Database under `rootrecordsoftwaresolutions` |
| Ownership narrative (deferred deep doc) | Library `Documentation/00-architecture/Repository Ownership Model.md` (not written yet) |

### 2.2 Completed so far

- [x] Dual-layer principle agreed (Master-Prompt = where; Library = why/history)
- [x] Working draft boundaries in WO-ECO
- [ ] Expand `08-repository-and-file-links.md`
- [ ] Optional deep doc in Library architecture

### 2.3 Known friction

- Org split: Library under `RootRecord-Software-Solutions`; operational repos under `rootrecordsoftwaresolutions`
- Live runtime still largely under `~/.ollama/skills`, not only `1 - Servers/`
- New repo names under Servers / Node not finalized

---

## 3. Tasks

1. Collect final list: repo name, GitHub owner/org, local Ecosystem path, purpose, contains / does-not-contain.
2. Expand `08-repository-and-file-links.md` with short sections only (purpose, URL, contains, does-not-contain) plus one Boundary Rule.
3. Include every live canonical repo (Library, Pacific, Mainland, Website, Weather-Database, and any new ones).
4. Link from each agent pack `CONTEXT/REPOS.md` to Master-Prompt map (one line), not a full copy.
5. Optionally add Library `Documentation/00-architecture/Repository Ownership Model.md` for migration history and examples.

---

## 4. Non-goals

- Full filesystem tree in boot prompt
- Duplicating entire agent packs into Master-Prompt
- Finalizing temporary READMEs on empty repos

---

## 5. Key file / path reference

| Path | Role |
| --- | --- |
| `0 - Master-Prompt/prompts/08-repository-and-file-links.md` | Short ownership contract |
| `0 - Master-Prompt/manifest/prompts.yaml` | Ensure 08 is in load path |
| `5 - RootRecord-Library/.../Repository Ownership Model.md` | Deep narrative (optional) |
| `github/scripts/repos.conf` | Sync catalog must stay consistent with map |

---

## 6. Open items

**Additional requirements:**

- Exact new server repo names under `1 - Servers/`
- Whether Master-Prompt itself becomes its own GitHub repo
- 

---

## 7. Notes & constraints

- No force-push.
- Secrets stay out of git.
- Prefer small reversible steps.
- Write the map only after the new-repo list is known so agents do not learn the wrong homes.

---

*Work order prepared 2026-09-27 HST. Update status when closed.*
