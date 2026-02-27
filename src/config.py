"""Pydantic configuration models for experiment YAML files.

Each experiment is fully described by an `ExperimentConfig` instance that
validates the YAML at load time and provides typed access to all settings.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List


class ModelSpec(BaseModel):
    """LLM provider and generation parameters."""

    provider: str = Field(..., description="openai | anthropic | google | mock")
    model: str = "gpt-3.5-turbo"
    temperature: float = 0.0
    top_p: float = 1.0
    max_tokens: int = 1024
    tools: List[str] = []   # e.g., ["python", "retrieval", "oracle"]

class ScenarioSpec(BaseModel):
    """Evaluation scenario selection and optional parameters."""

    name: str  # closed_book | tool_assisted | agentic_tool_use | decomposition | interactive
    params: Dict[str, Any] = {}

class DataSpec(BaseModel):
    """Dataset loader configuration."""

    loader: str  # autobench | baisbench | llm_srbench | scihorizon | researchbench | biodsa | synthetic
    path: Optional[str] = None
    limit: Optional[int] = 20

class ExperimentConfig(BaseModel):
    """Top-level experiment configuration validated from YAML."""

    name: str
    description: str = ""
    random_seed: int = 42
    data: DataSpec
    model: ModelSpec
    scenario: ScenarioSpec
    metrics: Dict[str, Any] = {
        "novelty": {"enabled": True},
        "generalization": {"enabled": True},
        "consistency": {"enabled": True},
        "reasoning_depth": {"enabled": True},
        "efficiency": {"enabled": True}
    }
