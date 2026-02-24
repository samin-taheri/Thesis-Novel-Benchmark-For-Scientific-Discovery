from __future__ import annotations

from typing import List, Optional
from ..schemas import TaskItem
import json


def load_baisbench(path: Optional[str] = None, limit: Optional[int] = 20) -> List[TaskItem]:
    """Load (a subset of) BaisBench.

    Requires a JSONL file where each line is a TaskItem-compatible record.
    """

    if not path:
        raise ValueError(
            "BaisBench loader requires a real dataset path (JSONL). "
            "Set data.path in the experiment YAML."
        )

    items: List[TaskItem] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            items.append(TaskItem(**rec))
            if limit and len(items) >= limit:
                break
    return items
