from typing import List, Optional
from ..schemas import TaskItem
import json

def load_researchbench(path: Optional[str]=None, limit: Optional[int]=20) -> List[TaskItem]:
    if not path:
        raise ValueError(
            "ResearchBench loader requires a real dataset path (JSONL). "
            "Set data.path in the experiment YAML."
        )

    items = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            items.append(TaskItem(**rec))
            if limit and len(items) >= limit:
                break
    return items
