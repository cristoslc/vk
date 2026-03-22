"""Tests for domain models."""

from __future__ import annotations

from vk.models import Task, Project, Bucket, Comment, Label, View


class TestTask:
    def test_from_api_full(self) -> None:
        data = {
            "id": 42,
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
            "done": False,
            "priority": 3,
            "due_date": "2026-04-01T00:00:00Z",
            "project_id": 1,
            "bucket_id": 7,
            "created": "2026-03-22T10:00:00Z",
            "updated": "2026-03-22T10:00:00Z",
        }
        t = Task.from_api(data)
        assert t.id == 42
        assert t.title == "Buy groceries"
        assert t.priority == 3
        assert t.due_date is not None
        assert t.due_date.year == 2026

    def test_from_api_missing_optional_fields(self) -> None:
        data = {"id": 1, "title": "Minimal task"}
        t = Task.from_api(data)
        assert t.id == 1
        assert t.due_date is None
        assert t.done is False

    def test_to_dict_roundtrip(self) -> None:
        data = {
            "id": 10,
            "title": "Test",
            "description": "",
            "done": True,
            "priority": 0,
            "due_date": None,
            "project_id": 1,
            "bucket_id": 0,
            "created": None,
            "updated": None,
        }
        t = Task.from_api(data)
        d = t.to_dict()
        assert d["id"] == 10
        assert d["done"] is True

    def test_null_date_handling(self) -> None:
        data = {"id": 1, "title": "x", "due_date": "0001-01-01T00:00:00Z"}
        t = Task.from_api(data)
        assert t.due_date is None


class TestProject:
    def test_from_api(self) -> None:
        data = {"id": 2, "title": "Household", "description": "Home tasks"}
        p = Project.from_api(data)
        assert p.title == "Household"

    def test_to_dict(self) -> None:
        p = Project(id=1, title="Test")
        d = p.to_dict()
        assert d["title"] == "Test"


class TestBucket:
    def test_from_api(self) -> None:
        data = {"id": 7, "title": "Do Now", "project_id": 1, "view_id": 4}
        b = Bucket.from_api(data)
        assert b.title == "Do Now"
        assert b.view_id == 4


class TestView:
    def test_from_api(self) -> None:
        data = {"id": 4, "title": "Kanban", "view_kind": 3, "project_id": 1}
        v = View.from_api(data)
        assert v.view_kind == 3


class TestComment:
    def test_from_api_with_author(self) -> None:
        data = {
            "id": 1,
            "task_id": 42,
            "comment": "Progress update",
            "author": {"username": "cristos"},
        }
        c = Comment.from_api(data)
        assert c.author == "cristos"
        assert c.comment == "Progress update"


class TestLabel:
    def test_from_api(self) -> None:
        data = {"id": 3, "title": "urgent", "hex_color": "ff0000"}
        l = Label.from_api(data)
        assert l.hex_color == "ff0000"
