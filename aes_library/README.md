# aes_library

## Purpose
This package provides a reusable AES-256 encryption API for Django applications. It keeps cryptographic logic separate from the web layer so the same code can be reused in views, services, and future automation.

## Module overview

### __init__.py
- Purpose: Export the public API of the package.
- Functions: Re-exports `AESCipher`, `derive_key`, `generate_salt`, and the Base64 helpers.
- Input: None.
- Output: Public symbols for the package.
- Algorithm explanation: Simple import re-export layer.
- Time complexity: O(1).
- Flow diagram:
  ```text
  Package import -> export public classes/functions
  ```
- Example usage:
  ```python
  from aes_library import AESCipher
  cipher = AESCipher("secret")
  ```

### cipher.py
- Purpose: Encrypt and decrypt text using AES-256 in EAX mode.
- Functions:
  - `AESCipher.__init__`
  - `AESCipher.encrypt`
  - `AESCipher.decrypt`
- Input: password string, plaintext string, encrypted payload string.
- Output: Base64-encoded encrypted payload and decrypted plaintext.
- Algorithm explanation: Password -> PBKDF2 key -> random nonce -> EAX encryption -> Base64 payload.
- Time complexity: O(n) for encryption and decryption.
- Flow diagram:
  ```text
  Password -> PBKDF2 -> AES key -> EAX encrypt -> Base64 payload
  ```
- Example usage:
  ```python
  from aes_library import AESCipher
  cipher = AESCipher("secret")
  payload = cipher.encrypt("hello")
  plain = cipher.decrypt(payload)
  ```

### key.py
- Purpose: Derive AES keys from passwords and generate salts.
- Functions:
  - `generate_salt`
  - `derive_key`
- Input: password, salt, iteration count, target key length.
- Output: random salt bytes and derived AES key bytes.
- Algorithm explanation: Use PBKDF2-HMAC-SHA256 to derive the AES key.
- Time complexity: O(iterations * key_length).
- Flow diagram:
  ```text
  Password + salt -> PBKDF2-HMAC-SHA256 -> AES key
  ```
- Example usage:
  ```python
  from aes_library.key import derive_key, generate_salt
  salt = generate_salt()
  key = derive_key("secret", salt)
  ```

### utils.py
- Purpose: Provide byte/string and Base64 conversion helpers.
- Functions:
  - `encode_base64`
  - `decode_base64`
  - `ensure_bytes`
  - `ensure_text`
- Input: strings and bytes.
- Output: bytes, strings, and Base64 text.
- Algorithm explanation: Wrap Python base64 and UTF-8 helpers for consistent serialization.
- Time complexity: O(n).
- Flow diagram:
  ```text
  string/bytes -> encode/decode -> UTF-8 or Base64
  ```
- Example usage:
  ```python
  from aes_library.utils import encode_base64, decode_base64
  encoded = encode_base64(b"hello")
  decoded = decode_base64(encoded)
  ```
