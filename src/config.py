from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

class ModelSpec(BaseModel):
    provider: str = Field(..., description="mock|openai|anthropic|google")
    model: str = "mock-science-001"
    temperature: float = 0.0
    top_p: float = 1.0
    max_tokens: int = 1024
    tools: List[str] = []   # e.g., ["python", "retrieval", "oracle"]

class ScenarioSpec(BaseModel):
    name: str  # closed_book|tool_assisted|agentic_tool_use|decomposition|interactive
    params: Dict[str, Any] = {}

class DataSpec(BaseModel):
    loader: str  # autobench|baisbench|llm_srbench|scihorizon|researchbench|biodsa|synthetic
    path: Optional[str] = None
    limit: Optional[int] = 20

class ExperimentConfig(BaseModel):
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
