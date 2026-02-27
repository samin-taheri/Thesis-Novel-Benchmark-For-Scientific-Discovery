"""Interactive scenario: simulated multi-turn hypothesis revision."""

from typing import Any, Dict, Optional


class Interactive:
    def __init__(self, params: Optional[Dict[str, Any]] = None):
        self.params = params or {}

    def make_prompt(self, item: Dict[str, Any]) -> str:
        return (
            "Interactive discovery (simulated): propose the next intervention and expected outcome, "
            "then revise the hypothesis accordingly.\n"
            f"Inputs: {item['input']}"
        )
