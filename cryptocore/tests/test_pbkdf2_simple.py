"""
Simple tests for PBKDF2 implementation.
"""
import unittest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from kdf.pbkdf2 import pbkdf2_hmac_sha256, _is_hex_string


class TestPBKDF2Simple(unittest.TestCase):

    def test_is_hex_string(self):
        """Test hex string detection."""
        self.assertTrue(_is_hex_string('73616c74'))
        self.assertTrue(_is_hex_string('a1b2c3'))
        self.assertTrue(_is_hex_string('ABCDEF'))
        self.assertFalse(_is_hex_string('salt'))
        self.assertFalse(_is_hex_string('hello world'))
        self.assertFalse(_is_hex_string('73 61 6c 74'))  # spaces not allowed

    def test_rfc_6070_vector1(self):
        """Test with RFC 6070 test vector 1."""
        result = pbkdf2_hmac_sha256(
            b'password',
            b'salt',
            1,
            20
        )
        expected = bytes.fromhex('0c60c80f961f0e71f3a9b524af6012062fe037a6')
        self.assertEqual(result, expected)

    def test_hex_salt(self):
        """Test with hex salt string."""
        result = pbkdf2_hmac_sha256(
            'password',
            '73616c74',  # hex for 'salt'
            1,
            20
        )
        expected = bytes.fromhex('0c60c80f961f0e71f3a9b524af6012062fe037a6')
        self.assertEqual(result, expected)

    def test_text_salt(self):
        """Test with text salt string."""
        result = pbkdf2_hmac_sha256(
            'password',
            'salt',  # text string
            1,
            20
        )
        expected = bytes.fromhex('0c60c80f961f0e71f3a9b524af6012062fe037a6')
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()