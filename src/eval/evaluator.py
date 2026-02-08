from typing import Tuple, List, Dict, Any
from pydantic import BaseModel
import pandas as pd
from ..utils.random_seed import fix_seed
from ..utils.logging import get_logger
from ..data.loaders import load_autobench, load_llm_srbench, load_scihorizon, load_researchbench, load_biodsa, load_synthetic, load_baisbench
from ..data.schemas import TaskItem
from ..scenarios import SCENARIOS
from ..eval.judge_science import score_item
from ..eval.metrics_science import summarize_metrics
from ..adapters import ADAPTERS
from ..config import ExperimentConfig
from ..tools.tool_registry import ToolRegistry
from ..utils.paths import data_path

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
    def __init__(self, cfg: ExperimentConfig, run_id: str):
        self.cfg = cfg
        self.logger = get_logger("evaluator", run_id)
        fix_seed(cfg.random_seed)

        # Data
        loader = LOADER_MAP[cfg.data.loader]
        self.items: List[TaskItem] = loader(cfg.data.path, cfg.data.limit)

        # Scenario
        self.scenario = SCENARIOS[cfg.scenario.name](cfg.scenario.params)

        # Model adapter
        A = ADAPTERS[cfg.model.provider]
        self.adapter = A(cfg.model.model, cfg.model.temperature, cfg.model.top_p, cfg.model.max_tokens, cfg.model.tools)

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
