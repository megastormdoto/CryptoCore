# tests/unit/test_hmac_simple.py
import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))


class TestHMACSimple(unittest.TestCase):
    """Простые тесты для HMAC класса"""

    def setUp(self):
        from src.mac.hmac import HMAC, hmac_sha256
        self.HMAC = HMAC
        self.hmac_sha256 = hmac_sha256

    def test_hmac_creation(self):
        """Тест создания экземпляра HMAC"""
        hmac = self.HMAC(b'secret_key', 'sha256')
        self.assertIsNotNone(hmac)

        # Проверяем наличие основных методов
        self.assertTrue(hasattr(hmac, 'compute'))
        self.assertTrue(hasattr(hmac, 'compute_hex'))
        self.assertTrue(hasattr(hmac, 'verify'))

    def test_hmac_sha256_function(self):
        """Тест удобной функции hmac_sha256()"""
        key = b'test_key'
        message = b'test_message'

        hmac_value = self.hmac_sha256(key, message)

        self.assertEqual(len(hmac_value), 32)  # SHA-256 = 32 байта
        self.assertIsInstance(hmac_value, bytes)

        # Проверяем детерминированность
        hmac_value2 = self.hmac_sha256(key, message)
        self.assertEqual(hmac_value, hmac_value2)

    def test_hmac_compute_and_verify(self):
        """Тест вычисления и проверки HMAC"""
        key = b'my_secret_key'
        message = b'important data'

        # Создаем HMAC экземпляр
        hmac = self.HMAC(key, 'sha256')

        # Вычисляем HMAC
        computed = hmac.compute(message)

        # Проверяем
        self.assertTrue(hmac.verify(message, computed))

        # Проверяем с неправильным сообщением
        wrong_message = b'tampered data'
        self.assertFalse(hmac.verify(wrong_message, computed))

        # Проверяем с неправильным HMAC
        wrong_hmac = b'x' * 32
        self.assertFalse(hmac.verify(message, wrong_hmac))

    def test_hmac_with_different_key_lengths(self):
        """Тест HMAC с ключами разной длины"""
        message = b'test'

        # Короткий ключ
        short_key = b'short'
        hmac1 = self.HMAC(short_key, 'sha256')
        result1 = hmac1.compute(message)

        # Ключ равный размеру блока (64 байта)
        block_key = b'x' * 64
        hmac2 = self.HMAC(block_key, 'sha256')
        result2 = hmac2.compute(message)

        # Длинный ключ
        long_key = b'x' * 100
        hmac3 = self.HMAC(long_key, 'sha256')
        result3 = hmac3.compute(message)

        # Все результаты должны быть разными
        self.assertEqual(len(result1), 32)
        self.assertEqual(len(result2), 32)
        self.assertEqual(len(result3), 32)

        self.assertNotEqual(result1, result2)
        self.assertNotEqual(result2, result3)
        self.assertNotEqual(result1, result3)

    def test_hmac_hex_output(self):
        """Тест hex вывода"""
        key = b'key123'
        message = b'hello world'

        hmac = self.HMAC(key, 'sha256')
        hex_result = hmac.compute_hex(message)

        self.assertEqual(len(hex_result), 64)  # 32 байта * 2 hex символа
        self.assertIsInstance(hex_result, str)

        # Проверяем, что hex соответствует bytes
        bytes_result = hmac.compute(message)
        self.assertEqual(hex_result, bytes_result.hex())


if __name__ == '__main__':
    unittest.main()