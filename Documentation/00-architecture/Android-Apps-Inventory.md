# Android Apps Inventory (import into `6 - Android Development`)

*Created 2026-09-29 14:45 HST. Android import pass. Test record: [2026-09-29-android-apps-import](../07-testing/2026-09-29-android-apps-import.md).*

From today on, all Android development lives in `/home/rootrecord/RootRecord-Ecosystem/6 - Android Development/`, one Title-case folder per app. This page records where each app came from, which copy was chosen and why, and what was left out.

## Target folder status

| Item | Value |
| --- | --- |
| Total size | **80.7 MB**, 1,033 files (budget 40 GB) |
| Git | **Not a git repo**. No `.git` anywhere in the tree. The Ecosystem root isn't a repo either |
| Auto-sync | **Not covered.** No row in Pacific `Github/scripts/repos.conf` or in `~/.ollama/skills/github/scripts/repos.conf`. `Push.sh` and `Pull.sh` only list Pacific, Database and Library |
| `.gitignore` | `6 - Android Development/.gitignore` covers keystores (`*.jks`, `*.keystore`, `*.p12`, `*.pem`, `keystore/`), `keystore.properties`, `local.properties`, `google-services.json`, `.env*`, recovery codes, `memory/test_credentials*`, build and cache folders, and `*.apk`, `*.aab` and `Releases/`. Checked with `git check-ignore` against a throwaway bare repo: **24/24** secret and artifact files ignored |
| Secrets | 17 files, all mode **0600**; `keystore/` folders are 0700. Paths are listed below. Contents were never printed or recorded |
| Android SDK / Studio / Java | **None on the desk.** No `~/Android/Sdk`, no `~/.local/opt/android-sdk` (the old `android-build` skill expects it there), no `ANDROID_HOME`, no `adb`, `sdkmanager` or `aapt`, no Android Studio (`/opt`, snap, flatpak, `~/.local/share/JetBrains`), no `java`, no `~/.gradle` or `~/.android` |

## Apps

| Target folder | App / applicationId | Version (source) | Chosen source | Source last modified | Releases/ (newest found) | Git |
| --- | --- | --- | --- | --- | --- | --- |
| `Kilauea-App/` | Kīlauea Alerts, native Kotlin/Compose, `com.rootrecord.kilauea` | **1.0.47** (47) | desk `~/old ollama/old skills/kilauea/kilauea-alerts/android` | 2026-09-20 09:11 HST (copy time; `.gitignore` and `local.properties` 2026-09-16) | `RootRecord-Kilauea-Alerts-1.0.47.apk` (5.1 MB, 2026-08-19), from `~/old ollama/old skills/minecraft/rootmc/workstations/android/builds/` | none local; older 1.0.46 is in GitHub monorepo `Mobile/kilauea-alerts-android` |
| `Weather-Manager/` | Weather Manager, Capacitor, `com.rootrecord.weathermanager` | **1.0.46** (46) | GitHub `rootrecordsoftwaresolutions/mirror-rootrecord-monorepo` @ `dc15487`, `Mobile/weather-manager-mobile` + `Web/apps/weather-manager-web` → `Web-Source/` | last content commit `aaa111b` 2026-06-07 15:27 HST | `RootRecord-Weather-main-8a2c9e6-20260502.apk` (7.3 MB, from `mirror-rootrecord-mobile-development-2026` main) and `RootRecord-Weather-v1.0.9-20260429-1913.aab` (7.0 MB, `business-work`). No 1.0.46 build was found | history on GitHub only |
| `RootMC-Android/` | RootMC / Block Notes, native Kotlin, `com.rootrecord.rootmc` | **1.0.31** (31) | desk `~/old ollama/old skills/rootmc-android/android` | 2026-09-17 01:38 HST | `RootRecord-RootMC-1.0.32.aab` (10.8 MB, 2026-08-03) **from the 2 TB drive**, sha256 identical to the desk copy; `RootRecord-RootMC-1.0.32.apk` (6.6 MB) from the desk | none local; `rootmc-emergent` repo also has 1.0.31 |
| `Ava-Ops/` | Ava Ops, native, `com.rootrecord.avaops` | **0.2.0** (2) | desk `~/old ollama/old skills/android/ava-ops/android` | 2026-09-20 09:11 HST | `RootRecord-Ava-Ops-0.2.0-debug.apk` (17.6 MB, **debug**, 2026-09-16 19:53, renamed from `app/build/outputs/apk/debug/app-debug.apk`) | none |
| `Business-Manager/` | Business Manager, Capacitor, `com.rootrecord.businessmanager` | **1.0.42** (42) | monorepo `Mobile/business-manager-app` + `Web/apps/business-manager-web` | `aaa111b` 2026-06-07 | `RootRecord-BusinessManager-debug-20260429-1939.apk` (7.3 MB, debug, older than the source) | GitHub only |
| `Root-Goals/` | Root Goals, Capacitor, `com.rootrecord.rootgoals` | **1.0.9** (9) | monorepo `Mobile/root-goals-mobile` + `Web/apps/root-goals-web` | `aaa111b` 2026-06-07 | none found | GitHub only |
| `Root-Farms/` | Root Units / Farms, Capacitor, `com.rootrecord.rootunits` | **1.0.9** (9) | monorepo `Mobile/root-farms-app` + `Web/apps/root-farms-mobile-web` | `db2b766` 2026-05-23 | none found | GitHub only; the `root-units-idle-farmer` mirror has only 1.0.2 |
| `Token-Manager/` | Token Manager, Capacitor, `com.rootrecord.tokenmanager` | **0.1.2** (4) | monorepo `Mobile/token-manager-app` + `Web/apps/token-manager-web` | `d41900b` 2026-05-23 | none found | GitHub only |
| `Account-Hub/` | Account Hub, Capacitor, `com.rootrecord.accounthub` | **0.1.3** (5) | monorepo `Mobile/account-hub-app` + `Web/apps/account-hub-web` | `535697d` 2026-05-19 | none found | GitHub only |

Not imported: **Visiting Hawaiʻi** (`Mobile/visiting-hawaii-app` is only a `capacitor.config.json`, `package.json` and README, with no `android/`), and the old **amplify-ui** React Native example on the drive (a third-party sample, not a RootRecord app).

### Sizes (source / Releases)

| App | Source copied | Releases/ | Folder total |
| --- | --- | --- | --- |
| Kilauea-App | 1.86 MB, 128 files | 4.9 MB | 7.2 MB |
| Weather-Manager | 5.40 MB, 119 files, plus Web-Source 2.1 MB, 48 files | 13.6 MB | 22 MB |
| RootMC-Android | 2.93 MB, 193 files | 16.6 MB | 21 MB |
| Ava-Ops | 0.25 MB, 41 files | 16.8 MB | 18 MB |
| Business-Manager | 1.18 MB, 73 files, plus Web-Source 1.9 MB, 48 files | 7.0 MB | 11 MB |
| Root-Goals | 0.32 MB, 60 files, plus Web-Source 0.10 MB, 27 files | none | 0.9 MB |
| Root-Farms | 3.02 MB, 67 files, plus Web-Source 0.58 MB, 17 files | none | 3.9 MB |
| Token-Manager | 0.36 MB, 66 files, plus Web-Source 1.34 MB, 43 files | none | 2.1 MB |
| Account-Hub | 0.34 MB, 61 files, plus Web-Source 1.28 MB, 33 files | none | 2.0 MB |

## Why these copies (selection rule: newest mtimes, then versionCode/versionName, then git log)

- **The 2 TB drive (`/dev/sda1`, WD20EARZ in a MAYA USB enclosure, NTFS label-less `6CD8FA150F0B0035`)** holds Alexander's old home layout. It has **no usable Android source.** Its only Android trees are `Solar-Pacific-RootRecord-Server(-Old)-main/{kilauea/kilauea-alerts,rootmc-android}/desk/live/` under `Downloads/`, `1/Downloads/stale downloaded/` and `New Folder 1/…`. There every `.kt` and Gradle file is **0 bytes**: GitHub-zip copies in which the symlinks became empty files. The drive has no `AndroidStudioProjects`, and `Desktop/` is empty. What the drive does have:
  - RootMC AABs 1.0.31 and 1.0.32 in `Send to External drive/large files extracted from skills/rootmc-android/android/builds/`. The 1.0.32 AAB was imported.
  - RootMC APKs 1.0.27 to 1.0.30 (July), twice: `Database/Send to External drive/SORT/presorted/OLD APKS/` and `Documents/imports/projects-phone/`. Older, not imported.
  - `RootRecord-Weather*.apk` ×3 (2026-04-25), same two folders. Older than the GitHub artifacts, not imported.
  - `Documents/council-deploy/Implemented/ava-ops-android.tgz` (2026-09-15), older than the desk copy (2026-09-20). Not imported.
  - `RootRecord-RootMC-main.zip` (14 files, docs only), plus the `weather*.zip` and `rootrecord_weather_fix_20260926.zip` archives (Python weather backend, not Android). Not imported.
- **Desk `~/old ollama/`** (G2 skills backup) has full Kilauea, RootMC and Ava-Ops projects in 4 copies each: `old skills/`, `github-history/09202026 1830/`, `…/09202026 1830/09202026 1830/` and `github-history/09202026 Early AM/`. `diff -rq` shows the source is identical across copies (same versionCode). The `old skills/` copy is the only one with the signing files and `.gitignore`, so it was chosen. `~/AndroidStudioProjects` doesn't exist, `~/Database` holds only backup and ops folders (`GITHUB/*.bak-*`, logs, flags), and `~/master` holds only an env file.
- **GitHub (read-only `gh`)**. A tree scan of all 90 non-empty repos (`rootrecordsoftwaresolutions` + `RootRecord-Software-Solutions`) found Android projects in `mirror-rootrecord-monorepo` (8 apps under `Mobile/`, newest for all Capacitor apps), `mirror-rootrecord-mobile-development-2026` (main: Weather 1.0.27, Business 1.10, Kilauea 1.0.4; `business-work`: Weather 1.0.8), `mirror-rootrecord-rr-weather-manager-mobile` (1.0.2), `rootmc-emergent` and its mirror (RootMC 1.0.31), and `mirror-rootrecord-root-units-idle-farmer` (1.0.2). Monorepo branch `conflict_230526_1657` is older (Weather 1.0.45, Business 1.0.40, Kilauea 1.0.32); `rootmc-apps` has RootMC 1.0.27. None of the org (`RootRecord-Software-Solutions`) repos contain Android code.
- The RootMC source says 1.0.31, but 1.0.32 release builds exist (2026-08-03). The 1.0.32 bump in source was never found in any copy.

## Excluded (per copy)

`build/`, `.gradle/`, `.idea/`, `.cxx/`, `node_modules/`, `__pycache__/`, `builds/` and `release/` artifact folders (only the newest artifact went to `Releases/`), older duplicate copies, SDKs and emulator images (none present), Ava-Ops `app/build/` (146 MB), Root-Farms `zoho-mail-desktop-lite-installer-x64-v1.9.2.exe` (99 MB) and `grok-video-….mp4` (2.3 MB), neither referenced by the app. No other drive material was copied.

## Secrets (paths only, all 0600, all git-ignored)

- Kilauea-App: `keystore/kilauea-upload.jks`, `keystore/kilauea-upload-cert.pem`, `local.properties` (sdk.dir + release signing values), `app/google-services.json`, `github-recovery-codes.txt` (**a GitHub account recovery-codes file inside the project folder**; consider moving it out of any app tree)
- Weather-Manager: `android/app/keystore/{rootrecord-weather-release.jks,upload.jks,keystore.properties}`, `android/app/google-services.json`
- RootMC-Android: `keystore/blocknotes-upload.jks`, `local.properties` (release signing values)
- Ava-Ops: `local.properties` (sdk.dir only)
- Business-Manager: `android/app/google-services.json`, `memory/test_credentials.md`
- Root-Farms: `google-services.json`, `android/app/google-services.json`
- Token-Manager: `memory/test_credentials.md`
- `*.example` templates (7) stay trackable; none contain key-like strings.

**Security note:** some signing material for these apps is in GitHub repositories that aren't private. Alexander has the details from the operator report; this public page doesn't repeat them.

## Not done / next

- No Gradle or Capacitor build (heavy, and the desk has no SDK, Java or Studio). First build needs: JDK 17, Android SDK (platforms and build-tools per each `compileSdk`), `sdk.dir` fixed in the three `local.properties`, and for the Capacitor apps `webDir` pointed at `Web-Source/build` (config left unedited).
- Decide whether each app gets its own GitHub repo (**private**) before any `git init`. The `.gitignore` here should be copied into each.
- Staging clones left in place for review (not deleted): `/home/rootrecord/.cache/rr-android-import-20260929/monorepo` (594 MB, disk) and `/tmp/android-inv/md2026` (93 MB, tmpfs).
