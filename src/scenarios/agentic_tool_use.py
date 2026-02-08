from __future__ import annotations

import json
from typing import Any, Dict


class AgenticToolUse:
    """Offline agentic scenario with a simple 2-step tool-use loop.

    The model is asked to emit a JSON tool call plan first, we execute it, then
    feed the observation back for a final answer.

    This is intentionally lightweight but it establishes the evaluation pattern
    you need for your thesis (Plan -> Tool -> Observe -> Final).
    """

    def __init__(self, params: Dict[str, Any] | None = None):
        self.params = params or {}
        self.max_steps = int(self.params.get("max_steps", 2))

    def _plan_prompt(self, item: Dict[str, Any], enabled_tools: list[str]) -> str:
        return (
            "You are an autonomous scientific discovery agent running offline.\n"
            "You may call tools only if needed.\n"
            f"Enabled tools: {enabled_tools}.\n\n"
            "First, output ONLY a JSON object describing one tool call, with keys:\n"
            "  tool: 'python' or 'retrieval'\n"
            "  payload: an object (for python: {code, variables}; for retrieval: {query, k, domain})\n"
            "If no tool is needed, output: {\"tool\": null, \"payload\": {}}\n\n"
            f"TASK:\n{json.dumps(item, ensure_ascii=False)}\n"
        )

    def _final_prompt(self, item: Dict[str, Any], tool_call: Dict[str, Any], tool_obs: Dict[str, Any]) -> str:
        return (
            "You are an autonomous scientific discovery agent.\n"
            "Now produce your final answer with a brief rationale.\n\n"
            f"TASK:\n{json.dumps(item, ensure_ascii=False)}\n\n"
            f"TOOL_CALL:\n{json.dumps(tool_call, ensure_ascii=False)}\n\n"
            f"TOOL_OBSERVATION:\n{json.dumps(tool_obs, ensure_ascii=False)}\n\n"
            "Return your final answer in plain text."
        )

    def run(self, item: Dict[str, Any], adapter, tool_registry, enabled_tools: list[str]) -> Dict[str, Any]:
        # Step 1: plan a tool call
        plan_prompt = self._plan_prompt(item, enabled_tools)
        plan_out = adapter.generate(plan_prompt, {"phase": "plan", "task_type": item.get("task_type"), "domain": item.get("domain")})
        plan_text = (plan_out.get("content") or "").strip()

        tool_call: Dict[str, Any] = {"tool": None, "payload": {}}
        try:
            tool_call = json.loads(plan_text)
        except Exception:
            # If model fails JSON, treat as no-tool and continue.
            tool_call = {"tool": None, "payload": {"raw": plan_text}}

        tool_name = tool_call.get("tool")
        if tool_name not in enabled_tools:
            tool_name = None

        tool_obs: Dict[str, Any] = {"ok": True, "skipped": True}
        if tool_name:
            tool_obs = tool_registry.run(tool_name, tool_call.get("payload") or {})

        # Step 2: final answer with tool observation
        final_prompt = self._final_prompt(item, tool_call, tool_obs)
        final_out = adapter.generate(final_prompt, {"phase": "final", "task_type": item.get("task_type"), "domain": item.get("domain")})

        # Merge usages (best-effort)
        usage = {}
        for u in [plan_out.get("usage", {}), final_out.get("usage", {})]:
            for k, v in (u or {}).items():
                try:
                    usage[k] = usage.get(k, 0) + int(v)
                except Exception:
                    pass

        return {
            "content": final_out.get("content"),
            "rationale": final_out.get("rationale") or plan_out.get("rationale"),
            "agent": {
                "plan": plan_text,
                "tool_call": tool_call,
                "tool_obs": tool_obs,
            },
            "usage": usage or final_out.get("usage", {}) or plan_out.get("usage", {}),
        }
