# WORK ORDER — Selective Recovery from Solar-Pacific-RootRecord-Server-Old (G1)

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-OLD-2026-09-28 |
| **Date** | 2026-09-28 (HST) |
| **Status** | OPEN — G3 is running the live jobs. The first new G1 packet is still not recovered. On 2026-09-30 only byte-identical skills copies were removed. Unique skills files and the 27 GB old-skills tree stay until Alexander names them. |
| **Owner** | RootRecord |
| **Related** | WO-SRV; WO-ECO; Migration lineage + Old inventory maps |

**Scope:** After G2→G3 domain imports stabilize, selectively recover unique useful scripts from the G1 archive repo without bulk-merging history or `origin/` into live runtime.

---

## 1. Intent

G1 (`rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server-Old`) holds thousands of historical skill packets. G3 is live. G2 still feeds residual jobs. Recovery must be packet-by-packet after the live path is safe.

---

## 2. Current reality

| Item | Status |
| --- | --- |
| G3 live | Confirmed (poller on Ecosystem Servers path) |
| G2 residual jobs | Pacific runs River reads, cameras, GitHub sync, plumbing, the Telegram relay, system sampling, reports, the globe, and the weather poller (rechecked 2026-09-30 01:24 HST). Delta 2 no longer transmits; that is expected. G2 code stays on disk until Alexander signs off retirement. River actuation and timelapse compile stay open on WO-SRV. |
| G1 inventory | Library `Solar-Pacific-Old-Inventory-Map-2026-09-28.md` |
| G1 path count | ~7286 (largest: `origin/` ~4k) |

### Completed

- [x] Lineage named (G1/G2/G3)
- [x] Old top-level map + proposed G3 homes
- [x] Import playbook (Phase 3 = G1)
- [ ] G2 Energy (and other residuals) imported into G3
- [ ] First G1 packet recovered under controlled diff

---

## 3. Tasks

1. Keep WO-SRV G2 imports ahead of this WO.
2. For each approved G1 packet: diff vs G3 domain; strip secrets; copy unique scripts only.
3. Prefer Energy G1 `ecoflow-*` only **after** G2 energy is in G3.
4. Explicitly exclude bulk `origin/`, `ecosystem-history/` from G3 runtime git.
5. Log each recovery commit + Library note.

---

## 4. Non-goals

- Replacing G3 Automations with G1 scheduler-clock / hybrid-night-poller without design review
- Importing product trees (rootmc, advertising, finance-desk) into Pacific server core
- Force-push or history rewrite on G1 or G3

---

## 5. Key references

| Resource | Role |
| --- | --- |
| https://github.com/rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server-Old | G1 archive |
| Library migration lineage + Old inventory + playbook | Process |
| WO-SRV | G2 residual cutover |

---

## 6. Notes

- No secrets in git.
- One packet at a time.
- Operational continuity beats archival purity.

---

*Work order opened 2026-09-28 HST.*
