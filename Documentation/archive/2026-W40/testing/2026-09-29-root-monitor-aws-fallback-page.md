# Test record: Root Monitor "AWS Fallback" page (per-function toggles, dry-run)

| Field | Value |
| --- | --- |
| **Date / time (HST)** | 2026-09-29 15:02–15:12 HST |
| **Tester** | Grok (executor) for Alexander Storey |
| **Change under test** | Pacific `Apps/Control-Panel`. New files: `rr_aws_page.py`, `Lib/rr_aws_fallback.py`, `Lib/rr_aws_fallback.json`. Edits: `rr_control_panel.py` (page registration + release on leave), `Lib/rr_settings.py` (`aws_fallback_mode` = `dry-run`, `aws_fallback_alias` = `rr-aws-ip`), `README.md`. `jobs.py` was **not** edited. [Proposal](../08-ideas/2026-09-29-aws-fallback-rebuild.md) |
| **State** | **PASS in dry-run.** Write mode **was not exercised**: the AWS flags dir doesn't exist yet, and the remote script would refuse with exit 3 |
| **Evidence** | screenshots in `/home/rootrecord/RootRecord-Ecosystem/test-reports/Control-Panel/aws-fallback-20260929/` (+ `shot-driver.py`) |
| **Commits** | Pacific + Library: desk auto-sync (see the worklog) |
| **Backup** | `/home/rootrecord/Database/GITHUB/aws-fallback-phase1.bak-20260929-150225/` (`rr_control_panel.py`, `rr_settings.py`, Control-Panel README, `settings.json`, the docs) |

## What was tested

- The page lists the 18 functions, grouped. Each row shows RAM, disk, network, fits and the default, with a switch.
- A budget box shows the enabled set against the ≥ 512 MB RAM and ≥ 1.5 GB disk floors, for t3.micro and 2 GB, plus the measured AWS values after a read.
- **Status** runs one read-only SSH call.
- A toggle opens a confirm dialog. In dry-run it writes nothing and reverts the switch.
- Widgets are built on visit and released on leave, with no timers.

## How (exact commands / procedure)

```bash
cd "Apps/Control-Panel"
python3 rr_control_panel.py --check                  # build every page, count errors/leaks
python3 Tests/test_settings_io.py                    # settings round-trip
python3 - <<'PY'   # rr_aws_fallback unit checks (13): load, budget micro/2GB, defaults,
                   # id regex rejects bad ids, write_script backs up before write, exit 3 if not deployed,
                   # status_argv read-only, parse_status
PY
# RSS A/B: --check with the page removed from PAGES vs with it (same session)
python3 /tmp/rr_aws_shot.py   # GTK driver: open page, press Status, toggle geology_current -> dialog, capture PNGs
```

## Results

| Check | Result |
| --- | --- |
| `--check` | 14 pages built, **0 errors, 0 leaks** |
| Memory | RSS 80.9 MB without the page vs **85.3 MB** with it (**+4.4 MB** with every page built). maxrss 86.9 → 91.5 MB. Window peak during the screenshot run was 102 MB (includes the texture captures) |
| `test_settings_io.py` | **103/103** |
| `rr_aws_fallback` unit checks | **13/13**. Default budget: t3.micro ~279 MB free (**below floor**, shown red); 2 GB ~1,419 MB free (OK). Bad ids are rejected; the backup comes before the write |
| Live read-only status | `deployed=0`, mem_total 908, avail 439, disk_free 3170 MB (read at 15:05:21 HST) |
| Screenshots | `20260929-150515-aws-fallback-01-dry-run.png` (dry-run banner + budget) · `…-02-after-status-read.png` (read in progress, "reading…") · `…-03-confirm-dialog.png` ("read 15:05:21 · deployed=0", measured budget line, dry-run confirm for disabling `geology_current`). Secret guard passed on all 3 |
| Dry-run safety | The dialog was not confirmed and `geology_current` stayed ON. **Nothing was written on AWS** |

## Verdict

**PASS (dry-run).** Switching `aws_fallback_mode` to `write` needs Alexander's sign-off and the Phase 2 runtime deploy (flags dir). Write mode should be re-tested then: toggle one function, check the dated `bin.bak-fallback-flags-*` backup and the flag content, then toggle it back.
