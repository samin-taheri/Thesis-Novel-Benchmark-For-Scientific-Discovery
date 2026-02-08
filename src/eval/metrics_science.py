import pandas as pd

def summarize_metrics(df: pd.DataFrame) -> pd.DataFrame:
    agg = df.groupby(['task_type','split'], dropna=False).agg({
        'acc':'mean',
        'novelty':'mean',
        'reasoning_depth':'mean',
        'efficiency':'mean',
        'consistency_pass':'mean'
    }).reset_index()
    agg = agg.rename(columns={'acc':'mean_acc','consistency_pass':'consistency_rate'})
    return agg
