---
title: "Domain Models"
artifact: SPEC-003
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
depends-on-artifacts: []
addresses: []
evidence-pool: "task-platform-comparison@62bd18a"
source-issue: ""
swain-do: required
---

# Domain Models

## Problem Statement

Core services need typed domain objects (Python dataclasses) instead of raw JSON dicts. This prevents Vikunja API structure from leaking into adapter code and provides type safety across the codebase.

## Desired Outcomes

All layers of the application work with well-typed domain objects. Serialization to/from Vikunja JSON happens at the client boundary. Adapters serialize to CLI output or MCP responses from domain objects.

## External Behavior

**Domain types needed (based on seed API surface):**
- `Task` — id, title, description, done, priority, due_date, project_id, bucket_id, created, updated
- `Project` — id, title, description, created, updated
- `Bucket` — id, title, project_id, view_id, position, created, updated
- `Comment` — id, task_id, comment (text), author, created, updated
- `Attachment` — id, task_id, file, created
- `Label` — id, title, hex_color, created, updated
- `User` — id, username, email, name
- `ApiToken` — id, title, token, permissions, expires_at

Each model has a `from_api(data: dict)` classmethod and a `to_dict()` method.

## Acceptance Criteria

- Given a Vikunja API JSON response for a task, when `Task.from_api(data)` is called, then all fields are correctly mapped
- Given a domain object, when `to_dict()` is called, then the output matches Vikunja API format
- Given an API response with missing optional fields, when parsed, then defaults are used (not exceptions)
- Given each model type, when instantiated, then type hints are enforced by dataclass

## Scope & Constraints

- File: `src/vk/models.py`
- Pure dataclasses — no ORM, no validation library
- Fields match Vikunja API naming where possible; Python snake_case

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-22 | — | Initial creation from seed document |
