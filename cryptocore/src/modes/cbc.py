from Crypto.Cipher import AES
from . import BaseMode


class CBCMode(BaseMode):
    def encrypt(self, plaintext, iv=None):
        if iv is None:
            raise ValueError("IV is required for CBC mode")
        if len(iv) != self.block_size:
            raise ValueError("IV must be 16 bytes")
        padded_data = self._pkcs7_pad(plaintext)
        cipher = AES.new(self.key, AES.MODE_ECB)
        encrypted_blocks = []
        previous_block = iv
        for i in range(0, len(padded_data), self.block_size):
            block = padded_data[i:i + self.block_size]
            xored_block = bytes(a ^ b for a, b in zip(block, previous_block))
            encrypted_block = cipher.encrypt(xored_block)
            encrypted_blocks.append(encrypted_block)
            previous_block = encrypted_block
        return b''.join(encrypted_blocks)

    def decrypt(self, ciphertext, iv=None):
        if iv is None:
            raise ValueError("IV is required for CBC mode")
        if len(iv) != self.block_size:
            raise ValueError("IV must be 16 bytes")
        if len(ciphertext) % self.block_size != 0:
            raise ValueError("Ciphertext must be multiple of block size")
        cipher = AES.new(self.key, AES.MODE_ECB)
        decrypted_blocks = []
        previous_block = iv
        for i in range(0, len(ciphertext), self.block_size):
            block = ciphertext[i:i + self.block_size]
            decrypted_block = cipher.decrypt(block)
            plaintext_block = bytes(a ^ b for a, b in zip(decrypted_block, previous_block))
            decrypted_blocks.append(plaintext_block)
            previous_block = block
        decrypted_data = b''.join(decrypted_blocks)
        return self._pkcs7_unpad(decrypted_data)