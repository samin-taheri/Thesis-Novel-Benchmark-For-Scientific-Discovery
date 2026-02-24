from typing import Dict, Any, Optional


class ClosedBook:
    def __init__(self, params: Optional[Dict[str, Any]] = None):
        self.params = params or {}

    def make_prompt(self, item: Dict[str, Any]) -> str:
        t = item["task_type"]
        if t == "equation":
            return (
                "You are a scientist. Given x and y samples, infer a symbolic relationship y=f(x). "
                "Return only an equation and a brief rationale.\n"
                f"x={item['input']['x']}\ny={item['input']['y']}"
            )
        if t == "causal":
            return (
                "You are a scientist. Infer a plausible causal graph over nodes. "
                "Return edges as pairs and a brief rationale.\n"
                f"nodes={item['input'].get('nodes', [])}"
            )
        if t == "qa":
            return "Answer concisely: " + item["input"]["question"]
        return "Propose a testable hypothesis for the given goal."
