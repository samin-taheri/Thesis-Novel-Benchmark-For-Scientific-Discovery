"""Logging configuration for experiment runs."""

import logging
import os


def get_logger(name: str, run_id: str) -> logging.Logger:
    """Return a logger that writes to both a run-specific file and stderr."""
    os.makedirs("logs", exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        fh = logging.FileHandler(f"logs/{run_id}.log", encoding="utf-8")
        ch = logging.StreamHandler()
        fmt = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
        fh.setFormatter(fmt); ch.setFormatter(fmt)
        logger.addHandler(fh); logger.addHandler(ch)
    return logger
