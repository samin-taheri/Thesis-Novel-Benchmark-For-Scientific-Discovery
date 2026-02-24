from typing import List, Optional
from ..schemas import TaskItem
import json
import os

def load_llm_srbench(path: Optional[str]=None, limit: Optional[int]=20) -> List[TaskItem]:
    """
    Load the official LLM-SRBench dataset from a JSONL file.
    Each record should have fields: id, domain, task_type, input, gold, split.
    If the official dataset is not JSONL, add a conversion script.
    """
    items = []
    if path is None:
        # Fallback: use placeholder
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
    # Official loader: expects JSONL file with TaskItem fields
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            items.append(TaskItem(**rec))
            if limit and len(items) >= limit:
                break
    return items
