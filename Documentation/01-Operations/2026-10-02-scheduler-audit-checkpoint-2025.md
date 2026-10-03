# Checkpoint — Pacific scheduler audit — 2026-10-02 20:25 HST

**Operator:** Alexander  
**Purpose:** Freeze the stand before restructuring EVERY_MINUTE / schedule functions. Not a new policy. Not a live-verify of boot.

**Working surface:** `scheduler-functions-scratchpad.html` (113 catalog functions). Alexander also saved the EVERY_MINUTE list as local text in docs.

**Desktop copy:** `/home/rootrecord/Desktop/Manual Audit Documentation/10-checkpoint-2026-10-02-2025.md`

**Prior stand:** `2026-10-02-scheduler-audit-stand-2003.md` (superseded by this page).

---

## Desk / schedule (measured 20:25)

| Item | State |
|------|--------|
| `polling-disconnected.json` | `armed: true`, `polling_disconnected: false` (stamp 19:37:41 HST). Recurring stay off. |
| `pacific.json` | Armed, not disconnected. **114 placements**. **9 enabled**, all `phase: boot`. |
| Catalog | **113** functions (`catalog-pacific.json`) |
| `rr-rootserver-poller.service` | **enabled**, **inactive**. Symlink in `default.target.wants` since 19:37. |
| Unit wait | `ExecStartPre` sleeps until the next `:00` (skip if already second 0). `TimeoutStartSec=120`. **`daemon-reload` before the next start.** |
| Root Monitor Save | Writes JSON only. Does not start the poller. |
| `RR_LOCAL_DATA_POLL` | `0` on the poller drop-in. ML2 owns gated data-poll jobs. |
| Tracked hosts | `play.rootmc.net` + test ava-core (OptiPlex) only. |

Schedule JSON is timing authority when armed. `jobs.py` lists are fallback only; several moved jobs still sit in the `EVERY_SECONDS` Python list even though the catalog section is `EVERY_MINUTE`.

---

## Catalog counts

| Section | Count | Walk |
|---------|-------|------|
| ON_BOOT | 8 | Enabled for next poller start (with SERVICE). |
| SERVICE | 1 | `ecoflow_ble_owner` on boot. |
| ENERGY | 2 | Not armed. |
| ONCE_AT_START | 0 | Gone. |
| EVERY_SECONDS | 3 | Camera re-timed. Dual-read job deleted. Not armed. |
| EVERY_MINUTE | 45 | Inventory listed. **Next restructure.** Not armed. |
| EVERY_HOUR | 7 | Not walked. |
| ON_AT | 19 | Includes `github_setup_remotes` (no clock). Not walked. |
| TIMER | 5 | Not armed. `rr-ecoflow-read.timer` still disabled. |
| BUILTIN | 1 | Not walked. |
| POWER | 22 | Not walked. |

---

## Signed this audit (do not reverse without Alexander)

| When (HST) | Decision |
|------------|----------|
| ~18:40 | Pacific `weather_poller` + launcher deleted. Hawaiʻi fetch is ML2. |
| ~19:33 | `github_setup_remotes` skip boot; keep function; rare ON_AT; do not merge into `github_sync_all`. |
| ~19:35 | `ava_ecoflow_ble_owner` → `ecoflow_ble_owner`. Script still `ble-owner.py`. |
| ~19:37 | Nine boot placements enabled; schedule armed; disconnect cleared; poller unit enabled, not started. |
| ~19:40–19:44 | ONCE_AT_START skipped; `ecoflow_read_boot` deleted. Keep `delta2_read` / `river2pro_read`. |
| ~20:03 | Intervals `> 60s` moved to EVERY_MINUTE, rounded up to the next minute. |
| ~20:07 | Exact **60s** jobs treated as **1 min** and moved. |
| ~20:08 | Unit wait-until-next-minute. `jobs.py` EVERY_SECONDS note: **59s or less**. |
| ~20:20 | `ecoflow_read_cycle` **deleted** (nothing else called that job id). `leapfrog-read.sh` + timer remain. |
| ~20:20 | `security_camera_frame_grab` **10s**. |

---

## Enabled for next poller start (boot only)

After the minute-align wait, `boot_jobs()` in priority order:

1. `self_terminal` (p0)
2. `cloudflare_tunnel` (p1)
3. `ollama_warmup` (p3)
4. `flm_npu_warmup` (p4)
5. `council_relay` (p5)
6. `security_camera_server` (p6)
7. `security_timelapse_catchup` (p7)
8. `network_globe_hawaii` (p9)
9. `ecoflow_ble_owner` (SERVICE, default priority 100)

Not live-verified this session (poller never started).

---

## EVERY_SECONDS left (3) — all disabled

Rule: this section is **59s or less**.

| id | every_seconds | Function |
|----|---------------|----------|
| `sys_stats_cycle` | 5 | Host CPU / load / mem → Database/SYSTEM. |
| `github_sync_all` | 5 | Sync all `repos.conf` rows (pull/merge/push). **Still tight.** |
| `security_camera_frame_grab` | 10 | Grab ch1–4 stills → Database `Media/Images/`. |

---

## EVERY_MINUTE (45) — all disabled — next restructure

29 were **moved** from seconds. 16 were already minute/clock.

### Moved — 1 min (`every_seconds` 60)

- **`heartbeat`** — ENERGY snapshot once per minute.
- **`system_uptime_log`** — Desk uptime / offline / morning-return samples → System/uptime/.
- **`discord_poller`** — Discord poller. No token, no post.
- **`communications_slack`** — Slack poller → slack-last.json. No HTTP/post until token + sign-off.
- **`status_snapshot`** — Backup public status write. TIMER publishes every 30s — do not enable both.

### Moved — 2 min

- **`worklog_scan`** — Offline work auto-doc → WORKLOG.
- **`council_quake_telegram`** — Carly per-quake from hawaii-last.json. Dry-run unless `RR_COUNCIL_QUAKE_SEND=1`.
- **`ml2_datapack_pickup`** — Drain ML2 Telegram offline datapacks into Database.

### Moved — 5 min

- **`service_supervisor`** — Respawn council relay if dead (max 3 / 30 min). Weather is ML2.
- **`geology_collect`** — USGS Hawaii + global quakes and HVO → Geology.
- **`smart_devices_collect`** — WiZ / Tuya read-only.
- **`system_python_drop`** — Allowlisted PythonDrop; empty catalog = no-op.
- **`vercel_builds`** — Redacted failed builds. No token = no API.
- **`council_health`** — Relay / getMe / 409 tail. No send.
- **`inbox_drain`** — Quiet inbox → feedback.jsonl. No D1 / no send.
- **`system_net_sample`** — Default-route iface bytes.
- **`public_health`** — Origin radio + :8787. Does not start origin.
- **`note_work_draft`** — Voice note → work-order draft. No execute.
- **`discord_report_relay`** — Post changed automated reports. Chat poller off.

### Moved — 10 min

- **`geology_kilauea_cams`** — HVO V1/V2/V3 stills.
- **`weather_radar_zip`** — Append HAWAII_loop GIFs into radar_archive.zip.

### Moved — 15 min

- **`country_location_pollers`** — Open-Meteo allowlist. Gate unset.
- **`analytics_pull`** — Mirror ML2 `/api/analytics/daily`. No send.
- **`voice_kilauea_image_check`** — Carly Gemma look. Voice if `RR_VOICE_DELIVER=1`.

### Moved — 30 min

- **`stripe_poll`** — Stripe snapshot. No key = no API.
- **`energy_river_car_drive`** — River car DC tick. Does not switch power.

### Moved — 60 min

- **`geology_kilauea_public_draft`** — Queue draft on HVO change. No send.
- **`earthquake_discord_post`** — Quake last-files → Discord pipe. Dry-run unless send sign-off.
- **`kilauea_draft_count`** — Count queued drafts. Does not publish.

### Already on minutes — every 1 min

- **`ensure_tunnel_online`** — Start Cloudflare if internet up and tunnel down.
- **`live_picture`** — Overlay live desk numbers; copy mainland thumb.
- **`reports_pipeline_tick`** — News-select windows + stream queue. No render / YouTube.

### Already on minutes — clock

- **`radio_rss_poll`** — :05 — RSS into Radio story queue.
- **`voice_timing_report`** — :05 — Rewrite voice-timing.md from the automations log.
- **`radio_news_update`** — :08 — Hourly news (two parts).
- **`voice_hourly_chime`** — :00 and :30 (schedule row currently shows :30) — prebuilt chime.
- **`voice_system_perf`** — :45 — Bruce system.
- **`voice_nws_weather`** — :45 — Ava NWS Hawaii.
- **`voice_remaining_tasks`** — :45 — Bruce remaining tasks.
- **`voice_earthquake_report`** — :45 — Carly USGS.
- **`voice_kilauea_report`** — :45 — Carly HVO.
- **`voice_solar_desk`** — :45 — Bruce packs / sun / ch1.
- **`voice_security_desk`** — :45 — Carly security.
- **`voice_bandwidth_desk`** — :45 — Carly bandwidth (needs net samples).
- **`voice_current_report`** — :45 — Full current report after the other desks.

Cadence for moved rows is still stored as `every_seconds = minutes × 60` so they fire on that gap, not as a single clock minute.

---

## Not walked (after minute restructure)

**ENERGY (2):** `delta2_read`, `river2pro_read` — keep; not armed.

**EVERY_HOUR (7):** `energy_sun_times`, `energy_moon_phase`, `weather_us_states`, `ai_processing_report_hourly`, `ai_usage_report`, `automations_log_hourly_archive`, `security_timelapse_hourly_compile`.

**ON_AT (19):** `github_setup_remotes` (p2, no clock), `security_timelapse_daily_render`, `reports_daily_roll_up`, `reports_weekly_archive`, `weather_retention`, `log_retention`, `path_index`, `template_reports_daily`, `voice_hurricane_desk`, `media_hurricane_radio`, `bruce_stats_posts`, `adsense_eod`, `admob_eod`, `overnight_relay`, `api_prices`, `cursor_fallback`, `reports_board_catchup`, `discord_report_8h`, `discord_report_24h`.

**TIMER (5):** `ecoflow_leapfrog_read` (legacy), `delta2_ac_force`, `river2pro_ac_recover`, `ml2_globe_state_push`, `status_snapshot_timer`.

**BUILTIN (1):** `ble_adapter_cycle`.

**POWER (22):** Delta 2 / River 2 Pro on-off pairs (was power-automations).

---

## BLE / Energy (side work, not schedule-armed)

- Adapter was rfkill soft-blocked; unblock then power on (first on can be Busy).
- `Energy/lib/adapter_on.py` — ensure on, drop stale lock, cycle, hci reset, recover (90s cooldown `/tmp/ecoflow-adapter-recover`; skip NeedBind*).
- `ble_client._scan` / `connect` use that path.
- Library `turn_ble_on.py` is a side-test wrapper.
- Standing read rule: `2026-10-01-ecoflow-ble-reads.md`. Repeating read = user timer / pack ENERGY jobs, not a deleted poller dual-read.

---

## Open / do not do until Alexander says

- Start the poller (unit is enabled). Reload user systemd first so `ExecStartPre` is live.
- Mass-enable EVERY_MINUTE or remaining seconds.
- Arm ENERGY / TIMER / POWER.
- Enable both `status_snapshot` and `status_snapshot_timer`.
- Re-add `weather_poller`, `ecoflow_read_boot`, or `ecoflow_read_cycle`.
- ML2 SSH stream (Desktop `07-ml2-ssh-stream-needs-work.md`).
- Optional: delete `turn_ble_on.py`; finish interrupted Modelfile / inventory drift.

---

## Resume

1. Restructure EVERY_MINUTE (45) from this checkpoint + Alexander’s saved text list.
2. Then ENERGY + TIMER if pack reads are next.
3. Then hour / ON_AT / POWER.
4. Start poller only on explicit ask.
