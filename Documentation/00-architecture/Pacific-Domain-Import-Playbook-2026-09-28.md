# Pacific Domain Import Playbook

| Field | Value |
| --- | --- |
| **Date** | 2026-09-28 (HST) |
| **Live runtime** | `RootRecord-Pacific-Solar-Server` on Ecosystem `1 - Servers/` |
| **Authority** | Org [RootRecord-Software-Solutions](https://github.com/RootRecord-Software-Solutions) |
| **Updated** | 2026-09-28 — domain list + residual verification state |

---

## Standing rules (always)

### 1. One domain folder — code domains only

Pacific **code** domains (capitalized), as present on the live tree:

```text
Automations/      Communications/   Energy/      System/
Weather/          Github/           Geology/     Security/
Reports/          A-Eyes/
```

**Not a Pacific domain:** `Logs/`.

Persistent logs and operational log files live under the **Database** authority:

```text
/home/rootrecord/RootRecord-Ecosystem/2 - RootRecord-Database/Logs/
  Automations/automations_current.log   # poller (canonical)
  …
```

Do **not** recreate a `Logs/` tree under Pacific for “pointers” — it duplicates authority and confuses operators. Code stays on Pacific; log **bytes** stay on Database.

**Do not** create parallel lowercase folders/symlinks for package names (e.g. no `energy` → `Energy`).

### 2. Python packages match the domain folder

Rewrite G2 imports to the Pacific folder name (`Energy`, `System`, `Geology`, …). `PYTHONPATH` includes Pacific root (+ vendor as needed).

### 3. Paths with spaces — always quote

### 4. No old desk as runtime host

G3 Automations is the only poller host. G1/G2 skill trees are not production schedulers.

### 5. Data stays in Database

Samples, ENERGY stores, frames, **and logs** → `/home/rootrecord/Database/…`.

### 6. Geology owns Kīlauea + all earthquake functions

See [Geology-Domain-Ownership-Kilauea-Earthquakes-2026-09-28.md](./Geology-Domain-Ownership-Kilauea-Earthquakes-2026-09-28.md).

### 7. Retirement stubs (preferred over silent delete)

When a G1/G2 packet is fully superseded:

1. Keep the folder shell and `SKILL.md` (if present).  
2. Add **`MIGRATED.md`** at the packet root: status, date, canonical org repo + path, “do not run”.  
3. Do not restore or schedule from the old path.  
4. Auto-sync will carry GitHub markers to desk trees the catalog owns.

**Example (done 2026-09-28 on `-Old`):** `hybrid-night-poller/`, `heartbeat/`, `net-gate/` → org Pacific Automations.

---

## Phase 0 — Preconditions

- [x] Pacific code domains; Automations live  
- [x] Energy + System LIVE  
- [x] Reports foundation LIVE (WO-RPT-001)  
- [x] Plumbing under `System/scripts/plumbing/`  
- [x] Pacific `Logs/` domain removed (2026-09-28) — Database only for logs  
- [x] G1 scheduler trio marked `MIGRATED.md` on `-Old` (2026-09-28)  

---

## Phase 1–4

Unchanged import template: copy into existing **code** domain folder → rewire jobs → Database for bytes → verify → optional `MIGRATED.md` on old packet.

Current residuals: **runtime verification / legacy retirement** for Telegram, A-Eyes, Energy actions, and Pacific poller ([G3 checklist](./G3-Runtime-Verification-Checklist-2026-09-28.md)). Weather remains disabled and outside the active cutover scope. Geology import remains a separate open work order. Skills were functional packets, not a long-term AI design; redesign planned separately.

---

*Playbook updated 2026-09-28 ~21:40 HST — Reports + A-Eyes on domain list; residual = verification.*


## Security Domain Naming Correction — 2026-09-28

Operator correction: the camera/security packet previously labeled **A-Eyes** is to be built under the Pacific **Security/** domain. A-Eyes is not the final domain name.

The Security runtime remains code on Pacific. Persistent security log bytes and media bytes belong to the new RootRecord-Database authority:

```text
/home/rootrecord/RootRecord-Ecosystem/2 - RootRecord-Database/
├── Logs/Security/
└── Media/
    ├── Images/
    └── Timelapses/
```

The existing A-Eyes migration is an intermediate state and must be renamed/rebased to Security before its runtime verification and legacy retirement gate can be satisfied. Runtime camera credentials/configuration are not Git artifacts.
