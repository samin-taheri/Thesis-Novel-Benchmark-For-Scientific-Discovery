"""Core evaluation loop.

The `Evaluator` class orchestrates data loading, prompt construction,
LLM inference, and per-item scoring for a single experiment run.
"""

from typing import List, Tuple

import pandas as pd

from ..adapters import ADAPTERS
from ..config import ExperimentConfig
from ..data.loaders import (
    load_autobench,
    load_baisbench,
    load_biodsa,
    load_llm_srbench,
    load_researchbench,
    load_scihorizon,
    load_synthetic,
)
from ..data.schemas import TaskItem
from ..eval.judge_science import score_item
from ..eval.metrics_science import summarize_metrics
from ..scenarios import SCENARIOS
from ..tools.tool_registry import ToolRegistry
from ..utils.logging import get_logger
from ..utils.paths import data_path
from ..utils.random_seed import fix_seed

LOADER_MAP = {
    "autobench": load_autobench,
    "llm_srbench": load_llm_srbench,
    "scihorizon": load_scihorizon,
    "researchbench": load_researchbench,
    "baisbench": load_baisbench,
    "biodsa": load_biodsa,
    "synthetic": load_synthetic,
}


class Evaluator:
    """Run all tasks through the configured scenario + adapter and collect scores."""

    def __init__(self, cfg: ExperimentConfig, run_id: str):
        self.cfg = cfg
        self.logger = get_logger("evaluator", run_id)
        fix_seed(cfg.random_seed)

        # Data
        loader = LOADER_MAP[cfg.data.loader]
        self.items: List[TaskItem] = loader(cfg.data.path, cfg.data.limit)

        # Scenario (prompt/workflow strategy)
        self.scenario = SCENARIOS[cfg.scenario.name](cfg.scenario.params)

        # Model adapter (LLM provider)
        adapter_cls = ADAPTERS[cfg.model.provider]
        self.adapter = adapter_cls(
            cfg.model.model,
            cfg.model.temperature,
            cfg.model.top_p,
            cfg.model.max_tokens,
            cfg.model.tools,
        )

        # Offline tools available to agentic scenarios
        self.tool_registry = ToolRegistry.from_config(
            tool_names=cfg.model.tools,
            corpus_path=data_path("corpus", "mini_science_corpus.jsonl"),
        )

    def run(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        rows = []
        enabled_tools = self.tool_registry.list_enabled(self.cfg.model.tools)

        for item in self.items:
            item_dict = item.model_dump()

            meta = {"task_type": item.task_type, "domain": item.domain, "id": item.id, "split": item.split}

            # If the scenario supports agentic execution with tools, use it.
            if hasattr(self.scenario, "run"):
                out = self.scenario.run(item_dict, self.adapter, self.tool_registry, enabled_tools)
                prompt = None
            else:
                prompt = self.scenario.make_prompt(item_dict)
                out = self.adapter.generate(prompt, meta)

            score = score_item(item, out)
            row = {
                "id": item.id,
                "domain": item.domain,
                "task_type": item.task_type,
                "split": item.split,
                "prompt": prompt,
                "prediction": out.get("content"),
                "rationale": out.get("rationale"),
                "agent_plan": (out.get("agent", {}) or {}).get("plan"),
                "agent_tool": ((out.get("agent", {}) or {}).get("tool_call", {}) or {}).get("tool"),
                "agent_tool_ok": ((out.get("agent", {}) or {}).get("tool_obs", {}) or {}).get("ok"),
                **score,
                **(out.get("usage", {}) or {}),
            }
            rows.append(row)

        per_item_df = pd.DataFrame(rows)
        summary_df = summarize_metrics(per_item_df)
        return summary_df, per_item_df
