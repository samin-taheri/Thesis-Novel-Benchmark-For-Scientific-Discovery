from __future__ import annotations

from typing import List, Optional, Any, Dict

from ..schemas import TaskItem
from ._json_helpers import read_json_or_jsonl


def _coerce_edges(raw_edges: Any) -> List[list[str]]:
    edges: List[list[str]] = []
    if raw_edges is None:
        return edges

    # edges can be [["A","B"], ...] or ["A->B", ...]
    for e in raw_edges:
        if isinstance(e, str) and "->" in e:
            u, v = e.split("->", 1)
            edges.append([u.strip(), v.strip()])
        elif isinstance(e, (list, tuple)) and len(e) == 2:
            edges.append([str(e[0]), str(e[1])])
    return edges


def load_autobench(path: Optional[str] = None, limit: Optional[int] = 20) -> List[TaskItem]:
    """Load Auto-Bench tasks.

    Supported now:
    - Local JSONL/JSON subset mapped into TaskItem.

    If no `path` is provided, returns a small synthetic toy set (for smoke tests).
    """

    # Real-data path
    if path:
        rows = read_json_or_jsonl(path)
        if limit:
            rows = rows[: int(limit)]

        items: List[TaskItem] = []
        for i, r in enumerate(rows):
            rid = str(r.get("id") or f"ab-{i}")
            domain = str(r.get("domain") or "physics")
            nodes = r.get("nodes") or r.get("variables") or ["A", "B", "C"]
            edges = _coerce_edges(r.get("edges") or r.get("gold_edges"))
            split = str(r.get("split") or "test")
            prompt = r.get("prompt")

            items.append(
                TaskItem(
                    id=rid,
                    domain=domain,
                    task_type="causal",
                    input={
                        "prompt": prompt,
                        "nodes": nodes,
                        # Optional agentic fields for future: observations/interventions.
                        "observations": r.get("observations"),
                        "interventions": r.get("interventions") or [],
                    },
                    gold={"edges": edges},
                    split=split,
                )
            )

        return items

    # Fallback: produce a tiny causal discovery toy set
    items: List[TaskItem] = []
    for i in range(limit or 10):
        items.append(
            TaskItem(
                id=f"auto-{i}",
                domain="physics",
                task_type="causal",
                input={"nodes": ["A", "B", "C"], "interventions": []},
                gold={"edges": [("A", "B"), ("B", "C")]},
                split="iid" if i < ((limit or 10) // 2) else "ood",
            )
        )
    return items
