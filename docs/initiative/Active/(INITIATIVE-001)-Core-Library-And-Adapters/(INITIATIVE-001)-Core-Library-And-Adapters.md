---
title: "Core Library and Adapters"
artifact: INITIATIVE-001
track: container
status: Active
author: cristos
created: 2026-03-22
last-updated: 2026-03-22
parent-vision:
  - VISION-001
priority-weight: high
success-criteria:
  - "All core services (task, project, bucket, comment, attachment, search, label, auth) implemented and tested"
  - "CLI adapter functional with all commands from the seed command surface"
  - "MCP stdio adapter serves all core service methods as MCP tools"
  - "MCP HTTP/SSE adapter serves the same tools over HTTP"
  - "Test suite covers core services with mocked HTTP"
depends-on-artifacts: []
addresses: []
evidence-pool: "task-platform-comparison@62bd18a"
---

# Core Library and Adapters

## Strategic Focus

Build the complete vk library from the ground up: a hexagonal architecture with a Vikunja HTTP client at the bottom, domain-typed core services in the middle, and three interchangeable adapters (CLI, MCP stdio, MCP HTTP/SSE) at the top. This is the entire buildout of vk as described in the seed document — from zero to a working, installable tool.

## Desired Outcomes

The operator can manage Vikunja tasks from the terminal (`vk task create`, `vk task move`, etc.) and AI agents can do the same through MCP. The Eisenhower workflow (bucket-based prioritization) works end-to-end. The system is testable without a live Vikunja instance.

## Scope Boundaries

**In scope:**
- Vikunja HTTP client with auth, pagination, error mapping
- Config/token resolution (env vars, dotfiles, CLI flags)
- Domain models (dataclasses)
- All 8 core services
- Click CLI adapter with all commands
- MCP tool definition generation from core service signatures
- MCP stdio and HTTP/SSE adapters
- Output formatting (compact + JSON)
- Test infrastructure with mocked HTTP

**Out of scope:**
- Webhook/event-driven automation
- Vikunja server management
- Multi-user auth flows
- CI/CD pipeline setup

## Child Epics

- [EPIC-001](../../epic/Active/(EPIC-001)-MVP-Implementation/(EPIC-001)-MVP-Implementation.md) — MVP Implementation

## Small Work (Epic-less Specs)

None yet.

## Key Dependencies

- Vikunja v2.2.0+ REST API (self-hosted, already running)
- Python 3.11+
- mcp Python SDK >= 1.0

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-22 | — | Initial creation from seed document |
