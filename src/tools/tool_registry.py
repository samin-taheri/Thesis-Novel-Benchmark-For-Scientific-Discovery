from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .python_tool import PythonTool
from .retrieval_tool import RetrievalTool


@dataclass
class ToolRegistry:
    """Container for offline tools available to agentic scenarios."""

    python: PythonTool
    retrieval: RetrievalTool

    @classmethod
    def from_config(cls, tool_names: List[str] | None, corpus_path: str) -> "ToolRegistry":
        # Always construct tools, but scenarios can choose to use them based on tool_names.
        return cls(
            python=PythonTool(),
            retrieval=RetrievalTool(corpus_path=corpus_path),
        )

    def list_enabled(self, tool_names: List[str] | None) -> List[str]:
        tool_names = tool_names or []
        allowed = set(tool_names)
        enabled: List[str] = []
        if "python" in allowed or "calculator" in allowed:
            enabled.append("python")
        if "retrieval" in allowed or "docs" in allowed:
            enabled.append("retrieval")
        return enabled

    def run(self, tool: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        if tool == "python":
            return self.python.run(code=str(payload.get("code", "")), variables=payload.get("variables"))
        if tool == "retrieval":
            return {
                "ok": True,
                "docs": self.retrieval.search(
                    query=str(payload.get("query", "")),
                    k=int(payload.get("k", 3)),
                    domain=payload.get("domain"),
                ),
            }
        return {"ok": False, "error": f"Unknown tool: {tool}"}
