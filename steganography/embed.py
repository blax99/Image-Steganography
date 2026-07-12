"""Embed text into an image by replacing the least significant bits of pixel channels."""

import os
from typing import Optional

from PIL import Image

from .binary import BinaryConverter
from .image_utils import get_capacity, prepare_image, validate_image
from .pixel import PixelBitHandler


class LSBEmbedder:
    """Hide text inside an image by modifying its least significant bits."""

    def __init__(self, converter: Optional[BinaryConverter] = None):
        self.converter = converter or BinaryConverter()
        self.handler = PixelBitHandler()

    def embed_text(self, image_path: str, message: str, output_path: str) -> str:
        """Embed a UTF-8 message into an image and save the altered PNG image."""
        if not isinstance(image_path, str) or not image_path.strip():
            raise ValueError("Image path must be a non-empty string.")
        if not isinstance(output_path, str) or not output_path.strip():
            raise ValueError("Output path must be a non-empty string.")
        if not isinstance(message, str):
            raise TypeError("Message must be a string.")

        validate_image(image_path)
        image = prepare_image(image_path)
        capacity = get_capacity(image)

        payload_bytes = message.encode("utf-8")
        payload_bits = self.converter.text_to_bits(message)
        length_header = format(len(payload_bytes), "032b")
        full_bits = length_header + payload_bits

        if len(full_bits) > capacity:
            raise ValueError(
                f"Message is too large for this image. Required bits: {len(full_bits)}, capacity: {capacity}."
            )

        pixels = image.load()
        bit_index = 0
        for y in range(image.height):
            for x in range(image.width):
                pixel = list(pixels[x, y])
                for channel_index, channel in enumerate(pixel):
                    if bit_index < len(full_bits):
                        pixel[channel_index] = self.handler.set_lsb(channel, full_bits[bit_index])
                        bit_index += 1
                    else:
                        break
                pixels[x, y] = tuple(pixel)
                if bit_index >= len(full_bits):
                    break
            if bit_index >= len(full_bits):
                break

        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        image.save(output_path, format="PNG")
        return output_path
