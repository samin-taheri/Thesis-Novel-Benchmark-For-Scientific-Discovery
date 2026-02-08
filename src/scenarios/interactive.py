from typing import Dict, Any
class Interactive:
    def __init__(self, params: Dict[str, Any] | None = None):
        self.params = params or {}
    def make_prompt(self, item: Dict[str, Any]) -> str:
        return ("Interactive discovery (simulated): propose the next intervention and expected outcome, "
                "then revise the hypothesis accordingly.\n"
                f"Inputs: {item['input']}")
