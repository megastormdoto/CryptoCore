# tests/unit/test_main_detailed.py
import unittest
import sys
import os
from io import StringIO
from unittest.mock import patch, MagicMock, mock_open

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))


class TestMainDetailed(unittest.TestCase):
    """Детальные тесты для main.py"""

    def setUp(self):
        try:
            from src.main import CryptoCore
            self.CryptoCore = CryptoCore
            self.has_main = True
        except ImportError:
            self.has_main = False

    def test_cryptocore_initialization(self):
        """Тест инициализации CryptoCore"""
        if not self.has_main:
            self.skipTest("Main module not available")

        crypto = self.CryptoCore()
        self.assertIsNotNone(crypto)
        self.assertTrue(hasattr(crypto, 'parser'))

    @patch('src.main.CLIParser')
    def test_cryptocore_run_calls_parser(self, mock_cliparser):
        """Тест, что run вызывает парсер"""
        if not self.has_main:
            self.skipTest("Main module not available")

        mock_parser_instance = MagicMock()
        mock_args = MagicMock()
        mock_args.command = 'encrypt'
        mock_parser_instance.parse_args.return_value = mock_args
        mock_cliparser.return_value = mock_parser_instance

        crypto = self.CryptoCore()

        # Симулируем вызов run с моком для handle_encryption
        with patch.object(crypto, 'handle_encryption') as mock_handle:
            crypto.run()

            # Проверяем, что парсер был вызван
            mock_parser_instance.parse_args.assert_called_once()

    @patch('src.main.AES')
    @patch('src.main.GCM')
    def test_handle_encryption_gcm(self, mock_gcm, mock_aes):
        """Тест handle_encryption для GCM"""
        if not self.has_main:
            self.skipTest("Main module not available")

        crypto = self.CryptoCore()

        # Создаем mock аргументы
        class MockArgs:
            command = 'encrypt'
            mode = 'gcm'
            key = '00112233445566778899aabbccddeeff'
            input = 'test.txt'
            output = 'test.enc'
            decrypt = False
            iv = None
            aad = ''

        args = MockArgs()

        # Mock для файловых операций
        mock_gcm_instance = MagicMock()
        mock_gcm_instance.encrypt.return_value = b'encrypted_data'
        mock_gcm.return_value = mock_gcm_instance

        with patch('builtins.open', mock_open(read_data=b'test data')):
            with patch('os.path.exists', return_value=True):
                # Вызываем handle_encryption
                crypto.handle_encryption(args)

                # Проверяем, что GCM был создан
                mock_gcm.assert_called_once()

    @patch('src.main.HMAC')
    def test_handle_digest_hmac(self, mock_hmac):
        """Тест handle_digest для HMAC"""
        if not self.has_main:
            self.skipTest("Main module not available")

        crypto = self.CryptoCore()

        class MockArgs:
            command = 'dgst'
            algorithm = 'sha256'
            input = 'test.txt'
            output = None
            hmac = True
            key = '00112233445566778899aabbccddeeff'
            verify = None
            cmac = False

        args = MockArgs()

        mock_hmac_instance = MagicMock()
        mock_hmac_instance.compute.return_value = b'hmac_value'  # b'hmac_value'.hex() = '686d61635f76616c7565'
        mock_hmac.return_value = mock_hmac_instance

        with patch('builtins.open', mock_open(read_data=b'test data')):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                crypto.handle_digest(args)
                output = mock_stdout.getvalue()

                # Ищем hex представление b'hmac_value'
                self.assertIn('686d61635f76616c7565', output)

    def test_main_function(self):
        """Тест основной функции main()"""
        if not self.has_main:
            self.skipTest("Main module not available")

        from src.main import main

        # Проверяем, что функция существует
        self.assertTrue(callable(main))

        # Тест с аргументами командной строки
        test_args = ['cryptocore', '--help']

        with patch('sys.argv', test_args):
            with patch('sys.stdout', new_callable=StringIO):
                try:
                    main()
                except SystemExit:
                    pass  # Ожидаем SystemExit для --help


if __name__ == '__main__':
    unittest.main()