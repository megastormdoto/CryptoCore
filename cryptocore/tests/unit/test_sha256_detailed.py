# tests/unit/test_sha256_simple.py
import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))


class TestSHA256Simple(unittest.TestCase):
    """Простые тесты для SHA256 класса"""

    def setUp(self):
        from src.hash.sha256 import SHA256, sha256
        self.SHA256 = SHA256
        self.sha256_func = sha256

    def test_sha256_class_creation(self):
        """Тест создания экземпляра SHA256"""
        hasher = self.SHA256()
        self.assertIsNotNone(hasher)

        # Проверяем наличие основных методов
        self.assertTrue(hasattr(hasher, 'update'))
        self.assertTrue(hasattr(hasher, 'digest'))
        self.assertTrue(hasattr(hasher, 'hexdigest'))
        self.assertTrue(hasattr(hasher, 'hash'))

    def test_sha256_convenience_function(self):
        """Тест удобной функции sha256()"""
        # Пустая строка
        result = self.sha256_func(b'')
        expected = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
        self.assertEqual(result, expected)

        # Тест 'abc'
        result = self.sha256_func(b'abc')
        expected = 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'
        self.assertEqual(result, expected)

    def test_sha256_incremental_hashing(self):
        """Тест пошагового хэширования"""
        hasher = self.SHA256()

        # Хэшируем по частям
        hasher.update(b'hello ')
        hasher.update(b'world')

        # Хэшируем всю строку сразу
        hasher2 = self.SHA256()
        hasher2.update(b'hello world')

        self.assertEqual(hasher.hexdigest(), hasher2.hexdigest())

        # Проверяем известный хэш для 'hello world'
        expected = 'b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9'
        self.assertEqual(hasher.hexdigest(), expected)

    def test_sha256_reset(self):
        """Тест сброса состояния"""
        hasher = self.SHA256()
        hasher.update(b'first message')
        hash1 = hasher.hexdigest()

        # Сбрасываем и хэшируем другое сообщение
        hasher.reset()
        hasher.update(b'second message')
        hash2 = hasher.hexdigest()

        # Хэши должны быть разными
        self.assertNotEqual(hash1, hash2)

        # Проверяем, что после сброса можно снова получить тот же хэш
        hasher.reset()
        hasher.update(b'second message')
        hash2_again = hasher.hexdigest()
        self.assertEqual(hash2, hash2_again)

    def test_sha256_large_data(self):
        """Тест с большими данными"""
        hasher = self.SHA256()

        # 10KB данных
        large_data = b'x' * (10 * 1024)
        hasher.update(large_data)
        hash_result = hasher.hexdigest()

        self.assertEqual(len(hash_result), 64)  # 32 байта в hex
        self.assertIsInstance(hash_result, str)

        # Проверяем, что можно хэшировать в несколько вызовов update
        hasher2 = self.SHA256()
        chunk_size = 1024
        for i in range(10):
            hasher2.update(b'x' * chunk_size)

        self.assertEqual(hash_result, hasher2.hexdigest())


if __name__ == '__main__':
    unittest.main()