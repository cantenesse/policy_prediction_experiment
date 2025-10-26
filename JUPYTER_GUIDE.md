# ACORD Policy Prediction Experiment - Jupyter Notebook Guide

Complete guide for running the ACORD form to policy JSON prediction experiment using Jupyter notebooks with uv dependency management.

## Table of Contents
- [Quick Start](#quick-start)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Running the Experiment](#running-the-experiment)
- [Understanding the Results](#understanding-the-results)
- [Troubleshooting](#troubleshooting)
- [Advanced Usage](#advanced-usage)

---

## Quick Start

For those who want to get started immediately:

```bash
# 1. Set your API key
export ANTHROPIC_API_KEY='your-api-key-here'

# 2. Install dependencies (first time only)
uv sync

# 3. Start Jupyter notebook
uv run jupyter notebook

# 4. Open experiment.ipynb and run all cells
```

---

## Prerequisites

### Required Software

1. **Python 3.11+**
   ```bash
   python --version  # Should show 3.11 or higher
   ```

2. **uv** (Python package manager)
   - Install from: https://docs.astral.sh/uv/
   - Or via Homebrew: `brew install uv`
   - Verify: `uv --version`

3. **Anthropic API Key**
   - Get one from: https://console.anthropic.com/
   - You'll need this to run the experiment

### System Requirements

- macOS, Linux, or Windows with WSL
- At least 2GB free RAM
- Internet connection for API calls

---

## Setup Instructions

### 1. Clone/Navigate to the Repository

```bash
cd /path/to/acord_experiment
```

### 2. Verify Project Structure

Your directory should contain:
```
acord_experiment/
├── acord_form_1.txt through acord_form_6.txt  # ACORD forms
├── policy_1.json through policy_6.json        # Corresponding policies
├── experiment.ipynb                            # Jupyter notebook (main interface)
├── run_experiment.py                           # Python script version
├── pyproject.toml                              # Project dependencies
├── JUPYTER_GUIDE.md                            # This file
└── README.md                                   # Project overview
```

### 3. Set Up Environment Variables

You have two options for providing your API key:

**Option A: Environment Variable (Recommended for terminal sessions)**
```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

**Option B: .env File (Recommended for persistent setup)**
```bash
# Create a .env file in the project root
echo "ANTHROPIC_API_KEY=your-api-key-here" > .env
```

The notebook will automatically load from `.env` if it exists.

### 4. Install Dependencies with uv

```bash
# Install all required packages
uv sync

# This will install:
# - anthropic (API client)
# - jupyter, notebook, ipykernel (Jupyter environment)
# - pandas, matplotlib, seaborn (data analysis and visualization)
# - python-dotenv (environment variable management)
```

### 5. Verify Installation

```bash
# Check that Jupyter is installed correctly
uv run jupyter --version

# Should show something like: jupyter core : 5.9.1
```

---

## Running the Experiment

### Method 1: Jupyter Notebook Interface (Recommended)

This provides an interactive experience with visualizations.

#### Step 1: Start Jupyter

```bash
uv run jupyter notebook
```

This will:
- Start the Jupyter server
- Open your default web browser
- Display the file browser at `http://localhost:8888`

#### Step 2: Open the Notebook

- Click on `experiment.ipynb` in the file browser
- The notebook will open in a new tab

#### Step 3: Run the Experiment

You have two options:

**Option A: Run All Cells at Once**
- Click "Kernel" → "Restart & Run All"
- Watch as each cell executes in sequence
- Takes ~30-60 seconds to complete

**Option B: Run Cells Step by Step**
- Click on the first code cell
- Press `Shift + Enter` to run and move to the next cell
- Repeat for each cell
- This lets you examine outputs as you go

#### Step 4: Review Results

The notebook will:
1. Load training data (5 ACORD forms + policies)
2. Load test case (6th ACORD form)
3. Create a few-shot prompt
4. Call Claude API to generate policy
5. Compare with ground truth
6. Display metrics and visualizations
7. Save results to files

### Method 2: JupyterLab Interface (Alternative)

For a more advanced IDE-like experience:

```bash
uv run jupyter lab
```

Features:
- Multiple notebooks side-by-side
- Terminal access
- File browser with drag-and-drop
- Extension support

### Method 3: Command Line Script

If you prefer running without the notebook interface:

```bash
uv run python run_experiment.py
```

This runs the same experiment but outputs to the terminal instead of generating visualizations.

---

## Understanding the Results

### Output Files

After running, you'll find these new files:

#### 1. `generated_policy_6.json`
The AI-generated policy for the 6th ACORD form.

```json
{
  "policy_number": "FIT-2025-001234",
  "business_name": "FitLife Wellness Center",
  "effective_date": "2025-01-15",
  ...
}
```

#### 2. `comparison_results.json`
Detailed comparison between generated and ground truth policies.

Contains:
- **Metrics**: Overall accuracy, match rates
- **Details**: Exact matches, close matches, mismatches
- **Missing fields**: Fields not generated
- **Extra fields**: Fields generated but not in ground truth

#### 3. `experiment_results.png`
Visual representation of the results with:
- Bar chart of field comparison breakdown
- Pie chart showing overall accuracy

### Key Metrics Explained

1. **Overall Accuracy**: `(Exact Matches + Close Matches) / Total Fields`
   - Goal: > 80% for production consideration
   - Indicates how well the model learned the patterns

2. **Exact Match Rate**: `Exact Matches / Total Fields`
   - Percentage of fields that match exactly
   - Higher is better for categorical fields

3. **Close Matches**: Numeric values within 10% of ground truth
   - Important for premium calculations
   - Shows the model understands relative magnitudes

4. **Missing Fields**: Fields in ground truth but not generated
   - Critical to examine - may indicate blind spots
   - High count suggests incomplete understanding

5. **Extra Fields**: Fields generated but not in ground truth
   - May indicate model is being creative or confused
   - Not necessarily bad if fields are valid

### Interpreting Results

#### Excellent Performance (>85% accuracy)
- Model has learned the patterns well
- Consider expanding to more test cases
- Ready for prototype testing with human review

#### Good Performance (70-85% accuracy)
- Model understands general patterns
- May need more training examples
- Examine mismatches for patterns

#### Poor Performance (<70% accuracy)
- Model is struggling with the task
- Consider:
  - Adding more training examples
  - Using chain-of-thought prompting
  - Fine-tuning instead of few-shot learning
  - Simplifying the output schema

### Common Patterns to Look For

1. **Premium Calculation Accuracy**
   - Are premiums in the right range?
   - Does the model understand risk factors?

2. **Coverage Selection**
   - Did it pick appropriate coverages for the business type?
   - Are limits reasonable?

3. **Field Completeness**
   - Are all critical fields present?
   - Is the structure correct?

4. **Business Logic**
   - Does it understand industry-specific requirements?
   - Are deductibles sensible?

---

## Troubleshooting

### Issue: "ANTHROPIC_API_KEY not found"

**Solution:**
```bash
# Check if it's set
echo $ANTHROPIC_API_KEY

# If empty, set it
export ANTHROPIC_API_KEY='your-api-key-here'

# Or create .env file
echo "ANTHROPIC_API_KEY=your-api-key-here" > .env
```

### Issue: "uv: command not found"

**Solution:**
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or on macOS with Homebrew
brew install uv
```

### Issue: "Port 8888 is already in use"

**Solution:**
```bash
# Use a different port
uv run jupyter notebook --port 8889

# Or kill the existing Jupyter process
pkill -f jupyter
```

### Issue: Jupyter opens but notebook won't run

**Solution:**
```bash
# Make sure dependencies are installed
uv sync

# Try reinstalling the kernel
uv run python -m ipykernel install --user --name=acord-env
```

### Issue: "ModuleNotFoundError: No module named 'anthropic'"

**Solution:**
```bash
# Reinstall dependencies
uv sync --reinstall
```

### Issue: API rate limits or errors

**Solution:**
- Check your API key is valid
- Verify you have credits: https://console.anthropic.com/
- Wait a few seconds and try again
- Check Anthropic status: https://status.anthropic.com/

### Issue: Notebook kernel keeps dying

**Solution:**
```bash
# Clear cached notebooks
rm -rf ~/.jupyter/runtime/*

# Restart with verbose logging
uv run jupyter notebook --debug
```

---

## Advanced Usage

### Running with Different Training Set Sizes

Modify the notebook to test with fewer examples:

```python
# In the "Load Training Examples" cell, change:
for i in range(1, 6):  # Original: 5 examples
    # to
for i in range(1, 4):  # Now: 3 examples
```

### Comparing Different Models

Change the model in the API call:

```python
message = client.messages.create(
    model="claude-sonnet-4-20250514",  # Different model
    max_tokens=4096,
    messages=[{"role": "user", "content": prompt}]
)
```

Available models:
- `claude-sonnet-4-5-20250929` (Default, most capable)
- `claude-sonnet-4-20250514` (Previous version)
- `claude-3-5-sonnet-20241022` (Older, faster, cheaper)

### Adding Chain-of-Thought Prompting

Modify the prompt to include reasoning:

```python
prompt += """
Before generating the JSON, first:
1. Identify the business type and key characteristics
2. Determine the risk factors present
3. Calculate appropriate premium modifiers
4. Select relevant coverages
5. Then generate the complete policy JSON

Generate the policy JSON following the same structure and logic as the examples.
"""
```

### Batch Processing Multiple Test Cases

Create a loop to test all forms:

```python
for test_idx in range(1, 7):
    # Load test case
    test_acord, ground_truth = load_test_case(test_idx)

    # Generate policy
    generated_policy = generate_policy_with_claude(prompt, api_key)

    # Compare and save results
    metrics, details = compare_policies(generated_policy, ground_truth)

    # Store results
    all_results[test_idx] = metrics
```

### Exporting Results to Different Formats

```python
# Export to CSV
df_results.to_csv('results.csv', index=False)

# Export to Excel
df_results.to_excel('results.xlsx', sheet_name='Experiment Results')

# Export visualizations as PDF
plt.savefig('results.pdf', format='pdf', dpi=300)
```

### Running Experiments Programmatically

Create a script to run multiple experiments:

```python
experiments = [
    {'name': '3-shot', 'training_size': 3},
    {'name': '5-shot', 'training_size': 5},
    {'name': '7-shot', 'training_size': 7},
]

for exp in experiments:
    # Run experiment with different parameters
    results = run_experiment(**exp)
    save_results(f"results_{exp['name']}.json", results)
```

### Using uv for Other Tasks

```bash
# Run Python scripts
uv run python your_script.py

# Install additional packages
uv add package-name

# Create a requirements.txt
uv pip freeze > requirements.txt

# Run with specific Python version
uv run --python 3.11 jupyter notebook

# Check for outdated packages
uv pip list --outdated
```

---

## Additional Resources

### Documentation
- **uv**: https://docs.astral.sh/uv/
- **Anthropic API**: https://docs.anthropic.com/
- **Jupyter Notebook**: https://jupyter-notebook.readthedocs.io/
- **Pandas**: https://pandas.pydata.org/docs/
- **Matplotlib**: https://matplotlib.org/stable/contents.html

### Project Files
- `README.md` - Project overview and experiment design
- `SETUP.md` - Original setup instructions
- `run_experiment.py` - Command-line script version
- `pyproject.toml` - Dependency configuration

### Getting Help

If you encounter issues:

1. Check this troubleshooting section
2. Review the existing README.md
3. Check uv documentation: https://docs.astral.sh/uv/
4. Check Anthropic documentation: https://docs.anthropic.com/
5. Verify your API key and credits

---

## Best Practices

### 1. Always Use uv run

Instead of activating a virtual environment, use `uv run` prefix:
```bash
# Good
uv run jupyter notebook

# Avoid (manual venv activation)
source .venv/bin/activate
jupyter notebook
```

### 2. Keep Dependencies Updated

```bash
# Update all packages
uv sync --upgrade

# Update specific package
uv add anthropic --upgrade
```

### 3. Use Version Control

```bash
# Don't commit generated files
echo "generated_policy_6.json" >> .gitignore
echo "comparison_results.json" >> .gitignore
echo "experiment_results.png" >> .gitignore
echo ".env" >> .gitignore
```

### 4. Monitor API Usage

The experiment makes one API call which typically:
- Uses ~20k-30k input tokens
- Generates ~2k-4k output tokens
- Costs approximately $0.60-$0.90 per run

Track your usage at: https://console.anthropic.com/settings/cost

### 5. Save Your Work

Jupyter notebooks auto-save, but you can also:
- Click "File" → "Save and Checkpoint" (Ctrl+S)
- Download notebook: "File" → "Download as" → "Notebook (.ipynb)"

---

## Next Steps

After running the experiment:

1. **Analyze the Results**
   - Which fields are most/least accurate?
   - Are there patterns in the mismatches?
   - Is the accuracy sufficient for your use case?

2. **Experiment with Variations**
   - Try different numbers of training examples
   - Test different Claude models
   - Add chain-of-thought reasoning
   - Modify the prompt structure

3. **Extend the Dataset**
   - Add more business types
   - Include edge cases
   - Test with real ACORD forms (with proper OCR)

4. **Build Production Pipeline**
   - Add validation rules
   - Implement confidence scoring
   - Create human-in-the-loop review process
   - Set up monitoring and logging

5. **Optimize Costs**
   - Use prompt caching for repeated examples
   - Consider using Claude Haiku for simpler cases
   - Batch process multiple forms

---

## Questions?

Review the existing documentation:
- Main README.md for experiment design
- SETUP.md for original setup instructions
- Anthropic docs for API details

Good luck with your experiment!
