"""Output formatting for CLI — compact and JSON modes."""

from __future__ import annotations

import json
from typing import Any

from vk.models import Attachment, Bucket, Comment, Label, Project, Task


def _json_out(obj: Any) -> str:
    if isinstance(obj, list):
        return json.dumps([item.to_dict() for item in obj], indent=2)
    return json.dumps(obj.to_dict(), indent=2)


def format_task(task: Task, as_json: bool = False) -> str:
    if as_json:
        return _json_out(task)
    done_mark = "x" if task.done else " "
    priority = f" P{task.priority}" if task.priority else ""
    due = f" due:{task.due_date.strftime('%Y-%m-%d')}" if task.due_date else ""
    return f"[{done_mark}] #{task.id}{priority}{due}  {task.title}"


def format_task_list(tasks: list[Task], as_json: bool = False) -> str:
    if as_json:
        return _json_out(tasks)
    if not tasks:
        return "No tasks found."
    return "\n".join(format_task(t) for t in tasks)


def format_project(project: Project, as_json: bool = False) -> str:
    if as_json:
        return _json_out(project)
    return f"#{project.id}  {project.title}"


def format_project_list(projects: list[Project], as_json: bool = False) -> str:
    if as_json:
        return _json_out(projects)
    if not projects:
        return "No projects found."
    return "\n".join(format_project(p) for p in projects)


def format_bucket(bucket: Bucket, as_json: bool = False) -> str:
    if as_json:
        return _json_out(bucket)
    return f"#{bucket.id}  {bucket.title}"


def format_bucket_list(buckets: list[Bucket], as_json: bool = False) -> str:
    if as_json:
        return _json_out(buckets)
    if not buckets:
        return "No buckets found."
    return "\n".join(format_bucket(b) for b in buckets)


def format_comment(comment: Comment, as_json: bool = False) -> str:
    if as_json:
        return _json_out(comment)
    author = f"@{comment.author}" if comment.author else "unknown"
    return f"{author}: {comment.comment}"


def format_comment_list(comments: list[Comment], as_json: bool = False) -> str:
    if as_json:
        return _json_out(comments)
    if not comments:
        return "No comments found."
    return "\n".join(format_comment(c) for c in comments)


def format_attachment(attachment: Attachment, as_json: bool = False) -> str:
    if as_json:
        return _json_out(attachment)
    name = attachment.file.get("name", f"attachment-{attachment.id}")
    return f"#{attachment.id}  {name}"


def format_attachment_list(
    attachments: list[Attachment], as_json: bool = False
) -> str:
    if as_json:
        return _json_out(attachments)
    if not attachments:
        return "No attachments found."
    return "\n".join(format_attachment(a) for a in attachments)


def format_label(label: Label, as_json: bool = False) -> str:
    if as_json:
        return _json_out(label)
    color = f" ({label.hex_color})" if label.hex_color else ""
    return f"#{label.id}  {label.title}{color}"


def format_label_list(labels: list[Label], as_json: bool = False) -> str:
    if as_json:
        return _json_out(labels)
    if not labels:
        return "No labels found."
    return "\n".join(format_label(l) for l in labels)
