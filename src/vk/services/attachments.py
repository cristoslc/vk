"""Attachment service."""

from __future__ import annotations

from pathlib import Path

from vk.client import VikunjaClient
from vk.models import Attachment


class AttachmentService:
    def __init__(self, client: VikunjaClient) -> None:
        self.client = client

    def list(self, task_id: int) -> list[Attachment]:
        data = self.client.get(f"/tasks/{task_id}/attachments")
        if data is None:
            return []
        return [Attachment.from_api(a) for a in data]

    def add(self, task_id: int, file_path: str) -> Attachment:
        data = self.client.upload(f"/tasks/{task_id}/attachments", file_path)
        # Upload response wraps in {"success": ..., ...}
        if isinstance(data, dict) and "success" in data:
            return Attachment.from_api(data.get("success", data))
        return Attachment.from_api(data)

    def get(
        self,
        task_id: int,
        attachment_id: int,
        output_path: str | None = None,
    ) -> bytes:
        content = self.client.download(
            f"/tasks/{task_id}/attachments/{attachment_id}"
        )
        if output_path:
            Path(output_path).write_bytes(content)
        return content
