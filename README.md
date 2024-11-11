# find-tests
Finds tests to run based on the files changed.
This tool is mainly made to work with .NET solutions for now.

# Usage
## Install
```shell
pip install git+git@github.com:juharris/find-tests.git
```

## Commands
```shell
find-tests <file paths as JSON or newline-separated list> <project dependency graph as JSON>
```

### Examples:
Example: One file is changed and there is one test project that depends on the file:
```shell
find-tests '["A/A.Common/Class.cs"]' '{"Projects":[{"Id": "A/A.Common/A.Common.csproj"}, {"Id": "A/A.Common.Tests/A.Common.Tests.csproj"}], "References":[{"From": "A/A.Common.Tests/A.Common.Tests.csproj", "To": "A/A.Common/A.Common.csproj"}]}'
```
Returns:
```
'A/A.Common.Tests/A.Common.Tests.csproj'
```

Example: One file is changed and there are two test projects that depend on the file, one is a transitive dependency:
```shell
find-tests 'A/A.Common/Class1.cs\nA/A.Common/Class2.cs' '{"Projects":[{"Id": "A/A.Common/A.Common.csproj"}, {"Id": "B.Logic/B.Logic.csproj"}, {"Id": "A/A.Common.Tests/A.Common.Tests.csproj"}, {"Id": "B.Logic.Tests/B.Logic.Tests.csproj"}], "References":[{"From": "A/A.Common.Tests/A.Common.Tests.csproj", "To": "A/A.Common/A.Common.csproj"}, {"From": "B.Logic/B.Logic.csproj", "To": "A/A.Common/A.Common.csproj"}, {"From": "B.Logic.Tests/B.Logic.Tests.csproj", "To": "B.Logic/B.Logic.csproj"}]}'
```
Returns:
```
'A/A.Common.Tests/A.Common.Tests.csproj' 'B.Logic.Tests/B.Logic.Tests.csproj'
```

If no tests are found, an empty string is returned.
```shell
$ test_projects=$(find-tests "$changedFiles" "$graph")
$ [ "$test_projects" = "" ] && echo "No tests found."
No tests found.
```

## Example in Continuous Integration

Get the changed files for a pull request.
```shell
git fetch --depth=1 origin main
changedFiles=$(git diff --name-only origin/main)
```

Get the project dependency graph.
For .NET, use [DependenSee](https://github.com/madushans/DependenSee).
```shell
dotnet tool install DependenSee --global
graph=$(DependenSee <code_path> -T ConsoleJson)
```

Find the tests.
```shell
test_projects=$(find-tests "$changedFiles" "$graph")
```

# Dev Setup
Written using Python 3.11

Example Python environment initialization with Conda:
```shell
conda create --yes --name find-tests python=3.11
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
pytest
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
