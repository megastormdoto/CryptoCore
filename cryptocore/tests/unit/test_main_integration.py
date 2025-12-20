# tests/integration/test_main_integration.py
import unittest
import sys
import os
from io import StringIO
from unittest.mock import patch, MagicMock, mock_open

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))


class TestMainIntegration(unittest.TestCase):
    """Интеграционные тесты для main.py"""

    def setUp(self):
        from src.main import CryptoCore, main
        self.CryptoCore = CryptoCore
        self.main_func = main

    def test_cryptocore_class_creation(self):
        """Тест создания CryptoCore класса"""
        crypto = self.CryptoCore()
        self.assertIsNotNone(crypto)
        self.assertTrue(hasattr(crypto, 'parser'))
        self.assertTrue(hasattr(crypto, 'run'))

    def test_main_function_exists(self):
        """Тест существования основной функции"""
        self.assertIsNotNone(self.main_func)
        self.assertTrue(callable(self.main_func))

    @patch('src.main.CryptoCore')
    def test_main_calls_cryptocore_run(self, mock_cryptocore):
        """Тест, что main вызывает CryptoCore.run()"""
        # Создаем mock экземпляр
        mock_instance = MagicMock()
        mock_cryptocore.return_value = mock_instance

        # Вызываем main
        try:
            self.main_func()
        except SystemExit:
            pass  # Ожидаем SystemExit, так как нет аргументов

        # Проверяем, что run был вызван
        mock_instance.run.assert_called_once()

    def test_cryptocore_handlers_exist(self):
        """Тест существования обработчиков команд"""
        crypto = self.CryptoCore()

        # Проверяем наличие методов-обработчиков
        self.assertTrue(hasattr(crypto, 'handle_encryption'))
        self.assertTrue(hasattr(crypto, 'handle_digest'))
        self.assertTrue(hasattr(crypto, 'handle_derive'))

    @patch('sys.argv', ['cryptocore', '--help'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_cli_help_output(self, mock_stdout):
        """Тест вывода help"""
        try:
            self.main_func()
        except SystemExit as e:
            # SystemExit(0) при успешном --help
            output = mock_stdout.getvalue()
            self.assertIn('usage:', output.lower())
            self.assertIn('cryptocore', output)


if __name__ == '__main__':
    unittest.main()