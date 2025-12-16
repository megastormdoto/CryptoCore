# src/modes/base.py
class BaseMode:
    """Base class for all block cipher modes"""

    def __init__(self, key, block_size=16):
        self.key = key
        self.block_size = block_size

    def encrypt(self, plaintext, iv=None):
        raise NotImplementedError("Subclasses must implement encrypt()")

    def decrypt(self, ciphertext, iv=None):
        raise NotImplementedError("Subclasses must implement decrypt()")