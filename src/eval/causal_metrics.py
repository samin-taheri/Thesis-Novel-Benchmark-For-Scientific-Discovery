from __future__ import annotations

from typing import Dict, List, Set, Tuple

from ..utils.text import extract_edges, normalize_edge


def gold_edges(item_gold) -> Set[str]:
    edges = item_gold.get("edges") or []
    out: Set[str] = set()
    for e in edges:
        if isinstance(e, str) and "->" in e:
            u, v = e.split("->", 1)
            out.add(normalize_edge(u, v))
        elif isinstance(e, (list, tuple)) and len(e) == 2:
            out.add(normalize_edge(str(e[0]), str(e[1])))
    return out


def score_predicted_edges(pred_text: str, gold: Set[str]) -> Dict[str, float]:
    pred = set(extract_edges(pred_text))
    if not gold:
        return {"edge_precision": 0.0, "edge_recall": 0.0, "edge_f1": 0.0}

    tp = len(pred & gold)
    fp = len(pred - gold)
    fn = len(gold - pred)

    precision = tp / max(1, tp + fp)
    recall = tp / max(1, tp + fn)
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0
    return {"edge_precision": precision, "edge_recall": recall, "edge_f1": f1}
