# Few-Shot Learning Experiment: ACORD Form to Policy JSON

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Claude](https://img.shields.io/badge/Claude-Sonnet%204.5-purple.svg)](https://www.anthropic.com/)

## Overview
This experiment tests whether a Large Language Model (LLM) can predict insurance policy attributes based on ACORD application forms using few-shot learning.

## Quick Start

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd acord_experiment

# 2. Set your API key
export ANTHROPIC_API_KEY='your-api-key-here'

# 3. Run with the launcher script
./start_notebook.sh
```

Or use the interactive Jupyter notebook:
```bash
uv sync
uv run jupyter notebook
# Open experiment.ipynb
```

See **[QUICK_START.md](QUICK_START.md)** for more options.

## Experiment Design

### Approach
- **Training Data**: 5 ACORD forms with corresponding policy JSON representations
- **Test Data**: 1 ACORD form (the 6th one)
- **Method**: Few-shot prompting with Claude Sonnet 4.5
- **Evaluation**: Compare generated JSON against ground truth policy

### Dataset Description
The synthetic dataset includes 6 different business types:

1. **Green Valley Landscaping** - Landscaping services
2. **Bella Vista Restaurant** - Full-service restaurant with liquor liability
3. **TechHub Electronics** - Retail electronics store
4. **Strategic Solutions** - Management consulting firm
5. **Precision Parts Manufacturing** - Custom metal parts manufacturer
6. **FitLife Wellness Center** (TEST CASE) - Fitness center and gym

Each example includes:
- Complete ACORD 125 form with business details, coverage requests, and loss history
- Corresponding policy JSON with premiums, coverages, and underwriting factors

## Files Structure

```
acord_form_1.txt → policy_1.json  (Training)
acord_form_2.txt → policy_2.json  (Training)
acord_form_3.txt → policy_3.json  (Training)
acord_form_4.txt → policy_4.json  (Training)
acord_form_5.txt → policy_5.json  (Training)
acord_form_6.txt → policy_6.json  (Test - Ground Truth)
run_experiment.py                  (Experiment script)
```

## Running the Experiment

### Prerequisites
1. Python 3.8+
2. Anthropic API key
3. Install required package:
   ```bash
   pip install anthropic --break-system-packages
   ```

### Steps

1. **Set your API key**:
   ```bash
   export ANTHROPIC_API_KEY='your-api-key-here'
   ```

2. **Run the experiment**:
   ```bash
   python run_experiment.py
   ```

### What the Script Does

1. Loads 5 training examples (ACORD forms + policy JSONs)
2. Loads the test ACORD form (form 6)
3. Creates a few-shot prompt with all training examples
4. Calls Claude API to generate policy JSON for test form
5. Compares generated policy against ground truth
6. Calculates accuracy metrics
7. Saves results to files

## Output Files

After running, you'll get:

- **generated_policy_6.json** - The AI-generated policy from the test ACORD form
- **comparison_results.json** - Detailed comparison showing:
  - Exact matches
  - Close matches (numeric values within 10%)
  - Mismatches
  - Missing fields
  - Extra fields

## Evaluation Metrics

The script calculates:

- **Overall Accuracy**: (Exact matches + Close matches) / Total fields
- **Exact Match Rate**: Exact matches / Total fields
- **Field-level comparison**: Detailed breakdown of matches and mismatches

## Interpreting Results

### Good Performance Indicators
- Accuracy > 80%: Strong pattern recognition
- Correct policy structure and required fields
- Accurate premium calculations based on risk factors
- Proper coverage limits and deductibles

### Areas to Examine
- **Mismatches**: Fields where AI predictions differ from actual
- **Missing Fields**: Critical fields the AI didn't generate
- **Premium Accuracy**: How close are premium predictions to actuals?
- **Coverage Logic**: Did AI correctly infer coverage based on business type?

## Key Patterns the LLM Should Learn

From the training examples, the model should identify:

1. **Premium Factors**:
   - Higher revenue → Higher premiums
   - More employees → Higher workers comp
   - Claims history → Higher rates (experience mod)
   - Industry risk level → Base premium adjustments

2. **Coverage Selection**:
   - Restaurants need liquor liability
   - Fitness centers need abuse/molestation coverage
   - Manufacturers need products liability
   - Consultants need professional E&O

3. **Limit Selection**:
   - Higher revenue businesses → Higher liability limits
   - Building ownership → Building coverage
   - Specialized equipment → Scheduled property coverage

4. **Deductibles**:
   - Inversely related to claims history
   - Higher for property than liability
   - Industry standards

## Extending the Experiment

### Try Different Approaches
1. **Vary training set size**: Test with 3, 5, 7, or 10 examples
2. **Different LLMs**: Compare Claude vs GPT-4 vs others
3. **Structured output**: Use function calling or JSON mode
4. **Chain-of-thought**: Add reasoning steps before prediction
5. **Fine-tuning**: Fine-tune a model on larger dataset

### Additional Metrics
- Field importance weighting (premium > other fields)
- Category-specific accuracy (coverages vs premiums)
- Business type generalization

## Real-World Considerations

If deploying this approach:

1. **Data Quality**: Real ACORD forms need proper OCR/extraction
2. **Validation**: Add business rules to validate LLM outputs
3. **Hybrid Approach**: Combine LLM predictions with rule-based systems
4. **Confidence Scores**: Implement uncertainty quantification
5. **Human Review**: Keep humans in the loop for final decisions
6. **Regulatory Compliance**: Ensure predictions meet insurance regulations

## Next Steps

Based on results:
- **High accuracy (>80%)**: Consider expanding to more complex scenarios
- **Medium accuracy (60-80%)**: Add more training examples or refine prompt
- **Low accuracy (<60%)**: May need different approach (fine-tuning, more structured data)

## Questions to Answer

After running the experiment:

1. Which fields does the LLM predict most accurately?
2. Which fields does it struggle with?
3. Are premium calculations reasonable?
4. Does it understand industry-specific coverage needs?
5. How consistent are predictions across business types?
6. Is few-shot learning sufficient, or is fine-tuning needed?

## Documentation

- **[QUICK_START.md](QUICK_START.md)** - Get running in 3 minutes
- **[JUPYTER_GUIDE.md](JUPYTER_GUIDE.md)** - Complete Jupyter notebook guide with troubleshooting
- **[SETUP.md](SETUP.md)** - Detailed setup instructions
- **[experiment.ipynb](experiment.ipynb)** - Interactive notebook with visualizations

## Project Structure

```
acord_experiment/
├── experiment.ipynb          # Interactive Jupyter notebook (recommended)
├── run_experiment.py         # Command-line script version
├── start_notebook.sh         # Convenience launcher script
│
├── acord_form_1-6.txt       # ACORD application forms (training + test)
├── policy_1-6.json          # Corresponding policy JSONs (ground truth)
│
├── pyproject.toml           # Project dependencies
├── uv.lock                  # Locked dependency versions
│
├── README.md                # This file - project overview
├── QUICK_START.md          # Quick start guide
├── JUPYTER_GUIDE.md        # Complete Jupyter guide
├── SETUP.md                # Detailed setup instructions
└── .env.example            # API key template
```

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- Anthropic API key

## Contributing

Contributions are welcome! Areas for exploration:
- Testing with different LLM models
- Implementing chain-of-thought prompting
- Adding validation rules for generated policies
- Expanding the dataset with more business types
- Comparing few-shot vs fine-tuning approaches

## License

MIT License - see LICENSE file for details

## Acknowledgments

Built with Claude Sonnet 4.5 by Anthropic
