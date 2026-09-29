# WORK ORDER — Pacific Runtime Path Cutover (`skills` → `1 - Servers`)

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-SRV-2026-09-27 |
| **Status** | **IN PROGRESS** — Energy + System LIVE; residual G2 domains remain |
| **Updated** | 2026-09-28 ~16:56 HST |

**Policy:** Do not run the old desk as the poller host.

**Domain naming SOP (standing):** One Pacific folder per domain (the capitalized name already in the tree). Python package name **matches that folder**. Never add a lowercase sibling symlink (e.g. no `energy` → `Energy`) to satisfy G2 imports — rewrite imports instead. Full text: [Pacific-Domain-Import-Playbook-2026-09-28.md](../../00-architecture/Pacific-Domain-Import-Playbook-2026-09-28.md) § Standing rules.

---

## Locked on Pacific

| Item | Status |
| --- | --- |
| systemd ExecStart | Pacific `run-poller.sh` (quoted) |
| Energy | LIVE — folder **`Energy/` only** |
| System | LIVE — folder **`System/` only** |

## Residual G2

worklog · github · plumbing · telegram · a-eyes · weather (disabled) · energy actions

## Next

Import next residual domain into its **existing** Pacific folder; rewire jobs; no parallel names.
