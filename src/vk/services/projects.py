"""Project service."""

from __future__ import annotations

from vk.client import VikunjaClient
from vk.models import Project


class ProjectService:
    def __init__(self, client: VikunjaClient) -> None:
        self.client = client

    def list(self) -> list[Project]:
        data = self.client.get("/projects")
        return [Project.from_api(p) for p in data]

    def get(self, project_id: int) -> Project:
        data = self.client.get(f"/projects/{project_id}", paginate=False)
        return Project.from_api(data)

    def create(self, title: str) -> Project:
        data = self.client.put("/projects", json={"title": title})
        return Project.from_api(data)
