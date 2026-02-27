"""Reproducibility helper: fix global random seeds."""

import random

import numpy as np


def fix_seed(seed: int = 42) -> None:
    """Set Python and NumPy random seeds for reproducible runs."""
    random.seed(seed)
    np.random.seed(seed)
