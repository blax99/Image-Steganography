"""Reusable AES-256 encryption helpers for Django projects.

Purpose
-------
Expose a small, reusable API for encrypting and decrypting text payloads
using AES-256 in EAX mode with a password-derived key.

Why this module exists
----------------------
This package keeps encryption logic separate from Django views so the
application can reuse the same logic in forms, views, or future services.
"""

from .cipher import AESCipher
from .key import derive_key, generate_salt
from .utils import decode_base64, encode_base64, ensure_bytes, ensure_text

__all__ = [
    "AESCipher",
    "derive_key",
    "generate_salt",
    "encode_base64",
    "decode_base64",
    "ensure_bytes",
    "ensure_text",
]
