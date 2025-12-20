# tests/unit/test_cli_parser_detailed.py
import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))


class TestCLIParserDetailed(unittest.TestCase):
    """Детальные тесты для cli_parser.py"""

    def setUp(self):
        from src.cli_parser import CLIParser
        self.CLIParser = CLIParser

    def test_all_commands_parsing(self):
        """Тест парсинга всех команд"""
        test_cases = [
            (['encrypt', '--key', '00' * 16, '--input', 'in', '--output', 'out', '--mode', 'gcm'],
             {'command': 'encrypt', 'mode': 'gcm'}),
            (['derive', '--password', 'test', '--salt', 'a1b2'],
             {'command': 'derive', 'password': 'test'}),
            (['dgst', '--algorithm', 'sha256', '--input', 'file.txt'],
             {'command': 'dgst', 'algorithm': 'sha256'}),
        ]

        for args, expected in test_cases:
            with self.subTest(args=args):
                parser = self.CLIParser()

                # Симулируем командную строку
                full_args = ['cryptocore'] + args

                import sys
                original_argv = sys.argv
                try:
                    sys.argv = full_args
                    parsed = parser.parse_args()

                    for key, value in expected.items():
                        self.assertEqual(getattr(parsed, key), value)
                finally:
                    sys.argv = original_argv

    def test_validation_functions_exist(self):
        """Тест существования функций валидации"""
        parser = self.CLIParser()

        # Проверяем наличие приватных методов валидации
        self.assertTrue(hasattr(parser, '_validate_encrypt_args'))
        self.assertTrue(hasattr(parser, '_validate_dgst_args'))
        self.assertTrue(hasattr(parser, '_validate_derive_args'))

    def test_parser_description(self):
        """Тест описания парсера"""
        parser = self.CLIParser()
        self.assertIsNotNone(parser.parser.description)
        self.assertIn('CryptoCore', parser.parser.description)


if __name__ == '__main__':
    unittest.main()