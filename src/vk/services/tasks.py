"""Task service — CRUD, move, and search operations on tasks."""

from __future__ import annotations

import re

from vk.client import VikunjaClient
from vk.models import Task

_DATE_ONLY = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _normalize_due_date(value: str | None) -> str | None:
    """Ensure date-only strings become full ISO-8601 datetimes."""
    if value and _DATE_ONLY.match(value):
        return f"{value}T00:00:00Z"
    return value


class TaskService:
    def __init__(self, client: VikunjaClient) -> None:
        self.client = client

    def list(
        self,
        project_id: int,
        bucket_id: int | None = None,
        done: bool | None = None,
    ) -> list[Task]:
        params: dict = {}
        if done is not None:
            params["filter"] = f"done = {str(done).lower()}"
        data = self.client.get(f"/projects/{project_id}/tasks", params=params)
        tasks = [Task.from_api(t) for t in data]
        if bucket_id is not None:
            tasks = [t for t in tasks if t.bucket_id == bucket_id]
        return tasks

    def get(self, task_id: int) -> Task:
        data = self.client.get(f"/tasks/{task_id}", paginate=False)
        return Task.from_api(data)

    def create(
        self,
        title: str,
        project_id: int,
        bucket_id: int | None = None,
        due_date: str | None = None,
        priority: int | None = None,
        description: str | None = None,
    ) -> Task:
        body: dict = {"title": title}
        if due_date:
            body["due_date"] = _normalize_due_date(due_date)
        if priority is not None:
            body["priority"] = priority
        if description:
            body["description"] = description
        if bucket_id is not None:
            body["bucket_id"] = bucket_id
        data = self.client.put(f"/projects/{project_id}/tasks", json=body)
        return Task.from_api(data)

    def update(
        self,
        task_id: int,
        title: str | None = None,
        done: bool | None = None,
        priority: int | None = None,
        due_date: str | None = None,
        description: str | None = None,
    ) -> Task:
        body: dict = {}
        if title is not None:
            body["title"] = title
        if done is not None:
            body["done"] = done
        if priority is not None:
            body["priority"] = priority
        if due_date is not None:
            body["due_date"] = _normalize_due_date(due_date)
        if description is not None:
            body["description"] = description
        data = self.client.post(f"/tasks/{task_id}", json=body)
        return Task.from_api(data)

    def move(
        self,
        task_id: int,
        bucket_id: int,
        project_id: int,
        view_id: int,
    ) -> Task:
        self.client.post(
            f"/projects/{project_id}/views/{view_id}/buckets/{bucket_id}/tasks",
            json={"task_id": task_id},
        )
        return self.get(task_id)

    def delete(self, task_id: int) -> None:
        self.client.delete(f"/tasks/{task_id}")
