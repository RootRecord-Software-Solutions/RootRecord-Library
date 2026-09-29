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
