# Product & Archive Repository Catalog

| Field | Value |
| --- | --- |
| **Date** | 2026-09-28 (HST) |
| **Purpose** | Inventory every independent product, Minecraft/RootMC, app, and inventory mirror so nothing is forgotten |
| **Authority** | Org [RootRecord-Software-Solutions](https://github.com/RootRecord-Software-Solutions) for ops; product code may stay under historical accounts until promoted |
| **Rule** | **Documentation only** — no migration execution here. Promote into org / new ops **after** Pacific residual domains catch up |

**Related:** [MIGRATION-DOCS-INDEX](./MIGRATION-DOCS-INDEX-2026-09-28.md) · [Migration-Lineage](./Migration-Lineage-Three-Generations-2026-09-28.md) · G1 [Solar-Pacific-Old README](https://github.com/rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server-Old/blob/main/README.md) · G0 [`old`](https://github.com/rootrecordsoftwaresolutions/old/blob/main/README.md)

---

## 1. Accounts & roles

| Account | Role |
| --- | --- |
| **`RootRecord-Software-Solutions` (org)** | Canonical ops: Library, Pacific, Database |
| **`rootrecordsoftwaresolutions` (user)** | Working set + **Aug 2026 inventory mirrors** + private product/infra |
| **`RootRecord` (user)** | Public **Paper/RootMC plugins** + download pages + older tools (last meaningful ~2026-07-30) |
| **`RootMC` (org/user)** | Legacy **Nukkit-era** plugins (2020–2022); long stale; mirrored |

Treat `RootRecord` + `RootMC` as **historical / read-only** sources. Prefer mirrors under `rootrecordsoftwaresolutions` for inventory; prefer org for future canonical homes.

---

## 2. Migration posture (products)

```text
1. Finish Pacific G2 residual domains (ops path)
2. Then promote or re-home products deliberately:
     - RootMC Paper suite  → product org path or dedicated RootMC home (not Pacific server core)
     - Weather/Business Manager apps → product repos under org when ready
     - Solana / websites / workspace  → product or Website track
3. Never bulk-merge plugin trees into RootRecord-Pacific-Solar-Server
```

Pacific = solar/ops/agents runtime. **Minecraft and desktop apps are separate product lines.**

---

## 3. Org (live ops) — already documented elsewhere

| Repo | Role |
| --- | --- |
| [RootRecord-Library](https://github.com/RootRecord-Software-Solutions/RootRecord-Library) | Docs / agent context |
| [RootRecord-Pacific-Solar-Server](https://github.com/RootRecord-Software-Solutions/RootRecord-Pacific-Solar-Server) | G3 live runtime |
| [RootRecord-Database](https://github.com/RootRecord-Software-Solutions/RootRecord-Database) | Data & log layout SOT |

---

## 4. `rootrecordsoftwaresolutions` — primary (non-mirror) working set

### 4.1 Pacific / ops / continuity

| Repo | Priv | Notes |
| --- | --- | --- |
| [Solar-Pacific-RootRecord-Server](https://github.com/rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server) | public | G2 residual skills desk |
| [Solar-Pacific-RootRecord-Server-Old](https://github.com/rootrecordsoftwaresolutions/Solar-Pacific-RootRecord-Server-Old) | public | **G1** archive + migration README |
| [old](https://github.com/rootrecordsoftwaresolutions/old) | private | **G0** deepest archive + README |
| [US-Mainland-Server](https://github.com/rootrecordsoftwaresolutions/US-Mainland-Server) | public | Continuity node |
| [ollama-skills](https://github.com/rootrecordsoftwaresolutions/ollama-skills) | private | OmniBook `~/.ollama/skills` desk |

### 4.2 Ava / core stacks (independent of Pacific domain folders)

| Repo | Priv | Notes |
| --- | --- | --- |
| [ava-core](https://github.com/rootrecordsoftwaresolutions/ava-core) | private | Current Ava core line |
| [ava-core-old](https://github.com/rootrecordsoftwaresolutions/ava-core-old) | private | Older Ava Ivy + GEO docs |
| [ava-core-private](https://github.com/rootrecordsoftwaresolutions/ava-core-private) | private | OptiPlex handoff subset mirror |
| [Ava-Directory](https://github.com/rootrecordsoftwaresolutions/Ava-Directory) | private | AVA Core directory / ops docs |
| [Ava-Ivy-Cloud](https://github.com/rootrecordsoftwaresolutions/Ava-Ivy-Cloud) | private | avaivy.cloud |
| [RootRecord-Core-Node](https://github.com/rootrecordsoftwaresolutions/RootRecord-Core-Node) | private | Core node |
| [RootRecord-Core-Ops](https://github.com/rootrecordsoftwaresolutions/RootRecord-Core-Ops) | private | Developer/operator desk |
| [RootRecord-Core-Processor](https://github.com/rootrecordsoftwaresolutions/RootRecord-Core-Processor) | private | 24/7 operations host |
| [RootRecord-Cloud](https://github.com/rootrecordsoftwaresolutions/RootRecord-Cloud) | private | Cloud surface |

### 4.3 RootMC / web product surfaces (not Paper plugins)

| Repo | Priv | Notes |
| --- | --- | --- |
| [RootRecord-RootMC](https://github.com/rootrecordsoftwaresolutions/RootRecord-RootMC) | private | RootMC product line under new account |
| [RootMC-Net](https://github.com/rootrecordsoftwaresolutions/RootMC-Net) | private | rootmc.net HTML |
| [rootmc-emergent](https://github.com/rootrecordsoftwaresolutions/rootmc-emergent) | private | Emergent monorepo: RootMC + Ava + web/Worker surfaces |
| [web-files](https://github.com/rootrecordsoftwaresolutions/web-files) | private | Aggregated web files for merge |
| [all-connections](https://github.com/rootrecordsoftwaresolutions/all-connections) | private | URL atlas / combined snapshot for agents |

### 4.4 Public product / data

| Repo | Priv | Notes |
| --- | --- | --- |
| [RootRecord-Website](https://github.com/rootrecordsoftwaresolutions/RootRecord-Website) | private | Public Next.js surface |
| [RootRecord-Weather-Database](https://github.com/rootrecordsoftwaresolutions/RootRecord-Weather-Database) | public | Weather data & media |

---

## 5. RootMC Paper plugin suite (`RootRecord/*`) — primary historical sources

Public Paper plugins (topics: `minecraft`, `paper-plugin`, `rootmc`). Last cluster of pushes ~**2026-07-27 → 2026-07-30**. **All mirrored** under `rootrecordsoftwaresolutions/mirror-rootrecord-*` (Aug 2026 inventory).

### 5.1 Spine / identity / perms

| Repo | Description |
| --- | --- |
| [root-core](https://github.com/RootRecord/root-core) | Central connection, cloud identity, license spine |
| [root-perms](https://github.com/RootRecord/root-perms) | First-party permissions (groups, tracks, Vault) |
| [root-memberships](https://github.com/RootRecord/root-memberships) | Cloud membership → permission group sync |
| [rootrecord-common](https://github.com/RootRecord/rootrecord-common) | Shared common library |
| [rootmc](https://github.com/RootRecord/rootmc) | Account linking, McMMO sync, shops economy, app heartbeat |
| [rootmc-official](https://github.com/RootRecord/rootmc-official) | Towny-claims progression link (playtime, votes, perms) |

### 5.2 Economy / shops / reserve

| Repo | Description |
| --- | --- |
| [root-economy](https://github.com/RootRecord/root-economy) | Gold economy (Vault, treasury, bonds, loans, upkeep) |
| [rootmc-shops](https://github.com/RootRecord/rootmc-shops) | Chest shops, dynamic caps, /buy /sell |
| [root-chestshops](https://github.com/RootRecord/root-chestshops) | Chest shop implementation line |
| [root-market](https://github.com/RootRecord/root-market) | Browse listings /market /items /shops |
| [root-bonds](https://github.com/RootRecord/root-bonds) | Bonded notes → reserve / redeem gold |
| [root-loans](https://github.com/RootRecord/root-loans) | Personal and town loans from Server Reserve |
| [root-upkeep](https://github.com/RootRecord/root-upkeep) | Inactivity tax (players, towns, nations) |
| [root-ranks](https://github.com/RootRecord/root-ranks) | Purchasable ranks (LuckPerms + gold) |
| [root-referrals](https://github.com/RootRecord/root-referrals) | Referral codes and milestones |
| [root-rewards](https://github.com/RootRecord/root-rewards) | Playtime milestones and vote rewards |
| [root-appreciation](https://github.com/RootRecord/root-appreciation) | /thanks stats, /bonus streaks |
| [root-try](https://github.com/RootRecord/root-try) | Paid feature tryouts from Reserve |

### 5.3 Play / progression / world

| Repo | Description |
| --- | --- |
| [root-play](https://github.com/RootRecord/root-play) | Play progression, ranks, help |
| [root-claims](https://github.com/RootRecord/root-claims) | Claims line |
| [root-spawn](https://github.com/RootRecord/root-spawn) | Spawn safe zone, wall, mapping |
| [root-territories](https://github.com/RootRecord/root-territories) | Nation influence, BlueMap shapes |
| [root-mapper](https://github.com/RootRecord/root-mapper) | Area mapper polygons / boundaries |
| [root-chamber](https://github.com/RootRecord/root-chamber) | Chamber survival minigame |
| [root-gamble](https://github.com/RootRecord/root-gamble) | Casino minigames |
| [root-haste](https://github.com/RootRecord/root-haste) | Pass-the-torch / joint minigame |
| [root-potions](https://github.com/RootRecord/root-potions) | Potion brewing guide |
| [root-iteminfo](https://github.com/RootRecord/root-iteminfo) | World item census /info |
| [root-times](https://github.com/RootRecord/root-times) | Day clock, AFK/activity, timezone peaks |
| [root-activity](https://github.com/RootRecord/root-activity) | Playtime by timezone |
| [root-banner](https://github.com/RootRecord/root-banner) | Banner-related |
| [root-essentials](https://github.com/RootRecord/root-essentials) | EssentialsX-style QoL |

### 5.4 Ops / admin / integrations

| Repo | Description |
| --- | --- |
| [root-ops](https://github.com/RootRecord/root-ops) | Admin, restart, announcer, mapper |
| [root-admin](https://github.com/RootRecord/root-admin) | Admin tools |
| [root-restart](https://github.com/RootRecord/root-restart) | Graceful restart/stop countdown |
| [root-announcer](https://github.com/RootRecord/root-announcer) | Announcements |
| [root-discord](https://github.com/RootRecord/root-discord) | Discord integration |
| [root-ping](https://github.com/RootRecord/root-ping) | /ping → MySQL samples |
| [root-webstat](https://github.com/RootRecord/root-webstat) | Per-server stats site + JSON APIs |
| [root-bluemap-r2-fix](https://github.com/RootRecord/root-bluemap-r2-fix) | BlueMap R2 fix |
| [roothelp](https://github.com/RootRecord/roothelp) | /rules /cmds /discord /map /feedback |

**Future home:** product track (e.g. org `RootMC` suite or dedicated product org), **not** Pacific Automations/Energy domains.

---

## 6. RootMC Nukkit legacy (`RootMC/*`) — 2020–2022

Fully stale; mirrors exist.

| Repo | Description |
| --- | --- |
| [NPCRotation](https://github.com/RootMC/NPCRotation) | NPCs look at player |
| [DynamicMOTD](https://github.com/RootMC/DynamicMOTD) | Dynamic MOTD |
| [ASkyBlock](https://github.com/RootMC/ASkyBlock) | Skyblock |
| [CustomNukkit](https://github.com/RootMC/CustomNukkit) | Custom multi-version Nukkit |
| [OnlyLobby](https://github.com/RootMC/OnlyLobby) | END portal / lobby |
| [CombineSlot](https://github.com/RootMC/CombineSlot) | Combine slot |

Also mirrored: `CustomSynapseAPI`, `EconomyAPI` (on mirror list; may not show as public on RootMC today).

---

## 7. Independent products & tools (`RootRecord` + mirrors)

| Product | Source / mirror | Notes |
| --- | --- | --- |
| **Business Manager** | [rootrecord-business-manager-download](https://github.com/RootRecord/rootrecord-business-manager-download); mirrors `*-business-manager-*`, `Alexrs94/...` | Windows installer / app / builder |
| **Weather Manager** | [rootrecord-weather-manager-download](https://github.com/RootRecord/rootrecord-weather-manager-download); mirrors `rr-weather-manager-*`, mobile, private dev | Desktop/mobile weather product |
| **Solana tools / sites** | [Solana-Tools](https://github.com/RootRecord/Solana-Tools); mirrors `solana-tools`, `solanasite`, `solana-rootrecord-site` | Local-first Solana dashboard |
| **Doc-Repo** | [Doc-Repo](https://github.com/RootRecord/Doc-Repo); mirror | Historical “official docs” — label historical vs org Library |
| **roboclipboard** | [roboclipboard](https://github.com/RootRecord/roboclipboard); mirror | Windows Explorer multi-thread copy menus |
| **Minecraft marketing** | mirrors `minecraft-marketing`, `rootmc-marketing` | Checklists / copy |
| **Web / mobile / workspace** | mirrors `web-development-2026`, `mobile-development-2026`, `rootrecord-website`, `rootrecord-workspace*`, `rootmc-web`, `monorepo` | Historical web/mobile aggregates |
| **Kīlauea product path** | mirror `kilauea` | Distinct from Pacific Geology domain import |
| **avas-core** | mirror `avas-core` | Older Ava naming |
| **Developer panel** | mirror `root-record-developer-panel` | Dev panel |
| **weather** (generic) | mirror `weather` | Older weather tree |

---

## 8. Inventory mirrors (Aug 2026) — complete list under `rootrecordsoftwaresolutions`

Created ~**2026-08-06/07**. Descriptions: *“Mirror of … Not primary.”* **Do not develop against mirrors** — use only for recovery if upstream is lost.

### 8.1 Nukkit / RootMC legacy mirrors

`mirror-rootmc-askyblock`, `mirror-rootmc-combineslot`, `mirror-rootmc-customnukkit`, `mirror-rootmc-customsynapseapi`, `mirror-rootmc-dynamicmotd`, `mirror-rootmc-economyapi`, `mirror-rootmc-npcrotation`, `mirror-rootmc-onlylobby`

### 8.2 Paper plugin mirrors (`mirror-rootrecord-root-*` and related)

`mirror-rootrecord-root-activity`, `root-admin`, `root-announcer`, `root-appreciation`, `root-banner`, `root-bluemap-r2-fix`, `root-bonds`, `root-chamber`, `root-chestshops`, `root-claims`, `root-core`, `root-discord`, `root-economy`, `root-essentials`, `root-gamble`, `root-haste`, `root-iteminfo`, `root-joint-test-perm`, `root-loans`, `root-mapper`, `root-market`, `root-memberships`, `root-ops`, `root-perms`, `root-ping`, `root-play`, `root-potions`, `root-ranks`, `root-referrals`, `root-restart`, `root-rewards`, `root-spawn`, `root-territories`, `root-times`, `root-try`, `root-units-idle-farmer`, `root-upkeep`, `root-webstat`, `roothelp`, `rootmc`, `rootmc-official`, `rootmc-shops`, `rootrecord-common`

### 8.3 Product / web / tools mirrors

`mirror-alexrs94-rootrecord-business-manager-app`, `mirror-rootrecord-avas-core`, `mirror-rootrecord-doc-repo`, `mirror-rootrecord-kilauea`, `mirror-rootrecord-minecraft-marketing`, `mirror-rootrecord-mobile-development-2026`, `mirror-rootrecord-monorepo`, `mirror-rootrecord-roboclipboard`, `mirror-rootrecord-root-record-developer-panel`, `mirror-rootrecord-rootmc-emergent`, `mirror-rootrecord-rootmc-marketing`, `mirror-rootrecord-rootmc-web`, `mirror-rootrecord-rootrecord-business-manager-app`, `mirror-rootrecord-rootrecord-business-manager-builder`, `mirror-rootrecord-rootrecord-business-manager-download`, `mirror-rootrecord-rootrecord-weather-manager-download`, `mirror-rootrecord-rootrecord-weather-manager-mobile`, `mirror-rootrecord-rootrecord-website`, `mirror-rootrecord-rootrecord-workspace`, `mirror-rootrecord-rootrecord-workspace-backup-20260428-231355`, `mirror-rootrecord-rr-weather-manager-dev-mobile-private`, `mirror-rootrecord-rr-weather-manager-dev-private`, `mirror-rootrecord-rr-weather-manager-mobile`, `mirror-rootrecord-solana-rootrecord-site`, `mirror-rootrecord-solana-tools`, `mirror-rootrecord-solanasite`, `mirror-rootrecord-weather`, `mirror-rootrecord-web-development-2026`

---

## 9. Suggested future migration tracks (after Pacific catch-up)

| Track | Contents | Target idea |
| --- | --- | --- |
| **A — RootMC Paper** | §5 plugins + mirrors | Dedicated product home (org or `RootMC` modern); versioned releases |
| **B — Nukkit legacy** | §6 | Archive-only; no active port unless business case |
| **C — Weather Manager** | download + mobile + private dev mirrors | Product repo under org; data stays Weather-Database |
| **D — Business Manager** | app + builder + download | Product repo under org |
| **E — Web / RootMC.net** | Website, RootMC-Net, rootmc-emergent, web-files | Align with RootRecord-Website / RootMC-Net |
| **F — Solana / crypto tools** | Solana-Tools + site mirrors | Product or tools repo; not Pacific |
| **G — Ava stacks** | ava-core*, Ava-*, Core-Node/Ops/Processor | Fold into Pacific/agents redesign **or** keep as sister product — decide at AI redesign |
| **H — Doc-Repo** | historical public docs | Label historical; Library is SOT |

---

## 10. Counts (snapshot 2026-09-28)

| Bucket | Approx. count |
| --- | --- |
| Org live ops | 3 |
| `rootrecordsoftwaresolutions` primary (non-mirror) | ~21 |
| Inventory mirrors | ~79 |
| `RootRecord` public (plugins + products) | ~48 |
| `RootMC` Nukkit public | 6 |

Search API may paginate; if a repo is missing from this doc, add a row and date the edit.

---

*Catalog 2026-09-28 HST. Update when promoting a product to org or retiring a mirror.*
