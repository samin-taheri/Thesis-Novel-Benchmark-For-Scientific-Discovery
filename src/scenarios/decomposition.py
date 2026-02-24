from typing import Any, Dict, Optional


class Decomposition:
    def __init__(self, params: Optional[Dict[str, Any]] = None):
        self.params = params or {}

    def make_prompt(self, item: Dict[str, Any]) -> str:
        return (
            "Plan → Decompose → Solve → Synthesize. "
            "Given background papers and a goal, propose 1–2 hypotheses and briefly rank them. "
            f"Papers: {item['input'].get('papers', [])}\nGoal: {item['input'].get('goal')}"
        )
