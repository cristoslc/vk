---
source-id: "vikunja-openapi-spec"
title: "Vikunja API v2.2.0 — OpenAPI Specification"
type: documentation-site
url: "http://localhost:3456/api/v1/docs.json"
fetched: 2026-03-24T20:10:11Z
hash: "cbe2833bf42e7be34cf9747f0dbc738a85dd1f8ce378aef82937581a12db7b23"
highlights:
  - "docs.json"
selective: false
---

# Vikunja API — OpenAPI Specification

**Title:** Vikunja API
**Version:** v2.2.0
**Description:** # Pagination
Every endpoint capable of pagination will return two headers:
* `x-pagination-total-pages`: The total number of available pages for this request
* `x-pagination-result-count`: The number of items returned for this request.
# Permissions
All endpoints which return a single item (project, task, etc.) - no array - will also return a `x-max-permission` header with the max permission the user has on this item as an int where `0` is `Read Only`, `1` is `Read & Write` and `2` is `Admin`.
This can be used to show or hide ui elements based on the permissions the user has.
# Errors
All errors have an error code and a human-readable error message in addition to the http status code. You should always check for the status code in the response, not only the http status code.
Due to limitations in the swagger library we're using for this document, only one error per http status code is documented here. Make sure to check the [error docs](https://vikunja.io/docs/errors/) in Vikunja's documentation for a full list of available error codes.
# Authorization
**JWT-Auth:** Main authorization method, used for most of the requests. Needs `Authorization: Bearer <jwt-token>`-header to authenticate successfully.

**API Token:** You can create scoped API tokens for your user and use the token to make authenticated requests in the context of that user. The token must be provided via an `Authorization: Bearer <token>` header, similar to jwt auth. See the documentation for the `api` group to manage token creation and revocation.

**BasicAuth:** Only used when requesting tasks via CalDAV.
<!-- ReDoc-Inject: <security-definitions> -->
**Base Path:** /api/v1
**Schemes:** 

## Security Definitions

### BasicAuth
- **Type:** basic

### JWTKeyAuth
- **Type:** apiKey
- **In:** header
- **Name:** Authorization

## Endpoints by Tag

### api

| Method | Path | Summary |
|--------|------|---------|
| GET | `/routes` | Get a list of all token api routes |
| GET | `/tokens` | Get all api tokens of the current user |
| PUT | `/tokens` | Create a new api token |
| DELETE | `/tokens/{tokenID}` | Deletes an existing api token |

### assignees

| Method | Path | Summary |
|--------|------|---------|
| GET | `/tasks/{taskID}/assignees` | Get all assignees for a task |
| PUT | `/tasks/{taskID}/assignees` | Add a new assignee to a task |
| POST | `/tasks/{taskID}/assignees/bulk` | Add multiple new assignees to a task |
| DELETE | `/tasks/{taskID}/assignees/{userID}` | Delete an assignee |

### auth

| Method | Path | Summary |
|--------|------|---------|
| POST | `/auth/openid/{provider}/callback` | Authenticate a user with OpenID Connect |
| POST | `/login` | Login |
| POST | `/register` | Register |
| POST | `/user/logout` | Logout |
| POST | `/user/token` | Renew link share token |
| POST | `/user/token/refresh` | Refresh user token |

### filter

| Method | Path | Summary |
|--------|------|---------|
| PUT | `/filters` | Creates a new saved filter |
| GET | `/filters/{id}` | Gets one saved filter |
| POST | `/filters/{id}` | Updates a saved filter |
| DELETE | `/filters/{id}` | Removes a saved filter |

### labels

| Method | Path | Summary |
|--------|------|---------|
| GET | `/labels` | Get all labels a user has access to |
| PUT | `/labels` | Create a label |
| GET | `/labels/{id}` | Gets one label |
| PUT | `/labels/{id}` | Update a label |
| DELETE | `/labels/{id}` | Delete a label |
| POST | `/tasks/{taskID}/labels/bulk` | Update all labels on a task. |
| GET | `/tasks/{task}/labels` | Get all labels on a task |
| PUT | `/tasks/{task}/labels` | Add a label to a task |
| DELETE | `/tasks/{task}/labels/{label}` | Remove a label from a task |

### migration

| Method | Path | Summary |
|--------|------|---------|
| GET | `/migration/microsoft-todo/auth` | Get the auth url from Microsoft Todo |
| POST | `/migration/microsoft-todo/migrate` | Migrate all projects, tasks etc. from Microsoft Todo |
| GET | `/migration/microsoft-todo/status` | Get migration status |
| POST | `/migration/ticktick/migrate` | Import all projects, tasks etc. from a TickTick backup export |
| GET | `/migration/ticktick/status` | Get migration status |
| GET | `/migration/todoist/auth` | Get the auth url from todoist |
| POST | `/migration/todoist/migrate` | Migrate all lists, tasks etc. from todoist |
| GET | `/migration/todoist/status` | Get migration status |
| GET | `/migration/trello/auth` | Get the auth url from trello |
| POST | `/migration/trello/migrate` | Migrate all projects, tasks etc. from trello |
| GET | `/migration/trello/status` | Get migration status |
| POST | `/migration/vikunja-file/migrate` | Import all projects, tasks etc. from a Vikunja data export |
| GET | `/migration/vikunja-file/status` | Get migration status |

### project

| Method | Path | Summary |
|--------|------|---------|
| GET | `/backgrounds/unsplash/image/{image}` | Get an unsplash image |
| GET | `/backgrounds/unsplash/image/{image}/thumb` | Get an unsplash thumbnail image |
| GET | `/backgrounds/unsplash/search` | Search for a background from unsplash |
| GET | `/projects` | Get all projects a user has access to |
| PUT | `/projects` | Creates a new project |
| GET | `/projects/{id}` | Gets one project |
| POST | `/projects/{id}` | Updates a project |
| DELETE | `/projects/{id}` | Deletes a project |
| GET | `/projects/{id}/background` | Get the project background |
| DELETE | `/projects/{id}/background` | Remove a project background |
| POST | `/projects/{id}/backgrounds/unsplash` | Set an unsplash photo as project background |
| PUT | `/projects/{id}/backgrounds/upload` | Upload a project background |
| GET | `/projects/{id}/projectusers` | Get users |
| GET | `/projects/{id}/views/{view}/buckets` | Get all kanban buckets of a project |
| PUT | `/projects/{id}/views/{view}/buckets` | Create a new bucket |
| PUT | `/projects/{projectID}/duplicate` | Duplicate an existing project |
| POST | `/projects/{projectID}/views/{view}/buckets/{bucketID}` | Update an existing bucket |
| DELETE | `/projects/{projectID}/views/{view}/buckets/{bucketID}` | Deletes an existing bucket |
| GET | `/projects/{project}/views` | Get all project views for a project |
| PUT | `/projects/{project}/views` | Create a project view |
| GET | `/projects/{project}/views/{id}` | Get one project view |
| POST | `/projects/{project}/views/{id}` | Updates a project view |
| DELETE | `/projects/{project}/views/{id}` | Delete a project view |

### service

| Method | Path | Summary |
|--------|------|---------|
| GET | `/info` | Info |

### sharing

| Method | Path | Summary |
|--------|------|---------|
| POST | `/notifications` | Mark all notifications of a user as read |
| GET | `/projects/{id}/teams` | Get teams on a project |
| PUT | `/projects/{id}/teams` | Add a team to a project |
| GET | `/projects/{id}/users` | Get users on a project |
| PUT | `/projects/{id}/users` | Add a user to a project |
| POST | `/projects/{projectID}/teams/{teamID}` | Update a team <-> project relation |
| DELETE | `/projects/{projectID}/teams/{teamID}` | Delete a team from a project |
| POST | `/projects/{projectID}/users/{userID}` | Update a user <-> project relation |
| DELETE | `/projects/{projectID}/users/{userID}` | Delete a user from a project |
| GET | `/projects/{project}/shares` | Get all link shares for a project |
| PUT | `/projects/{project}/shares` | Share a project via link |
| GET | `/projects/{project}/shares/{share}` | Get one link shares for a project |
| DELETE | `/projects/{project}/shares/{share}` | Remove a link share |
| POST | `/shares/{share}/auth` | Get an auth token for a share |

### subscriptions

| Method | Path | Summary |
|--------|------|---------|
| GET | `/notifications` | Get all notifications for the current user |
| POST | `/notifications/{id}` | Mark a notification as (un-)read |
| PUT | `/subscriptions/{entity}/{entityID}` | Subscribes the current user to an entity. |
| DELETE | `/subscriptions/{entity}/{entityID}` | Unsubscribe the current user from an entity. |

### task

| Method | Path | Summary |
|--------|------|---------|
| PUT | `/projects/{id}/tasks` | Create a task |
| GET | `/projects/{id}/views/{view}/tasks` | Get tasks in a project |
| POST | `/projects/{project}/views/{view}/buckets/{bucket}/tasks` | Update a task bucket |
| GET | `/tasks` | Get tasks |
| POST | `/tasks/bulk` | Update multiple tasks |
| GET | `/tasks/{id}` | Get one task |
| POST | `/tasks/{id}` | Update a task |
| DELETE | `/tasks/{id}` | Delete a task |
| GET | `/tasks/{id}/attachments` | Get  all attachments for one task. |
| PUT | `/tasks/{id}/attachments` | Upload a task attachment |
| GET | `/tasks/{id}/attachments/{attachmentID}` | Get one attachment. |
| DELETE | `/tasks/{id}/attachments/{attachmentID}` | Delete an attachment |
| POST | `/tasks/{id}/position` | Updates a task position |
| POST | `/tasks/{projecttask}/read` | Mark a task as read |
| GET | `/tasks/{taskID}/comments` | Get all task comments |
| PUT | `/tasks/{taskID}/comments` | Create a new task comment |
| GET | `/tasks/{taskID}/comments/{commentID}` | Remove a task comment |
| POST | `/tasks/{taskID}/comments/{commentID}` | Update an existing task comment |
| DELETE | `/tasks/{taskID}/comments/{commentID}` | Remove a task comment |
| PUT | `/tasks/{taskID}/duplicate` | Duplicate a task |
| PUT | `/tasks/{taskID}/relations` | Create a new relation between two tasks |
| DELETE | `/tasks/{taskID}/relations/{relationKind}/{otherTaskID}` | Remove a task relation |
| GET | `/{kind}/{id}/reactions` | Get all reactions for an entity |
| PUT | `/{kind}/{id}/reactions` | Add a reaction to an entity |
| POST | `/{kind}/{id}/reactions/delete` | Removes the user's reaction |

### team

| Method | Path | Summary |
|--------|------|---------|
| GET | `/teams` | Get teams |
| PUT | `/teams` | Creates a new team |
| GET | `/teams/{id}` | Gets one team |
| POST | `/teams/{id}` | Updates a team |
| DELETE | `/teams/{id}` | Deletes a team |
| PUT | `/teams/{id}/members` | Add a user to a team |
| POST | `/teams/{id}/members/{userID}/admin` | Toggle a team member's admin status |
| DELETE | `/teams/{id}/members/{username}` | Remove a user from a team |

### testing

| Method | Path | Summary |
|--------|------|---------|
| PATCH | `/test/{table}` | Reset the db to a defined state |

### user

| Method | Path | Summary |
|--------|------|---------|
| GET | `/user` | Get user information |
| POST | `/user/confirm` | Confirm the email of a new user |
| POST | `/user/deletion/cancel` | Abort a user deletion request |
| POST | `/user/deletion/confirm` | Confirm a user deletion request |
| POST | `/user/deletion/request` | Request the deletion of the user |
| GET | `/user/export` | Get current user data export |
| POST | `/user/export/download` | Download a user data export. |
| POST | `/user/export/request` | Request a user data export. |
| POST | `/user/password` | Change password |
| POST | `/user/password/reset` | Resets a password |
| POST | `/user/password/token` | Request password reset token |
| GET | `/user/settings/avatar` | Return user avatar setting |
| POST | `/user/settings/avatar` | Set the user's avatar |
| PUT | `/user/settings/avatar/upload` | Upload a user avatar |
| POST | `/user/settings/email` | Update email address |
| POST | `/user/settings/general` | Change general user settings of the current user. |
| GET | `/user/settings/token/caldav` | Returns the caldav tokens for the current user |
| PUT | `/user/settings/token/caldav` | Generate a caldav token |
| DELETE | `/user/settings/token/caldav/{id}` | Delete a caldav token by id |
| GET | `/user/settings/totp` | Totp setting for the current user |
| POST | `/user/settings/totp/disable` | Disable totp settings |
| POST | `/user/settings/totp/enable` | Enable a previously enrolled totp setting. |
| POST | `/user/settings/totp/enroll` | Enroll a user into totp |
| GET | `/user/settings/totp/qrcode` | Totp QR Code |
| GET | `/user/timezones` | Get all available time zones on this vikunja instance |
| GET | `/users` | Get users |
| GET | `/{username}/avatar` | User Avatar |

### webhooks

| Method | Path | Summary |
|--------|------|---------|
| GET | `/projects/{id}/webhooks` | Get all api webhook targets for the specified project |
| PUT | `/projects/{id}/webhooks` | Create a webhook target |
| POST | `/projects/{id}/webhooks/{webhookID}` | Change a webhook target's events. |
| DELETE | `/projects/{id}/webhooks/{webhookID}` | Deletes an existing webhook target |
| GET | `/user/settings/webhooks` | Get all user-level webhook targets |
| PUT | `/user/settings/webhooks` | Create a user-level webhook target |
| GET | `/user/settings/webhooks/events` | Get available user-directed webhook events |
| POST | `/user/settings/webhooks/{id}` | Update a user-level webhook target |
| DELETE | `/user/settings/webhooks/{id}` | Delete a user-level webhook target |
| GET | `/webhooks/events` | Get all possible webhook events |

## Models

### auth.Token
**Fields:** token

### background.Image
**Fields:** blur_hash, id, info, thumb, url

### code_vikunja_io_api_pkg_modules_auth_openid.Provider
**Fields:** auth_url, client_id, email_fallback, force_user_info, key, logout_url, name, scope, username_fallback

### files.File
**Fields:** created, id, mime, name, size

### handler.AuthURL
**Fields:** url

### microsofttodo.Migration
**Fields:** code

### migration.Status
**Fields:** finished_at, id, migrator_name, started_at

### models.APIPermissions
**Fields:** 

### models.APIToken
**Fields:** created, expires_at, id, permissions, title, token

### models.APITokenRoute
**Fields:** 

### models.Bucket
**Fields:** count, created, created_by, id, limit, position, project_view_id, tasks, title, updated

### models.BulkAssignees
**Fields:** assignees

### models.BulkTask
**Fields:** fields, task_ids, tasks, values

### models.DatabaseNotifications
**Fields:** created, id, name, notification, read, read_at

### models.Label
**Fields:** created, created_by, description, hex_color, id, title, updated

### models.LabelTask
**Fields:** created, label_id

### models.LabelTaskBulk
**Fields:** labels

### models.LinkSharing
**Fields:** created, hash, id, name, password, permission, shared_by, sharing_type, updated

### models.Message
**Fields:** message

### models.Permission
**Fields:** 

### models.Project
**Fields:** background_blur_hash, background_information, created, description, hex_color, id, identifier, is_archived, is_favorite, max_permission, owner, parent_project_id, position, subscription, title, ... (17 total)

### models.ProjectDuplicate
**Fields:** duplicated_project, parent_project_id

### models.ProjectUser
**Fields:** created, id, permission, updated, username

### models.ProjectView
**Fields:** bucket_configuration, bucket_configuration_mode, created, default_bucket_id, done_bucket_id, filter, id, position, project_id, title, updated, view_kind

### models.ProjectViewBucketConfiguration
**Fields:** filter, title

### models.Reaction
**Fields:** created, user, value

### models.ReactionMap
**Fields:** 

### models.RelatedTaskMap
**Fields:** 

### models.RelationKind
**Fields:** 

### models.ReminderRelation
**Fields:** 

### models.RouteDetail
**Fields:** method, path

### models.SavedFilter
**Fields:** created, description, filters, id, is_favorite, owner, title, updated

### models.SharingType
**Fields:** 

### models.Subscription
**Fields:** created, entity, entity_id, id

### models.Task
**Fields:** assignees, attachments, bucket_id, buckets, comment_count, comments, cover_image_attachment_id, created, created_by, description, done, done_at, due_date, end_date, hex_color, ... (34 total)

### models.TaskAssginee
**Fields:** created, user_id

### models.TaskAttachment
**Fields:** created, created_by, file, id, task_id

### models.TaskBucket
**Fields:** bucket, bucket_id, project_view_id, task, task_id

### models.TaskCollection
**Fields:** filter, filter_include_nulls, order_by, s, sort_by

### models.TaskComment
**Fields:** author, comment, created, id, reactions, updated

### models.TaskDuplicate
**Fields:** duplicated_task

### models.TaskPosition
**Fields:** position, project_view_id, task_id

### models.TaskRelation
**Fields:** created, created_by, other_task_id, relation_kind, task_id

### models.TaskReminder
**Fields:** relative_period, relative_to, reminder

### models.TaskRepeatMode
**Fields:** 

### models.TaskUnreadStatus
**Fields:** taskID, userID

### models.Team
**Fields:** created, created_by, description, external_id, id, include_public, is_public, members, name, updated

### models.TeamMember
**Fields:** admin, created, id, username

### models.TeamProject
**Fields:** created, id, permission, team_id, updated

### models.TeamUser
**Fields:** admin, created, email, id, name, updated, username

### models.TeamWithPermission
**Fields:** created, created_by, description, external_id, id, include_public, is_public, members, name, permission, updated

### models.UserWithPermission
**Fields:** created, email, id, name, permission, updated, username

### models.Webhook
**Fields:** basic_auth_password, basic_auth_user, created, created_by, events, id, project_id, secret, target_url, updated, user_id

### notifications.DatabaseNotification
**Fields:** created, id, name, notification, read_at

### openid.Callback
**Fields:** code, redirect_url, scope

### todoist.Migration
**Fields:** code

### trello.Migration
**Fields:** code

### user.EmailConfirm
**Fields:** token

### user.EmailUpdate
**Fields:** new_email, password

### user.Login
**Fields:** long_token, password, totp_passcode, username

### user.PasswordReset
**Fields:** new_password, token

### user.PasswordTokenRequest
**Fields:** email

### user.TOTP
**Fields:** enabled, secret, url

### user.TOTPPasscode
**Fields:** passcode

### user.Token
**Fields:** created, id, token

### user.User
**Fields:** created, email, id, name, updated, username

### v1.LinkShareAuth
**Fields:** password

### v1.UserAvatarProvider
**Fields:** avatar_provider

### v1.UserDeletionRequestConfirm
**Fields:** token

### v1.UserExportStatus
**Fields:** created, expires, id, size

### v1.UserPassword
**Fields:** new_password, old_password

### v1.UserPasswordConfirmation
**Fields:** password

### v1.UserRegister
**Fields:** email, language, password, username

### v1.UserSettings
**Fields:** default_project_id, discoverable_by_email, discoverable_by_name, email_reminders_enabled, extra_settings_links, frontend_settings, language, name, overdue_tasks_reminders_enabled, overdue_tasks_reminders_time, timezone, week_start

### v1.UserWithSettings
**Fields:** auth_provider, created, deletion_scheduled_at, email, id, is_local_user, name, settings, updated, username

### v1.authInfo
**Fields:** ldap, local, openid_connect

### v1.ldapAuthInfo
**Fields:** enabled

### v1.legalInfo
**Fields:** imprint_url, privacy_policy_url

### v1.localAuthInfo
**Fields:** enabled, registration_enabled

### v1.openIDAuthInfo
**Fields:** enabled, providers

### v1.vikunjaInfos
**Fields:** auth, available_migrators, caldav_enabled, demo_mode_enabled, email_reminders_enabled, enabled_background_providers, frontend_url, legal, link_sharing_enabled, max_file_size, max_items_per_page, motd, public_teams_enabled, task_attachments_enabled, task_comments_enabled, ... (19 total)

### web.HTTPError
**Fields:** code, message
