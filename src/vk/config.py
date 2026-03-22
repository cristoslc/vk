"""Configuration and token resolution for vk."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Any

from vk.exceptions import ConfigError


class Config:
    """Resolves Vikunja URL and token from multiple sources.

    Resolution order (highest wins):
    1. Explicit arguments
    2. Environment variables (VK_URL, VK_TOKEN)
    3. .vk-config.json in current directory (walk up to git root)
    4. ~/.config/vk/config.json
    """

    def __init__(
        self,
        url: str | None = None,
        token: str | None = None,
        config_path: str | None = None,
    ) -> None:
        self._explicit_url = url
        self._explicit_token = token
        self._config_path = config_path
        self._data: dict[str, Any] | None = None

    def _load_config_file(self) -> dict[str, Any]:
        if self._data is not None:
            return self._data

        if self._config_path:
            p = Path(self._config_path)
            if p.exists():
                data: dict[str, Any] = json.loads(p.read_text())
                self._data = data
                return data

        # Walk up from cwd to git root looking for .vk-config.json
        current = Path.cwd()
        git_root = self._find_git_root()
        stop_at = git_root or Path(current.anchor)

        while True:
            candidate = current / ".vk-config.json"
            if candidate.exists():
                data = json.loads(candidate.read_text())
                self._data = data
                return data
            if current == stop_at or current.parent == current:
                break
            current = current.parent

        # User config
        user_config = Path.home() / ".config" / "vk" / "config.json"
        if user_config.exists():
            data = json.loads(user_config.read_text())
            self._data = data
            return data

        self._data = {}
        return self._data

    @staticmethod
    def _find_git_root() -> Path | None:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                capture_output=True,
                text=True,
                check=True,
            )
            return Path(result.stdout.strip())
        except (subprocess.CalledProcessError, FileNotFoundError):
            return None

    @property
    def url(self) -> str:
        if self._explicit_url:
            return self._explicit_url
        if env_url := os.environ.get("VK_URL"):
            return env_url
        data = self._load_config_file()
        if file_url := data.get("url"):
            return file_url
        raise ConfigError(
            "No Vikunja URL configured. Set VK_URL, pass --url, or run 'vk auth login'."
        )

    @property
    def token(self) -> str:
        if self._explicit_token:
            return self._explicit_token
        if env_token := os.environ.get("VK_TOKEN"):
            return env_token
        data = self._load_config_file()
        if file_token := data.get("token"):
            return file_token
        raise ConfigError(
            "No Vikunja token configured. Set VK_TOKEN, pass --token, or run 'vk auth login'."
        )

    @property
    def default_project(self) -> str | None:
        data = self._load_config_file()
        return data.get("default_project")

    @property
    def kanban_view(self) -> str | None:
        data = self._load_config_file()
        return data.get("kanban_view")

    @staticmethod
    def write_config(
        url: str,
        token: str,
        path: Path | None = None,
        default_project: str | None = None,
        kanban_view: str | None = None,
    ) -> Path:
        """Write a config file. Returns the path written to."""
        if path is None:
            path = Path.cwd() / ".vk-config.json"
        data: dict[str, Any] = {"url": url, "token": token}
        if default_project:
            data["default_project"] = default_project
        if kanban_view:
            data["kanban_view"] = kanban_view
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2) + "\n")
        return path
