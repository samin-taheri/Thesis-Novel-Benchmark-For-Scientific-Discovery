#!/usr/bin/env python3
"""Aggregate and compare results across many experiment runs.

This replaces the old "mock vs openai" sanity-check with a study-level view:
- loads all `results/*_summary.csv`
- parses `run_id` to infer benchmark/model/scenario (best-effort)
- outputs grouped tables you can paste into the thesis

Usage:
  python compare_results.py

Optional:
  Set `ONLY_MATCH` env var to filter run_ids (substring match), e.g.
    ONLY_MATCH=autobench python compare_results.py
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Dict

import pandas as pd


def _infer_tags_from_run_id(run_id: str) -> Dict[str, str]:
    """Best-effort parsing of `<timestamp>_<experiment-name>` into tags."""
    name = run_id.split("_", 1)[-1]
    tokens = name.lower().replace("-", "_").split("_")

    # crude heuristics based on common naming in `experiments/*.yaml`
    provider = next((t for t in tokens if t in {"mock", "openai", "anthropic", "google", "gemini", "claude"}), "unknown")
    scenario = next((t for t in tokens if t in {"closed", "closedbook", "tool", "tool_assisted", "interactive", "decomposition"}), "unknown")

    benchmark = "unknown"
    for b in ["autobench", "llm", "srbench", "llm_srbench", "scihorizon", "researchbench", "baisbench"]:
        if b in name.lower():
            benchmark = "llm_srbench" if b in {"llm", "srbench"} else b
            break

    # normalize some tokens
    if scenario == "tool":
        scenario = "tool_assisted"
    if scenario in {"closed", "closedbook"}:
        scenario = "closed_book"

    return {
        "experiment": name,
        "provider": provider,
        "scenario": scenario,
        "benchmark": benchmark,
    }


def main() -> None:
    results_dir = Path("results")
    if not results_dir.exists():
        print("❌ No results/ directory found.")
        return

    only = os.getenv("ONLY_MATCH")

    summary_files = sorted(results_dir.glob("*_summary.csv"))
    if only:
        summary_files = [p for p in summary_files if only in p.name]

    if not summary_files:
        print("❌ No summary CSVs found in results/. Run at least one experiment first.")
        return

    frames = []
    for p in summary_files:
        run_id = p.name.replace("_summary.csv", "")
        df = pd.read_csv(p)
        tags = _infer_tags_from_run_id(run_id)
        for k, v in tags.items():
            df[k] = v
        df["run_id"] = run_id
        frames.append(df)

    all_df = pd.concat(frames, ignore_index=True)

    # Thesis-friendly pivot: mean metrics grouped by (benchmark, provider, scenario, task_type, split)
    metric_cols = [c for c in ["mean_acc", "novelty", "reasoning_depth", "efficiency", "consistency_rate"] if c in all_df.columns]
    group_cols = ["benchmark", "provider", "scenario", "task_type", "split"]

    agg = (
        all_df.groupby(group_cols, dropna=False)[metric_cols]
        .mean(numeric_only=True)
        .reset_index()
        .sort_values(group_cols)
    )

    print("📊 Aggregated Results (grouped)")
    print("=" * 80)
    print(agg.to_string(index=False))

    # Quick generalization view if split contains iid/ood
    if "split" in agg.columns and set(agg["split"].astype(str).str.lower().unique()) & {"iid", "ood"}:
        try:
            pivot = agg.pivot_table(
                index=["benchmark", "provider", "scenario", "task_type"],
                columns="split",
                values="mean_acc",
                aggfunc="mean",
            ).reset_index()
            if "iid" in pivot.columns and "ood" in pivot.columns:
                pivot["gen_gap_iid_minus_ood"] = pivot["iid"] - pivot["ood"]
            print("\n📉 Generalization (IID vs OOD on mean_acc)")
            print("=" * 80)
            print(pivot.to_string(index=False))
        except Exception:
            pass

    out_path = results_dir / "_study_aggregate.csv"
    agg.to_csv(out_path, index=False)
    print(f"\n✅ Wrote aggregated table to: {out_path}")


if __name__ == "__main__":
    main()
