---
title: "MCP Adapters"
artifact: SPEC-007
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
  - SPEC-004
depends-on-artifacts:
  - SPEC-004
addresses: []
evidence-pool: ""
source-issue: ""
swain-do: required
---

# MCP Adapters

## Problem Statement

AI agents need to interact with Vikunja through MCP (Model Context Protocol). Two transports are needed: stdio (for direct Claude Code integration) and HTTP/SSE (for network-accessible MCP clients). Both share the same tool definitions, generated from core service method signatures.

## Desired Outcomes

Claude Code and other MCP clients can connect to vk and perform all task management operations. Tool definitions are auto-generated from core services — one source of truth, no duplication.

## External Behavior

**Shared tool definitions (from seed):**

| Tool Name | Description | Parameters |
|-----------|-------------|------------|
| vk_task_list | List tasks in a project | project_id, bucket_id?, done? |
| vk_task_create | Create a task | title, project_id, bucket_id?, due_date?, priority?, description? |
| vk_task_update | Update a task | task_id, title?, done?, priority?, due_date?, description? |
| vk_task_move | Move task to a bucket | task_id, bucket_id, project_id, view_id? |
| vk_task_get | Get a single task | task_id |
| vk_task_delete | Delete a task | task_id |
| vk_comment_list | List comments on a task | task_id |
| vk_comment_add | Add a comment to a task | task_id, text |
| vk_attach_list | List attachments on a task | task_id |
| vk_attach_add | Attach a file to a task | task_id, file_path |
| vk_search | Search tasks | query, project_id?, done? |
| vk_project_list | List all projects | (none) |
| vk_project_create | Create a project | title |
| vk_project_get | Get a project | project_id |
| vk_bucket_list | List buckets | project_id, view_id? |
| vk_bucket_create | Create a bucket | project_id, title, view_id? |
| vk_label_list | List labels | (none) |
| vk_label_create | Create a label | title, color? |

**stdio transport:** `vk mcp stdio` — reads JSON-RPC from stdin, writes to stdout. Standard MCP protocol.

**HTTP/SSE transport:** `vk mcp http --port 8456` — serves MCP over HTTP with Server-Sent Events for streaming.

## Acceptance Criteria

- Given `vk mcp stdio`, when launched, then it responds to MCP tool discovery requests with all tool definitions
- Given an MCP tool call for vk_task_list, when received via stdio, then tasks are returned as structured MCP results
- Given `vk mcp http --port 8456`, when launched, then it accepts HTTP connections and serves MCP via SSE
- Given any MCP tool call, when the underlying service raises an error, then a proper MCP error response is returned
- Given the tool definitions, when compared to core service signatures, then they match 1:1

## Scope & Constraints

- Files: `src/vk/adapters/mcp_tools.py` (shared definitions), `mcp_stdio.py`, `mcp_http.py`
- Uses the `mcp` Python SDK
- Tool schemas generated from service method signatures + docstrings
- Both adapters share the same tool registration code

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-22 | — | Initial creation from seed document |
