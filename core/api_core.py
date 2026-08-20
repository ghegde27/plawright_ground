from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    import requests


class ApiCore:
    """Small requests wrapper for API tests."""

    def __init__(
            self,
            base_url: str,
            default_headers: dict[str, str] | None = None,
            timeout: int = 15,
    ):
        self.base_url = base_url.rstrip("/")
        self.default_headers = default_headers or {}
        self.timeout = timeout
        self.session = self._requests().Session()

    def get(
            self,
            path: str = "",
            params: dict[str, Any] | None = None,
            headers: dict[str, str] | None = None,
    ) -> requests.Response:
        response = self.session.get(
            self._url(path),
            params=params,
            headers=self._headers(headers),
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response

    def post(
            self,
            path: str = "",
            json: dict[str, Any] | list[Any] | None = None,
            headers: dict[str, str] | None = None,
    ) -> requests.Response:
        response = self.session.post(
            self._url(path),
            json=json,
            headers=self._headers(headers),
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response

    def _url(self, path: str) -> str:
        if path.startswith("http://") or path.startswith("https://"):
            return path
        return f"{self.base_url}/{path.lstrip('/')}" if path else self.base_url

    def _headers(self, headers: dict[str, str] | None = None) -> dict[str, str]:
        return {**self.default_headers, **(headers or {})}

    @staticmethod
    def _requests():
        try:
            import requests
        except ImportError as error:
            raise RuntimeError("Install the 'requests' package to use ApiCore.") from error
        return requests


def print_json_structure(data: Any, indent: int = 0) -> None:
    prefix = " " * indent

    if isinstance(data, dict):
        for key, value in data.items():
            print(f"{prefix}{key}: {type(value).__name__}")
            print_json_structure(value, indent + 4)
    elif isinstance(data, list):
        print(f"{prefix}List[{len(data)}]")
        if data:
            print_json_structure(data[0], indent + 4)
    else:
        print(f"{prefix}{data!r}")
