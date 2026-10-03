#!/usr/bin/env python3
"""Side test: turn the Bluetooth adapter on. Uses Energy/lib/adapter_on.py."""
import sys
from pathlib import Path

LIB = Path(
    "/home/rootrecord/RootRecord-Ecosystem/1 - Servers/"
    "1 - RootRecord-Pacific-Solar-Server/Energy/lib"
)
sys.path.insert(0, str(LIB))
from adapter_on import ensure_adapter_on  # noqa: E402

out = ensure_adapter_on()
print(
    f"turn_ble_on {'OK' if out['ok'] else 'FAIL'}  "
    f"tries={out['tries']}  {out['elapsed_s']:.3f}s",
    flush=True,
)
if out.get("detail"):
    print(out["detail"], flush=True)
sys.exit(0 if out["ok"] else 1)
