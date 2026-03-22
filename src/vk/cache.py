"""Name resolution cache for projects, buckets, and views."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from vk.exceptions import AmbiguousNameError


class NameCache:
    """Resolves human-readable names to IDs.

    Caches are stored in .vk-cache.json in the project root.
    """

    def __init__(self, cache_path: Path | None = None) -> None:
        self._path = cache_path or Path.cwd() / ".vk-cache.json"
        self._data: dict[str, Any] = {}
        if self._path.exists():
            self._data = json.loads(self._path.read_text())

    def _save(self) -> None:
        self._path.write_text(json.dumps(self._data, indent=2) + "\n")

    def set_projects(self, projects: list[dict[str, Any]]) -> None:
        self._data["projects"] = {p["title"]: p["id"] for p in projects}
        self._save()

    def set_buckets(self, view_id: int, buckets: list[dict[str, Any]]) -> None:
        key = f"buckets_{view_id}"
        self._data[key] = {b["title"]: b["id"] for b in buckets}
        self._save()

    def resolve_project(self, name: str) -> int:
        projects = self._data.get("projects", {})
        # Exact match first
        if name in projects:
            return projects[name]
        # Case-insensitive
        matches = [(k, v) for k, v in projects.items() if k.lower() == name.lower()]
        if len(matches) == 1:
            return matches[0][1]
        if len(matches) > 1:
            raise AmbiguousNameError(name, [m[0] for m in matches])
        # Substring match
        matches = [(k, v) for k, v in projects.items() if name.lower() in k.lower()]
        if len(matches) == 1:
            return matches[0][1]
        if len(matches) > 1:
            raise AmbiguousNameError(name, [m[0] for m in matches])
        raise KeyError(f"Project '{name}' not found in cache. Run a project list first.")

    def resolve_bucket(self, name: str, view_id: int) -> int:
        key = f"buckets_{view_id}"
        buckets = self._data.get(key, {})
        if name in buckets:
            return buckets[name]
        matches = [(k, v) for k, v in buckets.items() if k.lower() == name.lower()]
        if len(matches) == 1:
            return matches[0][1]
        if len(matches) > 1:
            raise AmbiguousNameError(name, [m[0] for m in matches])
        raise KeyError(f"Bucket '{name}' not found in cache for view {view_id}.")

    def clear(self) -> None:
        self._data = {}
        if self._path.exists():
            self._path.unlink()
