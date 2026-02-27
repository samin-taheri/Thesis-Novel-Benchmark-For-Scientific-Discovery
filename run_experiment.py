"""CLI entry point for running a single benchmark experiment.

Usage:
    python run_experiment.py experiments/<config>.yaml

The runner reads the YAML config, initialises the evaluator, executes the
benchmark, and writes all output artifacts to ``results/``.
"""

import argparse
import os
import platform
import subprocess
import sys
import time
from typing import List, Optional

import yaml
from dotenv import load_dotenv

from src.config import ExperimentConfig
from src.eval.evaluator import Evaluator
from src.eval.reporters import save_reports
from src.utils.io import ensure_dirs


def _slug(s: str) -> str:
    return (s or "").strip().lower().replace(" ", "-").replace("_", "-")


def _git_metadata() -> dict:
    """Return git commit + dirty flag if available; otherwise None values."""

    def _run(cmd: List[str]) -> str:
        return subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode("utf-8").strip()

    try:
        commit = _run(["git", "rev-parse", "HEAD"])
        try:
            status = _run(["git", "status", "--porcelain"])
            dirty = bool(status)
        except Exception:
            dirty = None
        return {"commit": commit, "dirty": dirty}
    except Exception:
        return {"commit": None, "dirty": None}


def _pip_freeze() -> Optional[List[str]]:
    """Best-effort dependency snapshot."""
    try:
        out = subprocess.check_output([sys.executable, "-m", "pip", "freeze"]).decode("utf-8")
        return [ln.strip() for ln in out.splitlines() if ln.strip()]
    except Exception:
        return None


def _write_manifest(run_id: str, cfg_path: str, raw_cfg: dict):
    manifest = {
        "run_id": run_id,
        "timestamp": int(time.time()),
        "config_path": os.path.abspath(cfg_path),
        "config": raw_cfg,
        "env": {
            "python": sys.version,
            "executable": sys.executable,
            "platform": platform.platform(),
            "git": _git_metadata(),
            "pip_freeze": _pip_freeze(),
        },
    }
    out_path = os.path.join("results", f"{run_id}_manifest.yaml")
    with open(out_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(manifest, f, sort_keys=False, allow_unicode=True)


def main(cfg_path: str):
    # Load environment variables from .env files in the project root (if present).
    # Existing shell environment variables are preserved.
    load_dotenv()

    with open(cfg_path, 'r', encoding='utf-8') as f:
        raw = yaml.safe_load(f)
    cfg = ExperimentConfig(**raw)

    # Thesis-grade run_id: timestamp + cfg.name + structured tags so downstream aggregation is reliable.
    # Example:
    #   1700000000_autobench-study_autobench_openai_gpt4_agentic-tool-use
    ts = int(time.time())
    tag_parts = [
        _slug(cfg.name),
        _slug(cfg.data.loader),
        _slug(cfg.model.provider),
        _slug(cfg.model.model),
        _slug(cfg.scenario.name),
    ]
    tag_parts = [p for p in tag_parts if p]
    run_id = f"{ts}_" + "_".join(tag_parts)

    ensure_dirs(['results', 'logs'])
    _write_manifest(run_id, cfg_path, raw)

    evaluator = Evaluator(cfg, run_id=run_id)
    summary_df, per_item_df = evaluator.run()

    save_reports(summary_df, per_item_df, run_id)

    print(f"✔ Done. See results/{run_id}_summary.csv and results/{run_id}_report.md")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Path to experiment YAML")
    args = parser.parse_args()
    main(args.config)
