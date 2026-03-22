# vk — Vikunja CLI and MCP Server

A unified Python library for interacting with a [Vikunja](https://vikunja.io) instance, exposed through three adapters: a CLI (`vk`), an MCP stdio server, and an MCP HTTP/SSE server. All three share a single core that owns Vikunja API communication, domain logic, and output formatting.

## Why

Vikunja is a self-hosted, open-source task management platform with a clean REST API and no rate limits. But it has no official CLI and no MCP server. `vk` fills both gaps with a single codebase — giving both humans (via terminal) and AI agents (via MCP) full access to Vikunja.

## Install

```bash
# With uv (recommended)
uv tool install git+https://github.com/cristoslc/vk.git

# From source
git clone https://github.com/cristoslc/vk.git
cd vk
uv sync
```

Requires Python 3.11+.

## Quick start

```bash
# Configure (writes .vk-config.json)
vk auth login --url http://localhost:3456 --token tk_your_api_token

# Check connection
vk auth status

# List projects
vk project list

# Create a task
vk task create --title "Buy groceries" --project "Household Tasks" --bucket "Incoming"

# Move a task between Eisenhower buckets
vk task move 42 --bucket "Do Now"

# Search
vk search "electric bill"

# JSON output (all commands)
vk task list "Household Tasks" --json
```

## Commands

```
vk auth login [--url URL] [--token TOKEN]     # Configure authentication
vk auth status                                 # Check connection

vk project list [--json]                       # List all projects
vk project create --title TITLE [--json]       # Create a project
vk project get ID [--json]                     # Get project details

vk bucket list PROJECT [--view VIEW] [--json]  # List kanban buckets
vk bucket create PROJECT --title T [--json]    # Create a bucket

vk task list [PROJECT] [--bucket B] [--json]   # List tasks
vk task get ID [--json]                        # Get a task
vk task create --title T --project P [--json]  # Create a task
vk task update ID [--title T] [--done] [--json]# Update a task
vk task move ID --bucket B [--json]            # Move to bucket
vk task delete ID [--force]                    # Delete a task

vk comment list TASK [--json]                  # List comments
vk comment add TASK --text TEXT [--json]        # Add a comment

vk attach list TASK [--json]                   # List attachments
vk attach add TASK --file PATH [--json]         # Upload attachment
vk attach get TASK ATTACH_ID [--output PATH]    # Download attachment

vk search QUERY [--project P] [--json]          # Search tasks

vk label list [--json]                          # List labels
vk label create --title T [--color HEX] [--json]# Create a label

vk mcp stdio                                    # MCP server (stdio)
vk mcp http [--port 8456]                        # MCP server (HTTP/SSE)
```

## MCP integration

### Claude Code (stdio)

Add to your `.mcp.json`:

```json
{
  "mcpServers": {
    "vk": {
      "command": "vk",
      "args": ["mcp", "stdio"],
      "env": {
        "VK_URL": "http://localhost:3456",
        "VK_TOKEN": "tk_your_token"
      }
    }
  }
}
```

### HTTP/SSE

```bash
vk mcp http --port 8456
```

Connects at `http://localhost:8456/sse` with messages endpoint at `/messages/`.

### Available MCP tools

18 tools mirroring the CLI surface: `vk_task_list`, `vk_task_create`, `vk_task_update`, `vk_task_move`, `vk_task_get`, `vk_task_delete`, `vk_project_list`, `vk_project_create`, `vk_project_get`, `vk_bucket_list`, `vk_bucket_create`, `vk_comment_list`, `vk_comment_add`, `vk_attach_list`, `vk_attach_add`, `vk_search`, `vk_label_list`, `vk_label_create`.

## Configuration

Token resolution order (highest wins):

1. `--token` flag / explicit parameter
2. `VK_TOKEN` environment variable
3. `.vk-config.json` in current directory (walks up to git root)
4. `~/.config/vk/config.json`

Config file format:

```json
{
  "url": "http://localhost:3456",
  "token": "tk_...",
  "default_project": "Household Tasks",
  "kanban_view": "Kanban"
}
```

## Architecture

Hexagonal architecture — three adapters share one core:

```
         CLI (Click)    MCP (stdio)    MCP (HTTP/SSE)
              \              |              /
               \             |             /
                +-------Core Services------+
                |  tasks, projects, buckets |
                |  comments, attachments    |
                |  search, labels, auth     |
                +----------+---------------+
                           |
                    Vikunja HTTP Client
                           |
                    Vikunja REST API
```

- **Core services** accept and return typed domain objects (dataclasses), not raw JSON
- **Name resolution** maps human names ("Household Tasks") to IDs via local cache
- **Pagination** handled transparently by the HTTP client

## Development

```bash
git clone https://github.com/cristoslc/vk.git
cd vk
uv sync
uv run pytest               # 47 tests
uv run vk --help
```

## License

MIT
