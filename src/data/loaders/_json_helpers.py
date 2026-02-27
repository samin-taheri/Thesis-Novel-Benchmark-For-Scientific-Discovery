"""Helpers for reading JSON and JSONL dataset files."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, List


def read_json_or_jsonl(path: str) -> List[Dict[str, Any]]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Dataset path not found: {path}")

    if p.suffix.lower() == ".jsonl":
        rows: List[Dict[str, Any]] = []
        with p.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                rows.append(json.loads(line))
        return rows

    if p.suffix.lower() == ".json":
        with p.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        raise ValueError("Expected a JSON list at top-level")

    raise ValueError("Unsupported dataset format. Use .jsonl or .json")
