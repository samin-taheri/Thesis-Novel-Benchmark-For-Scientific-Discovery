from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

import math


@dataclass
class PythonTool:
    """Very small offline "python" tool.

    This is intentionally limited: it supports evaluating simple numeric
    expressions with a restricted set of names.

    NOTE: This is *not* a secure sandbox. It is a pragmatic, restricted evaluator
    suited for controlled benchmark inputs.
    """

    name: str = "python"

    def run(self, code: str, variables: Dict[str, Any] | None = None) -> Dict[str, Any]:
        env: Dict[str, Any] = {
            "__builtins__": {},
            "math": math,
            "abs": abs,
            "min": min,
            "max": max,
            "sum": sum,
            "len": len,
            "range": range,
        }
        if variables:
            # Only allow JSON-like primitives/lists/dicts.
            env.update(variables)

        try:
            # Expression-first: supports things like "2*x+1" or "[f(x) for x in xs]".
            result = eval(code, env, {})
            return {"ok": True, "result": result}
        except Exception as e:
            return {"ok": False, "error": str(e)}
