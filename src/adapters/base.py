from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAdapter(ABC):
    def __init__(self, model: str, temperature: float, top_p: float, max_tokens: int, tools=None):
        self.model = model
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens
        self.tools = tools or []

    @abstractmethod
    def generate(self, prompt: str, meta: Dict[str, Any]) -> Dict[str, Any]:
        ...
