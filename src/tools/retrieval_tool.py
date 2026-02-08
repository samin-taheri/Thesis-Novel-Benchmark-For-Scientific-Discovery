from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class RetrievalTool:
    """Tiny offline retrieval tool over a local JSONL corpus.

    Scoring is simple keyword overlap (no heavy dependencies). This keeps the
    benchmark harness reproducible and offline.
    """

    corpus_path: str
    name: str = "retrieval"

    def _load(self) -> List[Dict[str, Any]]:
        docs: List[Dict[str, Any]] = []
        p = Path(self.corpus_path)
        if not p.exists():
            return docs
        with p.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                docs.append(json.loads(line))
        return docs

    def search(self, query: str, k: int = 3, domain: Optional[str] = None) -> List[Dict[str, Any]]:
        q = (query or "").lower()
        q_terms = {t for t in q.replace("/", " ").replace("=", " ").replace("*", " ").split() if len(t) > 2}

        scored: List[tuple[float, Dict[str, Any]]] = []
        for d in self._load():
            if domain and str(d.get("domain", "")).lower() != str(domain).lower():
                continue
            text = f"{d.get('title','')}\n{d.get('text','')}".lower()
            terms = {t for t in text.split() if len(t) > 2}
            overlap = len(q_terms & terms)
            score = float(overlap) / max(1.0, float(len(q_terms)))
            if score > 0:
                scored.append((score, d))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [d for _, d in scored[:k]]
