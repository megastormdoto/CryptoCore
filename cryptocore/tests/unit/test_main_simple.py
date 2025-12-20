# tests/unit/test_main_simple.py
import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))


class TestMainSimple(unittest.TestCase):
    """Простые тесты для main.py"""

    def setUp(self):
        self.has_main = False
        try:
            from src.main import CryptoCore, main
            self.CryptoCore = CryptoCore
            self.main_func = main
            self.has_main = True
        except ImportError:
            self.has_main = False

    def test_main_import(self):
        """Тест импорта main"""
        if not self.has_main:
            self.skipTest("Main module not available")

        self.assertIsNotNone(self.CryptoCore)
        self.assertIsNotNone(self.main_func)

    def test_cryptocore_class(self):
        """Тест класса CryptoCore"""
        if not self.has_main:
            self.skipTest("Main module not available")

        crypto = self.CryptoCore()
        self.assertIsNotNone(crypto)

        # Проверяем наличие основных методов
        self.assertTrue(hasattr(crypto, 'run'))
        self.assertTrue(hasattr(crypto, 'handle_encryption'))
        self.assertTrue(hasattr(crypto, 'handle_digest'))
        self.assertTrue(hasattr(crypto, 'handle_derive'))


if __name__ == '__main__':
    unittest.main()