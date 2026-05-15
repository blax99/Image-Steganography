import os
import base64
import tempfile
from pathlib import Path

def get_temp_path(filename):
    """Get cross-platform temporary file path"""
    temp_dir = tempfile.gettempdir()
    return os.path.join(temp_dir, filename)

def encrypt_message(message, secret_key):
    """Encrypt message using AES-256"""
    from Crypto.Cipher import AES
    from Crypto.Random import get_random_bytes
    from Crypto.Protocol.KDF import PBKDF2
    
    salt = get_random_bytes(16)
    key = PBKDF2(secret_key, salt, dkLen=32)
    cipher = AES.new(key, AES.MODE_GCM)
    nonce = cipher.nonce
    
    ciphertext, tag = cipher.encrypt_and_digest(message.encode('utf-8'))
    encrypted_data = salt + nonce + tag + ciphertext
    
    return base64.b64encode(encrypted_data).decode('utf-8')

def decrypt_message(encrypted_data, secret_key):
    """Decrypt message using AES-256"""
    from Crypto.Cipher import AES
    from Crypto.Protocol.KDF import PBKDF2
    
    try:
        encrypted_data = base64.b64decode(encrypted_data.encode('utf-8'))
        
        salt = encrypted_data[:16]
        nonce = encrypted_data[16:32]
        tag = encrypted_data[32:48]
        ciphertext = encrypted_data[48:]
        
        key = PBKDF2(secret_key, salt, dkLen=32)
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        message = cipher.decrypt_and_verify(ciphertext, tag)
        
        return message.decode('utf-8')
    except Exception as e:
        return None

def hide_message_in_image(image_path, encrypted_message):
    """Hide encrypted message in image using LSB steganography"""
    from PIL import Image
    
    img = Image.open(image_path).convert('RGB')
    pixels = img.load()
    
    message_bits = ''.join(format(ord(c), '08b') for c in encrypted_message)
    message_length = format(len(encrypted_message), '032b')
    full_message = message_length + message_bits
    
    if len(full_message) > img.width * img.height * 3:
        raise ValueError("Message too large for image")
    
    bit_index = 0
    for y in range(img.height):
        for x in range(img.width):
            pixel = list(pixels[x, y])
            
            for channel in range(3):
                if bit_index < len(full_message):
                    pixel[channel] = (pixel[channel] & 0xFE) | int(full_message[bit_index])
                    bit_index += 1
            
            pixels[x, y] = tuple(pixel)
            
            if bit_index >= len(full_message):
                return img
    
    return img

def extract_message_from_image(image_path):
    """Extract encrypted message from image using LSB steganography"""
    from PIL import Image
    
    img = Image.open(image_path).convert('RGB')
    pixels = img.load()
    
    binary_string = ''
    for y in range(img.height):
        for x in range(img.width):
            pixel = pixels[x, y]
            for channel in range(3):
                binary_string += str(pixel[channel] & 1)
    
    message_length = int(binary_string[:32], 2)
    message_bits = binary_string[32:32 + message_length * 8]
    
    message = ''.join(chr(int(message_bits[i:i+8], 2)) for i in range(0, len(message_bits), 8))
    
    return message

class SteganographyEngine:
    """Legacy class interface for backward compatibility"""
    
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