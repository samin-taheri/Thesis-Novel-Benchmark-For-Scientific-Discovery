# 🚀 How to Replace Mock Data with Real Models

This guide shows you how to switch from the mock adapter to real LLM providers in your thesis benchmark.

## ✅ **What's Now Available**

After setup, you now have:
- ✅ Mock adapter (for testing) 
- ✅ OpenAI adapter (GPT-4, GPT-3.5, etc.)
- ✅ Anthropic adapter (Claude-3, etc.)
- ✅ Google adapter (Gemini Pro, etc.)
- ✅ Real model experiment configs
- ✅ All dependencies installed

## 🔑 **Step 1: Get API Keys**

### OpenAI
1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Set environment variable:
```bash
export OPENAI_API_KEY="sk-your-openai-key-here"
```

### Anthropic
1. Go to https://console.anthropic.com/
2. Create a new API key
3. Set environment variable:
```bash
export ANTHROPIC_API_KEY="sk-ant-your-anthropic-key-here"
```

### Google
1. Go to https://ai.google.dev/
2. Create a new API key
3. Set environment variable:
```bash
export GOOGLE_API_KEY="your-google-api-key-here"
```

## 🧪 **Step 2: Test with Small Experiments**

Start with small experiments to avoid high costs:

### OpenAI GPT-4
```bash
# Set your API key first
export OPENAI_API_KEY="your-key-here"

# Run small experiment (5 items only)
python run_experiment.py experiments/openai_gpt4_experiment.yaml
```

### Anthropic Claude
```bash
# Set your API key first
export ANTHROPIC_API_KEY="your-key-here"

# Run small experiment (5 items only)
python run_experiment.py experiments/anthropic_claude_experiment.yaml
```

### Google Gemini
```bash
# Set your API key first
export GOOGLE_API_KEY="your-key-here"

# Run small experiment (5 items only)
python run_experiment.py experiments/google_gemini_experiment.yaml
```

## 📊 **Step 3: Compare Results**

After running real models, you'll get much more interesting results:

**Mock Results (fake):**
- Same response every time
- Low novelty/reasoning scores
- Perfect efficiency (unrealistic)

**Real Model Results:**
- Variable responses based on input
- Realistic novelty/reasoning scores
- Actual token usage and costs

## ⚙️ **Step 4: Create Custom Experiments**

Create your own experiment file:

```yaml
name: my-custom-experiment
description: Custom evaluation with real model
random_seed: 42

data:
  loader: synthetic  # or autobench, llm_srbench, etc.
  path: null
  limit: 10  # Start small!

model:
  provider: openai  # or anthropic, google
  model: gpt-4     # or claude-3-sonnet-20240229, gemini-pro
  temperature: 0.1  # Lower = more deterministic
  top_p: 1.0
  max_tokens: 512
  tools: []

scenario:
  name: closed_book  # or tool_assisted, decomposition, interactive
  params: {}

metrics:
  novelty: { enabled: true }
  generalization: { enabled: true }
  consistency: { enabled: true }
  reasoning_depth: { enabled: true }
  efficiency: { enabled: true }
```

## 💰 **Step 5: Cost Management**

Real APIs cost money! Here's how to manage costs:

### Start Small
- Use `limit: 5` or `limit: 10` for initial testing
- Gradually increase to full datasets

### Monitor Usage
- Check your API usage dashboards regularly
- Set spending limits in your API accounts

### Compare Efficiency
- The `efficiency` metric shows tokens per task
- Use this to compare model costs

### Model Cost Estimates (approximate)
- **GPT-4**: ~$0.03-0.06 per 1K tokens
- **Claude-3**: ~$0.015-0.075 per 1K tokens  
- **Gemini Pro**: ~$0.0005-0.0015 per 1K tokens

## 🔄 **Step 6: Iterate and Scale**

### Development Workflow
1. **Test with mock** - validate pipeline
2. **Small real tests** - 5-10 items per model
3. **Compare models** - see which performs best
4. **Scale up** - run full datasets on best models

### Advanced Configuration

#### Model Parameters
```yaml
model:
  provider: openai
  model: gpt-4
  temperature: 0.0    # Deterministic
  # temperature: 0.7  # More creative
  top_p: 1.0
  max_tokens: 1024    # Longer responses
```

#### Data Sources
```yaml
data:
  loader: autobench      # Real benchmark data
  path: "/path/to/data"  # Custom data file
  limit: 100             # More items
```

#### Scenarios
```yaml
scenario:
  name: tool_assisted    # Give model access to tools
  params:
    tools: ["calculator", "search"]
```

## 📈 **Step 7: Analyze Results**

Look for these patterns in real model results:

### Performance Metrics
- **Accuracy**: Which models get answers right?
- **Consistency**: Which models are most reliable?
- **Efficiency**: Which models use fewest tokens?

### Scientific Discovery Metrics
- **Novelty**: Which models generate creative hypotheses?
- **Reasoning Depth**: Which models show deeper scientific thinking?

### Example Analysis
```python
import pandas as pd

# Load results
df = pd.read_csv("results/your_experiment_items.csv")

# Compare by model
print(df.groupby('model')[['acc', 'novelty', 'reasoning_depth']].mean())

# Compare by task type
print(df.groupby('task_type')[['acc', 'novelty']].mean())
```

## 🎯 **Next Steps for Your Thesis**

1. **Baseline with Mock**: Validate your experimental setup
2. **Small Real Tests**: Compare 2-3 models on ~10 items each
3. **Choose Best Models**: Based on performance and cost
4. **Scale Up**: Run full experiments with chosen models
5. **Analyze Patterns**: What makes models good at scientific discovery?
6. **Iterate**: Refine prompts, scenarios, and metrics

## 🛠 **Troubleshooting**

### API Key Issues
```bash
# Check if keys are set
echo $OPENAI_API_KEY
echo $ANTHROPIC_API_KEY
echo $GOOGLE_API_KEY

# Add to shell profile for persistence
echo 'export OPENAI_API_KEY="your-key"' >> ~/.zshrc
source ~/.zshrc
```

### Rate Limits
If you hit rate limits, the adapters will return error messages. Add delays between requests or reduce batch sizes.

### Model Availability
Some models may not be available in all regions. Check the provider documentation for current model availability.

## 🏁 **You're Ready!**

Your thesis benchmark is now ready to evaluate real LLMs on scientific discovery tasks. Start small, compare models, and scale up based on your findings! 🎓
