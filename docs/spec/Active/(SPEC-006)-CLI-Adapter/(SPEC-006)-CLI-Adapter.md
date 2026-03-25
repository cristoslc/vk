---
title: "CLI Adapter"
artifact: SPEC-006
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
  - SPEC-002
  - SPEC-004
  - SPEC-005
depends-on-artifacts:
  - SPEC-002
  - SPEC-004
  - SPEC-005
addresses: []
trove: ""
source-issue: ""
swain-do: required
---

# CLI Adapter

## Problem Statement

The primary human interface to vk is a Click-based CLI installed as a console script. It must implement the full command surface from the seed document, wire each command to the appropriate core service, and format output using the formatting layer.

## Desired Outcomes

The operator can manage all Vikunja resources from the terminal with familiar, `asa`-like command patterns. Every command supports `--json` for scripting.

## External Behavior

**Command groups and commands (from seed):**

```
vk auth login [--url URL] [--token TOKEN]
vk auth status

vk project list [--json]
vk project create --title TITLE [--json]
vk project get ID [--json]

vk bucket list PROJECT [--view VIEW] [--json]
vk bucket create PROJECT --title TITLE [--view VIEW] [--json]

vk task list [PROJECT] [--bucket BUCKET] [--done] [--json]
vk task get ID [--json]
vk task create --title TITLE --project PROJECT [--bucket BUCKET] [--due DATE] [--priority N] [--description TEXT] [--json]
vk task update ID [--title TITLE] [--done] [--priority N] [--due DATE] [--description TEXT] [--json]
vk task move ID --bucket BUCKET [--view VIEW] [--json]
vk task delete ID [--force]

vk comment list TASK [--json]
vk comment add TASK --text TEXT [--json]

vk attach list TASK [--json]
vk attach add TASK --file PATH [--json]
vk attach get TASK ATTACHMENT_ID [--output PATH]

vk search QUERY [--project PROJECT] [--done BOOL] [--json]

vk label list [--json]
vk label create --title TITLE [--color HEX] [--json]

vk mcp stdio
vk mcp http [--port 8456]
```

**Entry point:** `vk = "vk.adapters.cli:cli"` in pyproject.toml

## Acceptance Criteria

- Given `vk task create --title "Test" --project "Household Tasks" --bucket "Incoming"`, when run, then a task is created in the correct bucket and output is shown
- Given `vk task list --json`, when run, then valid JSON array of tasks is output
- Given `vk task move ID --bucket "Do Now"`, when run, then the task moves and confirmation is shown
- Given `vk search "electric bill"`, when run, then matching tasks are displayed
- Given `vk auth login --url X --token Y`, when run, then config is saved and status confirmed
- Given any command without valid config, when run, then a helpful error message is shown
- Given `vk mcp stdio`, when run, then it delegates to the MCP stdio adapter
- Given `vk mcp http --port 8456`, when run, then it delegates to the MCP HTTP adapter

## Scope & Constraints

- File: `src/vk/adapters/cli.py`
- Uses Click groups for command hierarchy
- Each command: parse args → call service → format output
- Error handling: catch service exceptions → display user-friendly messages

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-22 | — | Initial creation from seed document |
