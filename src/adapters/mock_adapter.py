from .base import BaseAdapter
from typing import Dict, Any
import random

class MockAdapter(BaseAdapter):
    def generate(self, prompt: str, meta: Dict[str, Any]) -> Dict[str, Any]:
        # A deterministic but fake "scientific" response for pipeline testing
        task = meta.get("task_type", "unknown")
        if task == "equation":
            content = "y = 2*x + 1  # MOCK hypothesis"
            rationale = "Fitted a linear model using synthetic reasoning."
        elif task == "causal":
            content = "{A->B, B->C}  # MOCK causal graph"
            rationale = "Inferred edges via mock interventions."
        else:
            content = "Hypothesis: variable X positively affects Y."
            rationale = "Based on mock literature synthesis."
        tokens_used = len(prompt.split()) + 30
        return {
            "content": content,
            "rationale": rationale,
            "usage": {"prompt_tokens": len(prompt.split()), "completion_tokens": 30, "total_tokens": tokens_used},
        }
