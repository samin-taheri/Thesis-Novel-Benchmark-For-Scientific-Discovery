import argparse, yaml, time
from src.config import ExperimentConfig
from src.utils.io import ensure_dirs
from src.eval.evaluator import Evaluator
from src.eval.reporters import save_reports

def main(cfg_path: str):
    with open(cfg_path, 'r', encoding='utf-8') as f:
        raw = yaml.safe_load(f)
    cfg = ExperimentConfig(**raw)

    run_id = f"{int(time.time())}_{cfg.name}"
    ensure_dirs(['results', 'logs'])

    evaluator = Evaluator(cfg, run_id=run_id)
    summary_df, per_item_df = evaluator.run()

    save_reports(summary_df, per_item_df, run_id)

    print(f"✔ Done. See results/{run_id}_summary.csv and results/{run_id}_report.md")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Path to experiment YAML")
    args = parser.parse_args()
    main(args.config)
