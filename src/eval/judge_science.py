from __future__ import annotations

from typing import Dict, Any

import numpy as np

from ..data.schemas import TaskItem
from .causal_metrics import gold_edges, score_predicted_edges
from .novelty import novelty_against_retrieved_docs
from .reasoning import reasoning_depth_from_trace
from .efficiency import efficiency_from_usage


def _score_equation(item: TaskItem, pred: str) -> Dict[str, Any]:
    # very simple numeric check using eval with restricted globals (demo only)
    xs, ys = item.input["x"], item.input["y"]
    try:
        law = pred.split("#")[0].strip().replace("y=", "").replace("y =", "").strip()
        # evaluate numeric equivalence roughly (MSE)
        y_hat = [eval(law, {"__builtins__": {}}, {"x": x}) for x in xs]  # TODO: replace with sympy for safety
        mse = float(np.mean([(a - b) ** 2 for a, b in zip(ys, y_hat)]))
        acc = 1.0 if mse < 1e-6 else max(0.0, 1.0 - min(mse, 10.0) / 10.0)
    except Exception:
        acc = 0.0
        mse = 1e6
    return {"acc": acc, "mse": mse, "consistency_pass": acc > 0.8}


def _score_causal(item: TaskItem, pred: str) -> Dict[str, Any]:
    g = gold_edges(item.gold)
    m = score_predicted_edges(pred, g)
    # Primary accuracy = F1 (balanced)
    acc = float(m.get("edge_f1", 0.0))
    return {
        "acc": acc,
        "edge_precision": float(m["edge_precision"]),
        "edge_recall": float(m["edge_recall"]),
        "edge_f1": float(m["edge_f1"]),
        "consistency_pass": acc >= 0.8,
    }


def _score_qa(item: TaskItem, pred: str) -> Dict[str, Any]:
    gold = item.gold.get("answer", "").lower().replace(" ", "")
    got = (pred or "").lower().replace(" ", "")
    ok = gold in got if gold else False
    return {"acc": 1.0 if ok else 0.0, "consistency_pass": ok}


def _score_default(item: TaskItem, pred: str) -> Dict[str, Any]:
    return {"acc": 0.0, "consistency_pass": False}


def score_item(item: TaskItem, model_out: Dict[str, Any]) -> Dict[str, Any]:
    pred = (model_out.get("content") or "").strip()

    if item.task_type == "equation":
        base = _score_equation(item, pred)
    elif item.task_type == "causal":
        base = _score_causal(item, pred)
    elif item.task_type == "qa":
        base = _score_qa(item, pred)
    else:
        base = _score_default(item, pred)

    # Offline, reproducible proxies tied to agent behavior.
    retrieved_docs = None
    try:
        retrieved_docs = ((model_out.get("agent") or {}).get("tool_obs") or {}).get("docs")
    except Exception:
        retrieved_docs = None

    novelty = novelty_against_retrieved_docs(pred, retrieved_docs)
    reasoning_depth = reasoning_depth_from_trace(model_out)
    efficiency = efficiency_from_usage(model_out.get("usage"))

    return {
        **base,
        "novelty": float(novelty),
        "reasoning_depth": float(reasoning_depth),
        "efficiency": float(efficiency),
    }
