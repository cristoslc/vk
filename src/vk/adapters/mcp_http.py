"""MCP server — HTTP/SSE transport."""

from __future__ import annotations

from mcp.server import Server
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Mount, Route

from vk.adapters.mcp_tools import register_tools
from vk.config import Config


def run_http(config: Config, port: int = 8456) -> None:
    """Launch MCP server over HTTP with SSE transport."""
    import uvicorn

    server = Server("vk")
    register_tools(server, config)

    sse = SseServerTransport("/messages/")

    async def handle_sse(request):  # type: ignore[no-untyped-def]
        async with sse.connect_sse(
            request.scope, request.receive, request._send
        ) as streams:
            await server.run(
                streams[0], streams[1], server.create_initialization_options()
            )

    app = Starlette(
        routes=[
            Route("/sse", endpoint=handle_sse),
            Mount("/messages/", app=sse.handle_post_message),
        ],
    )

    uvicorn.run(app, host="0.0.0.0", port=port)
