"""Output writers for experiment results.

Produces four artifacts per run:
  - summary CSV   (aggregated metrics by task type / split)
  - items CSV     (per-item predictions, scores, token usage)
  - report MD     (human-readable Markdown tables)
  - metrics JSON  (machine-readable flat metrics for cross-run aggregation)
"""

import json

import pandas as pd
from tabulate import tabulate

def _flatten_summary(summary_df: pd.DataFrame) -> dict:
    """Flatten summary metrics by (task_type, split) into a single dict.

    Example column naming:
      mean_acc -> mean_acc__causal__iid
    """
    if summary_df is None or summary_df.empty:
        return {}

    key_cols = [c for c in ["task_type", "split"] if c in summary_df.columns]
    metric_cols = [c for c in summary_df.columns if c not in key_cols]

    out: dict = {}
    for _, r in summary_df.iterrows():
        key = "__".join(str(r[c]) for c in key_cols) if key_cols else "all"
        for m in metric_cols:
            v = r[m]
            # Convert numpy/pandas scalars to native Python for JSON serialization.
            try:
                v = v.item()  # type: ignore[attr-defined]
            except Exception:
                pass
            out[f"{m}__{key}"] = v
    return out

def save_reports(summary_df: pd.DataFrame, per_item_df: pd.DataFrame, run_id: str):
    summary_path = f"results/{run_id}_summary.csv"
    items_path = f"results/{run_id}_items.csv"
    md_path = f"results/{run_id}_report.md"
    metrics_path = f"results/{run_id}_metrics.json"

    summary_df.to_csv(summary_path, index=False)
    per_item_df.to_csv(items_path, index=False)

    # Machine-friendly one-row metrics artifact for aggregation.
    metrics = {
        "run_id": run_id,
        "n_items": int(len(per_item_df)) if per_item_df is not None else None,
        "tools_used_any": bool(per_item_df.get("agent_tool").notna().any()) if per_item_df is not None and "agent_tool" in per_item_df.columns else None,
        "summary_flat": _flatten_summary(summary_df),
    }
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Benchmark Report\n\n")
        f.write("## Summary (by task_type / split)\n\n")
        f.write(tabulate(summary_df, headers='keys', tablefmt='github', showindex=False))
        f.write("\n\n## First 10 Items\n\n")
        f.write(tabulate(per_item_df.head(10), headers='keys', tablefmt='github', showindex=False))
