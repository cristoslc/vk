"""Search service."""

from __future__ import annotations

from vk.client import VikunjaClient
from vk.models import Task


class SearchService:
    def __init__(self, client: VikunjaClient) -> None:
        self.client = client

    def search(
        self,
        query: str,
        project_id: int | None = None,
        done: bool | None = None,
    ) -> list[Task]:
        params: dict = {"s": query}
        if done is not None:
            params["filter"] = f"done = {str(done).lower()}"
        # Vikunja's search is on /tasks with ?s= param
        data = self.client.get("/tasks", params=params)
        tasks = [Task.from_api(t) for t in data]
        if project_id is not None:
            tasks = [t for t in tasks if t.project_id == project_id]
        return tasks
