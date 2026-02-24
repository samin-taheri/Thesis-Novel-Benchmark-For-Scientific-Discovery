from typing import List, Optional
from ..schemas import TaskItem
import json

def load_scihorizon(path: Optional[str]=None, limit: Optional[int]=20) -> List[TaskItem]:
    items = []
    if path:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                rec = json.loads(line)
                items.append(TaskItem(**rec))
                if limit and len(items) >= limit:
                    break
        return items
    # Placeholder: science QA style control tasks
    for i in range(limit or 10):
        items.append(TaskItem(
            id=f"scih-{i}",
            domain="general",
            task_type="qa",
            input={"question": "What law relates force, mass, and acceleration?"},
            gold={"answer": "F = m * a"},
            split="iid"
        ))
    return items
