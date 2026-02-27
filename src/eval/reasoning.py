"""Reasoning depth proxy scorer.

Estimates depth from rationale word count and presence of agent plans.
"""

from __future__ import annotations

from typing import Any, Dict


def reasoning_depth_from_trace(model_out: Dict[str, Any]) -> float:
    """Offline proxy for reasoning depth.

    Uses length of rationale + presence of structured agent plan.
    This remains a proxy until you add rubric-based judging.
    """
    rationale = (model_out.get("rationale") or "")
    plan = ((model_out.get("agent") or {}).get("plan") or "")

    words = len((rationale + " " + plan).split())
    # Normalize roughly: 0..1 by 0..200 words
    return float(max(0.0, min(1.0, words / 200.0)))
