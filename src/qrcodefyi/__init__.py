"""qrcodefyi — QR code encyclopedia API client for developers.

Look up QR code types, versions 1-40, encoding modes, error correction levels,
standards, and components from QRCodeFYI.

Usage::

    from qrcodefyi.api import QRCodeFYI

    with QRCodeFYI() as api:
        results = api.search("micro qr")
        print(results)
"""

__version__ = "0.1.0"
