from __future__ import annotations

from typing import List, Optional
from ..schemas import TaskItem
import json


def load_baisbench(path: Optional[str] = None, limit: Optional[int] = 20) -> List[TaskItem]:
    """Load (a subset of) BaisBench.

    Note: This repository currently ships a *placeholder* dataset so the end-to-end
    pipeline (agentic scenarios + scoring + reporting) works.

    To plug in the real benchmark, point `path` to a prepared JSON/JSONL file and
    replace this stub with a parser that maps BaisBench examples -> TaskItem.
    """

    items: List[TaskItem] = []
    if path:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                rec = json.loads(line)
                items.append(TaskItem(**rec))
                if limit and len(items) >= limit:
                    break
        return items

    n = limit or 10

    # Placeholder: biology/omics-style discovery tasks that benefit from tool use.
    for i in range(n):
        items.append(
            TaskItem(
                id=f"bais-{i}",
                domain="biology",
                task_type="analysis",
                input={
                    "prompt": (
                        "You are given a simplified gene expression table across two conditions. "
                        "Propose a mechanistic hypothesis and one follow-up experiment."
                    ),
                    "genes": ["TP53", "BRCA1", "EGFR"],
                    "condition_A": [1.0, 0.5, 2.2],
                    "condition_B": [2.1, 0.4, 1.1],
                },
                gold={
                    # Open-ended: keep empty or provide rubric keywords for judge-based scoring.
                    "keywords": ["differential expression", "hypothesis", "experiment"],
                },
                split="iid" if i < (n // 2) else "ood",
            )
        )

    return items
