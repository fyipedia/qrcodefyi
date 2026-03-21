"""MCP server for qrcodefyi — AI assistant tools for qrcodefyi.com.

Run: uvx --from "qrcodefyi[mcp]" python -m qrcodefyi.mcp_server
"""
from __future__ import annotations

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("QRCodeFYI")


@mcp.tool()
def list_encoding_modes(limit: int = 20, offset: int = 0) -> str:
    """List encoding_modes from qrcodefyi.com.

    Args:
        limit: Maximum number of results. Default 20.
        offset: Number of results to skip. Default 0.
    """
    from qrcodefyi.api import QRCodeFYI

    with QRCodeFYI() as api:
        data = api.list_encoding_modes(limit=limit, offset=offset)
        results = data.get("results", data) if isinstance(data, dict) else data
        if not results:
            return "No encoding_modes found."
        items = results[:limit] if isinstance(results, list) else []
        return "\n".join(f"- {item.get('name', item.get('slug', '?'))}" for item in items)


@mcp.tool()
def get_encoding_mode(slug: str) -> str:
    """Get detailed information about a specific encoding_mode.

    Args:
        slug: URL slug identifier for the encoding_mode.
    """
    from qrcodefyi.api import QRCodeFYI

    with QRCodeFYI() as api:
        data = api.get_encoding_mode(slug)
        return str(data)


@mcp.tool()
def list_standards(limit: int = 20, offset: int = 0) -> str:
    """List standards from qrcodefyi.com.

    Args:
        limit: Maximum number of results. Default 20.
        offset: Number of results to skip. Default 0.
    """
    from qrcodefyi.api import QRCodeFYI

    with QRCodeFYI() as api:
        data = api.list_standards(limit=limit, offset=offset)
        results = data.get("results", data) if isinstance(data, dict) else data
        if not results:
            return "No standards found."
        items = results[:limit] if isinstance(results, list) else []
        return "\n".join(f"- {item.get('name', item.get('slug', '?'))}" for item in items)


@mcp.tool()
def search_qrcode(query: str) -> str:
    """Search qrcodefyi.com for QR code encoding modes, standards, and components.

    Args:
        query: Search query string.
    """
    from qrcodefyi.api import QRCodeFYI

    with QRCodeFYI() as api:
        data = api.search(query)
        results = data.get("results", data) if isinstance(data, dict) else data
        if not results:
            return f"No results found for \"{query}\"."
        items = results[:10] if isinstance(results, list) else []
        return "\n".join(f"- {item.get('name', item.get('slug', '?'))}" for item in items)


def main() -> None:
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
