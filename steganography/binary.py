"""Binary conversion helpers for text payloads.

Purpose
-------
Convert UTF-8 text to and from binary strings so the LSB embedder can store
payload bits in image pixels.

Input
-----
- plain text string for ``text_to_bits``
- binary string for ``bits_to_text``

Output
------
- binary string representation of the text
- UTF-8 text reconstructed from binary bits

Algorithm explanation
--------------------
The converter splits each character into 8-bit ASCII values and joins them
into a string of zeros and ones. The reverse operation groups the bits into
8-bit chunks and converts them back to characters.

Time complexity
---------------
- ``text_to_bits``: O(n)
- ``bits_to_text``: O(n)

Flow diagram
------------
Text -> 8-bit ASCII -> binary string -> image bits -> binary string -> text

Example usage
-------------
>>> from steganography.binary import BinaryConverter
>>> converter = BinaryConverter()
>>> bits = converter.text_to_bits("hi")
>>> converter.bits_to_text(bits)
'hi'
"""

from typing import Final


class BinaryConverter:
    """Convert between text and binary strings."""

    @staticmethod
    def text_to_bits(text: str) -> str:
        """Convert UTF-8 text into a binary string of 8-bit values."""
        if not isinstance(text, str):
            raise TypeError("Text must be a string.")
        if not text:
            return ""
        return "".join(format(ord(char), "08b") for char in text)

    @staticmethod
    def bits_to_text(bits: str) -> str:
        """Convert a binary string into UTF-8 text."""
        if not isinstance(bits, str):
            raise TypeError("Bits must be provided as a string.")
        if len(bits) % 8 != 0:
            raise ValueError("Binary payload must contain a multiple of 8 bits.")
        if not bits:
            return ""
        characters = []
        for index in range(0, len(bits), 8):
            chunk = bits[index:index + 8]
            characters.append(chr(int(chunk, 2)))
        return "".join(characters)
