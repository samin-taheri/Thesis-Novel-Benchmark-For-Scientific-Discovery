"""Benchmark data loaders.

Each loader reads a JSONL dataset file and returns a list of `TaskItem` instances.
The `LOADERS` dict maps loader names (used in experiment YAMLs) to wrapper classes
that the evaluator can instantiate.
"""

from .autobench_loader import load_autobench
from .llm_srbench_loader import load_llm_srbench
from .scihorizon_loader import load_scihorizon
from .researchbench_loader import load_researchbench
from .biodsa_loader import load_biodsa
from .synthetic_loader import load_synthetic
from .baisbench_loader import load_baisbench


# ---------------------------------------------------------------------------
# Thin wrapper classes so the evaluator can call  loader(path, limit)
# directly via the LOADER_MAP without knowing the function signature.
# ---------------------------------------------------------------------------

class SyntheticLoader:
    """Generates minimal synthetic tasks for pipeline dry-runs."""
    def load(self, path=None, limit=10):
        return load_synthetic(path, limit)


class AutobenchLoader:
    """Loads AutoBench causal-discovery tasks from JSONL."""
    def load(self, path=None, limit=None):
        return load_autobench(path, limit)


class LLMSRBenchLoader:
    """Loads LLM-SRBench symbolic regression tasks from JSONL."""
    def load(self, path=None, limit=None):
        return load_llm_srbench(path, limit)


class SciHorizonLoader:
    """Loads SciHorizon science QA tasks from JSONL."""
    def load(self, path=None, limit=None):
        return load_scihorizon(path, limit)


class ResearchBenchLoader:
    """Loads ResearchBench hypothesis-generation tasks from JSONL."""
    def load(self, path=None, limit=None):
        return load_researchbench(path, limit)


class BioDSALoader:
    """Loads BioDSA biological analysis tasks from JSONL."""
    def load(self, path=None, limit=None):
        return load_biodsa(path, limit)


class BaisBenchLoader:
    """Loads BaisBench gene-expression analysis tasks from JSONL."""
    def load(self, path=None, limit=None):
        return load_baisbench(path, limit)


LOADERS = {
    "synthetic": SyntheticLoader,
    "autobench": AutobenchLoader,
    "llm_srbench": LLMSRBenchLoader,
    "scihorizon": SciHorizonLoader,
    "researchbench": ResearchBenchLoader,
    "biodsa": BioDSALoader,
    "baisbench": BaisBenchLoader,
}
