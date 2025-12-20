from Crypto.Cipher import AES
from . import BaseMode
import os


class CTRMode(BaseMode):
    def encrypt(self, plaintext, iv=None):
        if iv is None:
            # ИСПРАВЛЕНО: Используем абсолютный импорт или альтернативу
            try:
                # Способ 1: Абсолютный импорт
                from random import generate_iv
            except ImportError:
                try:
                    # Способ 2: Альтернативный путь
                    from ..random import generate_iv
                except ImportError:
                    # Способ 3: Если модуль random не существует, используем os.urandom напрямую
                    def generate_iv(length):
                        return os.urandom(length)

            iv = generate_iv(self.block_size)

        if len(iv) != self.block_size:
            raise ValueError("IV must be 16 bytes")

        cipher = AES.new(self.key, AES.MODE_ECB)
        encrypted_blocks = []
        counter = int.from_bytes(iv, byteorder='big')

        for i in range(0, len(plaintext), self.block_size):
            block = plaintext[i:i + self.block_size]
            counter_bytes = counter.to_bytes(self.block_size, byteorder='big')
            keystream = cipher.encrypt(counter_bytes)
            encrypted_block = bytes(a ^ b for a, b in zip(block, keystream))
            encrypted_blocks.append(encrypted_block)
            counter += 1

        # Возвращаем и IV и шифротекст
        return iv + b''.join(encrypted_blocks)

    def decrypt(self, ciphertext, iv=None):
        if iv is None:
            # Извлекаем IV из начала ciphertext
            if len(ciphertext) < self.block_size:
                raise ValueError("Ciphertext too short to contain IV")
            iv = ciphertext[:self.block_size]
            ciphertext = ciphertext[self.block_size:]

        if len(iv) != self.block_size:
            raise ValueError("IV must be 16 bytes")

        # Реализация дешифрования CTR
        cipher = AES.new(self.key, AES.MODE_ECB)
        decrypted_blocks = []
        counter = int.from_bytes(iv, byteorder='big')

        for i in range(0, len(ciphertext), self.block_size):
            block = ciphertext[i:i + self.block_size]
            counter_bytes = counter.to_bytes(self.block_size, byteorder='big')
            keystream = cipher.encrypt(counter_bytes)
            decrypted_block = bytes(a ^ b for a, b in zip(block, keystream))
            decrypted_blocks.append(decrypted_block)
            counter += 1

        return b''.join(decrypted_blocks)