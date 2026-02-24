#!/usr/bin/env python3
"""Generate an Auto-Bench-like offline dataset (numeric samples) for reproducible experiments.

This is used when the original Auto-Bench paper does not ship a public dataset.
It produces JSONL tasks compatible with `src/data/loaders/autobench_loader.py`.

Usage:
  python generate_autobench_dataset.py --out data/autobench/generated_autobench.jsonl --n 200
"""

from __future__ import annotations

import argparse

from src.data.generators.autobench_generator import AutoBenchGenConfig, generate_autobench_tasks, write_jsonl


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="data/autobench/generated_autobench.jsonl")
    ap.add_argument("--n", type=int, default=200)
    ap.add_argument("--nodes", type=int, default=6)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    cfg = AutoBenchGenConfig(n_tasks=args.n, n_nodes=args.nodes, seed=args.seed)
    items = generate_autobench_tasks(cfg)
    write_jsonl(args.out, items)
    print(f"Wrote {len(items)} tasks to {args.out}")


if __name__ == "__main__":
    main()
