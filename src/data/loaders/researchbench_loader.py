from typing import List, Optional
from ..schemas import TaskItem
import json

def load_researchbench(path: Optional[str]=None, limit: Optional[int]=20) -> List[TaskItem]:
    items = []
    if path:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                rec = json.loads(line)
                items.append(TaskItem(**rec))
                if limit and len(items) >= limit:
                    break
        return items
    # Placeholder: inspiration → hypothesis → ranking (collapsed into a single item with fields)
    for i in range(limit or 10):
        items.append(TaskItem(
            id=f"rb-{i}",
            domain="biology",
            task_type="decompose",
            input={"papers": ["P1 abstract", "P2 abstract"], "goal": "Propose testable hypothesis about gene X effect."},
            gold={"keywords": ["gene X", "pathway"]},
            split="iid"
        ))
    return items
