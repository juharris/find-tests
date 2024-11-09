from injector import Injector

from find_test_projects import TestFinder
from graph import ProjectDependencyGraph


def test_find_tests():
    inj = Injector()
    finder = inj.get(TestFinder)
    graph: ProjectDependencyGraph = {
        "References": [
            {"From": "\\B\\B.Common\\B.Common.csproj", "To": "\\A\\A.Common\\A.Common.csproj"},
            {"From": "\\A\\A.Common.Tests\\A.Common.Tests.csproj", "To": "\\A\\A.Common\\A.Common.csproj"},
            {"From": "\\C\\C.Logic\\C.Logic.csproj", "To": "\\B\\B.Common\\B.Common.csproj"},
            {"From": "\\B\\B.Common.Tests\\B.Common.Tests.csproj", "To": "\\B\\B.Common\\B.Common.csproj"},
            {"From": "\\tests\\Many.Tests\\Many.Tests.csproj", "To": "\\B\\B.Common\\B.Common.csproj"},
            {"From": "\\tests\\Many.Tests\\Many.Tests.csproj", "To": "\\C\\C.Logic\\C.Logic.csproj"},
            {"From": "\\tests\\Also.Tests\\Also.Tests.csproj", "To": "\\C\\C.Logic\\C.Logic.csproj"},
        ]
    }

    graph["Projects"] = [{"Id": p} for p in set(project["From"] for project in graph["References"])
                         | set(project["To"] for project in graph["References"])]

    file_paths = ["A/A.Common/A.Common.cs"]
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
