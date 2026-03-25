---
title: "HTTP Client Layer"
artifact: SPEC-001
track: implementable
status: Active
author: cristos
created: 2026-03-22
last-updated: 2026-03-22
priority-weight: ""
type: feature
parent-epic: EPIC-001
parent-initiative: ""
linked-artifacts: []
depends-on-artifacts: []
addresses: []
trove: "task-platform-comparison@62bd18a"
source-issue: ""
swain-do: required
---

# HTTP Client Layer

## Problem Statement

vk needs a thin, stateless HTTP adapter to the Vikunja REST API that handles authentication headers, pagination, multipart file uploads, and error mapping. This is the lowest layer of the hexagonal architecture — all core services depend on it.

## Desired Outcomes

Core services can call any Vikunja API endpoint through a typed Python client without dealing with HTTP details, auth headers, or pagination logic.

## External Behavior

**Inputs:** Base URL, auth token (API token or JWT), HTTP method, endpoint path, optional body/params/files.

**Outputs:** Parsed JSON response or domain-appropriate error.

**Preconditions:** Valid base URL and token must be available (from Config layer).

**Postconditions:** Responses are parsed; HTTP errors are mapped to domain exceptions.

**Constraints:**
- Stateless except for base URL and token
- Mirrors Vikunja Swagger spec closely
- Handles pagination transparently (fetch all pages by default)
- Supports multipart file upload for attachments

## Acceptance Criteria

- Given a valid token, when any API endpoint is called, then the Authorization header is set correctly
- Given a paginated endpoint, when default params are used, then all pages are fetched and concatenated
- Given a paginated endpoint with explicit limit/page, when called, then only the requested page is returned
- Given an HTTP error (4xx/5xx), when the client receives it, then a typed exception is raised with status code and message
- Given a file path, when uploading an attachment, then a multipart POST is sent correctly
- Given an expired/invalid token, when a 401 is received, then an AuthenticationError is raised

## Scope & Constraints

- One class: `VikunjaClient`
- No business logic — that lives in services
- File: `src/vk/client.py`
- Custom exceptions in `src/vk/exceptions.py`

## Lifecycle

| Phase | Date | Commit | Notes |
|-------|------|--------|-------|
| Active | 2026-03-22 | — | Initial creation from seed document |
