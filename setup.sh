#!/bin/bash

set -e

if [[ "$PWD" != "/home/vip/cps-cosimulation-env" ]]; then
    echo "This script should only be ran inside the Docker container"
    exit 1
fi

echo "--- Starting One-Time Project Setup ---"
echo "Installing Python 3.14t with uv..."
# Install to the shared volume so it persists across container instances
uv python install --install-dir .python python3.14t

echo "Creating Python 3.14t virtual environment..."
uv venv --python .python/* .venv
source .venv/bin/activate

echo "Installing Python dependencies from pyproject.toml..."
uv sync --verbose

echo "Building HELICS and Gridlab-D..."
make all-install

echo "--- Project Setup Complete ---"
echo "Your environment is ready. 'source .venv/bin/activate' to get started."

