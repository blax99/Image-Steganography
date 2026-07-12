# steganography

## Purpose
This package provides a reusable LSB steganography API for embedding and extracting UTF-8 text inside image pixels. The implementation is intentionally kept separate from Django view code so it can be reused by forms, views, or services.

## Module overview

### __init__.py
- Purpose: Export the public API of the package.
- Functions: Re-exports `BinaryConverter`, `LSBEmbedder`, `LSBExtractor`, `PixelBitHandler`, and the image helpers.
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
  from steganography import LSBEmbedder, LSBExtractor
  ```

### binary.py
- Purpose: Convert text into binary bits and back again.
- Functions:
  - `BinaryConverter.text_to_bits`
  - `BinaryConverter.bits_to_text`
- Input: text string or binary string.
- Output: binary string or reconstructed text.
- Algorithm explanation: Encode characters as 8-bit binary values and decode them back.
- Time complexity: O(n).
- Flow diagram:
  ```text
  Text -> 8-bit ASCII -> binary string
  ```
- Example usage:
  ```python
  from steganography.binary import BinaryConverter
  bits = BinaryConverter.text_to_bits("hello")
  ```

### pixel.py
- Purpose: Set and read the LSB of pixel channels.
- Functions:
  - `PixelBitHandler.set_lsb`
  - `PixelBitHandler.get_lsb`
- Input: channel value and bit value.
- Output: modified channel value or bit string.
- Algorithm explanation: Use masking and bitwise OR to modify the least significant bit of an integer channel value.
- Time complexity: O(1).
- Flow diagram:
  ```text
  channel value -> clear LSB -> set desired bit -> updated value
  ```
- Example usage:
  ```python
  from steganography.pixel import PixelBitHandler
  updated = PixelBitHandler.set_lsb(200, "1")
  ```

### embed.py
- Purpose: Hide text inside an image by modifying the least significant bits of pixels.
- Functions:
  - `LSBEmbedder.embed_text`
- Input: image path, message string, output path.
- Output: output image path.
- Algorithm explanation: Prefix a 32-bit length header to the message bits and overwrite the LSB of RGB channels in the image.
- Time complexity: O(width * height).
- Flow diagram:
  ```text
  Message -> bits -> length header -> embed into pixel LSBs -> output PNG
  ```
- Example usage:
  ```python
  from steganography.embed import LSBEmbedder
  embedder = LSBEmbedder()
  embedder.embed_text("cover.png", "secret", "stego.png")
  ```

### extract.py
- Purpose: Extract hidden text from an image file.
- Functions:
  - `LSBExtractor.extract_text`
- Input: image path.
- Output: extracted text string.
- Algorithm explanation: Read pixel LSBs, reconstruct the length header, decode the message payload, and convert it back to text.
- Time complexity: O(width * height).
- Flow diagram:
  ```text
  PNG image -> read pixel LSBs -> length header -> message bits -> text
  ```
- Example usage:
  ```python
  from steganography.extract import LSBExtractor
  extracted = LSBExtractor().extract_text("stego.png")
  ```

### image_utils.py
- Purpose: Validate and prepare images for embedding/extraction.
- Functions:
  - `validate_image`
  - `prepare_image`
  - `get_capacity`
- Input: existing image path or Pillow Image object.
- Output: validated image object or available capacity.
- Algorithm explanation: Ensure the file exists and the image can be loaded as an RGB image before processing.
- Time complexity: O(1).
- Flow diagram:
  ```text
  Image path -> open/convert -> capacity check
  ```
- Example usage:
  ```python
  from steganography.image_utils import prepare_image, get_capacity
  image = prepare_image("cover.png")
  capacity = get_capacity(image)
  ```
