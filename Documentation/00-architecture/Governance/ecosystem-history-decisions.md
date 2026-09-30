# Ecosystem history decisions

Source: G1 `ecosystem-history/NARRATIVE.md` only. Clock on that file: 2026-09-16 afternoon HST. `CURRENT.md` (generated), `references/` (docs dump), and `scripts/` (including delete, archive, and TTS helpers) were not copied into the live Folders.

Evidence label: **Historical**. The live tree is RootRecord-Ecosystem. Do not treat the paths below as the current host map.

## Locked facts from that draft

- The desk host named in the narrative is the HP OmniBook 5, Ubuntu, user `rootrecord`. The Dell OptiPlex is dead. **Historical** as a host map. The OptiPlex-is-dead fact still stands: do not point agent docs at it as production.
- The live tree named there is `/home/rootrecord/RootRecord/Ava-Core`, with origin at `http://127.0.0.1:8787/`. **Historical.** Authority is now `/home/rootrecord/RootRecord-Ecosystem`.
- Do not treat these as live: `C:\Users\rootr\ava`, `/home/ava-core/ava`, OptiPlex LAN, or Towny-as-production. RootMC production is `play.rootmc.net` only.
- Public doors named there: rootrecord.cloud and avaivy.cloud. Player currency named there is Gold, not USD.
- EcoFlow packs named there are DELTA 2 and RIVER 2 Pro only. Starlink was Delta AC and was never switched by the night window. **Historical** wiring note. Live power collection is the Pacific Energy BLE poller. Do not revive `drive-automation` or night-sleep job skips from this page.
- Topic skills existed so agents would read a short map instead of old markdown. Old trees are evidence, not runtime. Reading an August 2026 storage plan as live was called out as a lie.

## How it got there

- Through 2026-07, public products (Kīlauea, weather, RootMC, sites) already existed. The desk was not yet the OmniBook Ubuntu tree.
- 2026-08 was a dual world: Windows OmniBook (`C:\Users\rootr\ava`) and Linux OptiPlex (`/home/ava-core/ava`), with USB disks as cold archive. Towny was already not live. The SSD and HDD paths (`/home/ava-core/ava`, `/mnt/e`) are **Historical**.
- Early 2026-09 the OptiPlex failed (stale-docs inventory, 14 Sep 2026: dead since about August 2026). Agent-facing docs that still pointed at Windows or the OptiPlex were not to stay on the hot path.

## Disk notes, already executed

These describe what was done on 2026-09-16. They are not instructions to repeat.

- `/mnt/Archives` was to keep the Litecoin datadir, SteamLibrary, and ollama-models.
- A docs-only pull landed under `ecosystem-history/references/`. That dump was not imported here.
- `/mnt/Projects` was reformatted after an inventory. The narrative's "live repos are `~/RootRecord/<name>`" line is **Historical**.

The narrative's closing live-code line (Ava-Core plus `~/.ollama/skills`, Media at `~/Media`) is **Historical**.
