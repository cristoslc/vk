"""Tests for the Vikunja HTTP client."""

from __future__ import annotations

import responses

from vk.client import VikunjaClient
from vk.exceptions import ApiError, AuthenticationError, NotFoundError

import pytest


BASE_URL = "http://vikunja.test"
TOKEN = "test-token"


@pytest.fixture
def client() -> VikunjaClient:
    return VikunjaClient(BASE_URL, TOKEN)


class TestClientAuth:
    @responses.activate
    def test_auth_header_is_set(self, client: VikunjaClient) -> None:
        responses.add(
            responses.GET,
            f"{BASE_URL}/api/v1/user",
            json={"id": 1, "username": "test"},
        )
        client.get("/user", paginate=False)
        assert responses.calls[0].request.headers["Authorization"] == f"Bearer {TOKEN}"

    @responses.activate
    def test_401_raises_authentication_error(self, client: VikunjaClient) -> None:
        responses.add(
            responses.GET,
            f"{BASE_URL}/api/v1/user",
            status=401,
        )
        with pytest.raises(AuthenticationError):
            client.get("/user", paginate=False)


class TestClientErrors:
    @responses.activate
    def test_404_raises_not_found(self, client: VikunjaClient) -> None:
        responses.add(
            responses.GET,
            f"{BASE_URL}/api/v1/tasks/999",
            status=404,
        )
        with pytest.raises(NotFoundError):
            client.get("/tasks/999", paginate=False)

    @responses.activate
    def test_500_raises_api_error(self, client: VikunjaClient) -> None:
        responses.add(
            responses.GET,
            f"{BASE_URL}/api/v1/projects",
            json={"message": "Internal error"},
            status=500,
        )
        with pytest.raises(ApiError) as exc_info:
            client.get("/projects", paginate=False)
        assert exc_info.value.status_code == 500


class TestClientPagination:
    @responses.activate
    def test_fetches_all_pages(self, client: VikunjaClient) -> None:
        # Page 1: 50 items
        responses.add(
            responses.GET,
            f"{BASE_URL}/api/v1/projects",
            json=[{"id": i} for i in range(50)],
        )
        # Page 2: 10 items (less than per_page, so pagination stops)
        responses.add(
            responses.GET,
            f"{BASE_URL}/api/v1/projects",
            json=[{"id": i} for i in range(50, 60)],
        )
        result = client.get("/projects")
        assert len(result) == 60
        assert len(responses.calls) == 2

    @responses.activate
    def test_single_page(self, client: VikunjaClient) -> None:
        responses.add(
            responses.GET,
            f"{BASE_URL}/api/v1/projects",
            json=[{"id": 1}, {"id": 2}],
        )
        result = client.get("/projects")
        assert len(result) == 2

    @responses.activate
    def test_non_list_response_no_pagination(self, client: VikunjaClient) -> None:
        responses.add(
            responses.GET,
            f"{BASE_URL}/api/v1/user",
            json={"id": 1, "username": "test"},
        )
        result = client.get("/user")
        assert result == {"id": 1, "username": "test"}


class TestClientMethods:
    @responses.activate
    def test_post(self, client: VikunjaClient) -> None:
        responses.add(
            responses.POST,
            f"{BASE_URL}/api/v1/tasks/1",
            json={"id": 1, "title": "Updated"},
        )
        result = client.post("/tasks/1", json={"title": "Updated"})
        assert result["title"] == "Updated"

    @responses.activate
    def test_put(self, client: VikunjaClient) -> None:
        responses.add(
            responses.PUT,
            f"{BASE_URL}/api/v1/projects",
            json={"id": 5, "title": "New Project"},
        )
        result = client.put("/projects", json={"title": "New Project"})
        assert result["id"] == 5

    @responses.activate
    def test_delete(self, client: VikunjaClient) -> None:
        responses.add(
            responses.DELETE,
            f"{BASE_URL}/api/v1/tasks/1",
            status=204,
        )
        result = client.delete("/tasks/1")
        assert result is None
