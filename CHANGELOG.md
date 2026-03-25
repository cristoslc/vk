# Changelog

## [0.1.0-alpha.3] - 2026-03-25

### Features

#### Bucket delete

`vk bucket delete <project> <bucket>` removes buckets from kanban views. Supports name or ID resolution, confirmation prompt (skip with `--force`), and `--view` for non-default views. Also available as the `vk_bucket_delete` MCP tool. Closes #2.
- Date-only `--due` values (e.g. `2026-03-25`) are now normalized to full ISO-8601 datetime before sending to the API, fixing HTTP 400 errors. Applies to both task create and update. Closes #1.

## [0.1.0-alpha.2] - 2026-03-24

### Features

#### Integration-tested API client

Running against a live Vikunja v2.2.0 instance revealed and fixed three bugs: search used a non-existent endpoint (`/tasks/all` → `/tasks`), attachment uploads returned a list not parsed correctly, and `view_kind` is a string (`"kanban"`) not an integer. 15 integration tests now cover auth, projects, tasks, labels, comments, search, buckets, and attachments.

### Research
- Vikunja API trove — 5 sources collected including the full OpenAPI v2.2.0 spec (111 endpoints), official docs, filter API reference, and architecture overview

### Supporting Changes
- pytest `integration` marker configured; integration tests skip by default
- `.gitleaksignore` added for false-positive JWT example in OpenAPI spec

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
