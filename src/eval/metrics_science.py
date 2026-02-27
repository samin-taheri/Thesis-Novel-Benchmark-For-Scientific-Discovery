"""Metric aggregation across task items.

Groups per-item scores by (task_type, split) and computes means.
"""

import pandas as pd


def summarize_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate per-item metrics into a summary table."""
    agg_map = {
        'acc': 'mean',
        'novelty': 'mean',
        'reasoning_depth': 'mean',
        'efficiency': 'mean',
        'consistency_pass': 'mean',
    }
    if 'shd' in df.columns:
        agg_map['shd'] = 'mean'

    agg = df.groupby(['task_type','split'], dropna=False).agg(agg_map).reset_index()
    agg = agg.rename(columns={'acc':'mean_acc','consistency_pass':'consistency_rate', 'shd': 'mean_shd'})
    return agg
