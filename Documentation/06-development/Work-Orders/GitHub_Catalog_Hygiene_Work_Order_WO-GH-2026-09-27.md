# WORK ORDER — GitHub Catalog Hygiene & Non-Canonical Cleanup

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-GH-2026-09-27 |
| **Status** | **IN PROGRESS** — Pacific `Github/` sync **LIVE**; website/mainland still disabled |
| **Updated** | 2026-09-28 ~17:11 HST |

**Scope:** Catalog + auto-sync under Pacific; org remotes for canonical three; retire non-canonical clutter when convenient.

---

## Done

- [x] Github scripts imported to `…/Pacific/Github/scripts/`
- [x] `repos.conf` tab-separated: pacific, database, library, skills (enabled); website, mainland (disabled)
- [x] jobs.py → Pacific `setup-all-remotes` + `sync-all`
- [x] Poller cycle fetches org pacific / database / library + legacy skills without fail storms

## Remaining

- [ ] Enable website when mirror worktree exists under `Database/GITHUB/worktrees/website`
- [ ] Enable mainland when path is a real git clone
- [ ] Delete non-canonical user-account Library repo if still present
- [ ] Optional: stop publishing skills to historical Solar-Pacific remote when G2 is fully retired

## Catalog home

```text
/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server/Github/scripts/repos.conf
```

Token: `master-key.env` — never commit.


## Static Catalog Audit — 2026-09-28

- Direct Pacific inspection of `Github/scripts/repos.conf` confirms the enabled catalog entries are Pacific, Database, Library, and the historical skills repository; Website and mainland remain explicitly disabled.
- The two `.ollama/skills` references in `repos.conf` are the intentional `skills` catalog path and disabled Website/Mainland paths, not active Pacific runtime executable references.
- Direct inspection of `Github/scripts/setup-all-remotes.sh` and `Github/scripts/sync-all.sh` found no embedded `/home/rootrecord/.ollama/skills/` or `~/.ollama/skills/` executable references.
- Representative current source SHAs: `repos.conf` `d3a24a3133c51117084c7440473b58e030436424`; `setup-all-remotes.sh` `22253d003c01488f618f195d7a3a983dbfd51f46`; `sync-all.sh` `57e2c7b2a570ba6340cfcb29c578e765727ec001`.
- This is a static catalog audit only. It does not enable Website/Mainland or authorize removal of the historical skills catalog before the remaining WO-GH prerequisites are satisfied.
