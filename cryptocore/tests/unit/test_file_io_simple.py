# tests/unit/test_file_io_simple.py
import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))


class TestFileIOSimple(unittest.TestCase):
    """Простые тесты для file_io.py"""

    def setUp(self):
        self.has_file_io = False
        try:
            from src.file_io import read_file, write_file
            self.read_file = read_file
            self.write_file = write_file
            self.has_file_io = True
        except ImportError:
            self.has_file_io = False

    def test_file_io_import(self):
        """Тест импорта file_io"""
        if not self.has_file_io:
            self.skipTest("File IO module not available")

        # Проверяем, что функции существуют
        self.assertTrue(callable(self.read_file))
        self.assertTrue(callable(self.write_file))

    def test_file_io_functions(self):
        """Тест функций file_io"""
        if not self.has_file_io:
            self.skipTest("File IO module not available")

        # Создаем временный файл для теста
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, mode='wb') as tmp:
            tmp.write(b'test data')
            tmp_path = tmp.name

        try:
            # Тестируем read_file
            data = self.read_file(tmp_path)
            self.assertEqual(data, b'test data')

            # Тестируем write_file
            new_path = tmp_path + '.new'
            self.write_file(new_path, b'new data')

            # Проверяем записанное
            with open(new_path, 'rb') as f:
                written = f.read()
            self.assertEqual(written, b'new data')

            # Убираем временные файлы
            os.unlink(new_path)
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)


if __name__ == '__main__':
    unittest.main()