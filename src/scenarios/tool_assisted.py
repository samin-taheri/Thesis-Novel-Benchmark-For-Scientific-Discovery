from typing import Dict, Any
class ToolAssisted:
    def __init__(self, params: Dict[str, Any] | None = None):
        self.params = params or {}
    def make_prompt(self, item: Dict[str, Any]) -> str:
        # In a real run, you would allow calculator/code tools. Here we just change instructions.
        return "Use careful calculations when needed. " + (item.get("prompt") or "Solve the task: " + str(item["input"]))
