from src.find_dotnet_test_projects import DotNetTestFinder
from src.graph import ProjectDependencyGraph

finder = DotNetTestFinder()
graph: ProjectDependencyGraph = {
    "References": [
        {"From": "\\B\\B.Common\\B.Common.csproj", "To": "\\A\\A.Common\\A.Common.csproj"},
        {"From": "A/A.Common.Tests/A.Common.Tests.csproj", "To": "A/A.Common/A.Common.csproj"},
        {"From": "\\C\\C.Logic\\C.Logic.csproj", "To": "\\B\\B.Common\\B.Common.csproj"},
        {"From": "\\B\\B.Common.Tests\\B.Common.Tests.csproj", "To": "\\B\\B.Common\\B.Common.csproj"},
        {"From": "\\tests\\Many.Tests\\Many.Tests.csproj", "To": "\\B\\B.Common\\B.Common.csproj"},
        {"From": "tests/Many.Tests/Many.Tests.csproj", "To": "\\C\\C.Logic\\C.Logic.csproj"},
        {"From": "\\tests\\Also.Tests\\Also.Tests.csproj", "To": "\\C\\C.Logic\\C.Logic.csproj"},
    ]
}

graph["Projects"] = [{"Id": p} for p in set(project["From"] for project in graph["References"])
                     | set(project["To"] for project in graph["References"])]


def test_find_test_projects_simple():
    file_paths = ["A/A.Common/Common.cs"]
    assert finder.find_test_projects(file_paths, graph) == [
        "A/A.Common.Tests/A.Common.Tests.csproj",
        "B/B.Common.Tests/B.Common.Tests.csproj",
        "tests/Many.Tests/Many.Tests.csproj",
        "tests/Also.Tests/Also.Tests.csproj",
    ]

    file_paths = ["A/A.Common/Subdir1/Subdir2/Common.cs"]
    assert finder.find_test_projects(file_paths, graph) == [
        "A/A.Common.Tests/A.Common.Tests.csproj",
        "B/B.Common.Tests/B.Common.Tests.csproj",
        "tests/Many.Tests/Many.Tests.csproj",
        "tests/Also.Tests/Also.Tests.csproj",
    ]

    file_paths = ["A/A.Common/A.Common.csproj"]
    assert finder.find_test_projects(file_paths, graph) == [
        "A/A.Common.Tests/A.Common.Tests.csproj",
        "B/B.Common.Tests/B.Common.Tests.csproj",
        "tests/Many.Tests/Many.Tests.csproj",
        "tests/Also.Tests/Also.Tests.csproj",
    ]

    file_paths = ["B/B.Common/B.Common.cs"]
    assert finder.find_test_projects(file_paths, graph) == [
        "B/B.Common.Tests/B.Common.Tests.csproj",
        "tests/Many.Tests/Many.Tests.csproj",
        "tests/Also.Tests/Also.Tests.csproj",
    ]

    file_paths = ["C/C.Logic/C.Logic.cs"]
    assert finder.find_test_projects(file_paths, graph) == [
        "tests/Many.Tests/Many.Tests.csproj",
        "tests/Also.Tests/Also.Tests.csproj",
    ]

    file_paths = ["A/A.Common/A.Common.cs", "C/C.Logic/C.Logic.cs"]
    assert finder.find_test_projects(file_paths, graph) == [
        "A/A.Common.Tests/A.Common.Tests.csproj",
        "B/B.Common.Tests/B.Common.Tests.csproj",
        "tests/Many.Tests/Many.Tests.csproj",
        "tests/Also.Tests/Also.Tests.csproj",
    ]

    file_paths = ["C/C.Logic/C.Logic.cs", "B/B.Common/B.Common.cs"]
    assert finder.find_test_projects(file_paths, graph) == [
        "tests/Many.Tests/Many.Tests.csproj",
        "tests/Also.Tests/Also.Tests.csproj",
        "B/B.Common.Tests/B.Common.Tests.csproj",
    ]


def test_find_test_projects_none():
    # TODO There needs to be some indication that no tests were found for a file.
    # Raise an exception?
    file_paths = ["none"]
    assert finder.find_test_projects(file_paths, graph) == []


def test_find_test_projects_for_test_file():
    file_paths = ["B/B.Common.Tests/WhateverTests.cs"]
    assert finder.find_test_projects(file_paths, graph) == [
        "B/B.Common.Tests/B.Common.Tests.csproj",
    ]
