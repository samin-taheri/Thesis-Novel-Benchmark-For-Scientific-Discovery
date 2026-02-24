import argparse
import glob
import json
import os
from typing import Any, Dict, List

import pandas as pd
import yaml


def _safe_read_json(path: str) -> Dict[str, Any] | None:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def _safe_read_yaml(path: str) -> Dict[str, Any] | None:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception:
        return None


def _flatten_dict(d: Dict[str, Any], prefix: str = "", sep: str = ".") -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for k, v in (d or {}).items():
        key = f"{prefix}{sep}{k}" if prefix else str(k)
        if isinstance(v, dict):
            out.update(_flatten_dict(v, prefix=key, sep=sep))
        else:
            out[key] = v
    return out


def _extract_from_manifest(manifest: Dict[str, Any] | None) -> Dict[str, Any]:
    """Authoritative metadata from results/{run_id}_manifest.yaml."""
    if not manifest:
        return {}

    cfg = manifest.get("config", {}) or {}
    data = cfg.get("data", {}) or {}
    model = cfg.get("model", {}) or {}
    scenario = cfg.get("scenario", {}) or {}

    # Normalize loader names to match your study aggregate column naming.
    loader = data.get("loader")

    return {
        "run_id": manifest.get("run_id"),
        "timestamp": manifest.get("timestamp"),
        "config_path": manifest.get("config_path"),
        "benchmark": loader,
        "loader": loader,
        "provider": model.get("provider"),
        "model": model.get("model"),
        "scenario": scenario.get("name"),
        "random_seed": cfg.get("random_seed"),
        "data_path": data.get("path"),
        "data_limit": data.get("limit"),
    }


def _flatten_summary(summary_flat: Dict[str, Any] | None) -> Dict[str, Any]:
    # NEW metrics.json format stores summary under "summary_flat" (dict).
    # Keep as-is but lift keys to top-level for CSV friendliness.
    out: Dict[str, Any] = {}
    for k, v in (summary_flat or {}).items():
        out[k] = v
    return out


def aggregate(results_dir: str, include_env: bool = False) -> pd.DataFrame:
    metrics_paths = sorted(glob.glob(os.path.join(results_dir, "*_metrics.json")))
    rows: List[Dict[str, Any]] = []

    for mp in metrics_paths:
        run_id = os.path.basename(mp).replace("_metrics.json", "")
        metrics = _safe_read_json(mp) or {}

        manifest_path = os.path.join(results_dir, f"{run_id}_manifest.yaml")
        manifest = _safe_read_yaml(manifest_path)

        row: Dict[str, Any] = {}
        row.update(_extract_from_manifest(manifest))

        # Fallback if manifest missing.
        row.setdefault("run_id", run_id)

        # Attach basic run-level info and flattened metrics.
        row["n_items"] = metrics.get("n_items")
        row["tools_used_any"] = metrics.get("tools_used_any")
        row.update(_flatten_summary(metrics.get("summary_flat")))

        # Optional: include env/git metadata columns for auditing.
        if include_env and manifest and isinstance(manifest.get("env"), dict):
            row.update({f"env.{k}": v for k, v in _flatten_dict(manifest.get("env", {})).items()})

        rows.append(row)

    return pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", default="results", help="Results directory")
    ap.add_argument("--out", default=None, help="Output CSV path (default: results/aggregate_runs.csv)")
    ap.add_argument("--include-env", action="store_true", help="Include flattened env/git/pip columns")
    args = ap.parse_args()

    out_path = args.out or os.path.join(args.results, "aggregate_runs.csv")
    df = aggregate(args.results, include_env=args.include_env)
    df.to_csv(out_path, index=False)
    print(f"Wrote {out_path} ({len(df)} runs)")


if __name__ == "__main__":
    main()
