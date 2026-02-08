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
