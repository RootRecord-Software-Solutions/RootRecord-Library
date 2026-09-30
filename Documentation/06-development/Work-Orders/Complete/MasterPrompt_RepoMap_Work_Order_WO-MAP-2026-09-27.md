# WORK ORDER — Master-Prompt Repository Ownership Map

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-MAP-2026-09-27 |
| **Date** | 2026-09-27 (HST) |
| **Status** | COMPLETE — signed off 2026-09-29 ~21:41 HST. Short map and Library ownership note are in place. |
| **Owner** | RootRecord |
| **Related** | WO-ECO; WO-SRV; `0 - Master-Prompt/prompts/08-repository-and-file-links.md` |
| **Updated** | 2026-09-29 (HST) |

**Scope:** Add a short canonical ownership contract to the Master-Prompt boot path so agents answer *where does this go?* without loading full Library history. Do not paste the entire ecosystem tree into boot prompts.

---

## 1. Intent

Master-Prompt is the first thing agents load. Library holds deep *why* and history. The short map can now include the known Pacific org repo and live Servers path.

---

## 2. Current reality (2026-09-28)

### 2.1 What exists

| Item | Location / status |
| --- | --- |
| Master-Prompt tree | `RootRecord-Ecosystem/0 - Master-Prompt/` (prompts 00–09, state, manifest) |
| Intended file | `prompts/08-repository-and-file-links.md` |
| Library (canonical) | `RootRecord-Software-Solutions/RootRecord-Library` |
| **Pacific runtime (canonical)** | `RootRecord-Software-Solutions/RootRecord-Pacific-Solar-Server` |
| **Live local path** | `…/1 - Servers/1 - RootRecord-Pacific-Solar-Server` |
| Other runtime repos | US-Mainland, Website, Weather-Database under `rootrecordsoftwaresolutions` |
| Ownership narrative (deferred deep doc) | Library `Documentation/00-architecture/Repository Ownership Model.md` (not written yet) |

### 2.2 Completed so far

- [x] Dual-layer principle agreed (Master-Prompt = where; Library = why/history)
- [x] Working draft boundaries in WO-ECO
- [x] Pacific server name + org + live path confirmed (WO-SRV)
- [x] Expand `08-repository-and-file-links.md` (ownership contract, 2026-09-29)
- [x] Optional deep doc: `Documentation/00-architecture/Repository-Ownership-Model.md`
- [x] `prompts.yaml` already loads `08-repository-and-file-links.md` as required
- [x] One-line link added from Ava, Bruce, and Carly `CONTEXT/REPOS.md`

### 2.3 Known friction

- Org split: Library + Pacific under `RootRecord-Software-Solutions`; Mainland/Website/Weather under `rootrecordsoftwaresolutions`
- Residual job paths still reference legacy `~/.ollama/skills` for unimported domains
- **Historical:** prior remote `rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server` (superseded for Pacific runtime)

---

## 3. Tasks

1. Expand `08-repository-and-file-links.md` with short sections (purpose, URL, contains, does-not-contain) plus Boundary Rule.
2. Include every live canonical repo: Library, Pacific-Solar-Server, Mainland, Website, Weather-Database.
3. Note live Pacific path under Ecosystem `1 - Servers/`.
4. Link from each agent pack `CONTEXT/REPOS.md` to Master-Prompt map (one line), not a full copy.
5. Optionally add Library `Documentation/00-architecture/Repository Ownership Model.md` for migration history.

---

## 4. Non-goals

- Full filesystem tree in boot prompt
- Duplicating entire agent packs into Master-Prompt
- Finalizing temporary READMEs on empty domain shells

---

## 5. Key file / path reference

| Path | Role |
| --- | --- |
| `0 - Master-Prompt/prompts/08-repository-and-file-links.md` | Short ownership contract |
| `0 - Master-Prompt/manifest/prompts.yaml` | Ensure 08 is in load path |
| `5 - RootRecord-Library/.../Repository Ownership Model.md` | Deep narrative (optional) |
| `github/scripts/repos.conf` | Sync catalog must stay consistent with map |

---

## 6. Notes & constraints

- No force-push.
- Secrets stay out of git.
- Prefer small reversible steps.
- Pacific name is no longer blocking; residual domain imports do not block writing the short map.

---

*Work order prepared 2026-09-27 HST. Updated 2026-09-28 HST after Pacific cutover confirmation.*
