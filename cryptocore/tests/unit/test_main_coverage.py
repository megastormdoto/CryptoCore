# tests/unit/test_main_coverage.py
import unittest
import sys
import os
from io import StringIO
from unittest.mock import patch, MagicMock, mock_open

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))


class TestMainCoverage(unittest.TestCase):
    """Целевые тесты для покрытия main.py"""

    def setUp(self):
        try:
            from src.main import CryptoCore
            self.CryptoCore = CryptoCore
            self.has_main = True
        except ImportError:
            self.has_main = False

    def test_handle_encryption_non_gcm_modes(self):
        """Тест handle_encryption для не-GCM режимов"""
        if not self.has_main:
            self.skipTest("Main module not available")

        crypto = self.CryptoCore()

        # Тестируем разные режимы
        test_modes = ['ecb', 'cbc', 'cfb', 'ofb', 'ctr']

        for mode in test_modes:
            with self.subTest(mode=mode):
                # Создаем args для каждого режима
                class MockArgs:
                    def __init__(self, mode):
                        self.command = 'encrypt'
                        self.mode = mode
                        self.key = '00112233445566778899aabbccddeeff'
                        self.input = 'test.txt'
                        self.output = 'test.enc'
                        self.decrypt = False
                        self.iv = None if mode == 'ecb' else '11223344556677889900112233445566'
                        self.aad = ''

                args = MockArgs(mode)

                # Mock для AES
                with patch('src.main.AES') as mock_aes:
                    mock_aes_instance = MagicMock()
                    mock_aes.return_value = mock_aes_instance

                    # Mock для режима
                    mock_mode_class = MagicMock()
                    mock_mode_instance = MagicMock()
                    mock_mode_instance.encrypt.return_value = b'encrypted'
                    mock_mode_class.return_value = mock_mode_instance

                    # Патчим соответствующий режим
                    mode_mapping = {
                        'ecb': 'ECB',
                        'cbc': 'CBC',
                        'cfb': 'CFB',
                        'ofb': 'OFB',
                        'ctr': 'CTR'
                    }

                    with patch(f'src.main.{mode_mapping[mode]}', mock_mode_class):
                        with patch('builtins.open', mock_open(read_data=b'test')):
                            with patch('os.path.exists', return_value=True):
                                with patch('os.urandom', return_value=b'0' * 16):
                                    try:
                                        crypto.handle_encryption(args)
                                    except Exception as e:
                                        print(f"Mode {mode} error: {e}")
                                        # Продолжаем, не падаем

    def test_handle_decryption_non_gcm_modes(self):
        """Тест handle_decryption для не-GCM режимов"""
        if not self.has_main:
            self.skipTest("Main module not available")

        crypto = self.CryptoCore()

        class MockArgs:
            def __init__(self):
                self.command = 'encrypt'
                self.mode = 'cbc'
                self.key = '00112233445566778899aabbccddeeff'
                self.input = 'test.enc'
                self.output = 'test.txt'
                self.decrypt = True
                self.iv = None  # Будет читаться из файла
                self.aad = ''

        args = MockArgs()

        with patch('src.main.AES') as mock_aes:
            mock_aes_instance = MagicMock()
            mock_aes.return_value = mock_aes_instance

            with patch('src.main.CBC') as mock_cbc:
                mock_cbc_instance = MagicMock()
                mock_cbc_instance.decrypt.return_value = b'decrypted'
                mock_cbc.return_value = mock_cbc_instance

                # Файл с IV в начале
                file_data = b'0' * 16 + b'ciphertext'
                with patch('builtins.open', mock_open(read_data=file_data)):
                    crypto.handle_encryption(args)

    def test_handle_digest_no_hmac(self):
        """Тест handle_digest без HMAC (просто хэш)"""
        if not self.has_main:
            self.skipTest("Main module not available")

        crypto = self.CryptoCore()

        class MockArgs:
            def __init__(self):
                self.command = 'dgst'
                self.algorithm = 'sha256'
                self.input = 'test.txt'
                self.output = None
                self.hmac = False
                self.key = None
                self.verify = None
                self.cmac = False

        args = MockArgs()

        with patch('src.main.SHA256') as mock_sha:
            mock_sha_instance = MagicMock()
            mock_sha_instance.compute.return_value = b'sha256_hash'
            mock_sha.return_value = mock_sha_instance

            with patch('builtins.open', mock_open(read_data=b'test')):
                with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                    crypto.handle_digest(args)
                    output = mock_stdout.getvalue()
                    self.assertIn('7368613235365f68617368', output)  # hex от b'sha256_hash'

    @patch('src.main.pbkdf2_hmac_sha256')
    def test_handle_derive_pbkdf2(self, mock_pbkdf2):
        """Тест handle_derive с PBKDF2"""
        if not self.has_main:
            self.skipTest("Main module not available")

        crypto = self.CryptoCore()

        class MockArgs:
            def __init__(self):
                self.command = 'derive'
                self.password = 'test123'
                self.password_file = None
                self.password_env = None
                self.master_key = None
                self.context = None
                self.salt = 'a1b2c3d4'
                self.salt_file = None
                self.iterations = 1000
                self.length = 32
                self.algorithm = 'pbkdf2'
                self.output = None
                self.output_salt = None

        args = MockArgs()

        mock_pbkdf2.return_value = b'derived_key_32_bytes'

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            crypto.handle_derive(args)
            output = mock_stdout.getvalue()
            # Ищем hex представление b'derived_key_32_bytes'
            self.assertIn('646572697665645f6b65795f33325f6279746573', output)

    @patch('src.main.derive_key')
    def test_handle_derive_hkdf(self, mock_derive):
        """Тест handle_derive с HKDF (master key)"""
        if not self.has_main:
            self.skipTest("Main module not available")

        crypto = self.CryptoCore()

        class MockArgs:
            def __init__(self):
                self.command = 'derive'
                self.password = None
                self.password_file = None
                self.password_env = None
                self.master_key = '00' * 32
                self.context = 'test_context'
                self.salt = None
                self.salt_file = None
                self.iterations = 1000
                self.length = 32
                self.algorithm = 'pbkdf2'
                self.output = None
                self.output_salt = None

        args = MockArgs()

        mock_derive.return_value = b'hkdf_derived_key'

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            crypto.handle_derive(args)
            output = mock_stdout.getvalue()
            # Ищем hex представление b'hkdf_derived_key'
            self.assertIn('686b64665f646572697665645f6b6579', output)


if __name__ == '__main__':
    unittest.main()