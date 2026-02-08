from pydantic import BaseModel
from typing import Optional, Dict, Any

class TaskItem(BaseModel):
    id: str
    domain: str  # physics|biology|biomed|chemistry|general
    task_type: str  # equation|causal|qa|design|analysis
    input: Dict[str, Any]
    gold: Dict[str, Any]  # ground truth for programmatic scoring (may be empty for open tasks)
    split: str = "test"   # iid|ood|test
