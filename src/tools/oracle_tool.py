from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class OracleTool:
    """Offline oracle for Auto-Bench-like tasks.

    The task instance already contains an "intervention_menu" with precomputed
    interventional datasets. This tool simply returns the requested one.

    Payload format:
      {"node": "A"}  -> returns the menu entry with do(A=2.0)
      or {"index": 0}
    """

    name: str = "oracle"

    def run(self, item: Dict[str, Any], payload: Dict[str, Any]) -> Dict[str, Any]:
        menu: List[Dict[str, Any]] = (item.get("input") or {}).get("intervention_menu") or []
        if not menu:
            return {"ok": False, "error": "No intervention_menu in item"}

        idx = payload.get("index")
        node = payload.get("node")

        if idx is not None:
            try:
                idx_int = int(idx)
                if idx_int < 0 or idx_int >= len(menu):
                    return {"ok": False, "error": "index out of range"}
                return {"ok": True, "intervention": menu[idx_int]}
            except Exception as e:
                return {"ok": False, "error": str(e)}

        if node is not None:
            node = str(node)
            for entry in menu:
                do = entry.get("do") or {}
                if node in do:
                    return {"ok": True, "intervention": entry}
            return {"ok": False, "error": f"No intervention for node {node}"}

        # default: return first one
        return {"ok": True, "intervention": menu[0], "defaulted": True}
