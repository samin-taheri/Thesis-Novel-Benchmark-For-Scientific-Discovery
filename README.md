# Thesis Benchmark: Autonomous Scientific Discovery

A reproducible skeleton for running **comparative evaluations** of LLMs on scientific discovery tasks
and for prototyping a **new benchmark** (novelty/generalization/consistency).

## Quick Start

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Dry run with MOCK model + synthetic tasks
python run_experiment.py experiments/example_autobench.yaml
```

Outputs go to `results/` (CSV + markdown report) and logs to `logs/`.

## Layout

- `run_experiment.py` – CLI runner (config → load data → run scenarios → score → report)
- `src/config.py` – pydantic config models for experiment YAMLs
- `src/adapters/` – model adapters (OpenAI/Anthropic/Gemini/Mock)
- `src/data/` – loaders & schemas for each benchmark (Auto-Bench, LLM-SRBench, etc.)
- `src/scenarios/` – closed-book / tool-assisted / decomposition / interactive
- `src/eval/` – evaluator, scientific judge, metrics, reporters
- `experiments/` – YAML configs declaring benchmark, scenario, and model
- `prompts/` – base and decomposition prompt templates
- `docs/` – protocol + benchmark cards template

This skeleton is **provider-agnostic** and ships with a MOCK adapter so you can test the pipeline.
Replace `MockAdapter` with your real provider (OpenAI/Anthropic/Google), set env keys, and go.
