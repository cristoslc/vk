"""Tests for the task service."""

from __future__ import annotations

import responses

from vk.client import VikunjaClient
from vk.services.tasks import TaskService

import pytest

BASE_URL = "http://vikunja.test"


@pytest.fixture
def task_service() -> TaskService:
    client = VikunjaClient(BASE_URL, "test-token")
    return TaskService(client)


class TestTaskList:
    @responses.activate
    def test_list_tasks(self, task_service: TaskService) -> None:
        responses.add(
            responses.GET,
            f"{BASE_URL}/api/v1/projects/1/tasks",
            json=[
                {"id": 1, "title": "Task A", "bucket_id": 7},
                {"id": 2, "title": "Task B", "bucket_id": 8},
            ],
        )
        tasks = task_service.list(project_id=1)
        assert len(tasks) == 2
        assert tasks[0].title == "Task A"

    @responses.activate
    def test_list_filters_by_bucket(self, task_service: TaskService) -> None:
        responses.add(
            responses.GET,
            f"{BASE_URL}/api/v1/projects/1/tasks",
            json=[
                {"id": 1, "title": "Task A", "bucket_id": 7},
                {"id": 2, "title": "Task B", "bucket_id": 8},
            ],
        )
        tasks = task_service.list(project_id=1, bucket_id=7)
        assert len(tasks) == 1
        assert tasks[0].id == 1


class TestTaskCRUD:
    @responses.activate
    def test_get_task(self, task_service: TaskService) -> None:
        responses.add(
            responses.GET,
            f"{BASE_URL}/api/v1/tasks/42",
            json={"id": 42, "title": "Get milk"},
        )
        t = task_service.get(42)
        assert t.id == 42
        assert t.title == "Get milk"

    @responses.activate
    def test_create_task(self, task_service: TaskService) -> None:
        responses.add(
            responses.PUT,
            f"{BASE_URL}/api/v1/projects/1/tasks",
            json={"id": 99, "title": "New task", "project_id": 1},
        )
        t = task_service.create(title="New task", project_id=1)
        assert t.id == 99
        assert t.title == "New task"

    @responses.activate
    def test_update_task(self, task_service: TaskService) -> None:
        responses.add(
            responses.POST,
            f"{BASE_URL}/api/v1/tasks/1",
            json={"id": 1, "title": "Updated", "done": True},
        )
        t = task_service.update(1, title="Updated", done=True)
        assert t.done is True

    @responses.activate
    def test_delete_task(self, task_service: TaskService) -> None:
        responses.add(
            responses.DELETE,
            f"{BASE_URL}/api/v1/tasks/1",
            status=204,
        )
        task_service.delete(1)  # Should not raise


class TestTaskMove:
    @responses.activate
    def test_move_task(self, task_service: TaskService) -> None:
        responses.add(
            responses.POST,
            f"{BASE_URL}/api/v1/projects/1/views/4/buckets/7/tasks",
            json={},
        )
        responses.add(
            responses.GET,
            f"{BASE_URL}/api/v1/tasks/42",
            json={"id": 42, "title": "Moved", "bucket_id": 7},
        )
        t = task_service.move(task_id=42, bucket_id=7, project_id=1, view_id=4)
        assert t.bucket_id == 7
