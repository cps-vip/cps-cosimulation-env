#!/usr/bin/env bash

export REPO_ROOT=$(realpath ./.)
export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring

if command -v uv &> /dev/null; then
	if [ ! -d ".venv" ]; then
		# Important - free-threading must be enabled! This is the 't' in 3.14t
		uv venv --python 3.14t .venv
	fi
	source $REPO_ROOT/.venv/bin/activate
	# Specifying the Python version here should be a bug that gets fixed here: https://github.com/astral-sh/uv/issues/12445
	# At the time of writing this comment, that GitHub issue was only completed two weeks ago, so the fix hasn't made its way to the version of uv being used in Nix
	uv sync --python python3.14t --reinstall-package dnp3
fi

export PATH=$(realpath ./install/HELICS/bin):$PATH
export PATH=$(realpath ./install/gridlab/bin):$PATH
export PATH=$(realpath ./install/bin):$PATH

