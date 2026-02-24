from typing import List, Optional
from ..schemas import TaskItem
import json

def load_llm_srbench(path: Optional[str]=None, limit: Optional[int]=20) -> List[TaskItem]:
    """
    Load the official LLM-SRBench dataset from a JSONL file.
    Each record should have fields: id, domain, task_type, input, gold, split.
    If the official dataset is not JSONL, add a conversion script.
    """
    if path is None:
        raise ValueError(
            "LLM-SRBench loader requires a real dataset path (JSONL). "
            "Set data.path in the experiment YAML."
        )

    items = []
    # Official loader: expects JSONL file with TaskItem fields
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            items.append(TaskItem(**rec))
            if limit and len(items) >= limit:
                break
    return items
