# find-tests
Finds tests to run based on the files changed.

# Usage
## Install
```shell
pip install git+git@github.com:juharris/find-tests.git
```

# Commands
```shell
find-tests <file paths as JSON> <project dependency graph as JSON>
```

## Examples:
One file is changed and there is one test project that depends on the file:
```shell
find-tests '["A/A.Common/Class.cs"]' '{"Projects":[{"Id": "A/A.Common/A.Common.csproj"}, {"Id": "A/A.Common.Tests/A.Common.Tests.csproj"}], "References":[{"From": "A/A.Common.Tests/A.Common.Tests.csproj", "To": "A/A.Common/A.Common.csproj"}]}'
```
Returns:
```json
'A/A.Common.Tests/A.Common.Tests.csproj'
```

One file is changed and there are two test projects that depend on the file, one is a transitive dependency:
```shell
find-tests '["A/A.Common/Class.cs"]' '{"Projects":[{"Id": "A/A.Common/A.Common.csproj"}, {"Id": "B.Logic/B.Logic.csproj"}, {"Id": "A/A.Common.Tests/A.Common.Tests.csproj"}, {"Id": "B.Logic.Tests/B.Logic.Tests.csproj"}], "References":[{"From": "A/A.Common.Tests/A.Common.Tests.csproj", "To": "A/A.Common/A.Common.csproj"}, {"From": "B.Logic/B.Logic.csproj", "To": "A/A.Common/A.Common.csproj"}, {"From": "B.Logic.Tests/B.Logic.Tests.csproj", "To": "B.Logic/B.Logic.csproj"}]}'
```
Returns:
```json
'A/A.Common.Tests/A.Common.Tests.csproj' 'B.Logic.Tests/B.Logic.Tests.csproj'
```

# Dev Setup
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
