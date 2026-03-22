"""Auth service — login, status, token management."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

import requests

from vk.client import VikunjaClient
from vk.config import Config
from vk.exceptions import AuthenticationError
from vk.models import ApiToken


class AuthService:
    def __init__(self, client: VikunjaClient | None = None) -> None:
        self.client = client

    @staticmethod
    def login_with_credentials(url: str, username: str, password: str) -> str:
        """Authenticate with username/password and return a JWT token."""
        resp = requests.post(
            f"{url.rstrip('/')}/api/v1/login",
            json={"username": username, "password": password},
            timeout=30,
        )
        if resp.status_code != 200:
            raise AuthenticationError(f"Login failed: {resp.text}")
        return resp.json()["token"]

    def create_api_token(
        self,
        title: str,
        permissions: dict[str, list[str]] | None = None,
    ) -> ApiToken:
        """Create a long-lived API token (requires JWT auth)."""
        if self.client is None:
            raise AuthenticationError("Client not initialized")
        if permissions is None:
            permissions = {
                "tasks": ["read", "create", "update", "delete"],
                "projects": ["read", "create", "update"],
                "tasks_comments": ["read", "create"],
                "tasks_attachments": ["read", "create"],
                "labels": ["read", "create"],
            }
        expires = (datetime.now(timezone.utc) + timedelta(days=365 * 10)).isoformat()
        data = self.client.put(
            "/tokens",
            json={
                "title": title,
                "permissions": permissions,
                "expires_at": expires,
            },
        )
        return ApiToken.from_api(data)

    @staticmethod
    def status(config: Config) -> dict[str, Any]:
        """Check connection status."""
        try:
            url = config.url
            token = config.token
            client = VikunjaClient(url, token)
            data = client.get("/user", paginate=False)
            return {
                "connected": True,
                "url": url,
                "user": data.get("username", "unknown"),
            }
        except Exception as e:
            return {"connected": False, "error": str(e)}
