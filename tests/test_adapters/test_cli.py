"""Tests for the CLI adapter."""

from __future__ import annotations

import responses
from click.testing import CliRunner

from vk.adapters.cli import cli

import pytest

BASE_URL = "http://vikunja.test"
TOKEN = "test-token"


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


class TestCLIHelp:
    def test_main_help(self, runner: CliRunner) -> None:
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "vk" in result.output

    def test_task_help(self, runner: CliRunner) -> None:
        result = runner.invoke(cli, ["task", "--help"])
        assert result.exit_code == 0
        assert "list" in result.output

    def test_project_help(self, runner: CliRunner) -> None:
        result = runner.invoke(cli, ["project", "--help"])
        assert result.exit_code == 0

    def test_mcp_help(self, runner: CliRunner) -> None:
        result = runner.invoke(cli, ["mcp", "--help"])
        assert result.exit_code == 0
        assert "stdio" in result.output
        assert "http" in result.output


class TestProjectCommands:
    @responses.activate
    def test_project_list(self, runner: CliRunner) -> None:
        responses.add(
            responses.GET,
            f"{BASE_URL}/api/v1/projects",
            json=[{"id": 1, "title": "Household"}, {"id": 2, "title": "Work"}],
        )
        result = runner.invoke(cli, ["--url", BASE_URL, "--token", TOKEN, "project", "list"])
        assert result.exit_code == 0
        assert "Household" in result.output

    @responses.activate
    def test_project_list_json(self, runner: CliRunner) -> None:
        responses.add(
            responses.GET,
            f"{BASE_URL}/api/v1/projects",
            json=[{"id": 1, "title": "Household"}],
        )
        result = runner.invoke(cli, ["--url", BASE_URL, "--token", TOKEN, "project", "list", "--json"])
        assert result.exit_code == 0
        assert '"title": "Household"' in result.output

    @responses.activate
    def test_project_get(self, runner: CliRunner) -> None:
        responses.add(
            responses.GET,
            f"{BASE_URL}/api/v1/projects/1",
            json={"id": 1, "title": "Household"},
        )
        result = runner.invoke(cli, ["--url", BASE_URL, "--token", TOKEN, "project", "get", "1"])
        assert result.exit_code == 0
        assert "Household" in result.output


class TestTaskCommands:
    @responses.activate
    def test_task_get(self, runner: CliRunner) -> None:
        responses.add(
            responses.GET,
            f"{BASE_URL}/api/v1/tasks/42",
            json={"id": 42, "title": "Buy milk", "done": False},
        )
        result = runner.invoke(cli, ["--url", BASE_URL, "--token", TOKEN, "task", "get", "42"])
        assert result.exit_code == 0
        assert "Buy milk" in result.output

    @responses.activate
    def test_task_get_json(self, runner: CliRunner) -> None:
        responses.add(
            responses.GET,
            f"{BASE_URL}/api/v1/tasks/42",
            json={"id": 42, "title": "Buy milk", "done": False},
        )
        result = runner.invoke(
            cli, ["--url", BASE_URL, "--token", TOKEN, "task", "get", "42", "--json"]
        )
        assert result.exit_code == 0
        assert '"title": "Buy milk"' in result.output


class TestSearchCommand:
    @responses.activate
    def test_search(self, runner: CliRunner) -> None:
        responses.add(
            responses.GET,
            f"{BASE_URL}/api/v1/tasks",
            json=[{"id": 10, "title": "Electric bill", "project_id": 1}],
        )
        result = runner.invoke(
            cli, ["--url", BASE_URL, "--token", TOKEN, "search", "electric"]
        )
        assert result.exit_code == 0
        assert "Electric bill" in result.output
