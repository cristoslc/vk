---
source-id: "deepwiki-overview"
title: "Vikunja Architecture Overview — DeepWiki"
type: web
url: "https://deepwiki.com/go-vikunja/vikunja"
fetched: 2026-03-24T20:10:11Z
hash: "2b4ac9ae3dc08f00abcdf65771890f131965cbbf148f5b535a63309361942354"
---

# Vikunja Architecture Overview

Vikunja is an open-source, self-hosted task management application licensed under AGPL-3.0-or-later. It provides a comprehensive todo system with features including project organization, task collaboration, multiple view types (Kanban, List, Table, Gantt), and integrations with external systems via CalDAV and webhooks.

## System Components

| Component | Technology | Purpose |
| --- | --- | --- |
| **Web Frontend** | Vue 3.5.27, Pinia, Vite | Browser-based SPA for task management |
| **Backend API** | Go 1.25, Echo v5 | RESTful API server with JWT authentication |
| **Desktop Application** | Electron 40.0.0 | Native desktop wrapper for the web frontend |

## Backend Architecture

The backend is written in Go and uses the Echo v5 web framework. It provides a RESTful API with JWT-based authentication, serving endpoints for task management, project organization, user management, and more.

Configuration is loaded from environment variables and YAML files via Viper. Swagger documentation is generated from code annotations.

## Data Storage

Vikunja uses XORM as the ORM layer supporting SQLite, MySQL, or PostgreSQL. Search can be powered by Typesense or fall back to database LIKE queries. Files can be stored locally via Afero or in S3-compatible storage.

## Authentication Methods

| Method | Configuration | Description |
| --- | --- | --- |
| **Local** | `auth.local.enabled` | Username/password with BCrypt hashing |
| **LDAP** | `auth.ldap.enabled` | LDAP/Active Directory integration |
| **OpenID Connect** | `auth.openid.enabled` | OAuth2/OIDC providers |
| **API Tokens** | Always enabled | Long-lived scoped tokens |
| **Link Sharing** | `service.enablelinksharing` | Public access with optional password |

## Key Features

* **Task Management**: CRUD operations, task relations, repeating tasks, positions, buckets
* **Project Organization**: Hierarchical projects, multiple view types (List, Kanban, Table, Gantt)
* **Collaboration**: Team management, sharing, permissions, link sharing
* **Rich Content**: Task descriptions with markdown, attachments, comments
* **Search**: Typesense-powered full-text search with filter syntax
* **Integrations**: CalDAV protocol, webhooks, data migration from Todoist/Trello/TickTick
* **Security**: JWT authentication, 2FA (TOTP), rate limiting, CORS

## API Documentation

Vikunja uses Swagger/OpenAPI 2.0 for API documentation. Annotations in the Go source code are processed by `swaggo/swag` to generate the OpenAPI specification. The interactive API documentation is available at `/api/v1/docs` when the server is running.
