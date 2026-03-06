"""HTTP API client for qrcodefyi.com REST endpoints.

Requires the ``api`` extra: ``pip install qrcodefyi[api]``

Usage::

    from qrcodefyi.api import QRCodeFYI

    with QRCodeFYI() as api:
        results = api.search("micro qr")
        qr_type = api.qr_type("model-2")
        comparison = api.compare("model-1", "model-2")
"""

from __future__ import annotations

from typing import Any

import httpx


class QRCodeFYI:
    """API client for the qrcodefyi.com REST API.

    Provides access to 11 endpoints covering QR code types, versions,
    encoding modes, components, standards, use cases, glossary terms,
    search, comparison, and random discovery.

    Args:
        base_url: API base URL. Defaults to ``https://qrcodefyi.com``.
        timeout: Request timeout in seconds. Defaults to ``10.0``.
    """

    def __init__(
        self,
        base_url: str = "https://qrcodefyi.com",
        timeout: float = 10.0,
    ) -> None:
        self._client = httpx.Client(base_url=base_url, timeout=timeout)

    # -- HTTP helpers ----------------------------------------------------------

    def _get(self, path: str, **params: Any) -> dict[str, Any]:
        resp = self._client.get(path, params={k: v for k, v in params.items() if v is not None})
        resp.raise_for_status()
        result: dict[str, Any] = resp.json()
        return result

    # -- Endpoints -------------------------------------------------------------

    def qr_type(self, slug: str) -> dict[str, Any]:
        """Get QR code type detail with specifications and standards.

        Args:
            slug: QR type URL slug (e.g. ``"model-1"``, ``"model-2"``, ``"micro-qr"``).
        """
        return self._get(f"/api/type/{slug}/")

    def version(self, version: int) -> dict[str, Any]:
        """Get QR version detail with module count and data capacities.

        Args:
            version: QR version number (1-40).
        """
        return self._get(f"/api/version/{version}/")

    def component(self, slug: str) -> dict[str, Any]:
        """Get QR code structural component detail.

        Args:
            slug: Component URL slug (e.g. ``"finder-pattern"``, ``"timing-pattern"``).
        """
        return self._get(f"/api/component/{slug}/")

    def encoding(self, slug: str) -> dict[str, Any]:
        """Get encoding mode detail with character set and capacity.

        Args:
            slug: Encoding mode URL slug
                (e.g. ``"numeric"``, ``"alphanumeric"``, ``"byte"``, ``"kanji"``).
        """
        return self._get(f"/api/encoding/{slug}/")

    def standard(self, slug: str) -> dict[str, Any]:
        """Get QR code standard detail with linked types.

        Args:
            slug: Standard URL slug (e.g. ``"iso-iec-18004"``, ``"ais-gs1"``).
        """
        return self._get(f"/api/standard/{slug}/")

    def use_case(self, slug: str) -> dict[str, Any]:
        """Get QR code use case detail with examples.

        Args:
            slug: Use case URL slug (e.g. ``"mobile-payment"``, ``"wifi-sharing"``).
        """
        return self._get(f"/api/use-case/{slug}/")

    def glossary_term(self, slug: str) -> dict[str, Any]:
        """Get glossary term definition for tooltips and reference.

        Args:
            slug: Term URL slug (e.g. ``"error-correction"``, ``"module"``).
        """
        return self._get(f"/api/term/{slug}/")

    def search(self, query: str) -> dict[str, Any]:
        """Search across QR types, standards, components, and glossary terms.

        Args:
            query: Search term (minimum 2 characters).
        """
        return self._get("/api/search/", q=query)

    def compare(self, slug_a: str, slug_b: str) -> dict[str, Any]:
        """Compare two QR code types side by side.

        Args:
            slug_a: First QR type slug (e.g. ``"model-1"``).
            slug_b: Second QR type slug (e.g. ``"model-2"``).
        """
        return self._get("/api/compare/", a=slug_a, b=slug_b)

    def random(self) -> dict[str, Any]:
        """Get a random QR code type with full detail."""
        return self._get("/api/random/")

    def openapi(self) -> dict[str, Any]:
        """Get the OpenAPI 3.1.0 specification."""
        return self._get("/api/openapi.json")

    # -- Context manager -------------------------------------------------------

    def close(self) -> None:
        """Close the underlying HTTP connection."""
        self._client.close()

    def __enter__(self) -> QRCodeFYI:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
