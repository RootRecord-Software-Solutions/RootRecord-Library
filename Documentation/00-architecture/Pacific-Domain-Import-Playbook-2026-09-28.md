# Pacific Domain Import Playbook

| Field | Value |
| --- | --- |
| **Date** | 2026-09-28 (HST) |
| **Live runtime** | `RootRecord-Pacific-Solar-Server` on Ecosystem `1 - Servers/` |
| **Updated** | 2026-09-28 ~17:01 HST — no Pacific Logs domain |

---

## Standing rules (always)

### 1. One domain folder — code domains only

Pacific **code** domains (capitalized):

```text
Automations/  Communications/  Energy/  System/  Weather/
Github/  Geology/  Security/
```

**Not a Pacific domain:** `Logs/`.

Persistent logs and operational log files live under the **Database** authority:

```text
/home/rootrecord/Database/Logs/
  Automations/automations_current.log   # poller (canonical)
  …
```

Do **not** recreate a `Logs/` tree under Pacific for “pointers” — it duplicates authority and confuses operators. Code stays on Pacific; log **bytes** stay on Database.

**Do not** create parallel lowercase folders/symlinks for package names (e.g. no `energy` → `Energy`).

### 2. Python packages match the domain folder

Rewrite G2 imports to the Pacific folder name (`Energy`, `System`, `Geology`, …). `PYTHONPATH` includes Pacific root (+ vendor as needed).

### 3. Paths with spaces — always quote

### 4. No old desk as runtime host

### 5. Data stays in Database

Samples, ENERGY stores, frames, **and logs** → `/home/rootrecord/Database/…`.

### 6. Geology owns Kīlauea + all earthquake functions

See [Geology-Domain-Ownership-Kilauea-Earthquakes-2026-09-28.md](./Geology-Domain-Ownership-Kilauea-Earthquakes-2026-09-28.md).

---

## Phase 0 — Preconditions

- [x] Pacific code domains; Automations live
- [x] Energy + System LIVE
- [x] Pacific `Logs/` domain removed (2026-09-28) — Database only for logs

---

## Phase 1–4

Unchanged import template: copy into existing **code** domain folder → rewire jobs → Database for bytes → verify.

Remaining residuals: worklog, github, plumbing, telegram, a-eyes, weather, Geology import, energy actions.

---

*Playbook 2026-09-28 HST.*
