#!/bin/bash

# ACORD Experiment - Jupyter Notebook Launcher
# This script helps you quickly start the Jupyter notebook environment

set -e

echo "======================================"
echo "ACORD Policy Prediction Experiment"
echo "======================================"
echo ""

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "ERROR: uv is not installed"
    echo "Install it with: curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo "Or on macOS: brew install uv"
    exit 1
fi

echo "✓ uv is installed"

# Check for API key
if [ -z "$ANTHROPIC_API_KEY" ]; then
    if [ ! -f .env ]; then
        echo ""
        echo "WARNING: ANTHROPIC_API_KEY not found"
        echo ""
        echo "Please set your API key by either:"
        echo "1. Creating a .env file with: ANTHROPIC_API_KEY=your-key-here"
        echo "2. Or export it: export ANTHROPIC_API_KEY='your-key-here'"
        echo ""
        read -p "Do you want to create a .env file now? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            read -p "Enter your Anthropic API key: " api_key
            echo "ANTHROPIC_API_KEY=$api_key" > .env
            echo "✓ .env file created"
        else
            echo "Continuing without API key (notebook will fail when calling API)"
        fi
    else
        echo "✓ .env file found"
    fi
else
    echo "✓ ANTHROPIC_API_KEY is set"
fi

# Check if dependencies are installed
if [ ! -d ".venv" ]; then
    echo ""
    echo "Installing dependencies with uv..."
    uv sync
    echo "✓ Dependencies installed"
else
    echo "✓ Dependencies already installed"
fi

echo ""
echo "======================================"
echo "Starting Jupyter Notebook..."
echo "======================================"
echo ""
echo "The notebook will open in your browser at:"
echo "http://localhost:8888"
echo ""
echo "To run the experiment:"
echo "1. Click on 'experiment.ipynb'"
echo "2. Click 'Kernel' → 'Restart & Run All'"
echo ""
echo "Press Ctrl+C to stop the Jupyter server"
echo ""

# Start Jupyter notebook
uv run jupyter notebook
