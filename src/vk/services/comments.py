"""Comment service."""

from __future__ import annotations

from vk.client import VikunjaClient
from vk.models import Comment


class CommentService:
    def __init__(self, client: VikunjaClient) -> None:
        self.client = client

    def list(self, task_id: int) -> list[Comment]:
        data = self.client.get(f"/tasks/{task_id}/comments")
        return [Comment.from_api(c) for c in data]

    def add(self, task_id: int, text: str) -> Comment:
        data = self.client.put(
            f"/tasks/{task_id}/comments",
            json={"comment": text},
        )
        return Comment.from_api(data)
