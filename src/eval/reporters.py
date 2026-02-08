import pandas as pd
from tabulate import tabulate

def save_reports(summary_df: pd.DataFrame, per_item_df: pd.DataFrame, run_id: str):
    summary_path = f"results/{run_id}_summary.csv"
    items_path = f"results/{run_id}_items.csv"
    md_path = f"results/{run_id}_report.md"
    summary_df.to_csv(summary_path, index=False)
    per_item_df.to_csv(items_path, index=False)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Benchmark Report\n\n")
        f.write("## Summary (by task_type × split)\n\n")
        f.write(tabulate(summary_df, headers='keys', tablefmt='github', showindex=False))
        f.write("\n\n## First 10 Items\n\n")
        f.write(tabulate(per_item_df.head(10), headers='keys', tablefmt='github', showindex=False))
