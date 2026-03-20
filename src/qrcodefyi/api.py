"""HTTP API client for qrcodefyi.com REST endpoints.

Requires the ``api`` extra: ``pip install qrcodefyi[api]``

Usage::

    from qrcodefyi.api import QRCodeFYI

    with QRCodeFYI() as api:
        items = api.list_components()
        detail = api.get_component("example-slug")
        results = api.search("query")
"""

from __future__ import annotations

from typing import Any

import httpx


class QRCodeFYI:
    """API client for the qrcodefyi.com REST API.

    Provides typed access to all qrcodefyi.com endpoints including
    list, detail, and search operations.

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

    def _get(self, path: str, **params: Any) -> dict[str, Any]:
        resp = self._client.get(
            path,
            params={k: v for k, v in params.items() if v is not None},
        )
        resp.raise_for_status()
        result: dict[str, Any] = resp.json()
        return result

    # -- Endpoints -----------------------------------------------------------

    def list_comparisons(self, **params: Any) -> dict[str, Any]:
        """List all comparisons."""
        return self._get("/api/v1/comparisons/", **params)

    def get_comparison(self, slug: str) -> dict[str, Any]:
        """Get comparison by slug."""
        return self._get(f"/api/v1/comparisons/" + slug + "/")

    def list_components(self, **params: Any) -> dict[str, Any]:
        """List all components."""
        return self._get("/api/v1/components/", **params)

    def get_component(self, slug: str) -> dict[str, Any]:
        """Get component by slug."""
        return self._get(f"/api/v1/components/" + slug + "/")

    def list_encoding_modes(self, **params: Any) -> dict[str, Any]:
        """List all encoding modes."""
        return self._get("/api/v1/encoding-modes/", **params)

    def get_encoding_mode(self, slug: str) -> dict[str, Any]:
        """Get encoding mode by slug."""
        return self._get(f"/api/v1/encoding-modes/" + slug + "/")

    def list_faqs(self, **params: Any) -> dict[str, Any]:
        """List all faqs."""
        return self._get("/api/v1/faqs/", **params)

    def get_faq(self, slug: str) -> dict[str, Any]:
        """Get faq by slug."""
        return self._get(f"/api/v1/faqs/" + slug + "/")

    def list_glossary(self, **params: Any) -> dict[str, Any]:
        """List all glossary."""
        return self._get("/api/v1/glossary/", **params)

    def get_term(self, slug: str) -> dict[str, Any]:
        """Get term by slug."""
        return self._get(f"/api/v1/glossary/" + slug + "/")

    def list_guides(self, **params: Any) -> dict[str, Any]:
        """List all guides."""
        return self._get("/api/v1/guides/", **params)

    def get_guide(self, slug: str) -> dict[str, Any]:
        """Get guide by slug."""
        return self._get(f"/api/v1/guides/" + slug + "/")

    def list_recipes(self, **params: Any) -> dict[str, Any]:
        """List all recipes."""
        return self._get("/api/v1/recipes/", **params)

    def get_recipe(self, slug: str) -> dict[str, Any]:
        """Get recipe by slug."""
        return self._get(f"/api/v1/recipes/" + slug + "/")

    def list_scan_scenarios(self, **params: Any) -> dict[str, Any]:
        """List all scan scenarios."""
        return self._get("/api/v1/scan-scenarios/", **params)

    def get_scan_scenario(self, slug: str) -> dict[str, Any]:
        """Get scan scenario by slug."""
        return self._get(f"/api/v1/scan-scenarios/" + slug + "/")

    def list_standards(self, **params: Any) -> dict[str, Any]:
        """List all standards."""
        return self._get("/api/v1/standards/", **params)

    def get_standard(self, slug: str) -> dict[str, Any]:
        """Get standard by slug."""
        return self._get(f"/api/v1/standards/" + slug + "/")

    def list_tools(self, **params: Any) -> dict[str, Any]:
        """List all tools."""
        return self._get("/api/v1/tools/", **params)

    def get_tool(self, slug: str) -> dict[str, Any]:
        """Get tool by slug."""
        return self._get(f"/api/v1/tools/" + slug + "/")

    def list_types(self, **params: Any) -> dict[str, Any]:
        """List all types."""
        return self._get("/api/v1/types/", **params)

    def get_type(self, slug: str) -> dict[str, Any]:
        """Get type by slug."""
        return self._get(f"/api/v1/types/" + slug + "/")

    def list_use_cases(self, **params: Any) -> dict[str, Any]:
        """List all use cases."""
        return self._get("/api/v1/use-cases/", **params)

    def get_use_case(self, slug: str) -> dict[str, Any]:
        """Get use case by slug."""
        return self._get(f"/api/v1/use-cases/" + slug + "/")

    def list_versions(self, **params: Any) -> dict[str, Any]:
        """List all versions."""
        return self._get("/api/v1/versions/", **params)

    def get_version(self, slug: str) -> dict[str, Any]:
        """Get version by slug."""
        return self._get(f"/api/v1/versions/" + slug + "/")

    def search(self, query: str, **params: Any) -> dict[str, Any]:
        """Search across all content."""
        return self._get(f"/api/v1/search/", q=query, **params)

    # -- Lifecycle -----------------------------------------------------------

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._client.close()

    def __enter__(self) -> QRCodeFYI:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
