from typing import List, Optional
from ..schemas import TaskItem

def load_researchbench(path: Optional[str]=None, limit: Optional[int]=20) -> List[TaskItem]:
    # Placeholder: inspiration → hypothesis → ranking (collapsed into a single item with fields)
    items = []
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
