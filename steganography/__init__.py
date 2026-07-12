"""Reusable LSB steganography helpers for embedding and extracting text.

Purpose
-------
Expose a small, reusable API for hiding UTF-8 text inside the LSBs of RGB
pixel channels in image files.

Why this module exists
----------------------
This package keeps image steganography logic separate from Django views so the
application can reuse the same functionality in forms and views without
mixing business logic into the presentation layer.
"""

from .binary import BinaryConverter
from .embed import LSBEmbedder
from .extract import LSBExtractor
from .image_utils import get_capacity, prepare_image, validate_image
from .pixel import PixelBitHandler

__all__ = [
    "BinaryConverter",
    "LSBEmbedder",
    "LSBExtractor",
    "PixelBitHandler",
    "get_capacity",
    "prepare_image",
    "validate_image",
]
