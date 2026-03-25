---
title: "MVP Implementation"
artifact: EPIC-001
track: container
status: Active
author: cristos
created: 2026-03-22
last-updated: 2026-03-22
parent-vision: VISION-001
parent-initiative: INITIATIVE-001
priority-weight: high
success-criteria:
  - "vk task create/get/list/update/move/delete work against live Vikunja"
  - "vk mcp stdio launches a working MCP server"
  - "vk mcp http launches an SSE MCP server"
  - "All CLI commands accept --json for machine output"
  - "Test suite passes with mocked HTTP (no live Vikunja required)"
depends-on-artifacts: []
addresses: []
trove: "task-platform-comparison@62bd18a"
---

# MVP Implementation

## Goal / Objective

Deliver a fully functional vk CLI and MCP server that implements the complete command surface from the seed document. From zero to installable tool in one epic.

## Desired Outcomes

The operator can replace Asana CLI workflows with vk. AI agents can connect via MCP and perform all task management operations. The Eisenhower bucket workflow (Incoming → Do Now/Schedule/Delegate/Eliminate → Done) works end-to-end.

## Scope Boundaries

**In scope:** Everything in the seed document's command surface, architecture, and acceptance criteria.

**Out of scope:** Webhooks, CI/CD, multi-user auth, Vikunja admin operations.

## Child Specs

- [SPEC-001](../../spec/Active/(SPEC-001)-HTTP-Client-Layer/(SPEC-001)-HTTP-Client-Layer.md) — HTTP Client Layer
- [SPEC-002](../../spec/Active/(SPEC-002)-Config-And-Auth/(SPEC-002)-Config-And-Auth.md) — Config and Auth
- [SPEC-003](../../spec/Active/(SPEC-003)-Domain-Models/(SPEC-003)-Domain-Models.md) — Domain Models
- [SPEC-004](../../spec/Active/(SPEC-004)-Core-Services/(SPEC-004)-Core-Services.md) — Core Services
- [SPEC-005](../../spec/Active/(SPEC-005)-Output-Formatting/(SPEC-005)-Output-Formatting.md) — Output Formatting
- [SPEC-006](../../spec/Active/(SPEC-006)-CLI-Adapter/(SPEC-006)-CLI-Adapter.md) — CLI Adapter
- [SPEC-007](../../spec/Active/(SPEC-007)-MCP-Adapters/(SPEC-007)-MCP-Adapters.md) — MCP Adapters

## Key Dependencies

- Vikunja v2.2.0+ running locally
- Python 3.11+, Click >= 8.1, requests >= 2.31, mcp >= 1.0

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-22 | — | Initial creation from seed document |
