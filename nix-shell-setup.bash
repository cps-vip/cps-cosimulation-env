#!/usr/bin/env bash

export PATH=$(realpath ./install/bin):$PATH
export REPO_ROOT=$(realpath ./.)

export POETRY_VIRTUALENVS_CREATE=true
export POETRY_VIRTUALENVS_IN_PROJECT=true
export POETRY_VIRTUALENVS_PROMPT="cps-cosim-env"

if command -v poetry &> /dev/null; then
	poetry install
	source $REPO_ROOT/.venv/bin/activate
fi
