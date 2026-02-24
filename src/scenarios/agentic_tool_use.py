from __future__ import annotations

import json
from typing import Any, Dict, List


class AgenticToolUse:
    """Offline agentic scenario with a multi-step tool-use loop.

    Pattern: Think/Plan -> (Tool -> Observe)* -> Final.

    - Supports offline tools: retrieval, python, oracle
    - For causal discovery, encourages strict JSON output for edges.

    Notes:
    - We keep this deterministic/offline; no web access.
    - This is a lightweight protocol; you can later replace with a richer agent framework.
    """

    def __init__(self, params: Dict[str, Any] | None = None):
        self.params = params or {}
        self.max_steps = int(self.params.get("max_steps", 3))
        self.max_tool_calls = int(self.params.get("max_tool_calls", self.max_steps))

    def _system_instructions(self, item: Dict[str, Any], enabled_tools: list[str]) -> str:
        t = item.get("task_type")

        tool_doc = (
            "Tools:\n"
            "- retrieval payload: {query, k, domain}\n"
            "- python payload: {code, variables}\n"
            "- oracle payload: {node} or {index}  (oracle returns an interventional dataset)\n"
        )

        format_doc = ""
        if t == "causal":
            format_doc = (
                "\nOutput format requirement (causal):\n"
                "Return ONLY JSON: {\"edges\": [[\"A\",\"B\"], ...]}\n"
                "Edges must be directed and use node names exactly.\n"
            )

        return (
            "You are an autonomous scientific discovery agent running offline.\n"
            "You can call tools to gather evidence.\n"
            f"Enabled tools: {enabled_tools}.\n\n"
            + tool_doc
            + format_doc
        )

    def _tool_call_prompt(self, item: Dict[str, Any], enabled_tools: list[str], memory: List[Dict[str, Any]], remaining: int) -> str:
        return (
            self._system_instructions(item, enabled_tools)
            + "\nDecide the next action. Output ONLY JSON in one of these forms:\n"
            "1) Tool call: {\"tool\": <name>, \"payload\": {...}}\n"
            "2) Stop tool use and answer: {\"tool\": null, \"payload\": {}}\n\n"
            f"Remaining tool calls allowed: {remaining}\n\n"
            f"TASK:\n{json.dumps(item, ensure_ascii=False)}\n\n"
            f"MEMORY (previous tool observations):\n{json.dumps(memory, ensure_ascii=False)}\n"
        )

    def _final_prompt(self, item: Dict[str, Any], memory: List[Dict[str, Any]]) -> str:
        return (
            self._system_instructions(item, enabled_tools=[])
            + "\nNow produce your FINAL answer.\n"
            + "Use the evidence in MEMORY.\n\n"
            f"TASK:\n{json.dumps(item, ensure_ascii=False)}\n\n"
            f"MEMORY:\n{json.dumps(memory, ensure_ascii=False)}\n"
        )

    def run(self, item: Dict[str, Any], adapter, tool_registry, enabled_tools: list[str]) -> Dict[str, Any]:
        memory: List[Dict[str, Any]] = []
        tool_calls = 0
        traces: List[Dict[str, Any]] = []

        usage: Dict[str, int] = {}

        def _add_usage(u: Dict[str, Any] | None) -> None:
            for k, v in (u or {}).items():
                try:
                    usage[k] = usage.get(k, 0) + int(v)
                except Exception:
                    pass

        # Multi-step tool loop
        for step in range(self.max_steps):
            remaining = max(0, self.max_tool_calls - tool_calls)
            if remaining <= 0:
                break

            plan_prompt = self._tool_call_prompt(item, enabled_tools, memory, remaining)
            plan_out = adapter.generate(plan_prompt, {"phase": f"plan_{step}", "task_type": item.get("task_type"), "domain": item.get("domain")})
            _add_usage(plan_out.get("usage"))

            plan_text = (plan_out.get("content") or "").strip()
            tool_call: Dict[str, Any] = {"tool": None, "payload": {}}
            try:
                tool_call = json.loads(plan_text)
            except Exception:
                tool_call = {"tool": None, "payload": {"raw": plan_text}}

            tool_name = tool_call.get("tool")
            if tool_name not in enabled_tools:
                tool_name = None

            if not tool_name:
                traces.append({"step": step, "plan": plan_text, "tool": None})
                break

            payload = tool_call.get("payload") or {}
            if tool_name == "oracle":
                payload = {**payload, "item": item}

            tool_obs = tool_registry.run(tool_name, payload)
            tool_calls += 1

            memory.append({"tool": tool_name, "payload": tool_call.get("payload") or {}, "observation": tool_obs})
            traces.append({"step": step, "plan": plan_text, "tool": tool_name, "tool_obs": tool_obs})

        # Final answer
        final_prompt = self._final_prompt(item, memory)
        final_out = adapter.generate(final_prompt, {"phase": "final", "task_type": item.get("task_type"), "domain": item.get("domain")})
        _add_usage(final_out.get("usage"))

        return {
            "content": final_out.get("content"),
            "rationale": final_out.get("rationale"),
            "agent": {
                "memory": memory,
                "trace": traces,
                "tool_calls": tool_calls,
            },
            "usage": usage or final_out.get("usage", {}),
        }
