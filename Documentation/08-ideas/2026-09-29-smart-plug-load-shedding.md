# Proposal — Smart-plug load shedding and light dimming on low battery SOC

| Field | Value |
| --- | --- |
| **Date (HST)** | 2026-09-29 |
| **Proposed by** | Grok (executor, smart-devices pass) |
| **State** | PROPOSED |
| **Grounding** | [Smart-Devices-Energy](../00-architecture/Smart-Devices-Energy.md); test record [2026-09-29-smart-devices-foundation](../07-testing/2026-09-29-smart-devices-foundation.md); Database `Energy/soc/{delta2,river2pro}-last.json` (e.g. Delta 2 41.57 % at 13:17 HST) |
| **Needs sign-off from** | Alexander |
| **Related WO** | none yet |

## Problem (measured)

The desk runs on EcoFlow packs. SOC is already measured (BLE → `Energy/soc/*-last.json`), but nothing reduces load when SOC falls; non-essential loads (lamps, fans, chargers) keep draining the packs overnight.

## Proposal

A small rule engine `Energy/Smart-Devices/scripts/load_shed.py`, run by the poller only when a second gate `RR_SMART_DEVICES_SHED=1` is set (on top of `RR_SMART_DEVICES=1`):

| Rule (example thresholds — Alexander sets real ones) | Action |
| --- | --- |
| lowest pack SOC < 30 % and no solar input | WiZ bulbs → dim to 30 %, warm 2700 K |
| SOC < 20 % | BSD01 plugs tagged `shed: true` in `tuya-devices.local.json` → OFF |
| SOC recovers > 40 % (hysteresis) for 10 min | restore saved states (the `wiz.restore()` / saved plug state) |
| data stale (> 10 min) or any read FAIL | **do nothing** (fail-safe = no switching) |

Every action writes `Energy/Smart-Devices/actions-last.json` + a daily `.jsonl`, so Root Monitor and voice reports can say what was shed and why.

## Scope and non-goals

- In: plugs Alexander explicitly tags `shed: true`; bulbs he tags `dim_on_low: true`.
- Out: anything that powers the desk, router, Starlink, cameras, or the EcoFlow units themselves; any cloud control; any BLE use (ble-owner.py keeps the adapter).
- Out until Path A/B is chosen for the plugs (see architecture doc).

## Resource impact / safety

Stdlib + one short tinytuya subprocess per switched plug; < 1 s CPU per run, no resident process, no models. Max one switch per device per 10 min (anti-flap). Default fail-safe: no data → no action. Manual override file `config/shed-override.json` (`{"hold_until": "..."}`) pauses all rules.

## How it would be tested

One light test per rule with a fake SOC file (`RR_SMART_DEVICES_SOC_OVERRIDE=<path>`), `--dry-run` first (prints intended actions only), then one real cycle on one tagged plug with Alexander present. Pass = action logged, state restored after hysteresis, no other device touched.

## Open questions

- Which loads are on the BSD01 plugs, and which are safe to shed?
- Thresholds per pack (Delta 2 B2/B3 vs River 2 Pro) and whether solar input (watts) should suppress shedding.
- Voice/Telegram notification when shedding happens (would need Communications notify policy sign-off).
