"""Shared test fixtures."""

from __future__ import annotations

import pytest
import responses

from vk.client import VikunjaClient
from vk.config import Config


BASE_URL = "http://vikunja.test"
TOKEN = "test-token-abc123"


@pytest.fixture
def base_url() -> str:
    return BASE_URL


@pytest.fixture
def token() -> str:
    return TOKEN


@pytest.fixture
def config(tmp_path: object) -> Config:
    return Config(url=BASE_URL, token=TOKEN)


@pytest.fixture
def client() -> VikunjaClient:
    return VikunjaClient(BASE_URL, TOKEN)


@pytest.fixture
def mocked_responses():
    """Activate responses mock for HTTP requests."""
    with responses.RequestsMock() as rsps:
        yield rsps
