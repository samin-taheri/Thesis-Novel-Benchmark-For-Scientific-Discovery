"""Evaluation scenario strategies.

Each scenario controls how a TaskItem is transformed into a prompt (or a
multi-step agentic workflow) before being sent to the LLM adapter.
"""

from .closed_book import ClosedBook
from .tool_assisted import ToolAssisted
from .decomposition import Decomposition
from .interactive import Interactive
from .agentic_tool_use import AgenticToolUse

SCENARIOS = {
    "closed_book": ClosedBook,
    "tool_assisted": ToolAssisted,
    "decomposition": Decomposition,
    "interactive": Interactive,
    "agentic_tool_use": AgenticToolUse,
}
