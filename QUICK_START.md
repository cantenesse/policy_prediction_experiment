# Quick Start Guide

Get the ACORD experiment running in 3 minutes.

## Prerequisites

- Python 3.11+
- uv installed (`brew install uv` on macOS)
- Anthropic API key

## Three Ways to Run

### Option 1: Interactive Launcher (Easiest)

```bash
./start_notebook.sh
```

This script will:
- Check dependencies
- Prompt for API key if needed
- Install packages
- Launch Jupyter automatically

### Option 2: Manual Jupyter

```bash
# Set API key
export ANTHROPIC_API_KEY='your-api-key-here'

# Or create .env file
echo "ANTHROPIC_API_KEY=your-api-key-here" > .env

# Install dependencies (first time only)
uv sync

# Start Jupyter
uv run jupyter notebook

# Open experiment.ipynb and run all cells
```

### Option 3: Command Line Script

```bash
# Set API key
export ANTHROPIC_API_KEY='your-api-key-here'

# Install dependencies (first time only)
uv sync

# Run the experiment
uv run python run_experiment.py
```

## What Gets Created

After running, you'll have:
- `generated_policy_6.json` - AI-generated policy
- `comparison_results.json` - Detailed comparison metrics
- `experiment_results.png` - Visualization (notebook only)

## Key Commands

```bash
# Install/update dependencies
uv sync

# Start Jupyter notebook
uv run jupyter notebook

# Start JupyterLab (advanced)
uv run jupyter lab

# Run Python script directly
uv run python run_experiment.py

# Check Jupyter version
uv run jupyter --version
```

## Troubleshooting

**API Key Error?**
```bash
# Check if set
echo $ANTHROPIC_API_KEY

# Set it
export ANTHROPIC_API_KEY='your-key-here'

# Or create .env
cp .env.example .env
# Edit .env with your key
```

**Port 8888 in use?**
```bash
uv run jupyter notebook --port 8889
```

**Dependencies not working?**
```bash
uv sync --reinstall
```

## Full Documentation

- **JUPYTER_GUIDE.md** - Complete Jupyter notebook guide
- **README.md** - Experiment design and methodology
- **SETUP.md** - Detailed setup instructions

## Experiment Workflow

1. Load 5 ACORD forms + policies (training data)
2. Load 6th ACORD form (test case)
3. Create few-shot prompt with examples
4. Call Claude API to generate policy
5. Compare with ground truth
6. View results and metrics

## Expected Results

- **Accuracy**: Typically 70-90%
- **Runtime**: 30-60 seconds
- **API Cost**: ~$0.60-0.90 per run

## Next Steps

After your first run:
1. Review the generated policy
2. Examine mismatches in comparison_results.json
3. Try modifying the prompt
4. Test with different training set sizes
5. Compare different Claude models

See **JUPYTER_GUIDE.md** for advanced usage.
