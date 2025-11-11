from Crypto.Cipher import AES
from . import BaseMode


class ECBMode(BaseMode):
    def encrypt(self, plaintext, iv=None):
        padded_data = self._pkcs7_pad(plaintext)
        cipher = AES.new(self.key, AES.MODE_ECB)
        encrypted_blocks = []
        for i in range(0, len(padded_data), self.block_size):
            block = padded_data[i:i + self.block_size]
            encrypted_block = cipher.encrypt(block)
            encrypted_blocks.append(encrypted_block)
        return b''.join(encrypted_blocks)

    def decrypt(self, ciphertext, iv=None):
        if len(ciphertext) % self.block_size != 0:
            raise ValueError("Ciphertext must be multiple of block size")
        cipher = AES.new(self.key, AES.MODE_ECB)
        decrypted_blocks = []
        for i in range(0, len(ciphertext), self.block_size):
            block = ciphertext[i:i + self.block_size]
            decrypted_block = cipher.decrypt(block)
            decrypted_blocks.append(decrypted_block)
        decrypted_data = b''.join(decrypted_blocks)
        return self._pkcs7_unpad(decrypted_data)