from __future__ import annotations

import json
import random
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from ..schemas import TaskItem


def _rng(seed: int) -> random.Random:
    r = random.Random(seed)
    return r


def _sample_dag(nodes: List[str], edge_prob: float, r: random.Random) -> List[Tuple[str, str]]:
    """Sample an acyclic directed graph by only allowing edges i->j for i<j."""
    edges: List[Tuple[str, str]] = []
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if r.random() < edge_prob:
                edges.append((nodes[i], nodes[j]))
    return edges


def _parents(edges: List[Tuple[str, str]]) -> Dict[str, List[str]]:
    p: Dict[str, List[str]] = {}
    for u, v in edges:
        p.setdefault(v, []).append(u)
        p.setdefault(u, [])
    return p


def _simulate_linear_sem(
    nodes: List[str],
    edges: List[Tuple[str, str]],
    n: int,
    seed: int,
    interventions: Optional[Dict[str, float]] = None,
    noise_scale: float = 1.0,
) -> Dict[str, List[float]]:
    """Simulate samples from a simple linear SEM with Gaussian noise.

    Each node value is: x_v = sum_{p in Pa(v)} w_{p,v} * x_p + eps
    Interventions set x_v = constant.
    """
    interventions = interventions or {}

    rs = np.random.RandomState(seed)

    # sample weights for edges
    w: Dict[Tuple[str, str], float] = {}
    for (u, v) in edges:
        w[(u, v)] = float(rs.uniform(-2.0, 2.0))

    parents = _parents(edges)

    data: Dict[str, List[float]] = {v: [] for v in nodes}

    # topological order is nodes order (edges only i<j)
    for t in range(n):
        x: Dict[str, float] = {}
        for v in nodes:
            if v in interventions:
                x[v] = float(interventions[v])
                continue
            s = 0.0
            for p in parents.get(v, []):
                s += w[(p, v)] * x[p]
            eps = float(rs.normal(0.0, noise_scale))
            x[v] = s + eps
        for v in nodes:
            data[v].append(float(x[v]))

    return data


@dataclass
class AutoBenchGenConfig:
    n_tasks: int = 200
    n_nodes: int = 6
    edge_prob_iid: float = 0.25
    edge_prob_ood: float = 0.45
    n_obs: int = 64
    n_int: int = 64
    noise_scale: float = 1.0
    seed: int = 42
    domain: str = "physics"


def generate_autobench_tasks(cfg: AutoBenchGenConfig) -> List[TaskItem]:
    """Generate Auto-Bench-like interactive causal discovery tasks.

    Output TaskItem.task_type == 'causal'
    - input.observational: samples without intervention
    - input.interventional: a small intervention menu (one intervention per node)
    - gold.edges: ground-truth DAG

    Splits:
    - first half iid, second half ood (different graph density)
    """
    r = _rng(cfg.seed)

    items: List[TaskItem] = []
    for i in range(cfg.n_tasks):
        split = "iid" if i < (cfg.n_tasks // 2) else "ood"
        edge_prob = cfg.edge_prob_iid if split == "iid" else cfg.edge_prob_ood

        nodes = [chr(ord("A") + k) for k in range(cfg.n_nodes)]
        edges = _sample_dag(nodes, edge_prob=edge_prob, r=r)

        obs = _simulate_linear_sem(
            nodes,
            edges,
            n=cfg.n_obs,
            seed=cfg.seed * 100000 + i,
            interventions=None,
            noise_scale=cfg.noise_scale,
        )

        # define a menu of simple interventions do(V=+2.0)
        intervention_menu: List[Dict[str, Any]] = []
        for v in nodes:
            int_data = _simulate_linear_sem(
                nodes,
                edges,
                n=cfg.n_int,
                seed=cfg.seed * 100000 + i + 999,
                interventions={v: 2.0},
                noise_scale=cfg.noise_scale,
            )
            intervention_menu.append(
                {
                    "do": {v: 2.0},
                    "samples": int_data,
                }
            )

        prompt = (
            "You are performing interactive causal discovery. You are given an observational dataset, "
            "and you may request one interventional dataset of the form do(V=2.0) from the oracle. "
            "Infer the directed causal edges among nodes."
        )

        items.append(
            TaskItem(
                id=f"abgen-{split}-{i:04d}",
                domain=cfg.domain,
                task_type="causal",
                input={
                    "prompt": prompt,
                    "nodes": nodes,
                    "observational": obs,
                    "intervention_menu": intervention_menu,
                },
                gold={"edges": [[u, v] for (u, v) in edges]},
                split=split,
            )
        )

    return items


def write_jsonl(path: str, items: List[TaskItem]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for it in items:
            d = it.model_dump()
            f.write(json.dumps(d, ensure_ascii=False) + "\n")
