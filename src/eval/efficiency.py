from __future__ import annotations

from typing import Any, Dict


def efficiency_from_usage(usage: Dict[str, Any] | None) -> float:
    usage = usage or {}
    total = float(usage.get("total_tokens") or 0)
    if total <= 0:
        return 0.0
    # scale: 1.0 at <=250 tokens, 0.5 at 500, 0.25 at 1000
    return float(min(1.0, 250.0 / total))
