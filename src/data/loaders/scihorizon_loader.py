from typing import List, Optional
from ..schemas import TaskItem

def load_scihorizon(path: Optional[str]=None, limit: Optional[int]=20) -> List[TaskItem]:
    # Placeholder: science QA style control tasks
    items = []
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
