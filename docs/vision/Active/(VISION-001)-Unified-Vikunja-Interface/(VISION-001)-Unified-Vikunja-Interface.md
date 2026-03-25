---
title: "Unified Vikunja Interface"
artifact: VISION-001
track: standing
status: Active
product-type: personal
author: cristos
created: 2026-03-22
last-updated: 2026-03-22
priority-weight: high
depends-on-artifacts: []
trove: "task-platform-comparison@62bd18a"
---

# Unified Vikunja Interface

## Target Audience

Solo operators and AI agents managing household and personal tasks through a self-hosted Vikunja instance. Primary user is a technical household manager who coordinates task workflows via CLI and AI agent integrations (Claude Code, MCP clients).

## Problem Statement

Asana's free-tier API rate limit (150 req/min) is a hard blocker for agent-driven household task management. A self-hosted Vikunja instance has no rate limits, full data sovereignty, and a clean REST API — but Vikunja has no official CLI and no MCP server exists. There is no way to drive Vikunja from a terminal or connect it to AI agents.

## Existing Landscape

- **cristoslc/asa** — CLI for Asana. Validated the command surface and output patterns but is locked to a rate-limited platform.
- **Vikunja web UI** — Full-featured but not automatable. No CLI, no MCP.
- **Vikunja REST API** — Well-documented (Swagger), supports JWT and API token auth, no rate limits. The building block exists; the interface layer does not.

## Build vs. Buy

Tier 3 (build from scratch): No existing Vikunja CLI or MCP server exists. The REST API is the raw material. The `asa` CLI proves the pattern works — `vk` generalizes it with a hexagonal architecture so the same core serves CLI, MCP stdio, and MCP HTTP/SSE without duplication.

## Maintenance Budget

Low — single operator, personal use. Architecture must minimize surface area: one core library, three thin adapters. Dependencies kept minimal (Click, requests, mcp SDK). No ORM, no database, no server-side state.

## Value Proposition

A single Python library that gives both humans (via CLI) and AI agents (via MCP) full access to a self-hosted Vikunja instance — with no rate limits, full data sovereignty, and a familiar command surface inherited from the proven `asa` CLI.

## Success Metrics

1. All 10 acceptance criteria from the seed document pass
2. CLI is installable via `uv` and usable from any terminal
3. MCP server connects successfully to Claude Code
4. Zero Asana API dependency — full migration off Asana is possible
5. Single operator can maintain the codebase with minimal ongoing effort

## Non-Goals

- Multi-user authentication or user management
- Vikunja server administration (backups, upgrades, config)
- Mobile or web UI
- Real-time sync or webhook-driven automation (future consideration)
- Supporting task platforms other than Vikunja

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-22 | — | Initial creation from seed document |
