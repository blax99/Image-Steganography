import os
import tempfile
from django.test import SimpleTestCase
from PIL import Image

from aes_library import AESCipher
from steganography.embed import LSBEmbedder
from steganography.extract import LSBExtractor


class ModularLibraryTests(SimpleTestCase):
    def test_aes_round_trip(self):
        cipher = AESCipher("super-secret-key")
        message = "Hello from the modular library"

        encrypted = cipher.encrypt(message)
        self.assertNotEqual(encrypted, message)
        self.assertEqual(cipher.decrypt(encrypted), message)

    def test_lsb_round_trip(self):
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as handle:
            temp_path = handle.name

        try:
            image = Image.new("RGB", (64, 64), color=(255, 255, 255))
            image.save(temp_path)

            cipher = AESCipher("another-secret-key")
            payload = cipher.encrypt("Hidden message")
            output_path = temp_path + ".encoded.png"
            LSBEmbedder().embed_text(temp_path, payload, output_path)

            self.assertEqual(LSBExtractor().extract_text(output_path), payload)
            self.assertEqual(cipher.decrypt(LSBExtractor().extract_text(output_path)), "Hidden message")
        finally:
            for path in [temp_path, temp_path + ".encoded.png"]:
                if os.path.exists(path):
                    os.remove(path)

    def test_invalid_payload_is_handled_gracefully(self):
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as handle:
            temp_path = handle.name

        try:
            image = Image.new("RGB", (16, 16), color=(10, 20, 30))
            image.save(temp_path)
            with self.assertRaises(ValueError):
                LSBExtractor().extract_text(temp_path)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
