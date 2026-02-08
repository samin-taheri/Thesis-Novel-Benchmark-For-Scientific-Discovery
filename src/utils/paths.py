from __future__ import annotations

from pathlib import Path


def project_root() -> Path:
    # src/utils/paths.py -> src/utils -> src -> project root
    return Path(__file__).resolve().parents[2]


def data_path(*parts: str) -> str:
    return str(project_root() / "data" / Path(*parts))
