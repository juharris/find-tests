"""
Module for finding test projects affected by changes in source files.
"""

from collections import defaultdict, deque
from pathlib import Path
from .graph import ProjectDependencyGraph


class DotNetTestFinder:
    """
    Finds test projects affected by changes in source files.
    """

    def _get_project_for_file(self,
                              file_path: str,
                              project_folder_to_project_path: dict[Path, Path]) -> Path | None:
        file_path = Path(file_path)
        for project_folder, project_path in project_folder_to_project_path.items():
            if file_path.is_relative_to(project_folder):
                return project_path
        return None

    def _is_test_project(self, project_path: Path) -> bool:
        return str(project_path).endswith(".Tests.csproj")

    def _normalize_project_path(self, project_path: str) -> Path:
        if project_path.startswith("\\"):
            project_path = project_path[1:]
        # Replace Windows-style backslashes with Unix-style forward slashes.
        # Assume that directory and file names do not contain backslashes.
        return Path(project_path.replace("\\", "/"))

    def find_test_projects(self, file_paths: list[str], graph: ProjectDependencyGraph) -> list[str]:
        """
        Finds test projects affected by changes in the given files.

        Args:
            file_paths: List of files for which to find test projects.
            graph: Dependency graph of the repository or solution.

        Returns:
            List of test projects that need to be run.
        """
        result = []
        project_folder_to_project_path: dict[Path, Path] = {}
        for project in graph["Projects"]:
            project_path = self._normalize_project_path(project["Id"])
            project_folder_to_project_path[project_path.parent] = project_path
        edges: dict[str, list[str]] = defaultdict(list)
        for reference in graph["References"]:
            # Edges in References are from a project and to a project that it depends on,
            # but we're interested in the reverse direction because we want to find all projects
            # that depend on a given project.
            to_project = self._normalize_project_path(reference["To"])
            from_project = self._normalize_project_path(reference["From"])
            edges[to_project].append(from_project)
        visited_projects = set()

        for file_path in file_paths:
            project = self._get_project_for_file(file_path, project_folder_to_project_path)
            if project is None:
                # TODO Maybe raise an exception because maybe all tests should run?
                continue
            if project in visited_projects:
                continue
            queue = deque([project])

            while queue:
                project = queue.popleft()
                # Skip if we've already processed this project
                if project in visited_projects:
                    continue
                visited_projects.add(project)

                if self._is_test_project(project):
                    result.append(project.as_posix())
                queue.extend(edges[project])

        return result
