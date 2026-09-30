# 08 — Ideas and Feature Proposals

This folder holds ideas and feature proposals for the RootRecord ecosystem. It uses the same convention as [07-testing](../07-testing/README.md): one file per item, `YYYY-MM-DD-<slug>.md`, created from [TEMPLATE.md](./TEMPLATE.md).

**Every item here is PROPOSED.** Nothing in this folder authorizes a code, service, model, hardware or data change.
Items Alexander approved show their current state in the index. Four were approved 2026-09-29 and landed ~04:00–04:07 HST (Weather repo excluded).
- An item only moves forward after Alexander signs off. It is then carried out through a work order (`Documentation/06-development/Work-Orders/`) and tested with a record in `07-testing/`.
- Each proposal must name its grounding: the evidence file, test record or open item it comes from.
- Standing rules still apply: no resident models, light tests, G2/legacy files are KEPT unless Alexander signs off, and no secrets.

**Status vocabulary:** LANDED · VERIFY PENDING · PASS · FAIL · BLOCKED · RETIRED · PROPOSED · KEPT.

## Index

| Date | Proposal | State | Grounding |
| --- | --- | --- | --- |
| 2026-09-29 | [Auto-recovery for weather and relay after a mid-session crash](./2026-09-29-weather-relay-auto-recovery.md) | LANDED / VERIFY PENDING (next poller start) — Pacific `5353e1f`, `52573e7` | follow-ups evidence 02:50 HST: both are ON_BOOT only |
| 2026-09-29 | [Pacific copy of `npu-status.sh`](./2026-09-29-npu-status-pacific-copy.md) | LANDED / VERIFY PENDING (idle run PASS) — Pacific `5353e1f` | NPU/FLM evidence: G2-only script |
| 2026-09-29 | [AI processing log and daily report](./2026-09-29-ai-processing-log-and-report.md) | PROPOSED | NPU on-demand test; FLM log privacy finding |
| 2026-09-29 | [Restore voice reports](./2026-09-29-restore-voice-reports.md) | PROPOSED | G0/G1 voice packets; WO-RPT-001 |
| 2026-09-29 | [Relay quiet mode without losing messages](./2026-09-29-relay-quiet-mode-message-hold.md) | LANDED / VERIFY PENDING (next poller start) — Pacific `5353e1f`, `52573e7`; Database `57172d0` | relay quiet-mode caveat |
| 2026-09-29 | [Weather retention and a Weather repo](./2026-09-29-weather-retention-and-repo.md) | Retention LANDED / VERIFY PENDING (dry-run only; job disabled) — Pacific `52573e7`, Database `a775c2f` · Repo PROPOSED | Pacific `Weather/README.md` §Retention (PROPOSED) |
| 2026-09-29 | [AI specialist models and keyword router](./2026-09-29-ai-specialist-models-and-routing.md) | LANDED / gated: 10 `rr-*` specialists + 3 restored `*-telegram` built (disk only), router v2 + tests landed; `run-infer.sh` hook LANDED 04:56, OFF unless `RR_SPECIALIST_ROUTING=1` | operator request; team constitution §3; missing `*-telegram` models |
| 2026-09-29 | [Smart-plug load shedding and light dimming on low battery SOC](./2026-09-29-smart-plug-load-shedding.md) | PROPOSED | Smart-Devices foundation (plugs BLOCKED on `local_key`) |
| 2026-09-29 | [AWS US-Mainland node: stabilise, then health + hazard continuity mirror](./2026-09-29-aws-mainland-improvement-plan.md) | PROPOSED (P0 disk fix urgent) → P0-1 disk trim + P0-4 tunnel **LANDED / PASS** 14:07–14:15 HST ([record](../07-testing/2026-09-29-aws-hawaii-trim-and-cloudflared.md)) | read-only SSH 13:49 HST: `hawaii.ndjson` 1.82 GB, 1.6 GB free, trim script missing |
| 2026-09-29 | [Globe landing overlay for www.rootrecord.cloud (sign-up / home / status glass cards, rail)](./2026-09-29-globe-landing-overlay.md) | LANDED in Mainland checkout (uncommitted) · preview PASS · AWS deploy PROPOSED (sign-off) → **AWS deploy LANDED 16:10 HST** (v2 + AWS Ohio node 16:16, [record](../07-testing/2026-09-29-globe-overlay-aws-deploy.md)); real-browser check VERIFY PENDING | design brief from Alexander; [test record](../07-testing/2026-09-29-globe-landing-overlay-preview.md) |
| 2026-09-29 | [AWS as a small fallback node: rebuild, per-function toggles, buffer-to-relay catch-up](./2026-09-29-aws-fallback-rebuild.md) | **Phase 2 LANDED** (trimmed-micro on t3.micro, 16:03 HST) · Root Monitor write mode · pending: :8787, telegram_hold/basic_replies, relay_send, .env trim, 2 desk jobs, globe poll | Alexander's direction 14:57 HST; [inventory](../07-testing/2026-09-29-aws-fallback-inventory.md) (908 MB RAM, not 2 GB) |

*Folder created 2026-09-29 ~03:48 HST (docs only).*
