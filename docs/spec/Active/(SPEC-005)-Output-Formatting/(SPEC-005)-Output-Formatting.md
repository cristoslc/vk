---
title: "Output Formatting"
artifact: SPEC-005
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
  - SPEC-003
depends-on-artifacts:
  - SPEC-003
addresses: []
trove: ""
source-issue: ""
swain-do: required
---

# Output Formatting

## Problem Statement

The CLI needs two output modes: compact human-readable output (default) and JSON output (`--json` flag). The formatting layer must work with domain objects and be reusable across all CLI commands.

## Desired Outcomes

CLI output is clean and scannable for humans by default, and machine-parseable with `--json`. MCP adapters use JSON serialization from the same domain objects.

## External Behavior

**Compact mode (default):** Concise, aligned text output. Task lists show ID, title, priority, due date, done status. Project lists show ID and title. Comments show author and text.

**JSON mode (`--json`):** Pretty-printed JSON from domain object `to_dict()`. Lists wrapped in an array.

**Formatting functions:** One formatter per domain type (format_task, format_project, format_bucket, etc.) plus list variants.

## Acceptance Criteria

- Given a Task object, when formatted in compact mode, then ID/title/priority/due/done are shown on one line
- Given a list of Tasks, when formatted in compact mode, then output is aligned and scannable
- Given any domain object, when --json is active, then valid JSON is output
- Given an empty list, when formatted, then appropriate "no results" message (compact) or empty array (JSON)

## Scope & Constraints

- File: `src/vk/formatting.py`
- No external formatting libraries — plain string formatting
- Must handle None/missing fields gracefully

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-22 | — | Initial creation from seed document |
