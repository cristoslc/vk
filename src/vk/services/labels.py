"""Label service."""

from __future__ import annotations

from vk.client import VikunjaClient
from vk.models import Label


class LabelService:
    def __init__(self, client: VikunjaClient) -> None:
        self.client = client

    def list(self) -> list[Label]:
        data = self.client.get("/labels")
        return [Label.from_api(l) for l in data]

    def create(self, title: str, color: str | None = None) -> Label:
        body: dict = {"title": title}
        if color:
            body["hex_color"] = color
        data = self.client.put("/labels", json=body)
        return Label.from_api(data)
