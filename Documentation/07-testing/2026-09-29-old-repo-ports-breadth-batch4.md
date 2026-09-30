# Test record — Old-repo ports, breadth batch 4 (web facts, live-wx, Hawaiʻi news, host net/security, solar / security / bandwidth desks)

| Field | Value |
| --- | --- |
| **Date / time (HST)** | 2026-09-29 13:58–14:09 HST |
| **Tester** | Grok Bot (desk agent, old-repo migration pass; breadth-over-depth steering 13:53) |
| **Change under test** | G1 `websites/web-facts` → Pacific `Communications/web-facts/scripts/web_facts.py`; G1 `weather/live-wx` → `Communications/live-wx/scripts/live_wx.py`; G0 `operations/news/{_collector,hawaii/news}.py` → `Reports/News/scripts/{_collector,hawaii_news}.py`; G1 `host-metrics` (net + security parts) → `System/scripts/host_desks.py`; G1 `hourly-clip-reports` solar / security / bandwidth desks → `Media/Voice/scripts/voice_reports.py solar_desk | security_desk | bandwidth_desk`. Database `.gitignore` += `/Reports/News/**/*.db*`, `/System/network/Daily/`. [Matrix](../00-architecture/Old-Repo-Migration-Matrix.md) |
| **State** | **PASS** web facts, live-wx, host desks, three voice desks (text) · **FAIL on content** Hawaiʻi news (rc 0, 0 posts) · WAV renders **VERIFY PENDING** (no model load) · jobs **PROPOSED, not registered** (standing rule: no jobs.py edits) — blocks in [Pending-Job-Registrations-2026-09-29](../00-architecture/Pending-Job-Registrations-2026-09-29.md) |
| **Backup** | `/home/rootrecord/Database/GITHUB/migration-breadth.bak-20260929-135720/` |
| **Commits** | Auto-sync; see worklog / final report |

## Light smoke (one run each, nice 10, temp roots — nothing written to the real Database except where noted)

```bash
cd "/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server"
nice -n 10 python3 Communications/web-facts/scripts/web_facts.py https://earthquake.usgs.gov/fdsnws/event/1/version
nice -n 10 python3 Communications/web-facts/scripts/web_facts.py https://example.com/ ; nice -n 10 python3 Communications/web-facts/scripts/web_facts.py http://api.weather.gov/
nice -n 10 python3 Communications/live-wx/scripts/live_wx.py --offline ; nice -n 10 python3 Communications/live-wx/scripts/live_wx.py   # read-only, writes nothing
RR_DATABASE_ROOT=/tmp/rr-migr/newsdb nice -n 10 python3 Reports/News/scripts/hawaii_news.py
RR_DATABASE_ROOT=/tmp/rr-migr/hostdb nice -n 10 python3 System/scripts/host_desks.py net-sample   # + a simulated older sample for the 1 h window
RR_DATABASE_ROOT=/tmp/rr-migr/hostdb nice -n 10 python3 System/scripts/host_desks.py net-usage
RR_DATABASE_ROOT=/tmp/rr-migr/hostdb nice -n 10 python3 System/scripts/host_desks.py security
RR_VOICE_REPORT_OUT=/tmp/rr-migr/voice-test nice -n 10 python3 Media/Voice/scripts/voice_reports.py solar_desk --no-voice
RR_VOICE_REPORT_OUT=/tmp/rr-migr/voice-test nice -n 10 python3 Media/Voice/scripts/voice_reports.py security_desk --no-voice
RR_VOICE_REPORT_OUT=/tmp/rr-migr/voice-test RR_VOICE_BANDWIDTH_DRY=1 nice -n 10 python3 Media/Voice/scripts/voice_reports.py bandwidth_desk --no-voice
```

## Results

| Item | Result | Observed |
| --- | --- | --- |
| `web_facts.py` | **PASS** | USGS FDSN version → `2.7.0`; `example.com` refused (not allowlisted); `http://` refused; no args → rc 2 usage |
| `live_wx.py` | **PASS** | `--offline` 0.12 s / 26 MB: forecast DOWN (by design), "HI alerts: High Surf Advisory (Big Island in area)", "Hurricane Nolo, 270 nm from Līhuʻe"; live 2.07 s / 29 MB: "This Afternoon, 78F, Isolated Rain Showers, wind 12 mph" + Tonight + Wednesday |
| `hawaii_news.py` | **FAIL on content** (rc 0) | 12.3 s, ~31 MB RSS; 13 feeds + 12 pages checked, 25 × HTTP 404 (`source_health error 25`), 0 posts / 0 events; `hawaii-news-last.json` + `hawaii_news.db` written to the temp root only. `https://governor.hawaii.gov/feed/` answers 200 (not in the G0 discovery path) |
| `host_desks.py net-sample / net-usage` | **PASS** | iface `wlo1`; simulated 1 h window 56.7 MB total; files `System/network/net-last.json` + `Daily/net-YYYYMMDD.jsonl` (temp root) |
| `host_desks.py security` | **PASS** | counts only: failed sign-ins 1 h 0 / 24 h 1, 10 listeners, 15 established, ufw start-on-boot false, ssh active; no IPs / usernames / log lines stored |
| `solar_desk` (Bruce) | **PASS (text)** | "Delta 2: state of charge 46%, solar input 179 watts, AC out 71 watts. River 2 Pro: state of charge 100%, solar input 0.0 watts, AC out 0.0 watts. Sunrise was 06:11, sunset is 18:10." |
| `security_desk` (Carly) | **PASS (text)** | firewall / sshd / sign-in counts from the live snapshot builder |
| `bandwidth_desk` (Carly) | **PASS (text)** | real Database: "not on file yet" (no samples, sampler job not registered); temp root: MB figures |
| Resources | OK | MemAvailable ≈ 6.6–6.9 GB throughout; RSS 20–31 MB per run; no model loads, no playback, no sends |

## Check later (Alexander)

**web_facts.py**
- [ ] Decide whether to wire it into council chat (relay replies are BLOCKED on the `*-telegram` models).
- [ ] Review the allowlist (`HOSTS`, copied from G1: NWS, USGS, Wikipedia, Litecoin docs) and the 8 000-char cap.

**live_wx.py**
- [ ] The G1 point (19.5429, −155.0372) is kept: is that the right forecast point for the desk?
- [ ] Hurricane line uses only storms polled within 6 h (`HUR_ACTIVE_H`). The G1 "West of Kauaʻi is Asia/Japan" phrase for storms ≥ 800 nm was dropped: re-add it?
- [ ] Wire it into council chat once relay replies are unblocked.

**hawaii_news.py / _collector.py**
- [ ] Pick seed feeds (e.g. `governor.hawaii.gov/feed/`, department feeds). G0 discovery from `www.hawaii.gov` finds only 404s.
- [ ] Confirm the target (`Database Reports/News/hawaii/`, DB git-ignored, only the summary JSON tracked).
- [ ] Register `reports_hawaii_news` (`RR_HAWAII_NEWS`, ON_AT 10:00) only after it returns posts.
- [ ] Check the crawl caps (`RR_NEWS_MAX_*`) and the 10 s timeout cap against a full run (G0 defaults are 40 feeds / 12 pages / 8 sitemaps / 80 articles).

**host_desks.py**
- [ ] Register `system_net_sample` (`RR_NET_SAMPLES`, 300 s), then confirm after 1 h / 24 h that `net-usage` returns non-None windows.
- [ ] Check the Daily JSONL growth (about 290 lines a day; never deleted, git-ignored).
- [ ] Read-only `/var/log/auth.log` needs the `adm` group. Check the counts match `journalctl -u ssh` on a day with failures.
- [ ] Decide whether `security-last.json` (counts only) should be tracked in git.
- [ ] `ufw_boot false`: is that expected on this desk?

**Voice desks**
- [ ] Render WAVs (Bruce / Carly) once model loads are allowed; they are VERIFY PENDING.
- [ ] Clock helper said "two one p.m." at 14:01. It should say "two oh one". This is a shared helper, so check `hourly_chime` too.
- [ ] "0.0 watts" wording: round to "0 watts" or say "no solar input".
- [ ] "Sunrise was 06:11" is spoken with digits. Check the live-facts gate and TTS reading (G1 spelled the times out).
- [ ] Register `voice_solar_desk` (:04), `voice_security_desk` (:11), `voice_bandwidth_desk` (:12). The bandwidth desk needs the net sampler first.
- [ ] Delivery (speakers / Telegram) stays OFF, pending sign-off.

## Not done / BLOCKED

- Council health (G1 `council/council-health`): needs the three bot tokens for `getMe`, a live chat probe (model load) and alert sends to the council group. Needs sign-off. Bruce stats (WO-MIG-26, 2026-09-30): dry-run from live host and EcoFlow last files; job `bruce_stats_posts` gated `RR_BRUCE_STATS`; Telegram send stays off until `RR_BRUCE_STATS_SEND=1`.
- Load categories: needs a G1 cloud-quota → G3 last-file field map and a threshold check.

- 49 other state + global news builders: product / website data, out of Pacific scope.
- G1 host series-reset and wattage helpers; Windows PDH GPU/NPU counters (not applicable on Linux).
- official-weather-media: HLS / HWO are not collected by G3 weather (a weather-poller change in another domain), and there is no OBS.

## Update, 14:16–14:40 HST (breadth pass 2)

See [breadth batch 5](./2026-09-29-old-repo-ports-breadth-batch5.md).

- Hawaiʻi news is now **PASS**: 16 seed feeds give 278 posts. The FAIL above stands as the 14:05 result.
- The three voice check-later items are fixed (clock "two oh one", watts words / idle, spoken sun times).
- Load categories is ported with a G3 field adapter.
- **Correction:** the G3 weather poller already collects HWO. Only HLS was missing, and `Weather/scripts/official_statement.py` now fetches it.
