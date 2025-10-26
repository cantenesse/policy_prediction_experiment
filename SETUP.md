# ACORD Policy Predictor - Setup Guide

## Quick Start with uv

### 1. Install uv (if not already installed)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Set up the project
```bash
# Navigate to your project directory
cd /path/to/your/project

# Extract the experiment files
unzip acord_experiment.zip

# Copy pyproject.toml to the root (it's in the zip)
# The pyproject.toml is already configured!

# Initialize uv (this creates .venv and installs dependencies)
uv sync

# If pyproject.toml isn't present, you can create it from scratch:
# uv init --python 3.11
# Then add dependencies manually or copy the pyproject.toml
```

### 3. Set up environment variables
```bash
# Create .env file with your API key
echo "ANTHROPIC_API_KEY=your-api-key-here" > .env
```

### 4. Run Jupyter
```bash
uv run jupyter notebook
```

Or run the experiment directly:
```bash
uv run python run_experiment.py
```

## Project Structure

```
acord-policy-predictor/
├── pyproject.toml          # Project configuration
├── .env                    # Your API key (don't commit!)
├── .gitignore             # Git ignore rules
├── README.md              # Experiment documentation
├── run_experiment.py      # Main experiment script
├── acord_form_1.txt       # Training example 1
├── acord_form_2.txt       # Training example 2
├── acord_form_3.txt       # Training example 3
├── acord_form_4.txt       # Training example 4
├── acord_form_5.txt       # Training example 5
├── acord_form_6.txt       # Test case
├── policy_1.json          # Ground truth 1
├── policy_2.json          # Ground truth 2
├── policy_3.json          # Ground truth 3
├── policy_4.json          # Ground truth 4
├── policy_5.json          # Ground truth 5
└── policy_6.json          # Ground truth test case
```

## Common Commands

```bash
# Add a new dependency
uv add package-name

# Add a dev dependency
uv add --dev package-name

# Remove a dependency
uv remove package-name

# Update all dependencies
uv sync --upgrade

# Run Python scripts
uv run python script.py

# Run Jupyter notebook
uv run jupyter notebook

# Run Jupyter lab (alternative)
uv run jupyter lab

# Run pytest (if you add tests)
uv run pytest

# Format code with black
uv run black .

# Lint code with ruff
uv run ruff check .
```

## Installing Dev Tools (Optional)

The pyproject.toml includes optional dev dependencies. Install them with:

```bash
uv sync --extra dev
```

This adds:
- **black**: Code formatter
- **ruff**: Fast Python linter
- **pytest**: Testing framework
- **ipywidgets**: Interactive Jupyter widgets

## Environment Variables

The project uses python-dotenv to load environment variables from `.env`:

```bash
# .env file
ANTHROPIC_API_KEY=your-actual-api-key-here
```

## Git Setup

Create a `.gitignore`:
```bash
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Virtual Environment
.venv/
venv/
ENV/

# Jupyter
.ipynb_checkpoints/
*.ipynb_checkpoints

# Environment variables
.env
.env.local

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Project specific
generated_policy_6.json
comparison_results.json
*.zip

# uv
.uv/
EOF
```

Initialize git:
```bash
git init
git add .
git commit -m "Initial commit: ACORD policy predictor experiment"
```

## Troubleshooting

### API Key not found
Make sure your `.env` file exists and contains:
```
ANTHROPIC_API_KEY=sk-ant-...
```

### Dependencies not installing
Try:
```bash
uv sync --reinstall
```

### Python version issues
Specify the exact version:
```bash
uv python install 3.11.9
uv venv --python 3.11.9
```

### Jupyter kernel not found
Register the kernel manually:
```bash
uv run python -m ipykernel install --user --name acord-env
```

## Next Steps

1. Run the experiment: `uv run python run_experiment.py`
2. Open Jupyter: `uv run jupyter notebook`
3. Analyze results in `comparison_results.json`
4. Iterate on the prompt or add more training examples

## Resources

- [uv documentation](https://docs.astral.sh/uv/)
- [Anthropic API docs](https://docs.anthropic.com/)
- [Project README](README.md)
