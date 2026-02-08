import os, json, pathlib
from typing import List, Any, Dict

def ensure_dirs(names: List[str]):
    for n in names:
        os.makedirs(n, exist_ok=True)

def write_jsonl(path: str, rows: List[Dict[str, Any]]):
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
