# src/modes/aead.py
import os
from typing import Optional


class AEADEncryptThenMAC:
    """
    Реализация AEAD с использованием Encrypt-then-MAC
    Соответствует требованию AEAD-1 из Sprint 6
    """

    def __init__(self, master_key: bytes):
        """
        Инициализация с мастер-ключом и разделением на K_enc и K_mac

        Args:
            master_key: Мастер-ключ (16, 24 или 32 байта)
        """
        if len(master_key) not in [16, 24, 32]:
            raise ValueError("Master key must be 16, 24, or 32 bytes")

        self.master_key = master_key

        # Разделение ключей (K_enc, K_mac)
        self.k_enc, self.k_mac = self._derive_keys(master_key)

        # Импорт зависимостей
        from ciphers.aes import AES
        from mac.hmac import HMAC

        self.aes = AES(self.k_enc)
        self.hmac = HMAC(self.k_mac, 'sha256')

    def _derive_keys(self, master_key: bytes) -> tuple:
        """
        Разделение мастер-ключа на K_enc и K_mac
        Используется простой метод на основе HKDF-подобного подхода
        """
        # Для простоты используем SHA-256 для выработки производных ключей
        # В реальной системе следует использовать HKDF

        import hashlib

        # K_enc = SHA-256(master_key || "encryption")
        k_enc_input = master_key + b"encryption"
        k_enc = hashlib.sha256(k_enc_input).digest()[:len(master_key)]

        # K_mac = SHA-256(master_key || "authentication")
        k_mac_input = master_key + b"authentication"
        k_mac = hashlib.sha256(k_mac_input).digest()[:32]  # 32 байта для HMAC-SHA256

        return k_enc, k_mac

    def encrypt(self, plaintext: bytes, aad: bytes = b"",
                nonce: Optional[bytes] = None) -> bytes:
        """
        Шифрование по схеме Encrypt-then-MAC

        Args:
            plaintext: Открытый текст
            aad: Дополнительные аутентифицированные данные
            nonce: Nonce (если None, генерируется случайно)

        Returns:
            nonce + ciphertext + tag
        """
        # Генерируем nonce если не предоставлен
        if nonce is None:
            nonce = os.urandom(12)

        # 1. Шифрование в режиме CTR (как в GCM)
        ciphertext = self._ctr_encrypt(plaintext, nonce)

        # 2. MAC поверх (nonce || ciphertext || aad)
        mac_data = nonce + ciphertext + aad
        tag = self.hmac.compute(mac_data)[:16]  # Берем первые 16 байт HMAC

        return nonce + ciphertext + tag

    def decrypt(self, data: bytes, aad: bytes = b"") -> bytes:
        """
        Дешифрование с проверкой MAC

        Args:
            data: nonce + ciphertext + tag
            aad: Дополнительные аутентифицированные данные

        Returns:
            Расшифрованный текст

        Raises:
            AuthenticationError: Если проверка MAC не прошла
        """
        if len(data) < 12 + 16:  # Минимум: nonce(12) + tag(16)
            raise AuthenticationError("Data too short")

        # Извлекаем компоненты
        nonce = data[:12]
        tag = data[-16:]
        ciphertext = data[12:-16]

        # 1. Проверка MAC
        mac_data = nonce + ciphertext + aad
        expected_tag = self.hmac.compute(mac_data)[:16]

        if not self._constant_time_compare(tag, expected_tag):
            raise AuthenticationError("MAC verification failed")

        # 2. Расшифрование (только если MAC верен)
        return self._ctr_decrypt(ciphertext, nonce)

    def _ctr_encrypt(self, plaintext: bytes, nonce: bytes) -> bytes:
        """CTR шифрование"""
        ciphertext = bytearray()

        for i in range(0, len(plaintext), 16):
            # Генерация счетчика: nonce || counter
            counter = nonce + (i // 16).to_bytes(4, 'big')

            # Шифрование счетчика
            keystream = self.aes.encrypt(counter)

            # XOR с блоком открытого текста
            block = plaintext[i:i + 16]
            encrypted = bytes(p ^ k for p, k in zip(block, keystream[:len(block)]))
            ciphertext.extend(encrypted)

        return bytes(ciphertext)

    def _ctr_decrypt(self, ciphertext: bytes, nonce: bytes) -> bytes:
        """CTR дешифрование (симметрично шифрованию)"""
        return self._ctr_encrypt(ciphertext, nonce)  # CTR симметричен

    def _constant_time_compare(self, a: bytes, b: bytes) -> bool:
        """Сравнение с постоянным временем"""
        if len(a) != len(b):
            return False

        result = 0
        for x, y in zip(a, b):
            result |= x ^ y
        return result == 0


class AuthenticationError(Exception):
    """Исключение для ошибок аутентификации"""
    pass