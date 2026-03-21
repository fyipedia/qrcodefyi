# qrcodefyi

[![PyPI version](https://agentgif.com/badge/pypi/qrcodefyi/version.svg)](https://pypi.org/project/qrcodefyi/)
[![Python](https://img.shields.io/pypi/pyversions/qrcodefyi)](https://pypi.org/project/qrcodefyi/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

QR code encyclopedia API client for Python. Look up QR code types, versions 1-40, encoding modes, error correction levels, structural components, and standards from [QRCodeFYI](https://qrcodefyi.com) -- the comprehensive QR code reference covering Model 1, Model 2, Micro QR, rMQR, and every major QR variant in use today.

> **Explore QR codes at [qrcodefyi.com](https://qrcodefyi.com)** -- [Type Explorer](https://qrcodefyi.com/type/) | [Standards Reference](https://qrcodefyi.com/standard/) | | [Encoding Modes](https://qrcodefyi.com/encoding/)

## Install

```bash
pip install qrcodefyi[api]     # API client (httpx)
pip install qrcodefyi[cli]     # + CLI (typer, rich)
pip install qrcodefyi[mcp]     # + MCP server
pip install qrcodefyi[all]     # Everything
```

## Quick Start

```python
from qrcodefyi.api import QRCodeFYI

with QRCodeFYI() as api:
    # Search types, standards, components, glossary
    results = api.search("micro qr")
    print(results)

    # Look up a specific QR type
    model2 = api.qr_type("model-2")
    print(model2["name"], model2["year_introduced"])

    # Get version details (1-40)
    v10 = api.version(10)
    print(v10["modules"], v10["data_capacity"])

    # Compare two QR types
    diff = api.compare("model-1", "model-2")
    print(diff)

    # Discover a random QR type
    surprise = api.random()
    print(surprise["name"])
```

## What You'll Find on QRCodeFYI

QRCodeFYI is a comprehensive QR code encyclopedia covering every QR variant, all 40 versions, 4 encoding modes, 4 error correction levels, structural components, and governing standards. QR codes (Quick Response codes) are two-dimensional matrix barcodes invented by Denso Wave in 1994, now the most widely deployed 2D symbology in the world -- used for mobile payments, product tracking, WiFi sharing, digital menus, and billions of consumer interactions daily.

### QR Code Types

| Type | Year | Versions | Max Capacity |
|------|------|----------|--------------|
| QR Code Model 1 | 1992 | 1-14 | 1,167 numerics |
| QR Code Model 2 | 1997 | 1-40 | 7,089 numerics |
| Micro QR Code | 2004 | M1-M4 | 35 numerics |
| rMQR (Rectangular Micro QR) | 2022 | R7x43-R17x139 | 361 numerics |
| iQR Code | 2008 | 1-61 | 40,637 numerics |
| SQRC | 2007 | -- | Encrypted data |
| Frame QR | 2014 | -- | Canvas area for graphics |

### QR Code Versions (1-40)

Every QR Code Model 2 has a version number from 1 to 40 that determines its physical size. Version 1 is a 21x21 module grid; each subsequent version adds 4 modules per side, so Version 40 is a 177x177 module grid with 31,329 total modules. Higher versions encode more data but require more physical space and higher print resolution.

### Error Correction Levels

| Level | Recovery | Use Case |
|-------|----------|----------|
| L (Low) | ~7% | Clean environments, maximum data capacity |
| M (Medium) | ~15% | General purpose, default for most applications |
| Q (Quartile) | ~25% | Industrial environments, moderate damage expected |
| H (High) | ~30% | Harsh conditions, logos embedded in QR code |

QR codes use Reed-Solomon error correction. Higher levels increase redundancy at the cost of data capacity -- a Version 10 QR code holds 652 numeric characters at Level L but only 346 at Level H.

### Encoding Modes

| Mode | Character Set | Bits/Char | Example Use |
|------|---------------|-----------|-------------|
| Numeric | 0-9 | 3.33 | Phone numbers, product IDs |
| Alphanumeric | 0-9, A-Z, space, $%*+-./: | 5.5 | URLs, serial numbers |
| Byte (ISO 8859-1) | Full 8-bit | 8 | UTF-8 text, binary data |
| Kanji (Shift JIS) | JIS X 0208 | 13 | Japanese text |

Mixed-mode encoding allows a single QR code to switch between modes within the data stream, optimizing capacity by using the most efficient encoding for each segment.

### QR Code Structure

Every QR code contains mandatory structural components: finder patterns (three large squares at corners for orientation detection), timing patterns (alternating black/white modules for coordinate mapping), alignment patterns (smaller squares for distortion correction in Version 2+), format information (error correction level and mask pattern), and version information (encoded in Version 7+ codes). The data area fills the remaining modules using one of 8 mask patterns to ensure optimal readability.

Learn more: | [Version Explorer](https://qrcodefyi.com/version/)

## API Endpoints

Free, no authentication required. JSON responses with CORS enabled.

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/type/{slug}/` | QR code type detail with specs |
| GET | `/api/version/{version}/` | QR version detail (1-40) |
| GET | `/api/component/{slug}/` | Structural component detail |
| GET | `/api/encoding/{slug}/` | Encoding mode detail |
| GET | `/api/standard/{slug}/` | Standard detail with linked types |
| GET | `/api/use-case/{slug}/` | Use case detail with examples |
| GET | `/api/term/{slug}/` | Glossary term definition |
| GET | `/api/search/?q={query}` | Search across all content types |
| GET | `/api/compare/?a={slug}&b={slug}` | Compare two QR types |
| GET | `/api/random/` | Random QR type discovery |
| GET | `/api/openapi.json` | OpenAPI 3.1.0 specification |

```bash
# Example: search for micro QR formats
curl -s "https://qrcodefyi.com/api/search/?q=micro+qr" | python -m json.tool
```

## Command-Line Interface

```bash
qrcodefyi search "micro qr"
qrcodefyi qr-type model-2
qrcodefyi compare model-1 model-2
qrcodefyi random
```

## MCP Server (Claude, Cursor, Windsurf)

```json
{
    "mcpServers": {
        "qrcodefyi": {
            "command": "python",
            "args": ["-m", "qrcodefyi.mcp_server"]
        }
    }
}
```

Tools: `qrcode_search`, `qrcode_lookup`, `qrcode_compare`

## API Client

```python
from qrcodefyi.api import QRCodeFYI

with QRCodeFYI() as api:
    # All 11 endpoints
    api.search("micro qr")
    api.qr_type("model-2")
    api.version(10)
    api.component("finder-pattern")
    api.encoding("numeric")
    api.standard("iso-iec-18004")
    api.use_case("mobile-payment")
    api.glossary_term("error-correction")
    api.compare("model-1", "model-2")
    api.random()
    api.openapi()
```

## Also Available

| Language | Package | Install |
|----------|---------|---------|
| Python | [qrcodefyi](https://pypi.org/project/qrcodefyi/) | `pip install qrcodefyi` |
| TypeScript | [qrcodefyi](https://www.npmjs.com/package/qrcodefyi) | `npm install qrcodefyi` |
| Go | [qrcodefyi-go](https://pkg.go.dev/github.com/fyipedia/qrcodefyi-go) | `go get github.com/fyipedia/qrcodefyi-go` |
| Rust | [qrcodefyi](https://crates.io/crates/qrcodefyi) | `cargo add qrcodefyi` |
| Ruby | [qrcodefyi](https://rubygems.org/gems/qrcodefyi) | `gem install qrcodefyi` |

## Code FYI Family

| Site | Domain | Focus |
|------|--------|-------|
| QRCodeFYI | [qrcodefyi.com](https://qrcodefyi.com) | QR code types & encoding |
| BarcodeFYI | [barcodefyi.com](https://barcodefyi.com) | Barcode symbologies & standards |
| NFCFYI | [nfcfyi.com](https://nfcfyi.com) | NFC tags & NDEF records |
| BLEFYI | [blefyi.com](https://blefyi.com) | Bluetooth Low Energy profiles |
| RFIDFYI | [rfidfyi.com](https://rfidfyi.com) | RFID tags & frequency bands |
| SmartCardFYI | [smartcardfyi.com](https://smartcardfyi.com) | Smart card types & platforms |

## License

MIT
