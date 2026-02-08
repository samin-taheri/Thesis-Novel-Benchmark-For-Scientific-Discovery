from typing import List, Optional
from ..schemas import TaskItem

def load_biodsa(path: Optional[str]=None, limit: Optional[int]=20) -> List[TaskItem]:
    # Placeholder: executable analysis style task
    items = []
    for i in range(limit or 10):
        items.append(TaskItem(
            id=f"bio-{i}",
            domain="biomed",
            task_type="analysis",
            input={"table": {"x":[1,2,3,4], "y":[2,4,6,9]}},
            gold={"regression":"~ linear-ish"},
            split="iid"
        ))
    return items
