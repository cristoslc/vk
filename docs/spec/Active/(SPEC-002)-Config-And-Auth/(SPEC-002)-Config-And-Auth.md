---
title: "Config and Auth"
artifact: SPEC-002
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
depends-on-artifacts:
  - SPEC-001
addresses: []
trove: ""
source-issue: ""
swain-do: required
---

# Config and Auth

## Problem Statement

vk needs adapter-agnostic configuration resolution for Vikunja base URL and API token. The resolution order (CLI flag → env var → project dotfile → user config) must work identically for CLI, MCP stdio, and MCP HTTP adapters.

## Desired Outcomes

Users configure vk once and it works across all adapters. The `vk auth login` command provides an interactive setup path. Token storage is secure and follows XDG conventions.

## External Behavior

**Token resolution order:**
1. Explicit argument (`--token` flag or parameter)
2. `VK_TOKEN` environment variable
3. `.vk-config.json` in current directory (walk up to git root)
4. `~/.config/vk/config.json`

**URL resolution:** Same order with `VK_URL` env var and `url` config key.

**Config file format:**
```json
{
  "url": "http://localhost:3456",
  "token": "tk_...",
  "default_project": "Household Tasks",
  "kanban_view": "Kanban"
}
```

**`vk auth login`:** Interactive or `--url` + `--token` flags. Writes config file. If no token provided, prompts for username/password, authenticates via JWT, creates a long-lived API token via `PUT /tokens`, stores it.

## Acceptance Criteria

- Given VK_TOKEN is set, when no --token flag is passed, then the env var is used
- Given a .vk-config.json exists in a parent directory, when no env var or flag, then the dotfile token is used
- Given --token is passed, when VK_TOKEN is also set, then the flag wins
- Given `vk auth login --url X --token Y`, when run, then config file is written
- Given `vk auth status`, when a valid config exists, then connection info is displayed
- Given no config anywhere, when any command is run, then a clear error message is shown

## Scope & Constraints

- Files: `src/vk/config.py`
- Config class is a plain Python class, no framework
- Walk-up search stops at git root or filesystem root

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-22 | — | Initial creation from seed document |
