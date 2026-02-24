#!/usr/bin/env python3
"""Aggregate and compare results across many experiment runs.

This script produces a study-level view:
- loads all `results/*_summary.csv`
- uses `results/{run_id}_manifest.yaml` as authoritative metadata when available
- falls back to best-effort parsing of `run_id` when no manifest exists
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
from typing import Dict, Any

import pandas as pd
import yaml


def _infer_tags_from_run_id(run_id: str) -> Dict[str, str]:
    """Best-effort parsing of `<timestamp>_<experiment-name>` into tags.

    Kept only as a fallback when no manifest is found.
    """

    name = run_id.split("_", 1)[-1]
    tokens = name.lower().replace("-", "_").split("_")

    provider = next((t for t in tokens if t in {"mock", "openai", "anthropic", "google"}), "unknown")

    model = "unknown"
    if "gpt4" in tokens or "gpt_4" in tokens:
        model = "gpt4"
        provider = "openai" if provider == "unknown" else provider
    elif "gpt35" in tokens or "gpt3" in tokens or "gpt_35" in tokens or "gpt_3_5" in tokens:
        model = "gpt35"
        provider = "openai" if provider == "unknown" else provider
    elif "gemini" in tokens:
        model = "gemini"
        provider = "google" if provider == "unknown" else provider
    elif "claude" in tokens:
        model = "claude"
        provider = "anthropic" if provider == "unknown" else provider

    scenario_tokens = {
        "closed",
        "closedbook",
        "closed_book",
        "tool",
        "tool_assisted",
        "agentic",
        "agentic_tool_use",
        "interactive",
        "decomposition",
        "oracle",
        "oracle_agentic",
    }
    scenario = next((t for t in tokens if t in scenario_tokens), "unknown")
    if scenario == "tool":
        scenario = "tool_assisted"
    if scenario in {"closed", "closedbook"}:
        scenario = "closed_book"
    if scenario == "agentic":
        scenario = "agentic_tool_use"
    if "oracle" in tokens and "agentic" in tokens:
        scenario = "agentic_tool_use"

    benchmark = "unknown"
    for b in ["autobench", "llm_srbench", "srbench", "llm", "scihorizon", "researchbench", "baisbench"]:
        if b in name.lower():
            benchmark = "llm_srbench" if b in {"llm", "srbench"} else b
            break

    return {"experiment": name, "provider": provider, "model": model, "scenario": scenario, "benchmark": benchmark}


def _read_manifest_tags(results_dir: Path, run_id: str) -> Dict[str, Any] | None:
    mpath = results_dir / f"{run_id}_manifest.yaml"
    if not mpath.exists():
        return None
    try:
        manifest = yaml.safe_load(mpath.read_text(encoding="utf-8")) or {}
        cfg = (manifest.get("config") or {})
        data = (cfg.get("data") or {})
        model = (cfg.get("model") or {})
        scenario = (cfg.get("scenario") or {})
        # Use loader as the benchmark label (matches your thesis tables)
        return {
            "experiment": cfg.get("name") or run_id,
            "benchmark": data.get("loader") or "unknown",
            "provider": model.get("provider") or "unknown",
            "model": model.get("model") or "unknown",
            "scenario": scenario.get("name") or "unknown",
        }
    except Exception:
        return None


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

        tags = _read_manifest_tags(results_dir, run_id) or _infer_tags_from_run_id(run_id)
        for k, v in tags.items():
            df[k] = v
        df["run_id"] = run_id
        frames.append(df)

    all_df = pd.concat(frames, ignore_index=True)

    metric_cols = [
        c
        for c in ["mean_acc", "mean_shd", "novelty", "reasoning_depth", "efficiency", "consistency_rate"]
        if c in all_df.columns
    ]
    group_cols = ["benchmark", "provider", "model", "scenario", "task_type", "split"]

    agg = (
        all_df.groupby(group_cols, dropna=False)[metric_cols]
        .mean(numeric_only=True)
        .reset_index()
        .sort_values(group_cols)
    )

    print("📊 Aggregated Results (grouped)")
    print("=" * 80)
    print(agg.to_string(index=False))

    if {"mean_acc"} <= set(agg.columns):
        sort_cols = ["mean_acc"]
        sort_asc = [False]
        if "mean_shd" in agg.columns:
            sort_cols.append("mean_shd")
            sort_asc.append(True)

        ranked = (
            agg.sort_values(
                ["benchmark", "scenario", "task_type", "split", *sort_cols],
                ascending=[True, True, True, True, *sort_asc],
            )
            .groupby(["benchmark", "scenario", "task_type", "split"], dropna=False)
            .head(10)
        )

        print("\n🏁 Top models per benchmark (ranked by mean_acc, then mean_shd)")
        print("=" * 80)
        cols = [
            c
            for c in [
                "benchmark",
                "scenario",
                "task_type",
                "split",
                "provider",
                "model",
                "mean_acc",
                "mean_shd",
                "consistency_rate",
            ]
            if c in ranked.columns
        ]
        print(ranked[cols].to_string(index=False))

    if "split" in agg.columns and set(agg["split"].astype(str).str.lower().unique()) & {"iid", "ood"}:
        try:
            pivot = (
                agg.pivot_table(
                    index=["benchmark", "provider", "model", "scenario", "task_type"],
                    columns="split",
                    values="mean_acc",
                    aggfunc="mean",
                )
                .reset_index()
            )
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
