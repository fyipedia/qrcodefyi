"""Tests for qrcodefyi API client."""

from __future__ import annotations

from qrcodefyi.api import QRCodeFYI


def test_client_init() -> None:
    client = QRCodeFYI()
    assert client._client.base_url == "https://qrcodefyi.com"
    client.close()


def test_client_custom_base_url() -> None:
    client = QRCodeFYI(base_url="https://test.example.com")
    assert client._client.base_url == "https://test.example.com"
    client.close()


def test_client_context_manager() -> None:
    with QRCodeFYI() as api:
        assert api._client.base_url == "https://qrcodefyi.com"


def test_version() -> None:
    from qrcodefyi import __version__

    assert __version__ == "0.1.0"
