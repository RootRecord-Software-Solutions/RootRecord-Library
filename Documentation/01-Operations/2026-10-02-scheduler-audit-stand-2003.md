# Stand — 2026-10-02 20:03 HST

**Superseded** by `2026-10-02-scheduler-audit-checkpoint-2025.md` (20:25 HST).

**Operator:** Alexander  
**Working surface:** `scheduler-functions-scratchpad.html` (114 catalog functions)  
**This page:** where the Pacific scheduler audit is, not a new policy.

Desktop copy (audit trail): `/home/rootrecord/Desktop/Manual Audit Documentation/09-stand-2026-10-02-2003.md`

---

## Desk / schedule

| Item | State at 20:03 |
|------|----------------|
| `polling-disconnected.json` | `armed: true`, `polling_disconnected: false` (written 19:37:41 HST). Recurring stay off. |
| `pacific.json` | Armed, not disconnected. 115 placements. **9 enabled**, all `phase: boot`. Everything else disabled. |
| `rr-rootserver-poller.service` | **enabled** (`default.target.wants` since 19:37). **inactive** — not started this session. Next user boot / start will run the 9 boot jobs. |
| Root Monitor Save | Still writes JSON only. Do not treat a Save as “start the poller.” |
| `RR_LOCAL_DATA_POLL` | Still `0` on the poller drop-in (ML2 owns gated data-poll jobs). |
| Tracked hosts | Live production `play.rootmc.net` and test ava-core (OptiPlex) only. Not dual Towny-vs-Claims. |

---

## Catalog / scratchpad counts (Pacific)

| Section | Count | Walk status |
|---------|-------|-------------|
| ON_BOOT | 8 | Signed enough to enable for next boot. `github_setup_remotes` off this list. |
| SERVICE | 1 | `ecoflow_ble_owner` — enabled on boot with the 8. |
| ENERGY | 2 | `delta2_read`, `river2pro_read` — not armed. Notes still mention once-at-start. |
| ONCE_AT_START | 0 | Section gone. `ecoflow_read_boot` deleted. |
| EVERY_SECONDS | 9 | Inventory done. Not armed. Tight cadences left as-is. |
| EVERY_MINUTE | 40 | 16 original clock desks + **24 moved** from seconds (20:03). Not armed. |
| EVERY_HOUR | 7 | Not walked. |
| ON_AT | 19 | Includes p2 `github_setup_remotes` (no clock). Not walked. |
| TIMER | 5 | Not armed. `rr-ecoflow-read.timer` still disabled. |
| BUILTIN | 1 | `ble_adapter_cycle`. Not walked. |
| POWER | 22 | Not walked. |

---

## Enabled for next poller start (boot only)

Runtime order is catalog `priority` (BLE owner defaults to 100):

1. `self_terminal` (p0)
2. `cloudflare_tunnel` (p1)
3. `ollama_warmup` (p3)
4. `flm_npu_warmup` (p4)
5. `council_relay` (p5)
6. `security_camera_server` (p6)
7. `security_timelapse_catchup` (p7)
8. `network_globe_hawaii` (p9)
9. `ecoflow_ble_owner` (SERVICE)

`github_setup_remotes` is **not** on boot. Function kept under ON_AT, disabled, no clock. Do not merge into `github_sync_all`.

---

## Signed deletions / renames this audit

| What | Decision |
|------|----------|
| Pacific `weather_poller` + launcher | Deleted. Hawaiʻi fetch is ML2 `weather_hawaii`. |
| `ecoflow_read_boot` | Deleted (jobs, catalog, schedule, overrides, night-sleep allow, scratchpad). Dual-read helper gone. |
| `ava_ecoflow_ble_owner` | Renamed to **`ecoflow_ble_owner`**. Script still `ble-owner.py`. Unit name unchanged. |

---

## EVERY_SECONDS left (9) — all disabled

| id | every_seconds | Note |
|----|---------------|------|
| `heartbeat` | 60 | Builtin ENERGY snapshot |
| `ecoflow_read_cycle` | 15 | Legacy leapfrog. Prefer ENERGY `delta2_read` / `river2pro_read` |
| `sys_stats_cycle` | 5 | Host CPU/mem |
| `github_sync_all` | 5 | **Too tight** — re-time before enable |
| `security_camera_frame_grab` | 1 | **Too tight** — re-time before enable |
| `system_uptime_log` | 60 | Not the builtin heartbeat |
| `discord_poller` | 60 | No token; keep off |
| `communications_slack` | 60 | Also in ML1 catalog |
| `status_snapshot` | 60 | Backup of TIMER `status_snapshot_timer` — do not enable both |

---

## Moved to EVERY_MINUTE at ~20:03 (24)

Round-up: interval `> 60` → next whole minute. Schedule still stores `every_seconds = minutes × 60` so they fire on that gap, not once per hour. Catalog `section` is `EVERY_MINUTE`. Scratchpad regrouped. `jobs.py` fallback intervals match (worklog 90 → 120); that file still lists them in its seconds block.

| min | ids |
|-----|-----|
| 2 | `worklog_scan`, `council_quake_telegram`, `ml2_datapack_pickup` |
| 5 | `service_supervisor`, `geology_collect`, `smart_devices_collect`, `system_python_drop`, `vercel_builds`, `council_health`, `inbox_drain`, `system_net_sample`, `public_health`, `note_work_draft`, `discord_report_relay` |
| 10 | `geology_kilauea_cams`, `weather_radar_zip` |
| 15 | `country_location_pollers`, `analytics_pull`, `voice_kilauea_image_check` |
| 30 | `stripe_poll`, `energy_river_car_drive` |
| 60 | `geology_kilauea_public_draft`, `earthquake_discord_post`, `kilauea_draft_count` |

Do not enable this whole block. Next walk is these minute rows (plus the 16 existing clock desks), then ENERGY / TIMER if pack reads are next.

---

## BLE side test (same evening, not schedule-armed)

- Adapter was rfkill soft-blocked; unblock then `bluetoothctl power on` works (first on can be Busy).
- `Energy/lib/adapter_on.py`: `ensure_adapter_on`, stale-lock drop, cycle, hci reset, recover (90 s cooldown `/tmp/ecoflow-adapter-recover`; skip NeedBind*).
- `ble_client._scan` calls `ensure_adapter_on`; `connect` recovers on scan miss / connect fail, not on NeedBind.
- Library `01-Operations/turn_ble_on.py` is a side-test wrapper (imports the Energy helper).
- Pack reads still need ENERGY / TIMER when Alexander says. Leapfrog timer remains disabled.

---

## Open, not this stand

- ML2 SSH stream: Desktop `07-ml2-ssh-stream-needs-work.md`
- `rr-ml2-db-tunnel` not a catalog boot job
- ENERGY / TIMER / POWER / EVERY_HOUR / ON_AT not walked
- Poller not started; boot jobs not live-verified this session
- Camera 1 s and GitHub 5 s must be re-timed before enable
- Optional: finish interrupted Modelfile / Desktop count drift; delete `turn_ble_on.py` if not wanted

---

## Resume here

1. Stay on the scratchpad HTML.
2. Walk **EVERY_MINUTE** (40), decide keep / skip / re-time. Do not mass-enable.
3. Then ENERGY + TIMER if repeating pack reads are next.
4. Start the poller only when Alexander says (unit is already enabled for next boot).
