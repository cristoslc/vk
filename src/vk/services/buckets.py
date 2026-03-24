"""Bucket and view service."""

from __future__ import annotations

from vk.client import VikunjaClient
from vk.models import Bucket, View


class BucketService:
    def __init__(self, client: VikunjaClient) -> None:
        self.client = client

    def list_views(self, project_id: int) -> list[View]:
        data = self.client.get(f"/projects/{project_id}/views")
        return [View.from_api(v) for v in data]

    def get_kanban_view(self, project_id: int, view_name: str | None = None) -> View:
        """Find the kanban view for a project. Defaults to first kanban view."""
        views = self.list_views(project_id)
        if view_name:
            for v in views:
                if v.title.lower() == view_name.lower():
                    return v
        # Default: first kanban view
        for v in views:
            if v.view_kind == "kanban":
                return v
        raise ValueError(f"No kanban view found for project {project_id}")

    def list(self, project_id: int, view_id: int) -> list[Bucket]:
        data = self.client.get(
            f"/projects/{project_id}/views/{view_id}/buckets"
        )
        return [Bucket.from_api(b) for b in data]

    def create(
        self, project_id: int, title: str, view_id: int
    ) -> Bucket:
        data = self.client.put(
            f"/projects/{project_id}/views/{view_id}/buckets",
            json={"title": title},
        )
        return Bucket.from_api(data)
