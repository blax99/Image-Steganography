"""Extract a hidden UTF-8 message from an image using the LSB algorithm.

Purpose
-------
Read the least significant bits from image pixels and reconstruct a message.

Input
-----
- image path pointing to an existing image file

Output
------
- the extracted UTF-8 message string

Algorithm explanation
--------------------
1. Read the least significant bit of each RGB channel in each pixel.
2. Assemble the bits into a stream.
3. Read the first 32 bits to determine the message length.
4. Read the next length * 8 bits and decode them into UTF-8 text.

Time complexity
---------------
- O(width * height) because every pixel contributes a constant number of bits.

Flow diagram
------------
PNG image -> read pixel LSBs -> 32-bit length header -> payload bits -> text

Example usage
-------------
>>> from steganography.extract import LSBExtractor
>>> extractor = LSBExtractor()
>>> text = extractor.extract_text("output.png")
"""

from PIL import Image

from .binary import BinaryConverter
from .image_utils import prepare_image, validate_image
from .pixel import PixelBitHandler


class LSBExtractor:
    """Read text that was hidden in an image via the LSB algorithm."""

    def __init__(self, converter=None):
        self.converter = converter or BinaryConverter()
        self.handler = PixelBitHandler()

    def extract_text(self, image_path: str) -> str:
        """Extract the hidden UTF-8 message from an image file."""
        if not isinstance(image_path, str) or not image_path.strip():
            raise ValueError("Image path must be a non-empty string.")

        validate_image(image_path)
        image = prepare_image(image_path)
        pixels = image.load()

        bit_buffer = []
        for y in range(image.height):
            for x in range(image.width):
                pixel = list(pixels[x, y])
                for channel in pixel:
                    bit_buffer.append(self.handler.get_lsb(channel))

        if len(bit_buffer) < 32:
            raise ValueError("The image does not contain enough bits for a valid message header.")

        header_bits = "".join(bit_buffer[:32])
        try:
            message_length = int(header_bits, 2)
        except ValueError as exc:
            raise ValueError("The image contains an invalid message length header.") from exc

        if message_length <= 0:
            raise ValueError("The message length header is invalid.")

        payload_bits = "".join(bit_buffer[32:32 + message_length * 8])
        if len(payload_bits) != message_length * 8:
            raise ValueError("The image does not contain enough bits for the stored message.")

        return self.converter.bits_to_text(payload_bits)
