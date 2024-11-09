import json
import sys

from .find_dotnet_test_projects import DotNetTestFinder


def main():
    """Find tests in projects."""
    finder = DotNetTestFinder()
    file_paths = json.loads(sys.argv[1])
    graph = json.loads(sys.argv[2])
    test_projects = finder.find_test_projects(file_paths, graph)
    # Print all so that they can easily be given to `dotnet test`.
    print(' '.join(f"'{p}'" for p in test_projects))


if __name__ == '__main__':
    main()
