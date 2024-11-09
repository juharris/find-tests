# find-tests
Finds tests to run based on the files changed.

# Setup
Written using Python 3.12

Example Python environment initialization with Conda:
```shell
conda create --yes --name find-tests python=3.12
conda activate find-tests
```

## Install Poetry
See [here](https://python-poetry.org/docs/main).

## Install Dependencies
Run
```shell
poetry install
```

# Running
Make sure the environment is activated.
For example, if you are using Conda:
```shell
conda activate find-tests
```

# Testing
Run the automated tests:
```shell
PYTHONPATH=src pytest
```

# Linting
The rules are configured in [pyproject.toml](pyproject.toml).

To see the changes, run:
```shell
autopep8 --jobs 0 --exit-code --diff .
```

To make the changes automatically, run:
```shell
autopep8 --jobs 0 --in-place .
```
