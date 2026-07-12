"""Helpers for manipulating individual pixel channel bits.

Purpose
-------
Provide low-level operations for reading and writing the least significant bit
of RGB channel values.

Input
-----
- pixel channel value between 0 and 255
- bit value as ``"0"`` or ``"1"``

Output
------
- the modified channel value after setting the LSB
- the LSB value of the channel as a string

Algorithm explanation
--------------------
The module uses bit masking to clear the last bit and OR it with the chosen
bit value. Reading uses ``channel_value & 1`` to extract the least significant
bit.

Time complexity
---------------
- Both operations are O(1).

Flow diagram
------------
channel value -> mask/OR -> updated channel value
"""


class PixelBitHandler:
    """Manage least significant bit reads and writes for pixel channels."""

    @staticmethod
    def set_lsb(channel_value: int, bit: str) -> int:
        """Replace a channel's least significant bit with ``0`` or ``1``."""
        if not isinstance(channel_value, int):
            raise TypeError("Channel value must be an integer.")
        if channel_value < 0 or channel_value > 255:
            raise ValueError("Channel value must be between 0 and 255.")
        if bit not in {"0", "1"}:
            raise ValueError("Bit must be either '0' or '1'.")
        return (channel_value & 0xFE) | int(bit)

    @staticmethod
    def get_lsb(channel_value: int) -> str:
        """Read the least significant bit from a channel value."""
        if not isinstance(channel_value, int):
            raise TypeError("Channel value must be an integer.")
        if channel_value < 0 or channel_value > 255:
            raise ValueError("Channel value must be between 0 and 255.")
        return str(channel_value & 1)
