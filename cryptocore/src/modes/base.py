"""
Base class for block cipher modes.
"""


class BaseMode:
    """Base class for all block cipher modes."""

    def __init__(self, cipher):
        self.cipher = cipher

    def encrypt(self, plaintext):
        raise NotImplementedError

    def decrypt(self, ciphertext):
        raise NotImplementedError