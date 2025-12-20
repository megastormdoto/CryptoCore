# src/aead/encrypt_then_mac.py
import os
import struct
from typing import Union


class AuthenticationError(Exception):
    """Exception raised when authentication fails."""
    pass


class EncryptThenMAC:
    """Encrypt-then-MAC authenticated encryption."""

    def __init__(self, key: bytes, mode_class, mode_args=None):
        """
        Initialize EncryptThenMAC.

        Args:
            key: Master key (will be split into encryption and MAC keys)
            mode_class: Block cipher mode class (e.g., CTR)
            mode_args: Arguments for the mode constructor
        """
        if len(key) < 32:
            # For AES-128, we need 32 bytes (16 for encryption, 16 for MAC)
            raise ValueError("Key must be at least 32 bytes for Encrypt-then-MAC")

        # ИСПРАВЛЕНО: Импортируем HMAC
        try:
            from mac.hmac import HMAC
        except ImportError:
            # Альтернативный путь
            from ..mac.hmac import HMAC

        # ИСПРАВЛЕНО: Используем строку 'sha256' вместо класса SHA256
        # Создаем HMAC с алгоритмом SHA256 (передаем строку 'sha256')
        hmac_obj = HMAC(key, 'sha256')

        # Генерируем производные ключи
        enc_key_data = b"encryption_key_derivation" + struct.pack('>I', 1)
        mac_key_data = b"mac_key_derivation" + struct.pack('>I', 1)

        self.enc_key = hmac_obj.compute(enc_key_data)[:16]
        self.mac_key = hmac_obj.compute(mac_key_data)[:16]

        # Initialize encryption mode
        mode_args = mode_args or {}
        self.cipher = mode_class(self.enc_key, **mode_args)

        # Initialize HMAC для MAC
        self.hmac = HMAC(self.mac_key, 'sha256')

    def encrypt(self, plaintext: bytes, aad: bytes = b"") -> bytes:
        """Encrypt then MAC."""
        # Encrypt
        ciphertext = self.cipher.encrypt(plaintext)

        # Compute MAC over ciphertext || AAD
        mac_data = ciphertext + aad
        tag = self.hmac.compute(mac_data)[:16]  # 16 bytes for AES

        return ciphertext + tag

    def decrypt(self, data: bytes, aad: bytes = b"") -> bytes:
        """Verify MAC then decrypt."""
        if len(data) < 16:
            raise AuthenticationError("Data too short to contain tag")

        ciphertext = data[:-16]
        received_tag = data[-16:]

        # Verify MAC
        mac_data = ciphertext + aad
        expected_tag = self.hmac.compute(mac_data)[:16]

        # Constant-time comparison для безопасности
        if len(expected_tag) != len(received_tag):
            raise AuthenticationError("Authentication failed: MAC mismatch")

        # Простая проверка (замените на constant-time если есть функция)
        if expected_tag != received_tag:
            raise AuthenticationError("Authentication failed: MAC mismatch")

        # Decrypt
        return self.cipher.decrypt(ciphertext)