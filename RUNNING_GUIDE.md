# How to Run and Test the Thesis Benchmark

This guide explains how to run and test the thesis benchmark framework for evaluating LLMs on scientific discovery tasks.

## 🚀 Quick Start

### 1. Environment Setup

```bash
# Navigate to the project directory
cd /Users/samintaheri/Desktop/thesis-benchmark

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Test the Setup

```bash
# Run the setup test script
python test_setup.py
```

This will verify that all components are working correctly.

### 3. Run Basic Experiments

```bash
# Run experiment with mock adapter (safe for testing)
python run_experiment.py experiments/example_autobench.yaml

# Run another example
python run_experiment.py experiments/example_srbench.yaml
```

## 📊 Understanding the Output

After running an experiment, you'll find:

**Results Directory (`results/`):**
- `{timestamp}_{experiment_name}_summary.csv` - Aggregated metrics by task type
- `{timestamp}_{experiment_name}_items.csv` - Individual item results
- `{timestamp}_{experiment_name}_report.md` - Human-readable report

**Logs Directory (`logs/`):**
- `{timestamp}_{experiment_name}.log` - Detailed execution logs

## 🧪 Testing Different Components

### Test Individual Adapters

```python
from src.adapters import ADAPTERS

# Test mock adapter
mock = ADAPTERS['mock'](
    model="mock-science-001",
    temperature=0.0,
    top_p=1.0,
    max_tokens=512
)
result = mock.generate("Test prompt", {"task_type": "equation"})
print(result)
```

### Test Data Loaders

```python
from src.data.loaders import LOADERS

# Test synthetic data loader
loader = LOADERS['synthetic']()
items = loader.load(limit=5)
print(f"Loaded {len(items)} items")
for item in items:
    print(f"- {item.id}: {item.task_type}")
```

### Test Scenarios

```python
from src.scenarios import SCENARIOS

# Test closed book scenario
scenario = SCENARIOS['closed_book']()
test_item = {"input": {"question": "What is Newton's second law?"}}
prompt = scenario.make_prompt(test_item)
print(prompt)
```

## 🔧 Configuration

### Experiment Configuration (YAML)

```yaml
name: my-experiment
description: Custom experiment description
random_seed: 42

data:
  loader: synthetic    # synthetic, autobench, llm_srbench, etc.
  path: null          # path to data file (if needed)
  limit: 10           # number of items to process

model:
  provider: mock      # mock, openai, anthropic, google
  model: mock-science-001
  temperature: 0.0
  top_p: 1.0
  max_tokens: 512
  tools: []

scenario:
  name: closed_book   # closed_book, tool_assisted, decomposition, interactive
  params: {}

metrics:
  novelty: { enabled: true }
  generalization: { enabled: true }
  consistency: { enabled: true }
  reasoning_depth: { enabled: true }
  efficiency: { enabled: true }
```

## 🌐 Using Real Models

To use real LLM providers instead of the mock adapter:

### OpenAI
```bash
export OPENAI_API_KEY="YOUR_OPENAI_KEY_HERE"
```

Update YAML:
```yaml
model:
  provider: openai
  model: gpt-4
  temperature: 0.1
```

### Anthropic
```bash
export ANTHROPIC_API_KEY="YOUR_ANTHROPIC_KEY_HERE"
```

Update YAML:
```yaml
model:
  provider: anthropic
  model: claude-3-sonnet-20240229
  temperature: 0.1
```

### Google
```bash
export GOOGLE_API_KEY="YOUR_GOOGLE_KEY_HERE"
```

Update YAML:
```yaml
model:
  provider: google
  model: gemini-pro
  temperature: 0.1
```

## 📈 Available Metrics

The framework evaluates models on these scientific discovery metrics:

- **Novelty**: How novel are the generated hypotheses?
- **Generalization**: Do findings generalize beyond the training data?
- **Consistency**: Are results consistent across multiple runs?
- **Reasoning Depth**: How deep is the scientific reasoning?
- **Efficiency**: How efficiently does the model use tokens/time?

## 🎯 Available Scenarios

- **Closed Book**: Pure reasoning without external tools
- **Tool Assisted**: With access to computational tools
- **Decomposition**: Breaking complex problems into sub-problems
- **Interactive**: Multi-turn interactions

## 🛠 Troubleshooting

### Common Issues

1. **Import Errors**: Run `python test_setup.py` to verify setup
2. **Missing Dependencies**: Run `pip install -r requirements.txt`
3. **API Key Issues**: Ensure environment variables are set correctly
4. **Memory Issues**: Reduce `limit` in experiment YAML

### Debug Mode

Add debugging to any script:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📝 Creating Custom Experiments

1. Copy an existing YAML from `experiments/`
2. Modify the configuration as needed
3. Run with `python run_experiment.py your-experiment.yaml`

## 🧑‍💻 Development

### Adding New Adapters

1. Create new file in `src/adapters/`
2. Inherit from `BaseAdapter`
3. Add to `ADAPTERS` dict in `__init__.py`

### Adding New Data Loaders

1. Create new file in `src/data/loaders/`
2. Add loader class and function
3. Add to `LOADERS` dict in `__init__.py`

### Adding New Scenarios

1. Create new file in `src/scenarios/`
2. Add scenario class
3. Add to `SCENARIOS` dict in `__init__.py`

## 📚 Next Steps

1. **Start with Mock**: Always test with mock adapter first
2. **Small Batches**: Use small `limit` values when testing real APIs
3. **Monitor Costs**: Real API calls cost money - monitor usage
4. **Iterate**: Refine prompts and configurations based on results
5. **Scale Up**: Once validated, increase dataset sizes for full evaluation
