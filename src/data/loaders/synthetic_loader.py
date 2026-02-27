"""Synthetic data loader for pipeline dry-runs."""

from typing import List, Optional

from ..schemas import TaskItem


def load_synthetic(path: Optional[str] = None, limit: Optional[int] = 10) -> List[TaskItem]:
    """Generate a minimal mixed set of tasks for end-to-end testing."""
    items = []
    for i in range(limit):
        ttype = ["equation","causal","qa"][i % 3]
        if ttype == "equation":
            xs = list(range(-2,3))
            ys = [2*x+1 for x in xs]
            items.append(TaskItem(id=f"syn-eq-{i}", domain="physics", task_type="equation",
                                  input={"x": xs, "y": ys}, gold={"law": "2*x + 1"}))
        elif ttype == "causal":
            items.append(TaskItem(id=f"syn-cg-{i}", domain="physics", task_type="causal",
                                  input={"nodes": ["A","B","C"], "true_edges":[("A","B"),("B","C")]},
                                  gold={"edges":[("A","B"),("B","C")]}))
        else:
            items.append(TaskItem(id=f"syn-qa-{i}", domain="general", task_type="qa",
                                  input={"question":"Name Newton's second law."},
                                  gold={"answer":"F = m * a"}))
    return items
