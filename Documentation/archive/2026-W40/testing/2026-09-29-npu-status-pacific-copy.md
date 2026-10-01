# Test record — Pacific npu-status.sh (idle, read-only)

| Field | Value |
| --- | --- |
| **Date / time (HST)** | 2026-09-29 04:00:26 HST |
| **Tester** | executor agent (g3-proposals-impl) |
| **Change under test** | Copy of G2 `~/.ollama/skills/plumbing/scripts/npu-status.sh` → Pacific `System/scripts/plumbing/npu-status.sh` (G2 KEPT). Proposal: [08-ideas npu-status](../08-ideas/2026-09-29-npu-status-pacific-copy.md) |
| **State** | **PASS** (idle run) · lock-held run **VERIFY PENDING** |
| **Evidence** | `2 - RootRecord-Database/Logs/Migration/g3-proposals-impl-evidence-20260929T140900Z.md` |
| **Commits** | Pacific `5353e1f` |
| **Backup** | `/home/rootrecord/Database/GITHUB/g3-proposals-impl.bak-20260929-035910/` (new file, nothing overwritten) |

## How (exact commands / procedure)

```bash
bash ".../System/scripts/plumbing/npu-status.sh"
```

## Pass criteria (written before running)
1. rc 0. It lists `/dev/accel` and the XRT/NPU packages.
2. single-flight uses the Pacific script and the canonical `Github/plumbing/state`, and reports IDLE.
3. The FLM line says idle is normal: no `flm serve`, :52625 closed. No model is loaded.

## Result
1. `accel0` (root:render). Packages: libxrt-npu2, libxrt-utils, libxrt-utils-npu, libxrt2 1:2.25.0-4~resolute1, and linux-firmware-amd-misc 20260319. rc 0. **PASS**
2. `IDLE`, lock `/run/user/1000/rootrecord-inference.lock`, state dir empty. **PASS**
3. `IDLE (on demand): no flm serve, :52625 closed — normal`. **PASS**
4. The G2 original is unchanged (317 B, 2026-09-26 14:23).

## Resource impact
Read-only (ls, dpkg, pgrep, ss). Load/memory not recorded.

## Cleanup confirmation
- [x] no process left · [x] lock IDLE · [x] no resident model

## Open items / caveats
- Second run during an approved on-demand request (expect BUSY + `flm serve` + :52625 open).
