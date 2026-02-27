"""Abstract base class that all LLM provider adapters must implement."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BaseAdapter(ABC):
    """Common interface for LLM adapters.

    Subclasses must implement `generate()`, which takes a prompt string and
    task metadata and returns a dict with keys: content, rationale, usage.
    """

    def __init__(self, model: str, temperature: float, top_p: float, max_tokens: int, tools: Optional[List[str]] = None):
        self.model = model
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens
        self.tools = tools or []

    @abstractmethod
    def generate(self, prompt: str, meta: Dict[str, Any]) -> Dict[str, Any]:
        ...
