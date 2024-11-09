"""
Module containing type definitions for project dependency graphs.
"""

from typing import TypedDict


class Project(TypedDict):
    Id: str
    Name: str


class Package(TypedDict):
    pass


class Reference(TypedDict):
    From: str
    To: str


class ProjectDependencyGraph(TypedDict):
    """
    DependenSee style based on .NET project references.
    """
    Projects: list[Project]
    Packages: list[Package]
    References: list[Reference]
