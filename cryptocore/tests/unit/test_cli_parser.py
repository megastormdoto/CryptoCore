# tests/unit/test_cli_parser_fixed.py
import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))


class TestCLIParserFixed(unittest.TestCase):
    """Тесты для реального CLIParser из вашего проекта"""

    def setUp(self):
        # Импортируем реальный модуль
        from src.cli_parser import CLIParser
        self.CLIParser = CLIParser

    def test_cli_parser_creation(self):
        """Тест создания парсера командной строки"""
        parser = self.CLIParser()
        self.assertIsNotNone(parser)
        self.assertIsNotNone(parser.parser)

        # Проверяем наличие subparsers
        self.assertTrue(hasattr(parser.parser, '_subparsers') or
                        hasattr(parser.parser, '_actions'))

    def test_encrypt_command_args(self):
        """Тест парсинга команды encrypt"""
        parser = self.CLIParser()

        # Тест с минимальными аргументами (симулируем командную строку)
        test_args = [
            'cryptocore', 'encrypt',
            '--key', '00112233445566778899aabbccddeeff',
            '--input', 'test.txt',
            '--output', 'test.enc',
            '--mode', 'cbc'
        ]

        import sys
        original_argv = sys.argv
        try:
            sys.argv = test_args
            args = parser.parse_args()

            self.assertEqual(args.command, 'encrypt')
            self.assertEqual(args.key, '00112233445566778899aabbccddeeff')
            self.assertEqual(args.mode, 'cbc')
            self.assertEqual(args.input, 'test.txt')
            self.assertEqual(args.output, 'test.enc')
            self.assertFalse(args.decrypt)
        finally:
            sys.argv = original_argv

    def test_derive_command_args(self):
        """Тест парсинга команды derive"""
        parser = self.CLIParser()

        test_args = [
            'cryptocore', 'derive',
            '--password', 'test123',
            '--salt', 'a1b2c3d4',
            '--iterations', '100000',
            '--length', '32'
        ]

        import sys
        original_argv = sys.argv
        try:
            sys.argv = test_args
            args = parser.parse_args()

            self.assertEqual(args.command, 'derive')
            self.assertEqual(args.password, 'test123')
            self.assertEqual(args.salt, 'a1b2c3d4')
            self.assertEqual(args.iterations, 100000)
            self.assertEqual(args.length, 32)
            self.assertEqual(args.algorithm, 'pbkdf2')  # default
        finally:
            sys.argv = original_argv

    def test_dgst_command_args(self):
        """Тест парсинга команды dgst"""
        parser = self.CLIParser()

        test_args = [
            'cryptocore', 'dgst',
            '--algorithm', 'sha256',
            '--input', 'file.txt'
        ]

        import sys
        original_argv = sys.argv
        try:
            sys.argv = test_args
            args = parser.parse_args()

            self.assertEqual(args.command, 'dgst')
            self.assertEqual(args.algorithm, 'sha256')
            self.assertEqual(args.input, 'file.txt')
        finally:
            sys.argv = original_argv

    def test_error_handling(self):
        """Тест обработки ошибок парсером"""
        parser = self.CLIParser()

        # Недостаточные аргументы для encrypt
        test_args = ['cryptocore', 'encrypt']  # Нет --key, --input, --output

        import sys
        original_argv = sys.argv
        try:
            sys.argv = test_args
            # parse_args вызовет SystemExit при ошибке
            with self.assertRaises(SystemExit):
                args = parser.parse_args()
        finally:
            sys.argv = original_argv


if __name__ == '__main__':
    unittest.main()