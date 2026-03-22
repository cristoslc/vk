---
title: "Core Services"
artifact: SPEC-004
track: implementable
status: Active
author: cristos
created: 2026-03-22
last-updated: 2026-03-22
priority-weight: ""
type: feature
parent-epic: EPIC-001
parent-initiative: ""
linked-artifacts:
  - SPEC-001
  - SPEC-003
depends-on-artifacts:
  - SPEC-001
  - SPEC-003
addresses: []
evidence-pool: ""
source-issue: ""
swain-do: required
---

# Core Services

## Problem Statement

The core service layer is the port in the hexagonal architecture — it owns all domain logic and mediates between adapters and the Vikunja HTTP client. Eight services are needed: tasks, projects, buckets, comments, attachments, search, labels, and auth. Each service accepts and returns domain objects, not raw JSON.

## Desired Outcomes

Adapters (CLI, MCP) can call any service method with typed arguments and receive typed results. Business logic (e.g., "mark done" = set done:true + move to Done bucket) lives here, not in adapters.

## External Behavior

**Services and key methods:**

| Service | Methods |
|---------|---------|
| TaskService | list(project_id, bucket_id?, done?), get(id), create(title, project_id, bucket_id?, due?, priority?, desc?), update(id, ...), move(id, bucket_id, view_id?), delete(id) |
| ProjectService | list(), get(id), create(title) |
| BucketService | list(project_id, view_id?), create(project_id, title, view_id?) |
| CommentService | list(task_id), add(task_id, text) |
| AttachmentService | list(task_id), add(task_id, file_path), get(task_id, attachment_id, output_path?) |
| SearchService | search(query, project_id?, done?) |
| LabelService | list(), create(title, color?) |
| AuthService | login(url, token?, username?, password?), status(), create_api_token(title, permissions) |

**Name resolution:** Services that accept project/bucket names resolve them to IDs via a local cache (`.vk-cache.json`). Ambiguous matches produce an error listing candidates. View resolution defaults to the first `view_kind: kanban` view.

## Acceptance Criteria

- Given a project name, when TaskService.list("Household Tasks") is called, then it resolves to the project ID and returns typed Task objects
- Given task creation params, when TaskService.create() is called, then a Task is returned with the Vikunja-assigned ID
- Given a task ID and bucket name, when TaskService.move() is called, then the task appears in the target bucket
- Given a search query, when SearchService.search() is called, then matching Task objects are returned
- Given a file path, when AttachmentService.add() is called, then the file is uploaded via multipart POST
- Given a bucket name in a project, when BucketService.list() is called with view resolution, then buckets for the kanban view are returned
- Given an ambiguous name match, when name resolution runs, then an error is raised listing candidates

## Scope & Constraints

- Files: `src/vk/services/tasks.py`, `projects.py`, `buckets.py`, `comments.py`, `attachments.py`, `search.py`, `labels.py`, `auth.py`, `__init__.py`
- Name resolution cache: `src/vk/cache.py`
- Services are stateless — they receive a VikunjaClient instance
- No adapter-specific logic in services

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-22 | — | Initial creation from seed document |
