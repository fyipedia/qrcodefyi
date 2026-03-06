"""MCP server for qrcodefyi — QR code reference tools for AI assistants.

Requires the ``mcp`` extra: ``pip install qrcodefyi[mcp]``

Run as a standalone server::

    python -m qrcodefyi.mcp_server

Or configure in ``claude_desktop_config.json``::

    {
        "mcpServers": {
            "qrcodefyi": {
                "command": "python",
                "args": ["-m", "qrcodefyi.mcp_server"]
            }
        }
    }
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("qrcodefyi")


@mcp.tool()
def qrcode_search(query: str) -> str:
    """Search for QR code types, standards, and terminology on QRCodeFYI.

    Search across QR code formats (Model 1, Model 2, Micro QR, rMQR),
    standards (ISO/IEC 18004), encoding modes, components, and glossary terms.

    Args:
        query: Search term (e.g. "micro qr", "kanji", "error correction", "finder pattern").
    """
    from qrcodefyi.api import QRCodeFYI

    with QRCodeFYI() as api:
        results = api.search(query)

    items = results.get("results", [])
    if not items:
        return f"No results found for '{query}'."

    lines = [
        f"## QR Code Search: {query}",
        "",
        f"Found {len(items)} result(s):",
        "",
        "| Type | Name | Slug |",
        "|------|------|------|",
    ]

    for item in items:
        row = f"| {item.get('type', '')} | {item.get('name', '')} | {item.get('slug', '')} |"
        lines.append(row)

    return "\n".join(lines)


@mcp.tool()
def qrcode_lookup(slug: str) -> str:
    """Look up a specific QR code type by slug.

    Returns full specifications including versions, encoding modes,
    error correction levels, module sizes, and related standards.

    Args:
        slug: QR type slug (e.g. "model-2", "micro-qr", "rmqr", "iqr-code").
    """
    from qrcodefyi.api import QRCodeFYI

    with QRCodeFYI() as api:
        data = api.qr_type(slug)

    lines = [
        f"## {data.get('name', slug)}",
        "",
        data.get("description", ""),
        "",
        f"- **Year Introduced**: {data.get('year_introduced', 'N/A')}",
        f"- **Versions**: {data.get('versions', 'N/A')}",
        f"- **Max Data Capacity**: {data.get('max_data_capacity', 'N/A')}",
        f"- **Error Correction**: {data.get('error_correction_levels', 'N/A')}",
        f"- **Encoding Modes**: {data.get('encoding_modes', 'N/A')}",
        f"- **Module Range**: {data.get('module_range', 'N/A')}",
    ]

    standards = data.get("standards", [])
    if standards:
        lines.append("")
        lines.append("### Standards")
        for st in standards:
            lines.append(f"- {st.get('name', '')} ({st.get('issuing_body', '')})")

    return "\n".join(lines)


@mcp.tool()
def qrcode_compare(slug_a: str, slug_b: str) -> str:
    """Compare two QR code types side by side.

    Args:
        slug_a: First QR type slug (e.g. "model-1").
        slug_b: Second QR type slug (e.g. "model-2").
    """
    from qrcodefyi.api import QRCodeFYI

    with QRCodeFYI() as api:
        data = api.compare(slug_a, slug_b)

    a = data.get("a", {})
    b = data.get("b", {})

    lines = [
        f"## {a.get('name', slug_a)} vs {b.get('name', slug_b)}",
        "",
        "| Property | " + a.get("name", slug_a) + " | " + b.get("name", slug_b) + " |",
        "|----------|"
        + "-" * len(a.get("name", slug_a))
        + "--|"
        + "-" * len(b.get("name", slug_b))
        + "--|",
    ]

    fields = [
        ("Year", "year_introduced"),
        ("Versions", "versions"),
        ("Max Capacity", "max_data_capacity"),
        ("Error Correction", "error_correction_levels"),
        ("Encoding Modes", "encoding_modes"),
        ("Module Range", "module_range"),
    ]
    for label, key in fields:
        lines.append(f"| {label} | {a.get(key, '-')} | {b.get(key, '-')} |")

    return "\n".join(lines)


if __name__ == "__main__":
    mcp.run()
