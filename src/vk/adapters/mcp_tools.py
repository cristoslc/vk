"""Shared MCP tool definitions — one source of truth for both transports."""

from __future__ import annotations

from mcp.server import Server
from mcp.types import TextContent, Tool

from vk.client import VikunjaClient
from vk.config import Config
from vk.services.attachments import AttachmentService
from vk.services.buckets import BucketService
from vk.services.comments import CommentService
from vk.services.labels import LabelService
from vk.services.projects import ProjectService
from vk.services.search import SearchService
from vk.services.tasks import TaskService


def register_tools(server: Server, config: Config) -> None:
    """Register all vk tools on an MCP server instance."""

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name="vk_project_list",
                description="List all Vikunja projects",
                inputSchema={"type": "object", "properties": {}},
            ),
            Tool(
                name="vk_project_get",
                description="Get a project by ID",
                inputSchema={
                    "type": "object",
                    "properties": {"project_id": {"type": "integer"}},
                    "required": ["project_id"],
                },
            ),
            Tool(
                name="vk_project_create",
                description="Create a new project",
                inputSchema={
                    "type": "object",
                    "properties": {"title": {"type": "string"}},
                    "required": ["title"],
                },
            ),
            Tool(
                name="vk_task_list",
                description="List tasks in a project",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "project_id": {"type": "integer"},
                        "bucket_id": {"type": "integer"},
                        "done": {"type": "boolean"},
                    },
                    "required": ["project_id"],
                },
            ),
            Tool(
                name="vk_task_get",
                description="Get a task by ID",
                inputSchema={
                    "type": "object",
                    "properties": {"task_id": {"type": "integer"}},
                    "required": ["task_id"],
                },
            ),
            Tool(
                name="vk_task_create",
                description="Create a new task",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "project_id": {"type": "integer"},
                        "bucket_id": {"type": "integer"},
                        "due_date": {"type": "string"},
                        "priority": {"type": "integer"},
                        "description": {"type": "string"},
                    },
                    "required": ["title", "project_id"],
                },
            ),
            Tool(
                name="vk_task_update",
                description="Update a task",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "integer"},
                        "title": {"type": "string"},
                        "done": {"type": "boolean"},
                        "priority": {"type": "integer"},
                        "due_date": {"type": "string"},
                        "description": {"type": "string"},
                    },
                    "required": ["task_id"],
                },
            ),
            Tool(
                name="vk_task_move",
                description="Move a task to a different bucket",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "integer"},
                        "bucket_id": {"type": "integer"},
                        "project_id": {"type": "integer"},
                        "view_id": {"type": "integer"},
                    },
                    "required": ["task_id", "bucket_id", "project_id", "view_id"],
                },
            ),
            Tool(
                name="vk_task_delete",
                description="Delete a task",
                inputSchema={
                    "type": "object",
                    "properties": {"task_id": {"type": "integer"}},
                    "required": ["task_id"],
                },
            ),
            Tool(
                name="vk_bucket_list",
                description="List buckets in a project view",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "project_id": {"type": "integer"},
                        "view_id": {"type": "integer"},
                    },
                    "required": ["project_id", "view_id"],
                },
            ),
            Tool(
                name="vk_bucket_create",
                description="Create a bucket in a project view",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "project_id": {"type": "integer"},
                        "title": {"type": "string"},
                        "view_id": {"type": "integer"},
                    },
                    "required": ["project_id", "title", "view_id"],
                },
            ),
            Tool(
                name="vk_comment_list",
                description="List comments on a task",
                inputSchema={
                    "type": "object",
                    "properties": {"task_id": {"type": "integer"}},
                    "required": ["task_id"],
                },
            ),
            Tool(
                name="vk_comment_add",
                description="Add a comment to a task",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "integer"},
                        "text": {"type": "string"},
                    },
                    "required": ["task_id", "text"],
                },
            ),
            Tool(
                name="vk_attach_list",
                description="List attachments on a task",
                inputSchema={
                    "type": "object",
                    "properties": {"task_id": {"type": "integer"}},
                    "required": ["task_id"],
                },
            ),
            Tool(
                name="vk_attach_add",
                description="Attach a file to a task",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "integer"},
                        "file_path": {"type": "string"},
                    },
                    "required": ["task_id", "file_path"],
                },
            ),
            Tool(
                name="vk_search",
                description="Search tasks by keyword",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string"},
                        "project_id": {"type": "integer"},
                        "done": {"type": "boolean"},
                    },
                    "required": ["query"],
                },
            ),
            Tool(
                name="vk_label_list",
                description="List all labels",
                inputSchema={"type": "object", "properties": {}},
            ),
            Tool(
                name="vk_label_create",
                description="Create a label",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "color": {"type": "string"},
                    },
                    "required": ["title"],
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        import json

        client = VikunjaClient(config.url, config.token)

        handlers = {
            "vk_project_list": lambda: _project_list(client),
            "vk_project_get": lambda: _project_get(client, arguments),
            "vk_project_create": lambda: _project_create(client, arguments),
            "vk_task_list": lambda: _task_list(client, arguments),
            "vk_task_get": lambda: _task_get(client, arguments),
            "vk_task_create": lambda: _task_create(client, arguments),
            "vk_task_update": lambda: _task_update(client, arguments),
            "vk_task_move": lambda: _task_move(client, arguments),
            "vk_task_delete": lambda: _task_delete(client, arguments),
            "vk_bucket_list": lambda: _bucket_list(client, arguments),
            "vk_bucket_create": lambda: _bucket_create(client, arguments),
            "vk_comment_list": lambda: _comment_list(client, arguments),
            "vk_comment_add": lambda: _comment_add(client, arguments),
            "vk_attach_list": lambda: _attach_list(client, arguments),
            "vk_attach_add": lambda: _attach_add(client, arguments),
            "vk_search": lambda: _search(client, arguments),
            "vk_label_list": lambda: _label_list(client),
            "vk_label_create": lambda: _label_create(client, arguments),
        }

        handler = handlers.get(name)
        if not handler:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]

        try:
            result = handler()
            text = json.dumps(result, indent=2, default=str)
        except Exception as e:
            text = json.dumps({"error": str(e)})
        return [TextContent(type="text", text=text)]


# --- Tool handler functions ---


def _project_list(client: VikunjaClient) -> list[dict]:
    return [p.to_dict() for p in ProjectService(client).list()]


def _project_get(client: VikunjaClient, args: dict) -> dict:
    return ProjectService(client).get(args["project_id"]).to_dict()


def _project_create(client: VikunjaClient, args: dict) -> dict:
    return ProjectService(client).create(args["title"]).to_dict()


def _task_list(client: VikunjaClient, args: dict) -> list[dict]:
    return [
        t.to_dict()
        for t in TaskService(client).list(
            args["project_id"],
            bucket_id=args.get("bucket_id"),
            done=args.get("done"),
        )
    ]


def _task_get(client: VikunjaClient, args: dict) -> dict:
    return TaskService(client).get(args["task_id"]).to_dict()


def _task_create(client: VikunjaClient, args: dict) -> dict:
    return TaskService(client).create(
        title=args["title"],
        project_id=args["project_id"],
        bucket_id=args.get("bucket_id"),
        due_date=args.get("due_date"),
        priority=args.get("priority"),
        description=args.get("description"),
    ).to_dict()


def _task_update(client: VikunjaClient, args: dict) -> dict:
    return TaskService(client).update(
        args["task_id"],
        title=args.get("title"),
        done=args.get("done"),
        priority=args.get("priority"),
        due_date=args.get("due_date"),
        description=args.get("description"),
    ).to_dict()


def _task_move(client: VikunjaClient, args: dict) -> dict:
    return TaskService(client).move(
        args["task_id"],
        args["bucket_id"],
        args["project_id"],
        args["view_id"],
    ).to_dict()


def _task_delete(client: VikunjaClient, args: dict) -> dict:
    TaskService(client).delete(args["task_id"])
    return {"deleted": True, "task_id": args["task_id"]}


def _bucket_list(client: VikunjaClient, args: dict) -> list[dict]:
    return [
        b.to_dict()
        for b in BucketService(client).list(args["project_id"], args["view_id"])
    ]


def _bucket_create(client: VikunjaClient, args: dict) -> dict:
    return BucketService(client).create(
        args["project_id"], args["title"], args["view_id"]
    ).to_dict()


def _comment_list(client: VikunjaClient, args: dict) -> list[dict]:
    return [c.to_dict() for c in CommentService(client).list(args["task_id"])]


def _comment_add(client: VikunjaClient, args: dict) -> dict:
    return CommentService(client).add(args["task_id"], args["text"]).to_dict()


def _attach_list(client: VikunjaClient, args: dict) -> list[dict]:
    return [a.to_dict() for a in AttachmentService(client).list(args["task_id"])]


def _attach_add(client: VikunjaClient, args: dict) -> dict:
    return AttachmentService(client).add(args["task_id"], args["file_path"]).to_dict()


def _search(client: VikunjaClient, args: dict) -> list[dict]:
    return [
        t.to_dict()
        for t in SearchService(client).search(
            args["query"],
            project_id=args.get("project_id"),
            done=args.get("done"),
        )
    ]


def _label_list(client: VikunjaClient) -> list[dict]:
    return [l.to_dict() for l in LabelService(client).list()]


def _label_create(client: VikunjaClient, args: dict) -> dict:
    return LabelService(client).create(
        args["title"], color=args.get("color")
    ).to_dict()
