import pandas as pd

def summarize_metrics(df: pd.DataFrame) -> pd.DataFrame:
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
