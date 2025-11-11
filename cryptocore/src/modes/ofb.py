from Crypto.Cipher import AES
from . import BaseMode


class OFBMode(BaseMode):
    def encrypt(self, plaintext, iv=None):
        if iv is None:
            raise ValueError("IV is required for OFB mode")
        if len(iv) != self.block_size:
            raise ValueError("IV must be 16 bytes")
        cipher = AES.new(self.key, AES.MODE_ECB)
        encrypted_blocks = []
        feedback = iv
        for i in range(0, len(plaintext), self.block_size):
            block = plaintext[i:i + self.block_size]
            keystream = cipher.encrypt(feedback)
            encrypted_block = bytes(a ^ b for a, b in zip(block, keystream))
            encrypted_blocks.append(encrypted_block)
            feedback = keystream
        return b''.join(encrypted_blocks)

    def decrypt(self, ciphertext, iv=None):
        if iv is None:
            raise ValueError("IV is required for OFB mode")
        if len(iv) != self.block_size:
            raise ValueError("IV must be 16 bytes")
        return self.encrypt(ciphertext, iv)