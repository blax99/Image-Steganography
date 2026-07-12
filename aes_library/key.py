"""Password-based key derivation helpers.

Purpose
-------
Generate cryptographically strong salts and derive AES-256 keys from user
passwords using PBKDF2-HMAC-SHA256.

Input
-----
- password: non-empty plain-text password string
- salt: byte sequence used as the PBKDF2 salt
- iterations: number of PBKDF2 iterations (default 100_000)
- key_length: derived key size in bytes (default 32 for AES-256)

Output
------
- random salt bytes for a new encryption operation
- a derived AES key in bytes

Algorithm explanation
--------------------
1. A random salt is created with ``Crypto.Random.get_random_bytes``.
2. The password and salt are passed into PBKDF2-HMAC-SHA256.
3. The produced bytes are used as the AES-256 key material.

Time complexity
---------------
- ``generate_salt``: O(1) for the requested length
- ``derive_key``: O(iterations * key_length)

Flow diagram
------------
Password -> PBKDF2-HMAC-SHA256 -> AES key

Example usage
-------------
>>> from aes_library.key import derive_key, generate_salt
>>> salt = generate_salt()
>>> key = derive_key("my-password", salt)
"""

from typing import Optional

from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes


def generate_salt(length: int = 16) -> bytes:
    """Create a random salt of the requested byte length.

    Args:
        length: Number of random bytes to generate.

    Returns:
        Random salt bytes.

    Raises:
        ValueError: If the requested length is invalid.
    """
    if not isinstance(length, int) or length <= 0:
        raise ValueError("Salt length must be a positive integer.")
    return get_random_bytes(length)


def derive_key(
    password: str,
    salt: bytes,
    iterations: int = 100_000,
    key_length: int = 32,
) -> bytes:
    """Derive an AES key from a password and salt using PBKDF2.

    Args:
        password: Human-readable password supplied by the user.
        salt: Random bytes used as PBKDF2 salt.
        iterations: Number of PBKDF2 iterations. Higher values improve safety.
        key_length: Length of the derived key in bytes.

    Returns:
        PBKDF2-derived key bytes suitable for AES-256.

    Raises:
        ValueError: If the inputs are invalid.
    """
    if not isinstance(password, str) or not password.strip():
        raise ValueError("Password must be a non-empty string.")
    if not isinstance(salt, (bytes, bytearray)) or len(salt) == 0:
        raise ValueError("Salt must be a non-empty bytes-like object.")
    if not isinstance(iterations, int) or iterations <= 0:
        raise ValueError("Iterations must be a positive integer.")
    if not isinstance(key_length, int) or key_length <= 0:
        raise ValueError("Key length must be a positive integer.")

    password_bytes = password.encode("utf-8")
    return PBKDF2(
        password_bytes,
        salt,
        dkLen=key_length,
        count=iterations,
        hmac_hash_module=SHA256,
    )
