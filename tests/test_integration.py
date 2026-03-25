"""Integration tests against a live Vikunja instance.

Requires a running Vikunja with valid credentials in .vk-config.json or
VK_URL/VK_TOKEN env vars. Run with:

    uv run pytest tests/test_integration.py -m integration -v
"""

from __future__ import annotations

import uuid

import pytest

from vk.client import VikunjaClient
from vk.config import Config
from vk.exceptions import NotFoundError
from vk.services.auth import AuthService
from vk.services.projects import ProjectService
from vk.services.tasks import TaskService
from vk.services.labels import LabelService
from vk.services.comments import CommentService
from vk.services.search import SearchService
from vk.services.buckets import BucketService
from vk.services.attachments import AttachmentService

pytestmark = pytest.mark.integration


def _unique(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


@pytest.fixture(scope="module")
def config() -> Config:
    """Load config from the real config file."""
    return Config()


@pytest.fixture(scope="module")
def client(config: Config) -> VikunjaClient:
    return VikunjaClient(config.url, config.token)


@pytest.fixture(scope="module")
def project_svc(client: VikunjaClient) -> ProjectService:
    return ProjectService(client)


@pytest.fixture(scope="module")
def task_svc(client: VikunjaClient) -> TaskService:
    return TaskService(client)


@pytest.fixture(scope="module")
def label_svc(client: VikunjaClient) -> LabelService:
    return LabelService(client)


@pytest.fixture(scope="module")
def comment_svc(client: VikunjaClient) -> CommentService:
    return CommentService(client)


@pytest.fixture(scope="module")
def search_svc(client: VikunjaClient) -> SearchService:
    return SearchService(client)


@pytest.fixture(scope="module")
def bucket_svc(client: VikunjaClient) -> BucketService:
    return BucketService(client)


@pytest.fixture(scope="module")
def attachment_svc(client: VikunjaClient) -> AttachmentService:
    return AttachmentService(client)


@pytest.fixture(scope="module")
def test_project(project_svc: ProjectService):
    """Create a throwaway project for the test run, delete it after."""
    proj = project_svc.create(_unique("vk-inttest"))
    yield proj
    # Cleanup: Vikunja cascades task/bucket/comment deletes with the project
    try:
        project_svc.client.delete(f"/projects/{proj.id}")
    except Exception:
        pass


class TestAuth:
    def test_status(self, config: Config) -> None:
        result = AuthService.status(config)
        assert result["connected"] is True
        assert result["url"]
        assert result["user"]


class TestProjects:
    def test_list_includes_test_project(
        self, project_svc: ProjectService, test_project
    ) -> None:
        projects = project_svc.list()
        ids = [p.id for p in projects]
        assert test_project.id in ids

    def test_get_project(self, project_svc: ProjectService, test_project) -> None:
        proj = project_svc.get(test_project.id)
        assert proj.id == test_project.id
        assert proj.title == test_project.title

    def test_create_and_delete_project(self, project_svc: ProjectService) -> None:
        proj = project_svc.create(_unique("vk-tmpproj"))
        assert proj.id > 0
        assert proj.title.startswith("vk-tmpproj")
        # Clean up
        project_svc.client.delete(f"/projects/{proj.id}")
        with pytest.raises(NotFoundError):
            project_svc.get(proj.id)


class TestTasks:
    def test_create_and_get(self, task_svc: TaskService, test_project) -> None:
        task = task_svc.create(title=_unique("task"), project_id=test_project.id)
        assert task.id > 0
        assert task.project_id == test_project.id

        fetched = task_svc.get(task.id)
        assert fetched.title == task.title

    def test_list_tasks(self, task_svc: TaskService, test_project) -> None:
        task_svc.create(title=_unique("list-task"), project_id=test_project.id)
        tasks = task_svc.list(project_id=test_project.id)
        assert len(tasks) >= 1

    def test_update_task(self, task_svc: TaskService, test_project) -> None:
        task = task_svc.create(title=_unique("upd"), project_id=test_project.id)
        updated = task_svc.update(task.id, title="Updated Title", done=True)
        assert updated.title == "Updated Title"
        assert updated.done is True

    def test_create_with_optional_fields(
        self, task_svc: TaskService, test_project
    ) -> None:
        task = task_svc.create(
            title=_unique("detailed"),
            project_id=test_project.id,
            priority=3,
            description="A test description",
        )
        fetched = task_svc.get(task.id)
        assert fetched.priority == 3
        assert fetched.description == "A test description"

    def test_create_with_date_only_due_date(
        self, task_svc: TaskService, test_project
    ) -> None:
        """Regression test for gh#1: date-only --due values cause HTTP 400."""
        task = task_svc.create(
            title=_unique("due-date"),
            project_id=test_project.id,
            due_date="2026-03-25",
        )
        fetched = task_svc.get(task.id)
        assert fetched.due_date is not None

    def test_update_with_date_only_due_date(
        self, task_svc: TaskService, test_project
    ) -> None:
        task = task_svc.create(title=_unique("upd-due"), project_id=test_project.id)
        updated = task_svc.update(task.id, due_date="2026-04-01")
        assert updated.due_date is not None

    def test_delete_task(self, task_svc: TaskService, test_project) -> None:
        task = task_svc.create(title=_unique("del"), project_id=test_project.id)
        task_svc.delete(task.id)
        with pytest.raises(NotFoundError):
            task_svc.get(task.id)


class TestLabels:
    def test_create_and_list(self, label_svc: LabelService) -> None:
        label = label_svc.create(_unique("label"), color="#ff0000")
        assert label.id > 0
        assert label.title.startswith("label")

        labels = label_svc.list()
        ids = [l.id for l in labels]
        assert label.id in ids


class TestComments:
    def test_add_and_list(
        self, comment_svc: CommentService, task_svc: TaskService, test_project
    ) -> None:
        task = task_svc.create(title=_unique("cmt-task"), project_id=test_project.id)
        comment = comment_svc.add(task.id, "Integration test comment")
        assert comment.id > 0
        assert comment.comment == "Integration test comment"

        comments = comment_svc.list(task.id)
        ids = [c.id for c in comments]
        assert comment.id in ids


class TestSearch:
    def test_search_finds_task(
        self, search_svc: SearchService, task_svc: TaskService, test_project
    ) -> None:
        unique_word = _unique("searchable")
        task_svc.create(title=unique_word, project_id=test_project.id)
        results = search_svc.search(unique_word)
        titles = [t.title for t in results]
        assert unique_word in titles


class TestBuckets:
    def test_list_views(self, bucket_svc: BucketService, test_project) -> None:
        views = bucket_svc.list_views(test_project.id)
        assert len(views) >= 1

    def test_get_kanban_view_and_buckets(
        self, bucket_svc: BucketService, test_project
    ) -> None:
        try:
            kanban = bucket_svc.get_kanban_view(test_project.id)
        except ValueError:
            pytest.skip("No kanban view on test project")
        buckets = bucket_svc.list(test_project.id, kanban.id)
        assert isinstance(buckets, list)

    def test_create_and_delete_bucket(
        self, bucket_svc: BucketService, test_project
    ) -> None:
        try:
            kanban = bucket_svc.get_kanban_view(test_project.id)
        except ValueError:
            pytest.skip("No kanban view on test project")
        bucket = bucket_svc.create(test_project.id, _unique("tmpbucket"), kanban.id)
        assert bucket.id > 0
        bucket_svc.delete(test_project.id, kanban.id, bucket.id)
        # Verify it's gone
        remaining = bucket_svc.list(test_project.id, kanban.id)
        ids = [b.id for b in remaining]
        assert bucket.id not in ids


class TestAttachments:
    def test_upload_list_download(
        self,
        attachment_svc: AttachmentService,
        task_svc: TaskService,
        test_project,
        tmp_path,
    ) -> None:
        task = task_svc.create(title=_unique("attach"), project_id=test_project.id)
        test_file = tmp_path / "hello.txt"
        test_file.write_text("integration test content")

        attachment = attachment_svc.add(task.id, str(test_file))
        assert attachment.id > 0

        attachments = attachment_svc.list(task.id)
        ids = [a.id for a in attachments]
        assert attachment.id in ids

        content = attachment_svc.get(task.id, attachment.id)
        assert b"integration test content" in content
