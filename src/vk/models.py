"""Domain models for Vikunja resources."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


def _parse_dt(value: str | None) -> datetime | None:
    if not value or value == "0001-01-01T00:00:00Z":
        return None
    # Vikunja uses ISO-8601 with Z suffix
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    done: bool = False
    priority: int = 0
    due_date: datetime | None = None
    project_id: int = 0
    bucket_id: int = 0
    created: datetime | None = None
    updated: datetime | None = None

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Task:
        return cls(
            id=data.get("id", 0),
            title=data.get("title", ""),
            description=data.get("description", ""),
            done=data.get("done", False),
            priority=data.get("priority", 0),
            due_date=_parse_dt(data.get("due_date")),
            project_id=data.get("project_id", 0),
            bucket_id=data.get("bucket_id", 0),
            created=_parse_dt(data.get("created")),
            updated=_parse_dt(data.get("updated")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "done": self.done,
            "priority": self.priority,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "project_id": self.project_id,
            "bucket_id": self.bucket_id,
            "created": self.created.isoformat() if self.created else None,
            "updated": self.updated.isoformat() if self.updated else None,
        }


@dataclass
class Project:
    id: int
    title: str
    description: str = ""
    created: datetime | None = None
    updated: datetime | None = None

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Project:
        return cls(
            id=data.get("id", 0),
            title=data.get("title", ""),
            description=data.get("description", ""),
            created=_parse_dt(data.get("created")),
            updated=_parse_dt(data.get("updated")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "created": self.created.isoformat() if self.created else None,
            "updated": self.updated.isoformat() if self.updated else None,
        }


@dataclass
class View:
    id: int
    title: str
    project_id: int = 0
    view_kind: int = 0  # 0=list, 1=gantt, 2=table, 3=kanban
    default_bucket_id: int = 0
    done_bucket_id: int = 0

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> View:
        return cls(
            id=data.get("id", 0),
            title=data.get("title", ""),
            project_id=data.get("project_id", 0),
            view_kind=data.get("view_kind", 0),
            default_bucket_id=data.get("default_bucket_id", 0),
            done_bucket_id=data.get("done_bucket_id", 0),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "project_id": self.project_id,
            "view_kind": self.view_kind,
            "default_bucket_id": self.default_bucket_id,
            "done_bucket_id": self.done_bucket_id,
        }


@dataclass
class Bucket:
    id: int
    title: str
    project_id: int = 0
    view_id: int = 0
    position: float = 0.0
    created: datetime | None = None
    updated: datetime | None = None

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Bucket:
        return cls(
            id=data.get("id", 0),
            title=data.get("title", ""),
            project_id=data.get("project_id", 0),
            view_id=data.get("view_id", 0),
            position=data.get("position", 0.0),
            created=_parse_dt(data.get("created")),
            updated=_parse_dt(data.get("updated")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "project_id": self.project_id,
            "view_id": self.view_id,
            "position": self.position,
            "created": self.created.isoformat() if self.created else None,
            "updated": self.updated.isoformat() if self.updated else None,
        }


@dataclass
class Comment:
    id: int
    task_id: int
    comment: str = ""
    author: str = ""
    created: datetime | None = None
    updated: datetime | None = None

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Comment:
        author = ""
        if author_data := data.get("author"):
            author = author_data.get("username", "") if isinstance(author_data, dict) else str(author_data)
        return cls(
            id=data.get("id", 0),
            task_id=data.get("task_id", 0),
            comment=data.get("comment", ""),
            author=author,
            created=_parse_dt(data.get("created")),
            updated=_parse_dt(data.get("updated")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "task_id": self.task_id,
            "comment": self.comment,
            "author": self.author,
            "created": self.created.isoformat() if self.created else None,
            "updated": self.updated.isoformat() if self.updated else None,
        }


@dataclass
class Attachment:
    id: int
    task_id: int
    file: dict[str, Any] = field(default_factory=dict)
    created: datetime | None = None

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Attachment:
        return cls(
            id=data.get("id", 0),
            task_id=data.get("task_id", 0),
            file=data.get("file", {}),
            created=_parse_dt(data.get("created")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "task_id": self.task_id,
            "file": self.file,
            "created": self.created.isoformat() if self.created else None,
        }


@dataclass
class Label:
    id: int
    title: str
    hex_color: str = ""
    created: datetime | None = None
    updated: datetime | None = None

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Label:
        return cls(
            id=data.get("id", 0),
            title=data.get("title", ""),
            hex_color=data.get("hex_color", ""),
            created=_parse_dt(data.get("created")),
            updated=_parse_dt(data.get("updated")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "hex_color": self.hex_color,
            "created": self.created.isoformat() if self.created else None,
            "updated": self.updated.isoformat() if self.updated else None,
        }


@dataclass
class User:
    id: int
    username: str
    email: str = ""
    name: str = ""

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> User:
        return cls(
            id=data.get("id", 0),
            username=data.get("username", ""),
            email=data.get("email", ""),
            name=data.get("name", ""),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "name": self.name,
        }


@dataclass
class ApiToken:
    id: int
    title: str
    token: str = ""
    permissions: dict[str, list[str]] = field(default_factory=dict)
    expires_at: datetime | None = None

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> ApiToken:
        return cls(
            id=data.get("id", 0),
            title=data.get("title", ""),
            token=data.get("token", ""),
            permissions=data.get("permissions", {}),
            expires_at=_parse_dt(data.get("expires_at")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "token": self.token,
            "permissions": self.permissions,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
        }
