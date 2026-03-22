"""Tests for config and token resolution."""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from vk.config import Config
from vk.exceptions import ConfigError


class TestConfigResolution:
    def test_explicit_args_win(self) -> None:
        c = Config(url="http://explicit", token="tok-explicit")
        assert c.url == "http://explicit"
        assert c.token == "tok-explicit"

    def test_env_vars(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("VK_URL", "http://env")
        monkeypatch.setenv("VK_TOKEN", "tok-env")
        c = Config()
        assert c.url == "http://env"
        assert c.token == "tok-env"

    def test_explicit_beats_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("VK_URL", "http://env")
        monkeypatch.setenv("VK_TOKEN", "tok-env")
        c = Config(url="http://explicit", token="tok-explicit")
        assert c.url == "http://explicit"

    def test_config_file(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("VK_URL", raising=False)
        monkeypatch.delenv("VK_TOKEN", raising=False)
        config_file = tmp_path / ".vk-config.json"
        config_file.write_text(json.dumps({"url": "http://file", "token": "tok-file"}))
        c = Config(config_path=str(config_file))
        assert c.url == "http://file"
        assert c.token == "tok-file"

    def test_missing_config_raises(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        monkeypatch.delenv("VK_URL", raising=False)
        monkeypatch.delenv("VK_TOKEN", raising=False)
        monkeypatch.chdir(tmp_path)
        c = Config()
        with pytest.raises(ConfigError):
            _ = c.url


class TestConfigWrite:
    def test_write_config(self, tmp_path: Path) -> None:
        path = tmp_path / ".vk-config.json"
        Config.write_config("http://test", "tok-123", path=path)
        data = json.loads(path.read_text())
        assert data["url"] == "http://test"
        assert data["token"] == "tok-123"

    def test_write_config_with_extras(self, tmp_path: Path) -> None:
        path = tmp_path / ".vk-config.json"
        Config.write_config(
            "http://test", "tok-123", path=path,
            default_project="Household", kanban_view="Kanban"
        )
        data = json.loads(path.read_text())
        assert data["default_project"] == "Household"
