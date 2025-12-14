# src/mac/hmac.py
import hashlib
from typing import Union, Optional
import os
import sys


class HMAC:
    def __init__(self, key: Union[bytes, str], hash_function='sha256'):
        """
        Инициализация HMAC с заданным ключом и хеш-функцией.
        """
        if isinstance(key, str):
            self.key = bytes.fromhex(key)
        else:
            self.key = key

        self.hash_function_name = hash_function
        self.block_size = 64  # 512 бит = 64 байта

        # Инициализируем хеш-функцию - ИСПРАВЛЕННЫЙ ИМПОРТ
        if hash_function == 'sha256':
            # Пробуем импортировать SHA256
            try:
                # Способ 1: Относительный импорт
                from ..hash.sha256 import SHA256
                self.hash = SHA256
            except ImportError:
                try:
                    # Способ 2: Абсолютный импорт
                    from hash.sha256 import SHA256
                    self.hash = SHA256
                except ImportError:
                    try:
                        # Способ 3: Импорт через sys.path
                        import sys
                        # Добавляем родительскую директорию в путь
                        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                        if parent_dir not in sys.path:
                            sys.path.insert(0, parent_dir)
                        from hash.sha256 import SHA256
                        self.hash = SHA256
                    except ImportError as e:
                        raise ImportError(f"Cannot import SHA256: {e}. Make sure hash.sha256 exists.")
        else:
            raise ValueError(f"Unsupported hash function: {hash_function}")

        # Обработка ключа согласно RFC 2104
        self._processed_key = self._process_key(self.key)

    def _process_key(self, key: bytes) -> bytes:
        """
        Обработка ключа согласно RFC 2104:
        1. Если ключ длиннее block_size - хешируем его
        2. Если ключ короче block_size - дополняем нулями
        """
        # Шаг 1: Если ключ длиннее block_size, хешируем его
        if len(key) > self.block_size:
            hasher = self.hash()
            hasher.update(key)
            key = hasher.digest()

        # Шаг 2: Если ключ короче block_size, дополняем нулями
        if len(key) < self.block_size:
            key = key + b'\x00' * (self.block_size - len(key))

        return key

    def _xor_bytes(self, a: bytes, b: bytes) -> bytes:
        """Побитовый XOR двух байтовых строк одинаковой длины."""
        return bytes(x ^ y for x, y in zip(a, b))

    def compute(self, message: bytes) -> bytes:
        """
        Вычисление HMAC по формуле:
        HMAC(K, m) = H((K ⊕ opad) || H((K ⊕ ipad) || m))

        Args:
            message: Сообщение для аутентификации

        Returns:
            HMAC в виде байтов
        """
        # Константы для ipad и opad
        ipad = b'\x36' * self.block_size
        opad = b'\x5c' * self.block_size

        # Вычисляем K ⊕ ipad и K ⊕ opad
        key_ipad = self._xor_bytes(self._processed_key, ipad)
        key_opad = self._xor_bytes(self._processed_key, opad)

        # Внутренний хеш: H((K ⊕ ipad) || message)
        inner_hasher = self.hash()
        inner_hasher.update(key_ipad)
        inner_hasher.update(message)
        inner_hash = inner_hasher.digest()

        # Внешний хеш: H((K ⊕ opad) || inner_hash)
        outer_hasher = self.hash()
        outer_hasher.update(key_opad)
        outer_hasher.update(inner_hash)

        return outer_hasher.digest()

    def compute_hex(self, message: bytes) -> str:
        """Вычисление HMAC и возврат в виде hex-строки."""
        return self.compute(message).hex()

    def verify(self, message: bytes, hmac: Union[bytes, str]) -> bool:
        """
        Проверка HMAC.

        Args:
            message: Сообщение
            hmac: Ожидаемый HMAC в виде байтов или hex-строки

        Returns:
            True если HMAC совпадает, иначе False
        """
        computed = self.compute(message)

        if isinstance(hmac, str):
            expected = bytes.fromhex(hmac)
        else:
            expected = hmac

        # Сравнение с постоянным временем для предотвращения timing attacks
        return self._constant_time_compare(computed, expected)

    def _constant_time_compare(self, a: bytes, b: bytes) -> bool:
        """Сравнение байтовых строк с постоянным временем."""
        if len(a) != len(b):
            return False

        result = 0
        for x, y in zip(a, b):
            result |= x ^ y
        return result == 0


# Функция для удобства использования
def hmac_sha256(key: Union[bytes, str], message: bytes) -> bytes:
    """Удобная функция для быстрого вычисления HMAC-SHA256."""
    hmac = HMAC(key, 'sha256')
    return hmac.compute(message)


def hmac_sha256_hex(key: Union[bytes, str], message: bytes) -> str:
    """Удобная функция для быстрого вычисления HMAC-SHA256 в hex."""
    hmac = HMAC(key, 'sha256')
    return hmac.compute_hex(message)