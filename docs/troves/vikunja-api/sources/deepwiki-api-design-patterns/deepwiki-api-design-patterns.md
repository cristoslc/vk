---
source-id: "deepwiki-api-design-patterns"
title: "Vikunja API Design Patterns — DeepWiki"
type: web
url: "https://deepwiki.com/go-vikunja/vikunja/7.1-api-design-patterns"
fetched: 2026-03-24T20:10:11Z
hash: "af0e7fcccb913d7b8c9ec54994ae6b3d9ad8c9113041e6c32c01c3343bd3ae4c"
---

# API Design Patterns

The Vikunja API follows REST conventions with resource-based URLs under the `/api/v1` base path. All endpoints return JSON (except for file downloads) and follow consistent patterns for CRUD operations, authentication, pagination, and error handling.

## HTTP Method Conventions

Vikunja uses a specific mapping of HTTP methods to CRUD operations that **differs from standard REST**:

| HTTP Method | Operation | Usage |
| --- | --- | --- |
| **GET** | Read (single or collection) | Retrieve resources |
| **PUT** | Create | Create new resources |
| **POST** | Update | Modify existing resources |
| **DELETE** | Delete | Remove resources |

**Note:** `PUT` is used for creation and `POST` for updates — the opposite of standard REST convention.

## Authentication

### Methods

- **JWT-Auth:** Main authorization method. Needs `Authorization: Bearer <jwt-token>` header.
- **API Token:** Long-lived scoped tokens, also via `Authorization: Bearer <token>` header.
- **BasicAuth:** Only used for CalDAV endpoints.

### Permission Headers

Single-item responses include an `x-max-permission` header:

| Value | Permission Level |
| --- | --- |
| `0` | Read Only |
| `1` | Read & Write |
| `2` | Admin |

## Pagination

All list endpoints support pagination:

### Request Parameters

| Parameter | Description | Default |
| --- | --- | --- |
| `page` | Page number (1-indexed) | 1 |
| `per_page` | Items per page | 50 |
| `s` | Search term | - |

### Response Headers

| Header | Description |
| --- | --- |
| `x-pagination-total-pages` | Total number of pages |
| `x-pagination-result-count` | Number of items in response |

## Error Handling

All errors follow a consistent structure with both HTTP status codes and Vikunja-specific error codes:

| HTTP Status | Vikunja Code | Meaning |
| --- | --- | --- |
| 400 | 1001 | Invalid input data |
| 401 | 1000 | No authentication provided |
| 403 | 3001 | Insufficient permissions |
| 404 | 4001 | Resource not found |
| 500 | 1 | Internal server error |

## Rate Limiting

### Authenticated Routes

- `ratelimit.kind`: `"user"` or `"ip"`
- `ratelimit.period`: Time window (default: 60s)
- `ratelimit.limit`: Max requests per period (default: 100)

### Unauthenticated Routes

- Limited by IP address only
- Default: 10 requests per 60s
- Prevents brute force attacks

## Content Types

| Scenario | Content-Type |
| --- | --- |
| Standard API | `application/json` |
| File uploads | `multipart/form-data` |
| File downloads | `application/octet-stream` |
| CalDAV | `text/calendar`, `text/xml` |

## Key Documentation Endpoints

| Endpoint | Purpose |
| --- | --- |
| `/api/v1/docs.json` | OpenAPI JSON schema |
| `/api/v1/docs` | ReDoc UI viewer |
| `/health` | Health check (no auth required) |
| `/api/v1/info` | Server info and enabled features |
