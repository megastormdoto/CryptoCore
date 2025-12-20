# tests/unit/test_cli_parser_coverage.py
import unittest
import sys
import os
from io import StringIO

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))


class TestCLIParserCoverage(unittest.TestCase):
    """Тесты для покрытия cli_parser.py"""

    def setUp(self):
        from src.cli_parser import CLIParser
        self.CLIParser = CLIParser

    def test_validate_encrypt_args_gcm_with_nonce(self):
        """Тест валидации GCM с nonce"""
        parser = self.CLIParser()

        # Создаем args для теста
        class MockArgs:
            def __init__(self):
                self.mode = 'gcm'
                self.key = '00112233445566778899aabbccddeeff'
                self.nonce = '112233445566778899001122'  # 12 байт
                self.iv = None
                self.aad = 'test_aad'
                self.decrypt = False

        args = MockArgs()

        # Вызываем валидацию
        parser._validate_encrypt_args(args)

        # Проверяем, что aad преобразовано в bytes
        self.assertEqual(args.aad, b'test_aad')

    def test_validate_encrypt_args_gcm_with_hex_aad(self):
        """Тест валидации GCM с hex AAD"""
        parser = self.CLIParser()

        class MockArgs:
            def __init__(self):
                self.mode = 'gcm'
                self.key = '00' * 16
                self.nonce = None
                self.iv = None
                self.aad = 'aabbccdd'
                self.decrypt = False

        args = MockArgs()

        parser._validate_encrypt_args(args)
        # AAD должно быть bytes.fromhex('aabbccdd')
        self.assertEqual(args.aad, bytes.fromhex('aabbccdd'))

    def test_validate_dgst_args_hmac_with_verify(self):
        """Тест валидации HMAC с verify"""
        parser = self.CLIParser()

        class MockArgs:
            def __init__(self):
                self.hmac = True
                self.key = '00' * 32
                self.verify = 'verify_file.txt'
                self.cmac = False

        args = MockArgs()

        # Не должно вызывать ошибку
        parser._validate_dgst_args(args)

    def test_validate_derive_args_password_file(self):
        """Тест валидации derive с password-file"""
        parser = self.CLIParser()

        class MockArgs:
            def __init__(self):
                self.password = None
                self.password_file = 'pass.txt'
                self.password_env = None
                self.master_key = None
                self.context = None
                self.salt = 'a1b2'
                self.algorithm = 'pbkdf2'
                self.iterations = 1000
                self.length = 32

        args = MockArgs()

        parser._validate_derive_args(args)
        # Не должно вызывать ошибку

    def test_validate_derive_args_master_key_short(self):
        """Тест валидации master key (короткий)"""
        parser = self.CLIParser()

        class MockArgs:
            def __init__(self):
                self.password = None
                self.password_file = None
                self.password_env = None
                self.master_key = '00' * 8  # Только 8 байт
                self.context = 'test'
                self.salt = None
                self.algorithm = 'pbkdf2'
                self.iterations = 1000
                self.length = 32

        args = MockArgs()

        # Должно вызвать warning но не error
        old_stderr = sys.stderr
        sys.stderr = StringIO()

        try:
            parser._validate_derive_args(args)
            output = sys.stderr.getvalue()
            self.assertIn('Warning', output)
            self.assertIn('16 bytes', output)
        finally:
            sys.stderr = old_stderr

    def test_parser_error_messages(self):
        """Тест сообщений об ошибках"""
        parser = self.CLIParser()

        # Тест с неправильными аргументами
        test_args = ['cryptocore', 'encrypt']  # Нет обязательных аргументов

        original_argv = sys.argv
        old_stderr = sys.stderr

        try:
            sys.argv = test_args
            sys.stderr = StringIO()

            with self.assertRaises(SystemExit):
                parser.parse_args()

            error_output = sys.stderr.getvalue()
            self.assertIn('error', error_output.lower())

        finally:
            sys.argv = original_argv
            sys.stderr = old_stderr


if __name__ == '__main__':
    unittest.main()