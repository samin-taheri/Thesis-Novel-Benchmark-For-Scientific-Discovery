"""Consistency metric: threshold-based pass/fail derived from accuracy."""

from __future__ import annotations


def consistency_pass_from_acc(acc: float) -> bool:
    # Placeholder policy: treat acc>=0.8 as consistent.
    return float(acc) >= 0.8
