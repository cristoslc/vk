"""Click CLI adapter — entry point: vk."""

from __future__ import annotations

import sys

import click

from vk.cache import NameCache
from vk.client import VikunjaClient
from vk.config import Config
from vk.exceptions import ConfigError, VkError
from vk.formatting import (
    format_attachment_list,
    format_bucket,
    format_bucket_list,
    format_comment,
    format_comment_list,
    format_label,
    format_label_list,
    format_project,
    format_project_list,
    format_task,
    format_task_list,
)
from vk.services.attachments import AttachmentService
from vk.services.auth import AuthService
from vk.services.buckets import BucketService
from vk.services.comments import CommentService
from vk.services.labels import LabelService
from vk.services.projects import ProjectService
from vk.services.search import SearchService
from vk.services.tasks import TaskService


pass_config = click.make_pass_decorator(Config, ensure=True)


def _make_client(config: Config) -> VikunjaClient:
    return VikunjaClient(config.url, config.token)


def _resolve_project(
    name_or_id: str, client: VikunjaClient, cache: NameCache
) -> int:
    """Resolve project name or ID to int."""
    try:
        return int(name_or_id)
    except ValueError:
        pass
    # Try cache first, then refresh
    try:
        return cache.resolve_project(name_or_id)
    except KeyError:
        # Refresh cache
        svc = ProjectService(client)
        projects = svc.list()
        cache.set_projects([p.to_dict() for p in projects])
        return cache.resolve_project(name_or_id)


def _resolve_bucket(
    name_or_id: str,
    project_id: int,
    view_id: int,
    client: VikunjaClient,
    cache: NameCache,
) -> int:
    """Resolve bucket name or ID to int."""
    try:
        return int(name_or_id)
    except ValueError:
        pass
    try:
        return cache.resolve_bucket(name_or_id, view_id)
    except KeyError:
        svc = BucketService(client)
        buckets = svc.list(project_id, view_id)
        cache.set_buckets(view_id, [b.to_dict() for b in buckets])
        return cache.resolve_bucket(name_or_id, view_id)


def _get_view_id(
    project_id: int, client: VikunjaClient, config: Config, view: str | None = None
) -> int:
    svc = BucketService(client)
    v = svc.get_kanban_view(project_id, view or config.kanban_view)
    return v.id



# --- Main CLI group ---


@click.group()
@click.option("--url", envvar="VK_URL", default=None, help="Vikunja instance URL")
@click.option("--token", envvar="VK_TOKEN", default=None, help="API token")
@click.pass_context
def cli(ctx: click.Context, url: str | None, token: str | None) -> None:
    """vk — Vikunja CLI and MCP server."""
    ctx.ensure_object(dict)
    ctx.obj = Config(url=url, token=token)


# --- Auth ---


@cli.group()
def auth() -> None:
    """Authentication commands."""


@auth.command("login")
@click.option("--url", prompt="Vikunja URL", help="Vikunja instance URL")
@click.option("--token", default=None, help="API token (skip interactive login)")
@pass_config
def auth_login(config: Config, url: str, token: str | None) -> None:
    """Log in to a Vikunja instance."""
    if token:
        path = Config.write_config(url, token)
        click.echo(f"Config saved to {path}")
    else:
        username = click.prompt("Username")
        password = click.prompt("Password", hide_input=True)
        jwt = AuthService.login_with_credentials(url, username, password)
        # Create a long-lived API token
        client = VikunjaClient(url, jwt)
        svc = AuthService(client)
        api_token = svc.create_api_token("vk-cli")
        path = Config.write_config(url, api_token.token)
        click.echo(f"Logged in. Config saved to {path}")


@auth.command("status")
@pass_config
def auth_status_cmd(config: Config) -> None:
    """Check authentication status."""
    result = AuthService.status(config)
    if result["connected"]:
        click.echo(f"Connected to {result['url']} as {result['user']}")
    else:
        click.echo(f"Not connected: {result['error']}", err=True)
        sys.exit(1)


# --- Projects ---


@cli.group()
def project() -> None:
    """Project commands."""


@project.command("list")
@click.option("--json", "as_json", is_flag=True, help="JSON output")
@pass_config
def project_list(config: Config, as_json: bool) -> None:
    """List all projects."""
    client = _make_client(config)
    svc = ProjectService(client)
    projects = svc.list()
    # Update cache
    cache = NameCache()
    cache.set_projects([p.to_dict() for p in projects])
    click.echo(format_project_list(projects, as_json))


@project.command("create")
@click.option("--title", required=True, help="Project title")
@click.option("--json", "as_json", is_flag=True, help="JSON output")
@pass_config
def project_create(config: Config, title: str, as_json: bool) -> None:
    """Create a project."""
    client = _make_client(config)
    svc = ProjectService(client)
    p = svc.create(title)
    click.echo(format_project(p, as_json))


@project.command("get")
@click.argument("project_id", type=int)
@click.option("--json", "as_json", is_flag=True, help="JSON output")
@pass_config
def project_get(config: Config, project_id: int, as_json: bool) -> None:
    """Get a project by ID."""
    client = _make_client(config)
    svc = ProjectService(client)
    p = svc.get(project_id)
    click.echo(format_project(p, as_json))


# --- Buckets ---


@cli.group()
def bucket() -> None:
    """Bucket commands."""


@bucket.command("list")
@click.argument("project_name")
@click.option("--view", default=None, help="View name")
@click.option("--json", "as_json", is_flag=True, help="JSON output")
@pass_config
def bucket_list(
    config: Config, project_name: str, view: str | None, as_json: bool
) -> None:
    """List buckets in a project."""
    client = _make_client(config)
    cache = NameCache()
    project_id = _resolve_project(project_name, client, cache)
    view_id = _get_view_id(project_id, client, config, view)
    svc = BucketService(client)
    buckets = svc.list(project_id, view_id)
    cache.set_buckets(view_id, [b.to_dict() for b in buckets])
    click.echo(format_bucket_list(buckets, as_json))


@bucket.command("create")
@click.argument("project_name")
@click.option("--title", required=True, help="Bucket title")
@click.option("--view", default=None, help="View name")
@click.option("--json", "as_json", is_flag=True, help="JSON output")
@pass_config
def bucket_create(
    config: Config,
    project_name: str,
    title: str,
    view: str | None,
    as_json: bool,
) -> None:
    """Create a bucket."""
    client = _make_client(config)
    cache = NameCache()
    project_id = _resolve_project(project_name, client, cache)
    view_id = _get_view_id(project_id, client, config, view)
    svc = BucketService(client)
    b = svc.create(project_id, title, view_id)
    click.echo(format_bucket(b, as_json))


@bucket.command("delete")
@click.argument("project_name")
@click.argument("bucket_name")
@click.option("--view", default=None, help="View name")
@click.option("--force", is_flag=True, help="Skip confirmation")
@pass_config
def bucket_delete(
    config: Config,
    project_name: str,
    bucket_name: str,
    view: str | None,
    force: bool,
) -> None:
    """Delete a bucket."""
    client = _make_client(config)
    cache = NameCache()
    project_id = _resolve_project(project_name, client, cache)
    view_id = _get_view_id(project_id, client, config, view)
    bucket_id = _resolve_bucket(bucket_name, project_id, view_id, client, cache)
    if not force:
        click.confirm(f"Delete bucket '{bucket_name}'?", abort=True)
    svc = BucketService(client)
    svc.delete(project_id, view_id, bucket_id)
    click.echo(f"Bucket '{bucket_name}' deleted.")


# --- Tasks ---


@cli.group()
def task() -> None:
    """Task commands."""


@task.command("list")
@click.argument("project_name", required=False, default=None)
@click.option("--bucket", "bucket_name", default=None, help="Filter by bucket")
@click.option("--done", is_flag=True, default=None, help="Show done tasks")
@click.option("--json", "as_json", is_flag=True, help="JSON output")
@pass_config
def task_list(
    config: Config,
    project_name: str | None,
    bucket_name: str | None,
    done: bool | None,
    as_json: bool,
) -> None:
    """List tasks."""
    client = _make_client(config)
    cache = NameCache()

    if project_name is None:
        project_name = config.default_project
    if project_name is None:
        click.echo("Specify a project or set default_project in config.", err=True)
        sys.exit(1)

    project_id = _resolve_project(project_name, client, cache)
    bucket_id = None
    if bucket_name:
        view_id = _get_view_id(project_id, client, config)
        bucket_id = _resolve_bucket(bucket_name, project_id, view_id, client, cache)

    svc = TaskService(client)
    tasks = svc.list(project_id, bucket_id=bucket_id, done=done)
    click.echo(format_task_list(tasks, as_json))


@task.command("get")
@click.argument("task_id", type=int)
@click.option("--json", "as_json", is_flag=True, help="JSON output")
@pass_config
def task_get(config: Config, task_id: int, as_json: bool) -> None:
    """Get a task by ID."""
    client = _make_client(config)
    svc = TaskService(client)
    t = svc.get(task_id)
    click.echo(format_task(t, as_json))


@task.command("create")
@click.option("--title", required=True, help="Task title")
@click.option("--project", "project_name", required=True, help="Project name or ID")
@click.option("--bucket", "bucket_name", default=None, help="Bucket name or ID")
@click.option("--due", default=None, help="Due date (ISO format)")
@click.option("--priority", type=int, default=None, help="Priority (0-5)")
@click.option("--description", default=None, help="Task description")
@click.option("--json", "as_json", is_flag=True, help="JSON output")
@pass_config
def task_create(
    config: Config,
    title: str,
    project_name: str,
    bucket_name: str | None,
    due: str | None,
    priority: int | None,
    description: str | None,
    as_json: bool,
) -> None:
    """Create a task."""
    client = _make_client(config)
    cache = NameCache()
    project_id = _resolve_project(project_name, client, cache)

    bucket_id = None
    if bucket_name:
        view_id = _get_view_id(project_id, client, config)
        bucket_id = _resolve_bucket(bucket_name, project_id, view_id, client, cache)

    svc = TaskService(client)
    t = svc.create(
        title=title,
        project_id=project_id,
        bucket_id=bucket_id,
        due_date=due,
        priority=priority,
        description=description,
    )

    # If bucket was specified, move the task into it
    if bucket_id is not None:
        view_id = _get_view_id(project_id, client, config)
        t = svc.move(t.id, bucket_id, project_id, view_id)

    click.echo(format_task(t, as_json))


@task.command("update")
@click.argument("task_id", type=int)
@click.option("--title", default=None, help="New title")
@click.option("--done", is_flag=True, default=None, help="Mark as done")
@click.option("--priority", type=int, default=None, help="Priority")
@click.option("--due", default=None, help="Due date")
@click.option("--description", default=None, help="Description")
@click.option("--json", "as_json", is_flag=True, help="JSON output")
@pass_config
def task_update(
    config: Config,
    task_id: int,
    title: str | None,
    done: bool | None,
    priority: int | None,
    due: str | None,
    description: str | None,
    as_json: bool,
) -> None:
    """Update a task."""
    client = _make_client(config)
    svc = TaskService(client)
    t = svc.update(
        task_id,
        title=title,
        done=done,
        priority=priority,
        due_date=due,
        description=description,
    )
    click.echo(format_task(t, as_json))


@task.command("move")
@click.argument("task_id", type=int)
@click.option("--bucket", "bucket_name", required=True, help="Target bucket")
@click.option("--view", default=None, help="View name")
@click.option("--json", "as_json", is_flag=True, help="JSON output")
@pass_config
def task_move(
    config: Config,
    task_id: int,
    bucket_name: str,
    view: str | None,
    as_json: bool,
) -> None:
    """Move a task to a bucket."""
    client = _make_client(config)
    cache = NameCache()
    # Get task to know the project
    svc = TaskService(client)
    t = svc.get(task_id)
    project_id = t.project_id
    view_id = _get_view_id(project_id, client, config, view)
    bucket_id = _resolve_bucket(bucket_name, project_id, view_id, client, cache)
    t = svc.move(task_id, bucket_id, project_id, view_id)
    click.echo(format_task(t, as_json))


@task.command("delete")
@click.argument("task_id", type=int)
@click.option("--force", is_flag=True, help="Skip confirmation")
@pass_config
def task_delete(config: Config, task_id: int, force: bool) -> None:
    """Delete a task."""
    if not force:
        click.confirm(f"Delete task #{task_id}?", abort=True)
    client = _make_client(config)
    svc = TaskService(client)
    svc.delete(task_id)
    click.echo(f"Task #{task_id} deleted.")


# --- Comments ---


@cli.group()
def comment() -> None:
    """Comment commands."""


@comment.command("list")
@click.argument("task_id", type=int)
@click.option("--json", "as_json", is_flag=True, help="JSON output")
@pass_config
def comment_list(config: Config, task_id: int, as_json: bool) -> None:
    """List comments on a task."""
    client = _make_client(config)
    svc = CommentService(client)
    comments = svc.list(task_id)
    click.echo(format_comment_list(comments, as_json))


@comment.command("add")
@click.argument("task_id", type=int)
@click.option("--text", required=True, help="Comment text")
@click.option("--json", "as_json", is_flag=True, help="JSON output")
@pass_config
def comment_add(config: Config, task_id: int, text: str, as_json: bool) -> None:
    """Add a comment to a task."""
    client = _make_client(config)
    svc = CommentService(client)
    c = svc.add(task_id, text)
    click.echo(format_comment(c, as_json))


# --- Attachments ---


@cli.group()
def attach() -> None:
    """Attachment commands."""


@attach.command("list")
@click.argument("task_id", type=int)
@click.option("--json", "as_json", is_flag=True, help="JSON output")
@pass_config
def attach_list(config: Config, task_id: int, as_json: bool) -> None:
    """List attachments on a task."""
    client = _make_client(config)
    svc = AttachmentService(client)
    attachments = svc.list(task_id)
    click.echo(format_attachment_list(attachments, as_json))


@attach.command("add")
@click.argument("task_id", type=int)
@click.option("--file", "file_path", required=True, type=click.Path(exists=True))
@click.option("--json", "as_json", is_flag=True, help="JSON output")
@pass_config
def attach_add(config: Config, task_id: int, file_path: str, as_json: bool) -> None:
    """Attach a file to a task."""
    client = _make_client(config)
    svc = AttachmentService(client)
    a = svc.add(task_id, file_path)
    click.echo(f"Attachment #{a.id} added." if not as_json else _json_out_single(a))


@attach.command("get")
@click.argument("task_id", type=int)
@click.argument("attachment_id", type=int)
@click.option("--output", default=None, help="Output file path")
@pass_config
def attach_get(
    config: Config, task_id: int, attachment_id: int, output: str | None
) -> None:
    """Download an attachment."""
    client = _make_client(config)
    svc = AttachmentService(client)
    content = svc.get(task_id, attachment_id, output_path=output)
    if output:
        click.echo(f"Saved to {output}")
    else:
        sys.stdout.buffer.write(content)


def _json_out_single(obj: object) -> str:
    import json
    return json.dumps(obj.to_dict(), indent=2)  # type: ignore[attr-defined]


# --- Search ---


@cli.command("search")
@click.argument("query")
@click.option("--project", "project_name", default=None, help="Filter by project")
@click.option("--done", is_flag=True, default=None, help="Include done tasks")
@click.option("--json", "as_json", is_flag=True, help="JSON output")
@pass_config
def search(
    config: Config,
    query: str,
    project_name: str | None,
    done: bool | None,
    as_json: bool,
) -> None:
    """Search tasks."""
    client = _make_client(config)
    project_id = None
    if project_name:
        cache = NameCache()
        project_id = _resolve_project(project_name, client, cache)
    svc = SearchService(client)
    tasks = svc.search(query, project_id=project_id, done=done)
    click.echo(format_task_list(tasks, as_json))


# --- Labels ---


@cli.group()
def label() -> None:
    """Label commands."""


@label.command("list")
@click.option("--json", "as_json", is_flag=True, help="JSON output")
@pass_config
def label_list(config: Config, as_json: bool) -> None:
    """List labels."""
    client = _make_client(config)
    svc = LabelService(client)
    labels = svc.list()
    click.echo(format_label_list(labels, as_json))


@label.command("create")
@click.option("--title", required=True, help="Label title")
@click.option("--color", default=None, help="Hex color (e.g., ff0000)")
@click.option("--json", "as_json", is_flag=True, help="JSON output")
@pass_config
def label_create(
    config: Config, title: str, color: str | None, as_json: bool
) -> None:
    """Create a label."""
    client = _make_client(config)
    svc = LabelService(client)
    l = svc.create(title, color=color)
    click.echo(format_label(l, as_json))


# --- MCP ---


@cli.group()
def mcp() -> None:
    """MCP server commands."""


@mcp.command("stdio")
@pass_config
def mcp_stdio(config: Config) -> None:
    """Launch MCP server (stdio transport)."""
    from vk.adapters.mcp_stdio import run_stdio

    run_stdio(config)


@mcp.command("http")
@click.option("--port", default=8456, type=int, help="Port to listen on")
@pass_config
def mcp_http(config: Config, port: int) -> None:
    """Launch MCP server (HTTP/SSE transport)."""
    from vk.adapters.mcp_http import run_http

    run_http(config, port)
