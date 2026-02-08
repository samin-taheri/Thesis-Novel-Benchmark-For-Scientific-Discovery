from __future__ import annotations

import hashlib
from typing import Any, Dict, Optional


def novelty_against_retrieved_docs(prediction: str, retrieved_docs: Optional[list[dict[str, Any]]]) -> float:
    """Offline novelty proxy.

    For offline-only runs, we approximate novelty as *non-copying* from retrieved
    context. If the prediction shares large exact substrings with retrieved docs,
    novelty decreases.

    This is still a proxy, but it is measurable and reproducible.
    """
    if not prediction:
        return 0.0
    if not retrieved_docs:
        return 0.5

    pred = prediction.lower()
    doc_text = "\n".join((d.get("text", "") or "") for d in retrieved_docs).lower()

    # Simple n-gram overlap (character 30-grams) for copy detection.
    n = 30
    if len(pred) < n or len(doc_text) < n:
        return 0.8

    def grams(s: str) -> set[str]:
        return {s[i : i + n] for i in range(0, len(s) - n + 1, 5)}

    g_pred = grams(pred)
    g_doc = grams(doc_text)
    overlap = len(g_pred & g_doc) / max(1, len(g_pred))

    # Higher overlap => less novelty
    novelty = 1.0 - min(1.0, overlap)
    return float(max(0.0, min(1.0, novelty)))
