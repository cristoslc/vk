# Changelog

## [0.1.0-alpha.1] - 2026-03-22

### Features

#### Vikunja CLI

Full CLI for managing a self-hosted Vikunja instance from the terminal. Commands cover tasks, projects, kanban buckets, comments, attachments, labels, and search. All commands accept --json for machine-parseable output. Name resolution maps human-readable project and bucket names to IDs via a local cache.

#### MCP Server (dual transport)

18 MCP tools exposing the same capabilities as the CLI — connect AI agents to Vikunja via stdio (for Claude Code integration) or HTTP/SSE (for network-accessible clients). Tool definitions are auto-generated from core service signatures.

#### Hexagonal Architecture

Vikunja HTTP client, 8 typed core services, and 3 interchangeable adapters (CLI, MCP stdio, MCP HTTP/SSE) sharing domain dataclasses. Adapter-agnostic config resolves URL and token from flags, env vars, and dotfiles.
- Transparent pagination — the HTTP client fetches all pages by default
- 47 tests covering client, models, config, services, and CLI adapter

### Supporting Changes
- Pre-commit security hooks (gitleaks) configured during project setup
