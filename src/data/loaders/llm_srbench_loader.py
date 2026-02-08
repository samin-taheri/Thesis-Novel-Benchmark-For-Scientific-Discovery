from typing import List, Optional
from ..schemas import TaskItem

def load_llm_srbench(path: Optional[str]=None, limit: Optional[int]=20) -> List[TaskItem]:
    # Placeholder: tiny equation discovery toy set (linear, quadratic)
    items = []
    for i in range(limit or 10):
        if i % 2 == 0:
            law = "2*x + 1"
            xs = list(range(-3,4))
            ys = [2*x+1 for x in xs]
        else:
            law = "x**2 - 3*x + 2"
            xs = list(range(-3,4))
            ys = [x**2 - 3*x + 2 for x in xs]
        items.append(TaskItem(
            id=f"sr-{i}",
            domain="physics",
            task_type="equation",
            input={"x": xs, "y": ys},
            gold={"law": law},
            split="iid" if i < (limit//2) else "ood"
        ))
    return items
