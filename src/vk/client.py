"""Vikunja REST API HTTP client."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import requests

from vk.exceptions import ApiError, AuthenticationError, NotFoundError


class VikunjaClient:
    """Stateless HTTP adapter to the Vikunja REST API.

    Handles auth headers, pagination, multipart uploads, and error mapping.
    """

    def __init__(self, base_url: str, token: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.token = token
        self._session = requests.Session()
        self._session.headers["Authorization"] = f"Bearer {token}"

    def _url(self, path: str) -> str:
        return f"{self.base_url}/api/v1{path}"

    def _handle_response(self, resp: requests.Response) -> Any:
        if resp.status_code == 401:
            raise AuthenticationError("Invalid or expired token")
        if resp.status_code == 404:
            raise NotFoundError(f"Resource not found: {resp.url}")
        if resp.status_code >= 400:
            try:
                body = resp.json()
                msg = body.get("message", resp.text)
            except (ValueError, KeyError):
                msg = resp.text
            raise ApiError(resp.status_code, msg)
        if resp.status_code == 204:
            return None
        return resp.json()

    def get(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        paginate: bool = True,
    ) -> Any:
        """GET request. If paginate=True, fetches all pages."""
        if not paginate:
            resp = self._session.get(self._url(path), params=params)
            return self._handle_response(resp)

        all_results: list[Any] = []
        page = 1
        per_page = 50
        while True:
            p = dict(params or {})
            p["page"] = page
            p["per_page"] = per_page
            resp = self._session.get(self._url(path), params=p)
            data = self._handle_response(resp)
            if not isinstance(data, list):
                return data  # Non-list endpoints don't paginate
            all_results.extend(data)
            if len(data) < per_page:
                break
            page += 1
        return all_results

    def post(self, path: str, json: dict[str, Any] | None = None) -> Any:
        """POST request."""
        resp = self._session.post(self._url(path), json=json)
        return self._handle_response(resp)

    def put(self, path: str, json: dict[str, Any] | None = None) -> Any:
        """PUT request."""
        resp = self._session.put(self._url(path), json=json)
        return self._handle_response(resp)

    def delete(self, path: str) -> Any:
        """DELETE request."""
        resp = self._session.delete(self._url(path))
        return self._handle_response(resp)

    def upload(self, path: str, file_path: str | Path) -> Any:
        """Multipart file upload (PUT)."""
        file_path = Path(file_path)
        with open(file_path, "rb") as f:
            resp = self._session.put(
                self._url(path),
                files={"files": (file_path.name, f)},
            )
        return self._handle_response(resp)

    def download(self, path: str) -> bytes:
        """Download raw bytes."""
        resp = self._session.get(self._url(path))
        if resp.status_code == 401:
            raise AuthenticationError("Invalid or expired token")
        if resp.status_code == 404:
            raise NotFoundError(f"Resource not found: {resp.url}")
        if resp.status_code >= 400:
            raise ApiError(resp.status_code, resp.text)
        return resp.content
