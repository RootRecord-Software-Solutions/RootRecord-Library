# Test record — NPU / FastFlowLM install and validate

| Field | Value |
| --- | --- |
| **Date / time (HST)** | 2026-09-29 02:50–02:56 HST (addendum 03:02 HST) |
| **Change under test** | Alexander installed `libxrt-utils`, `libxrt-utils-npu` and FastFlowLM 1.0.6. Validation plus one gated inference |
| **State** | **PASS** |
| **Evidence** | `2 - RootRecord-Database/Logs/Migration/g3-npu-flm-evidence-20260929T125429Z.md` |
| **Commits** | No runtime code change for the gate itself. Related: Database `d64b8fd` (02:52, FLM log accidentally committed) → `4331c0f` (02:59, approved untrack); Pacific `ebc32a7` (02:58, relay quiet mode) |
| **Backup** | `/home/rootrecord/Database/GITHUB/g3-npu-verify.bak-20260929-025336/` |

## How
`xrt-smi examine`, `flm validate`, `flm version`. Pulled `llama3.2:1b` once. Then `FLM_MODEL=llama3.2:1b flm-warmup.sh`, one `run-infer.sh ava "…2+2?"`, and one parallel `single-flight.sh run parallel-test` while the lock was held.

## Pass criteria
1. `xrt-smi` sees the NPU and `flm validate` is OK.
2. One inference answered on the NPU through the single-flight gate (rc 0).
3. A parallel run is refused.
4. The test server is stopped afterwards.

## Result
- `xrt-smi`: RyzenAI-npu6 (aie2p, 6x8, FW 1.1.2.64). `flm validate`: `/dev/accel/accel0`, 8 columns, amdxdna 0.7, memlock infinity (operator-reported). `flm` v1.0.6.
- Gate: `[ok] FLM/NPU llama3.2:1b`, rc 0, **1.04 s** end-to-end (warm model). FLM log: `NPU Locked!` → prefill 132 tokens → `NPU Lock Released!`.
- Parallel run → `[busy] refuse parallel run`, **rc 75**.
- 03:02 addendum: `llama3.2:3b` pre-pulled (2666.7 MB, `flm check` OK). It is now installed but unused (see the [1b on-demand record](./2026-09-29-npu-llama3.2-1b-on-demand.md)).

## Resource impact
Model on disk: 1.3 GB (1b) + 2.7 GB (3b) in `~/.config/flm/models/`. Runtime memory was not recorded for this test.

## Cleanup confirmation
Test server pid 57993 stopped (`kill`), port closed, single-flight IDLE.
