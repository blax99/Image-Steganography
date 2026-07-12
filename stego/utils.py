import os
import tempfile

from aes_library import AESCipher
from steganography.embed import LSBEmbedder
from steganography.extract import LSBExtractor


def get_temp_path(filename):
    """Get cross-platform temporary file path."""
    temp_dir = tempfile.gettempdir()
    return os.path.join(temp_dir, filename)


def encrypt_message(message, secret_key):
    """Encrypt a message using the reusable AES package."""
    cipher = AESCipher(secret_key)
    return cipher.encrypt(message)


def decrypt_message(encrypted_data, secret_key):
    """Decrypt a payload using the reusable AES package."""
    try:
        cipher = AESCipher(secret_key)
        return cipher.decrypt(encrypted_data)
    except Exception:
        return None


def hide_message_in_image(image_path, encrypted_message):
    """Hide encrypted data in an image using the reusable LSB embedder."""
    output_path = get_temp_path(f"{os.path.splitext(os.path.basename(image_path))[0]}_encoded.png")
    LSBEmbedder().embed_text(image_path, encrypted_message, output_path)
    return output_path


def extract_message_from_image(image_path):
    """Extract encrypted data from an image using the reusable LSB extractor."""
    return LSBExtractor().extract_text(image_path)


class SteganographyEngine:
    """Compatibility wrapper for the modular implementation."""

    @staticmethod
    def encrypt_message(message, secret_key):
        return encrypt_message(message, secret_key)

    @staticmethod
    def decrypt_message(encrypted_data, secret_key):
        return decrypt_message(encrypted_data, secret_key)

    @staticmethod
    def hide_message_in_image(image_path, encrypted_message):
        return hide_message_in_image(image_path, encrypted_message)

    @staticmethod
    def extract_message_from_image(image_path):
        return extract_message_from_image(image_path)