"""Command-line interface for qrcodefyi.

Requires the ``cli`` extra: ``pip install qrcodefyi[cli]``

Usage::

    qrcodefyi search "micro qr"
    qrcodefyi qr-type model-2
    qrcodefyi compare model-1 model-2
    qrcodefyi random
"""

from __future__ import annotations

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(
    name="qrcodefyi",
    help="QR code encyclopedia — look up types, versions, and specs from QRCodeFYI.",
    no_args_is_help=True,
)
console = Console()


@app.command()
def search(
    query: str = typer.Argument(help="Search term (e.g. 'micro qr', 'kanji', 'iso 18004')"),
) -> None:
    """Search across QR types, standards, components, and glossary."""
    from qrcodefyi.api import QRCodeFYI

    with QRCodeFYI() as api:
        results = api.search(query)

    table = Table(title=f"Search: {query}")
    table.add_column("Type", style="cyan", no_wrap=True)
    table.add_column("Name")
    table.add_column("Slug")

    items = results.get("results", [])
    if not items:
        console.print(f"[yellow]No results found for '{query}'[/yellow]")
        return

    for item in items:
        table.add_row(item.get("type", ""), item.get("name", ""), item.get("slug", ""))

    console.print(table)


@app.command("qr-type")
def qr_type(
    slug: str = typer.Argument(help="QR type slug (e.g. 'model-2', 'micro-qr')"),
) -> None:
    """Look up a QR code type with full specifications."""
    from qrcodefyi.api import QRCodeFYI

    with QRCodeFYI() as api:
        data = api.qr_type(slug)

    console.print(f"\n[bold]{data.get('name', slug)}[/bold]")
    if data.get("description"):
        console.print(f"  {data['description'][:200]}")
    console.print()

    table = Table(title="Specifications")
    table.add_column("Property", style="cyan")
    table.add_column("Value")

    specs = [
        ("Year Introduced", data.get("year_introduced")),
        ("Versions", data.get("versions")),
        ("Max Data Capacity", data.get("max_data_capacity")),
        ("Error Correction", data.get("error_correction_levels")),
        ("Encoding Modes", data.get("encoding_modes")),
        ("Module Range", data.get("module_range")),
        ("Standard", data.get("primary_standard")),
    ]
    for label, value in specs:
        if value is not None:
            table.add_row(label, str(value))

    console.print(table)


@app.command()
def compare(
    slug_a: str = typer.Argument(help="First QR type slug"),
    slug_b: str = typer.Argument(help="Second QR type slug"),
) -> None:
    """Compare two QR code types side by side."""
    from qrcodefyi.api import QRCodeFYI

    with QRCodeFYI() as api:
        data = api.compare(slug_a, slug_b)

    a = data.get("a", {})
    b = data.get("b", {})

    table = Table(title=f"{a.get('name', slug_a)} vs {b.get('name', slug_b)}")
    table.add_column("Property", style="cyan")
    table.add_column(a.get("name", slug_a), style="green")
    table.add_column(b.get("name", slug_b), style="yellow")

    fields = [
        ("Year", "year_introduced"),
        ("Versions", "versions"),
        ("Max Capacity", "max_data_capacity"),
        ("Error Correction", "error_correction_levels"),
        ("Encoding Modes", "encoding_modes"),
        ("Module Range", "module_range"),
    ]
    for label, key in fields:
        table.add_row(label, str(a.get(key, "-")), str(b.get(key, "-")))

    console.print(table)


@app.command()
def random() -> None:
    """Discover a random QR code type."""
    from qrcodefyi.api import QRCodeFYI

    with QRCodeFYI() as api:
        data = api.random()

    console.print(f"\n[bold]{data.get('name', 'Unknown')}[/bold]")
    if data.get("description"):
        console.print(f"  {data['description'][:200]}")
    console.print(f"  Year: {data.get('year_introduced', 'N/A')}")
    console.print(f"  Max Capacity: {data.get('max_data_capacity', 'N/A')}")
    console.print(f"  Error Correction: {data.get('error_correction_levels', 'N/A')}")
    console.print()


if __name__ == "__main__":
    app()
