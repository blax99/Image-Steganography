"""Image validation and preparation helpers.

Purpose
-------
Provide utility functions to validate that an image exists, is readable, and
has enough capacity for the requested payload.

Input
-----
- image path string
- Pillow image object

Output
------
- validated image object
- capacity count in bits

Algorithm explanation
--------------------
The helpers wrap Pillow image loading and check if the image has enough RGB
channel capacity for the payload bits before embedding.

Time complexity
---------------
- ``get_capacity``: O(1)
- ``prepare_image``: O(1) for loading the image object

Flow diagram
------------
Image path -> open/convert -> validate -> capacity

Example usage
-------------
>>> from steganography.image_utils import get_capacity, prepare_image
>>> image = prepare_image("cover.png")
>>> capacity = get_capacity(image)
"""

import os
from typing import Optional

from PIL import Image


def validate_image(image_path: str) -> None:
    """Ensure that the image exists and can be opened as a Pillow image."""
    if not isinstance(image_path, str) or not image_path.strip():
        raise ValueError("Image path must be a non-empty string.")
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    try:
        with Image.open(image_path) as image:
            image.verify()
    except Exception as exc:
        raise ValueError("The provided file is not a valid image file.") from exc


def prepare_image(image_path: str) -> Image.Image:
    """Load an image and convert it to RGB mode for consistent access."""
    validate_image(image_path)
    image = Image.open(image_path).convert("RGB")
    return image


def get_capacity(image: Image.Image) -> int:
    """Return the number of available bits in the image's RGB channels."""
    if not isinstance(image, Image.Image):
        raise TypeError("Expected a Pillow Image object.")
    return image.width * image.height * 3
