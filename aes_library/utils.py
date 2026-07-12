"""Utility helpers for serialization and text conversion.

Purpose
-------
Provide small helper functions for encoding/decoding Base64 data and for
converting between strings and bytes.

Input
-----
- plain text or bytes-like values
- Base64 data represented as ASCII strings

Output
------
- UTF-8 encoded bytes
- UTF-8 decoded strings
- Base64-encoded ASCII strings

Algorithm explanation
--------------------
The helpers wrap Python's standard library Base64 implementation and UTF-8
encoding/decoding so the rest of the encryption API can stay consistent.

Time complexity
---------------
- All helpers are O(n), where n is the size of the input bytes.

Flow diagram
------------
bytes/string -> UTF-8 encode/decode or base64 encode/decode

Example usage
-------------
>>> from aes_library.utils import encode_base64, decode_base64
>>> encoded = encode_base64(b"hello")
>>> decoded = decode_base64(encoded)
"""

import base64
from typing import Union


def encode_base64(data: bytes) -> str:
    """Encode bytes into a Base64 ASCII string."""
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("Data must be bytes-like.")
    return base64.b64encode(bytes(data)).decode("ascii")


def decode_base64(value: str) -> bytes:
    """Decode a Base64 ASCII string into bytes."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Base64 value must be a non-empty string.")
    try:
        return base64.b64decode(value.encode("ascii"))
    except (ValueError, UnicodeEncodeError) as exc:
        raise ValueError("Invalid Base64 payload.") from exc


def ensure_bytes(value: str) -> bytes:
    """Convert a UTF-8 string into bytes."""
    if not isinstance(value, str):
        raise TypeError("Expected a string value.")
    return value.encode("utf-8")


def ensure_text(value: bytes) -> str:
    """Convert UTF-8 bytes into a string."""
    if not isinstance(value, (bytes, bytearray)):
        raise TypeError("Expected bytes-like data.")
    return bytes(value).decode("utf-8")
