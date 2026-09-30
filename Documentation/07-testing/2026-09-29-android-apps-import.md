# Test record: Android apps import into `6 - Android Development`

| Field | Value |
| --- | --- |
| **Date / time (HST)** | 2026-09-29 14:19–14:50 HST |
| **Tester** | Grok Bot (executor subagent) for Alexander |
| **Change under test** | Copy the latest source, signing files and newest release artifact of every RootRecord Android app into `6 - Android Development/<App>/`, with the fragile 2 TB drive read-only. [Inventory](../00-architecture/Android-Apps-Inventory.md) |
| **State** | **PASS** (copy integrity, secrets 0600 + ignored, drive clean) · build **VERIFY PENDING** (not attempted: no SDK/Java on the desk) |
| **Evidence** | This record + [Android-Apps-Inventory](../00-architecture/Android-Apps-Inventory.md). Scratch listings in `/tmp/android-inv/` (tmpfs, not kept) |
| **Commits** | Library `1e85c1e` (inventory, this record, 07 README row; auto `desk sync` 14:41 HST) · Library `7ab947f` (worklog section; auto `desk sync` 14:45 HST). Both checked with `git log`. No manual git writes. Target folder has no repo |
| **Backup** | `/home/rootrecord/Database/GITHUB/android-import.bak-20260929-143931/` (07 README + overnight worklog before edit). Target was empty before the copy (created 14:12, 0 entries) |

## What was tested

1. The 2 TB drive: identification, read-only inventory, kernel health during reads.
2. Copy integrity for 9 apps (source trees, Web-Source trees and Releases).
3. Secret handling: mode 0600 and git-ignore coverage.
4. Git and auto-sync exposure of the target folder.

## How (exact commands / procedure)

```bash
lsblk -o NAME,SIZE,FSTYPE,LABEL,MOUNTPOINT          # sda1 1.8T ntfs → /run/media/rootrecord/6CD8FA150F0B0035 (udisks auto-mount, ntfs3)
journalctl -k --since today | grep -iE 'sda|ntfs|I/O|reset|disconnect'   # dmesg not readable (EPERM)
nice -n10 ionice -c3 find "$M" \( -name node_modules -o -name .cache … -prune \) -o \( -name build.gradle* -o -name settings.gradle* -o -name AndroidManifest.xml -o -name gradlew -o -iname '*.apk' -o -iname '*.aab' … \) -print
nice -n10 ionice -c3 rsync -a --chmod=Do-w,Fo-w --ignore-existing --info=progress2 \
  --exclude=build/ --exclude=.gradle/ --exclude=.idea/ --exclude=.cxx/ --exclude=node_modules/ --exclude=__pycache__/ \
  --exclude=builds/ --exclude=release/ --exclude='*.apk' --exclude='*.aab' --exclude='*.exe' --exclude='*.mp4' SRC/ "6 - Android Development/<App>/"
rsync -a --open-noatime … "$M/Send to External drive/…/RootRecord-RootMC-1.0.32.aab" RootMC-Android/Releases/   # only file read from the drive
rsync -anc --itemize-changes <same excludes> SRC/ DST/ | grep -c '^>f'     # checksum compare, expect 0
git --git-dir=/tmp/android-inv/ignorecheck.git --work-tree="6 - Android Development" check-ignore --stdin < secret+artifact list
find . -type f \( -iname '*.jks' -o -name local.properties -o … \) ! -perm 600 | wc -l
```

## Pass criteria (written before running)

1. No kernel I/O error, reset or disconnect for `sda` during the pass. No write, remount, fsck, chkdsk or ntfsfix on the drive.
2. For every app, destination file count and bytes equal the source after exclusions, and the checksum dry-run shows 0 differences.
3. Every keystore, `keystore.properties`, `local.properties`, `google-services.json`, recovery-code and test-credential file is 0600 and git-ignored, and `*.apk`/`*.aab` are ignored.
4. Total size stays under the 40 GB budget. Internal disk stays above 50 GB free.
5. Nothing is written inside `Desktop/old txt` or `I'll sort these models tomorrow`. Both were pruned from every `find`.

## Result

| Check | Result |
| --- | --- |
| Drive | `/dev/sda1` 1.8 T NTFS (WD20EARZ, MAYA USB enclosure), attached 14:19:21, **clean mount**: none of the "volume is dirty" lines the 03:50–03:55 128 GB JMicron drive logged. 0 I/O errors, resets or disconnects 14:19–14:50. It was already auto-mounted `rw` by udisks; it wasn't remounted and nothing was written (reads only, `--open-noatime` for the one file copied) | **PASS** |
| Kilauea-App | 128/128 files, 1,861,143 B, 0 diffs; Releases 1 APK | **PASS** |
| Weather-Manager | 119/119, 5,399,940 B, 0 diffs; Web-Source 48 files 0 diffs; Releases 1 APK + 1 AAB (APK sha256 matches the git blob) | **PASS** |
| RootMC-Android | 193/193, 2,933,784 B, 0 diffs; AAB from drive sha256 `3b4b0a23…` = desk copy; APK `dd13afd2…` = both desk copies | **PASS** |
| Ava-Ops | 41/41, 249,286 B, 0 diffs; Releases 1 debug APK | **PASS** |
| Business-Manager | 73/73, 1,182,351 B, 0 diffs; Web-Source 48 files 0 diffs; Releases 1 debug APK | **PASS** |
| Root-Goals / Root-Farms / Token-Manager / Account-Hub | 60/60, 67/67, 66/66, 61/61 files, 0 diffs; Web-Source 27/17/43/33 files, 0 diffs | **PASS** |
| Secrets | 17 files, 17 at 0600 (`keystore/` dirs 0700); 24/24 secret + artifact paths `check-ignore`d; 0 world-writable files | **PASS** |
| Git / sync | target is not a repo; not in either `repos.conf`, `Push.sh` or `Pull.sh` | **PASS** (no exposure) |
| Size | **80.7 MB**, 1,033 files (budget 40 GB). Internal disk 193 GB free after | **PASS** |
| Build | not attempted: no Android SDK, Studio, Java or `~/.gradle` on the desk | **VERIFY PENDING** |

## Resource impact

| When | Load (1/5/15) | MemAvailable | Swap used | Peak RSS |
| --- | --- | --- | --- | --- |
| before (14:19) | not recorded | 6.7 GiB | 533 MiB | not recorded |
| during (14:33, monorepo clone) | not recorded | 6,666 MiB | not recorded | not recorded |
| after (14:39) | 1.98 / 1.63 / 1.63 | 6,609 MiB | 679 MiB | not recorded |

## Cleanup confirmation

- [x] no test process left (every `rsync`/`find`/`git clone` finished in the foreground)
- [x] no ports, locks or models used
- [ ] staging clones **left in place on purpose** (the "never delete" rule): `/home/rootrecord/.cache/rr-android-import-20260929/` (594 MB) and `/tmp/android-inv/` (tmpfs, ≈ 93 MB + listings). Alexander to remove when satisfied

## Open items / caveats

- The drive held no usable Android source (0-byte symlink remnants only). The source came from the desk `~/old ollama/` G2 backup and from GitHub mirrors, and only the RootMC 1.0.32 AAB came from the drive. See the inventory for the full reasoning.
- Weather Manager: the source is 1.0.46, but the newest artifact found is older (v1.0.9 AAB, plus a 2026-05-02 APK). Business Manager: the source is 1.0.42 and only a 2026-04-29 debug APK was found.
- `udisks` auto-mounted the drive `rw` with `relatime`. Reads can still update NTFS access times. This pass didn't remount it; if the drive is to stay attached, remounting `ro` needs Alexander.
- Capacitor `webDir` still points to the monorepo layout (`../../Web/apps/<app>-web/build`) and was left unedited.
