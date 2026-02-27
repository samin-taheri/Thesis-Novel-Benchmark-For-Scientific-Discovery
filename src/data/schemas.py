"""Common data schema shared by all benchmark loaders."""

from pydantic import BaseModel
from typing import Any, Dict


class TaskItem(BaseModel):
    """A single benchmark task instance.

    Attributes:
        id:        Unique identifier within the dataset.
        domain:    Scientific domain (physics, biology, biomed, chemistry, general).
        task_type: Kind of task (equation, causal, qa, design, analysis, decompose).
        input:     Task-specific input payload (prompts, data points, etc.).
        gold:      Ground-truth for programmatic scoring (may be empty for open tasks).
        split:     Dataset split label (iid, ood, test).
    """
    id: str
    domain: str
    task_type: str
    input: Dict[str, Any]
    gold: Dict[str, Any]
    split: str = "test"
