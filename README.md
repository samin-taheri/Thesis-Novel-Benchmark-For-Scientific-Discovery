# TOWARDS A NOVEL BENCHMARK FOR AUTONOMOUS SCIENTIFIC DISCOVERY: A COMPARATIVE EVALUATION

## What This Project Does

This project is a **benchmarking framework** that systematically evaluates how well Large Language Models (LLMs) perform on scientific discovery tasks. It answers the research question:

> *How do state-of-the-art LLMs compare when asked to perform core scientific reasoning — discovering equations from data, inferring causal graphs, answering science questions, and proposing research hypotheses?*

The framework runs **controlled experiments** across multiple LLM providers (OpenAI GPT-3.5/GPT-4, Anthropic Claude, Google Gemini) on five benchmark families, under identical conditions, and produces quantitative metrics and reproducible reports.

### Purpose

In a typical thesis evaluation you need to:
1. **Compare models fairly** — same data, same prompts, same scoring.
2. **Measure multiple dimensions** — not just accuracy, but also novelty, reasoning depth, consistency, and token efficiency.
3. **Produce reproducible evidence** — every run generates a manifest (exact config, git commit, dependency snapshot) so results can be independently verified.

This framework automates all three.

### How It Works

The pipeline has five stages, driven by a single YAML configuration file:

```
┌─────────────┐     ┌──────────────┐     ┌────────────┐     ┌───────────┐     ┌───────────┐
│ 1. Load Data│ ──▶ │ 2. Build     │ ──▶ │ 3. Call LLM│ ──▶ │ 4. Score  │ ──▶ │ 5. Report │
│   (loader)  │     │    Prompt    │     │  (adapter) │     │  (judge)  │     │  (CSV+MD) │
│             │     │  (scenario)  │     │            │     │           │     │           │
└─────────────┘     └──────────────┘     └────────────┘     └───────────┘     └───────────┘
```

1. **Data Loading** — A loader reads benchmark tasks from JSONL files into a common `TaskItem` schema. Each task has an ID, domain, task type, input data, and gold-standard answer.

2. **Prompt Construction** — A scenario module (e.g. closed-book, tool-assisted, decomposition) transforms the task into a prompt appropriate for the evaluation mode.

3. **LLM Inference** — An adapter sends the prompt to the chosen provider's API and returns the model's response with token usage metadata.

4. **Scoring** — A judge module compares the model output against the gold standard. For equations it checks numeric equivalence; for causal graphs it computes edge precision/recall/F1 and structural Hamming distance (SHD); for QA it checks answer containment. Cross-cutting metrics (novelty, reasoning depth, efficiency) are computed for every task.

5. **Reporting** — Results are saved as per-item CSV, aggregated summary CSV, a human-readable Markdown report, a machine-readable metrics JSON, and a full manifest YAML recording the exact environment.

### Benchmarks Included

| Benchmark     | Task Type       | Domain          | What It Tests                                    |
|---------------|-----------------|-----------------|--------------------------------------------------|
| AutoBench     | Causal discovery| Physics/general | Inferring causal DAGs from variables              |
| LLM-SRBench   | Equation finding| Physics         | Symbolic regression — discovering y = f(x)        |
| SciHorizon    | Science QA      | Multi-domain    | Factual scientific knowledge                      |
| ResearchBench | Hypothesis gen. | Biology/physics | Proposing testable hypotheses from paper contexts |
| BaisBench     | Bio analysis    | Biology         | Gene expression analysis and experiment design    |

### Metrics Measured

| Metric            | Description                                                       |
|-------------------|-------------------------------------------------------------------|
| **Accuracy**      | Task-specific correctness (numeric MSE, edge F1, answer match)    |
| **Novelty**       | Non-copying score — how much the answer diverges from source text |
| **Reasoning Depth** | Proxy based on rationale length and structured planning          |
| **Efficiency**    | Token economy — lower token usage scores higher                   |
| **Consistency**   | Whether accuracy exceeds a reliability threshold                  |
| **SHD** (causal)  | Structural Hamming Distance for causal graph tasks                |

### Evaluation Scenarios

| Scenario          | Description                                                    |
|-------------------|----------------------------------------------------------------|
| **Closed-book**   | Pure reasoning — no tools, no retrieval                         |
| **Tool-assisted** | Model may use a calculator/code evaluator                      |
| **Agentic**       | Multi-step loop: Think → Tool-call → Observe → Answer          |
| **Decomposition** | Plan → Decompose → Solve → Synthesize                          |
| **Interactive**   | Simulated multi-turn intervention and hypothesis revision       |

---

## Quick Start

```bash
# 1. Create environment
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. Configure API keys
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY

# 3. Run an experiment
python run_experiment.py experiments/example_autobench.yaml
```

Outputs are written to `results/` (CSV summaries, Markdown reports, JSON metrics, YAML manifests).
Logs are written to `logs/`.

### Running the Full Study Matrix

To run all 20 study configurations (5 benchmarks × 4 models) at once:

```bash
for cfg in experiments/study_*_closed_book.yaml; do
    echo "[RUN] $cfg"
    python run_experiment.py "$cfg"
done
```

Each run produces timestamped output files so results never overwrite each other.

---

## Project Structure

```
run_experiment.py              ← CLI entry point
src/
├── config.py                  ← Pydantic models for experiment YAML validation
├── adapters/                  ← LLM provider adapters (OpenAI, Anthropic, Google)
│   ├── base.py                ← Abstract base class all adapters implement
│   ├── openai_adapter.py
│   ├── anthropic_adapter.py
│   └── google_adapter.py
├── data/
│   ├── schemas.py             ← TaskItem data model (common schema for all benchmarks)
│   ├── loaders/               ← One loader per benchmark family (JSONL → TaskItem)
│   └── generators/            ← Synthetic data generators for testing
├── scenarios/                 ← Prompt/workflow strategies
│   ├── closed_book.py
│   ├── tool_assisted.py
│   ├── agentic_tool_use.py
│   ├── decomposition.py
│   └── interactive.py
├── eval/                      ← Scoring and reporting
│   ├── evaluator.py           ← Main evaluation loop
│   ├── judge_science.py       ← Per-item scoring dispatcher
│   ├── metrics_science.py     ← Aggregation (group-by task_type × split)
│   ├── causal_metrics.py      ← Edge precision/recall/F1/SHD
│   ├── novelty.py             ← N-gram overlap novelty proxy
│   ├── reasoning.py           ← Reasoning depth proxy
│   ├── efficiency.py          ← Token efficiency scorer
│   ├── consistency.py         ← Consistency threshold check
│   └── reporters.py           ← CSV/Markdown/JSON output writers
├── tools/                     ← Offline tools for agentic scenarios
│   ├── tool_registry.py       ← Tool dispatcher
│   ├── python_tool.py         ← Restricted expression evaluator
│   ├── retrieval_tool.py      ← Keyword-overlap document retrieval
│   └── oracle_tool.py         ← Interventional data oracle (causal tasks)
└── utils/                     ← Shared helpers
    ├── io.py, logging.py, paths.py, random_seed.py, text.py
experiments/                   ← YAML experiment configurations
data/                          ← Benchmark dataset files (JSONL)
results/                       ← Generated output artifacts (git-ignored)
logs/                          ← Run logs (git-ignored)
docs/                          ← Protocol documentation and checklists
```

---

## Output Artifacts

Each run produces five files in `results/`, prefixed with a unique run ID:

| File                  | Content                                              |
|-----------------------|------------------------------------------------------|
| `*_summary.csv`       | Aggregated metrics grouped by task type and split     |
| `*_items.csv`         | Per-item predictions, scores, and token usage         |
| `*_report.md`         | Human-readable Markdown report with tables            |
| `*_metrics.json`      | Machine-readable flattened metrics for aggregation    |
| `*_manifest.yaml`     | Full reproducibility record (config, git hash, deps)  |
