"""Text processing utilities for parsing model outputs."""

from __future__ import annotations

import re
from typing import List, Tuple


def normalize_edge(u: str, v: str) -> str:
    return f"{u.strip()}->{v.strip()}"


def extract_edges(text: str) -> List[str]:
    """Extract directed edges from free-form model text.

    Supports patterns like:
    - A->B
    - A -> B
    - (A,B)
    - A,B

    Returns normalized strings "A->B".
    """
    if not text:
        return []

    t = text.replace("→", "->")

    edges: List[Tuple[str, str]] = []

    # A->B patterns
    for m in re.finditer(r"([A-Za-z][A-Za-z0-9_]*)\s*->\s*([A-Za-z][A-Za-z0-9_]*)", t):
        edges.append((m.group(1), m.group(2)))

    # (A,B) patterns
    for m in re.finditer(r"\(\s*([A-Za-z][A-Za-z0-9_]*)\s*,\s*([A-Za-z][A-Za-z0-9_]*)\s*\)", t):
        edges.append((m.group(1), m.group(2)))

    # {A,B} heuristic: only if it looks like edge list "{A,B} {B,C}" is too ambiguous; skip.

    return [normalize_edge(u, v) for u, v in edges]
