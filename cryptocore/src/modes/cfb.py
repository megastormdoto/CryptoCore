from Crypto.Cipher import AES
from . import BaseMode


class CFBMode(BaseMode):
    def encrypt(self, plaintext, iv=None):
        if iv is None:
            raise ValueError("IV is required for CFB mode")
        if len(iv) != self.block_size:
            raise ValueError("IV must be 16 bytes")
        cipher = AES.new(self.key, AES.MODE_ECB)
        encrypted_blocks = []
        feedback = iv
        for i in range(0, len(plaintext), self.block_size):
            block = plaintext[i:i + self.block_size]
            encrypted_feedback = cipher.encrypt(feedback)
            encrypted_block = bytes(a ^ b for a, b in zip(block, encrypted_feedback))
            encrypted_blocks.append(encrypted_block)
            feedback = encrypted_block
        return b''.join(encrypted_blocks)

    def decrypt(self, ciphertext, iv=None):
        if iv is None:
            raise ValueError("IV is required for CFB mode")
        if len(iv) != self.block_size:
            raise ValueError("IV must be 16 bytes")
        cipher = AES.new(self.key, AES.MODE_ECB)
        decrypted_blocks = []
        feedback = iv
        for i in range(0, len(ciphertext), self.block_size):
            block = ciphertext[i:i + self.block_size]
            encrypted_feedback = cipher.encrypt(feedback)
            decrypted_block = bytes(a ^ b for a, b in zip(block, encrypted_feedback))
            decrypted_blocks.append(decrypted_block)
            feedback = block
        return b''.join(decrypted_blocks)