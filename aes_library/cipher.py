"""Simple AES-256 EAX wrapper for text encryption and decryption."""

import json
from typing import Optional

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

from .key import derive_key, generate_salt
from .utils import decode_base64, encode_base64, ensure_bytes, ensure_text


class AESCipher:
    """Reusable wrapper around AES-256 EAX encryption."""

    def __init__(self, password: str, salt: Optional[bytes] = None, iterations: int = 100_000):
        """Initialize the cipher with a password and optional custom salt.

        Args:
            password: User-provided password.
            salt: Optional custom salt. A new random salt is generated when
                omitted.
            iterations: PBKDF2 iteration count.
        """
        if not isinstance(password, str) or not password.strip():
            raise ValueError("Password must be a non-empty string.")
        if salt is None:
            salt = generate_salt()
        if not isinstance(salt, (bytes, bytearray)) or len(salt) == 0:
            raise ValueError("Salt must be a non-empty bytes-like object.")
        if not isinstance(iterations, int) or iterations <= 0:
            raise ValueError("Iterations must be a positive integer.")

        self.password = password
        self.salt = bytes(salt)
        self.iterations = iterations
        self.key = derive_key(password, self.salt, iterations=iterations, key_length=32)

    def encrypt(self, plaintext: str) -> str:
        """Encrypt plaintext and return it as a Base64-encoded payload."""
        if not isinstance(plaintext, str):
            raise TypeError("Plaintext must be a string.")

        nonce = get_random_bytes(16)
        cipher = AES.new(self.key, AES.MODE_EAX, nonce=nonce)
        ciphertext, tag = cipher.encrypt_and_digest(ensure_bytes(plaintext))

        payload = {
            "salt": encode_base64(self.salt),
            "nonce": encode_base64(nonce),
            "tag": encode_base64(tag),
            "ciphertext": encode_base64(ciphertext),
        }
        payload_bytes = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
        return encode_base64(payload_bytes)

    def decrypt(self, encrypted_payload: str) -> str:
        """Decrypt a Base64-encoded payload created by ``encrypt``."""
        if not isinstance(encrypted_payload, str) or not encrypted_payload.strip():
            raise ValueError("Encrypted payload must be a non-empty string.")

        try:
            payload_bytes = decode_base64(encrypted_payload)
            payload = json.loads(payload_bytes.decode("utf-8"))
        except (ValueError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Encrypted payload is malformed.") from exc

        required_fields = {"salt", "nonce", "tag", "ciphertext"}
        if not required_fields.issubset(payload.keys()):
            raise ValueError("Encrypted payload is missing required fields.")

        try:
            salt = decode_base64(payload["salt"])
            nonce = decode_base64(payload["nonce"])
            tag = decode_base64(payload["tag"])
            ciphertext = decode_base64(payload["ciphertext"])
        except (TypeError, ValueError) as exc:
            raise ValueError("Encrypted payload contains invalid field values.") from exc

        key = derive_key(self.password, salt, iterations=self.iterations, key_length=32)
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        try:
            plaintext_bytes = cipher.decrypt_and_verify(ciphertext, tag)
        except ValueError as exc:
            raise ValueError("Authentication failed: payload may be corrupted or tampered with.") from exc
        return ensure_text(plaintext_bytes)
