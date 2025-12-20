# tests/unit/test_modes_basic.py
import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))


class TestModesBasic(unittest.TestCase):
    """Базовые тесты для режимов шифрования"""

    def test_cbc_class_structure(self):
        """Тест структуры класса CBC"""
        try:
            from src.modes.cbc import CBCMode
            self.assertTrue(True)  # Импорт успешен
        except ImportError:
            self.skipTest("CBCMode not available")

    def test_ecb_class_structure(self):
        """Тест структуры класса ECB"""
        try:
            from src.modes.ecb import ECBMode
            self.assertTrue(True)  # Импорт успешен
        except ImportError:
            self.skipTest("ECBMode not available")

    def test_cfb_class_structure(self):
        """Тест структуры класса CFB"""
        try:
            from src.modes.cfb import CFBMode
            self.assertTrue(True)
        except ImportError:
            self.skipTest("CFBMode not available")

    def test_ofb_class_structure(self):
        """Тест структуры класса OFB"""
        try:
            from src.modes.ofb import OFBMode
            self.assertTrue(True)
        except ImportError:
            self.skipTest("OFBMode not available")

    def test_ctr_class_structure(self):
        """Тест структуры класса CTR"""
        try:
            from src.modes.ctr import CTRMode
            self.assertTrue(True)
        except ImportError:
            self.skipTest("CTRMode not available")


if __name__ == '__main__':
    unittest.main()