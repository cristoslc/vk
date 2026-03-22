"""Tests for the project service."""

from __future__ import annotations

import responses

from vk.client import VikunjaClient
from vk.services.projects import ProjectService

import pytest

BASE_URL = "http://vikunja.test"


@pytest.fixture
def project_service() -> ProjectService:
    return ProjectService(VikunjaClient(BASE_URL, "test-token"))


class TestProjectService:
    @responses.activate
    def test_list_projects(self, project_service: ProjectService) -> None:
        responses.add(
            responses.GET,
            f"{BASE_URL}/api/v1/projects",
            json=[{"id": 1, "title": "Household"}, {"id": 2, "title": "Work"}],
        )
        projects = project_service.list()
        assert len(projects) == 2

    @responses.activate
    def test_get_project(self, project_service: ProjectService) -> None:
        responses.add(
            responses.GET,
            f"{BASE_URL}/api/v1/projects/1",
            json={"id": 1, "title": "Household"},
        )
        p = project_service.get(1)
        assert p.title == "Household"

    @responses.activate
    def test_create_project(self, project_service: ProjectService) -> None:
        responses.add(
            responses.PUT,
            f"{BASE_URL}/api/v1/projects",
            json={"id": 5, "title": "New Project"},
        )
        p = project_service.create("New Project")
        assert p.id == 5
