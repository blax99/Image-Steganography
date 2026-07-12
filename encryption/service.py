import os
import tempfile
import uuid
from typing import Optional

from PIL import Image

from aes_library import AESCipher
from steganography.embed import LSBEmbedder
from steganography.extract import LSBExtractor


class SteganographyService:
    """Coordinate encryption and steganography operations for Django views."""

    def __init__(self):
        self.embedder = LSBEmbedder()
        self.extractor = LSBExtractor()

    def encode_message(self, message: str, password: str, image_path: str, output_path: Optional[str] = None) -> str:
        """Encrypt a message, hide it inside an image, and save the output image."""
        if not isinstance(message, str) or not message.strip():
            raise ValueError("Message must be a non-empty string.")
        if not isinstance(password, str) or not password.strip():
            raise ValueError("Password must be a non-empty string.")
        if not isinstance(image_path, str) or not image_path.strip():
            raise ValueError("Image path must be a non-empty string.")

        cipher = AESCipher(password)
        encrypted_message = cipher.encrypt(message)

        if output_path is None:
            output_dir = tempfile.gettempdir()
            output_path = os.path.join(output_dir, f"{uuid.uuid4().hex}.png")
        else:
            output_dir = os.path.dirname(output_path)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)

        self.embedder.embed_text(image_path, encrypted_message, output_path)
        return output_path

    def decode_message(self, image_path: str, password: str) -> str:
        """Extract an encrypted payload from an image and decrypt it back to plaintext."""
        if not isinstance(image_path, str) or not image_path.strip():
            raise ValueError("Image path must be a non-empty string.")
        if not isinstance(password, str) or not password.strip():
            raise ValueError("Password must be a non-empty string.")

        cipher = AESCipher(password)
        encrypted_message = self.extractor.extract_text(image_path)
        return cipher.decrypt(encrypted_message)
