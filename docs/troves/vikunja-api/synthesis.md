# Vikunja API — Synthesis

## Key Findings

### API Surface
Vikunja v2.2.0 exposes **111 endpoint paths** under `/api/v1`, organized into resource groups: tasks, projects, labels, views, buckets, teams, users, filters, tokens, sharing, webhooks, subscriptions, notifications, migration, and auth. The full OpenAPI 2.0 spec is served at `/api/v1/docs.json` on any running instance. (vikunja-openapi-spec, vikunja-api-docs)

### Non-Standard HTTP Method Mapping
Vikunja deliberately inverts the typical REST convention: **PUT creates** resources and **POST updates** them. GET reads, DELETE deletes — those are standard. This is a conscious design choice, not a bug. Our vk client already follows this pattern correctly. (deepwiki-api-design-patterns, vikunja-openapi-spec)

### Authentication
Two primary auth methods for API consumers: **API tokens** (recommended, long-lived, scoped) and **JWT tokens** (obtained via `/api/v1/login` with username/password). Both use `Authorization: Bearer <token>` header. BasicAuth is only for CalDAV. Vikunja Cloud only supports API tokens — no username/password login. (vikunja-api-docs, deepwiki-api-design-patterns)

### Pagination
All list endpoints paginate with `page` (1-indexed) and `per_page` (default 50) query params. Response headers `x-pagination-total-pages` and `x-pagination-result-count` report totals. The `s` parameter provides simple text search on list endpoints. (deepwiki-api-design-patterns, vikunja-openapi-spec)

### Filtering
Task listing supports a powerful filter syntax via the `filter` query parameter. Supports boolean operators (`&&`, `||`), comparisons, date math (`now+7d`, `now/d`), and field references in snake_case. Labels and projects must be referenced by numeric ID in API filters, not by name. Saved filters are first-class objects with CRUD endpoints. (vikunja-filter-api)

### Search
The search endpoint is `GET /api/v1/tasks` with `?s=<query>` parameter — **not** `/tasks/all` which returns HTTP 400 in v2.2.0. This was confirmed by our integration tests. (vikunja-openapi-spec, vikunja-filter-api)

### View System
`view_kind` is a **string** enum (`"list"`, `"gantt"`, `"table"`, `"kanban"`), not an integer. New projects automatically get all four view types. Kanban views have `bucket_configuration_mode: "manual"` with `default_bucket_id` and `done_bucket_id` set. (vikunja-openapi-spec — confirmed by integration testing)

### Error Handling
Errors return JSON with both HTTP status code and a Vikunja-specific `code` field for granular error identification. Multiple error codes can map to the same HTTP status. (deepwiki-api-design-patterns)

## Points of Agreement

All sources agree on:
- REST-ish API under `/api/v1` with Bearer token auth
- PUT=create, POST=update convention
- OpenAPI spec auto-generated from Go code annotations via swaggo/swag
- Pagination via query params + response headers

## Points of Disagreement

- The OpenAPI spec is labeled as v2.0 (Swagger), but the actual Vikunja version is v2.2.0. The spec format hasn't been upgraded to OpenAPI 3.x.
- DeepWiki (indexed Feb 2026) references some older patterns — the live instance is the authoritative source for current behavior.

## Gaps

- **Webhook payload schemas**: The spec documents webhook CRUD endpoints but doesn't detail the payload format Vikunja sends to webhook receivers.
- **Typesense search**: When Typesense is enabled, search behavior may differ from the default database LIKE queries — not documented in the API spec.
- **Rate limit response headers**: Not clear whether rate limit remaining/reset info is returned in response headers.
- **Reactions and relations**: Task relations and reactions are in the spec but not well documented beyond endpoint signatures.
