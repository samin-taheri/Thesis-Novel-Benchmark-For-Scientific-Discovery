from .autobench_loader import load_autobench
from .llm_srbench_loader import load_llm_srbench
from .scihorizon_loader import load_scihorizon
from .researchbench_loader import load_researchbench
from .biodsa_loader import load_biodsa
from .synthetic_loader import load_synthetic
from .baisbench_loader import load_baisbench

# Adapter class wrappers for the loader functions
class SyntheticLoader:
    def load(self, path=None, limit=10):
        return load_synthetic(path, limit)

class AutobenchLoader:
    def load(self, path=None, limit=None):
        return load_autobench(path, limit)

class LLMSRBenchLoader:
    def load(self, path=None, limit=None):
        return load_llm_srbench(path, limit)

class SciHorizonLoader:
    def load(self, path=None, limit=None):
        return load_scihorizon(path, limit)

class ResearchBenchLoader:
    def load(self, path=None, limit=None):
        return load_researchbench(path, limit)

class BioDSALoader:
    def load(self, path=None, limit=None):
        return load_biodsa(path, limit)

class BaisBenchLoader:
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
